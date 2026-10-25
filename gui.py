import logging
import queue
import threading
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

import pywhatkit
import schedule

import database
from validation import validate_daily_time, validate_message, validate_recipients

LOG = logging.getLogger(__name__)
logging.basicConfig(
    filename="whatsapp_automation.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)



class WhatsAppAutomationApp:
    """Small Tkinter UI with background scheduling and safe UI-thread updates."""

    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp Automation Tool")
        self.root.geometry("640x560")
        self.root.minsize(520, 420)
        self.jobs = queue.Queue()
        self.stop_event = threading.Event()
        self.scheduler_thread = threading.Thread(
            target=self._scheduler_loop, name="message-scheduler", daemon=True
        )
        database.create_table()
        database.create_contact_table()
        self._build_ui()
        self.scheduler_thread.start()
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def _build_ui(self):
        frame = ttk.Frame(self.root, padding=16)
        frame.pack(fill="both", expand=True)
        ttk.Label(frame, text="WhatsApp Automation", font=("TkDefaultFont", 16, "bold")).pack(anchor="w")
        ttk.Label(frame, text="Use international numbers, e.g. +2547XXXXXXXX").pack(anchor="w", pady=(4, 12))

        ttk.Label(frame, text="Recipients (comma-separated)").pack(anchor="w")
        self.phone_entry = ttk.Entry(frame)
        self.phone_entry.pack(fill="x", pady=(2, 10))

        ttk.Label(frame, text="Message (optional {name} placeholder)").pack(anchor="w")
        self.message_entry = tk.Text(frame, height=6, wrap="word")
        self.message_entry.pack(fill="both", expand=True, pady=(2, 10))

        row = ttk.Frame(frame)
        row.pack(fill="x")
        ttk.Label(row, text="Send daily at (24-hour HH:MM)").pack(side="left")
        self.time_entry = ttk.Entry(row, width=10)
        self.time_entry.insert(0, "09:00")
        self.time_entry.pack(side="left", padx=8)
        ttk.Button(row, text="Schedule", command=self.schedule_messages).pack(side="left")
        ttk.Button(row, text="View logs", command=self.open_logs).pack(side="left", padx=6)
        ttk.Button(row, text="Contacts", command=self.manage_contacts).pack(side="left")

        self.status = tk.StringVar(value="Ready. Scheduled jobs run daily until the app closes.")
        ttk.Label(frame, textvariable=self.status, wraplength=570).pack(anchor="w", pady=(12, 0))

    def schedule_messages(self):
        try:
            recipients = validate_recipients(self.phone_entry.get())
            message = validate_message(self.message_entry.get("1.0", "end-1c"))
            time_text = validate_daily_time(self.time_entry.get())
        except ValueError as exc:
            messagebox.showerror("Check your input", str(exc), parent=self.root)
            return

        if not messagebox.askyesno(
            "Confirm schedule",
            f"Schedule this message daily at {time_text} for {len(recipients)} recipient(s)?\n\n"
            "Confirm that every recipient has consented. This uses unofficial browser automation.",
            parent=self.root,
        ):
            return

        for number in recipients:
            schedule.every().day.at(time_text).do(self._send_message, number, message)
        database.log_message(", ".join(recipients), message, "Scheduled daily at " + time_text)
        self.status.set(f"Scheduled {len(recipients)} recipient(s) daily at {time_text}.")
        LOG.info("Scheduled %d recipient(s) for %s", len(recipients), time_text)

    def _scheduler_loop(self):
        while not self.stop_event.is_set():
            try:
                schedule.run_pending()
            except Exception:
                LOG.exception("Scheduler loop error")
            self.stop_event.wait(1)

    def _send_message(self, phone, template):
        # Called by the scheduler worker, never directly by the Tkinter event loop.
        personalized = template
        try:
            personalized = template.format(name=self._contact_name(phone))
            # This sends immediately when the scheduled job fires. It relies on
            # WhatsApp Web/browser automation and may fail if the session is not ready.
            pywhatkit.sendwhatmsg_instantly(
                phone, personalized, wait_time=20, tab_close=True, close_time=3
            )
            database.log_message(phone, personalized, "Automation submitted; delivery unconfirmed")
            LOG.info("Automation submitted for recipient ending %s", phone[-4:])
            self.jobs.put(("status", f"Automation submitted for recipient ending {phone[-4:]}; delivery is unconfirmed."))
        except Exception as exc:
            try:
                database.log_message(phone, personalized, "Failed: " + str(exc)[:300])
            except Exception:
                LOG.exception("Could not persist failed message outcome")
            LOG.exception("Automation failed for recipient ending %s", phone[-4:])
            self.jobs.put(("error", f"Could not send to recipient ending {phone[-4:]}: {exc}"))
        # Keep the job scheduled daily; the UI explicitly labels this recurring behavior.

    @staticmethod
    def _contact_name(phone):
        try:
            for contact in database.get_contacts():
                if contact[2] == phone:
                    return contact[1]
        except Exception:
            LOG.exception("Could not look up contact name")
        return phone

    def open_logs(self):
        window = tk.Toplevel(self.root)
        window.title("Message Logs")
        window.geometry("760x360")
        listing = tk.Listbox(window, width=110)
        listing.pack(fill="both", expand=True, padx=10, pady=10)
        for row in database.get_logs():
            listing.insert(tk.END, f"{row[4]} | {row[1]} | {row[3]} | {row[2][:100]}")

    def manage_contacts(self):
        window = tk.Toplevel(self.root)
        window.title("Contact Management")
        window.geometry("520x400")
        listing = tk.Listbox(window)
        listing.pack(fill="both", expand=True, padx=10, pady=10)

        def refresh():
            listing.delete(0, tk.END)
            for contact in database.get_contacts():
                listing.insert(tk.END, f"{contact[0]} | {contact[1]} | {contact[2]}")

        def add():
            name = simpledialog.askstring("Add contact", "Contact name:", parent=window)
            if not name or not name.strip():
                return
            phone = simpledialog.askstring("Add contact", "Phone in international format (+254...):", parent=window)
            if not phone:
                return
            try:
                from validation import normalize_phone
                phone = normalize_phone(phone)
                database.add_contact(name.strip(), phone)
                refresh()
            except Exception as exc:
                messagebox.showerror("Could not add contact", str(exc), parent=window)

        def delete():
            selected = listing.curselection()
            if not selected:
                messagebox.showinfo("Select contact", "Select a contact first.", parent=window)
                return
            contact_id = int(listing.get(selected[0]).split("|", 1)[0].strip())
            if messagebox.askyesno("Delete contact", "Delete the selected contact?", parent=window):
                database.delete_contact(contact_id)
                refresh()

        buttons = ttk.Frame(window)
        buttons.pack(fill="x", padx=10, pady=(0, 10))
        ttk.Button(buttons, text="Add", command=add).pack(side="left")
        ttk.Button(buttons, text="Delete selected", command=delete).pack(side="left", padx=6)
        refresh()

    def _poll_worker_messages(self):
        try:
            while True:
                kind, message = self.jobs.get_nowait()
                self.status.set(message)
                if kind == "error":
                    messagebox.showerror("Automation failed", message, parent=self.root)
        except queue.Empty:
            pass
        if not self.stop_event.is_set():
            self.root.after(250, self._poll_worker_messages)

    def close(self):
        self.stop_event.set()
        schedule.clear()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = WhatsAppAutomationApp(root)
    app._poll_worker_messages()
    root.mainloop()

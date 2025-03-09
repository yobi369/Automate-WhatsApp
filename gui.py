import tkinter as tk
from tkinter import messagebox, simpledialog
import pywhatkit as kt
import database
import schedule
import time
import logging

# Set up logging
logging.basicConfig(filename='whatsapp_automation.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WhatsAppAutomationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("WhatsApp Automation Tool")

        # Create input fields
        self.phone_numbers_label = tk.Label(root, text="Phone Numbers (comma separated):")
        self.phone_numbers_label.pack()
        self.phone_numbers_entry = tk.Entry(root, width=50)
        self.phone_numbers_entry.pack()

        self.message_label = tk.Label(root, text="Message:")
        self.message_label.pack()
        self.message_entry = tk.Entry(root, width=50)
        self.message_entry.pack()

        self.personalization_label = tk.Label(root, text="Personalization (e.g., {name}):")
        self.personalization_label.pack()
        self.personalization_entry = tk.Entry(root, width=50)
        self.personalization_entry.pack()

        self.schedule_label = tk.Label(root, text="Schedule Time (HH:MM):")
        self.schedule_label.pack()
        self.schedule_entry = tk.Entry(root, width=20)
        self.schedule_entry.pack()

        self.send_button = tk.Button(root, text="Send Message", command=self.open_log_window)
        self.send_button.pack()
        
        self.view_logs_button = tk.Button(root, text="View Logs", command=self.open_log_window)
        self.view_logs_button.pack()
        
        self.contact_management_button = tk.Button(root, text="Manage Contacts", command=self.manage_contacts)
        self.contact_management_button.pack()
        
        self.view_contacts_button = tk.Button(root, text="View Contacts", command=self.view_contacts)
        self.view_contacts_button.pack()
        
        self.contacts = []  # Initialize an empty list to store contacts

        # Create database tables
        database.create_table()
        database.create_contact_table()

    def open_log_window(self):
        log_window = tk.Toplevel(self.root)
        log_window.title("Message Logs")

        # Create a Listbox to display logs
        self.log_listbox = tk.Listbox(log_window, width=80)
        self.log_listbox.pack()

        # Fetch logs and populate the Listbox
        logs = database.get_logs()
        for log in logs:
            self.log_listbox.insert(tk.END, f"ID: {log[0]}, Phone: {log[1]}, Message: {log[2]}, Status: {log[3]}, Time: {log[4]}")
        
        phone_numbers = self.phone_numbers_entry.get().split(',')
        message = self.message_entry.get()
        schedule_time = self.schedule_entry.get().split(':')
        hour = int(schedule_time[0])
        minute = int(schedule_time[1])

        # Schedule the message
        messagebox.showinfo("Scheduled", "Message has been scheduled!")
        for p_num in phone_numbers:
            schedule.every().day.at(f"{int(hour):02}:{int(minute):02}").do(self.send_message, p_num.strip(), message, hour, minute)

        # Start a background thread to run the scheduler
        self.run_scheduler()

    def view_contacts(self):
        contacts = database.get_contacts()
        contact_window = tk.Toplevel(self.root)
        contact_window.title("Contacts")

        contact_listbox = tk.Listbox(contact_window, width=50)
        contact_listbox.pack()

        for contact in contacts:
            contact_listbox.insert(tk.END, f"{contact[1]}: {contact[2]}")  # Name: Phone Number

    def add_contact(self):
        contact_name = simpledialog.askstring("Input", "Enter contact name:")
        if contact_name:
            self.contacts.append(contact_name)
            self.contact_listbox.insert(tk.END, contact_name)

    def send_message(self, p_num, message, hour, minute):
        try:
            personalized_message = message.format(name=p_num.strip())
            kt.sendwhatmsg(p_num.strip(), personalized_message, hour, minute)
            messagebox.showinfo("Success", f"Message sent to {p_num.strip()} at {hour}:{minute} with message: {personalized_message}")
            database.log_message(p_num.strip(), personalized_message, "Sent")
            logging.info(f"Message sent to {p_num.strip()} at {hour}:{minute} with message: {personalized_message}")
        except Exception as e:
            logging.error(f"Failed to send message to {p_num.strip()}: {e}")
            messagebox.showerror("Error", f"Failed to send message to {p_num.strip()}: {e}")

    def manage_contacts(self):
        self.contact_window = tk.Toplevel(self.root)
        self.contact_window.title("Contact Management")

        self.contact_label = tk.Label(self.contact_window, text="Contacts:")
        self.contact_label.pack()

        self.contact_listbox = tk.Listbox(self.contact_window)
        self.contact_listbox.pack()

        self.add_contact_button = tk.Button(self.contact_window, text="Add Contact", command=self.add_contact)
        self.add_contact_button.pack()

        self.delete_contact_button = tk.Button(self.contact_window, text="Delete Contact", command=self.delete_contact)
        self.delete_contact_button.pack()

        self.load_contacts()

    def delete_contact(self):
        selected_contact_index = self.contact_listbox.curselection()
        if selected_contact_index:
            contact_id = self.contacts[selected_contact_index[0]][0]  # Assuming the first element is the ID
            database.delete_contact(contact_id)
            self.contact_listbox.delete(selected_contact_index)
            messagebox.showinfo("Success", "Contact deleted successfully.")
        else:
            messagebox.showwarning("Warning", "Please select a contact to delete.")

    def run_scheduler(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

if __name__ == "__main__":
    root = tk.Tk()
    app = WhatsAppAutomationApp(root)
    root.mainloop()

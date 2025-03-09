'''
#import the necessary module!
import pywhatkit as kt
import getpass as gp
import time
import logging
import csv

# Set up logging
logging.basicConfig(filename='whatsapp_automation.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Function to send messages
def send_whatsapp_message(phone_numbers, message, schedule_times):
    for i, p_num in enumerate(phone_numbers):
        try:
            kt.sendwhatmsg(p_num, message, schedule_times[i][0], schedule_times[i][1])
            logging.info(f"Message sent to {p_num} at {schedule_times[i][0]}:{schedule_times[i][1]}")
            print(f"Message sent to {p_num} at {schedule_times[i][0]}:{schedule_times[i][1]}")
        except Exception as e:
            logging.error(f"Failed to send message to {p_num}: {e}")
            print(f"Failed to send message to {p_num}: {e}")

# Function to capture user input
def capture_user_input():
    print("Let's Automate WhatsApp!")
    p_nums = input("Enter phone numbers separated by commas: ").split(',')
    p_nums = [num.strip() for num in p_nums]
    
    # Allow user to select a message template or enter a custom message
    templates = {
        "1": "Hello, this is a message from my automation script!",
        "2": "Reminder: Your appointment is scheduled for tomorrow.",
        "3": "Thank you for your support!"
    }
    
    print("Select a message template:")
    for key, value in templates.items():
        print(f"{key}: {value}")
    
    template_choice = input("Enter the template number or type your custom message: ")
    if template_choice in templates:
        msg = templates[template_choice]
    else:
        msg = template_choice  # Custom message
    
    schedule_times = []
    for i in range(len(p_nums)):
        hour = int(input(f"Enter hour to send message to {p_nums[i]}: "))
        minute = int(input(f"Enter minute to send message to {p_nums[i]}: "))
        schedule_times.append((hour, minute))
    
    return p_nums, msg, schedule_times

# Function to load contacts from a CSV file
def load_contacts_from_csv(file_path):
    phone_numbers = []
    messages = []
    with open(file_path, mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            phone_numbers.append(row[0])  # Assuming phone numbers are in the first column
            messages.append(row[1])  # Assuming messages are in the second column
    return phone_numbers, messages

# Main execution
if __name__ == "__main__":
    phone_numbers, message, schedule_times = capture_user_input()
    send_whatsapp_message(phone_numbers, message, schedule_times)
'''

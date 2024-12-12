import schedule
import time
from db_operations import get_all_data
from send_email import send_email
import threading
import re

def is_valid_email(email):
    # Regular expression to validate an email address
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None



def job():
    records = get_all_data()
    counter = 0
    for record in records:
        email = record.get('email')
        if email and is_valid_email(email) and record:
            try:    
                send_email(record)
                print(f'email sent to {email}')
                counter += 1
            except Exception as e:
                print(f"Failed to send email to {email}. Error: {e}")
                    
        else:
            print(f"Invalid email address: {email}")
            



job_id=schedule.every().day.at("07:00").do(job)

def run_scheduler():
    while True:
        schedule.run_pending()
        print("Scheduler running...")
        time.sleep(1)        

scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
scheduler_thread.start()


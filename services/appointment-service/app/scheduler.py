from apscheduler.schedulers.background import BackgroundScheduler
from app.reminders import send_reminders

def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_reminders, 'interval', hours=1)  # Run every hour
    scheduler.start()

import time
import threading
import smtplib
import os
from datetime import datetime, timedelta, timezone
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import Config
from utils import supabase, get_supabase_admin

def send_email(to_email, subject, html_body):
    """Sends an email using the SMTP configuration."""
    if not Config.SMTP_EMAIL or not Config.SMTP_PASSWORD:
        print("SMTP not configured. Skipping email.")
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = f"DIGIANCHORZ <{Config.SMTP_EMAIL}>"
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(html_body, "html"))

        # Gmail Settings (Standard for this project context)
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(Config.SMTP_EMAIL, Config.SMTP_PASSWORD)
        server.sendmail(Config.SMTP_EMAIL, to_email, msg.as_string())
        server.quit()
        print(f"Email sent to {to_email}: {subject}")
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {e}")
        return False

def check_task_deadlines():
    """Checks for upcoming and overdue deadlines."""
    print("Checking task deadlines...")
    
    try:
        # We need the service role to read all tasks/users without RLS issues in background
        admin_client = get_supabase_admin() or supabase
        
        # Fetch non-completed tasks with a deadline
        # Note: We need to filter manually if logic is complex, or use simple filters
        # Assuming 'tasks' table has 'reminder_sent' and 'overdue_notified' columns.
        
        # 1. Fetch relevant tasks
        try:
             res = admin_client.table("tasks").select("*").neq("status", "Completed").not_.is_("deadline", "null").execute()
             tasks = res.data
        except Exception as e:
            print(f"Error fetching tasks: {e}")
            return

        if not tasks:
            return

        now = datetime.now()
        
        for task in tasks:
            try:
                # Parse deadline (Assuming ISO format)
                deadline_str = task['deadline']
                # Handle simplified parsing
                deadline = datetime.fromisoformat(deadline_str.replace('Z', '+00:00'))
                # Ensure 'now' is offset-aware UTC
                current_time = datetime.now(timezone.utc)
                
                # Check if deadline is offset-naive, assume UTC if so (Supabase default)
                if deadline.tzinfo is None:
                    deadline = deadline.replace(tzinfo=timezone.utc)
                
                time_diff = deadline - current_time
                hours_remaining = time_diff.total_seconds() / 3600
                
                print(f"[Scheduler] Task {task['id']} | Due: {deadline} | Now: {current_time} | Hours Left: {hours_remaining:.2f}")

                # --- 12 Hour Warning ---
                # Criteria: Between 0 and 12 hours remaining, and not yet reminded
                if 0 < hours_remaining <= 12 and not task.get('reminder_sent'):
                    # Send In-App Notification
                    user_id = task.get('assigned_to')
                    if user_id:
                        title = "Deadline Approaching"
                        message = f"Task '{task.get('title')}' is due in less than 12 hours."
                        
                        # Insert Notification
                        admin_client.table("notifications").insert({
                            "user_id": user_id,
                            "title": title,
                            "message": message,
                            "link": f"/projects/{task.get('project_id')}"
                        }).execute()
                        
                        # Mark as reminded
                        admin_client.table("tasks").update({"reminder_sent": True}).eq("id", task['id']).execute()
                        print(f"Sent 12h warning for task {task['id']}")

                # --- Overdue Email ---
                # Criteria: Deadline passed (negative time_diff) and not yet notified
                elif hours_remaining < 0 and not task.get('overdue_notified'):
                    # User asked for: "email notification about task deadline is crossed"
                    user_id = task.get('assigned_to')
                    
                    if user_id:
                        # Fetch User Email
                        u_res = admin_client.table("users").select("email, full_name").eq("id", user_id).single().execute()
                        user_data = u_res.data
                        
                        if user_data and user_data.get('email'):
                            subject = f"OVERDUE: Task '{task.get('title')}' Deadline Crossed"
                            body = f"""
                            <h3>Task Overdue Alert</h3>
                            <p>Hello {user_data.get('full_name')},</p>
                            <p>The deadline for the task <strong>{task.get('title')}</strong> has passed.</p>
                            <p><strong>Deadline:</strong> {deadline_str}</p>
                            <p>Please update the status or contact your manager.</p>
                            <br>
                            <a href="{os.getenv('BASE_URL', 'http://127.0.0.1:5000')}/projects/{task.get('project_id')}">View Task</a>
                            """
                            if send_email(user_data['email'], subject, body):
                                # Mark as notified
                                admin_client.table("tasks").update({"overdue_notified": True}).eq("id", task['id']).execute()
                                print(f"Sent overdue email for task {task['id']}")

            except Exception as inner_e:
                print(f"Error processing task {task.get('id')}: {inner_e}")
                continue

    except Exception as e:
        print(f"Scheduler Error: {e}")

def start_scheduler():
    def run_job():
        while True:
            check_task_deadlines()
            # Sleep for 60 seconds (1 minute) for better responsiveness
            time.sleep(60)

    # Daemon thread to run in background
    thread = threading.Thread(target=run_job, daemon=True)
    thread.start()
    print("Scheduler started (60s interval).")

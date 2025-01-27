import sqlite3
from models.job import Job

def initialize_db():
    """Initialize the database and create the jobs table if it doesn't exist."""
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            contact_name TEXT,
            position TEXT,
            email TEXT,
            company_website TEXT,
            company_address TEXT,
            application_date TEXT,
            cover_letter_sent INTEGER,
            interview_date TEXT,
            how_did_you_find_them TEXT,
            resume TEXT,
            notes TEXT,
            application TEXT,
            cover_letter TEXT,
            application_status TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_job(job: Job):
    """Save a job application to the database."""
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO jobs (
            company, contact_name, position, email, company_website, company_address,
            application_date, cover_letter_sent, interview_date, how_did_you_find_them,
            resume, notes, application, cover_letter, application_status
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        job.company, job.contact_name, job.position, job.email, job.company_website,
        job.company_address, job.application_date, job.cover_letter_sent, job.interview_date,
        job.how_did_you_find_them, job.resume, job.notes, job.application, job.cover_letter, job.application_status
    ))
    conn.commit()
    conn.close()
    
def fetch_all_jobs():
    """Fetch all job records from the database."""
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs")
    data = cursor.fetchall()
    conn.close()
    return data

def update_application_status(job_id, new_status):
    """Update the application status for a specific job."""
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE jobs SET application_status = ? WHERE id = ?",
        (new_status, job_id)
    )
    conn.commit()
    conn.close()


def fetch_application_data():
    """Fetch application data from the database."""
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT application_status, COUNT(*) FROM jobs GROUP BY application_status")
    data = cursor.fetchall()
    conn.close()
    return data

def fetch_application_stat():
    conn = sqlite3.connect('jobs.db')
    cursor = conn.cursor()
    cursor.execute("SELECT application_date, COUNT(*) FROM jobs GROUP BY application_date ORDER BY application_date")
    data = cursor.fetchall()
    conn.close()
    return data 


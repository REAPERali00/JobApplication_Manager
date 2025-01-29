# Job Application Manager

## Description

This application helps users track their job applications efficiently. It simplifies the process by:

- Generating folders for each job application.
- Automatically adding both the resume and cover letter to the job folder.
- Storing job application data in a local SQLite database.
- Generating charts to monitor daily application goals and response rates.
- Providing a database view where users can see and update application statuses.

## Demo

![Video Demo](/home/alireza/Documents/Git-Resume/JobApplication_Manager/assets/jobapp_demo.mp4)

## Features

- [ ] Add GPT API integration?
- add docker file
- [x] View page for the database, including charts for application rate and reply rate.
- [x] Frequency analyzer to track application activity and send reminders.
- [x] Dropdown selection for job type in the Tkinter UI.
- [x] SQLite database functionality for storing job applications.
- [x] Dedicated section for writing cover letters.
- [x] Create only the final AI prompt instead of using the entire prompt folder.
- [x] Category selection for choosing the correct resume type when creating a job folder.
- [x] Improved folder naming convention (`Company_JobTitle`).

## Dependencies

Make sure you have these installed:

- Python
- SQLite

## Setup Instructions

1. **Clone the GitHub repository:**

   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. **Remove the `.git` folder** (optional if you don't want Git tracking the cloned repo):

   ```bash
   rm -rf .git  # Mac/Linux
   rmdir /s /q .git  # Windows
   ```

3. **Create a virtual environment:**

   ```bash
   python -m venv .venv
   ```

4. **Activate the virtual environment:**

   ```bash
   # Windows
   .venv\Scripts\activate

   # Mac/Linux
   source .venv/bin/activate
   ```

5. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

6. **Prepare your documents:**

   - Place your resumes in the `Resume/resume_types/` folder.
   - Replace the default cover letter with your own.

7. **Run the application:**

   ```bash
   python3 ./src/App.py
   ```

   You can also use the `run.sh` script to run the application

   ```bash
   chmod +x ./run.sh
   ./run.sh
   ```

## How to Use

1. Copy and paste the job description into the application text box.
2. Write a summary of your cover letter in the designated field.
3. A new folder will automatically appear in the `Submissions/` directory containing:

   - Your resume
   - Your cover letter
   - The generated AI prompt

4. Customize the AI prompt by modifying `./cache/prompts.txt`.

# Description

This git repo is made to make creating cv and tracking job applications easier and quicker. Bellow you can find a quick guide on what each folder and script is for:

- Defaults: This is where default resume and cover letter will go, this folder will be copied to each new job folder
  - Prompt: this subfolder is where the script generator will go
- Submissions: This is the folder that each job application will be created in, and the folder name will be the company name
- cd_ui: This is the ui, to enter the job information
- makeCv: this adds data to the excel file, and creates the job applicatiuon folder in Submissions
- Job_list.xlsx: this keeps track of the job application

# TODO

- [ ] add gpt api?
- [x] add view page for database, with charts for the application rate a nd reply rate
- [x] a frequency analyzer, to see how often I am applying and get reminders
- [x] add type selection drop down to tkinter
- [x] add database functionality (store in sqlite)
- [x] a large section to write cover letter
- [x] instead of using the entire prompt folder, just create the final prompt
- [x] a category selection option, to choose a resume type to copy when creating doc
- [x] a better naming sense for folders, maybe company+job?

## Start up

- clone the git hub repositiory
- Delete the .git folder
- Clear the job_list file to start tracking yours
- Delete the folders in Submissions
- install python venv: `python -m venv venv`
- activate the venv script:

```bash
venv\Scripts\activate #Windows
source venv/bin/activate #Mac/Linux
```

- Install dependencies: `pip install -r requirements.txt`
- run the project: `python cd_ui.py`

## Adding a job

## Generating script

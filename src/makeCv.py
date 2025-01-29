import os
import shutil
import PyPDF2
from models.job import Job


"""
TODO: 
    add the job data to a database 
    add content to cache 
    grab content from cache, generate prompt and put it in job folder
"""


def get_resume(directory="Resume/resume_types/"): 
    if not os.path.exists(directory): 
        print("could not find resume directory")
        exit(1)
    res = [os.path.splitext(file)[0] for file in os.listdir(directory) if file.endswith(".pdf")]
    return res

def read_file(file_path):
    """Reads the content of a file."""
    with open(file_path, "r") as f:
        return f.read()

def write_file(file_path, content):
    """Writes content to a file."""
    with open(file_path, "w") as f:
        f.write(content)

def convert_pdf_to_text(pdf_path):
    """Converts a PDF to plain text."""
    text = ""
    if os.path.exists(pdf_path) and pdf_path.endswith(".pdf"):
        with open(pdf_path, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            for page in pdf_reader.pages:
                text += page.extract_text()
    return text

def generate_prompt(job:Job, application_path, cover_letter_path, final_prompt_path, prompts_path, resume_path):
    """Generate the final prompt by replacing placeholders in the template."""
    # Dynamically read all file contents
    files_content = {
        "application": read_file(application_path),
        "cover_letter": read_file(cover_letter_path),
        "resume": read_file(resume_path),
        "prompts": read_file(prompts_path),
        "role": job.position, 
        "company": job.company,
    }

    # Replace placeholders
    final_prompt_content = (
        files_content["prompts"]
        .replace("[resume]", files_content["resume"] or "")
        .replace("[application]", files_content["application"] or "")
        .replace("[cover]", files_content["cover_letter"] or "")
        .replace("[role]", files_content["role"] or "")
        .replace("[company]", files_content["company"] or "")
    )

    # Write the final prompt
    write_file(final_prompt_path, final_prompt_content)

def write_cache(job: Job):
    """Write all job data to the cache folder."""
    cache_loc = "cache"
    os.makedirs(cache_loc, exist_ok=True)

    # Define cache file paths
    cache_files = {
        "application": os.path.join(cache_loc, "application.txt"),
        "cover_letter": os.path.join(cache_loc, "cover_letter.txt"),
        "final_prompt": os.path.join(cache_loc, "final_prompt.txt"),
        "prompts": os.path.join(cache_loc, "prompts.txt"),
        "resume": os.path.join(cache_loc, "resume.txt"),
    }

    # Write job data to cache
    write_file(cache_files["application"], job.application or "")
    write_file(cache_files["cover_letter"], job.cover_letter or "")

    # Convert resume PDF to text and save
    resume_pdf_path = os.path.join("Resume", "resume_types", f"{job.resume}.pdf")
    resume_text = convert_pdf_to_text(resume_pdf_path)
    write_file(cache_files["resume"], resume_text)

    # Generate the final prompt
    generate_prompt(
        job=job,
        application_path=cache_files["application"],
        cover_letter_path=cache_files["cover_letter"],
        final_prompt_path=cache_files["final_prompt"],
        prompts_path=cache_files["prompts"],
        resume_path=cache_files["resume"],
    )

def submission_folder(job: Job):
    """Create the submission folder and copy necessary files."""
    folder_name = f"{job.company}_{job.position}"
    folder = os.path.join("Submissions", folder_name)
    files_location = "Resume"
    cv = os.path.join(files_location, "Coverletter.docx")
    prompt = os.path.join("cache", "final_prompt.txt")
    resume = None

    if os.path.exists(folder):
        print("Folder already exists")
        return
    os.mkdir(folder)

    # Find the matching resume
    for file in os.listdir(os.path.join(files_location, "resume_types")):
        if file.startswith(job.resume) and file.endswith(".pdf"):
            resume = os.path.join(files_location, "resume_types", file)

    if not resume or not os.path.exists(cv):
        print("Could not find resume or cover letter")
        return

    # Copy files to the submission folder
    shutil.copy(resume, folder)
    shutil.copy(cv, folder)
    shutil.copy(prompt, folder)
    print(f"Submission folder created at: {folder}")

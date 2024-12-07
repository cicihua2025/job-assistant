from flask import Flask, render_template, request, jsonify
import openai
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from fpdf import FPDF
from docx import Document

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Ensure static directory exists
STATIC_DIR = app.static_folder
os.makedirs(STATIC_DIR, exist_ok=True)

# Function to extract text from a PDF file
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text.strip()

# Analyze Job Posting Function
def analyze_job_post(job_post):
    """Analyzes a job posting for key skills and responsibilities."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use "gpt-4" if preferred
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"Analyze this job posting for key skills and responsibilities: {job_post}"}
            ],
            max_tokens=150
        )
        return {"analysis": response.choices[0].message['content'].strip()}
    except Exception as e:
        return {"error": f"Failed to analyze job posting: {str(e)}"}

# Tailor Resume Function
def tailor_resume(job_post, resume, file_format):
    """Tailors the resume based on the job posting and saves it as a PDF or Word document."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert resume coach."},
                {"role": "user", "content": f"Tailor this resume to better match this job posting:\n\nJob Posting:\n{job_post}\n\nResume:\n{resume}"}
            ],
            max_tokens=300
        )
        tailored_resume = response.choices[0].message['content'].strip()

        # Save tailored resume as PDF or Word
        if file_format == "pdf":
            output_file = "tailored_resume.pdf"
            file_path = os.path.join(STATIC_DIR, output_file)

            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)
            pdf.multi_cell(0, 10, tailored_resume)
            pdf.output(file_path)
        elif file_format == "word":
            output_file = "tailored_resume.docx"
            file_path = os.path.join(STATIC_DIR, output_file)

            doc = Document()
            doc.add_paragraph(tailored_resume)
            doc.save(file_path)
        else:
            raise ValueError("Invalid file format selected")

        return {"tailored_resume": tailored_resume, "download_link": f"/static/{output_file}"}
    except Exception as e:
        return {"error": f"Failed to tailor resume: {str(e)}"}

# Prepare Interview Function
def prepare_interview(job_post, resume):
    """Generates interview questions and tips."""
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert interview coach."},
                {"role": "user", "content": f"Based on the job posting and resume, generate interview questions and preparation tips:\n\nJob Posting:\n{job_post}\n\nResume:\n{resume}"}
            ],
            max_tokens=200
        )
        return {"interview_questions": response.choices[0].message['content'].strip()}
    except Exception as e:
        return {"error": f"Failed to prepare interview: {str(e)}"}

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def process():
    task = request.form.get("task")
    job_post = request.form.get("job_post")
    file_format = request.form.get("file_format")

    # Handle file upload
    uploaded_file = request.files.get("resume_file")
    if uploaded_file and uploaded_file.filename.endswith(".pdf"):
        resume = extract_text_from_pdf(uploaded_file)
    else:
        resume = request.form.get("resume")

    if not job_post or not resume:
        return jsonify({"error": "Job posting and resume are required!"})

    # Call the appropriate function based on the selected task
    if task == "analyze":
        response = analyze_job_post(job_post)
    elif task == "tailor":
        response = tailor_resume(job_post, resume, file_format)
    elif task == "interview":
        response = prepare_interview(job_post, resume)
    else:
        response = {"error": "Invalid task selected!"}

    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

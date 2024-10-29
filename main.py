import re
from openai import OpenAI
from dotenv import load_dotenv
import os
import PyPDF2

# Load environment variables
load_dotenv()

# Get OpenAI API key from environment variables
openai_api_key = os.getenv("OPENAI_API_KEY")
openai = OpenAI(api_key=openai_api_key)

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_file_path):
    with open(pdf_file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text


# Read the job description from a text file
with open("job_description.txt", "r") as file:
    job_description = file.read()

# Extract text from the resume PDF
resume_text = extract_text_from_pdf("Bradley_Allen_Resume.pdf")

# Define additional roles and cover letter structure for OpenAI
role_description = (
    "You are a cover letter generator with 20 years of experience. Your task is to create a professional and concise cover letter."
)
cover_letter_structure = (
    "To compose a compelling cover letter, you must scrutinize the job description for key qualifications. "
    "Begin with a succinct introduction about the candidate's identity and career goals. "
    "Highlight skills aligned with the job, underpinned by tangible examples. "
    "Incorporate details about the company, emphasising its mission or unique aspects that align with the candidate's values. "
    "Conclude by reaffirming the candidate's suitability, inviting further discussion. "
    "Do not make anything up, but feel free to use neighboring examples based on my resume. "
    "Use job-specific terminology for a tailored and impactful letter, maintaining a professional style suitable for the job role. "
    "Use the company name."
    "Please provide your response in under [250] words."  # Limit to ensure it's concise
)

# Combine job description and resume for OpenAI input
content = (
    f"{role_description}\n\n{cover_letter_structure}\n\n"
    f"Job Description:\n{job_description}\n\n"
    f"Resume:\n{resume_text}"
)

# Request completion from OpenAI with system role
response = openai.chat.completions.create(
    messages=[
        {"role": "system", "content": role_description},
        {"role": "user", "content": content}
    ],
    model="gpt-3.5-turbo",
)

# Extract the generated cover letter
cover_letter = response.choices[0].message.content

# Dynamically generate the file name
candidate_name = "Bradley Allen"  # Replace with actual candidate name
output_filename = f"meat.txt"

# Write the cover letter to a text file
with open(output_filename, "w") as text_file:
    text_file.write(cover_letter)

print(f"Cover letter saved to {output_filename}")

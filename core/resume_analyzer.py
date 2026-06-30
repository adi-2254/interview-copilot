from pypdf import PdfReader
from .llm import chat_json

def extract_resume_text(uploaded_file) -> str:
    """Extract clear text from a PDF file object."""
    reader = PdfReader(uploaded_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def analyze_gaps(resume_text: str, job_dict: dict) -> dict:
    """Analyze missing skills, tech stack, and experience gaps."""
    system = (
        "You are an expert technical recruiter. Compare the candidate's resume "
        "against the job description. Identify what is missing or weak. "
        "Return a JSON object with keys: matched_skills (list), missing_skills (list), "
        "missing_tech (list), recommendations (list)."
    )
    user = (
        f"Job Details:\nRole: {job_dict.get('role')}\nTech Stack: {job_dict.get('tech_stack')}\n"
        f"Required Skills: {job_dict.get('required_skills')}\n\n"
        f"Candidate Resume Text:\n{resume_text}"
    )
    return chat_json(system, user)
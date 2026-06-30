from .llm import chat_json

def research_company(company_name: str, role: str) -> str:
    """Simulates real-world company context/pain points for target roles."""
    if not company_name or company_name.lower() == "unknown":
        return "Generic modern tech company scale and architecture constraints."
    
    system = "You are an industry researcher. Identify 2 key engineering or operational focuses for this company."
    user = f"Company: {company_name}\nRole: {role}\nWhat are their likely engineering priorities or stack dynamics?"
    
    # Simple text fallback using chat_json wrapped as a string field if needed, 
    # or just use standard generation for brief context notes.
    res = chat_json(system, f"Provide a brief summary for {company_name} hiring for {role}. Return JSON with key 'summary'.")
    return res.get("summary", "")

def generate_questions(job: dict, resume_text: str = "", n_behavioral=3, n_technical=3) -> list[dict]:
    company = job.get('company_name', 'the company')
    company_context = research_company(company, job.get('role', 'Software Engineer'))
    
    system = (
        "You are a senior technical interviewer. Generate interview questions weighted "
        "toward the role's actual requirements and the company's real-world constraints. "
        "If resume text is provided, tailor questions to probe potential gaps or deep experience areas. "
        "Return JSON format: "
        '{"questions": [{"text": str, "type": "behavioral"|"technical", "competency": str}]}'
    )
    
    user = (
        f"Company Name: {company}\n"
        f"Company Context: {company_context}\n"
        f"Role: {job.get('role')} ({job.get('seniority')})\n"
        f"Tech stack: {', '.join(job.get('tech_stack', []))}\n"
        f"Key skills: {', '.join(job.get('required_skills', []))}\n"
    )
    if resume_text:
        user += f"\nCandidate Resume Context (Probe gaps here): {resume_text[:4000]}"
        
    user += f"\nGenerate exactly {n_behavioral} behavioral and {n_technical} technical questions."
    
    return chat_json(system, user)["questions"]
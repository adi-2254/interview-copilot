import requests
from bs4 import BeautifulSoup
from .llm import chat_json

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; InterviewCopilot/1.0)"}

def fetch_raw_text(url: str) -> str:
    """Scrapes raw web page text and strips away headers, footers, and styles."""
    if not url:
        return ""
    r = requests.get(url, headers=HEADERS, timeout=15)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    text = " ".join(soup.get_text(separator=" ").split())
    return text[:8000]  # Caps token volume to preserve context windows

def parse_job(raw_text: str) -> dict:
    """Transforms unformatted job page strings into cleanly structured JSON parameters."""
    system = (
        "You extract structured data from a job posting. "
        "Return a clean JSON object with keys: role, seniority, tech_stack (list), "
        "required_skills (list), responsibilities (list), company_name."
    )
    return chat_json(system, f"Job posting text:\n{raw_text}")
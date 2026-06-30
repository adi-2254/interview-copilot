# 🎯 Interview Prep Copilot

An AI-powered, closed-loop interview simulator designed to automate rigorous preparation for software engineering roles. 

Instead of relying on generic question banks, Interview Copilot dynamically generates a tailored mock interview experience by cross-referencing live job descriptions with your personal resume. It identifies skill gaps, simulates realistic technical and behavioral grilling, and provides real-time, rubric-based feedback.

## ✨ Core Features

*   **Job Specification Extraction:** Scrapes and parses target job postings (via URL or raw text) to extract required tech stacks, responsibilities, and seniority levels using a structured LLM pipeline.
*   **Resume Gap Analysis:** Ingests PDF resumes, extracts text, and runs a comparative analysis against the parsed job description to highlight matched skills, missing core tech, and preparation recommendations.
*   **Contextual Question Generation:** Synthesizes the company's real-world engineering constraints, job requirements, and resume gaps to generate highly specific technical and behavioral questions.
*   **Voice-Native Interface:** Integrates OpenAI's Whisper API for seamless, timed voice responses, simulating the pressure of a real verbal interview.
*   **Automated Evaluation Engine:** Scores responses based on clarity, technical accuracy, and structural frameworks (like the STAR method). Provides a numeric breakdown, identifies strengths/weaknesses, and generates an optimized "Rewritten Answer."
*   **Progress Analytics:** Persists evaluation data locally via SQLite, surfacing weak areas and competency trends over time in a dedicated dashboard.

## 🛠️ Architecture & Tech Stack

*   **Frontend:** [Streamlit](https://streamlit.io/) (including `st.audio_input` for native voice capture)
*   **Intelligence Layer:** OpenAI API (`gpt-4o-mini` for JSON-guaranteed structured data extraction, `whisper-1` for audio transcription)
*   **Web Scraping:** `BeautifulSoup4`, `requests`
*   **Document Processing:** `pypdf`
*   **Data Persistence:** SQLite3

## ⚙️ Local Setup & Installation

**1. Clone the repository**
```bash
git clone [https://github.com/adi-2254/interview-copilot.git](https://github.com/adi-2254/interview-copilot.git)
cd interview-copilot

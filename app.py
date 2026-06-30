import streamlit as st
from core.scraper import fetch_raw_text, parse_job
from core.question_gen import generate_questions
from core.feedback import score_answer
from core.resume_analyzer import extract_resume_text, analyze_gaps
from core.llm import transcribe_audio
import db

st.set_page_config(page_title="Interview Prep Copilot", page_icon="🎯", layout="wide")
db.init_db()

# Initialize Session States
for key in ["job", "questions", "idx", "resume_text", "gap_analysis"]:
    st.session_state.setdefault(key, None)

st.title("🎯 Interview Prep Copilot")

tab_setup, tab_resume, tab_practice, tab_progress = st.tabs(
    ["1. Job Setup", "2. Resume Analyzer", "3. Practice Arena", "4. Progress Dashboard"]
)

# --- TAB 1: JOB SETUP ---
with tab_setup:
    st.subheader("Target Job Profile")
    url = st.text_input("Job posting URL (optional)")
    pasted = st.text_area("...or paste the job description here", height=150)

    if st.button("Analyze Job Description", type="primary"):
        with st.spinner("Processing job metadata..."):
            try:
                raw = fetch_raw_text(url) if url and not pasted else pasted
            except Exception:
                st.warning("Couldn't scrape the URL automatically. Parsing fallback pasted text.")
                raw = pasted
            
            if raw and raw.strip():
                st.session_state.job = parse_job(raw)
                st.success(f"Successfully loaded role: {st.session_state.job.get('role', 'Unknown')} at {st.session_state.job.get('company_name', 'Unknown')}")
                st.rerun()

    if st.session_state.job:
        st.json(st.session_state.job)

# --- TAB 2: RESUME ANALYZER ---
with tab_resume:
    st.subheader("Resume Gap Analysis")
    if not st.session_state.job:
        st.info("⚠️ Please complete the Job Setup step first to analyze your resume against specifications.")
    else:
        uploaded_file = st.file_uploader("Upload your resume (PDF format)", type=["pdf"])
        if uploaded_file:
            if st.button("Run Match Analysis"):
                with st.spinner("Analyzing resume against job parameters..."):
                    resume_txt = extract_resume_text(uploaded_file)
                    st.session_state.resume_text = resume_txt
                    st.session_state.gap_analysis = analyze_gaps(resume_txt, st.session_state.job)
                    
                    # Generate highly custom questions based on both Job AND Resume Context
                    st.session_state.questions = generate_questions(
                        st.session_state.job, 
                        resume_text=st.session_state.resume_text
                    )
                    st.session_state.idx = 0
                    st.success("Analysis complete! Tailored questions generated.")
        
        if st.session_state.gap_analysis:
            ga = st.session_state.gap_analysis
            col1, col2 = st.columns(2)
            with col1:
                st.success("🟢 **Matched Qualifications**")
                st.write(", ".join(ga.get("matched_skills", [])))
                st.warning("🟡 **Missing Core Tech Stack**")
                st.write(", ".join(ga.get("missing_tech", [])))
            with col2:
                st.error("🔴 **Missing Skills / Experience Gaps**")
                st.write(", ".join(ga.get("missing_skills", [])))
                st.info("💡 **Preparation Recommendations**")
                for rec in ga.get("recommendations", []):
                    st.markdown(f"- {rec}")

# --- TAB 3: PRACTICE ARENA ---
with tab_practice:
    # Build fallback base questions if user decided to skip the resume upload phase
    if st.session_state.job and not st.session_state.questions:
        if st.button("Generate Generic Role Questions (No Resume)"):
            st.session_state.questions = generate_questions(st.session_state.job)
            st.session_state.idx = 0
            st.rerun()

    qs = st.session_state.questions
    if not qs:
        st.info("Please set up your Job criteria and Resume profiles to start practicing.")
    else:
        i = st.session_state.idx
        q = qs[i]
        
        st.caption(f"Question {i+1} of {len(qs)} · Type: {q['type'].upper()} · Domain: {q['competency']}")
        st.markdown(f"### **{q['text']}**")
        
        # Input choice selection
        input_mode = st.radio("Choose response format:", ["Voice Input", "Text Editor"], horizontal=True)
        
        final_answer = ""
        if input_mode == "Voice Input":
            audio_data = st.audio_input("Record your spoken answer:", key=f"audio_{i}")
            if audio_data:
                with st.spinner("Transcribing your audio input using Whisper..."):
                    # Use unique state key to avoid transcription re-runs on layout updates
                    if f"transcription_{i}" not in st.session_state:
                        st.session_state[f"transcription_{i}"] = transcribe_audio(audio_data)
                    final_answer = st.session_state[f"transcription_{i}"]
                    st.info(f"**Transcribed Script:** {final_answer}")
        else:
            final_answer = st.text_area("Type your technical response here:", key=f"text_{i}", height=150)
            
        if st.button("Evaluate Performance", type="primary") and final_answer.strip():
            with st.spinner("Scoring parameters via Interview Engine..."):
                fb = score_answer(q, final_answer)
                db.save_attempt(q, final_answer, fb)
                
            st.metric(label="Overall Match Score", value=f"{fb['overall']}/10")
            c1, c2 = st.columns(2)
            c1.success("**Key Strengths Identified:**\n\n" + "\n".join(f"- {s}" for s in fb["strengths"]))
            c2.warning("**Areas for Improvement:**\n\n" + "\n".join(f"- {s}" for s in fb["improvements"]))
            
            with st.expander("Review an Optimal Alternative Rewrite"):
                st.write(fb["rewritten_answer"])

        if i < len(qs) - 1 and st.button("Move to Next Question ➡️"):
            st.session_state.idx += 1
            st.rerun()

# --- TAB 4: PROGRESS DASHBOARD ---
with tab_progress:
    st.subheader("Performance Metric Insights")
    rows = db.weak_areas()
    if rows:
        st.dataframe(rows, use_container_width=True)
        st.bar_chart({r["competency"]: r["avg_score"] for r in rows})
    else:
        st.info("Your analytics dashboard will populate once you evaluate your first responses.")
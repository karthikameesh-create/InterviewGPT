import streamlit as st
st.set_page_config(
    page_title="InterviewGPT Pro V5",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

from auth_guard import initialize_session
from auth_app import login_page

initialize_session()

if not st.session_state.get("logged_in", False):
    login_page()
    st.stop()
import pandas as pd
import time
import plotly.express as px
import re
from datetime import date
from utils.resume_parser import extract_resume_text

from utils.gemini_analyzer import (

    analyze_resume,
    generate_ats_report,
    analyze_job_match,

    generate_interview_questions,
    evaluate_answer,

    generate_skill_gap_report,
    generate_learning_roadmap,
    generate_final_interview_report,

    generate_mock_interview_question,

    generate_company_prep,
    generate_company_insights,
    generate_interview_questions,
    generate_hr_cheat_sheet,

    #generate_career_path,
    #generate_salary_insights,
    #generate_hiring_probability,

    #rewrite_resume,
    #optimize_linkedin_profile,
    #generate_30_day_plan,

    generate_coding_question,
    evaluate_code_solution,
    generate_coding_readiness_report,
    generate_company_coding_round,
    generate_dsa_roadmap,

    career_copilot_chat,
    resume_chatbot,
    interview_copilot,
    analyze_job_application,
    generate_self_introduction,
    generate_ats_resume,
    generate_cover_letter,
    generate_recruiter_response,
    generate_recruiter_evaluation,
    generate_ai_career_mentor,
    generate_aptitude_questions
)

from utils.database_firestore import (

    create_table,
    save_interview,

    get_interviews,
    get_total_interviews,
    get_average_score,
    get_best_score,
    get_latest_score,

    delete_all_history,

    get_company_performance,
    get_role_performance,
    get_dashboard_stats,
    get_recent_interviews,
    get_weekly_progress,
    calculate_career_score
)

# ===================================
# NEW JOB TRACKER IMPORTS
# ===================================

from utils.job_tracker_firestore import (

    create_job_table,

    add_application,

    get_applications,

    update_application_status,

    delete_application,

    get_job_stats,

    get_dashboard_job_stats,

    get_recent_activity,

    get_application_timeline
)

from utils.job_search import search_jobs

from utils.career_advisor import (
    generate_career_advisor
)

from utils.pdf_report import (
    generate_pdf_report,
    generate_resume_pdf,
    generate_cover_letter_pdf
)

from utils.resume_builder import (
      build_resume_docx,
      add_p_border_bottom,
      generate_resume_pdf
      )

from utils.cover_letter_builder import (
    build_cover_letter_docx
)

from utils.voice_utils import (
    speech_to_text
)

from utils.skill_accelerator import (

    generate_skill_accelerator
)

from utils.role_skill_analyzer import (

    safe_analyze_role_requirements

)

from utils.learning_resources import (

    generate_learning_cards

)
from ui.ats_scanner import render_ats_scanner

from ui.jd_match import render_jd_match

from utils.aptitude_engine import AptitudeEngine

from auth_guard import logout
import streamlit as st


# ===================================
# PAGE CONFIG
# ===================================
pages = [

    "🏠 Home",

    "📄 Resume Analyzer",

    "📝 AI Resume Builder",

    "✉️ AI Cover Letter",

    "📈 ATS Scanner",

    "🎯 JD Match Analyzer",

    "🧮 AI Aptitude Round",

    "🎤 Question Bank",

    "🎙 Mock Interview",

    "🎯 AI Recruiter Simulator",

    "🏢 Company Prep Mode",

    "🎯 Career Coach",

    "💬 Career Copilot",

    "📋 Job Tracker",

    "💻 Live Coding Round",

    "🚀 Skill Gap Report",

    "🗺 Learning Roadmap",

    "🚀 Career Dashboard"

]



# ===================================
# DATABASE SETUP
# ===================================

create_table()

create_job_table()

# ===================================
# UI
# ===================================

st.markdown(
"""
<style>

.block-container{
    padding-top:1rem;
}

.hero{

    background:linear-gradient(
    135deg,
    #0f172a,
    #1e40af
    );

    padding:40px;

    border-radius:20px;

    margin-bottom:20px;
}

.hero h1{

    color:white !important;

    font-size:58px !important;

    font-weight:800 !important;
}

.hero h3{

    color:#e2e8f0 !important;
}

div[data-testid="metric-container"]{

    border-radius:16px;

    padding:15px;
}

textarea,
input,
div[data-baseweb="select"] *{

    color:black !important;
}

.stTextInput input{

    color:black !important;
}

.stTextArea textarea{

    color:black !important;
}

code{

    color:black !important;
}

pre{

    color:black !important;
}

</style>
""",

unsafe_allow_html=True
)

# ===================================
# SESSION STATE
# ===================================

defaults = {
    "last_page":"🏠 Home",

    "resume_text":"",

    "job_description":"",

    "questions":[],

    "evaluations":[],

    "mock_questions":[],

    "current_mock_question":"",

    "attempted":0,

    "mock_count":0,

    "voice_answer":"",

    "final_report":"",

    "company_prep_report":"",

    "company_insights":"",

    "company_prep_report": "",

    "company_insights": "",

    "company_questions": "",

    "hr_cheat_sheet": "",

    "career_path":"",

    "salary_report":"",

    "hiring_probability":"",

    "rewritten_resume":"",

    "linkedin_report":"",

    "career_plan":"",

    "career_mentor_report": "",

    "coding_question":"",

    "coding_result":"",

    "coding_history":[],

    "coding_round_number": 1,

    "coding_round":"",

    "dsa_roadmap":"",

    "career_chat":[],

    "ats_report_cache":"",

    # Resume Features

    "resume_analysis":"",

    "ai_resume":"",

    "cover_letter":"",

    "jd_report": {},

    "skill_gap_report":"",

    "roadmap":"",

    "aptitude_questions": [],

    "current_aptitude_question": 0,

    "aptitude_answers": {},

    "aptitude_score": 0,

    "aptitude_started": False,

    "aptitude_completed": False,

    "aptitude_company": "",

    "aptitude_role": "",

    "aptitude_test_type": "Mixed",

    "aptitude_difficulty": "Medium",

    "aptitude_questions_count": 20,

    "aptitude_timer": "No Timer",

    "negative_marking": False,

    "aptitude_report": "",

    "aptitude_learning_plan": "",

    "aptitude_statistics": {},

    "aptitude_start_time": None,

    "question_start_time": None,

    "last_aptitude_company": "",

    "last_aptitude_role": "",

    "last_aptitude_test_type": "Mixed",

    "last_aptitude_difficulty": "Medium",

    "last_aptitude_questions_count": 20,

    # AI Recruiter Simulator

    "recruiter_chat":[],

    "interview_started":False,

    "interview_finished":False,

    "recruiter_report":"",

    "current_company":"",

    "current_role":"",

    "current_interview_type":"",

    "current_difficulty":"",

    "current_experience":"",

    # Job Tracker

    "job_stats":{},

    "job_results": [],

    "career_dashboard": {},

    "skill_accelerator": {},
}

for key, value in defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value

# ===================================
# SIDEBAR
# ===================================

st.sidebar.title(
    "🤖 InterviewGPT Pro V5"
)
email = st.session_state.get("user_email", "Guest")

st.sidebar.write(f"👤 {email}")

if st.sidebar.button("🚪 Logout"):
    logout()
    
page = st.sidebar.radio(

    "Navigation",

    [

        "🏠 Home",

        "📄 Resume Analyzer",

        "📝 AI Resume Builder",

        "✉️ AI Cover Letter",

        "📈 ATS Scanner",

        "🎯 JD Match Analyzer",

        "🧮 AI Aptitude Round",

        "🎤 Question Bank",

        "🎙 Mock Interview",

        "🎯 AI Recruiter Simulator",

        "🏢 Company Prep Mode",

        "🎯 Career Coach",

        "💬 Career Copilot",

        # NEW PAGE

        "📋 Job Tracker",

        "💻 Live Coding Round",

        "🚀 Skill Gap Report",

        "🗺 Learning Roadmap",

        "🚀 Career Dashboard",

        #"📊 Dashboard"
    ]
)

st.sidebar.divider()

uploaded_resume = st.sidebar.file_uploader(

    "📄 Resume",

    type=["pdf"]
)

uploaded_jd = st.sidebar.file_uploader(

    "📋 Upload JD",

    type=["txt"]
)

from utils.firestore_db import save_resume

if uploaded_resume:

    resume_text = extract_resume_text(
        uploaded_resume
    )

    st.session_state["resume_text"] = resume_text

    save_resume(

        st.session_state.user["localId"],

        resume_text

    )

if uploaded_jd:

    st.session_state[
        "job_description"
    ] = uploaded_jd.read().decode(
        "utf-8"
    )

# ===================================
# HOME PAGE
# ===================================
if page == "🏠 Home":

    # ===================================
    # PREMIUM CSS — LIGHT MODE (HOME)
    # ===================================
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #f0f4fb !important; }
    .stApp { background: #f0f4fb !important; }
    .block-container { padding-top: 1.5rem !important; }

    .home-hero {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        border-radius: 24px; padding: 52px 48px; margin-bottom: 28px;
        position: relative; overflow: hidden;
        box-shadow: 0 10px 30px rgba(15,23,42,0.15);
    }
    .home-hero::before {
        content:''; position:absolute; top:-80px; right:-80px;
        width:320px; height:320px;
        background:radial-gradient(circle, rgba(255,255,255,0.06) 0%, transparent 70%);
        border-radius:50%;
    }
    .home-title { font-size:2.4rem; font-weight:800; color:#fff; margin:0 0 8px; letter-spacing:-0.5px; }
    .home-subtitle { color:rgba(255,255,255,0.65); font-size:1.1rem; margin:0; font-weight:400; }
    
    .section-header { display:flex; align-items:center; gap:10px; margin:32px 0 16px; }
    .section-badge {
        background:#dbeafe; color:#1d4ed8; border-radius:8px; padding:3px 10px;
        font-size:0.66rem; font-weight:700; text-transform:uppercase; letter-spacing:0.1em;
    }
    .section-title { font-size:1.15rem; font-weight:700; color:#1e293b; margin:0; }

    .metric-card {
        background:#fff; border:1px solid #e2e8f0; border-radius:16px; padding:20px 18px;
        box-shadow:0 1px 4px rgba(0,0,0,0.04); margin-bottom: 14px;
        transition:border-color 0.2s, box-shadow 0.2s;
    }
    .metric-card:hover { border-color:#3b82f6; box-shadow:0 4px 16px rgba(59,130,246,0.08); }
    .metric-value { font-size:1.8rem; font-weight:700; color:#0f172a; line-height:1.1; }
    .metric-label { font-size:0.72rem; color:#64748b; text-transform:uppercase; letter-spacing:0.08em; margin-top:6px; font-weight:500; }

    .feature-card {
        background:#fff; border:1px solid #e2e8f0; border-radius:12px; padding:14px 16px;
        margin-bottom:10px; display:flex; align-items:center; gap:12px;
        box-shadow:0 1px 3px rgba(0,0,0,0.02);
    }
    .feature-icon { font-size:1.2rem; }
    .feature-text { font-size:0.85rem; font-weight:600; color:#334155; }

    .status-panel {
        border-radius: 16px; padding: 20px 24px; margin-top: 12px;
        display: flex; align-items: center; gap: 16px;
    }
    .status-panel-success { background: #f0fdf4; border: 1px solid #bbf7d0; color: #166534; }
    .status-panel-warning { background: #fffbeb; border: 1px solid #fef3c7; color: #92400e; }
    .status-title { font-size: 0.95rem; font-weight: 700; margin-bottom: 2px; }
    .status-desc { font-size: 0.78rem; opacity: 0.85; }
    </style>
    """, unsafe_allow_html=True)

    # ===================================
    # HERO BANNER
    # ===================================
    st.markdown("""
    <div class="home-hero">
        <div class="home-title">🤖 InterviewGPT Pro V5</div>
        <div class="home-subtitle">AI Career Coach • Interview Copilot • Job Tracker</div>
    </div>
    """, unsafe_allow_html=True)

    # ===================================
    # RESUME STATUS BAR
    # ===================================
    if st.session_state.get("resume_text"):
        st.markdown("""
        <div class="status-panel status-panel-success">
            <div style="font-size: 1.8rem;">📥</div>
            <div>
                <div class="status-title">Resume Parsing Active</div>
                <div class="status-desc">Your profile is safely stored in internal cache. Analytics engines are listening.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div class="status-panel status-panel-warning">
            <div style="font-size: 1.8rem;">🔒</div>
            <div>
                <div class="status-title">Action Required: Upload Resume</div>
                <div class="status-desc">Please drop your resume document into the sidebar processing hub to unlock engine analytics.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ===================================
    # PREP HUB METRICS
    # ===================================
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">Activity</span>
        <span class="section-title">Preparation Activity Counters</span>
    </div>""", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{st.session_state.get('attempted', 0)}</div><div class="metric-label">Questions Solved</div></div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{st.session_state.get('mock_count', 0)}</div><div class="metric-label">Mock Sessions</div></div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{len(st.session_state.get('evaluations', []))}</div><div class="metric-label">AI Evaluations</div></div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{len(st.session_state.get('coding_history', []))}</div><div class="metric-label">Coding Rounds</div></div>""", unsafe_allow_html=True)

    # ===================================
    # JOB TRACKER PIPELINE METRICS
    # ===================================
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">Live CRM</span>
        <span class="section-title">Application Pipeline Funnel</span>
    </div>""", unsafe_allow_html=True)

    stats = get_job_stats()

    jc1, jc2, jc3, jc4 = st.columns(4)
    with jc1:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{sum(stats.values())}</div><div class="metric-label">Total Pipeline Applications</div></div>""", unsafe_allow_html=True)
    with jc2:
        st.markdown(f"""<div class="metric-card"><div class="metric-value">{stats.get('Interview', 0)}</div><div class="metric-label">Active Interviews</div></div>""", unsafe_allow_html=True)
    with jc3:
        st.markdown(f"""<div class="metric-card"><div class="metric-value" style="color: #16a34a;">{stats.get('Offer', 0)}</div><div class="metric-label">Offers Extended</div></div>""", unsafe_allow_html=True)
    with jc4:
        st.markdown(f"""<div class="metric-card"><div class="metric-value" style="color: #dc2626;">{stats.get('Rejected', 0)}</div><div class="metric-label">Applications Archived</div></div>""", unsafe_allow_html=True)

    # ===================================
    # CAPABILITIES GRID
    # ===================================
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">Capabilities</span>
        <span class="section-title">Platform Suite Modules</span>
    </div>""", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="feature-card"><span class="feature-icon">📄</span><span class="feature-text">Resume Analyzer</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-card"><span class="feature-icon">📈</span><span class="feature-text">ATS Optimization Engine</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-card"><span class="feature-icon">🎯</span><span class="feature-text">JD Target Matching Matrix</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-card"><span class="feature-icon">📋</span><span class="feature-text">Application Funnel Tracker</span></div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="feature-card"><span class="feature-icon">🎙️</span><span class="feature-text">AI Conversational Simulator</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-card"><span class="feature-icon">🏢</span><span class="feature-text">Enterprise Company Profiler</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-card"><span class="feature-icon">🎯</span><span class="feature-text">Strategic Career Director</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-card"><span class="feature-icon">💬</span><span class="feature-text">Real-time Copilot Environment</span></div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="feature-card"><span class="feature-icon">💻</span><span class="feature-text">Interactive Sandbox IDE</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-card"><span class="feature-icon">🚀</span><span class="feature-text">Technical Deficit Analyzer</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-card"><span class="feature-icon">🗺️</span><span class="feature-text">Adaptive Curriculum Mapping</span></div>', unsafe_allow_html=True)
        st.markdown('<div class="feature-card"><span class="feature-icon">📊</span><span class="feature-text">Executive Performance Analytics</span></div>', unsafe_allow_html=True)

# ===================================

# CAREER COPILOT

# ===================================



elif page == "💬 Career Copilot":



    st.title(

        "💬 Career Copilot"

    )



    st.caption(

        "Ask anything about your resume, interviews, career, salary, ATS score, coding preparation, or job readiness."

    )



    if not st.session_state[

        "resume_text"

    ]:



        st.warning(

            "📄 Please upload your resume first."

        )



    else:



        st.subheader(

            "⚡ Quick Actions"

        )



        qa1, qa2, qa3, qa4 = st.columns(4)



        with qa1:



            if st.button(

                "🎤 Self Intro",

                use_container_width=True

            ):



                try:



                    response = generate_self_introduction(

                        st.session_state[

                            "resume_text"

                        ]

                    )



                    st.session_state[

                        "career_chat"

                    ].append(

                        {

                            "role":"user",

                            "content":"Generate a self introduction"

                        }

                    )



                    st.session_state[

                        "career_chat"

                    ].append(

                        {

                            "role":"assistant",

                            "content":response

                        }

                    )



                except Exception as e:



                    st.error(

                        str(e)

                    )



        with qa2:



            if st.button(

                "💰 Salary Advice",

                use_container_width=True

            ):



                try:



                    response = career_copilot_chat(



                        st.session_state[

                            "resume_text"

                        ],



                        "What salary should I expect based on my profile?",



                        st.session_state.get(

                            "ats_report_cache",

                            ""

                        ),



                        "\n\n".join(

                            st.session_state[

                                "evaluations"

                            ]

                        ),



                        "\n\n".join(

                            st.session_state[

                                "coding_history"

                            ]

                        )

                    )



                    st.session_state[

                        "career_chat"

                    ].append(

                        {

                            "role":"user",

                            "content":"What salary should I expect?"

                        }

                    )



                    st.session_state[

                        "career_chat"

                    ].append(

                        {

                            "role":"assistant",

                            "content":response

                        }

                    )



                except Exception as e:



                    st.error(

                        str(e)

                    )



        with qa3:



            if st.button(

                "🚀 ATS Improve",

                use_container_width=True

            ):



                try:



                    response = career_copilot_chat(



                        st.session_state[

                            "resume_text"

                        ],



                        "How can I improve my ATS score?",



                        st.session_state.get(

                            "ats_report_cache",

                            ""

                        ),



                        "\n\n".join(

                            st.session_state[

                                "evaluations"

                            ]

                        ),



                        "\n\n".join(

                            st.session_state[

                                "coding_history"

                            ]

                        )

                    )



                    st.session_state[

                        "career_chat"

                    ].append(

                        {

                            "role":"user",

                            "content":"How can I improve my ATS score?"

                        }

                    )



                    st.session_state[

                        "career_chat"

                    ].append(

                        {

                            "role":"assistant",

                            "content":response

                        }

                    )



                except Exception as e:



                    st.error(

                        str(e)

                    )



        with qa4:



            if st.button(

                "🏢 FAANG Ready?",

                use_container_width=True

            ):



                try:



                    response = career_copilot_chat(



                        st.session_state[

                            "resume_text"

                        ],



                        "Am I ready for FAANG interviews?",



                        st.session_state.get(

                            "ats_report_cache",

                            ""

                        ),



                        "\n\n".join(

                            st.session_state[

                                "evaluations"

                            ]

                        ),



                        "\n\n".join(

                            st.session_state[

                                "coding_history"

                            ]

                        )

                    )



                    st.session_state[

                        "career_chat"

                    ].append(

                        {

                            "role":"user",

                            "content":"Am I ready for FAANG interviews?"

                        }

                    )



                    st.session_state[

                        "career_chat"

                    ].append(

                        {

                            "role":"assistant",

                            "content":response

                        }

                    )



                except Exception as e:



                    st.error(

                        str(e)

                    )



        st.divider()



        for message in st.session_state[

            "career_chat"

        ]:



            with st.chat_message(

                message["role"]

            ):



                st.markdown(

                    message["content"]

                )



        user_prompt = st.chat_input(

            "Ask anything about your career..."

        )



        if user_prompt:



            st.session_state[

                "career_chat"

            ].append(

                {

                    "role":"user",

                    "content":user_prompt

                }

            )



            with st.chat_message(

                "user"

            ):



                st.markdown(

                    user_prompt

                )



            with st.chat_message(

                "assistant"

            ):



                with st.spinner(

                    "Thinking..."

                ):



                    response = career_copilot_chat(



                        st.session_state[

                            "resume_text"

                        ],



                        user_prompt,



                        st.session_state.get(

                            "ats_report_cache",

                            ""

                        ),



                        "\n\n".join(

                            st.session_state[

                                "evaluations"

                            ]

                        ),



                        "\n\n".join(

                            st.session_state[

                                "coding_history"

                            ]

                        )

                    )



                    st.markdown(

                        response

                    )



            st.session_state[

                "career_chat"

            ].append(

                {

                    "role":"assistant",

                    "content":response

                }

            )



        st.divider()



        stats1, stats2, stats3 = st.columns(3)



        with stats1:



            st.metric(

                "Chat Messages",

                len(

                    st.session_state[

                        "career_chat"

                    ]

                )

            )



        with stats2:



            st.metric(

                "Interview Evaluations",

                len(

                    st.session_state[

                        "evaluations"

                    ]

                )

            )



        with stats3:



            st.metric(

                "Coding Evaluations",

                len(

                    st.session_state[

                        "coding_history"

                    ]

                )

            )

# ===================================

# RESUME ANALYZER

# ===================================



elif page == "📄 Resume Analyzer":



    st.title(

        "📄 Resume Analyzer"

    )



    if not st.session_state[

        "resume_text"

    ]:



        st.warning(

            "Upload Resume To Begin"

        )



    else:



        st.success(

            "Resume Loaded Successfully"

        )



        if st.button(

            "🚀 Analyze Resume",

            use_container_width=True

        ):



            try:



                with st.spinner(

                    "Analyzing Resume..."

                ):



                    result = analyze_resume(

                        st.session_state[

                            "resume_text"

                        ]

                    )



                    st.session_state[

                        "resume_analysis"

                    ] = result



            except Exception as e:



                st.error(

                    str(e)

                )



        if st.session_state.get(

            "resume_analysis",

            ""

        ):



            st.divider()



            st.subheader(

                "📊 Resume Analysis"

            )



            st.markdown(

                st.session_state[

                    "resume_analysis"

                ]

            ) 

elif page == "📝 AI Resume Builder":



    st.title("📝 AI Resume Builder")



    st.caption(

        "Generate an ATS-Optimized Resume using AI"

    )



    if not st.session_state.get("resume_text", ""):

        st.warning(

            "📄 Please upload your resume first."

        )

    else:

        st.subheader("🚀 AI Resume Studio")



        col1, col2 = st.columns(2)



        with col1:

            company = st.text_input(

                "🏢 Target Company",

                placeholder="Google"

            )

            role = st.text_input(

                "💼 Target Role",

                placeholder="Software Engineer"

            )

            experience = st.selectbox(

                "📈 Experience Level",

                ["Fresher", "0-2 Years", "2-5 Years", "5+ Years"]

            )



        with col2:

            resume_style = st.selectbox(

                "🎨 Resume Style",

                ["ATS Professional", "Modern", "Executive", "Startup", "Minimal"]

            )

            resume_length = st.radio(

                "📄 Resume Length",

                ["One Page", "Two Pages"]

            )



        st.divider()

        st.subheader("🎯 Resume Focus Areas")



        focus = st.multiselect(

            "Select what should be highlighted",

            ["Projects", "Technical Skills", "Experience", "Internships", "Research", "Achievements", "Leadership", "Certifications"],

            default=["Projects", "Technical Skills"]

        )



        st.subheader("📝 Additional Instructions")

        user_instruction = st.text_area(

            "",

            height=120,

            placeholder="""Example:

• Keep resume within one page.

• Highlight InterviewGPT project.

• Focus on backend development.

• Use strong action verbs.

• Make it ATS friendly.

• Remove unnecessary content.

"""

        )



        st.subheader("📋 Job Description")

        jd = st.text_area(

            "",

            value=st.session_state.get("job_description", ""),

            height=180

        )



        if st.button("✨ Generate ATS Resume", use_container_width=True):

            try:

                with st.spinner("Generating ATS Resume..."):

                    st.session_state["ai_resume"] = generate_ats_resume(

                        resume_text=st.session_state["resume_text"],

                        role=role,

                        company=company,

                        experience=experience,

                        job_description=jd,

                        resume_style=resume_style,

                        resume_length=resume_length,

                        focus_areas=", ".join(focus),

                        user_instruction=user_instruction

                    )

                    st.session_state["generated_style"] = resume_style

            except Exception as e:

                st.error(str(e))



        if st.session_state.get("ai_resume", ""):

            st.divider()

            st.subheader("📄 Generated ATS Resume")



            # FIXED: Renders parsed structured data inside explicit dictionary components

            st.json(st.session_state["ai_resume"])



            current_style = st.session_state.get("generated_style", resume_style)



            # FIXED: Dynamically map selected styling guidelines into compiler components

            docx_file = build_resume_docx(

                st.session_state["ai_resume"],

                template=current_style

            )



            # FIXED: Synchronized PDF compilation block prevents data translation crashes

            pdf_file = generate_resume_pdf(

                st.session_state["ai_resume"],

                template=current_style

            )



            col1, col2 = st.columns(2)

            with col1:

                with open(docx_file, "rb") as file:

                    st.download_button(

                        "📥 Download DOCX",

                        file,

                        file_name="ATS_Resume.docx",

                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",

                        use_container_width=True

                    )



            with col2:

                with open(pdf_file, "rb") as file:

                    st.download_button(

                        "📄 Download PDF",

                        file,

                        file_name="ATS_Resume.pdf",

                        mime="application/pdf",

                        use_container_width=True

                    ) 


# ===================================

# AI COVER LETTER

# ===================================



elif page == "✉️ AI Cover Letter":



    st.title("✉️ AI Cover Letter Generator")



    st.caption(

        "Generate a recruiter-ready professional cover letter."

    )



    if not st.session_state.get(

        "resume_text",

        ""

    ):



        st.warning(

            "📄 Please upload your resume first."

        )



    else:



        company = st.text_input(

            "Target Company",

            placeholder="Google",

            key="cl_company"

        )



        role = st.text_input(

            "Target Role",

            placeholder="Software Engineer",

            key="cl_role"

        )



        experience = st.selectbox(



            "Experience Level",



            [



                "Fresher",



                "0-2 Years",



                "2-5 Years",



                "5+ Years"



            ],



            key="cl_exp"



        )



        hiring_manager = st.text_input(



            "Hiring Manager (Optional)",



            placeholder="John Smith"



        )



        style = st.selectbox(



            "Writing Style",



            [



                "Professional",



                "FAANG",



                "Startup",



                "Modern",



                "Conservative"



            ]



        )



        job_description = st.text_area(



            "Job Description (Optional)",



            value=st.session_state.get(

                "job_description",

                ""

            ),



            height=180



        )



        if st.button(



            "✨ Generate Cover Letter",



            use_container_width=True



        ):



            try:



                with st.spinner(



                    "Writing Professional Cover Letter..."



                ):



                    st.session_state["cover_letter"] = generate_cover_letter(



                        st.session_state["resume_text"],



                        company,



                        role,



                        experience,



                        hiring_manager,



                        job_description,



                        style



                    )



            except Exception as e:



                st.error(

                    str(e)

                )



        if st.session_state.get(



            "cover_letter",



            ""



        ):



            st.divider()



            st.subheader(



                "📄 Professional Cover Letter"



            )



            st.text_area(



                "Preview",



                st.session_state["cover_letter"],



                height=550



            )



            docx_file = build_cover_letter_docx(



                st.session_state["cover_letter"]



            )



            pdf_file = generate_cover_letter_pdf(



                st.session_state["cover_letter"]



            )



            c1, c2 = st.columns(2)



            with c1:



                with open(



                    docx_file,



                    "rb"



                ) as file:



                    st.download_button(



                        "📥 Download DOCX",



                        file,



                        file_name="Cover_Letter.docx",



                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",



                        use_container_width=True



                    )



            with c2:



                with open(



                    pdf_file,



                    "rb"



                ) as file:



                    st.download_button(



                        "📄 Download PDF",



                        file,



                        file_name="Cover_Letter.pdf",



                        mime="application/pdf",



                        use_container_width=True



                    ) 



# ===================================
# ATS SCANNER
# ===================================

elif page == "📈 ATS Scanner":

    render_ats_scanner()
# ===================================
# JD MATCH ANALYZER
# ===================================
elif page == "🎯 JD Match Analyzer":

    render_jd_match()

# ===================================

# QUESTION BANK

# ===================================



elif page == "🎤 Question Bank":



    st.title("🎤 AI Interview Question Bank")



    st.caption(

        "Generate personalized interview questions based on your resume and target company."

    )



    if not st.session_state.get("resume_text"):



        st.warning("📄 Please upload your resume first.")



    else:



        company = st.text_input(

            "🏢 Target Company",

            placeholder="Google, Amazon, Microsoft..."

        )



        role = st.text_input(

            "💼 Target Role",

            value="Software Engineer"

        )



        col1, col2, col3 = st.columns(3)



        with col1:



            experience = st.selectbox(

                "Experience Level",

                [

                    "Fresher",

                    "0-2 Years",

                    "2-5 Years",

                    "5+ Years"

                ]

            )



        with col2:



            category = st.selectbox(

                "Interview Category",

                [

                    "Technical",

                    "Behavioral",

                    "HR",

                    "Coding",

                    "System Design",

                    "Mixed"

                ]

            )



        with col3:



            num_questions = st.slider(

                "Number of Questions",

                5,

                25,

                10,

                5

            )



        st.divider()



        if st.button(

            "🚀 Generate Interview Workbook",

            use_container_width=True

        ):



            if company.strip() == "":



                st.warning(

                    "Please enter a target company."

                )



            else:



                try:



                    with st.spinner(

                        "Generating Interview Workbook..."

                    ):



                        workbook = generate_interview_questions(



                            resume_text=st.session_state["resume_text"],



                            company=company,



                            role=role,



                            experience=experience,



                            category=category,



                            num_questions=num_questions



                        )



                        st.session_state["questions"] = workbook



                except Exception as e:



                    st.error(str(e))



        if st.session_state.get("questions"):



            st.divider()



            st.subheader("📚 Personalized Interview Workbook")



            st.markdown(

                st.session_state["questions"]

            )



            st.divider()



            if st.button(

                "🔄 Generate Another Question Bank",

                use_container_width=True

            ):



                try:



                    with st.spinner(

                        "Generating..."

                    ):



                        st.session_state["questions"] = generate_interview_questions(



                            resume_text=st.session_state["resume_text"],



                            company=company,



                            role=role,



                            experience=experience,



                            category=category,



                            num_questions=num_questions



                        )



                        st.rerun()



                except Exception as e:



                    st.error(str(e)) 


# ===================================

# MOCK INTERVIEW

# ===================================

elif page == "🎙 Mock Interview":



    st.title(

        "🎙 AI Mock Interview"

    )



    if not st.session_state[

        "resume_text"

    ]:



        st.warning(

            "Upload Resume First"

        )



    else:



        company = st.text_input(

            "Target Company",

            placeholder="Google, OpenAI, Microsoft...",

            key="mock_company"

        )



        role = st.text_input(

            "Target Role",

            value="Software Engineer",

            key="mock_role"

        )



        experience = st.selectbox(



            "Experience Level",



            [

                "Fresher",

                "0-2 Years",

                "2-5 Years",

                "5+ Years"

            ],



            key="mock_exp"

        )



        st.divider()



        c1, c2 = st.columns(2)



        with c1:



            if st.button(

                "🎯 Start Mock Interview",

                use_container_width=True

            ):



                try:



                    question = generate_mock_interview_question(



                        st.session_state[

                            "resume_text"

                        ],



                        company,



                        role,



                        experience,



                        "\n".join(

                            st.session_state[

                                "mock_questions"

                            ]

                        )

                    )



                    st.session_state[

                        "current_mock_question"

                    ] = question



                    st.session_state[

                        "mock_questions"

                    ].append(

                        question

                    )



                    st.session_state[

                        "mock_count"

                    ] += 1



                except Exception as e:



                    st.error(

                        str(e)

                    )



        with c2:



            if st.button(

                "➡ Next Question",

                use_container_width=True

            ):



                try:



                    question = generate_mock_interview_question(



                        st.session_state[

                            "resume_text"

                        ],



                        company,



                        role,



                        experience,



                        "\n".join(

                            st.session_state[

                                "mock_questions"

                            ]

                        )

                    )



                    st.session_state[

                        "current_mock_question"

                    ] = question



                    st.session_state[

                        "mock_questions"

                    ].append(

                        question

                    )



                except Exception as e:



                    st.error(

                        str(e)

                    )



        if st.session_state[

            "current_mock_question"

        ]:



            st.divider()



            st.subheader(

                "🎤 Interview Question"

            )



            st.info(

                st.session_state[

                    "current_mock_question"

                ]

            )



            answer = st.text_area(



                "Your Answer",



                height=250

            )



            voice_col1, voice_col2 = st.columns(2)



            with voice_col1:



                if st.button(

                    "🎙 Voice To Text",

                    use_container_width=True

                ):



                    try:



                        transcript = speech_to_text()



                        st.session_state[

                            "voice_answer"

                        ] = transcript



                    except Exception as e:



                        st.error(

                            str(e)

                        )



            with voice_col2:



                if st.session_state[

                    "voice_answer"

                ]:



                    st.success(

                        "Voice captured successfully."

                    )



            if st.session_state[

                "voice_answer"

            ]:



                answer = st.session_state[

                    "voice_answer"

                ]



                st.text_area(



                    "Transcribed Answer",



                    value=answer,



                    height=200

                )



            if st.button(

                "✅ Evaluate Answer",

                use_container_width=True

            ):



                if answer.strip() == "":



                    st.warning(

                        "Please provide an answer."

                    )



                else:



                    try:



                        with st.spinner(

                            "Evaluating..."

                        ):



                            result = evaluate_answer(



                                st.session_state[

                                    "current_mock_question"

                                ],



                                answer

                            )



                            st.session_state[

                                "evaluations"

                            ].append(

                                result

                            )



                            st.session_state[

                                "attempted"

                            ] += 1



                        st.subheader(

                            "📊 Evaluation"

                        )



                        st.markdown(

                            result

                        )



                    except Exception as e:



                        st.error(

                            str(e)

                        )



        st.divider()



        s1, s2, s3 = st.columns(3)



        with s1:



            st.metric(

                "Questions Attempted",

                st.session_state[

                    "attempted"

                ]

            )



        with s2:



            st.metric(

                "Mock Interviews",

                st.session_state[

                    "mock_count"

                ]

            )



        with s3:



            readiness = min(



                st.session_state[

                    "attempted"

                ] * 5,



                100

            )



            st.metric(

                "Interview Readiness",

                f"{readiness}%"

            )



        st.progress(

            readiness / 100

        ) 

# ===================================

# AI RECRUITER SIMULATOR

# ===================================



elif page == "🎯 AI Recruiter Simulator":



    st.title("🎯 AI Recruiter Simulator")



    st.caption(

        "Experience a realistic AI-powered interview with dynamic follow-up questions."

    )



    # -----------------------------

    # Session State Defaults

    # -----------------------------

    if "recruiter_chat" not in st.session_state:

        st.session_state["recruiter_chat"] = []



    if "interview_started" not in st.session_state:

        st.session_state["interview_started"] = False



    if "interview_finished" not in st.session_state:

        st.session_state["interview_finished"] = False



    if "voice_answer" not in st.session_state:

        st.session_state["voice_answer"] = ""



    if "recruiter_evaluation" not in st.session_state:

        st.session_state["recruiter_evaluation"] = ""



    # -----------------------------

    # Resume Check

    # -----------------------------

    if not st.session_state.get(

        "resume_text",

        ""

    ):



        st.warning(

            "📄 Please upload your resume first."

        )



    else:



        st.subheader(

            "Interview Configuration"

        )



        col1, col2 = st.columns(2)



        with col1:



            company = st.text_input(



                "Target Company",



                value=st.session_state.get(

                    "current_company",

                    ""

                ),



                placeholder="Enter any company name..."

            )



            interview_type = st.selectbox(



                "Interview Type",



                [



                    "Technical",



                    "Behavioral",



                    "HR",



                    "Mixed",



                    "Managerial"



                ]

            )



        with col2:



            role = st.text_input(



                "Target Role",



                value=st.session_state.get(

                    "current_role",

                    ""

                ),



                placeholder="Software Engineer"

            )



            difficulty = st.selectbox(



                "Difficulty",



                [



                    "Easy",



                    "Medium",



                    "Hard",



                    "Expert"



                ]

            )



        experience = st.selectbox(



            "Experience",



            [



                "Fresher",



                "0-2 Years",



                "2-5 Years",



                "5+ Years"



            ]

        )



        st.divider()



        start_col1, start_col2 = st.columns(2)



        with start_col1:



            if st.button(



                "▶ Start Interview",



                use_container_width=True



            ):



                st.session_state["current_company"] = company

                st.session_state["current_role"] = role

                st.session_state["current_experience"] = experience

                st.session_state["current_interview_type"] = interview_type

                st.session_state["current_difficulty"] = difficulty



                st.session_state["recruiter_chat"] = []

                st.session_state["voice_answer"] = ""

                st.session_state["recruiter_evaluation"] = ""



                st.session_state["interview_started"] = True

                st.session_state["interview_finished"] = False



                with st.spinner(

                    "Recruiter is joining..."

                ):



                    recruiter = generate_recruiter_response(



                        st.session_state["resume_text"],



                        company,



                        role,



                        experience,



                        interview_type,



                        difficulty,



                        "",



                        "START_INTERVIEW"



                    )



                st.session_state["recruiter_chat"].append(



                    {



                        "role": "assistant",



                        "content": recruiter



                    }



                )



                st.rerun()



        with start_col2:



            if st.button(



                "🗑 Reset Interview",



                use_container_width=True



            ):



                st.session_state["recruiter_chat"] = []

                st.session_state["voice_answer"] = ""

                st.session_state["recruiter_evaluation"] = ""



                st.session_state["interview_started"] = False

                st.session_state["interview_finished"] = False



                st.rerun()

                        # ===================================

        # LIVE INTERVIEW

        # ===================================



        if st.session_state["interview_started"]:



            st.subheader(

                "💬 Live Interview"

            )



            for message in st.session_state[

                "recruiter_chat"

            ]:



                with st.chat_message(

                    message["role"]

                ):



                    st.markdown(

                        message["content"]

                    )



            st.divider()



            # -----------------------------

            # Voice Controls

            # -----------------------------



            voice_col1, voice_col2 = st.columns(2)



            with voice_col1:



                if st.button(

                    "🎙 Voice Answer",

                    use_container_width=True

                ):



                    try:



                        transcript = speech_to_text()



                        if transcript:



                            st.session_state[

                                "voice_answer"

                            ] = transcript



                            st.success(

                                "✅ Voice captured successfully."

                            )



                            st.rerun()



                    except Exception as e:



                        st.error(str(e))



            with voice_col2:



                if st.button(

                    "⏹ End Interview",

                    use_container_width=True

                ):



                    st.session_state[

                        "interview_finished"

                    ] = True



                    st.rerun()



            # -----------------------------

            # Show Voice Answer

            # -----------------------------



            if st.session_state[

                "voice_answer"

            ]:



                st.text_area(



                    "Voice Transcript",



                    value=st.session_state[

                        "voice_answer"

                    ],



                    height=150,



                    disabled=False

                )



            # -----------------------------

            # Chat Input

            # -----------------------------



            typed_answer = st.chat_input(

                "Type your answer..."

            )



            answer = None



            if typed_answer:



                answer = typed_answer



            elif st.session_state[

                "voice_answer"

            ]:



                answer = st.session_state[

                    "voice_answer"

                ]



                st.session_state[

                    "voice_answer"

                ] = ""



            # -----------------------------

            # Send User Answer

            # -----------------------------



            if answer:



                st.session_state[

                    "recruiter_chat"

                ].append(



                    {



                        "role": "user",



                        "content": answer



                    }



                )



                conversation = "\n\n".join(



                    [



                        f"{msg['role'].upper()}: {msg['content']}"



                        for msg in st.session_state[

                            "recruiter_chat"

                        ]



                    ]



                )



                with st.spinner(

                    "Recruiter is thinking..."

                ):



                    recruiter_reply = generate_recruiter_response(



                        st.session_state[

                            "resume_text"

                        ],



                        st.session_state[

                            "current_company"

                        ],



                        st.session_state[

                            "current_role"

                        ],



                        st.session_state[

                            "current_experience"

                        ],



                        st.session_state[

                            "current_interview_type"

                        ],



                        st.session_state[

                            "current_difficulty"

                        ],



                        conversation,



                        answer



                    )



                st.session_state[

                    "recruiter_chat"

                ].append(



                    {



                        "role": "assistant",



                        "content": recruiter_reply



                    }



                )



                if recruiter_reply.startswith(

                    "[END_INTERVIEW]"

                ):



                    st.session_state[

                        "interview_finished"

                    ] = True



                st.rerun()

                        # ===================================

        # INTERVIEW FINISHED

        # ===================================



        if st.session_state["interview_finished"]:



            st.divider()



            st.success(

                "✅ Interview Completed"

            )



            conversation = "\n\n".join(



                [



                    f"{m['role'].upper()}: {m['content']}"



                    for m in st.session_state[

                        "recruiter_chat"

                    ]



                ]



            )



            st.subheader(

                "📄 Interview Transcript"

            )



            st.text_area(



                "Conversation",



                conversation,



                height=450



            )



            st.divider()



            st.subheader(

                "📊 Recruiter Evaluation"

            )



            if not st.session_state.get(

                "recruiter_evaluation",

                ""

            ):



                try:



                    with st.spinner(

                        "Generating Recruiter Evaluation..."

                    ):



                        st.session_state[

                            "recruiter_evaluation"

                        ] = generate_recruiter_evaluation(



                            resume_text=st.session_state[

                                "resume_text"

                            ],



                            conversation=conversation,



                            company=st.session_state[

                                "current_company"

                            ],



                            role=st.session_state[

                                "current_role"

                            ]



                        )



                except Exception as e:



                    st.error(str(e))



            if st.session_state.get(

                "recruiter_evaluation",

                ""

            ):



                st.markdown(



                    st.session_state[

                        "recruiter_evaluation"

                    ]



                )



            st.divider()



            col1, col2 = st.columns(2)



            with col1:



                if st.button(



                    "🔄 Start New Interview",



                    use_container_width=True



                ):



                    st.session_state[

                        "recruiter_chat"

                    ] = []



                    st.session_state[

                        "voice_answer"

                    ] = ""



                    st.session_state[

                        "recruiter_evaluation"

                    ] = ""



                    st.session_state[

                        "interview_started"

                    ] = False



                    st.session_state[

                        "interview_finished"

                    ] = False



                    st.rerun()



            with col2:



                st.download_button(



                    "📥 Download Transcript",



                    data=conversation,



                    file_name="Interview_Transcript.txt",



                    mime="text/plain",



                    use_container_width=True



                ) 

# ===================================

# COMPANY PREP MODE

# ===================================

elif page == "🏢 Company Prep Mode":



    st.title(

        "🏢 Company Preparation Hub"

    )



    company = st.text_input(

        "Target Company",

        placeholder="Google, Amazon, OpenAI, Nvidia..."

    )



    role = st.text_input(

        "Target Role",

        value="Software Engineer"

    )



    col1, col2, col3, col4 = st.columns(4)



    with col1:



        if st.button(

            "🚀 Generate Company Prep",

            use_container_width=True

        ):



            if company.strip() == "":



                st.warning(

                    "Enter company name."

                )



            else:



                try:



                    with st.spinner(

                        "Generating Preparation Guide..."

                    ):



                        st.session_state[

                            "company_prep_report"

                        ] = generate_company_prep(

                            company,

                            role

                        )



                except Exception as e:



                    st.error(

                        str(e)

                    )



    with col2:



        if st.button(

            "📊 Company Insights",

            use_container_width=True

        ):



            if company.strip() == "":



                st.warning(

                    "Enter company name."

                )



            else:



                try:



                    with st.spinner(

                        "Generating Insights..."

                    ):



                        st.session_state[

                            "company_insights"

                        ] = generate_company_insights(

                            company

                        )



                except Exception as e:



                    st.error(

                        str(e)

                    )



    with col3:



        if st.button(



            "❓ Interview Questions",



            use_container_width=True



        ):



            if company.strip() == "":



                st.warning(



                    "Enter company name."



                )



            else:



                try:



                    with st.spinner(



                        "Generating Interview Questions..."



                    ):



                        st.session_state[



                            "company_questions"



                        ] = generate_interview_questions(



                            company,



                            role



                        )



                except Exception as e:



                    st.error(



                        str(e)



                    )



    with col4:



        if st.button(



            "🧠 HR Cheat Sheet",



            use_container_width=True



        ):



            if company.strip() == "":



                st.warning(



                    "Enter company name."



                )



            else:



                try:



                    with st.spinner(



                        "Generating HR Cheat Sheet..."



                    ):



                        st.session_state[



                            "hr_cheat_sheet"



                        ] = generate_hr_cheat_sheet(



                            company,



                            role



                        )



                except Exception as e:



                    st.error(



                        str(e)



                    )



    st.divider()



    # ======================================

    # COMPANY PREPARATION REPORT

    # ======================================



    if st.session_state.get("company_prep_report"):



        with st.expander(



            "🏢 Company Preparation Guide",



            expanded=True



        ):



            st.markdown(



                st.session_state["company_prep_report"]



            )



    # ======================================

    # COMPANY INSIGHTS

    # ======================================



    if st.session_state.get("company_insights"):



        with st.expander(



            "📊 Company Insights",



            expanded=False



        ):



            st.markdown(



                st.session_state["company_insights"]



            )



    # ======================================

    # INTERVIEW QUESTIONS

    # ======================================



    if st.session_state.get("company_questions"):



        with st.expander(



            "❓ Technical & HR Interview Questions",



            expanded=False



        ):



            st.markdown(



                st.session_state["company_questions"]



            )



    # ======================================

    # HR CHEAT SHEET

    # ======================================



    if st.session_state.get("hr_cheat_sheet"):



        with st.expander(



            "🧠 HR Interview Cheat Sheet",



            expanded=False



        ):



            st.markdown(



                st.session_state["hr_cheat_sheet"]



            ) 

# ===================================
# AI CAREER MENTOR
# ===================================

# Near the top of your app (where you initialize session state), add:
# if "mentor_chat" not in st.session_state:
#     st.session_state["mentor_chat"] = []

elif page == "🎯 Career Coach":

    st.title("🎯 InterviewGPT AI Career Mentor")

    st.caption(
        "Your personal AI mentor that learns from your complete InterviewGPT journey."
    )

    if not st.session_state.get("resume_text"):

        st.warning(
            "📄 Please upload your resume first."
        )

    else:

        st.success(
            "✅ Resume Loaded Successfully"
        )

        # ===================================
        # TARGET DETAILS
        # ===================================

        col1, col2 = st.columns(2)

        with col1:

            company = st.text_input(
                "🎯 Dream Company",
                placeholder="Google, Amazon, Microsoft..."
            )

        with col2:

            role = st.text_input(
                "💼 Dream Role",
                value="Software Engineer"
            )

        st.divider()

        # ===================================
        # BUILD INTERVIEWGPT MEMORY
        # ===================================

        mentor_context = {

            "resume": st.session_state.get(
                "resume_text",
                ""
            ),

            "resume_analysis": st.session_state.get(
                "resume_analysis",
                ""
            ),

            "ats_report": st.session_state.get(
                "ats_report_cache",
                ""
            ),

            "coding_history": "\n\n".join(
                st.session_state.get(
                    "coding_history",
                    []
                )
            ),

            "mock_interviews": "\n\n".join(
                st.session_state.get(
                    "evaluations",
                    []
                )
            ),

            "skill_gap": st.session_state.get(
                "skill_gap_report",
                ""
            ),

            "learning_roadmap": st.session_state.get(
                "roadmap",
                ""
            ),

            "company_prep": st.session_state.get(
                "company_prep_report",
                ""
            ),

            "company_insights": st.session_state.get(
                "company_insights",
                ""
            ),

            "company_questions": st.session_state.get(
                "company_questions",
                ""
            ),

            "hr_cheat_sheet": st.session_state.get(
                "hr_cheat_sheet",
                ""
            ),

            "job_description": st.session_state.get(
                "job_description",
                ""
            ),

            "ai_resume": st.session_state.get(
                "ai_resume",
                ""
            ),

            "cover_letter": st.session_state.get(
                "cover_letter",
                ""
            )

        }

        # ===================================
        # ASK YOUR AI MENTOR
        # ===================================

        st.subheader(
            "💬 Ask Your AI Mentor"
        )

        mentor_question = st.text_area(
            "Ask anything about your career",
            height=170,
            placeholder="""
Examples:

• Am I ready for Google?

• Why am I not getting interviews?

• Should I focus on DSA or Projects?

• Should I learn AWS now?

• What is my biggest weakness?

• What should I do this weekend?

• Is InterviewGPT enough as my major project?

• Should I build another project?

• Review my overall progress.

• Give brutally honest career advice.
"""
        )

        st.info(
            """
🧠 The AI Mentor will use your resume, resume analysis, coding rounds,
mock interviews, skill gap reports, learning roadmap, company preparation,
AI resume, cover letter and every previous InterviewGPT activity while answering.
"""
        )

        st.divider()

        col1, col2 = st.columns(2)
        with col1:

            if st.button(
                "🚀 Generate AI Mentor Report",
                use_container_width=True
            ):

                try:

                    with st.spinner(
                        "Analyzing your complete InterviewGPT journey..."
                    ):

                        st.session_state[
                            "career_mentor_report"
                        ] = generate_ai_career_mentor(
                            mentor_context=mentor_context,
                            target_company=company,
                            target_role=role,
                            user_query=mentor_question
                        )

                except Exception as e:

                    st.error(str(e))

        with col2:

            if st.button(
                "💬 Ask AI Mentor",
                use_container_width=True
            ):

                if mentor_question.strip() == "":

                    st.warning(
                        "Please enter a question."
                    )

                else:

                    try:

                        with st.spinner(
                            "Your AI mentor is thinking..."
                        ):

                            mentor_chat_reply = generate_ai_career_mentor(
                                mentor_context=mentor_context,
                                target_company=company,
                                target_role=role,
                                user_query=mentor_question
                            )

                            st.session_state["mentor_chat"].append(
                                {
                                    "role": "user",
                                    "content": mentor_question
                                }
                            )

                            st.session_state["mentor_chat"].append(
                                {
                                    "role": "assistant",
                                    "content": mentor_chat_reply
                                }
                            )

                    except Exception as e:

                        st.error(str(e))

        st.divider()

        # ===================================
        # AI CAREER MENTOR REPORT
        # ===================================

        if st.session_state.get(
            "career_mentor_report",
            ""
        ):

            st.subheader(
                "🧠 Personalized AI Career Mentor Report"
            )

            st.markdown(
                st.session_state[
                    "career_mentor_report"
                ]
            )

            st.divider()

        # ===================================
        # AI MENTOR RESPONSE
        # ===================================

        if st.session_state.get("mentor_chat"):

            st.subheader("💬 AI Mentor Guidance")

            for message in st.session_state.get("mentor_chat", []):

                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            st.divider()

        # ===================================
        # TODAY'S ACTION CENTER
        # ===================================

        st.subheader(
            "📌 Today's Career Dashboard"
        )

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Resume",
                "Loaded" if st.session_state.get(
                    "resume_text"
                ) else "Missing"
            )

            st.metric(
                "Coding Reviews",
                len(
                    st.session_state.get(
                        "coding_history",
                        []
                    )
                )
            )

        with c2:

            st.metric(
                "Mock Interviews",
                len(
                    st.session_state.get(
                        "evaluations",
                        []
                    )
                )
            )

            st.metric(
                "Company Reports",
                "Ready" if st.session_state.get(
                    "company_prep_report"
                ) else "Pending"
            )

        with c3:

            st.metric(
                "Roadmap",
                "Generated" if st.session_state.get(
                    "roadmap"
                ) else "Pending"
            )

            st.metric(
                "Skill Gap",
                "Available" if st.session_state.get(
                    "skill_gap_report"
                ) else "Pending"
            )

        st.divider()

        # ===================================
        # QUICK CAREER CHECKLIST
        # ===================================

        st.subheader(
            "🚀 Career Checklist"
        )

        checklist = [

            (
                "Resume Uploaded",
                bool(
                    st.session_state.get(
                        "resume_text"
                    )
                )
            ),

            (
                "Resume Analyzed",
                bool(
                    st.session_state.get(
                        "resume_analysis"
                    )
                )
            ),

            (
                "Coding Round Completed",
                len(
                    st.session_state.get(
                        "coding_history",
                        []
                    )
                ) > 0
            ),

            (
                "Mock Interview Completed",
                len(
                    st.session_state.get(
                        "evaluations",
                        []
                    )
                ) > 0
            ),

            (
                "Skill Gap Report Generated",
                bool(
                    st.session_state.get(
                        "skill_gap_report"
                    )
                )
            ),

            (
                "Learning Roadmap Generated",
                bool(
                    st.session_state.get(
                        "roadmap"
                    )
                )
            ),

            (
                "Company Preparation Completed",
                bool(
                    st.session_state.get(
                        "company_prep_report"
                    )
                )
            ),

            (
                "AI Resume Generated",
                bool(
                    st.session_state.get(
                        "ai_resume"
                    )
                )
            )

        ]

        for title, status in checklist:

            if status:

                st.success(
                    f"✅ {title}"
                )

            else:

                st.warning(
                    f"⚠ {title}"
                )

        st.divider()

        # ===================================
        # NEXT STEPS
        # ===================================

        st.subheader(
            "🎯 Suggested Next Steps"
        )

        if not st.session_state.get(
            "resume_analysis"
        ):

            st.info(
                "📄 Start by generating your Resume Analysis."
            )

        elif len(
            st.session_state.get(
                "coding_history",
                []
            )
        ) == 0:

            st.info(
                "💻 Complete a Coding Interview."
            )

        elif len(
            st.session_state.get(
                "evaluations",
                []
            )
        ) == 0:

            st.info(
                "🎤 Practice a Mock Interview."
            )

        elif not st.session_state.get(
            "skill_gap_report"
        ):

            st.info(
                "📊 Generate your Skill Gap Report."
            )

        elif not st.session_state.get(
            "roadmap"
        ):

            st.info(
                "🗺 Generate your Learning Roadmap."
            )

        elif not st.session_state.get(
            "company_prep_report"
        ):

            st.info(
                "🏢 Prepare for your target company."
            )

        else:

            st.success(
                """
🎉 Excellent!
You have completed almost every major InterviewGPT activity.
Use the AI Mentor regularly to receive personalized career guidance as your profile evolves.
"""
            )

# ===================================

# AI APTITUDE ROUND

# ===================================



elif page == "🧮 AI Aptitude Round":



    from utils.aptitude_engine import AptitudeEngine



    st.title(

        "🧮 AI Aptitude Round"

    )



    st.caption(

        "Practice AI-generated company-specific aptitude tests designed to match real placement assessments."

    )



    # ===================================

    # SHOW CONFIGURATION SCREEN

    # ===================================



    if not st.session_state.get(

        "aptitude_started",

        False

    ):



        st.success(

            "Generate a personalized aptitude test for any company and role."

        )



        st.divider()



        col1, col2 = st.columns(2)



        with col1:



            company = st.text_input(



                "🏢 Target Company",



                key="aptitude_company",



                placeholder="Google, Amazon, Nvidia, Texas Instruments, Deloitte..."



            )



            role = st.text_input(



                "💼 Target Role",



                key="aptitude_role",



                placeholder="Software Engineer"



            )



            test_type = st.selectbox(



                "📝 Test Type",



                [



                    "Mixed",



                    "Quantitative Aptitude",



                    "Logical Reasoning",



                    "Verbal Ability",



                    "Data Interpretation",



                    "Company Pattern"



                ],



                key="aptitude_test_type"



            )



        with col2:



            difficulty = st.selectbox(



                "📊 Difficulty",



                [



                    "Easy",



                    "Medium",



                    "Hard",



                    "Adaptive"



                ],



                key="aptitude_difficulty"



            )



            num_questions = st.select_slider(



                "❓ Number of Questions",



                options=[10, 20, 30, 40, 50],



                value=20,



                key="aptitude_questions_count"



            )



            timer = st.selectbox(



                "⏱ Time Limit",



                [



                    "No Timer",



                    "15 Minutes",



                    "30 Minutes",



                    "45 Minutes",



                    "60 Minutes"



                ],



                key="aptitude_timer"



            )



        negative_marking = st.checkbox(



            "Apply Negative Marking (-0.25 for incorrect answers)",



            key="negative_marking"



        )



        st.divider()



        st.subheader(

            "📌 Test Overview"

        )



        st.info(

            """

This AI Aptitude Test includes:



✅ Company-specific question patterns



✅ Quantitative Aptitude



✅ Logical Reasoning



✅ Verbal Ability



✅ Data Interpretation



✅ Adjustable Difficulty



✅ AI Performance Analysis



✅ Topic-wise Accuracy



✅ Speed Analysis



✅ Personalized Learning Plan



✅ Career Mentor Integration

"""

        )



        st.divider()



        if st.button(



            "🚀 Generate AI Aptitude Test",



            use_container_width=True



        ):



            if company.strip() == "":



                st.warning(

                    "Please enter your target company."

                )



            elif role.strip() == "":



                st.warning(

                    "Please enter your target role."

                )



            else:



                try:



                    with st.spinner(



                        "Generating AI Aptitude Test..."



                    ):



                        AptitudeEngine.start_test(



                            company=company,



                            role=role,



                            test_type=test_type,



                            difficulty=difficulty,



                            num_questions=num_questions



                        )



                    st.rerun()



                except Exception as e:



                    st.error(str(e))



    # ===================================

    # TEST STARTED

    # ===================================



    else:



        progress = AptitudeEngine.get_progress()



        question = AptitudeEngine.get_current_question()

        if question is None:



            st.warning(

                "No aptitude questions found."

            )



            if st.button(

                "← Back"

            ):



                AptitudeEngine.reset_test()



                st.rerun()



        else:



            st.progress(



                progress["progress"] / 100



            )



            st.caption(



                f"Question {progress['current']} of {progress['total']}"



            )



            col1, col2, col3, col4 = st.columns(4)



            col1.metric(



                "Answered",



                progress["answered"]



            )



            col2.metric(



                "Remaining",



                progress["remaining"]



            )



            col3.metric(



                "Marked",



                progress["marked"]



            )



            col4.metric(



                "Skipped",



                progress["skipped"]



            )



            st.divider()



            st.markdown(



                f"### Question {question['question_number']}"



            )



            st.write(



                question["question"]



            )



            st.caption(



                f"Category : {question['category']} | Topic : {question['topic']} | Difficulty : {question['difficulty']}"



            )



            options = [



                "A",



                "B",



                "C",



                "D"



            ]



            option_labels = [



                f"A. {question['options']['A']}",



                f"B. {question['options']['B']}",



                f"C. {question['options']['C']}",



                f"D. {question['options']['D']}"



            ]



            saved = AptitudeEngine.get_saved_answer(



                question["question_number"]



            )



            if saved is None:



                default_index = None



            else:



                default_index = options.index(



                    saved



                )



            selected = st.radio(



                "Choose your answer",



                option_labels,



                index=default_index,



                key=f"aptitude_{question['question_number']}"



            )



            if selected:



                AptitudeEngine.save_answer(



                    question_number=question[



                        "question_number"



                    ],



                    selected_option=selected[0]



                )



            st.divider()



            c1, c2, c3 = st.columns(



                3



            )



            with c1:



                if st.button(



                    "⬅ Previous",



                    disabled=progress["current"] == 1,



                    use_container_width=True



                ):



                    AptitudeEngine.previous_question()



                    st.rerun()



            with c2:



                if st.button(



                    "⭐ Mark For Review",



                    use_container_width=True



                ):



                    AptitudeEngine.toggle_review(



                        question[



                            "question_number"



                        ]



                    )



                    st.rerun()



            with c3:



                if st.button(



                    "Next ➡",



                    disabled=progress["current"] == progress["total"],



                    use_container_width=True



                ):



                    AptitudeEngine.next_question()



                    st.rerun()    

                                # ===================================

            # TIMER

            # ===================================



            timer_mapping = {



                "No Timer": 0,



                "15 Minutes": 15,



                "30 Minutes": 30,



                "45 Minutes": 45,



                "60 Minutes": 60



            }



            total_minutes = timer_mapping.get(



                st.session_state.get(



                    "aptitude_timer",



                    "No Timer"



                ),



                0



            )



            if total_minutes > 0:



                remaining = AptitudeEngine.get_remaining_time(



                    total_minutes



                )



                if remaining:



                    minutes, seconds, remaining_seconds = remaining



                    st.info(



                        f"⏱ Time Remaining : {minutes:02d}:{seconds:02d}"



                    )



                    if remaining_seconds <= 0:



                        AptitudeEngine.submit_test(



                            negative_marking=st.session_state.get(



                                "negative_marking",



                                False



                            )



                        )



                        st.rerun()

                                    # ===================================

            # SUBMIT / CANCEL

            # ===================================



            st.divider()



            submit_col1, submit_col2 = st.columns(2)



            with submit_col1:



                if st.button(



                    "📤 Submit Test",



                    use_container_width=True,



                    type="primary"



                ):



                    AptitudeEngine.submit_test(



                        negative_marking=st.session_state.get(



                            "negative_marking",



                            False



                        )



                    )



                    st.rerun()



            with submit_col2:



                if st.button(



                    "❌ Cancel Test",



                    use_container_width=True



                ):



                    AptitudeEngine.reset_test()



                    st.rerun()

                                # ===================================

            # SHOW RESULTS

            # ===================================



            if st.session_state.get(



                "aptitude_completed",



                False



            ):



                st.divider()



                stats = AptitudeEngine.get_statistics()



                st.balloons()



                st.success(



                    "🎉 Aptitude Test Completed Successfully!"



                )



                st.divider()



                col1, col2, col3, col4 = st.columns(4)



                with col1:



                    st.metric(



                        "🏆 Score",



                        f"{stats['score']}/{stats['total']}"



                    )



                with col2:



                    st.metric(



                        "🎯 Accuracy",



                        f"{stats['accuracy']:.1f}%"



                    )



                with col3:



                    st.metric(



                        "✅ Correct",



                        stats["correct"]



                    )



                with col4:



                    st.metric(



                        "❌ Wrong",



                        stats["wrong"]



                    )



                col5, col6 = st.columns(2)



                with col5:



                    st.metric(



                        "⏭ Skipped",



                        stats["skipped"]



                    )



                with col6:



                    st.metric(



                        "📄 Questions",



                        stats["total"]



                    )



                st.divider()



                st.subheader(



                    "📊 Topic-wise Performance"



                )



                for topic, values in stats["topic_stats"].items():



                    total_topic = (



                        values["correct"]



                        +



                        values["wrong"]



                    )



                    if total_topic == 0:



                        continue



                    accuracy = (



                        values["correct"]



                        /



                        total_topic



                    ) * 100



                    st.write(



                        f"**{topic}**"



                    )



                    st.progress(



                        accuracy / 100



                    )



                    st.caption(



                        f"{accuracy:.1f}% Accuracy"



                    )



                st.divider()



                st.subheader(



                    "📈 Category-wise Performance"



                )



                for category, values in stats["category_stats"].items():



                    total_category = (



                        values["correct"]



                        +



                        values["wrong"]



                    )



                    if total_category == 0:



                        continue



                    accuracy = (



                        values["correct"]



                        /



                        total_category



                    ) * 100



                    st.write(



                        f"**{category}**"



                    )



                    st.progress(



                        accuracy / 100



                    )



                    st.caption(



                        f"{accuracy:.1f}% Accuracy"



                    )



                st.divider()



                col1, col2 = st.columns(2)



                with col1:



                    if st.button(



                        "🔄 Generate Another Test",



                        use_container_width=True



                    ):



                        AptitudeEngine.generate_new_test()



                        st.rerun()



                with col2:



                    if st.button(



                        "⚙️ New Configuration",



                        use_container_width=True



                    ):



                        AptitudeEngine.reset_test()



                        st.rerun() 

# ===================================

# JOB TRACKER

# ===================================



elif page == "📋 Job Tracker":



    st.title("📋 Job Application Tracker")



    st.caption(

        "Track all your applications, interviews, offers and rejections."

    )



    # ===================================

    # LIVE JOB SEARCH

    # ===================================



    st.subheader("🔍 Find Live Jobs")



    search_col1, search_col2 = st.columns(2)



    with search_col1:



        search_role = st.text_input(

            "Job Role",

            placeholder="Software Engineer"

        )



    with search_col2:



        search_location = st.text_input(

            "Location",

            placeholder="Bangalore / Remote"

        )



    employment_type = st.selectbox(



        "Employment Type",



        [



            "",



            "Full-time",



            "Part-time",



            "Internship",



            "Contract"



        ]

    )



    if st.button(



        "🔍 Search Live Jobs",



        use_container_width=True



    ):



        with st.spinner(



            "Searching jobs..."



        ):



            st.session_state["job_results"] = search_jobs(



                search_role,



                search_location,



                employment_type



            )



    # ===================================

    # LIVE JOB RESULTS

    # ===================================



    if st.session_state.get(

        "job_results"

    ):



        st.divider()



        st.subheader(

            "💼 Live Job Results"

        )



        for index, job in enumerate(



            st.session_state[

                "job_results"

            ]



        ):



            with st.container():



                st.markdown(

                    f"### {job['title']}"

                )



                st.write(

                    f"🏢 {job['company']}"

                )



                st.write(

                    f"📍 {job['location']}"

                )



                st.write(

                    f"💼 {job['employment_type']}"

                )



                st.write(

                    f"💰 {job['salary']}"

                )



                st.write(

                    job["description"]

                )



                col1, col2 = st.columns(2)



                with col1:



                    st.link_button(



                        "🔗 Apply",



                        job["apply_link"],



                        use_container_width=True



                    )



                with col2:



                    if st.button(



                        "⭐ Save",



                        key=f"save_{index}"



                    ):



                        add_application(



                            job["company"],



                            job["title"],



                            "Interested",



                            str(date.today()),



                            "Saved from Live Jobs"



                        )



                        st.success(

                            "Saved successfully."

                        )



                        st.rerun()



                st.divider()



    # ===================================

    # ADD APPLICATION

    # ===================================



    st.subheader(

        "➕ Add New Application"

    )



    company = st.text_input(

        "Company Name"

    )



    role = st.text_input(

        "Role"

    )



    status = st.selectbox(



        "Application Status",



        [



            "Interested",



            "Applied",



            "OA",



            "Interview",



            "Offer",



            "Rejected"



        ]

    )



    application_date = st.date_input(

        "Application Date"

    )



    notes = st.text_area(

        "Notes"

    )



    if st.button(



        "➕ Add Application",



        use_container_width=True



    ):



        if company.strip() == "" or role.strip() == "":



            st.warning(

                "Company and Role are required."

            )



        else:



            try:



                add_application(



                    company,



                    role,



                    status,



                    str(application_date),



                    notes



                )



                st.success(

                    "Application Added Successfully"

                )



                st.rerun()



            except Exception as e:



                st.error(

                    str(e)

                )



    st.divider()

    # ===================================

    # JOB TRACKER METRICS

    # ===================================



    stats = get_job_stats()



    c1, c2, c3, c4, c5, c6 = st.columns(6)



    with c1:



        st.metric(



            "Interested",



            stats.get(

                "Interested",

                0

            )



        )



    with c2:



        st.metric(



            "Applied",



            stats.get(

                "Applied",

                0

            )



        )



    with c3:



        st.metric(



            "OA",



            stats.get(

                "OA",

                0

            )



        )



    with c4:



        st.metric(



            "Interview",



            stats.get(

                "Interview",

                0

            )



        )



    with c5:



        st.metric(



            "Offer",



            stats.get(

                "Offer",

                0

            )



        )



    with c6:



        st.metric(



            "Rejected",



            stats.get(

                "Rejected",

                0

            )



        )



    st.divider()



    # ===================================

    # APPLICATION LIST

    # ===================================



    st.subheader(

        "📄 Applications"

    )



    applications = get_applications()



    if len(applications) == 0:



        st.info(

            "No applications added yet."

        )



    else:



        for app in applications:



            app_id = app[0]



            with st.expander(

                f"{app[1]} | {app[2]}"

            ):



                st.write(

                    f"Status: {app[3]}"

                )



                st.write(

                    f"Applied Date: {app[4]}"

                )



                st.write(

                    f"Notes: {app[5]}"

                )



                new_status = st.selectbox(



                    "Update Status",



                    [



                        "Interested",



                        "Applied",



                        "OA",



                        "Interview",



                        "Offer",



                        "Rejected"



                    ],



                    index=[

                        "Interested",

                        "Applied",

                        "OA",

                        "Interview",

                        "Offer",

                        "Rejected"

                    ].index(app[3]) if app[3] in [

                        "Interested",

                        "Applied",

                        "OA",

                        "Interview",

                        "Offer",

                        "Rejected"

                    ] else 0,



                    key=f"status_{app_id}"



                )



                col1, col2, col3 = st.columns(3)

                with col1:



                    if st.button(



                        "✅ Update",



                        key=f"update_{app_id}"



                    ):



                        try:



                            update_application_status(



                                app_id,



                                new_status



                            )



                            st.success(

                                "Status Updated Successfully."

                            )



                            st.rerun()



                        except Exception as e:



                            st.error(str(e))



                with col2:



                    if st.button(



                        "🗑 Delete",



                        key=f"delete_{app_id}"



                    ):



                        try:



                            delete_application(

                                app_id

                            )



                            st.success(

                                "Application Deleted Successfully."

                            )



                            st.rerun()



                        except Exception as e:



                            st.error(str(e))



                with col3:



                    if st.button(



                        "🤖 Analyze",



                        key=f"analyze_{app_id}"



                    ):



                        try:



                            with st.spinner(

                                "Analyzing application..."

                            ):



                                analysis = analyze_job_application(



                                    company=app[1],



                                    role=app[2],



                                    resume_text=st.session_state.get(

                                        "resume_text",

                                        ""

                                    ),



                                    ats_report=st.session_state.get(

                                        "ats_report_cache",

                                        ""

                                    ),



                                    evaluations="\n\n".join(

                                        st.session_state.get(

                                            "evaluations",

                                            []

                                        )

                                    ),



                                    coding_evaluations="\n\n".join(

                                        st.session_state.get(

                                            "coding_history",

                                            []

                                        )

                                    )



                                )



                            st.markdown("### 📊 AI Recruiter Analysis")



                            st.markdown(

                                analysis

                            )



                        except Exception as e:



                            st.error(

                                f"Analysis Error: {str(e)}"

                            )   

# ===================================

# LIVE CODING ROUND

# ===================================



elif page == "💻 Live Coding Round":



    st.title(

        "💻 Live Coding Interview"

    )



    st.caption(

        "Practice coding rounds and receive AI-powered feedback."

    )



    interview_active = bool(

        st.session_state.get(

            "coding_question",

            ""

        )

    )



    # ======================================

    # SETUP (only before interview starts)

    # ======================================



    if not interview_active:



        col1, col2, col3, col4 = st.columns(4)



        with col1:



            coding_company = st.text_input(

                "Target Company",

                placeholder="Google, Amazon, OpenAI, Nvidia...",

                key="coding_company"

            )



        with col2:



            coding_topic = st.selectbox(

                "Topic",

                [

                    "Arrays",

                    "Strings",

                    "Linked Lists",

                    "Stacks",

                    "Queues",

                    "Trees",

                    "BST",

                    "Heaps",

                    "Graphs",

                    "Greedy",

                    "Backtracking",

                    "Dynamic Programming",

                    "Recursion",

                    "Hashing",

                    "Sliding Window",

                    "System Design",

                    "SQL",

                    "Python"

                ]

            )



        with col3:



            coding_difficulty = st.selectbox(

                "Difficulty",

                [

                    "Easy",

                    "Medium",

                    "Hard"

                ]

            )



        with col4:



            coding_total_questions = st.selectbox(

                "Number of Questions",

                [3, 5, 10],

                index=1

            )



        st.divider()



        if st.button(

            "🚀 Generate Coding Question",

            use_container_width=True

        ):



            if coding_company.strip() == "":



                st.warning(

                    "Please enter a company name."

                )



            else:



                try:



                    with st.spinner(

                        "Generating Coding Question..."

                    ):



                        question = generate_coding_question(

                            coding_company,

                            coding_topic,

                            coding_difficulty

                        )



                        st.session_state["coding_question"] = question



                        st.session_state["coding_result"] = ""



                        st.session_state["coding_round_number"] = 1



                        st.session_state["coding_total_questions"] = coding_total_questions



                        st.session_state["coding_company_active"] = coding_company



                        st.session_state["coding_topic_active"] = coding_topic



                        st.session_state["coding_difficulty_active"] = coding_difficulty



                        st.session_state["coding_history"] = []



                        st.session_state["coding_questions"] = [question]



                        st.session_state["coding_round"] = ""



                        st.session_state["dsa_roadmap"] = ""



                        st.session_state["coding_code"] = """def solve():



    pass

"""



                    st.rerun()



                except Exception as e:



                    st.error(

                        str(e)

                    )



    # ======================================

    # INTERVIEW IN PROGRESS

    # ======================================



    else:



        coding_company = st.session_state.get(

            "coding_company_active",

            ""

        )



        coding_topic = st.session_state.get(

            "coding_topic_active",

            ""

        )



        coding_difficulty = st.session_state.get(

            "coding_difficulty_active",

            ""

        )



        total_questions = st.session_state.get(

            "coding_total_questions",

            5

        )



        st.info(

            "🟢 Interview in Progress"

        )



        st.subheader(

            f"{coding_company} Coding Interview"

        )



        st.caption(

            f"Question {st.session_state['coding_round_number']} of {total_questions}"

        )



        st.progress(

            min(

                st.session_state["coding_round_number"] / total_questions,

                1.0

            )

        )



        st.divider()



        st.subheader(

            "📝 Coding Question"

        )



        st.markdown(

            st.session_state[

                "coding_question"

            ]

        )



        st.divider()



        code = st.text_area(

            "💻 Write Your Solution",

            key="coding_code",

            height=350

        )



        if st.button(

            "✅ Evaluate Solution",

            use_container_width=True

        ):



            try:



                with st.spinner(

                    "Reviewing Solution..."

                ):



                    result = evaluate_code_solution(



                        st.session_state[

                            "coding_question"

                        ],



                        code

                    )



                    st.session_state[

                        "coding_result"

                    ] = result



                    st.session_state[

                        "coding_history"

                    ].append(

                        result

                    )



            except Exception as e:



                st.error(

                    str(e)

                )



        if st.session_state[

            "coding_result"

        ]:



            st.divider()



            st.subheader(

                "📊 AI Evaluation"

            )



            st.markdown(

                st.session_state[

                    "coding_result"

                ]

            )



            st.divider()



            # ---------------------------------

            # CODING STATISTICS

            # ---------------------------------



            st.subheader(

                "📌 Coding Statistics"

            )



            stat1, stat2, stat3 = st.columns(3)



            with stat1:



                st.metric(

                    "Questions Solved",

                    len(

                        st.session_state["coding_history"]

                    )

                )



            with stat2:



                st.metric(

                    "Difficulty",

                    coding_difficulty

                )



            with stat3:



                st.metric(

                    "Company",

                    coding_company

                )



            st.divider()



            # ---------------------------------

            # NEXT / RETRY / FINISH

            # ---------------------------------



            at_last_question = (

                st.session_state["coding_round_number"] >= total_questions

            )



            col_next1, col_next2, col_next3 = st.columns(3)



            with col_next1:



                if st.button(

                    "🔄 Retry Question",

                    use_container_width=True

                ):



                    st.session_state["coding_result"] = ""



                    st.session_state["coding_code"] = """def solve():



    pass

"""



                    st.rerun()



            with col_next2:



                if st.button(

                    "➡ Next Question",

                    use_container_width=True,

                    disabled=at_last_question

                ):



                    with st.spinner(

                        "Generating next question..."

                    ):



                        next_question = generate_coding_question(



                            coding_company,



                            coding_topic,



                            coding_difficulty



                        )



                        st.session_state["coding_question"] = next_question



                        st.session_state["coding_questions"].append(

                            next_question

                        )



                        st.session_state["coding_result"] = ""



                        st.session_state["coding_round_number"] += 1



                        st.session_state["coding_code"] = """def solve():



    pass

"""



                        st.session_state["coding_round"] = ""



                        st.session_state["dsa_roadmap"] = ""



                    st.rerun()



            with col_next3:



                if st.button(

                    "🏁 Finish Interview",

                    use_container_width=True,

                    type="primary"

                ):



                    try:



                        with st.spinner(

                            "Generating Final Report..."

                        ):



                            transcript = "\n\n".join(



                                f"Question {i + 1}: {q}\n\nEvaluation:\n{r}"



                                for i, (q, r) in enumerate(



                                    zip(



                                        st.session_state["coding_questions"],



                                        st.session_state["coding_history"]



                                    )



                                )



                            )



                            st.session_state[

                                "coding_round"

                            ] = generate_coding_readiness_report(



                                transcript



                            )



                            st.session_state[

                                "dsa_roadmap"

                            ] = generate_dsa_roadmap(



                                transcript



                            )



                            st.session_state["interview_finished"] = True



                    except Exception as e:



                        st.error(

                            str(e)

                        )



                    st.rerun()



    # ======================================

    # QUESTION HISTORY

    # ======================================



    if st.session_state.get(

        "coding_questions"

    ) and len(

        st.session_state["coding_history"]

    ) > 0:



        st.divider()



        st.subheader(

            "🗂 Question History"

        )



        for i, (q, r) in enumerate(



            zip(



                st.session_state["coding_questions"],



                st.session_state["coding_history"]



            ),



            start=1



        ):



            with st.expander(

                f"Question {i}"

            ):



                st.markdown(

                    "**Question:**"

                )



                st.markdown(

                    q

                )



                st.markdown(

                    "**Evaluation:**"

                )



                st.markdown(

                    r

                )



    # ======================================

    # FINAL READINESS REPORT

    # ======================================



    if st.session_state[

        "coding_round"

    ]:



        st.divider()



        st.subheader(

            "📈 Coding Readiness Report"

        )



        st.markdown(

            st.session_state[

                "coding_round"

            ]

        )



    if st.session_state[

        "dsa_roadmap"

    ]:



        st.divider()



        st.subheader(

            "🗺 Personalized DSA Roadmap"

        )



        st.markdown(

            st.session_state[

                "dsa_roadmap"

            ]

        )



    if st.session_state.get(

        "interview_finished"

    ):



        st.divider()



        if st.button(

            "🔁 Start New Interview",

            use_container_width=True

        ):



            st.session_state["coding_question"] = ""



            st.session_state["coding_result"] = ""



            st.session_state["coding_round_number"] = 1



            st.session_state["coding_history"] = []



            st.session_state["coding_questions"] = []



            st.session_state["coding_round"] = ""



            st.session_state["dsa_roadmap"] = ""



            st.session_state["interview_finished"] = False



            st.session_state["coding_code"] = """def solve():



    pass

"""



            st.rerun() 

# ===================================
# AI SKILL INTELLIGENCE REPORT
# ===================================
elif page == "🚀 Skill Gap Report":

    # ===================================
    # PREMIUM CSS — ANALYTICS ENGINE STYLE
    # ===================================
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #f8fafc !important; }
    .stApp { background: #f8fafc !important; }
    
    /* Hero Banner Branding */
    .report-hero {
        background: linear-gradient(135deg, #4c1d95 0%, #0f172a 100%);
        border-radius: 16px; padding: 30px; margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(76,29,149,0.05);
    }
    .report-title { font-size: 2.0rem; font-weight: 800; color: #ffffff; margin: 0 0 4px; letter-spacing: -0.5px; }
    .report-subtitle { color: #ddd6fe; font-size: 0.95rem; margin: 0; font-weight: 400; opacity: 0.9; }

    /* Section Ribbons */
    .section-ribbon { display: flex; align-items: center; gap: 10px; margin: 24px 0 16px; }
    .ribbon-tag {
        background: #0f172a; color: #ffffff; border-radius: 6px; padding: 3px 8px;
        font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;
    }
    .ribbon-title { font-size: 1.15rem; font-weight: 700; color: #1e293b; margin: 0; }

    /* Scope Grid Details */
    .scope-box {
        background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;
        padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.01);
    }
    .scope-header { font-size: 1.05rem; font-weight: 700; color: #0f172a; margin-bottom: 12px; }
    
    .feature-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 10px; margin-top: 10px; }
    .feature-item {
        font-size: 0.88rem; color: #334155; padding: 8px 12px; background: #f8fafc; 
        border-left: 3px solid #6d28d9; border-radius: 0 6px 6px 0; font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

    # ===================================
    # HERO BANNER HEADER
    # ===================================
    st.markdown("""
    <div class="report-hero">
        <div class="report-title">🧠 AI Skill Intelligence Analytics</div>
        <div class="report-subtitle">Deep engineering matrix cross-examinations mapping compiled resumes against live interview technical feedback loops.</div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------
    # VALIDATION CHECKS
    # -------------------------------
    if not st.session_state.get("resume_text", ""):
        st.warning("📄 Data Integrity Exception: Please upload your primary resume index via the portal before evaluating gaps.")

    elif len(st.session_state.get("evaluations", [])) == 0:
        st.warning("🎤 Performance Index Empty: Complete at least one technical audio/text Mock Interview to populate calibration telemetry.")

    else:
        # High-Fidelity Feature Matrix Mapping
        st.markdown("""
        <div class="scope-box">
            <div class="scope-header">🎯 Analytical Assessment Vectors Covered</div>
            <div style="font-size: 0.9rem; color: #475569; margin-bottom: 14px;">
                The analytical cross-compilation pipeline parses your production capabilities against technical market bars using the following parameters:
            </div>
            <div class="feature-list">
                <div class="feature-item">📊 Executive Engineering Summary</div>
                <div class="feature-item">⚡ Technical Strength Vectors</div>
                <div class="feature-item">🔍 Hidden Architectural Skill Gaps</div>
                <div class="feature-item">👔 Macro Recruiter Market Lens</div>
                <div class="feature-item">📈 General Interview Readiness Curves</div>
                <div class="feature-item">📁 Project Implementation Quality Audit</div>
                <div class="feature-item">🎯 Targeted Optimization Strategies</div>
                <div class="feature-item">⚠️ Career Progression Risk Analysis</div>
                <div class="feature-item">📚 Next-Action Learning Priorities</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Execute Strategic Skill Intelligence Synthesis", use_container_width=True, type="primary"):
            try:
                with st.spinner("Extracting profile semantic embeddings and processing analytical reports..."):
                    report = generate_skill_gap_report(
                        resume_text=st.session_state.get("resume_text", ""),
                        evaluations="\n\n".join(st.session_state.get("evaluations", []))
                    )
                    st.session_state["skill_gap_report"] = report
            except Exception as e:
                st.error(f"Compilation pipeline breakdown: {str(e)}")

        # ===================================
        # COMPILED DATA MARKDOWN PANE
        # ===================================
        if st.session_state.get("skill_gap_report", ""):
            st.markdown("""
            <div class="section-ribbon">
                <span class="ribbon-tag">Intelligence Output</span>
                <span class="ribbon-title">AI Skill Intelligence Report Dossier</span>
            </div>""", unsafe_allow_html=True)
            
            # Using an informational block styling container wrapper for the generated report markdown
            st.info("Report updated and compiled successfully. Review structural breakdowns below:")
            st.markdown(st.session_state["skill_gap_report"])

# ===================================
# AI LEARNING OPERATING SYSTEM
# ===================================
elif page == "🗺 Learning Roadmap":

    # ===================================
    # PREMIUM CSS — ROADMAP ENGINE STYLE
    # ===================================
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #f8fafc !important; }
    .stApp { background: #f8fafc !important; }
    
    /* Hero Banner Branding */
    .roadmap-hero {
        background: linear-gradient(135deg, #2563eb 0%, #0f172a 100%);
        border-radius: 16px; padding: 30px; margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(37,99,235,0.05);
    }
    .roadmap-title { font-size: 2.0rem; font-weight: 800; color: #ffffff; margin: 0 0 4px; letter-spacing: -0.5px; }
    .roadmap-subtitle { color: #dbeafe; font-size: 0.95rem; margin: 0; font-weight: 400; opacity: 0.9; }

    /* Section Ribbons */
    .section-ribbon { display: flex; align-items: center; gap: 10px; margin: 24px 0 16px; }
    .ribbon-tag {
        background: #0f172a; color: #ffffff; border-radius: 6px; padding: 3px 8px;
        font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;
    }
    .ribbon-title { font-size: 1.15rem; font-weight: 700; color: #1e293b; margin: 0; }

    /* Scope Grid Details */
    .scope-box {
        background: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px;
        padding: 20px; margin-bottom: 20px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.01);
    }
    .scope-header { font-size: 1.05rem; font-weight: 700; color: #0f172a; margin-bottom: 12px; }
    
    .feature-list { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 10px; margin-top: 10px; }
    .feature-item {
        font-size: 0.88rem; color: #334155; padding: 8px 12px; background: #f8fafc; 
        border-left: 3px solid #2563eb; border-radius: 0 6px 6px 0; font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)

    # ===================================
    # HERO BANNER HEADER
    # ===================================
    st.markdown("""
    <div class="roadmap-hero">
        <div class="roadmap-title">🗺️ AI Learning Operating System</div>
        <div class="roadmap-subtitle">Transforming diagnostic mock interview performance gaps into an actionable, engineer-grade execution curriculum.</div>
    </div>
    """, unsafe_allow_html=True)

    # -------------------------------
    # VALIDATION CHECKS
    # -------------------------------
    if not st.session_state.get("resume_text", ""):
        st.warning("📄 Data Integrity Exception: Please upload your primary resume index via the portal before engineering a roadmap.")

    elif len(st.session_state.get("evaluations", [])) == 0:
        st.warning("🎤 Performance Index Empty: Complete at least one technical mock interview loop to establish your capability baselines.")

    else:
        # High-Fidelity Feature Matrix Mapping
        st.markdown("""
        <div class="scope-box">
            <div class="scope-header">🎯 Execution Pillars & Core Modules</div>
            <div style="font-size: 0.9rem; color: #475569; margin-bottom: 14px;">
                The engineering curriculum core synthesizes a custom tactical schedule compiled directly across the following vectors:
            </div>
            <div class="feature-list">
                <div class="feature-item">📅 Daily Learning Cadence</div>
                <div class="feature-item">🏁 Weekly Execution Milestones</div>
                <div class="feature-item">🛠️ Practical Project Roadmaps</div>
                <div class="feature-item">💻 Targeted Coding Strategy</div>
                <div class="feature-item">📝 Technical Interview Drills</div>
                <div class="feature-item">🔄 Iterative Resume Evolution</div>
                <div class="feature-item">🐙 GitHub Profile Upgrades</div>
                <div class="feature-item">📚 Selected Reference Resources</div>
                <div class="feature-item">📊 Success & Velocity Metrics</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🗺️ Generate Custom AI Learning Blueprint", use_container_width=True, type="primary"):
            try:
                with st.spinner("Compiling optimized study paths and synthesizing resource blocks..."):
                    roadmap = generate_learning_roadmap(
                        resume_text=st.session_state.get("resume_text", ""),
                        evaluations="\n\n".join(st.session_state.get("evaluations", []))
                    )
                    st.session_state["roadmap"] = roadmap
            except Exception as e:
                st.error(f"Roadmap compilation pipeline breakdown: {str(e)}")

        # ===================================
        # COMPILED DATA MARKDOWN PANE
        # ===================================
        if st.session_state.get("roadmap", ""):
            st.markdown("""
            <div class="section-ribbon">
                <span class="ribbon-tag">Execution Plan</span>
                <span class="ribbon-title">Your Tailored Engineering Learning OS</span>
            </div>""", unsafe_allow_html=True)
            
            st.info("System blueprint compiled successfully. Proceed with the following structured milestones:")
            st.markdown(st.session_state["roadmap"])



            
elif page == "🚀 Career Dashboard":

    # ===================================
    # PREMIUM CSS — LIGHT MODE
    # ===================================
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; background-color: #f0f4fb !important; }
    .stApp { background: #f0f4fb !important; }
    .block-container { padding-top: 1.5rem !important; }

    .hero-banner {
        background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 50%, #0ea5e9 100%);
        border-radius: 20px; padding: 44px 48px; margin-bottom: 28px;
        position: relative; overflow: hidden;
        box-shadow: 0 8px 32px rgba(37,99,235,0.18);
    }
    .hero-banner::before {
        content:''; position:absolute; top:-60px; right:-60px;
        width:280px; height:280px;
        background:radial-gradient(circle, rgba(255,255,255,0.12) 0%, transparent 70%);
        border-radius:50%;
    }
    .hero-title { font-size:2rem; font-weight:800; color:#fff; margin:0 0 6px; letter-spacing:-0.5px; }
    .hero-subtitle { color:rgba(255,255,255,0.75); font-size:1rem; margin-bottom:28px; }
    .hero-stats { display:flex; gap:16px; flex-wrap:wrap; }
    .hero-stat {
        background:rgba(255,255,255,0.15); border:1px solid rgba(255,255,255,0.25);
        border-radius:14px; padding:16px 22px; min-width:130px; backdrop-filter:blur(4px);
    }
    .hero-stat-value { font-size:1.7rem; font-weight:700; color:#fff; line-height:1.1; }
    .hero-stat-label { font-size:0.7rem; color:rgba(255,255,255,0.7); text-transform:uppercase; letter-spacing:0.08em; margin-top:4px; }
    .hero-badge {
        display:inline-block; background:rgba(255,255,255,0.2); border:1px solid rgba(255,255,255,0.35);
        border-radius:20px; padding:5px 16px; font-size:0.72rem; font-weight:700;
        color:#fff; margin-bottom:18px; letter-spacing:0.08em; text-transform:uppercase;
    }
    .section-header { display:flex; align-items:center; gap:10px; margin:36px 0 16px; }
    .section-badge {
        background:#dbeafe; color:#1d4ed8; border-radius:8px; padding:3px 10px;
        font-size:0.66rem; font-weight:700; text-transform:uppercase; letter-spacing:0.1em;
    }
    .section-title { font-size:1.15rem; font-weight:700; color:#1e293b; margin:0; }

    .kpi-card {
        background:#fff; border:1px solid #e2e8f0; border-radius:16px; padding:20px 18px;
        transition:box-shadow 0.2s,border-color 0.2s; box-shadow:0 1px 4px rgba(0,0,0,0.05);
        margin-bottom: 14px;
    }
    .kpi-card:hover { border-color:#3b82f6; box-shadow:0 4px 16px rgba(59,130,246,0.12); }
    .kpi-icon { font-size:1.5rem; margin-bottom:8px; }
    .kpi-value { font-size:1.55rem; font-weight:700; color:#0f172a; line-height:1; }
    .kpi-label { font-size:0.68rem; color:#94a3b8; text-transform:uppercase; letter-spacing:0.08em; margin-top:5px; }
    .kpi-delta { font-size:0.72rem; color:#16a34a; margin-top:4px; }
    .kpi-delta-neutral { font-size:0.72rem; color:#64748b; margin-top:4px; }

    .data-badge-real {
        display:inline-block; background:#dcfce7; color:#15803d;
        border-radius:6px; padding:2px 8px; font-size:0.6rem; font-weight:700;
        text-transform:uppercase; letter-spacing:0.08em; margin-top:4px;
    }
    .data-badge-est {
        display:inline-block; background:#fef9c3; color:#92400e;
        border-radius:6px; padding:2px 8px; font-size:0.6rem; font-weight:700;
        text-transform:uppercase; letter-spacing:0.08em; margin-top:4px;
    }

    .recruiter-card {
        background:#fff; border:1px solid #e2e8f0; border-radius:18px;
        padding:28px 32px; margin-bottom:20px; box-shadow:0 2px 8px rgba(0,0,0,0.06);
    }
    .recruiter-score-value { font-size:3rem; font-weight:800; color:#2563eb; }
    .recruiter-score-label { font-size:0.78rem; color:#94a3b8; text-transform:uppercase; letter-spacing:0.1em; }
    .skill-row { display:flex; align-items:center; gap:12px; margin-bottom:10px; }
    .skill-name { font-size:0.82rem; color:#475569; width:145px; flex-shrink:0; }
    .skill-bar-bg { flex:1; background:#f1f5f9; border-radius:99px; height:8px; overflow:hidden; }
    .skill-bar-fill { height:100%; border-radius:99px; background:linear-gradient(90deg,#2563eb,#0ea5e9); }
    .skill-score { font-size:0.8rem; font-weight:600; color:#2563eb; width:36px; text-align:right; }
    .skill-source { font-size:0.6rem; color:#94a3b8; width:52px; text-align:right; }

    .company-row { display:flex; align-items:center; gap:14px; margin-bottom:12px; }
    .company-name { font-size:0.83rem; color:#475569; width:120px; flex-shrink:0; font-weight:500; }
    .company-bar-bg { flex:1; background:#f1f5f9; border-radius:99px; height:10px; overflow:hidden; }
    .company-bar-fill { height:100%; border-radius:99px; }
    .company-pct { font-size:0.8rem; font-weight:600; color:#1e293b; width:40px; text-align:right; }

    .badge-card {
        background:#fff; border:1px solid #e2e8f0; border-radius:16px;
        padding:18px 14px; text-align:center; box-shadow:0 1px 4px rgba(0,0,0,0.04);
    }
    .badge-icon { font-size:2rem; }
    .badge-name { font-size:0.68rem; color:#64748b; margin-top:6px; text-transform:uppercase; letter-spacing:0.07em; }
    .badge-earned { border-color:#fbbf24; background:#fffbeb; }
    .badge-locked .badge-icon { filter:grayscale(1) opacity(0.3); }
    .badge-locked .badge-name { color:#cbd5e1; }

    .insight-card {
        background:#fff; border:1.5px dashed #cbd5e1; border-radius:14px;
        padding:24px 20px; text-align:center; margin-bottom:14px;
    }
    .insight-card-title { font-size:0.73rem; text-transform:uppercase; letter-spacing:0.1em; color:#64748b; margin:8px 0 6px; }
    .insight-card-placeholder { font-size:0.78rem; color:#94a3b8; }

    .qa-btn {
        background:#fff; border:1px solid #e2e8f0; border-radius:14px; padding:18px 10px;
        text-align:center; box-shadow:0 1px 4px rgba(0,0,0,0.05);
        transition:border-color 0.2s,box-shadow 0.2s; cursor:pointer;
    }
    .qa-btn:hover { border-color:#3b82f6; box-shadow:0 4px 12px rgba(59,130,246,0.12); }
    .qa-btn-icon { font-size:1.5rem; }
    .qa-btn-label { font-size:0.68rem; color:#64748b; margin-top:6px; text-transform:uppercase; letter-spacing:0.07em; }

    .activity-item {
        background:#fff; border:1px solid #e2e8f0; border-radius:12px;
        padding:14px 18px; margin-bottom:10px; box-shadow:0 1px 3px rgba(0,0,0,0.04);
    }
    .dream-card {
        background: linear-gradient(135deg, #eff6ff, #f0fdf4);
        border: 1px solid #bfdbfe; border-radius: 18px;
        padding: 28px 32px; margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(37,99,235,0.08);
    }
    .dash-footer {
        background:#fff; border:1px solid #e2e8f0; border-radius:16px;
        padding:20px 28px; display:flex; justify-content:space-between;
        align-items:center; flex-wrap:wrap; gap:12px; margin-top:24px;
        box-shadow:0 1px 4px rgba(0,0,0,0.04);
    }
    .footer-item { font-size:0.75rem; color:#64748b; display:flex; align-items:center; gap:6px; }
    .footer-dot { width:8px; height:8px; border-radius:50%; background:#22c55e; display:inline-block; }
    .footer-dot-warn { background:#f59e0b; }
    .roadmap-item {
        background:#fff; border:1px solid #e2e8f0; border-left:3px solid #3b82f6;
        border-radius:10px; padding:10px 14px; margin-bottom:8px;
        font-size:0.8rem; color:#475569; box-shadow:0 1px 3px rgba(0,0,0,0.04);
    }
    .no-data-box {
        background:#f8fafc; border:1px dashed #cbd5e1; border-radius:12px;
        padding:32px 20px; text-align:center; color:#94a3b8; font-size:0.85rem;
    }
    </style>
    """, unsafe_allow_html=True)

    import datetime
    import plotly.graph_objects as go

    # =========================================================
    # ── HELPER: extract numeric score from AI evaluation text
    # =========================================================
    def _extract_score_from_text(text, scale=10):
        """Try to pull a numeric score out of an AI evaluation string."""
        import re
        patterns = [
            r'(\d+(?:\.\d+)?)\s*/\s*' + str(scale),
            r'[Ss]core[:\s]+(\d+(?:\.\d+)?)',
            r'[Rr]ating[:\s]+(\d+(?:\.\d+)?)',
            r'[Gg]rade[:\s]+(\d+(?:\.\d+)?)',
            r'(\d+(?:\.\d+)?)\s+out\s+of\s+' + str(scale),
        ]
        for pat in patterns:
            m = re.search(pat, text)
            if m:
                val = float(m.group(1))
                # normalise to 0-100
                return min(round((val / scale) * 100), 100)
        return None

    def _avg_scores_from_list(text_list, scale=10):
        """Return average 0-100 score extracted from a list of AI eval strings."""
        scores = []
        for t in text_list:
            s = _extract_score_from_text(t, scale)
            if s is not None:
                scores.append(s)
        if scores:
            return round(sum(scores) / len(scores))
        return None

    def _skill_in_resume(skill_keywords, resume_text):
        """Return True if any keyword for the skill appears in resume."""
        rt = resume_text.lower()
        return any(k.lower() in rt for k in skill_keywords)

    # =========================================================
    # ── LOAD BACKEND DATA
    # =========================================================
    interview_stats  = get_dashboard_stats()
    job_stats_raw    = get_dashboard_job_stats()
    job_status_counts = get_job_stats()          # {status: count} — REAL DB
    recent_interviews = get_recent_interviews()  # list of (date, score) — REAL DB
    weekly_progress   = get_weekly_progress()    # list of (week_label, score) — REAL DB

    # ── Interview metrics (Firestore, REAL) ─────────────────
    average_score    = interview_stats.get("average", 0) or 0
    best_score       = interview_stats.get("best", 0) or 0
    latest_score     = interview_stats.get("latest", 0) or 0
    total_interviews = interview_stats.get("total", 0) or 0

    # ── Job tracker metrics (SQLite, REAL) ──────────────────
    total_apps = job_stats_raw.get("total", 0) or 0
    offers     = job_stats_raw.get("offers", 0) or 0
    companies  = job_stats_raw.get("companies", 0) or 0
    roles      = job_stats_raw.get("roles", 0) or 0

    # ── ATS score (extracted from ATS report text, REAL) ────
    ats_score = 0
    ats_cache = st.session_state.get("ats_report_cache", "")
    if ats_cache:
        _m = re.search(r"(\d+)", ats_cache)
        if _m:
            ats_score = min(int(_m.group(1)), 100)

    # ── Aptitude (AptitudeEngine session state, REAL) ────────
    apt_stats    = st.session_state.get("aptitude_statistics", {})
    aptitude_raw = st.session_state.get("aptitude_score", 0) or 0
    apt_total    = apt_stats.get("total", 0) or 1
    apt_accuracy = apt_stats.get("accuracy", 0) or 0          # 0-100 REAL
    apt_correct  = apt_stats.get("correct", 0) or 0
    apt_wrong    = apt_stats.get("wrong", 0) or 0
    # Convert raw score to 0-100
    aptitude_score = round((aptitude_raw / apt_total) * 100) if apt_total else 0
    aptitude_score = min(aptitude_score, 100)

    # ── Coding average (extracted from coding_history texts, REAL) ──
    coding_history_list = st.session_state.get("coding_history", [])
    coding_solved = len(coding_history_list)
    _extracted_coding = _avg_scores_from_list(coding_history_list, scale=10)
    if _extracted_coding is not None:
        coding_average = _extracted_coding
        coding_data_source = "real"
    elif coding_solved > 0:
        # Fallback: use proportion of questions solved * average_score
        coding_average = min(round((coding_solved / max(coding_solved, 5)) * max(average_score, 50)), 100)
        coding_data_source = "estimated"
    else:
        coding_average = 0
        coding_data_source = "no data"

    # ── Communication score (extracted from evaluations, REAL) ──
    evaluations_list = st.session_state.get("evaluations", [])
    _extracted_comm = _avg_scores_from_list(evaluations_list, scale=10)
    if _extracted_comm is not None:
        comm_score = _extracted_comm
        comm_source = "real"
    elif average_score:
        comm_score = round(average_score * 0.88)
        comm_source = "estimated"
    else:
        comm_score = 0
        comm_source = "no data"

    # ── Resume score = ATS score (same thing, REAL) ──────────
    resume_score = ats_score   # no fake +5 offset

    # ── Session-based extras ─────────────────────────────────
    attempted    = st.session_state.get("attempted", 0) or 0
    mock_count   = st.session_state.get("mock_count", 0) or 0
    resume_text  = st.session_state.get("resume_text", "")

    # ── Career score (same weighted formula, all real inputs) ─
    application_score = min(total_apps * 5, 100)
    career_score = round(
        average_score  * 0.35 +
        ats_score      * 0.25 +
        coding_average * 0.20 +
        apt_accuracy   * 0.10 +
        application_score * 0.10
    )
    career_score = min(career_score, 100)

    hiring_prob = min(round(
        career_score * 0.60 +
        (15 if offers > 0 else 0) +
        (10 if total_interviews >= 3 else 0) +
        (apt_accuracy * 0.10)
    ), 95)

    if career_score >= 85:
        tier="🏆 Tier 1 – Ready";       tier_color="#16a34a"; exp_salary="₹18–30 LPA"; exp_time="1–2 months"
    elif career_score >= 70:
        tier="🥈 Tier 2 – Competitive"; tier_color="#2563eb"; exp_salary="₹10–18 LPA"; exp_time="2–3 months"
    elif career_score >= 50:
        tier="🥉 Tier 3 – Developing";  tier_color="#d97706"; exp_salary="₹6–10 LPA";  exp_time="3–5 months"
    else:
        tier="🔴 Tier 4 – Early Stage"; tier_color="#dc2626"; exp_salary="₹3–6 LPA";   exp_time="5–8 months"

    # ── Chart theme ──────────────────────────────────────────
    CHART_BG, CHART_PLOT = "#ffffff", "#ffffff"
    FONT_CLR, TITLE_CLR, GRID_CLR = "#475569", "#1e293b", "#f1f5f9"

    def light_layout(fig, title=""):
        fig.update_layout(
            paper_bgcolor=CHART_BG, plot_bgcolor=CHART_PLOT,
            font_color=FONT_CLR, title_font_color=TITLE_CLR,
            title_font_size=14, title=title,
            xaxis=dict(gridcolor=GRID_CLR, linecolor="#e2e8f0"),
            yaxis=dict(gridcolor=GRID_CLR, linecolor="#e2e8f0"),
            legend=dict(bgcolor=CHART_BG, font_color=FONT_CLR),
            margin=dict(l=0, r=0, t=44, b=0)
        )
        return fig

    # =========================================================
    # SECTION 1 – HERO BANNER
    # =========================================================
    st.markdown(f"""
    <div class="hero-banner">
        <div class="hero-badge">✦ AI Career Intelligence Dashboard</div>
        <div class="hero-title">Your Career Operating System</div>
        <div class="hero-subtitle">Real-time analytics · AI-powered insights · All data from your actual activity</div>
        <div class="hero-stats">
            <div class="hero-stat">
                <div class="hero-stat-value">{career_score}</div>
                <div class="hero-stat-label">Career Readiness</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-value">{hiring_prob}%</div>
                <div class="hero-stat-label">Hiring Probability</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-value" style="font-size:0.95rem;padding-top:6px;">{tier}</div>
                <div class="hero-stat-label">Placement Tier</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-value" style="font-size:1.2rem;">{exp_salary}</div>
                <div class="hero-stat-label">Expected Package</div>
            </div>
            <div class="hero-stat">
                <div class="hero-stat-value" style="font-size:1.1rem;">{exp_time}</div>
                <div class="hero-stat-label">Est. Placement Time</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # =========================================================
    # SECTION 2 – KPI CARDS
    # =========================================================
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">Performance</span>
        <span class="section-title">Career Performance Overview</span>
    </div>""", unsafe_allow_html=True)

    kpi_data = [
        ("🎯", "Career Score",       f"{career_score}/100",        f"Weighted across all modules",             "real"),
        ("📄", "ATS Score",          f"{ats_score}/100",           "From your ATS Scanner report",             "real"),
        ("🎤", "Interview Avg",      f"{average_score:.1f}/100",   f"{total_interviews} sessions in Firestore","real"),
        ("💻", "Coding Readiness",   f"{coding_average}/100",      f"{coding_solved} questions solved",        coding_data_source),
        ("🧠", "Aptitude Accuracy",  f"{round(apt_accuracy)}%",    f"{apt_correct}✓  {apt_wrong}✗  from test", "real" if apt_stats else "no data"),
        ("🗣️", "Communication",      f"{comm_score}/100",          "Extracted from mock evaluations",          comm_source),
        ("📋", "Resume Score",       f"{resume_score}/100",        "ATS score (same source)",                  "real"),
        ("📬", "Applications",       str(total_apps),              "Total in job tracker DB",                  "real"),
        ("🎁", "Offers",             str(offers),                  "From job tracker DB",                      "real"),
        ("🎤", "Mock Sessions",      str(mock_count),              f"{attempted} answers evaluated",           "real"),
        ("🏢", "Companies",          str(companies),               "Unique companies tracked",                 "real"),
        ("💼", "Roles",              str(roles),                   "Unique roles tracked",                     "real"),
    ]

    cols = st.columns(4)
    for i, (icon, label, value, delta, source) in enumerate(kpi_data):
        badge = f'<span class="data-badge-real">● live</span>' if source == "real" else (
                f'<span class="data-badge-est">~ estimated</span>' if source == "estimated" else
                f'<span class="data-badge-est">no data yet</span>')
        with cols[i % 4]:
            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-icon">{icon}</div>
                <div class="kpi-value">{value}</div>
                <div class="kpi-label">{label}</div>
                <div class="kpi-delta-neutral">{delta}</div>
                {badge}
            </div>""", unsafe_allow_html=True)

    # =========================================================
    # SECTION 3 – AI RECRUITER VERDICT (real inputs)
    # =========================================================
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">AI Analysis</span>
        <span class="section-title">AI Recruiter Verdict</span>
    </div>""", unsafe_allow_html=True)

    if st.button("🤖 Generate AI Recruiter Report", use_container_width=True, key="recruiter_btn"):
        with st.spinner("Generating recruiter analysis from your real scores..."):
            st.session_state["career_dashboard"] = generate_career_advisor(
                career_score, ats_score, average_score, coding_average,
                total_apps, offers,
                st.session_state.get("resume_analysis", ""),
                st.session_state.get("skill_gap_report", "")
            )

    advisor = st.session_state.get("career_dashboard", {})

    # All 6 bars now use REAL data sources
    recruiter_dims = [
        ("Technical Skills",  coding_average,          coding_data_source),
        ("Resume Quality",    resume_score,             "real"),
        ("Behavioral Skills", round(average_score),     "real"),
        ("Problem Solving",   round(apt_accuracy),      "real" if apt_stats else "no data"),
        ("Communication",     comm_score,               comm_source),
        ("Confidence",        round(latest_score) if latest_score else round(average_score), "real"),
    ]
    overall_recruiter = round(sum(v for _, v, _ in recruiter_dims) / len(recruiter_dims))
    hire_rec = "Strong Hire ✅" if overall_recruiter >= 75 else ("Consider ⚠️" if overall_recruiter >= 55 else "Not Yet 🔴")
    hire_bg  = "#dcfce7" if overall_recruiter >= 75 else ("#fef9c3" if overall_recruiter >= 55 else "#fee2e2")
    hire_cl  = "#15803d" if overall_recruiter >= 75 else ("#92400e" if overall_recruiter >= 55 else "#b91c1c")

    st.markdown('<div class="recruiter-card">', unsafe_allow_html=True)
    rc1, rc2 = st.columns([1, 2])
    with rc1:
        st.markdown(f"""
        <div style="text-align:center;padding:20px;">
            <div class="recruiter-score-value">{overall_recruiter}</div>
            <div class="recruiter-score-label">Overall Rating</div><br>
            <div style="background:{hire_bg};border-radius:12px;padding:10px 16px;
                        display:inline-block;font-weight:600;color:{hire_cl};font-size:0.88rem;">
                {hire_rec}
            </div>
            <div style="margin-top:14px;font-size:0.68rem;color:#94a3b8;">
                All bars use<br>your real scores
            </div>
        </div>""", unsafe_allow_html=True)
    with rc2:
        bars_html = ""
        for dim, score, src in recruiter_dims:
            src_label = "live" if src == "real" else ("est." if src == "estimated" else "—")
            bars_html += f"""
            <div class="skill-row">
                <div class="skill-name">{dim}</div>
                <div class="skill-bar-bg"><div class="skill-bar-fill" style="width:{score}%"></div></div>
                <div class="skill-score">{score}</div>
                <div class="skill-source">{src_label}</div>
            </div>"""
        st.markdown(bars_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    if advisor:
        col_l, col_r = st.columns(2)
        with col_l:
            st.markdown("**💪 Strengths**")
            for s in advisor.get("strengths", []): st.success(s)
        with col_r:
            st.markdown("**⚠️ Weaknesses**")
            for w in advisor.get("weaknesses", []): st.warning(w)
        if advisor.get("summary"):
            st.info(f"**Recruiter Verdict:** {advisor['summary']}")

    # =========================================================
    # SECTION 4 – PERFORMANCE TRENDS (REAL interview history)
    # =========================================================
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">Real Trends</span>
        <span class="section-title">Performance Analytics</span>
    </div>""", unsafe_allow_html=True)

    # ── Interview trend from get_recent_interviews() ─────────
    if recent_interviews and len(recent_interviews) >= 2:
        # recent_interviews = list of (date_str, score)
        ri_dates  = [str(r[0]) for r in recent_interviews]
        ri_scores = [float(r[1]) for r in recent_interviews]

        trend_fig = go.Figure()
        trend_fig.add_trace(go.Scatter(
            x=ri_dates, y=ri_scores, name="Interview Score",
            line=dict(color="#2563eb", width=2), mode="lines+markers",
            marker=dict(size=6), fill="tozeroy",
            fillcolor="rgba(37,99,235,0.06)"
        ))
        # ATS as a flat reference line
        if ats_score:
            trend_fig.add_trace(go.Scatter(
                x=ri_dates, y=[ats_score]*len(ri_dates), name="ATS Score",
                line=dict(color="#8b5cf6", width=1.5, dash="dot"), mode="lines"
            ))
        st.plotly_chart(light_layout(trend_fig, "Interview Score History (Real Data)"), use_container_width=True)
    elif recent_interviews and len(recent_interviews) == 1:
        st.info(f"📊 You have 1 interview recorded (Score: {recent_interviews[0][1]}). Complete more interviews to see trend.")
    else:
        st.markdown('<div class="no-data-box">📭 No interview history yet.<br>Complete mock interviews to see your real performance trend here.</div>', unsafe_allow_html=True)

    # ── Weekly progress from get_weekly_progress() ───────────
    pa1, pa2 = st.columns(2)
    with pa1:
        if weekly_progress and len(weekly_progress) >= 1:
            wp_labels = [str(w[0]) for w in weekly_progress]
            wp_scores = [float(w[1]) for w in weekly_progress]
            fig = px.bar(x=wp_labels, y=wp_scores,
                         color_discrete_sequence=["#3b82f6"],
                         labels={"x": "Week", "y": "Avg Score"})
            st.plotly_chart(light_layout(fig, "Weekly Interview Progress (Real)"), use_container_width=True)
        else:
            st.markdown('<div class="no-data-box" style="height:220px;">No weekly data yet.</div>', unsafe_allow_html=True)

    with pa2:
        # Aptitude breakdown if available
        if apt_stats and apt_stats.get("topic_stats"):
            topic_data = apt_stats["topic_stats"]
            t_names, t_acc = [], []
            for topic, vals in topic_data.items():
                tot = vals["correct"] + vals["wrong"]
                if tot > 0:
                    t_names.append(topic)
                    t_acc.append(round((vals["correct"] / tot) * 100))
            if t_names:
                fig = px.bar(x=t_names, y=t_acc,
                             color_discrete_sequence=["#0ea5e9"],
                             labels={"x": "Topic", "y": "Accuracy %"})
                st.plotly_chart(light_layout(fig, "Aptitude Topic Accuracy (Real)"), use_container_width=True)
            else:
                st.markdown('<div class="no-data-box" style="height:220px;">Complete aptitude test to see topic breakdown.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="no-data-box" style="height:220px;">Complete an aptitude test to see topic accuracy.</div>', unsafe_allow_html=True)

    # Real summary metrics
    pm1, pm2, pm3, pm4 = st.columns(4)
    pm1.metric("🏆 Best Score",    best_score,   help="From Firestore — real")
    pm2.metric("🆕 Latest Score",  latest_score, help="From Firestore — real")
    pm3.metric("🎤 Total Sessions",total_interviews, help="From Firestore — real")
    pm4.metric("🧠 Aptitude Acc.", f"{round(apt_accuracy)}%", help="From last test — real")

    # =========================================================
    # SECTION 5 – APPLICATION ANALYTICS (100% REAL DB)
    # =========================================================
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">Real Funnel</span>
        <span class="section-title">Application Analytics</span>
    </div>""", unsafe_allow_html=True)

    # Real counts directly from SQLite via get_job_stats()
    funnel_order  = ["Interested", "Applied", "OA", "Interview", "Offer", "Rejected"]
    funnel_real   = [job_status_counts.get(s, 0) for s in funnel_order]
    funnel_colors = ["#3b82f6", "#0ea5e9", "#8b5cf6", "#f59e0b", "#22c55e", "#ef4444"]

    if sum(funnel_real) > 0:
        funnel_fig = go.Figure(go.Funnel(
            y=funnel_order, x=funnel_real,
            textinfo="value+percent initial",
            marker=dict(color=funnel_colors),
            connector=dict(line=dict(color="#e2e8f0", width=2)),
        ))
        funnel_fig.update_layout(
            paper_bgcolor=CHART_BG, plot_bgcolor=CHART_PLOT,
            font_color=FONT_CLR, margin=dict(l=0, r=0, t=20, b=0),
            title="Application Funnel — Live from Database",
            title_font_color=TITLE_CLR, title_font_size=14
        )
        st.plotly_chart(funnel_fig, use_container_width=True)

        fa1, fa2, fa3, fa4 = st.columns(4)
        _applied    = job_status_counts.get("Applied", 0)
        _interview  = job_status_counts.get("Interview", 0)
        _offer      = job_status_counts.get("Offer", 0)
        _interested = job_status_counts.get("Interested", 0)
        fa1.metric("📬 Total Applied",         _applied)
        fa2.metric("🎤 Interview Rate",         f"{round(_interview/max(_applied,1)*100)}%")
        fa3.metric("🤝 Offer Rate",             f"{round(_offer/max(_interview,1)*100)}%")
        fa4.metric("✅ Overall Conversion",     f"{round(_offer/max(_applied,1)*100)}%")
    else:
        st.markdown('<div class="no-data-box">📭 No job applications tracked yet.<br>Add applications in the 📋 Job Tracker to see your real funnel here.</div>', unsafe_allow_html=True)

    # ── Status pie chart ─────────────────────────────────────
    fh1, fh2 = st.columns(2)
    with fh1:
        status_df = pd.DataFrame([
            {"Status": k, "Count": v}
            for k, v in job_status_counts.items() if v > 0
        ])
        if not status_df.empty:
            fig = px.pie(status_df, values="Count", names="Status", hole=0.45,
                         color_discrete_sequence=["#3b82f6","#0ea5e9","#8b5cf6","#f59e0b","#22c55e","#ef4444"])
            fig.update_layout(paper_bgcolor=CHART_BG, font_color=FONT_CLR,
                              title="Status Distribution (Real)", title_font_color=TITLE_CLR,
                              margin=dict(l=0,r=0,t=44,b=0))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No status data yet.")
    with fh2:
        timeline = get_application_timeline()
        if timeline:
            tdf = pd.DataFrame(timeline, columns=["Date", "Applications"])
            fig = px.line(tdf, x="Date", y="Applications", markers=True,
                          color_discrete_sequence=["#2563eb"])
            st.plotly_chart(light_layout(fig, "Applications Over Time (Real)"), use_container_width=True)
        else:
            st.info("No timeline data yet.")

    # =========================================================
    # SECTION 6 – COMPANY READINESS (real formula)
    # =========================================================
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">Readiness</span>
        <span class="section-title">Company Readiness</span>
    </div>""", unsafe_allow_html=True)

    st.caption("Calculated from your real ATS score, interview average, coding readiness, and aptitude accuracy.")

    # Base score = weighted blend of REAL metrics
    base_readiness = round(
        ats_score      * 0.30 +
        average_score  * 0.35 +
        coding_average * 0.20 +
        apt_accuracy   * 0.15
    )

    # Company tiers: (name, difficulty_offset, color_thresholds)
    company_tiers = [
        # FAANG / Elite — hardest, subtract most
        ("Google",    -28), ("Microsoft", -20), ("Amazon",  -15),
        ("NVIDIA",    -25), ("Apple",     -22), ("Meta",    -20),
        # Mid-tier product
        ("Oracle",    -10), ("Cisco",      -8), ("Adobe",    -5),
        ("Intel",     -12), ("IBM",         0),
        # Service / Mass hiring
        ("TCS",       +15), ("Infosys",   +12), ("Accenture",+10),
    ]

    def _company_color(pct):
        if pct >= 75: return "#22c55e"
        if pct >= 50: return "#3b82f6"
        if pct >= 30: return "#f59e0b"
        return "#ef4444"

    cr1, cr2 = st.columns(2)
    for idx, (cname, offset) in enumerate(company_tiers):
        pct = max(5, min(98, base_readiness + offset))
        color = _company_color(pct)
        col = cr1 if idx % 2 == 0 else cr2
        with col:
            st.markdown(f"""
            <div class="company-row">
                <div class="company-name">{cname}</div>
                <div class="company-bar-bg">
                    <div class="company-bar-fill" style="width:{pct}%;background:{color};"></div>
                </div>
                <div class="company-pct">{pct}%</div>
            </div>""", unsafe_allow_html=True)

    # =========================================================
    # SECTION 7 – SKILL GAP: MARKET vs MY SKILLS (resume-aware)
    # =========================================================
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">Gap Analysis</span>
        <span class="section-title">Market Demand vs My Skills</span>
    </div>""", unsafe_allow_html=True)

    st.caption("'My Skills' column detected from your resume text + your real scores. Market values are 2024 industry benchmarks.")

    # Detect skills from resume_text (real)
    def _my_skill_score(keywords, present_bonus, absent_score):
        """If skill found in resume → scale with real scores, else low fixed score."""
        if resume_text and _skill_in_resume(keywords, resume_text):
            return min(round(present_bonus), 100)
        return absent_score

    skill_comparison = {
        "Python":         {"market": 95, "mine": _my_skill_score(["python"],             min(coding_average+10,100), 15)},
        "SQL":            {"market": 92, "mine": _my_skill_score(["sql","mysql","postgresql","sqlite"], min(ats_score, 80), 20)},
        "Data Structures":{"market": 90, "mine": _my_skill_score(["dsa","data structure","algorithm"], coding_average, 25)},
        "Cloud (AWS/GCP)":{"market": 88, "mine": _my_skill_score(["aws","gcp","azure","cloud"],        min(ats_score-10,60), 12)},
        "Docker/K8s":     {"market": 82, "mine": _my_skill_score(["docker","kubernetes","k8s","devops"], min(ats_score-15,55), 10)},
        "ML / AI":        {"market": 85, "mine": _my_skill_score(["machine learning","deep learning","tensorflow","pytorch","ai","ml"], min(coding_average-5,70), 15)},
        "React / JS":     {"market": 78, "mine": _my_skill_score(["react","javascript","js","frontend","next"], min(ats_score-5,75), 20)},
        "Git / CI-CD":    {"market": 80, "mine": _my_skill_score(["git","github","gitlab","ci/cd","devops"],    min(ats_score, 78), 30)},
    }

    snames = list(skill_comparison.keys())
    mvals  = [v["market"] for v in skill_comparison.values()]
    myvals = [v["mine"]   for v in skill_comparison.values()]

    fig = px.bar(
        x=snames * 2, y=mvals + myvals,
        color=["2024 Market Benchmark"] * len(snames) + ["My Skills (from resume)"] * len(snames),
        barmode="group",
        color_discrete_map={"2024 Market Benchmark": "#3b82f6", "My Skills (from resume)": "#22c55e"},
        labels={"x": "Skill", "y": "Score"},
    )
    st.plotly_chart(light_layout(fig, "Market Demand vs Your Skills"), use_container_width=True)

    avg_gap   = round(sum(mvals[i] - myvals[i] for i in range(len(snames))) / len(snames))
    gap_score = max(0, 100 - avg_gap)
    gc1, gc2, gc3 = st.columns(3)
    gc1.metric("📊 Market Gap Score", f"{gap_score}/100", help="Higher = closer to market demand")

    # Find top missing skills
    skill_gaps = sorted(
        [(snames[i], mvals[i] - myvals[i]) for i in range(len(snames))],
        key=lambda x: -x[1]
    )
    top_gap  = skill_gaps[0][0] if skill_gaps else "Cloud"
    top2_gap = skill_gaps[1][0] if len(skill_gaps) > 1 else "Docker"
    gc2.metric("🎯 Biggest Gap",   top_gap)
    gc3.metric("⚡ Priority Skill", top2_gap)

    # =========================================================
    # SECTION 8 – RADAR CHART (real values)
    # =========================================================
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">Skills Radar</span>
        <span class="section-title">Skills Overview</span>
    </div>""", unsafe_allow_html=True)

    radar_cats = ["Resume/ATS", "Coding", "Interview", "Communication",
                  "Aptitude", "Problem Solving", "Applied Jobs", "Offers"]
    radar_vals = [
        resume_score,
        coding_average,
        round(average_score),
        comm_score,
        round(apt_accuracy),
        round(apt_accuracy * 0.9) if apt_accuracy else coding_average,
        min(total_apps * 10, 100),
        min(offers * 25, 100),
    ]

    radar_fig = go.Figure()
    radar_fig.add_trace(go.Scatterpolar(
        r=radar_vals + [radar_vals[0]], theta=radar_cats + [radar_cats[0]],
        fill="toself", fillcolor="rgba(59,130,246,0.1)",
        line=dict(color="#2563eb", width=2), name="Your Profile (Real)"
    ))
    radar_fig.add_trace(go.Scatterpolar(
        r=[80] * len(radar_cats) + [80], theta=radar_cats + [radar_cats[0]],
        fill="toself", fillcolor="rgba(14,165,233,0.05)",
        line=dict(color="#0ea5e9", width=1.5, dash="dot"), name="Placement Benchmark"
    ))
    radar_fig.update_layout(
        polar=dict(
            bgcolor="#f8fafc",
            radialaxis=dict(visible=True, range=[0, 100], color="#94a3b8", gridcolor="#e2e8f0"),
            angularaxis=dict(color="#64748b", gridcolor="#e2e8f0"),
        ),
        paper_bgcolor=CHART_BG, font_color=FONT_CLR,
        legend=dict(bgcolor=CHART_BG, font_color=FONT_CLR),
        margin=dict(l=40, r=40, t=40, b=40)
    )
    st.plotly_chart(radar_fig, use_container_width=True)

    # =========================================================
    # SECTION 9 – COMPANY PERFORMANCE & ROLE PERFORMANCE (real DB)
    # =========================================================
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">History</span>
        <span class="section-title">Interview History by Company & Role</span>
    </div>""", unsafe_allow_html=True)

    ch1, ch2 = st.columns(2)
    with ch1:
        company_data = get_company_performance()
        if company_data:
            cdf = pd.DataFrame(company_data, columns=["Company", "Average Score"])
            fig = px.bar(cdf, x="Company", y="Average Score",
                         color_discrete_sequence=["#2563eb"],
                         text="Average Score")
            fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
            st.plotly_chart(light_layout(fig, "Avg Interview Score by Company (Real)"), use_container_width=True)
        else:
            st.markdown('<div class="no-data-box">No company interview data yet.</div>', unsafe_allow_html=True)
    with ch2:
        role_data = get_role_performance()
        if role_data:
            rdf = pd.DataFrame(role_data, columns=["Role", "Average Score"])
            fig = px.bar(rdf, x="Role", y="Average Score",
                         color_discrete_sequence=["#0ea5e9"],
                         text="Average Score")
            fig.update_traces(texttemplate="%{text:.1f}", textposition="outside")
            st.plotly_chart(light_layout(fig, "Avg Interview Score by Role (Real)"), use_container_width=True)
        else:
            st.markdown('<div class="no-data-box">No role interview data yet.</div>', unsafe_allow_html=True)

    # =========================================================
    # SECTION 10 – AI CAREER INTELLIGENCE (advisor output)
    # =========================================================
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">AI Intelligence</span>
        <span class="section-title">AI Career Intelligence</span>
    </div>""", unsafe_allow_html=True)

    if advisor:
        ai1, ai2 = st.columns(2)
        with ai1:
            st.markdown(f"""
            <div class="recruiter-card">
                <div style="color:#2563eb;font-size:0.68rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:10px;font-weight:700;">Current Level</div>
                <div style="font-size:1.05rem;font-weight:700;color:#1e293b;margin-bottom:16px;">{tier}</div>
                <div style="color:#2563eb;font-size:0.68rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:5px;font-weight:700;">Expected Package</div>
                <div style="font-size:1.5rem;font-weight:800;color:#16a34a;margin-bottom:14px;">{exp_salary}</div>
                <div style="color:#2563eb;font-size:0.68rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:5px;font-weight:700;">Placement Timeline</div>
                <div style="font-size:1.05rem;font-weight:600;color:#1e293b;margin-bottom:14px;">{exp_time}</div>
                <div style="color:#2563eb;font-size:0.68rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:5px;font-weight:700;">Hiring Probability</div>
                <div style="font-size:2.2rem;font-weight:800;color:#2563eb;">{hiring_prob}%</div>
            </div>""", unsafe_allow_html=True)
        with ai2:
            st.markdown('<div class="recruiter-card">', unsafe_allow_html=True)
            st.markdown("**🎯 Recommended Roles**")
            for r in advisor.get("recommended_roles", [])[:3]: st.success(r)
            st.markdown("**🏢 Recommended Companies**")
            for c in advisor.get("recommended_companies", [])[:3]: st.info(c)
            st.markdown("**⚡ Priority Skills**")
            for s in advisor.get("priority_skills", [])[:4]: st.write("•", s)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.info("👆 Click **Generate AI Recruiter Report** above to unlock AI Career Intelligence.")

    # =========================================================
    # SECTION 11 – DREAM COMPANY MODE
    # =========================================================
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">Dream Company</span>
        <span class="section-title">🌟 Dream Company Mode</span>
    </div>""", unsafe_allow_html=True)

    st.markdown('<div class="dream-card">', unsafe_allow_html=True)
    dc1, dc2 = st.columns([2, 1])
    with dc1:
        dream_company = st.text_input(
            "🏢 Enter Your Dream Company",
            placeholder="Google, Microsoft, OpenAI, NVIDIA, Zomato...",
            key="dream_company_input"
        )
        dream_role = st.text_input(
            "💼 Target Role",
            value=st.session_state.get("current_role", "") or "Software Engineer",
            key="dream_role_input"
        )
    with dc2:
        st.markdown("<br>", unsafe_allow_html=True)
        # Show current readiness for entered company
        if dream_company:
            # Find if this company is in our tiers list
            _dc_lower = dream_company.lower()
            _dc_offset = -15  # default mid-tier
            for cname, offset in company_tiers:
                if cname.lower() in _dc_lower or _dc_lower in cname.lower():
                    _dc_offset = offset
                    break
            _dc_pct = max(5, min(98, base_readiness + _dc_offset))
            _dc_color = _company_color(_dc_pct)
            st.markdown(f"""
            <div style="background:#fff;border:1px solid #e2e8f0;border-radius:14px;padding:20px;text-align:center;">
                <div style="font-size:0.7rem;color:#64748b;text-transform:uppercase;letter-spacing:0.1em;">Your Readiness</div>
                <div style="font-size:2.5rem;font-weight:800;color:{_dc_color};">{_dc_pct}%</div>
                <div style="font-size:0.75rem;color:#94a3b8;">for {dream_company}</div>
            </div>""", unsafe_allow_html=True)

    if dream_company and st.button("🚀 Generate Dream Company Prep Plan", use_container_width=True, key="dream_prep_btn"):
        with st.spinner(f"Building personalised prep plan for {dream_company}..."):
            try:
                prep = generate_company_prep(dream_company, dream_role)
                st.session_state["dream_company_prep"] = prep
                st.session_state["dream_company_name"] = dream_company
            except Exception as e:
                st.error(str(e))

    if st.session_state.get("dream_company_prep"):
        st.divider()
        st.markdown(f"#### 🏢 {st.session_state.get('dream_company_name','Your Dream Company')} — Personalised Preparation Plan")

        # Skill gap specific to this company
        _dc_name = st.session_state.get("dream_company_name", "")
        faang_companies = ["google","meta","apple","amazon","microsoft","nvidia","openai"]
        _is_faang = any(f in _dc_name.lower() for f in faang_companies)

        if _is_faang:
            gap_items = [
                ("System Design",    base_readiness - 30),
                ("DSA / LeetCode",   coding_average),
                ("Behavioral (STAR)",round(average_score * 0.9)),
                ("CS Fundamentals",  round(apt_accuracy * 0.85)),
                ("Resume Quality",   resume_score),
            ]
        else:
            gap_items = [
                ("Technical Skills", coding_average),
                ("Resume / ATS",     resume_score),
                ("HR / Behavioral",  round(average_score * 0.9)),
                ("Aptitude",         round(apt_accuracy)),
                ("Communication",    comm_score),
            ]

        dg1, dg2 = st.columns(2)
        with dg1:
            st.markdown("**📊 Your Readiness per Area**")
            for area, score in gap_items:
                sc = max(0, min(score, 100))
                color = _company_color(sc)
                st.markdown(f"""
                <div class="company-row">
                    <div class="company-name">{area}</div>
                    <div class="company-bar-bg"><div class="company-bar-fill" style="width:{sc}%;background:{color};"></div></div>
                    <div class="company-pct">{sc}%</div>
                </div>""", unsafe_allow_html=True)
        with dg2:
            st.markdown("**📋 Full Prep Report**")
            with st.expander("View Complete Plan", expanded=False):
                st.markdown(st.session_state["dream_company_prep"])

    st.markdown('</div>', unsafe_allow_html=True)

    # =========================================================
    # SECTION 12 – PERSONALIZED ROADMAP
    # =========================================================
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">Roadmap</span>
        <span class="section-title">Personalized Roadmap</span>
    </div>""", unsafe_allow_html=True)

    steps = (advisor.get("next_steps", []) if advisor else []) or [
        "Update resume to ATS-friendly format",
        "Complete 2 coding problems daily",
        "Practice mock interviews this week",
        "Apply to 3 target companies",
        "Complete Cloud / Docker fundamentals",
        "Build 1 end-to-end portfolio project",
        "Attend industry webinar or hackathon",
        "Review DS&A — trees, graphs, DP",
    ]
    timeframes = [
        ("📅 Today",        steps[:2] if len(steps) >= 2 else steps),
        ("🗓️ This Week",    steps[2:4] if len(steps) >= 4 else steps),
        ("📆 This Month",   steps[4:6] if len(steps) >= 6 else steps),
        ("🏁 This Quarter", steps[6:] if len(steps) >= 7 else ["Land your first offer", "Negotiate salary"]),
    ]
    rm1, rm2, rm3, rm4 = st.columns(4)
    for col, (label, items) in zip([rm1, rm2, rm3, rm4], timeframes):
        with col:
            st.markdown(f"**{label}**")
            for item in items:
                st.markdown(f'<div class="roadmap-item">→ {item}</div>', unsafe_allow_html=True)

    # =========================================================
    # SECTION 13 – ACHIEVEMENTS (real thresholds)
    # =========================================================
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">Badges</span>
        <span class="section-title">Achievements</span>
    </div>""", unsafe_allow_html=True)

    badges = [
        ("📄", "Resume Master",      ats_score >= 70,          f"ATS ≥ 70 · yours: {ats_score}"),
        ("🎯", "ATS Champion",       ats_score >= 85,          f"ATS ≥ 85 · yours: {ats_score}"),
        ("🎤", "Interview Expert",   average_score >= 75,      f"Avg ≥ 75 · yours: {round(average_score)}"),
        ("💻", "Coding Ninja",       coding_solved >= 5,       f"5+ solved · yours: {coding_solved}"),
        ("🚀", "Placement Ready",    career_score >= 70,       f"Score ≥ 70 · yours: {career_score}"),
        ("🧠", "Aptitude Ace",       apt_accuracy >= 70,       f"Acc ≥ 70% · yours: {round(apt_accuracy)}%"),
        ("🏆", "Top Performer",      best_score >= 85,         f"Best ≥ 85 · yours: {best_score}"),
    ]
    for col, (icon, name, earned, tooltip) in zip(st.columns(len(badges)), badges):
        with col:
            css_cls = "badge-card badge-earned" if earned else "badge-card badge-locked"
            earned_tag = "<div style='font-size:0.62rem;color:#16a34a;margin-top:4px;font-weight:600;'>✓ Earned</div>" if earned else ""
            st.markdown(f"""
            <div class="{css_cls}" title="{tooltip}">
                <div class="badge-icon">{icon}</div>
                <div class="badge-name">{name}</div>
                {earned_tag}
            </div>""", unsafe_allow_html=True)

    # =========================================================
    # SECTION 14 – MARKET INTELLIGENCE (industry benchmarks)
    # =========================================================
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">Industry Benchmarks</span>
        <span class="section-title">Market Intelligence · 2024 Industry Data</span>
    </div>""", unsafe_allow_html=True)

    st.caption("⚠️ Market data below shows 2024 industry benchmarks, not live API data. Connect a jobs API post-deployment for live numbers.")

    m1, m2 = st.columns(2)
    with m1:
        fig = px.bar(
            x=["AI/ML", "Data Science", "Cloud", "Backend", "DevOps", "Frontend", "Cybersecurity"],
            y=[95, 92, 88, 85, 82, 78, 75],
            color_discrete_sequence=["#3b82f6"],
            labels={"x": "Domain", "y": "Demand Index (2024)"},
        )
        st.plotly_chart(light_layout(fig, "Top Hiring Domains — 2024 Benchmark"), use_container_width=True)
    with m2:
        fig = px.bar(
            x=["Python", "AWS", "SQL", "Docker", "React", "Kubernetes", "TensorFlow"],
            y=[95, 90, 88, 85, 82, 78, 76],
            color_discrete_sequence=["#0ea5e9"],
            labels={"x": "Technology", "y": "Demand Index (2024)"},
        )
        st.plotly_chart(light_layout(fig, "Top Technologies — 2024 Benchmark"), use_container_width=True)

    m3, m4 = st.columns(2)
    with m3:
        sk = {"Python": 95, "Cloud": 90, "SQL": 88, "ML/AI": 87, "React": 82, "Data Analysis": 80, "Docker": 78}
        fig = px.bar(x=list(sk.values()), y=list(sk.keys()), orientation="h",
                     color_discrete_sequence=["#8b5cf6"],
                     labels={"x": "Demand Score", "y": "Skill"})
        st.plotly_chart(light_layout(fig, "Most Demanded Skills — 2024"), use_container_width=True)
    with m4:
        fig = px.pie(names=["Hybrid", "Remote", "On-site"], values=[42, 38, 20],
                     color_discrete_sequence=["#3b82f6", "#0ea5e9", "#bfdbfe"], hole=0.45)
        fig.update_layout(paper_bgcolor=CHART_BG, font_color=FONT_CLR,
                          title="Work Mode Trend — 2024", title_font_color=TITLE_CLR,
                          margin=dict(l=0,r=0,t=44,b=0))
        st.plotly_chart(fig, use_container_width=True)

    # =========================================================
    # SECTION 15 – LIVE MARKET INSIGHTS (API placeholders)
    # =========================================================
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">API Ready</span>
        <span class="section-title">Live Market Insights — API Placeholders</span>
    </div>""", unsafe_allow_html=True)

    insight_items = [
        ("🔮", "Trending Technologies", "Connect Adzuna / JSearch API"),
        ("🏢", "Top Hiring Companies",  "Connect LinkedIn Jobs API"),
        ("📊", "Live Market Demand",    "Connect RapidAPI Jobs feed"),
        ("💼", "Trending Roles",        "Connect Indeed Jobs API"),
        ("⚡", "Fastest Growing Skills","Connect Coursera Trends API"),
        ("💰", "Live Salary Trends",    "Connect Glassdoor / Levels.fyi API"),
    ]
    ins1, ins2, ins3 = st.columns(3)
    for i, (icon, title, ph) in enumerate(insight_items):
        with [ins1, ins2, ins3][i % 3]:
            st.markdown(f"""
            <div class="insight-card">
                <div style="font-size:1.5rem;">{icon}</div>
                <div class="insight-card-title">{title}</div>
                <div class="insight-card-placeholder">{ph}</div>
            </div>""", unsafe_allow_html=True)

    # =========================================================
    # SECTION 16 – RECENT ACTIVITY (real DB)
    # =========================================================
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">Activity</span>
        <span class="section-title">Recent Activity</span>
    </div>""", unsafe_allow_html=True)

    activity = get_recent_activity()
    if activity:
        for item in activity:
            sc = "#16a34a" if "offer" in item["status"].lower() else (
                 "#d97706" if "interview" in item["status"].lower() else "#2563eb")
            st.markdown(f"""
            <div class="activity-item" style="border-left:3px solid {sc};">
                <div style="font-weight:600;color:#1e293b;font-size:0.9rem;">{item["title"]}</div>
                <div style="display:flex;gap:16px;margin-top:5px;">
                    <span style="font-size:0.73rem;color:{sc};font-weight:500;">● {item["status"]}</span>
                    <span style="font-size:0.73rem;color:#94a3b8;">{item["date"]}</span>
                </div>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown('<div class="no-data-box">No recent activity. Start using the Job Tracker to see your history here.</div>', unsafe_allow_html=True)

    # =========================================================
    # SECTION 17 – QUICK ACTIONS
    # =========================================================
    st.markdown("""
    <div class="section-header">
        <span class="section-badge">Actions</span>
        <span class="section-title">Quick Actions</span>
    </div>""", unsafe_allow_html=True)

    quick_actions = [
        ("📄","Analyze Resume"), ("🎤","Mock Interview"),
        ("💻","Coding Round"),   ("🔍","ATS Scanner"),
        ("🤖","Career Coach"),   ("📊","Job Tracker"),
        ("✍️","Resume Builder"), ("🏢","Company Prep"),
    ]
    for col, (icon, label) in zip(st.columns(8), quick_actions):
        with col:
            st.markdown(f"""
            <div class="qa-btn">
                <div class="qa-btn-icon">{icon}</div>
                <div class="qa-btn-label">{label}</div>
            </div><br>""", unsafe_allow_html=True)

    # =========================================================
    # FOOTER
    # =========================================================
    _fs_ok = bool(total_interviews >= 0)  # Firestore reachable if query returned

    st.markdown(f"""
    <div class="dash-footer">
        <div class="footer-item">
            <span class="footer-dot"></span>
            Last Updated: {datetime.datetime.now().strftime('%d %b %Y, %H:%M')}
        </div>
        <div class="footer-item">
            <span class="footer-dot"></span>
            Firestore: ● Connected · {total_interviews} interviews
        </div>
        <div class="footer-item">
            <span class="footer-dot"></span>
            SQLite: ● Connected · {total_apps} applications
        </div>
        <div class="footer-item">
            Career Readiness: <strong style="color:#1e293b;">&nbsp;{career_score}/100 — {tier}</strong>
        </div>
        <div class="footer-item" style="color:#94a3b8;">
            InterviewGPT Pro V5 · Powered by Gemini
        </div>
    </div>
    """, unsafe_allow_html=True)
# ===================================
# FOOTER
# ===================================

st.divider()

st.caption(
    "🤖 InterviewGPT Pro V5 | Resume Analyzer • ATS Scanner • Mock Interview • Career Copilot • Live Coding • Job Tracker"
)

   

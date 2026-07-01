import re
import streamlit as st

from utils.gemini_analyzer import (
    analyze_resume
)

from utils.skill_accelerator import (
    generate_skill_accelerator,
    generate_career_report
)

from utils.database import (
    get_average_score
)


# ===================================
# ATS SCANNER PAGE
# ===================================

def render_ats_scanner():

    st.title("📈 AI ATS Resume Scanner")

    st.caption(
        "Analyze your resume, discover skill gaps, and get a personalized learning roadmap."
    )

    # ----------------------------------
    # Resume Validation
    # ----------------------------------

    if "resume_text" not in st.session_state:

        st.warning(
            "Please upload and analyze your resume from the Resume Analyzer page first."
        )

        return

    resume_text = st.session_state["resume_text"]

    # ----------------------------------
    # Target Information
    # ----------------------------------

    st.subheader("🎯 Target Job")

    col1, col2 = st.columns(2)

    with col1:

        company = st.text_input(
            "Target Company",
            placeholder="Google, Amazon, Microsoft..."
        )

    with col2:

        role = st.text_input(
            "Target Role",
            placeholder="Backend Developer, Data Engineer..."
        )

    experience = st.selectbox(

        "Experience Level",

        [

            "Intern",

            "Fresher",

            "0-1 Years",

            "1-3 Years",

            "3-5 Years",

            "5+ Years"

        ]

    )

    job_description = st.text_area(

        "Job Description (Optional)",

        height=220,

        placeholder="Paste the complete job description for a much more accurate ATS analysis."

    )

    st.divider()

    # ----------------------------------
    # Analyze Button
    # ----------------------------------

    analyze = st.button(

        "🚀 Analyze Resume",

        use_container_width=True,

        type="primary"

    )

    if analyze:

        with st.spinner(

            "Running AI ATS Analysis..."

        ):

            try:

                # -----------------------------
                # Generate ATS Report
                # -----------------------------

                ats_report = analyze_resume(

                    resume_text,

                    company,

                    role,

                    experience,

                    job_description

                )

                st.session_state["ats_report"] = ats_report

                # -----------------------------
                # Extract ATS Score
                # -----------------------------

                ats_score = 0

                match = re.search(

                    r"(\d{1,3})",

                    ats_report

                )

                if match:

                    ats_score = int(

                        match.group(1)

                    )

                # -----------------------------
                # Resume Score
                # -----------------------------

                resume_score = ats_score

                # -----------------------------
                # Previous Scores
                # -----------------------------

                interview_score = get_average_score()

                coding_score = st.session_state.get(

                    "coding_average",

                    0

                )

                # -----------------------------
                # Skill Accelerator
                # -----------------------------

                accelerator = generate_skill_accelerator(

                    company=company,

                    role=role,

                    resume_text=resume_text,

                    ats_score=ats_score,

                    resume_score=resume_score,

                    interview_score=interview_score,

                    coding_score=coding_score,

                    job_description=job_description

                )

                # -----------------------------
                # Cache Results
                # -----------------------------

                st.session_state["accelerator"] = accelerator

                st.session_state["career_report"] = generate_career_report(

                    accelerator

                )

                st.success(

                    "✅ Analysis Completed Successfully"

                )

            except Exception as e:

                st.error(

                    str(e)

                )

                return

    # ----------------------------------
    # Wait Until Analysis Exists
    # ----------------------------------

    if "accelerator" not in st.session_state:

        st.info(

            "Run an ATS analysis to view your personalized dashboard."

        )

        return

    accelerator = st.session_state["accelerator"]

    career_report = st.session_state["career_report"]
    # ===================================
    # DASHBOARD METRICS
    # ===================================

    st.divider()

    st.subheader("📊 Career Intelligence Dashboard")

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "🚀 Career Score",

            f"{accelerator['career_score']}%"

        )

    with c2:

        st.metric(

            "📄 ATS Score",

            f"{accelerator['ats_score']}%"

        )

    with c3:

        st.metric(

            "💻 Technical Score",

            f"{accelerator['technical_score']}%"

        )

    c4, c5, c6 = st.columns(3)

    with c4:

        st.metric(

            "🎯 Placement Score",

            f"{accelerator['placement_score']}%"

        )

    with c5:

        st.metric(

            "📚 Learning Progress",

            f"{accelerator['learning_progress']}%"

        )

    with c6:

        st.metric(

            "⭐ Readiness",

            accelerator["readiness"]

        )

    st.divider()

    # ===================================
    # TABS
    # ===================================

    tab1, tab2, tab3, tab4 = st.tabs(

        [

            "📄 ATS Report",

            "🎯 Skill Gap",

            "📚 Learning",

            "🚀 Roadmap"

        ]

    )

    # ===================================
    # TAB 1
    # ===================================

    with tab1:

        st.subheader("📄 ATS Analysis")

        st.markdown(

            st.session_state.get(

                "ats_report",

                "No ATS report available."

            )

        )

    # ===================================
    # TAB 2
    # ===================================

    with tab2:

        st.subheader("✅ Matched Skills")

        matched = accelerator.get(

            "matched_skills",

            []

        )

        if matched:

            cols = st.columns(3)

            i = 0

            for skill in matched:

                if isinstance(skill, dict):

                    name = skill.get(

                        "name",

                        ""

                    )

                else:

                    name = str(skill)

                cols[i % 3].success(

                    f"✅ {name}"

                )

                i += 1

        else:

            st.info(

                "No matched skills detected."

            )

        st.divider()

        st.subheader("❌ Missing Skills")

        missing = accelerator.get(

            "missing_skills",

            []

        )

        if missing:

            for skill in missing:

                if isinstance(skill, dict):

                    title = skill.get(

                        "name",

                        ""

                    )

                    importance = skill.get(

                        "importance",

                        "Medium"

                    )

                    reason = skill.get(

                        "reason",

                        ""

                    )

                else:

                    title = str(skill)

                    importance = "Medium"

                    reason = ""

                with st.expander(

                    f"{title} • {importance}"

                ):

                    st.write(reason)

        else:

            st.success(

                "No critical skill gaps found."

            )

        st.divider()

        st.subheader("🛠 Recommended Tools")

        tools = accelerator.get(

            "tools",

            []

        )

        if tools:

            cols = st.columns(4)

            i = 0

            for tool in tools:

                cols[i % 4].info(tool)

                i += 1

        else:

            st.info(

                "No tool recommendations."

            )

        st.divider()

        st.subheader("🏆 Certifications")

        certs = accelerator.get(

            "certifications",

            []

        )

        if certs:

            for cert in certs:

                if isinstance(cert, dict):

                    st.success(

                        cert.get(

                            "name",

                            ""

                        )

                    )

                    st.caption(

                        cert.get(

                            "reason",

                            ""

                        )

                    )

                else:

                    st.success(cert)

        else:

            st.info(

                "No certifications recommended."

            )
    # ===================================
    # TAB 3 - LEARNING HUB
    # ===================================

    with tab3:

        st.subheader("📚 Personalized Learning Hub")

        learning_cards = accelerator.get(
            "learning_cards",
            []
        )

        if not learning_cards:

            st.info(
                "No personalized learning resources available."
            )

        else:

            for card in learning_cards:

                with st.container(border=True):

                    st.markdown(
                        f"## 🎯 {card.get('skill','Unknown Skill')}"
                    )

                    resources = card.get(
                        "resources",
                        {}
                    )

                    categories = [

                        (
                            "📖 Official Documentation",
                            "documentation"
                        ),

                        (
                            "🎓 Courses",
                            "courses"
                        ),

                        (
                            "🏆 Certifications",
                            "certifications"
                        ),

                        (
                            "💻 Practice Platforms",
                            "practice"
                        ),

                        (
                            "🖥 GitHub Projects",
                            "github"
                        ),

                        (
                            "▶ YouTube Tutorials",
                            "youtube"
                        ),

                        (
                            "🌐 Other Resources",
                            "others"
                        )

                    ]

                    for title, key in categories:

                        items = resources.get(
                            key,
                            []
                        )

                        if not items:
                            continue

                        st.markdown(f"### {title}")

                        for item in items[:3]:

                            col1, col2 = st.columns(
                                [5, 1]
                            )

                            with col1:

                                st.markdown(
                                    f"**{item.get('title','Untitled')}**"
                                )

                                snippet = item.get(
                                    "snippet",
                                    ""
                                )

                                if snippet:

                                    st.caption(
                                        snippet
                                    )

                            with col2:

                                st.link_button(

                                    "Open",

                                    item.get(
                                        "url",
                                        "#"
                                    ),

                                    use_container_width=True

                                )

                    st.markdown("---")
    # ===================================
    # TAB 4 - AI ROADMAP
    # ===================================

    with tab4:

        st.subheader("🚀 AI Career Roadmap")

        st.markdown(
            f"""
### 🎯 Current Readiness

**{accelerator.get("readiness","Unknown")}**

Current Career Score:

**{accelerator.get("career_score",0)}%**
"""
        )

        st.divider()

        # ----------------------------------
        # NEXT STEPS
        # ----------------------------------

        st.subheader("📝 Recommended Next Steps")

        next_steps = accelerator.get(

            "next_steps",

            []

        )

        if next_steps:

            for index, step in enumerate(

                next_steps,

                start=1

            ):

                st.checkbox(

                    f"Step {index}: {step}",

                    value=False,

                    key=f"roadmap_{index}"

                )

        else:

            st.info(

                "No roadmap available."

            )

        st.divider()

        # ----------------------------------
        # SUMMARY
        # ----------------------------------

        st.subheader("📄 Career Summary")

        summary = accelerator.get(

            "summary",

            ""

        )

        if summary:

            st.info(summary)

        else:

            st.info(

                "No summary generated."

            )

        st.divider()

        # ----------------------------------
        # EXPECTED IMPROVEMENT
        # ----------------------------------

        st.subheader("📈 Expected Improvement")

        current_score = accelerator.get(

            "career_score",

            0

        )

        expected_score = min(

            current_score + 10,

            100

        )

        improvement = expected_score - current_score

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(

                "Current Score",

                f"{current_score}%"

            )

        with c2:

            st.metric(

                "Potential Score",

                f"{expected_score}%",

                delta=f"+{improvement}%"

            )

        with c3:

            st.metric(

                "Missing Skills",

                len(

                    accelerator.get(

                        "missing_skills",

                        []

                    )

                )

            )

        st.divider()

        # ----------------------------------
        # EXPORT REPORT
        # ----------------------------------

        st.subheader("📥 Export Report")

        report = f"""

==============================

InterviewGPT ATS Report

==============================

Career Score:

{accelerator.get('career_score',0)}%

ATS Score:

{accelerator.get('ats_score',0)}%

Technical Score:

{accelerator.get('technical_score',0)}%

Placement Score:

{accelerator.get('placement_score',0)}%

Learning Progress:

{accelerator.get('learning_progress',0)}%

Readiness:

{accelerator.get('readiness','Unknown')}

Matched Skills:

{len(accelerator.get('matched_skills',[]))}

Missing Skills:

{len(accelerator.get('missing_skills',[]))}

Next Steps:

"""

        for step in accelerator.get(

            "next_steps",

            []

        ):

            report += f"\n• {step}"

        report += "\n\nSummary:\n"

        report += accelerator.get(

            "summary",

            ""

        )

        st.download_button(

            "📄 Download Report",

            report,

            file_name="InterviewGPT_ATS_Report.txt",

            mime="text/plain",

            use_container_width=True

        )                                    
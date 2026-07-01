import streamlit as st

from utils.jd_match_engine import run_jd_match
from utils.pdf_generator import create_jd_match_pdf
import os


# ==========================================
# JD MATCH UI
# ==========================================

def render_jd_match():

    st.title("🎯 AI JD Match Analyzer")

    st.markdown(
        """
Compare your resume against a specific Job Description and
receive recruiter-style feedback, match score, keyword analysis,
resume improvements and interview probability.
"""
    )

    st.divider()

    # ======================================
    # LOADED DOCUMENTS
    # ======================================

    st.subheader("📂 Loaded Documents")

    resume_text = st.session_state.get(

        "resume_text",

        ""

    )

    job_description = st.session_state.get(

        "job_description",

        ""

    )

    col1, col2 = st.columns(2)

    with col1:

        if resume_text:

            st.success(
                "✅ Resume Loaded"
            )

        else:

            st.error(
                "❌ Resume not uploaded"
            )

    with col2:

        if job_description:

            st.success(
                "✅ Job Description Loaded"
            )

        else:

            st.error(
                "❌ Job Description not uploaded"
            )

    st.divider()

    company = st.text_input(

        "🏢 Target Company (Optional)",

        value=st.session_state.get(

            "current_company",

            ""

        ),

        placeholder="Google"

    )

    role = st.text_input(

        "💼 Target Role (Optional)",

        value=st.session_state.get(

            "current_role",

            ""

        ),

        placeholder="Software Engineer"

    )

    analyze = st.button(

        "🚀 Analyze JD Match",

        use_container_width=True,

        type="primary"

    )

    # ======================================
    # VALIDATION
    # ======================================

    if analyze:

        if not resume_text:

            st.warning(

                "Please upload your resume from the sidebar."

            )

            return

        if not job_description:

            st.warning(

                "Please upload or paste the Job Description from the sidebar."

            )

            return

        with st.spinner(

            "Analyzing Resume vs Job Description..."

        ):

            report = run_jd_match(

                resume_text,

                job_description

            )

            st.session_state["jd_report"] = report

            st.session_state["jd_company"] = company

            st.session_state["jd_role"] = role

            st.success(

                "Analysis Completed Successfully!"

            )
    # ======================================
    # WAIT FOR REPORT
    # ======================================

    if "jd_report" not in st.session_state:

        st.info(

            "Upload your Resume and Job Description from the sidebar to begin."

        )

        return

    report = st.session_state["jd_report"]

    # ======================================
    # MAIN TABS
    # ======================================

    overview_tab, skills_tab, optimizer_tab, recruiter_tab = st.tabs(

        [

            "📊 Overview",

            "🧠 Skills Analysis",

            "✨ Resume Optimizer",

            "📋 Recruiter Report"

        ]

    )
    # ======================================
    # OVERVIEW TAB
    # ======================================

    with overview_tab:

        st.subheader("📊 Recruiter Dashboard")

        hiring_summary = report.get(

            "hiring_summary",

            {}

        )

        dashboard = report.get(

            "dashboard",

            {}

        )

        decision = report.get(

            "decision",

            {}

        )

        # -----------------------------
        # TOP METRICS
        # -----------------------------

        c1, c2, c3, c4 = st.columns(4)

        with c1:

            st.metric(

                "🎯 Match Score",

                f"{report.get('overall_match',0)}%"

            )

        with c2:

            st.metric(

                "🎤 Interview Chance",

                f"{hiring_summary.get('interview_probability',0)}%"

            )

        with c3:

            st.metric(

                "🧠 Confidence",

                f"{dashboard.get('confidence',0)}%"

            )

        with c4:

            stage = dashboard.get(

                "hiring_stage",

                {}

            )

            st.metric(

                "🏁 Hiring Stage",

                stage.get(

                    "stage",

                    "Unknown"

                )

            )

        st.divider()

        # -----------------------------
        # RECRUITER VERDICT
        # -----------------------------

        st.subheader("👨‍💼 Recruiter Verdict")

        verdict = decision.get(

            "label",

            "Unknown"

        )

        recommendation = decision.get(

            "recommendation",

            "No Recommendation"

        )

        score = report.get(

            "overall_match",

            0

        )

        if score >= 90:

            st.success(

                f"🏆 {verdict}\n\n{recommendation}"

            )

        elif score >= 75:

            st.info(

                f"✅ {verdict}\n\n{recommendation}"

            )

        elif score >= 60:

            st.warning(

                f"⚠ {verdict}\n\n{recommendation}"

            )

        else:

            st.error(

                f"❌ {verdict}\n\n{recommendation}"

            )

        st.divider()

        # -----------------------------
        # MATCH BREAKDOWN
        # -----------------------------

        st.subheader("📈 Match Breakdown")

        breakdown = report.get(

            "score_breakdown",

            {}

        )

        for title, value in breakdown.items():

            st.write(

                f"**{title}**"

            )

            st.progress(

                value / 100

            )

            st.caption(

                f"{value}%"

            )

        st.divider()

        # -----------------------------
        # EXECUTIVE SUMMARY
        # -----------------------------

        st.subheader("📄 Executive Summary")

        st.info(

            report.get(

                "summary",

                "No summary available."

            )

        )
    # ======================================
    # SKILLS ANALYSIS TAB
    # ======================================

    with skills_tab:

        st.subheader("🧠 Skills & Keyword Analysis")

        left, right = st.columns(2)

        # -----------------------------
        # MATCHED SKILLS
        # -----------------------------

        with left:

            st.markdown("### ✅ Matched Skills")

            matched_skills = report.get(

                "matched_skills",

                []

            )

            if matched_skills:

                for skill in matched_skills:

                    st.success(skill)

            else:

                st.info("No matched skills found.")

            st.divider()

            st.markdown("### ✅ Matched Keywords")

            matched_keywords = report.get(

                "matched_keywords",

                []

            )

            if matched_keywords:

                for keyword in matched_keywords:

                    st.success(keyword)

            else:

                st.info("No matched keywords found.")

        # -----------------------------
        # MISSING SKILLS
        # -----------------------------

        with right:

            st.markdown("### ❌ Missing Skills")

            missing_skills = report.get(

                "missing_skills",

                []

            )

            if missing_skills:

                for skill in missing_skills:

                    st.error(skill)

            else:

                st.success("No missing skills 🎉")

            st.divider()

            st.markdown("### ❌ Missing Keywords")

            missing_keywords = report.get(

                "missing_keywords",

                []

            )

            if missing_keywords:

                for keyword in missing_keywords:

                    st.error(keyword)

            else:

                st.success("No missing keywords 🎉")

        st.divider()

        # -----------------------------
        # RECRUITER FEEDBACK
        # -----------------------------

        feedback1, feedback2 = st.columns(2)

        with feedback1:

            st.subheader("💪 Strengths")

            strengths = report.get(

                "strengths",

                []

            )

            if strengths:

                for item in strengths:

                    st.success(item)

            else:

                st.info("No strengths available.")

        with feedback2:

            st.subheader("⚠ Recruiter Concerns")

            weaknesses = report.get(

                "weaknesses",

                []

            )

            if weaknesses:

                for item in weaknesses:

                    st.warning(item)

            else:

                st.success("No major concerns found.")

        st.divider()

        # -----------------------------
        # QUICK INSIGHTS
        # -----------------------------

        st.subheader("📌 Quick Insights")

        st.info(

            f"""
**Matched Skills:** {len(report.get('matched_skills', []))}

**Missing Skills:** {len(report.get('missing_skills', []))}

**Matched Keywords:** {len(report.get('matched_keywords', []))}

**Missing Keywords:** {len(report.get('missing_keywords', []))}
"""
        )
    # ======================================
    # RESUME OPTIMIZER TAB
    # ======================================

    with optimizer_tab:

        st.subheader("✨ AI Resume Optimizer")

        improvements = report.get(

            "resume_improvements",

            []

        )

        rewrites = report.get(

            "resume_rewrite",

            []

        )

        dashboard = report.get(

            "dashboard",

            {}

        )

        # ---------------------------------
        # PRIORITY IMPROVEMENTS
        # ---------------------------------

        st.markdown("### 🚀 Priority Improvements")

        if improvements:

            for index, item in enumerate(

                improvements,

                start=1

            ):

                st.warning(

                    f"**{index}.** {item}"

                )

        else:

            st.success(

                "No major improvements suggested."

            )

        st.divider()

        # ---------------------------------
        # AI RESUME REWRITE
        # ---------------------------------

        st.markdown("### ✍ AI Resume Rewrite Suggestions")

        if rewrites:

            for index, rewrite in enumerate(

                rewrites,

                start=1

            ):

                with st.expander(

                    f"Suggestion {index}"

                ):

                    st.write(rewrite)

        else:

            st.info(

                "No rewrite suggestions available."

            )

        st.divider()

        # ---------------------------------
        # SECTION SCORECARD
        # ---------------------------------

        st.markdown("### 📊 Resume Section Scorecard")

        section_scores = dashboard.get(

            "section_scores",

            {}

        )

        if section_scores:

            for section, score in section_scores.items():

                st.write(

                    f"**{section}**"

                )

                st.progress(

                    score / 100

                )

                st.caption(

                    f"{score}%"

                )

        else:

            st.info(

                "Section analysis unavailable."

            )

        st.divider()

        # ---------------------------------
        # AI COACH
        # ---------------------------------

        st.markdown("### 🎯 AI Career Coach")

        overall = report.get(

            "overall_match",

            0

        )

        if overall >= 90:

            st.success(

                """
Excellent match!

Your resume aligns very well with the job description.

Focus on interview preparation rather than resume changes.
"""

            )

        elif overall >= 75:

            st.info(

                """
Good match.

A few improvements in keywords and projects
can significantly increase your interview chances.
"""

            )

        elif overall >= 60:

            st.warning(

                """
Average match.

Improve your resume before applying.
Add more relevant projects and technologies.
"""

            )

        else:

            st.error(

                """
Weak match.

Consider learning the missing skills and
updating your resume before applying.
"""

            )

        st.divider()

        # ---------------------------------
        # COPY READY SUMMARY
        # ---------------------------------

        st.markdown("### 📄 Optimized Resume Summary")

        optimized_summary = report.get(
            "optimized_resume_summary",
            report.get("summary", "")
        )

        st.text_area(

            "Copy & Use",

            optimized_summary,

            height=180

        )
    # ======================================
    # RECRUITER REPORT TAB
    # ======================================

    with recruiter_tab:

        st.subheader("📋 Recruiter Evaluation Report")

        hiring_summary = report.get(

            "hiring_summary",

            {}

        )

        dashboard = report.get(

            "dashboard",

            {}

        )

        # ---------------------------------
        # RECRUITER CHECKLIST
        # ---------------------------------

        st.markdown("### ✅ Recruiter Checklist")

        checklist = {

            "Skills Match":
                report.get(
                    "score_breakdown",
                    {}
                ).get(
                    "Skill Match",
                    0
                ) >= 70,

            "Experience Match":
                report.get(
                    "score_breakdown",
                    {}
                ).get(
                    "Experience Match",
                    0
                ) >= 70,

            "Education Match":
                report.get(
                    "score_breakdown",
                    {}
                ).get(
                    "Education Match",
                    0
                ) >= 70,

            "Project Match":
                report.get(
                    "score_breakdown",
                    {}
                ).get(
                    "Project Match",
                    0
                ) >= 70,

            "Keyword Match":
                report.get(
                    "score_breakdown",
                    {}
                ).get(
                    "Keyword Match",
                    0
                ) >= 70

        }

        for item, passed in checklist.items():

            if passed:

                st.success(f"✔ {item}")

            else:

                st.error(f"✘ {item}")

        st.divider()

        # ---------------------------------
        # HIRING SUMMARY
        # ---------------------------------

        st.markdown("### 👨‍💼 Hiring Recommendation")

        col1, col2 = st.columns(2)

        with col1:

            st.metric(

                "Interview Probability",

                f"{hiring_summary.get('interview_probability',0)}%"

            )

            st.metric(

                "Analysis Confidence",

                f"{hiring_summary.get('analysis_confidence',0)}%"

            )

        with col2:

            st.metric(

                "Expected Hiring Stage",

                hiring_summary.get(

                    "expected_stage",

                    "Unknown"

                )

            )

            st.metric(

                "Recruiter Verdict",

                hiring_summary.get(

                    "recruiter_verdict",

                    "Unknown"

                )

            )

        st.divider()

        # ---------------------------------
        # FINAL RECOMMENDATION
        # ---------------------------------

        recommendation = hiring_summary.get(

            "recommendation",

            "No recommendation available."

        )

        score = report.get(

            "overall_match",

            0

        )

        if score >= 90:

            st.success(recommendation)

        elif score >= 75:

            st.info(recommendation)

        elif score >= 60:

            st.warning(recommendation)

        else:

            st.error(recommendation)

        st.divider()

        # ---------------------------------
        # EXECUTIVE SUMMARY
        # ---------------------------------

        st.markdown("### 👤 Executive Summary")

        st.info(

            report.get(

                "summary",

                "No summary available."

            )

        )

        st.divider()

        # ---------------------------------
        # CANDIDATE STRENGTHS / CONCERNS
        # ---------------------------------

        left, right = st.columns(2)

        with left:

            st.markdown("### 💪 Key Strengths")

            strengths = report.get(

                "strengths",

                []

            )

            if strengths:

                for item in strengths:

                    st.success(item)

            else:

                st.info(

                    "No strengths available."

                )

        with right:

            st.markdown("### ⚠ Recruiter Concerns")

            concerns = report.get(

                "weaknesses",

                []

            )

            if concerns:

                for item in concerns:

                    st.warning(item)

            else:

                st.success(

                    "No major concerns."

                )

        st.divider()

        # ---------------------------------
        # RESUME IMPROVEMENTS
        # ---------------------------------

        st.markdown("### 🚀 Resume Improvements")

        improvements = report.get(

            "resume_improvements",

            []

        )

        if improvements:

            for i, item in enumerate(

                improvements,

                start=1

            ):

                st.success(f"✅ {item}")

        else:

            st.success(

                "No improvements suggested."

            )

        st.divider()

        # ---------------------------------
        # RESUME REWRITE
        # ---------------------------------

        st.markdown("### ✍ Resume Rewrite Suggestions")

        rewrites = report.get(

            "resume_rewrite",

            []

        )

        if rewrites:

         for index, rewrite in enumerate(rewrites, start=1):

          with st.container(border=True):

            st.markdown(f"#### 💡 AI Suggestion {index}")

            st.write(rewrite)

        else:

            st.success(

                "No rewrite suggestions."

            )

        st.divider()

        # ---------------------------------
        # DOWNLOAD PDF REPORT
        # ---------------------------------

        try:

            pdf_path = "JD_Match_Report.pdf"

            create_jd_match_pdf(
                report,
                pdf_path
            )

            with open(pdf_path, "rb") as pdf_file:

                pdf_bytes = pdf_file.read()

            st.download_button(

                label="📄 Download Recruiter Report (PDF)",

                data=pdf_bytes,

                file_name="JD_Match_Report.pdf",

                mime="application/pdf",

                use_container_width=True

            )

        except Exception as e:

            st.error(f"PDF generation failed: {e}")

        st.success(
            "JD Match Analysis Completed Successfully!"
        )
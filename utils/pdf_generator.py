from datetime import datetime

from reportlab.lib import colors

from reportlab.lib.enums import TA_CENTER

from reportlab.lib.styles import getSampleStyleSheet

from reportlab.lib.units import inch

from reportlab.platypus import (

    SimpleDocTemplate,

    Paragraph,

    Spacer,

    Table,

    TableStyle,

    HRFlowable

)

# ==========================================
# STYLES
# ==========================================

styles = getSampleStyleSheet()

title_style = styles["Heading1"]
title_style.alignment = TA_CENTER
title_style.textColor = colors.HexColor("#0F62FE")

subtitle_style = styles["Heading2"]
subtitle_style.alignment = TA_CENTER
subtitle_style.textColor = colors.HexColor("#444444")

heading_style = styles["Heading2"]
heading_style.textColor = colors.HexColor("#0F62FE")

body_style = styles["BodyText"]

body_style.leading = 18

body_style.spaceAfter = 8

small_style = styles["BodyText"]

small_style.fontSize = 9

small_style.textColor = colors.grey


# ==========================================
# SECTION HEADER
# ==========================================

def add_section(elements, title):

    elements.append(

        Spacer(1, 0.15 * inch)

    )

    elements.append(

        HRFlowable(

            width="100%",

            thickness=1,

            color=colors.HexColor("#DDDDDD")

        )

    )

    elements.append(

        Spacer(1, 0.08 * inch)

    )

    elements.append(

        Paragraph(

            title,

            heading_style

        )

    )

    elements.append(

        Spacer(1, 0.08 * inch)

    )
def create_jd_match_pdf(report, output_path):

    doc = SimpleDocTemplate(

        output_path,

        rightMargin=40,

        leftMargin=40,

        topMargin=40,

        bottomMargin=40

    )

    elements = []

    # ==========================================
    # HEADER
    # ==========================================

    elements.append(

        Paragraph(

            "InterviewGPT",

            title_style

        )

    )

    elements.append(

        Paragraph(

            "AI Recruiter Evaluation Report",

            subtitle_style

        )

    )

    elements.append(

        Spacer(1, 0.25 * inch)

    )

    generated = datetime.now().strftime(

        "%d %B %Y %I:%M %p"

    )

    elements.append(

        Paragraph(

            f"<b>Generated:</b> {generated}",

            small_style

        )

    )

    elements.append(

        Spacer(1, 0.20 * inch)

    )

    # ==========================================
    # SUMMARY TABLE
    # ==========================================

    hiring = report.get(

        "hiring_summary",

        {}

    )

    table_data = [

        [

            "Overall Match",

            f"{report.get('overall_match',0)}%"

        ],

        [

            "Recruiter Verdict",

            hiring.get(

                "recruiter_verdict",

                "N/A"

            )

        ],

        [

            "Recommendation",

            hiring.get(

                "recommendation",

                "N/A"

            )

        ],

        [

            "Interview Probability",

            f"{hiring.get('interview_probability',0)}%"

        ],

        [

            "Hiring Stage",

            hiring.get(

                "expected_stage",

                "N/A"

            )

        ]

    ]

    summary_table = Table(

        table_data,

        colWidths=[2.7 * inch, 3.0 * inch]

    )

    summary_table.setStyle(

        TableStyle([

            ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#EAF2FF")),

            ("GRID", (0,0), (-1,-1), 0.5, colors.grey),

            ("BACKGROUND", (0,0), (0,-1), colors.HexColor("#F7F9FC")),

            ("FONTNAME", (0,0), (-1,-1), "Helvetica"),

            ("BOTTOMPADDING", (0,0), (-1,-1), 8),

            ("TOPPADDING", (0,0), (-1,-1), 8),

            ("VALIGN", (0,0), (-1,-1), "MIDDLE"),

            ("TEXTCOLOR", (0,0), (0,-1), colors.HexColor("#0F62FE"))

        ])

    )

    elements.append(summary_table)

    # ==========================================
    # EXECUTIVE SUMMARY
    # ==========================================

    add_section(

        elements,

        "Executive Summary"

    )

    elements.append(

        Paragraph(

            report.get(

                "summary",

                "No summary available."

            ),

            body_style

        )

    )
    # ==========================================
    # KEY STRENGTHS
    # ==========================================

    add_section(

        elements,

        "Key Strengths"

    )

    strengths = report.get(

        "strengths",

        []

    )

    if strengths:

        for item in strengths:

            elements.append(

                Paragraph(

                    f"✓ {item}",

                    body_style

                )

            )

    else:

        elements.append(

            Paragraph(

                "No strengths available.",

                body_style

            )

        )

    # ==========================================
    # RECRUITER CONCERNS
    # ==========================================

    add_section(

        elements,

        "Recruiter Concerns"

    )

    concerns = report.get(

        "weaknesses",

        []

    )

    if concerns:

        for item in concerns:

            elements.append(

                Paragraph(

                    f"⚠ {item}",

                    body_style

                )

            )

    else:

        elements.append(

            Paragraph(

                "No major concerns found.",

                body_style

            )

        )

    # ==========================================
    # RESUME IMPROVEMENTS
    # ==========================================

    add_section(

        elements,

        "Resume Improvements"

    )

    improvements = report.get(

        "resume_improvements",

        []

    )

    if improvements:

        for index, item in enumerate(

            improvements,

            start=1

        ):

            elements.append(

                Paragraph(

                    f"{index}. {item}",

                    body_style

                )

            )

    else:

        elements.append(

            Paragraph(

                "No resume improvements suggested.",

                body_style

            )

        )
    # ==========================================
    # RESUME REWRITE SUGGESTIONS
    # ==========================================

    add_section(

        elements,

        "Resume Rewrite Suggestions"

    )

    rewrites = report.get(

        "resume_rewrite",

        []

    )

    if rewrites:

        for item in rewrites:

            elements.append(

                Paragraph(

                    f"• {item}",

                    body_style

                )

            )

    else:

        elements.append(

            Paragraph(

                "No rewrite suggestions available.",

                body_style

            )

        )

    # ==========================================
    # SCORE BREAKDOWN
    # ==========================================

    add_section(

        elements,

        "Recruiter Score Breakdown"

    )

    breakdown = report.get(

        "score_breakdown",

        {}

    )

    if breakdown:

        table_data = [

            [

                "Category",

                "Score"

            ]

        ]

        for key, value in breakdown.items():

            table_data.append(

                [

                    key,

                    f"{value}%"

                ]

            )

        score_table = Table(

            table_data,

            colWidths=[3.8 * inch, 1.6 * inch]

        )

        score_table.setStyle(

            TableStyle([

                ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#0F62FE")),

                ("TEXTCOLOR", (0,0), (-1,0), colors.white),

                ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),

                ("BACKGROUND", (0,1), (-1,-1), colors.whitesmoke),

                ("GRID", (0,0), (-1,-1), 0.5, colors.grey),

                ("BOTTOMPADDING", (0,0), (-1,-1), 8),

                ("TOPPADDING", (0,0), (-1,-1), 8),

                ("ALIGN", (1,1), (1,-1), "CENTER")

            ])

        )

        elements.append(score_table)

    # ==========================================
    # FOOTER
    # ==========================================

    elements.append(

        Spacer(

            1,

            0.35 * inch

        )

    )

    elements.append(

        HRFlowable(

            width="100%",

            thickness=1,

            color=colors.HexColor("#CCCCCC")

        )

    )

    elements.append(

        Spacer(

            1,

            0.12 * inch

        )

    )

    elements.append(

        Paragraph(

            "<b>InterviewGPT</b> | AI Powered Resume & Interview Platform",

            small_style

        )

    )

    elements.append(

        Paragraph(

            "This report is AI-generated and intended to assist candidates in improving resume quality and job readiness.",

            small_style

        )

    )

    # ==========================================
    # BUILD PDF
    # ==========================================

    doc.build(

        elements

    )                
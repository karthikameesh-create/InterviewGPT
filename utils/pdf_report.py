from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)


# ===================================
# INTERVIEW REPORT PDF
# ===================================

def generate_pdf_report(

    filename,
    company,
    role,
    report

):

    pdf = SimpleDocTemplate(
        filename
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "InterviewGPT Report",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            f"Company: {company}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Role: {role}",
            styles["Normal"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    content.append(
        Paragraph(
            report.replace(
                "\n",
                "<br/>"
            ),
            styles["BodyText"]
        )
    )

    pdf.build(
        content
    )

    return filename


# ===================================
# AI RESUME PDF
# ===================================

def generate_resume_pdf(

    resume_text,
    filename="ATS_Resume.pdf"

):

    pdf = SimpleDocTemplate(
        filename
    )

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "AI Generated ATS Resume",
            styles["Title"]
        )
    )

    content.append(
        Spacer(1, 20)
    )

    for line in resume_text.split("\n"):

        line = line.strip()

        if not line:
            continue

        if (
            line.isupper()
            or line.endswith(":")
        ):

            content.append(

                Paragraph(

                    f"<b>{line.replace(':','')}</b>",

                    styles["Heading2"]

                )

            )

        else:

            content.append(

                Paragraph(

                    line,

                    styles["BodyText"]

                )

            )

    pdf.build(
        content
    )

    return filename

# ===================================
# COVER LETTER PDF
# ===================================

from reportlab.lib.enums import TA_LEFT


def generate_cover_letter_pdf(

    cover_letter,

    filename="Cover_Letter.pdf"

):

    pdf = SimpleDocTemplate(

        filename,

        rightMargin=50,

        leftMargin=50,

        topMargin=50,

        bottomMargin=50

    )

    styles = getSampleStyleSheet()

    normal = styles["BodyText"]

    normal.fontName = "Helvetica"

    normal.fontSize = 11

    normal.leading = 18

    normal.alignment = TA_LEFT

    story = []

    for line in cover_letter.split("\n"):

        line = line.strip()

        if not line:

            story.append(
                Spacer(1, 12)
            )

            continue

        story.append(

            Paragraph(

                line,

                normal

            )

        )

    pdf.build(story)

    return filename
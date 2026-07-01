import os
import json
import subprocess
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

def add_p_border_bottom(paragraph, color_hex="00468C", size="12"):
    pPr = paragraph._element.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), size)
    bottom.set(qn('w:space'), '4')
    bottom.set(qn('w:color'), color_hex)
    pBdr.append(bottom)
    pPr.append(pBdr)

def add_hyperlink(paragraph, url, text, color="00468C", underline=True):
    part = paragraph.part
    r_id = part.relate_to(url, "http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink", is_external=True)
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), r_id)
    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    c = OxmlElement('w:color')
    c.set(qn('w:val'), color)
    rPr.append(c)
    if underline:
        u = OxmlElement('w:u')
        u.set(qn('w:val'), 'single')
        rPr.append(u)
    new_run.append(rPr)
    text_node = OxmlElement('w:t')
    text_node.text = text
    new_run.append(text_node)
    hyperlink.append(new_run)
    paragraph._element.append(hyperlink)
    return hyperlink

def add_page_number(run):
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = "PAGE"
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    run._element.append(fldChar1)
    run._element.append(instrText)
    run._element.append(fldChar2)
    run._element.append(fldChar3)

def build_resume_docx(
    resume_data,
    filename="ATS_Resume.docx",
    template="ATS Professional"
):
    if isinstance(resume_data, str):
        try:
            resume_data = json.loads(resume_data)
        except Exception:
            resume_data = {"summary": resume_data, "name": "Format Error Profile"}

    document = Document()

    # Layout Parameters
    font_family = "Calibri"
    show_separators = True
    use_icons = False
    line_spacing = 1.15
    space_after_bullet = Pt(2)
    margin_tb, margin_lr = 0.6, 0.7

    if template == "ATS Professional":
        primary_rgb = RGBColor(0, 70, 140)
        primary_hex = "00468C"
        heading_size, body_size, name_size = 13, 11, 22
        line_spacing = 1.10
    elif template == "Modern":
        primary_rgb = RGBColor(41, 98, 255)
        primary_hex = "2962FF"
        heading_size, body_size, name_size = 14, 11, 24
        use_icons = True
        line_spacing = 1.20
        space_after_bullet = Pt(3)
    elif template == "Executive":
        primary_rgb = RGBColor(64, 64, 64)
        primary_hex = "404040"
        heading_size, body_size, name_size = 14, 11, 22
        font_family = "Times New Roman"
        line_spacing = 1.15
    elif template == "Startup":
        primary_rgb = RGBColor(0, 140, 90)
        primary_hex = "008C5A"
        heading_size, body_size, name_size = 14, 11, 23
        line_spacing = 1.20
    elif template == "Minimal":
        primary_rgb = RGBColor(0, 0, 0)
        primary_hex = "000000"
        heading_size, body_size, name_size = 12, 10, 20
        show_separators = False
        margin_tb, margin_lr = 0.5, 0.5
        line_spacing = 1.05

    section = document.sections[0]
    section.top_margin = Inches(margin_tb)
    section.bottom_margin = Inches(margin_tb)
    section.left_margin = Inches(margin_lr)
    section.right_margin = Inches(margin_lr)

    styles = document.styles
    styles["Normal"].font.name = font_family
    styles["Normal"]._element.rPr.rFonts.set(qn("w:eastAsia"), font_family)
    styles["Normal"].font.size = Pt(body_size)

    # Header Identity
    name = resume_data.get("name", "Your Name")
    if name:
        title_p = document.add_paragraph()
        title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        title_p.paragraph_format.space_after = Pt(2)
        run = title_p.add_run(name)
        run.bold = True
        run.font.size = Pt(name_size)
        run.font.color.rgb = RGBColor(30, 30, 30)

    contact_data = resume_data.get("contact", {})
    contact_p = document.add_paragraph()
    contact_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    contact_p.paragraph_format.space_after = Pt(12)

    elements = []
    if contact_data.get("email"):
        elements.append((f"📧 {contact_data['email']}" if use_icons else contact_data['email'], None))
    if contact_data.get("phone"):
        elements.append((f"📱 {contact_data['phone']}" if use_icons else contact_data['phone'], None))
    if contact_data.get("portfolio"):
        elements.append(("🌐 Portfolio" if use_icons else "Portfolio", contact_data['portfolio']))
    if contact_data.get("linkedin"):
        elements.append(("💼 LinkedIn" if use_icons else "LinkedIn", contact_data['linkedin']))
    if contact_data.get("github"):
        elements.append(("💻 GitHub" if use_icons else "GitHub", contact_data['github']))

    for i, (text_content, link_url) in enumerate(elements):
        if link_url:
            target_url = link_url if link_url.startswith("http") else f"https://{link_url}"
            add_hyperlink(contact_p, target_url, text_content, color=primary_hex)
        else:
            r = contact_p.add_run(text_content)
            r.font.size = Pt(body_size - 1)
        if i < len(elements) - 1:
            sep_run = contact_p.add_run("  |  ")
            sep_run.font.size = Pt(body_size - 1)
            sep_run.font.color.rgb = RGBColor(140, 140, 140)

    # Layout Priority Order Computation
    has_heavy_exp = len(resume_data.get("experience", [])) > 2
    if template == "Startup":
        layout_order = ["summary", "skills", "projects", "experience", "education", "certifications", "achievements", "languages"]
    elif not has_heavy_exp:
        layout_order = ["summary", "skills", "projects", "education", "experience", "certifications", "achievements", "languages"]
    else:
        layout_order = ["summary", "experience", "skills", "projects", "education", "certifications", "achievements", "languages"]

    def render_section_header(title_text):
        document.add_paragraph()
        h_p = document.add_paragraph()
        h_p.paragraph_format.space_before = Pt(8)
        h_p.paragraph_format.space_after = Pt(4)
        h_p.paragraph_format.keep_with_next = True
        run = h_p.add_run(title_text.upper())
        run.bold = True
        run.font.size = Pt(heading_size)
        run.font.color.rgb = primary_rgb
        if show_separators:
            add_p_border_bottom(h_p, color_hex=primary_hex, size="12")

    # Document Structure Builder Elements
    for block in layout_order:
        if block == "summary" and resume_data.get("summary"):
            render_section_header("Professional Summary")
            p = document.add_paragraph(resume_data["summary"])
            p.paragraph_format.line_spacing = line_spacing
            p.paragraph_format.space_after = Pt(4)

        elif block == "skills" and resume_data.get("skills"):
            render_section_header("Technical Skills")
            skills = resume_data.get("skills", {})
            for category, items in skills.items():
                if not items:
                    continue
                p = document.add_paragraph()
                p.paragraph_format.space_after = Pt(3)
                p.paragraph_format.line_spacing = line_spacing
                title = p.add_run(f"{category}: ")
                title.bold = True
                title.font.size = Pt(body_size)
                body = p.add_run(", ".join(items))
                body.font.size = Pt(body_size)

        elif block == "experience" and resume_data.get("experience"):
            render_section_header("Experience")
            for job in resume_data["experience"]:
                p = document.add_paragraph()
                p.paragraph_format.space_before = Pt(4)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.keep_with_next = True
                
                r_role = p.add_run(f"{job.get('role', '')} ")
                r_role.bold = True
                p.add_run(f"| {job.get('company', '')} ({job.get('location', '')})")
                
                p.paragraph_format.tab_stops.add_tab_stop(Inches(6.8), alignment=WD_TAB_ALIGNMENT.RIGHT)
                r_date = p.add_run(f"\t{job.get('duration', '')}")
                r_date.font.color.rgb = RGBColor(100, 100, 100)
                
                for b in job.get("bullets", []):
                    bp = document.add_paragraph(style="List Bullet")
                    bp.paragraph_format.left_indent = Inches(0.2)
                    bp.paragraph_format.space_after = space_after_bullet
                    bp.paragraph_format.line_spacing = line_spacing
                    bp.add_run(b)

        elif block == "projects" and resume_data.get("projects"):
            render_section_header("Projects")
            for proj in resume_data["projects"]:
                p = document.add_paragraph()
                p.paragraph_format.space_before = Pt(4)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.keep_with_next = True
                
                r_title = p.add_run(proj.get("title", ""))
                r_title.bold = True
                
                if proj.get("technologies"):
                    r_tech_label = p.add_run("  •  Technologies: ")
                    r_tech_label.bold = True
                    r_tech_list = p.add_run(", ".join(proj.get("technologies")))
                    r_tech_list.font.italic = True
                    r_tech_list.font.size = Pt(body_size - 0.5)

                for b in proj.get("bullets", []):
                    bp = document.add_paragraph(style="List Bullet")
                    bp.paragraph_format.left_indent = Inches(0.2)
                    bp.paragraph_format.space_after = space_after_bullet
                    bp.paragraph_format.line_spacing = line_spacing
                    bp.add_run(b)

        elif block == "education" and resume_data.get("education"):
            render_section_header("Education")
            for edu in resume_data["education"]:
                p = document.add_paragraph()
                p.paragraph_format.space_after = Pt(2)
                r_deg = p.add_run(f"{edu.get('degree', '')} ")
                r_deg.bold = True
                p.add_run(f"- {edu.get('institution', '')}")
                
                p.paragraph_format.tab_stops.add_tab_stop(Inches(6.8), alignment=WD_TAB_ALIGNMENT.RIGHT)
                r_dur = p.add_run(f"\t{edu.get('duration', edu.get('year', ''))}")
                r_dur.font.color.rgb = RGBColor(100, 100, 100)
                
                details = edu.get("details", "") or (f"CGPA: {edu.get('cgpa')}" if edu.get("cgpa") else "")
                if details:
                    dp = document.add_paragraph(details)
                    dp.paragraph_format.left_indent = Inches(0.15)
                    dp.paragraph_format.space_after = Pt(3)
                    dp.runs[0].font.size = Pt(body_size - 0.5)
                    dp.runs[0].font.italic = True

        elif block == "certifications" and resume_data.get("certifications"):
            render_section_header("Certifications")
            for cert in resume_data["certifications"]:
                bp = document.add_paragraph(style="List Bullet")
                bp.paragraph_format.space_after = Pt(2)
                bp.add_run(cert)

        elif block == "achievements" and resume_data.get("achievements"):
            render_section_header("Achievements")
            for ach in resume_data["achievements"]:
                bp = document.add_paragraph(style="List Bullet")
                bp.paragraph_format.space_after = Pt(2)
                bp.add_run(ach)

        elif block == "languages" and resume_data.get("languages"):
            render_section_header("Languages")
            p = document.add_paragraph(", ".join(resume_data["languages"]))
            p.paragraph_format.space_after = Pt(4)

    # Footers
    footer = section.footer
    footer_para = footer.paragraphs[0]
    footer_para.alignment = WD_ALIGN_PARAGRAPH.LEFT
    footer_para.paragraph_format.tab_stops.add_tab_stop(Inches(6.8), alignment=WD_TAB_ALIGNMENT.RIGHT)
    
    f_run = footer_para.add_run("Generated by InterviewGPT AI Resume Studio")
    f_run.font.name = font_family
    f_run.font.size = Pt(8)
    f_run.font.color.rgb = RGBColor(140, 140, 140)
    
    footer_para.add_run("\tPage ")
    p_run = footer_para.add_run()
    p_run.font.size = Pt(8)
    p_run.font.bold = True
    p_run.font.color.rgb = RGBColor(100, 100, 100)
    add_page_number(p_run)

    document.save(filename)
    return filename

# FIXED: Accepts **kwargs to swallow and capture any mismatched keyword parameter calls smoothly
def generate_resume_pdf(resume_data, template="ATS Professional", pdf_filename="ATS_Resume.pdf", **kwargs):
    temp_docx = "temp_render_track.docx"
    
    # Extract template argument dynamically if provided via kwargs key mapping
    selected_template = kwargs.get("template", template)
    
    # Pass structural definitions safely
    build_resume_docx(resume_data, filename=temp_docx, template=selected_template)
    
    try:
        from docx2pdf import convert
        convert(temp_docx, pdf_filename)
    except Exception:
        try:
            subprocess.run([
                'libreoffice', '--headless', '--convert-to', 'pdf', temp_docx
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists("temp_render_track.pdf"):
                os.rename("temp_render_track.pdf", pdf_filename)
        except Exception as err:
            raise RuntimeError("PDF rendering pipeline failed completely.") from err
    finally:
        if os.path.exists(temp_docx):
            os.remove(temp_docx)
            
    return pdf_filename
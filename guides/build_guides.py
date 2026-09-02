#!/usr/bin/env python3
"""
Builds the two beginner install guides as PDFs.

Re-run this whenever Claude or ChatGPT change their menus:
edit the STEPS lists below, then run `python3 build_guides.py`.

    LINK  the one place to change the "latest version" URL.
    DATE  shown on every page, so a reader knows how old the guide is.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether)

LINK = "github.com/alistairphillips1/health-content-check"
DATE = "2 September 2026"
VERSION = "Version 1.0"

INK = colors.HexColor("#14243A")
MUTED = colors.HexColor("#5B6B7F")
ACCENT = colors.HexColor("#1F6F5C")
RULE = colors.HexColor("#D8DEE6")
BOXBG = colors.HexColor("#F2F5F8")
WARNBG = colors.HexColor("#FDF6E7")

S = {
    "title": ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=25, leading=29,
                            textColor=INK, spaceAfter=5),
    "sub": ParagraphStyle("sub", fontName="Helvetica", fontSize=12.5, leading=17,
                          textColor=MUTED, spaceAfter=3),
    "h2": ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=14.5, leading=18,
                         textColor=ACCENT, spaceBefore=15, spaceAfter=7),
    "body": ParagraphStyle("body", fontName="Helvetica", fontSize=11, leading=16,
                           textColor=INK, alignment=TA_LEFT, spaceAfter=6),
    "step": ParagraphStyle("step", fontName="Helvetica", fontSize=11.5, leading=16.5,
                           textColor=INK),
    "note": ParagraphStyle("note", fontName="Helvetica-Oblique", fontSize=10, leading=14.5,
                           textColor=MUTED),
    "num": ParagraphStyle("num", fontName="Helvetica-Bold", fontSize=13, leading=17,
                          textColor=ACCENT),
    "boxh": ParagraphStyle("boxh", fontName="Helvetica-Bold", fontSize=11, leading=15,
                           textColor=INK, spaceAfter=3),
    "boxb": ParagraphStyle("boxb", fontName="Helvetica", fontSize=10.5, leading=15,
                           textColor=INK),
    "cell": ParagraphStyle("cell", fontName="Helvetica", fontSize=10, leading=14,
                           textColor=INK),
    "cellb": ParagraphStyle("cellb", fontName="Helvetica-Bold", fontSize=10, leading=14,
                            textColor=INK),
}


def step(n, text, note=None):
    """One numbered step. Number in the margin, text beside it."""
    inner = [Paragraph(text, S["step"])]
    if note:
        inner.append(Spacer(1, 2.5))
        inner.append(Paragraph(note, S["note"]))
    t = Table([[Paragraph(str(n), S["num"]), inner]], colWidths=[11 * mm, 149 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 3),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def box(heading, lines, bg=BOXBG):
    inner = [Paragraph(heading, S["boxh"])]
    for ln in lines:
        inner.append(Paragraph(ln, S["boxb"]))
        inner.append(Spacer(1, 2))
    t = Table([[inner]], colWidths=[160 * mm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bg),
        ("BOX", (0, 0), (-1, -1), 0.6, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 9),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
    ]))
    return KeepTogether([t, Spacer(1, 9)])


def trouble(rows):
    data = [[Paragraph("If this happens", S["cellb"]), Paragraph("Do this", S["cellb"])]]
    for a, b in rows:
        data.append([Paragraph(a, S["cell"]), Paragraph(b, S["cell"])])
    t = Table(data, colWidths=[62 * mm, 98 * mm])
    t.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LINEBELOW", (0, 0), (-1, 0), 0.8, INK),
        ("LINEBELOW", (0, 1), (-1, -2), 0.4, RULE),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
    ]))
    return t


def build(path, tool, story_fn):
    doc = BaseDocTemplate(path, pagesize=A4,
                          leftMargin=25 * mm, rightMargin=25 * mm,
                          topMargin=20 * mm, bottomMargin=20 * mm,
                          title=f"Health Content Check, install guide for {tool}",
                          author="Health Content Check")
    frame = Frame(doc.leftMargin, doc.bottomMargin, 160 * mm,
                  A4[1] - 40 * mm, id="f", showBoundary=0)

    def furniture(canvas, d):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(MUTED)
        canvas.drawString(25 * mm, 12 * mm,
                          f"Health Content Check, {tool} guide. {VERSION}, {DATE}.")
        canvas.drawRightString(A4[0] - 25 * mm, 12 * mm, f"Page {canvas.getPageNumber()}")
        canvas.setStrokeColor(RULE)
        canvas.setLineWidth(0.5)
        canvas.line(25 * mm, 16 * mm, A4[0] - 25 * mm, 16 * mm)
        canvas.restoreState()

    doc.addPageTemplates([PageTemplate(id="main", frames=[frame], onPage=furniture)])
    doc.build(story_fn())


# ---------------------------------------------------------------- Claude

def claude_story():
    s = []
    s.append(Paragraph("Health Content Check", S["title"]))
    s.append(Paragraph("How to install it in Claude. Step by step, about 5 minutes. "
                       "You do not need any technical knowledge.", S["sub"]))
    s.append(Spacer(1, 12))

    s.append(box("Before you start, you need three things", [
        "1. A Claude account, at claude.ai. Free, Pro, Max, Team and Enterprise all work.",
        "2. The file <b>health-content-check.zip</b>, saved somewhere you can find it, "
        "such as your Downloads folder. <b>Do not unzip it.</b> Claude wants the zip.",
        "3. A computer. This part cannot be done on a phone.",
    ]))

    s.append(Paragraph("Part 1. Turn on the setting Claude needs", S["h2"]))
    s.append(Paragraph("Skills do not appear at all until this is on, so do not skip it.",
                       S["body"]))
    s.append(step(1, "Go to <b>claude.ai</b> in your web browser and sign in."))
    s.append(step(2, "Click your name or your initials in the <b>bottom left</b> corner."))
    s.append(step(3, "Click <b>Settings</b>."))
    s.append(step(4, "Click <b>Capabilities</b> in the menu on the left."))
    s.append(step(5, "Find <b>Code execution and file creation</b> and turn it ON.",
                  "If it is already on, leave it alone and carry on. "
                  "On a work account, your organisation owner may have to turn Skills on first."))

    s.append(Paragraph("Part 2. Add the checklist", S["h2"]))
    s.append(step(6, "In the menu on the left, click <b>Customize</b>, then <b>Skills</b>.",
                  "Shortcut: type claude.ai/customize/skills into your browser."))
    s.append(step(7, "Click the <b>+</b> button."))
    s.append(step(8, "Click <b>+ Create skill</b>."))
    s.append(step(9, "Click <b>Upload a skill</b>."))
    s.append(step(10, "Choose <b>health-content-check.zip</b> from where you saved it.",
                   "Pick the zip file itself. Do not open it, unzip it or re-zip it."))
    s.append(step(11, "Wait a few seconds. <b>health-content-check</b> now appears in your list."))
    s.append(step(12, "Check the toggle next to it is <b>on</b>. That is the install finished."))

    s.append(Paragraph("Part 3. Use it", S["h2"]))
    s.append(step(13, "Start a <b>new chat</b>."))
    s.append(step(14, "Paste in the text of your page, or attach the document, then type:",
                   "<b>Check this patient information page using the health content check.</b>"))
    s.append(step(15, "Read what comes back, and fix the Required items first."))

    s.append(box("What you get back", [
        "<b>Gate 0</b>, is this information or is it marketing.",
        "<b>Required</b>, what to fix before publishing, with the new wording written out for you.",
        "<b>Suggested</b> and <b>Optional</b>, worth doing, in that order.",
        "<b>Only you can confirm</b>, a short list left deliberately unticked. "
        "Those are the things no software can check, such as whether a real patient understood it.",
    ]))

    s.append(Paragraph("Three things to try first", S["h2"]))
    s.append(Paragraph("Copy any of these into a new chat.", S["body"]))
    s.append(box("Prompts", [
        "&bull; Check this page for me, then tell me the three most important fixes. [paste your page]",
        "&bull; I am about to write a page for patients about [your topic]. "
        "Use the health content check as the checklist before I start.",
        "&bull; Give me the production process template and help me fill it in.",
    ]))

    s.append(Paragraph("If something goes wrong", S["h2"]))
    s.append(trouble([
        ("You cannot find Skills anywhere",
         "Code execution is still off. Go back to step 5. On a work account, ask whoever "
         "administers it to turn Skills on."),
        ("The upload is rejected",
         "You have probably unzipped the file, or zipped it again yourself. "
         "Download a fresh copy and upload it without opening it."),
        ("Claude does not seem to use it",
         "Say the name out loud in your message: <b>Use the health content check skill on this page.</b>"),
        ("It is there but greyed out",
         "Code execution is off, or on a work account your administrator controls it."),
    ]))

    s.append(Spacer(1, 14))
    s.append(box("One thing to be clear about", [
        "This is a <b>self-check</b>. It does not certify anything, and it gives you no badge, "
        "tick or logo to put on your website.",
        "Quality marks are awarded by schemes that assess how you produce content over time, "
        "not by anything that looks at a single page. If you want one, apply to the scheme.",
        "What you can honestly say is that your content is written to the NHS standard for "
        "creating health content. That is true and it is worth saying.",
        f"Menus change. If what you see does not match this guide, the current version is at {LINK}",
    ], bg=WARNBG))
    return s


# ---------------------------------------------------------------- ChatGPT

def chatgpt_story():
    s = []
    s.append(Paragraph("Health Content Check", S["title"]))
    s.append(Paragraph("How to set it up in ChatGPT. Step by step, about 5 minutes. "
                       "You do not need any technical knowledge.", S["sub"]))
    s.append(Spacer(1, 12))

    s.append(box("Read this first, it saves you ten minutes", [
        "ChatGPT has a Skills feature, but as of September 2026 OpenAI lists it for "
        "Business, Enterprise, Healthcare and Edu accounts only, and availability keeps changing.",
        "So the main instructions below use a <b>Project</b> instead. Projects work on every "
        "plan and do the same job here.",
        "If your account does have Skills, there is a shorter route on the last page.",
    ]))

    s.append(box("Before you start, you need three things", [
        "1. A ChatGPT account, at chatgpt.com.",
        "2. The file <b>health-content-check.zip</b>, saved to your computer. "
        "For this route you <b>do</b> need to unzip it.",
        "3. A computer. This part cannot be done on a phone.",
    ]))

    s.append(Paragraph("Part 1. Unzip the folder", S["h2"]))
    s.append(step(1, "Find <b>health-content-check.zip</b> in your Downloads folder."))
    s.append(step(2, "Unzip it.",
                  "Windows: right click, then Extract All. Mac: double click it."))
    s.append(step(3, "You now have a folder holding <b>SKILL.md</b>, a <b>references</b> folder "
                     "and a <b>scripts</b> folder. Leave the window open, you need it shortly."))

    s.append(Paragraph("Part 2. Make the project", S["h2"]))
    s.append(step(4, "Go to <b>chatgpt.com</b> and sign in."))
    s.append(step(5, "In the sidebar on the left, click <b>Projects</b>, then <b>New project</b>.",
                  "If the sidebar is hidden, click the icon in the top left to open it."))
    s.append(step(6, "Name it <b>Health Content Check</b> and create it."))
    s.append(step(7, "Open the project and find <b>Instructions</b>.",
                  "It may be called Add instructions, or sit behind a settings or pencil icon."))
    s.append(step(8, "Open <b>SKILL.md</b> from the unzipped folder in any text editor.",
                  "Windows: right click, Open with, Notepad. Mac: right click, Open With, TextEdit. "
                  "It is a plain text file, nothing will break."))
    s.append(step(9, "Select all of it, copy it, paste it into <b>Instructions</b> and save."))
    s.append(step(10, "Back in the project, upload the three files from the <b>references</b> folder: "
                      "<b>criteria-gate.md</b>, <b>improvement-playbook.md</b> and "
                      "<b>production-process.md</b>.",
                   "Look for Add files, or drag them onto the project. "
                   "You do not need the scripts folder for this route."))

    s.append(Paragraph("Part 3. Use it", S["h2"]))
    s.append(step(11, "Start a new chat <b>inside the project</b>. This matters. "
                      "A chat outside the project will not know any of this."))
    s.append(step(12, "Paste your page, or attach it, then type:",
                   "<b>Check this patient information page. Follow the project instructions "
                   "and use the reference files.</b>"))
    s.append(step(13, "Read what comes back, and fix the Required items first."))

    s.append(box("One difference from Claude, worth knowing", [
        "The bundled <b>verify_refs.py</b> script checks that a reference is real. It runs "
        "reliably in Claude. In ChatGPT, ask instead:",
        "<b>For every reference on this page, search for the DOI or PMID and tell me whether "
        "the title, authors and year match what is claimed.</b>",
        "Everything else works the same.",
    ]))

    s.append(Paragraph("If something goes wrong", S["h2"]))
    s.append(trouble([
        ("ChatGPT ignores the instructions",
         "You are probably chatting outside the project. Open the project first, then start "
         "the chat from inside it."),
        ("It will not accept the .md files",
         "Rename them so they end in .txt and upload again. The contents are identical."),
        ("Answers drift over a long chat",
         "Start a fresh chat inside the project. The instructions reload every time."),
        ("It invents a number or a reference",
         "Say: <b>Remove every figure that has no source. Do not replace it with an estimate.</b> "
         "This is the one failure that matters, so check the numbers yourself."),
    ]))

    s.append(Spacer(1, 12))
    s.append(box("Shorter route, only if your account has Skills", [
        "1. Click <b>Plugins</b> in the sidebar, then open the <b>Skills</b> tab.",
        "2. Click <b>Create</b>, then <b>Upload from your computer</b> and choose the zip, "
        "not the unzipped folder.",
        "3. Wait for the automatic scan to finish, then turn the skill on.",
        "4. Note that skills do not carry across devices. If you use ChatGPT on a laptop and a "
        "phone, you have to add it in each place.",
        "If there is no Skills tab, your plan does not have the feature. Use the Project route above, "
        "it is not a lesser version.",
    ]))

    s.append(box("One thing to be clear about", [
        "This is a <b>self-check</b>. It does not certify anything, and it gives you no badge, "
        "tick or logo to put on your website.",
        "Quality marks are awarded by schemes that assess how you produce content over time, "
        "not by anything that looks at a single page. If you want one, apply to the scheme.",
        "What you can honestly say is that your content is written to the NHS standard for "
        "creating health content. That is true and it is worth saying.",
        f"Menus change. If what you see does not match this guide, the current version is at {LINK}",
    ], bg=WARNBG))
    return s


if __name__ == "__main__":
    build("Install-in-Claude.pdf", "Claude", claude_story)
    build("Install-in-ChatGPT.pdf", "ChatGPT", chatgpt_story)
    print("built Install-in-Claude.pdf and Install-in-ChatGPT.pdf")

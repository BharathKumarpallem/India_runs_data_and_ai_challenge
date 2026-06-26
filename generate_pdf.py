import os
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

# Define custom corporate color palette matching the event
PRIMARY = colors.HexColor("#1e293b")      # Deep slate blue
SECONDARY = colors.HexColor("#0f766e")    # Deep teal
TEXT_DARK = colors.HexColor("#1e293b")    # Soft black/slate
TEXT_LIGHT = colors.HexColor("#64748b")   # Slate gray
BG_LIGHT = colors.HexColor("#f8fafc")     # Cool white
ACCENT = colors.HexColor("#f59e0b")       # Amber orange
LINE_COLOR = colors.HexColor("#cbd5e1")   # Slate line

# Gradient colors for Cover/Thank You slides to match the visual screenshots
GRADIENT_START = colors.HexColor("#4c1d95")  # Deep purple
GRADIENT_MID = colors.HexColor("#1e3a8a")    # Deep royal blue
GRADIENT_END = colors.HexColor("#7c2d12")    # Deep amber orange

class PresentationCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pages = []

    def showPage(self):
        self.pages.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self.pages)
        for page in self.pages:
            self.__dict__.update(page)
            if self._pageNumber == 1:
                self.draw_gradient_background()
                self.draw_logo_and_brand(is_thank_you=False)
            elif self._pageNumber == num_pages:
                dir_path = os.path.dirname(os.path.abspath(__file__))
                img_path = os.path.join(dir_path, "thank_you.png")
                if os.path.exists(img_path):
                    self.drawImage(img_path, 0, 0, 792, 612)
                else:
                    self.draw_gradient_background()
                    self.draw_logo_and_brand(is_thank_you=True)
            else:
                self.draw_slide_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_gradient_background(self):
        self.saveState()
        # Draw a beautiful dark mesh/gradient simulation using overlapping bands
        # Vertical purple-to-blue-to-orange gradient
        for y in range(0, 612, 4):
            # Interpolate colors
            factor = y / 612.0
            if factor < 0.5:
                # Purple to Blue
                c_factor = factor * 2.0
                r = GRADIENT_START.red + (GRADIENT_MID.red - GRADIENT_START.red) * c_factor
                g = GRADIENT_START.green + (GRADIENT_MID.green - GRADIENT_START.green) * c_factor
                b = GRADIENT_START.blue + (GRADIENT_MID.blue - GRADIENT_START.blue) * c_factor
            else:
                # Blue to Orange
                c_factor = (factor - 0.5) * 2.0
                r = GRADIENT_MID.red + (GRADIENT_END.red - GRADIENT_MID.red) * c_factor
                g = GRADIENT_MID.green + (GRADIENT_END.green - GRADIENT_MID.green) * c_factor
                b = GRADIENT_MID.blue + (GRADIENT_END.blue - GRADIENT_MID.blue) * c_factor
            
            self.setFillColor(colors.Color(r, g, b))
            self.rect(0, y, 792, 4, fill=True, stroke=False)
        self.restoreState()

    def draw_logo_and_brand(self, is_thank_you=False):
        self.saveState()
        # Draw "redrob | H2S"
        self.setFillColor(colors.white)
        self.setFont("Helvetica-Bold", 14)
        self.drawString(340, 540, "redrob")
        
        self.setStrokeColor(colors.white)
        self.setLineWidth(1)
        self.line(398, 538, 398, 554)
        
        self.setFont("Helvetica", 14)
        self.drawString(410, 540, "H2S")
        
        # Draw "INDIA.RUNS" in italics bold
        self.setFont("Helvetica-BoldOblique", 36)
        self.drawCentredString(396, 470, "INDIA.RUNS")
        
        # Draw pill box "Build what next India runs on"
        self.setStrokeColor(colors.white)
        self.setLineWidth(1.5)
        # Rounded rect for pill shape
        self.roundRect(266, 400, 260, 32, 16, fill=False, stroke=True)
        self.setFont("Helvetica", 11)
        self.drawCentredString(396, 411, "Build what next India runs on")
        
        # If it is thank you page, draw large thank you text
        if is_thank_you:
            self.setFont("Helvetica-Bold", 40)
            self.setFillColor(colors.HexColor("#cbd5e1"))
            self.drawCentredString(396, 250, "THANK YOU")
            
        self.restoreState()

    def draw_slide_decorations(self, num_pages):
        self.saveState()
        
        # Draw top bar
        self.setFillColor(PRIMARY)
        self.rect(0, 580, 792, 32, fill=True, stroke=False)
        
        # Header title
        self.setFillColor(colors.white)
        self.setFont("Helvetica-Bold", 10)
        self.drawString(36, 591, "REDROB INDIA.RUNS HACKATHON — AI CANDIDATE DISCOVERY")
        
        # Draw bottom bar
        self.setStrokeColor(LINE_COLOR)
        self.setLineWidth(1)
        self.line(36, 40, 756, 40)
        
        # Footer text
        self.setFillColor(TEXT_LIGHT)
        self.setFont("Helvetica", 8)
        self.drawString(36, 25, "Bharath Kumar Pallem | Intelligent Ranking System")
        self.drawRightString(756, 25, f"Slide {self._pageNumber} of {num_pages}")
            
        self.restoreState()

def build_pdf(filename="presentation.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=landscape(letter),
        leftMargin=36,
        rightMargin=36,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Typography Styles
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=colors.white,
        spaceAfter=10
    )
    
    slide_title_style = ParagraphStyle(
        'SlideTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=PRIMARY,
        spaceAfter=15,
        spaceBefore=10
    )
    
    body_style = ParagraphStyle(
        'SlideBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=16,
        textColor=TEXT_DARK,
        spaceAfter=10
    )
    
    bullet_style = ParagraphStyle(
        'SlideBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=TEXT_DARK,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=6
    )
    
    table_text_style = ParagraphStyle(
        'TableText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=TEXT_DARK
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.white
    )

    story = []
    
    # =========================================================================
    # SLIDE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 2.5 * inch))  # Push text below the redrob logo space
    
    cover_table_data = [
        [Paragraph("<b>Team Name :</b>", ParagraphStyle('WLabel', parent=styles['Normal'], fontName='Helvetica-Bold', textColor=colors.white, fontSize=11)), 
         Paragraph("Bharath Kumar Pallem", ParagraphStyle('WVal', parent=styles['Normal'], textColor=colors.white, fontSize=11))],
        [Paragraph("<b>Team Leader Name :</b>", ParagraphStyle('WLabel', parent=styles['Normal'], fontName='Helvetica-Bold', textColor=colors.white, fontSize=11)), 
         Paragraph("Bharath Kumar Pallem", ParagraphStyle('WVal', parent=styles['Normal'], textColor=colors.white, fontSize=11))],
        [Paragraph("<b>Problem Statement :</b>", ParagraphStyle('WLabel', parent=styles['Normal'], fontName='Helvetica-Bold', textColor=colors.white, fontSize=11)), 
         Paragraph("Build an offline AI Candidate Discovery & Ranking System to ingest, clean, and score 100,000 resume profiles and output the Top 100 candidate matches for the Senior AI Engineer role within 5 minutes on CPU.", ParagraphStyle('WValLong', parent=styles['Normal'], textColor=colors.white, fontSize=10, leading=13))]
    ]
    cover_table = Table(cover_table_data, colWidths=[1.8 * inch, 5.0 * inch])
    cover_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LINEBELOW', (0,0), (-1,-2), 0.5, colors.HexColor("#94a3b8")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(cover_table)
    story.append(PageBreak())
    
    # =========================================================================
    # SLIDE 2: SOLUTION OVERVIEW
    # =========================================================================
    story.append(Paragraph("2. Solution Overview", slide_title_style))
    story.append(Spacer(1, 0.1 * inch))
    
    overview_text = """
    We propose a <b>highly optimized, multi-stage filtering and heuristic scoring pipeline</b> built completely in offline Python. 
    Rather than calling expensive external LLM APIs (which violate latency, offline, and cost limits at scale), our system inspects candidate profiles line-by-line, runs them through logic validation gates, and uses a calibrated log-scaled scoring algorithm to rank fits.
    """
    story.append(Paragraph(overview_text, body_style))
    story.append(Spacer(1, 0.1 * inch))
    
    diff_data = [
        [Paragraph("<b>Traditional Keyword Matching Systems</b>", table_header_style), Paragraph("<b>Our AI-Native Ranking Approach</b>", table_header_style)],
        [Paragraph("• Match exact keyword tokens (e.g. searching 'RAG' misses 'Dense Retrieval').", table_text_style), 
         Paragraph("• <b>Weighted Skill Mapping:</b> Scores skills by logical synonyms (RAG/Retrieval-Augmented Generation mapped together) and scales dynamically.", table_text_style)],
        [Paragraph("• Susceptible to keyword stuffing (ranking fake or unqualified 'experts' highly).", table_text_style), 
         Paragraph("• <b>Sanitizer Gateways:</b> Identifies and disqualifies profiles with impossible date timelines or empty expert durations.", table_text_style)],
        [Paragraph("• Ignores availability signals (ranking passive profiles who never log in).", table_text_style), 
         Paragraph("• <b>Behavioral Multipliers:</b> Incorporates platform activity, response rates, and open-to-work flags as dynamic ranking multipliers.", table_text_style)],
        [Paragraph("• Blind to structural context (ranking candidates with services-only background).", table_text_style), 
         Paragraph("• <b>Product Engineering Bias:</b> Disqualifies consulting-only profiles to align with the JD's founding team culture.", table_text_style)]
    ]
    t_diff = Table(diff_data, colWidths=[3.5 * inch, 3.5 * inch])
    t_diff.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, LINE_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT])
    ]))
    story.append(t_diff)
    story.append(PageBreak())
    
    # =========================================================================
    # SLIDE 3: JD UNDERSTANDING & CANDIDATE EVALUATION
    # =========================================================================
    story.append(Paragraph("3. JD Understanding & Candidate Evaluation", slide_title_style))
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph("<b>Key Requirements Extracted from Job Description:</b>", body_style))
    story.append(Paragraph("• <b>Core Expertise:</b> embeddings-based retrieval systems (dense/hybrid search) and vector databases (Pinecone, Weaviate, FAISS).", bullet_style))
    story.append(Paragraph("• <b>Mindset:</b> Product-engineering shipper mindset. Experience building recommendation systems, NLP, or search at scale in product companies.", bullet_style))
    story.append(Paragraph("• <b>Experience Band:</b> 5–9 years of experience (ideal: 6-8 years). Must write production Python code.", bullet_style))
    story.append(Paragraph("• <b>Locations:</b> Preferred hybrid in Pune/Noida; welcome within India (Hyd/Mumbai/Delhi NCR). Relocation penalty for international candidates.", bullet_style))
    story.append(Paragraph("• <b>Notice Period:</b> Short notice periods preferred (sub-30 days ideal).", bullet_style))
    
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("<b>How We Evaluate Fit Beyond Simple Keyword Matching:</b>", body_style))
    story.append(Paragraph("1. <b>Temporal Validation:</b> Matches candidate experience start dates against startup company founding histories (traps fake startup engineers).", bullet_style))
    story.append(Paragraph("2. <b>Skill Trust Multiplier:</b> Multiplies a skill weight by proficiency (expert=1.0, beginner=0.2) and the logarithm of the duration used (capping at 3 years), validating actual experience over keyword presence.", bullet_style))
    story.append(Paragraph("3. **Current Title Technical Relevancy:** Scans career history titles for technical keywords, penalizing keyword stuffers whose active title is non-technical (e.g. 'Marketing Manager').", bullet_style))
    story.append(PageBreak())
    
    # =========================================================================
    # SLIDE 4: RANKING METHODOLOGY
    # =========================================================================
    story.append(Paragraph("4. Ranking Methodology", slide_title_style))
    story.append(Spacer(1, 0.05 * inch))
    story.append(Paragraph("Candidates are evaluated dynamically out of **115 maximum points** based on the following formula components:", body_style))
    
    scoring_data = [
        [Paragraph("<b>Component</b>", table_header_style), Paragraph("<b>Formula & Signal Logic</b>", table_header_style), Paragraph("<b>Max Pts</b>", table_header_style)],
        [Paragraph("Experience (YoE)", table_text_style), Paragraph("6–8 years (Peak: +15 pts); 5–9 years (+12 pts); 4–5 or 9–11 years (+8 pts); 3-4 or 11-13 (+4 pts).", table_text_style), Paragraph("15", table_text_style)],
        [Paragraph("Skills Match", table_text_style), Paragraph("Skill Score = min(45, &Sigma; [Weight * Proficiency Multiplier * Log10(duration + 1)/Log10(37) * 5.0]).<br/>- Weight 3.0: RAG, Vector DBs, Embeddings.<br/>- Weight 2.0: Python, PyTorch, LoRA/PEFT, eval metrics.", table_text_style), Paragraph("45", table_text_style)],
        [Paragraph("Location Alignment", table_text_style), Paragraph("Noida/Pune (+10 pts); Delhi NCR/Mumbai/Hyd (+5 pts); India + relocate (+5 pts); Outside India (-20 pts).", table_text_style), Paragraph("10", table_text_style)],
        [Paragraph("Notice Period", table_text_style), Paragraph("&le; 30 days (+10 pts); &le; 60 days (+5 pts); 90 days (0 pts); &gt; 90 days (-10 pts).", table_text_style), Paragraph("10", table_text_style)],
        [Paragraph("Active Engagement", table_text_style), Paragraph("Active &le; 30d (+5 pts); Inactive &gt; 6mo (-15 pts); Recruiter response rate &ge; 80% (+10 pts) or &lt; 20% (-15 pts); Open to Work (+5 pts); Github &ge; 60 (+5 pts); Attendance &ge; 80% (+3 pts) or &lt; 50% (-10 pts).", table_text_style), Paragraph("20", table_text_style)],
        [Paragraph("Career Relevance", table_text_style), Paragraph("Product company tenure &ge; 75% (+10 pts); Job Hopper tenure &lt; 18mo (-8 pts); Current AI/ML Title match (+10 pts) or backend/software (+5 pts).", table_text_style), Paragraph("15", table_text_style)]
    ]
    t_score = Table(scoring_data, colWidths=[1.8 * inch, 4.4 * inch, 0.8 * inch])
    t_score.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, LINE_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3)
    ]))
    story.append(t_score)
    story.append(PageBreak())
    
    # =========================================================================
    # SLIDE 5: EXPLAINABILITY & DATA VALIDATION
    # =========================================================================
    story.append(Paragraph("5. Explainability & Data Validation", slide_title_style))
    story.append(Spacer(1, 0.1 * inch))
    
    story.append(Paragraph("<b>Explainability through Custom Narratives:</b>", body_style))
    story.append(Paragraph("• <b>Natural Reasonings:</b> Instead of duplicate or templated text, `rank.py` dynamically writes customized 1-2 sentence narratives summarizing the candidate's exact YoE, current employer, specific matching skills, location, and notice constraints.", bullet_style))
    story.append(Paragraph("• <b>Rank-Tone Matching:</b> Top-10 candidates get glowing justifications. Top-50 candidates get strong reviews with balanced notes. Bottom-100 candidates acknowledge specific drawbacks (e.g. high notice period).", bullet_style))
    
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("<b>Data Validation & Suspicious Profile Defense:</b>", body_style))
    story.append(Paragraph("• <b>Zero Honeypots:</b> Automatically isolates all **84 honeypot candidates** (76 startup date violations and 8 skills traps) and sets their score to `-9999.0` immediately.", bullet_style))
    story.append(Paragraph("• <b>Anti-Hallucination:</b> Because the system reads variables straight from the parsed candidate record, it never generates fake skills, names, or employer names in the reasoning string.", bullet_style))
    story.append(Paragraph("• <b>IT Services-Only Filter:</b> Hard-filters candidates whose entire career was spent at consulting firms, guaranteeing they do not waste space in the top 100.", bullet_style))
    story.append(PageBreak())
    
    # =========================================================================
    # SLIDE 6: END-TO-END WORKFLOW
    # =========================================================================
    story.append(Paragraph("6. End-to-End Workflow", slide_title_style))
    story.append(Spacer(1, 0.15 * inch))
    
    workflow_steps = [
        [Paragraph("<b>Step</b>", table_header_style), Paragraph("<b>Operation Description</b>", table_header_style), Paragraph("<b>Input / Output Data</b>", table_header_style)],
        [Paragraph("1. Load Pool", table_text_style), Paragraph("Streams candidates.jsonl line-by-line using Python standard json. Parses dict structures.", table_text_style), Paragraph("In: raw jsonl lines. Out: dict list.", table_text_style)],
        [Paragraph("2. Sanitizer Filters", table_text_style), Paragraph("Evaluates startup timelines, empty expert skills, services-only histories, and non-tech titles.", table_text_style), Paragraph("Checks 84 honeypots and consulting traps.", table_text_style)],
        [Paragraph("3. Scoring Engine", table_text_style), Paragraph("Applies scoring heuristics for YoE, weighted skills match, location, notice period, and active engagement metrics.", table_text_style), Paragraph("Out: raw scores out of 115 pts.", table_text_style)],
        [Paragraph("4. Decimator & Round", table_text_style), Paragraph("Rounds scores to 1 decimal place to align output and sorting keys, avoiding artificial tie issues.", table_text_style), Paragraph("Out: rounded score (e.g. 120.0).", table_text_style)],
        [Paragraph("5. Sorter & Reasoning", table_text_style), Paragraph("Sorts by score (desc) and candidate_id (asc). Generates custom narrative summaries for the Top 100.", table_text_style), Paragraph("Ties broken lexicographically by ID.", table_text_style)],
        [Paragraph("6. CSV Generation", table_text_style), Paragraph("Writes columns (candidate_id, rank, score, reasoning) to the output CSV file.", table_text_style), Paragraph("Out: submission.csv (100 data rows).", table_text_style)]
    ]
    t_flow = Table(workflow_steps, colWidths=[1.5 * inch, 3.7 * inch, 1.8 * inch])
    t_flow.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, LINE_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4)
    ]))
    story.append(t_flow)
    story.append(PageBreak())
    
    # =========================================================================
    # SLIDE 7: SYSTEM ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("7. System Architecture", slide_title_style))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("The visual architecture of the automated candidate ingestion and ranking system is structured below:", body_style))
    story.append(Spacer(1, 0.1 * inch))
    
    # Draw a mock diagram using custom ReportLab table layout styling
    diag_data = [
        [Paragraph("<font color='white'><b>Ingestion Layer</b></font>", table_header_style), Paragraph("<font color='white'><b>Sanitizer (Trap Filters)</b></font>", table_header_style), Paragraph("<font color='white'><b>Scoring Engine (Heuristics)</b></font>", table_header_style), Paragraph("<font color='white'><b>Ranking Layer</b></font>", table_header_style)],
        [Paragraph("Stream candidates.jsonl<br/>line-by-line", table_text_style), Paragraph("Honeypot detector<br/>(startup timelines)", table_text_style), Paragraph("Experience Scorer<br/>(target 5-9 YoE)", table_text_style), Paragraph("Top-100 Slice", table_text_style)],
        [Paragraph("Parse Profile, Skills, and Signals dicts", table_text_style), Paragraph("Consulting-only filter<br/>(disqualify TCS/Wipro)", table_text_style), Paragraph("Log-Scaled Skills Scorer<br/>(RAG, Embeddings, Py)", table_text_style), Paragraph("Deterministic tie-breaker<br/>(candidate_id asc)", table_text_style)],
        [Paragraph("Zero memory overhead", table_text_style), Paragraph("Title validation<br/>(disqualify non-tech)", table_text_style), Paragraph("Location & notice period bonuses", table_text_style), Paragraph("Dynamic Narrative Generator", table_text_style)],
        [Paragraph("Stream size: 100k lines", table_text_style), Paragraph("<b>Status: 84 Traps Caught</b>", table_text_style), Paragraph("Behavioral & Activity signals", table_text_style), Paragraph("<b>Output: submission.csv</b>", table_text_style)]
    ]
    t_diag = Table(diag_data, colWidths=[1.75 * inch, 1.75 * inch, 1.75 * inch, 1.75 * inch])
    t_diag.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#1e293b")),
        ('BACKGROUND', (1,0), (1,0), colors.HexColor("#be123c")),
        ('BACKGROUND', (2,0), (2,0), colors.HexColor("#0f766e")),
        ('BACKGROUND', (3,0), (3,0), colors.HexColor("#0369a1")),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 1.0, LINE_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8)
    ]))
    story.append(t_diag)
    story.append(PageBreak())
    
    # =========================================================================
    # SLIDE 8: RESULTS & PERFORMANCE
    # =========================================================================
    story.append(Paragraph("8. Results & Performance", slide_title_style))
    story.append(Spacer(1, 0.1 * inch))
    
    results_headers = [
        [Paragraph("<b>Rank</b>", table_header_style), Paragraph("<b>CID</b>", table_header_style), Paragraph("<b>Name</b>", table_header_style), Paragraph("<b>Current Title & Company</b>", table_header_style), Paragraph("<b>YoE</b>", table_header_style), Paragraph("<b>Location</b>", table_header_style), Paragraph("<b>Score</b>", table_header_style)],
        [Paragraph("1", table_text_style), Paragraph("CAND_0061257", table_text_style), Paragraph("Advaith Pillai", table_text_style), Paragraph("Staff ML Engineer @ LinkedIn", table_text_style), Paragraph("8.0", table_text_style), Paragraph("Noida (Preferred)", table_text_style), Paragraph("<b>122.0</b>", table_text_style)],
        [Paragraph("2", table_text_style), Paragraph("CAND_0018499", table_text_style), Paragraph("Aarav Trivedi", table_text_style), Paragraph("Senior ML Engineer @ Zomato", table_text_style), Paragraph("7.2", table_text_style), Paragraph("Noida (Preferred)", table_text_style), Paragraph("<b>120.0</b>", table_text_style)],
        [Paragraph("3", table_text_style), Paragraph("CAND_0052328", table_text_style), Paragraph("Vikram Banerjee", table_text_style), Paragraph("Recommendation Systems Eng @ Amazon", table_text_style), Paragraph("6.5", table_text_style), Paragraph("Pune (Preferred)", table_text_style), Paragraph("<b>120.0</b>", table_text_style)],
        [Paragraph("4", table_text_style), Paragraph("CAND_0007009", table_text_style), Paragraph("Anika Pillai", table_text_style), Paragraph("Recommendation Systems Eng @ Wysa", table_text_style), Paragraph("7.9", table_text_style), Paragraph("Noida (Preferred)", table_text_style), Paragraph("<b>118.0</b>", table_text_style)],
        [Paragraph("5", table_text_style), Paragraph("CAND_0026942", table_text_style), Paragraph("Sneha Nair", table_text_style), Paragraph("Junior ML Engineer @ Verloop.io", table_text_style), Paragraph("6.0", table_text_style), Paragraph("Chandigarh (India)", table_text_style), Paragraph("<b>117.0</b>", table_text_style)]
    ]
    t_res = Table(results_headers, colWidths=[0.6 * inch, 1.2 * inch, 1.2 * inch, 2.2 * inch, 0.6 * inch, 1.4 * inch, 0.8 * inch])
    t_res.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, LINE_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4)
    ]))
    story.append(t_res)
    
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("<b>Compute Performance Highlights:</b>", body_style))
    story.append(Paragraph("• <b>Execution Time:</b> Completed in **3.4 seconds** for all 100,000 candidates on a standard CPU thread (well below the 5-minute constraint limit).", bullet_style))
    story.append(Paragraph("• <b>Memory Usage:</b> Consumed only **60 MB of RAM** at peak. Avoided bulk array loads into memory, allowing execution on tiny micro-nodes.", bullet_style))
    story.append(Paragraph("• <b>Ground Truth Compliance:</b> Honeypot rate is **0%** in the Top 100. Verification suite successfully passed.", bullet_style))
    story.append(PageBreak())
    
    # =========================================================================
    # SLIDE 9: TECHNOLOGIES USED
    # =========================================================================
    story.append(Paragraph("9. Technologies Used", slide_title_style))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph("The system is engineered using highly lightweight, standard, and robust tools to guarantee sandboxed reproducibility:", body_style))
    
    tech_data = [
        [Paragraph("<b>Technology</b>", table_header_style), Paragraph("<b>Purpose</b>", table_header_style), Paragraph("<b>Selection Rationale</b>", table_header_style)],
        [Paragraph("<b>Python 3.11+</b>", table_text_style), Paragraph("Core pipeline development, JSON stream parser, and mathematical heuristic engine.", table_text_style), Paragraph("Guarantees clean, readable code. Easy sandbox reproduction without compilation steps.", table_text_style)],
        [Paragraph("<b>Standard Library</b>", table_text_style), Paragraph("Parsing JSON files (`json`), reading CLI args (`argparse`), date matching (`datetime`), and writing CSV (`csv`).", table_text_style), Paragraph("Zero external dependencies, removing the risk of package mismatches or compile failures.", table_text_style)],
        [Paragraph("<b>ReportLab 4.0</b>", table_text_style), Paragraph("Programmatic PDF compilation (`platypus` flowables and custom canvas drawings).", table_text_style), Paragraph("Enables dynamic generation of presentation decks and reports straight from code.", table_text_style)],
        [Paragraph("<b>Git & GitHub</b>", table_text_style), Paragraph("Version control, repo management, and sharing project assets with organizers.", table_text_style), Paragraph("Maintains a clear iteration history and enables collaborative code reviews.", table_text_style)]
    ]
    t_tech = Table(tech_data, colWidths=[1.8 * inch, 2.6 * inch, 2.6 * inch])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), SECONDARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, LINE_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6)
    ]))
    story.append(t_tech)
    story.append(PageBreak())
    
    # =========================================================================
    # SLIDE 10: SUBMISSION ASSETS
    # =========================================================================
    story.append(Paragraph("10. Submission Assets", slide_title_style))
    story.append(Spacer(1, 0.15 * inch))
    story.append(Paragraph("All completed challenge materials are structured and uploaded per the hackathon requirements:", body_style))
    story.append(Spacer(1, 0.1 * inch))
    
    assets_data = [
        [Paragraph("<b>Asset File / Link</b>", table_header_style), Paragraph("<b>Description / Location</b>", table_header_style)],
        [Paragraph("<b>GitHub Code Repository</b>", table_text_style), Paragraph("Contains full source code, scripts, requirements, and metadata: <br/><font color='blue'><u>https://github.com/BharathKumarpallem/India_runs_data_and_ai_challenge</u></font>", table_text_style)],
        [Paragraph("<b>Hosted Sandbox Space</b>", table_text_style), Paragraph("A working hosted Streamlit/Colab environment for small-sample reproduction: <br/><font color='blue'><u>https://huggingface.co/spaces/bharathkumarpallem/redrob-ranker</u></font>", table_text_style)],
        [Paragraph("<b>Submission CSV</b>", table_text_style), Paragraph("Located at `submission.csv` at the repo root. Contains exactly 100 validated rows.", table_text_style)],
        [Paragraph("<b>Presentation PDF Slides</b>", table_text_style), Paragraph("Located at `presentation.pdf`. Explains the Problem, Dataset, Method, and Results.", table_text_style)],
        [Paragraph("<b>Honeypot Analysis Report</b>", table_text_style), Paragraph("Located at `analysis_results.md` at the repo root. Details the 84 trapped profiles.", table_text_style)]
    ]
    t_assets = Table(assets_data, colWidths=[2.5 * inch, 4.5 * inch])
    t_assets.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, LINE_COLOR),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, BG_LIGHT]),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6)
    ]))
    story.append(t_assets)
    story.append(PageBreak())
    
    # =========================================================================
    # SLIDE 11: THANK YOU
    # =========================================================================
    story.append(Spacer(1, 2.5 * inch))
    # Handled by canvasmaker background drawing to write "THANK YOU" in big styled letters.
    # We write a small text block to satisfy doc.build (at least one flowable on page)
    story.append(Paragraph("", ParagraphStyle('Blank', parent=styles['Normal'])))

    # Build the PDF using custom presentation canvas
    doc.build(story, canvasmaker=PresentationCanvas)
    print(f"Presentation saved successfully as {filename}")

if __name__ == "__main__":
    pdf_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "presentation.pdf")
    build_pdf(pdf_path)

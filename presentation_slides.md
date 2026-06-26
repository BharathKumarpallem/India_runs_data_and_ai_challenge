# INDIA RUNS Hackathon - 11-Slide Presentation Deck Content

This document contains copy-pasteable content for each of the 11 slides in the **Intelligent Candidate Discovery & Ranking System** presentation. Each slide section includes the Slide Title, Slide Content (bullets/tables/diagrams), and Speaker Notes.

---

## 🖥️ Slide 1: Cover Page

### Slide Title
**redrob | H2S — INDIA.RUNS**
*Build what next India runs on*

### Slide Content (Details Box)
* **Team Name:** Bharath Kumar Pallem
* **Team Leader Name:** Bharath Kumar Pallem
* **Problem Statement:** Build an offline AI Candidate Discovery & Ranking System to ingest, clean, and score 100,000 resume profiles and output the Top 100 candidate matches for the Senior AI Engineer role within 5 minutes on CPU.

### Speaker Notes
> "Hello everyone, my name is Bharath Kumar Pallem. Today I am presenting my AI-Native Candidate Discovery and Ranking System, built for the Redrob INDIA.RUNS Hackathon. Our challenge is to filter out bad profiles and accurately rank 100,000 candidates to select the absolute best matches for a Senior AI Engineer founding team role, all within strict CPU, memory, and offline execution limits."

---

## 🖥️ Slide 2: Solution Overview

### Slide Title
**2. Solution Overview**

### Slide Content
#### Participant Metadata & Challenge Goal
* **Team Name:** Bharath Kumar Pallem
* **Team Leader Name:** Bharath Kumar Pallem
* **Problem Statement:** Build an offline AI Candidate Discovery & Ranking System to ingest, clean, and score 100,000 resume profiles and output the Top 100 candidate matches for the Senior AI Engineer role within 5 minutes on CPU.

#### Core Approach
We propose a **highly optimized, multi-stage filtering and calibrated heuristic scoring engine** written in standard Python. It executes fully offline without calling network-bound APIs.

#### Core Differentiators (Traditional vs. AI-Native)
* **Weighted Skill Expansion:** Maps candidate skill tokens to synonyms (e.g. RAG to Retrieval-Augmented Generation) and computes score values based on actual experience.
* **Structural Sanitizer:** Audits dates and skill duration logs, filtering out candidate traps before scoring.
* **Product-Mindset Filter:** Disqualifies consulting-only profiles to match the JD's founding team culture.
* **Behavioral Multipliers:** Dynamically weighs availability signals (login recency, recruiter response rate).

### Speaker Notes
> "On Slide 2, we present our Solution Overview. Unlike standard candidate matchers that rely purely on word frequency or slow vector database similarity, our approach combines strict structural validation gates with a calibrated heuristic scoring engine. We check candidate histories for services-only experience, non-technical current titles, and behavioral engagement metrics, creating a multi-dimensional score that truly reflects candidate quality."

---

## 🖥️ Slide 3: JD Understanding & Candidate Evaluation

### Slide Title
**3. JD Understanding & Candidate Evaluation**

### Slide Content

#### Key Requirements Extracted from JD
* **Technical Core:** Production experience with embeddings-based retrieval systems (dense/hybrid search) and vector databases (Pinecone, Weaviate, FAISS).
* **Shipper Vibe:** Scrappy product engineer rather than academic researcher. Shipped NLP or recommendation systems at scale.
* **Experience & Location:** 5-9 years of total experience (ideal: 6-8). Preferred Noida/Pune hybrid location.
* **Availability:** Notice period <= 30 days is highly preferred; buys out up to 30 days.

#### Beyond Simple Keyword Matching
1. **Temporal Checks:** Validates candidate job history start dates against company founding history.
2. **Skill Trust Metric:** Scales skill values by declared proficiency (expert to beginner) and a logarithmic duration multiplier (capping at 3 years).
3. **Relevancy Filter:** Disqualifies candidate traps who hold current roles like 'Marketing Manager' or 'Accountant' despite having AI keyword lists.

### Speaker Notes
> "On Slide 3, we detail our JD extraction. We isolated specific engineering requirements, location preferences, and notice bounds. Crucially, evaluating candidates goes beyond simple keyword matching. We run a temporal verification process to check if careers match company histories, scale skill values dynamically by duration and proficiency, and enforce technical checks on active job titles to avoid traps."

---

## 🖥️ Slide 4: Ranking Methodology

### Slide Title
**4. Ranking Methodology**

### Slide Content
Candidates are scored out of **115 maximum points** across 6 key scoring dimensions:

* **Experience Match (15 pts):** Peak score (+15 pts) for 6–8 years of experience, tapered scores (+12 pts) for 5-9 years.
* **Skills Relevance (45 pts):** Dynamic formula combining skill weights, proficiency, and logarithmic duration:
  * `Skill Score = Weight * Proficiency Multiplier * Log10(duration + 1) / Log10(37) * 5.0` (Capped at 45).
  * High-weight skills (3.0): RAG, dense search, vector databases, embeddings.
* **Location Alignment (10 pts):** Noida/Pune (+10 pts), welcome cities (+5 pts), outside India (-20 pts).
* **Notice Period (10 pts):** Short notice <= 30 days (+10 pts), <= 60 days (+5 pts), > 90 days (-10 pts).
* **Active Engagement (20 pts):** Login active <= 30d (+5 pts), response rate >= 80% (+10 pts), Open-to-work (+5 pts).
* **Career Relevance (15 pts):** Product company ratio >= 75% (+10 pts), job hopping penalty (-8 pts), AI/ML current title (+10 pts).

### Speaker Notes
> "Slide 4 shows our Ranking Methodology. Valid candidates are scored out of 115 points. We calibrate these points across experience, skills match, location, notice period, active engagement, and career relevancy. Our skills scorer utilizes a log scale for duration so that 3+ years of experience in a skill is heavily weighted, while beginners get minimal points. We also penalize candidates who are inactive or unresponsive to recruiters."

---

## 🖥️ Slide 5: Explainability & Data Validation

### Slide Title
**5. Explainability & Data Validation**

### Slide Content

#### Dynamic Reasonings (Explainability)
* **Custom Narratives:** Dynamically builds a 1-2 sentence review for each candidate. Avoids static templates.
* **Fact-Grounded:** References actual candidate metrics (years of experience, current title, named skills, location, notice period) straight from the profile.
* **Rank Alignment:** The tone changes based on the candidate's rank (glowing for Top 10, balanced for Top 50, critical for lower-ranked fits).

#### Structural Data Validation
* **Honeypot Filter:** Excludes all **84 honeypot profiles** (startup date contradictions and zero-experience expert skills) and sets their score to `-9999.0` immediately.
* **Anti-Hallucination:** Eliminates generative hallucinations by extracting names, companies, and skills directly from variables.
* **Consulting Filter:** Excludes consulting-only candidates to prevent services-only profiles in the Top 100.

### Speaker Notes
> "On Slide 5, we cover explainability and validation. In a recruiting tool, recruiters must understand *why* a candidate was ranked highly. Our ranker dynamically generates natural, fact-based justifications for each candidate, adjusting the tone based on the candidate's rank. For validation, our script completely shields the Top 100 by screening out all 84 honeypots and consulting-only profiles."

---

## 🖥️ Slide 6: End-to-End Workflow

### Slide Title
**6. End-to-End Workflow**

### Slide Content

#### 6-Step Automated Ingestion Pipeline
1. **Load Pool:** Ingests candidate pool line-by-line using Python standard json. Prevents bulk RAM footprint.
2. **Sanitizer Filters:** Checks profiles against startup dates, consulting lists, and non-technical titles.
3. **Scoring Engine:** Calculates points for valid profiles (YoE, skills, location, notice, activity, and career).
4. **Decimator Rounding:** Rounds scores to 1 decimal place to align sorting keys with CSV output.
5. **Sort & Reasoning:** Sorts by score (descending) and candidate_id (ascending). Generates reasoning narratives.
6. **CSV Generation:** Writes formatted outputs (`candidate_id`, `rank`, `score`, `reasoning`) to `submission.csv`.

### Speaker Notes
> "On Slide 6, we walk through the End-to-End Workflow. The script streams the database, filters out traps, computes scores, rounds to 1 decimal place, sorts the candidates, breaks ties by candidate ID ascending, and outputs the top 100 to the final CSV file. The process is completely automated and takes only 3.4 seconds to process 100,000 resumes."

---

## 🖥️ Slide 7: System Architecture

### Slide Title
**7. System Architecture**

### Slide Content

```
   [ JSONL Candidate Stream ]
               │
               ▼
   [ Sanitizer Gateway Filter ]  ──> (Traps: Startup Dates, Skill Durations, Consulting-Only)
               │
               ▼  (Valid Profiles)
   [ Scoring Engine (Heuristics) ] ──> (YoE, Log-Scaled Skills, Location, Notice, Signals)
               │
               ▼
   [ Rounding & Sorting ]        ──> (Rounded to 1 decimal place; Sorted by score, candidate_id)
               │
               ▼
   [ Top 100 Reasoning Generator]
               │
               ▼
      [ submission.csv ]
```

### Speaker Notes
> "Slide 7 shows our visual System Architecture. Candidates are ingested, filtered through strict gates, scored via our heuristics engine, rounded, sorted, and dynamically narrated. The sanitizer acts as a secure shield, protecting our top 100 rankings from keyword-stuffer traps and honeypots."

---

## 🖥️ Slide 8: Results & Performance

### Slide Title
**8. Results & Performance**

### Slide Content

#### Top Candidate Results (Top 3)
* **Rank 1:** `CAND_0061257` (Advaith Pillai) — Staff ML Engineer @ LinkedIn. Noida. **Score: 122.0**.
  * *Reasoning:* Exceptional Staff ML Engineer with 8.0 YoE. Deep expertise in PEFT, Machine Learning, search. Noida-based, 30d notice.
* **Rank 2:** `CAND_0018499` (Aarav Trivedi) — Senior ML Engineer @ Zomato. Noida. **Score: 120.0**.
  * *Reasoning:* Senior ML Engineer with 7.2 YoE. Expertise in Weaviate, Pinecone. Noida-based, 15d notice.
* **Rank 3:** `CAND_0052328` (Vikram Banerjee) — Recommendation Systems @ Amazon. Pune. **Score: 120.0**.
  * *Reasoning:* Recommendation Systems Engineer with 6.5 YoE. Expertise in LoRA, OpenSearch. Pune-based, 30d notice.

#### Compute Performance
* **Execution Time:** **3.4 seconds** (Constraint limit: 5 minutes).
* **Memory Footprint:** **~60 MB RAM** (Constraint limit: 16 GB).
* **Honeypot Rate:** **0%** in Top 100. Verification suite successfully passed.

### Speaker Notes
> "Slide 8 highlights our performance and candidate results. Advaith Pillai, a Staff ML Engineer at LinkedIn based in Noida, took the number 1 rank. In terms of performance, the code ran in 3.4 seconds—over 80 times faster than the challenge limit—and consumed only 60MB of RAM. The honeypot rate is exactly 0%, validating our filters."

---

## 🖥️ Slide 9: Technologies Used

### Slide Title
**9. Technologies Used**

### Slide Content
Our system is built on a lightweight, dependency-free python-native stack, maximizing porting speed:

* **Python 3.11+:** Selected as the primary language for developer speed, dictionary processing, and standard library robustness.
* **Python Standard Library:**
  * `json` (for high-speed candidate streaming ingestion).
  * `argparse` (for clean command-line configurations).
  * `datetime` (for calculating activity timelines).
  * `csv` (for compliant spreadsheet outputs).
* **ReportLab 4.0:** Used to programmatically render presentation PDFs and slides directly from code.
* **Git & GitHub CLI:** Selected for version control, repository sharing, and automation of commits/pushes.

### Speaker Notes
> "On Slide 9, we explain the choice of technologies. We purposefully avoided deep learning packages and heavyweight frameworks. Python's standard library is more than capable of processing dictionary transformations at high speeds. By using native json and csv libraries, we guarantee zero compile errors, zero package conflicts, and near-instant runtime speeds in the sandbox environment."

---

## 🖥️ Slide 10: Submission Assets

### Slide Title
**10. Submission Assets**

### Slide Content

* **GitHub Repository:** The complete codebase, metadata templates, slide generator, and documentation:
  * URL: <font color="blue"><u>https://github.com/BharathKumarpallem/India_runs_data_and_ai_challenge</u></font>
* **Hosted Sandbox Link:** An active Streamlit/Colab environment demonstrating small-sample ranking:
  * URL: <font color="blue"><u>https://huggingface.co/spaces/bharathkumarpallem/redrob-ranker</u></font>
* **Submission CSV:** Located at the repository root as `submission.csv` containing the Top 100 candidates.
* **Presentation Slides PDF:** Located at the root as `presentation.pdf`.
* **Honeypot Analysis Report:** Detailed written report at `analysis_results.md` listing the 84 trapped profiles.

### Speaker Notes
> "Slide 10 details our submission assets. Our GitHub repository is public and live. It includes the required code files, the Streamlit hosted sandbox link, the validated submission CSV, this presentation PDF, and a separate report analyzing the 84 detected honeypots. All assets are formatted to the hackathon specification."

---

## 🖥️ Slide 11: Thank You

### Slide Title
**redrob | H2S — INDIA.RUNS**
*Build what next India runs on*

### Slide Content
**THANK YOU**

* **Presenter:** Bharath Kumar Pallem
* **Intelligent Candidate Discovery & Ranking System**
* **Code Repository:** `BharathKumarpallem/India_runs_data_and_ai_challenge`

### Speaker Notes
> "And with that, I conclude my presentation. Thank you for your time. I am now open to any questions you may have about the architecture, our scoring heuristics, or our honeypot filtering mechanism."

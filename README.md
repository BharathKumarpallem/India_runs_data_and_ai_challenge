# Intelligent Candidate Discovery & Ranking System (Team Antigravity)

This repository contains the AI candidate ranking system developed for the **Redrob Data & AI Challenge 2026**. 

Our program reads a list of 100,000 candidates from `candidates.jsonl`, filters out invalid/honeypot candidates, scores them against the **Senior AI Engineer — Founding Team** job description, and outputs the **Top 100 candidates** in a format-validated CSV.

---

## 🚀 Reproduction Quick Start

Ensure you have Python 3.10+ installed.

### 1. Install Dependencies
All scoring and filtering code runs entirely on the Python Standard Library. To build the optional presentation PDF, you'll need the `reportlab` library:
```bash
pip install -r requirements.txt
```

### 2. Run the Candidate Ranker
Execute the ranker by pointing to the candidate pool JSONL file. The ranking process is highly optimized and completes in **under 5 seconds**:
```bash
python rank.py --candidates ./candidates.jsonl --out ./submission.csv
```

### 3. Validate the Output CSV
Confirm that the generated CSV complies with the format validation checks:
```bash
python validate_submission.py submission.csv
```

---

## 🛠️ System Architecture & Methodology

Our pipeline is structured into a multi-stage process designed to balance execution speed, accuracy, and defense against data noise.

```
Ingestion (Streamed JSONL) -> Strict Filters (Honeypot + Relevancy) -> Calibrated Scoring -> Deterministic Sorting -> Narrative Reasoning -> CSV Output
```

### 1. Strict Filters (Honeypots & Traps Excluded)
To safeguard search quality and naturally ignore deceptive profiles:
* **Honeypot Profiles (0% rate in Top 100)**: We programmatically isolate all 84 honeypots by checking for:
  - *Startup Founding Contradictions:* Candidates claiming to work at Indian AI startups (e.g., Krutrim, Sarvam AI, Rephrase.ai, Genpact AI) years before they were officially founded.
  - *Expert Skill Duration Mismatch:* Candidates claiming 5+ "expert" level skills with exactly `0` months of experience.
* **Consulting/Services-Only Filter:** Candidates who have only worked at consulting/services firms (TCS, Infosys, Wipro, Capgemini, Accenture, Cognizant, Tech Mahindra, Mindtree, Mphasis, HCL) in their entire career are disqualified, matching the JD's requirement for product engineering background.
* **Relevancy Filter:** Candidates whose titles and career histories are completely non-technical (e.g. "Marketing Manager") but contain stuffed AI keywords are disqualified.

### 2. Calibrated Scoring (Max 115 Points)
Valid profiles are scored based on six dimensions matching the JD's ranking criteria:
1. **Years of Experience (YoE) Match (Max 15 pts):** Peak score (15 pts) for 6–8 years of experience, with tapered points for 5–9 years.
2. **AI/ML Skills Match (Max 45 pts):** Match score is a function of weight, proficiency, and duration.
   - *High-Weight (3.0):* RAG, Retrieval, Vector DBs (Pinecone, Weaviate, Qdrant), Embeddings.
   - *Medium-Weight (2.0):* Python, Fine-tuning (LoRA, QLoRA, PEFT), PyTorch, NLP, eval metrics (NDCG, MAP).
   - *Proficiency Multiplier:* expert (1.0) to beginner (0.2).
   - *Duration Multiplier:* log-scaled and capped at 3 years.
3. **Location Alignment (Max 10 pts):** Noida/Pune (+10 pts), welcome cities (Delhi/NCR/Mumbai/Hyd) (+5 pts), other Indian cities (+2 pts), and relocation penalty for candidates outside India (-20 pts).
4. **Notice Period (Max 10 pts):** Short notice <= 30 days (+10 pts), penalizing notices > 90 days (-10 pts).
5. **Career History Match (Max 15 pts):** Highlights candidates with >= 75% product company experience (+10 pts) and penalizes job hoppers with average tenure < 18 months (-8 pts). Gives current AI/ML titles (+10 pts) priority.
6. **Active Platform Signals (Max 20 pts):** Penalizes inactive profiles (no login for 6 months) and low recruiter response rates. Rewards active profiles (Open-to-Work flags, strong GitHub scores).

### 3. Deterministic Sorting & Tie-breaking
Ranks are sorted by `score` in descending order. If two candidates share the same score, the system enforces a strict tie-breaker sorting by `candidate_id` ascending lexicographically (e.g. `CAND_0000001` before `CAND_0000002`).

---

## 📂 Repository Contents
* `rank.py`: The main ranking execution script.
* `generate_pdf.py`: PDF presentation slide deck generator.
* `submission_metadata.yaml`: Required team portal metadata.
* `requirements.txt`: Project dependencies.
* `submission.csv`: Generated Top 100 ranked candidates file.
* `presentation.pdf`: The final PDF presentation slide deck.

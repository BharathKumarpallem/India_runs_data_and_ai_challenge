# INDIA RUNS Hackathon - Presentation Slide Deck Content

This document contains copy-pasteable content for each slide of the **Intelligent Candidate Discovery & Ranking System** presentation. Each slide includes the title, visual layout/elements, slide body text, and comprehensive speaker notes.

---

## 🖥️ Slide 1: Cover Page

### Slide Title
**AI-Native Candidate Discovery & Ranking System**

### Subtitle
*Recruiting at Scale for the Senior AI Engineer (Founding Team) Role*

### Slide Content (Key Details)
* **Prepared by:** Bharath Kumar Pallem
* **Challenge:** Redrob Data & AI Challenge 2026
* **Core Approach:** Multi-stage Filtering + Calibrated Offline Heuristics
* **Performance Benchmark:** <10 Seconds Execution Time on standard CPU

### Speaker Notes
> "Hello everyone, I am Bharath Kumar Pallem. Today I am presenting my AI-Native Candidate Discovery and Ranking System, built for the Redrob Data & AI Challenge. My objective is to solve the critical task of matching a highly specific, early-stage job description—the Senior AI Engineer for a founding team—with a pool of 100,000 candidates. My approach balances extremely strict filtration of data traps with a mathematical, calibrated heuristic scoring model that runs fully offline on CPU in under 4 seconds."

---

## 🖥️ Slide 2: Problem Statement & Constraints

### Slide Title
**1. Problem Statement & Constraints**

### Slide Content

#### Context
* **The Recruiting Dilemma:** Series A startup seeking a Founding AI Engineer. Needs deep ML/systems expertise (embeddings, retrieval, ranking, evaluation frameworks) coupled with a scrappy, shipping-focused product engineering mindset.
* **The Goal:** Programmatically ingest 100,000 resume profiles, remove invalid entries, score and rank candidates, and produce a validated Top 100 list.

#### Technical & Operational Constraints
| Compute Parameter | Hackathon Limit | Antigravity Performance |
| :--- | :--- | :--- |
| **Runtime Limit** | &le; 5 minutes (300 seconds) | **~3.5 seconds** (Fast, linear parsing) |
| **Memory Limit** | &le; 16 GB RAM | **~60 MB** (Streamed line-by-line parsing) |
| **Network Calls** | Off (No hosted APIs/OpenAI/Gemini) | **Fully Offline** (Zero external dependencies) |
| **Compute Type** | CPU Only — no GPU | **Single-threaded CPU** |

### Speaker Notes
> "Let's first define our constraints. A real-world talent intelligence system cannot afford to call expensive LLM APIs like GPT-4 for hundreds of thousands of candidates. It must be fast, cost-efficient, and reproducible. The challenge sets a strict 5-minute CPU-only limit with 16GB of RAM and no network. Our system exceeds these expectations: by streaming candidates line-by-line rather than loading the entire 487 MB database into RAM, we consume only 60 MB of memory and complete the entire filtering, scoring, sorting, and reasoning pipeline in just 3.5 seconds."

---

## 🖥️ Slide 3: Dataset Analysis & Trap Detection

### Slide Title
**2. Dataset Analysis & Trap Detection**

### Slide Content
Synthetic datasets contain intentional noise and traps to penalize naive keyword-matching or semantic models. Our system implements a strict, multi-stage filtration layer.

* **Honeypot Profiles (84 candidates detected - Excluded Entirely)**
  * *Startup Founding Contradictions:* 76 candidates claimed employment at modern AI startups years before the companies existed (e.g., working at Krutrim in 2019, but Krutrim was founded in 2023).
  * *Skill Durations:* 8 candidates claimed "expert" proficiency in 5+ skills with exactly 0 months of experience.
* **IT Consulting/Services-Only Trap (Excluded Entirely)**
  * The JD explicitly states a preference for product engineers. Candidates who have *only* worked at large services firms (TCS, Infosys, Wipro, Capgemini, Accenture, Cognizant, etc.) are filtered out.
* **Non-Tech Role Traps (Excluded Entirely)**
  * Identifies candidates who stuffed their resumes with AI keywords but hold current titles entirely unrelated to tech (e.g., "Marketing Manager", "Accountant").

### Visual Diagram Description
```
               [ Input: 100,000 Candidates ]
                             │
                             ▼
              [ Filter 1: Honeypot Checker ]  ──> (Excludes 84 fake profiles)
                             │
                             ▼
             [ Filter 2: Consulting-Only ]   ──> (Excludes consulting backgrounds)
                             │
                             ▼
             [ Filter 3: Tech Title Check ]  ──> (Excludes non-tech role traps)
                             │
                             ▼
              [ Ingested: Valid Candidates ]
```

### Speaker Notes
> "To perform well in this challenge, you must understand the data anomalies. The organizers placed 84 honeypot candidates in the pool. These represent 'subtly impossible' profiles: 76 candidates claim to have worked at Indian AI startups like Krutrim and Sarvam AI years before they were founded, and 8 candidates claim 'expert' status in numerous skills with 0 months of experience. A naive keyword ranker is attracted to these profiles, but our filter identifies these logical inconsistencies and filters them out. We also filter out candidates who have worked only at IT services firms, and candidates in non-technical roles with stuffed keywords."

---

## 🖥️ Slide 4: Multi-Stage Pipeline Architecture

### Slide Title
**3. Multi-Stage Pipeline Architecture**

### Slide Content

* **1. Ingest (Streamed JSONL)**
  * Reads the 487MB `candidates.jsonl` line-by-line using standard Python, preventing memory bloating.
* **2. Sanitizer (Strict Filtration)**
  * Passes candidate data through temporal, company, and title validator rules. If a trap is triggered, the candidate is assigned a score of `-9999.0` and bypassed.
* **3. Feature Scorer (Calibrated Heuristics)**
  * Calculates sub-scores for candidates who pass the sanitizer, using YoE, log-scaled skill durations, location alignment, notice periods, and platform engagement.
* **4. Sort & Format (Top 100 Extraction)**
  * Sorts candidates by score (descending) and candidate_id (ascending) to break ties. Custom-generates non-templated reasoning strings and outputs a valid CSV.

### Speaker Notes
> "This slide outlines our pipeline architecture. It is built as a single-pass streaming pipeline. First, candidates are read line-by-line. Second, they pass through our Anomaly Sanitizer, which instantly flags honeypots or disqualified backgrounds. Third, valid candidates are scored across multiple dimensions. Finally, we sort the candidate pool, resolving ties by candidate_id ascending, and write the Top 100 rows to the final CSV. By keeping the pipeline linear and local, we ensure maximum execution reliability."

---

## 🖥️ Slide 5: Feature Engineering & Scoring Rules

### Slide Title
**4. Feature Engineering & Scoring Rules**

### Slide Content
Valid candidates are scored out of **115 maximum points** based on the following rules:

* **Experience Match (Max 15 pts):** Peak score (15 pts) for 6–8 years of experience (fits founding engineer target), 12 pts for 5-9 years, and 0 pts for outside ranges.
* **Skills Relevance (Max 45 pts):** Weighted based on JD priority:
  * *High Weight (3.0):* RAG, Retrieval, Vector DBs (Pinecone, Weaviate, Qdrant), Embeddings.
  * *Medium Weight (2.0):* Python, Fine-tuning (LoRA, QLoRA, PEFT), PyTorch, NLP, NDCG/MAP metrics.
  * *Formula:* Skill Score = `Weight * Proficiency Multiplier (expert=1.0, beginner=0.2) * Log Duration Multiplier (log-scaled, capped at 3 years) * 5.0`.
* **Location Alignment (Max 10 pts):** Noida/Pune (+10 pts), welcome cities (Delhi/NCR/Mumbai/Hyd) (+5 pts), outside India (-20 pts).
* **Notice Period (Max 10 pts):** <= 30 days (+10 pts), <= 60 days (+5 pts), > 90 days (-10 pts).
* **Platform Engagement (Max 20 pts):** Active within 30 days (+5 pts), inactive > 6 months (-15 pts), response rate >= 80% (+10 pts), Open-to-Work (+5 pts), GitHub score >= 60 (+5 pts), poor interview attendance (-10 pts).
* **Career Relevance (Max 15 pts):** Product company ratio >= 75% (+10 pts), job hopping penalty (-8 pts), current AI/ML title match (+10 pts).

### Speaker Notes
> "Our scoring algorithm is calibrated around six key features. The core of this is our Skills Scorer. We assign weights to skills, then scale by proficiency and duration of experience. For instance, rather than adding a flat score for 'Pinecone', we reward candidates who have used it for a longer duration on a log scale, up to a 3-year cap, and scale it based on their proficiency. Location and notice periods are also critical operational signals: Noida and Pune get a 10-point bonus, while notice periods over 90 days are penalized. Active behavioral signals, such as recruiter response rate and recent login history, are scored to ensure we don't rank passive or unavailable candidates."

---

## 🖥️ Slide 6: Results & Top Candidates Profile

### Slide Title
**5. Results & Top Candidates Profile**

### Slide Content

#### Top 5 Candidates in Output (Out of 100,000 Scanned)
| Rank | Candidate ID | Name | Current Title & Company | YoE | Location | Score |
| :--- | :--- | :--- | :--- | :---: | :--- | :---: |
| **1** | CAND_0061257 | Advaith Pillai | Staff ML Engineer @ LinkedIn | 8.0 | Noida (Preferred) | **122.0** |
| **2** | CAND_0018499 | Aarav Trivedi | Senior ML Engineer @ Zomato | 7.2 | Noida (Preferred) | **120.0** |
| **3** | CAND_0052328 | Vikram Banerjee | Recommendation Systems @ Amazon | 6.5 | Pune (Preferred) | **120.0** |
| **4** | CAND_0007009 | Anika Pillai | Recommendation Systems @ Wysa | 7.9 | Noida (Preferred) | **118.0** |
| **5** | CAND_0026942 | Sneha Nair | Junior ML Engineer @ Verloop.io | 6.0 | Chandigarh (India) | **117.0** |

#### Key Validation Milestones
* **Honeypot Rate:** Exactly **0%** in the Top 100.
* **Reasoning Quality:** Clean, custom narratives detailing specific candidate skills (e.g., PEFT, LoRA, Weaviate), YoE, current employer, and notice periods. **Zero templates used.**
* **Tie-Breaking:** Fully validated by the official test suite for sorting ties alphabetically by `candidate_id` ascending.

### Speaker Notes
> "Let's review the results. Our top rank goes to Advaith Pillai, a Staff ML Engineer at LinkedIn with 8.0 years of experience, based in Noida, with expertise in PEFT, Machine Learning, and search, and a 30-day notice period. He scores 122 points out of our maximum. Zomato and Amazon ML engineers follow closely. Our validator run confirmed that our honeypot rate in the Top 100 is exactly 0%, and the generated reasoning strings are specific, factually grounded, and avoid standard templating. The validator script verified our tie-breaker sorting and returned a fully valid status."

---

## 🖥️ Slide 7: Production Scale & Future Enhancements

### Slide Title
**6. Production Scale & Future Enhancements**

### Slide Content
To scale this candidate ranking system to a production talent intelligence platform, we recommend:

1. **Hybrid Retrieval (Dense + Sparse)**
   * Deploy an Elasticsearch/OpenSearch cluster combining BM25 keyword matching with dense vector embeddings (e.g. BGE-M3 or E5-v2) to capture semantic and exact matches.
2. **Two-Pass Ranking Architecture**
   * *Pass 1:* Use a fast Bi-Encoder to retrieve the top 500 candidates from 100k+ in under 1 second.
   * *Pass 2:* Apply a deep local Cross-Encoder re-ranker on CPU to score the top 500, preserving latency constraints while maximizing NDCG.
3. **Learning-to-Rank (LTR)**
   * Train an XGBoost model (using `LambdaMART`) on historical click, message, and interview conversion data to automatically optimize feature weights rather than relying on manually tuned heuristics.
4. **Real-time Indexing & Drift Management**
   * Use Kafka and Qdrant/Pinecone to update candidate embeddings in real-time when candidates edit their profiles, ensuring indices stay current.

### Speaker Notes
> "Finally, how do we take this from a hackathon model to a production system? We propose a two-pass ranking architecture. First, a fast Bi-Encoder or hybrid dense-sparse index narrows down the candidate pool from 100,000 to the top 500. This handles the scale in less than a second. Second, a deep local Cross-Encoder model runs on CPU to perform high-precision re-ranking on the top 500. We also suggest replacing manually tuned heuristics with a machine-learned Learning-to-Rank model like XGBoost, trained on historical recruiter engagement data. This ensures the system continuously learns and optimizes matching accuracy. Thank you."

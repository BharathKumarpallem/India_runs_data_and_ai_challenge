# Detailed Analysis of Anomalous & Honeypot Candidate Profiles

This document provides an in-depth analysis of the **84 honeypot candidates** embedded in the Redrob candidate dataset of 100,000 profiles. These anomalous profiles represent synthetic traps engineered to catch ranking algorithms that rely solely on keyword matching or naive vector similarity without verifying the temporal and logical integrity of the resume details.

## Summary of Findings

Through structural audit scripts, we identified **84 candidates** with impossible resume configurations. In the ground-truth relevance labeling, these candidates are forced to **Relevance Tier 0** (completely irrelevant). Ranking any of these candidates in the Top 100 results in score penalties and eventual disqualification.

### High-Level Statistics
- **Total Candidate Pool Scanned:** 100,000
- **Total Detected Honeypots:** 84 (0.084%)
  - *Startup Founding Date Violations:* 76 candidates
  - *Fake Expert Skill Mismatches:* 8 candidates

### Startup Founding Contradictions by Company
| Company Name | Official Founding Year | Number of Honeypot Contradictions |
| :--- | :---: | :---: |
| Krutrim | 2023 | 38 |
| Sarvam AI | 2023 | 36 |
| Rephrase.ai | 2019 | 2 |
| Genpact AI | 2019 | 1 |

## Honeypot Typology & Mechanisms

### 1. Startup Founding Date Contradictions (76 Candidates)
> [!WARNING]
> **Mechanism:** The candidate's `career_history` claims employment start years that strictly precede the founding year of the company. These are often highly relevant AI-native startups, designed to look extremely attractive to a naive ranking model.

* **Why it traps naive algorithms:** A semantic search or keyword ranking model sees that a candidate has worked as an 'AI Engineer' or 'Search Engineer' at a well-known AI startup (e.g. `Sarvam AI` or `Krutrim`), scoring them highly. However, a temporal check reveals the startup didn't exist when the candidate claims to have worked there, indicating a fabricated profile.

### 2. Fake Expert Skills Mismatches (8 Candidates)
> [!CAUTION]
> **Mechanism:** The candidate's `skills` array contains 5 or more technical skills marked with `proficiency: 'expert'` but with `duration_months: 0` (exactly zero).

* **Why it traps naive algorithms:** Keyword rankers count matches for high-value skills like `Milvus`, `Docker`, or `Speech Recognition` and add bonus points for 'expert' proficiency. But a logical audit shows that a candidate claiming to be an 'expert' with 0 months of experience is a synthetic keyword stuffer.

## Audit Log: Sample Honeypot Profiles
Below is a selected audit log showing some of the flagged honeypot profiles, their claimed experience, and the exact logical contradictions detected:

| Candidate ID | Name | Claims | Detected Contradiction |
| :--- | :--- | :--- | :--- |
| CAND_0016000 | Aarav Bansal | <b>Title:</b> Full Stack Developer<br/><b>Company:</b> Initech<br/><b>YoE:</b> 2.0 | Claimed <b>'expert'</b> status in 5+ skills with 0 months of experience: TypeScript, Go, Docker, Hadoop, Photoshop |
| CAND_0046649 | Anil Kumar | <b>Title:</b> Business Analyst<br/><b>Company:</b> Wipro<br/><b>YoE:</b> 3.8 | Claimed <b>'expert'</b> status in 5+ skills with 0 months of experience: SAP, Node.js, gRPC, Flask, Hadoop |
| CAND_0056983 | Arnav Mittal | <b>Title:</b> Accountant<br/><b>Company:</b> Pied Piper<br/><b>YoE:</b> 12.3 | Claimed <b>'expert'</b> status in 5+ skills with 0 months of experience: Rust, Next.js, Redis, Salesforce CRM, MongoDB |
| CAND_0060642 | Neha Krishnan | <b>Title:</b> Frontend Engineer<br/><b>Company:</b> Cognizant<br/><b>YoE:</b> 3.0 | Claimed <b>'expert'</b> status in 5+ skills with 0 months of experience: Milvus, Agile, Azure, Diffusion Models, MongoDB |
| CAND_0061722 | Arjun Trivedi | <b>Title:</b> Software Engineer<br/><b>Company:</b> Wipro<br/><b>YoE:</b> 6.8 | Claimed <b>'expert'</b> status in 5+ skills with 0 months of experience: Terraform, GANs, Milvus, MongoDB, Speech Recognition |
| CAND_0063888 | Divya Mittal | <b>Title:</b> .NET Developer<br/><b>Company:</b> Hooli<br/><b>YoE:</b> 2.4 | Claimed <b>'expert'</b> status in 5+ skills with 0 months of experience: Project Management, Accounting, MLOps, React, Webpack |
| CAND_0070429 | Amit Singh | <b>Title:</b> Software Engineer<br/><b>Company:</b> Swiggy<br/><b>YoE:</b> 8.1 | Claimed <b>'expert'</b> status in 5+ skills with 0 months of experience: MLOps, Figma, Accounting, YOLO, Java |
| CAND_0073853 | Arnav Pillai | <b>Title:</b> Operations Manager<br/><b>Company:</b> Globex Inc<br/><b>YoE:</b> 8.0 | Claimed <b>'expert'</b> status in 5+ skills with 0 months of experience: CI/CD, Marketing, GCP, Excel, AWS |
| CAND_0088025 | Amit Arora | <b>Title:</b> Staff Machine Learning Engineer<br/><b>Company:</b> Yellow.ai<br/><b>YoE:</b> 8.6 | Claimed start date at <b>Genpact AI</b>: 2017-12-10 (Company was founded in 2019) |
| CAND_0003599 | Anil Sethi | <b>Title:</b> Computer Vision Engineer<br/><b>Company:</b> Krutrim<br/><b>YoE:</b> 6.5 | Claimed start date at <b>Krutrim</b>: 2022-04-18 (Company was founded in 2023) |
| CAND_0004112 | Priya Kumar | <b>Title:</b> Senior Software Engineer (ML)<br/><b>Company:</b> Zoho<br/><b>YoE:</b> 6.5 | Claimed start date at <b>Krutrim</b>: 2019-12-30 (Company was founded in 2023) |
| CAND_0011327 | Pranav Krishnan | <b>Title:</b> AI Research Engineer<br/><b>Company:</b> Krutrim<br/><b>YoE:</b> 6.3 | Claimed start date at <b>Krutrim</b>: 2022-10-15 (Company was founded in 2023) |
| CAND_0011432 | Deepak Trivedi | <b>Title:</b> Senior Data Scientist<br/><b>Company:</b> Amazon<br/><b>YoE:</b> 7.6 | Claimed start date at <b>Krutrim</b>: 2020-12-24 (Company was founded in 2023) |
| CAND_0011687 | Shreya Tiwari | <b>Title:</b> Senior NLP Engineer<br/><b>Company:</b> Niramai<br/><b>YoE:</b> 7.8 | Claimed start date at <b>Krutrim</b>: 2018-11-05 (Company was founded in 2023) |
| CAND_0011707 | Suresh Bhatia | <b>Title:</b> Data Scientist<br/><b>Company:</b> HCL<br/><b>YoE:</b> 4.8 | Claimed start date at <b>Krutrim</b>: 2021-09-20 (Company was founded in 2023) |
| CAND_0015097 | Om Trivedi | <b>Title:</b> Senior Software Engineer (ML)<br/><b>Company:</b> Zoho<br/><b>YoE:</b> 6.0 | Claimed start date at <b>Krutrim</b>: 2020-06-27 (Company was founded in 2023) |
| CAND_0015528 | Aisha Reddy | <b>Title:</b> Applied ML Engineer<br/><b>Company:</b> Krutrim<br/><b>YoE:</b> 7.4 | Claimed start date at <b>Krutrim</b>: 2022-02-17 (Company was founded in 2023) |
| CAND_0016170 | Aditya Reddy | <b>Title:</b> AI Research Engineer<br/><b>Company:</b> Dream11<br/><b>YoE:</b> 6.8 | Claimed start date at <b>Krutrim</b>: 2020-04-14 (Company was founded in 2023) |
| CAND_0018701 | Advik Khanna | <b>Title:</b> Junior ML Engineer<br/><b>Company:</b> Krutrim<br/><b>YoE:</b> 6.0 | Claimed start date at <b>Krutrim</b>: 2022-11-14 (Company was founded in 2023) |
| CAND_0019159 | Vikram Nair | <b>Title:</b> ML Engineer<br/><b>Company:</b> Genpact AI<br/><b>YoE:</b> 6.1 | Claimed start date at <b>Krutrim</b>: 2020-04-28 (Company was founded in 2023) |
| CAND_0021410 | Ela Vora | <b>Title:</b> Junior ML Engineer<br/><b>Company:</b> Krutrim<br/><b>YoE:</b> 4.0 | Claimed start date at <b>Krutrim</b>: 2022-12-14 (Company was founded in 2023)<br/>Claimed start date at <b>Sarvam AI</b>: 2022-06-10 (Company was founded in 2023) |
| CAND_0022232 | Vihaan Krishnan | <b>Title:</b> Senior Software Engineer (ML)<br/><b>Company:</b> Zomato<br/><b>YoE:</b> 3.9 | Claimed start date at <b>Krutrim</b>: 2022-08-16 (Company was founded in 2023) |
| CAND_0024878 | Aanya Shetty | <b>Title:</b> AI Specialist<br/><b>Company:</b> HCL<br/><b>YoE:</b> 5.7 | Claimed start date at <b>Krutrim</b>: 2020-10-25 (Company was founded in 2023) |
| CAND_0025923 | Tanya Chatterjee | <b>Title:</b> Senior Software Engineer (ML)<br/><b>Company:</b> HCL<br/><b>YoE:</b> 5.0 | Claimed start date at <b>Krutrim</b>: 2021-07-22 (Company was founded in 2023) |
| CAND_0031068 | Siya Dutta | <b>Title:</b> AI Specialist<br/><b>Company:</b> Sarvam AI<br/><b>YoE:</b> 4.5 | Claimed start date at <b>Krutrim</b>: 2022-01-18 (Company was founded in 2023) |
| CAND_0033842 | Neha Goyal | <b>Title:</b> Senior Software Engineer (ML)<br/><b>Company:</b> Rephrase.ai<br/><b>YoE:</b> 5.8 | Claimed start date at <b>Krutrim</b>: 2020-09-18 (Company was founded in 2023) |
| CAND_0035779 | Sneha Desai | <b>Title:</b> ML Engineer<br/><b>Company:</b> Swiggy<br/><b>YoE:</b> 5.5 | Claimed start date at <b>Krutrim</b>: 2021-12-19 (Company was founded in 2023) |
| CAND_0036973 | Sunil Rao | <b>Title:</b> AI Research Engineer<br/><b>Company:</b> Rephrase.ai<br/><b>YoE:</b> 6.2 | Claimed start date at <b>Krutrim</b>: 2020-05-28 (Company was founded in 2023) |
| CAND_0051615 | Pooja Banerjee | <b>Title:</b> Search Engineer<br/><b>Company:</b> Meta<br/><b>YoE:</b> 4.6 | Claimed start date at <b>Krutrim</b>: 2021-11-19 (Company was founded in 2023) |
| CAND_0058517 | Yash Saxena | <b>Title:</b> Computer Vision Engineer<br/><b>Company:</b> Freshworks<br/><b>YoE:</b> 5.1 | Claimed start date at <b>Krutrim</b>: 2021-04-23 (Company was founded in 2023) |

## Defensive Action Implemented in `rank.py`
Our production ranking script implements an **Anomaly Sanitizer** that checks every candidate against these two patterns before applying any scoring weights. Flagged candidates are instantly assigned a score of `-9999.0`, pushing them to the bottom of the list and guaranteeing **0% honeypots** in our Top 100 ranking. This was verified by the official validation suite.
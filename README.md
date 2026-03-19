# Fiduciary Vault 🏛️
### India's First Deterministic Multi-Agent Wealth Management System

> Built for the Indian middle class (₹50L–₹5Cr net worth) who deserve CA-grade financial advice without CA-grade fees.

---

## The Problem

A 35-year-old salaried Indian with ₹80L in savings has no one to trust with his money.
- Human CA: ₹5,000–₹10,000 per session. Unaffordable monthly.
- Generic AI (ChatGPT): Gives confident advice with hallucinated numbers. Dangerous.
- Robo-advisors: Suggest products. Never protect. Never block bad decisions.

**His salary disappears every month. He invests based on FOMO. He has no retirement plan.**

---

## The Solution

A 7-agent LangGraph system where each agent is a domain specialist with a real persona, real tools, and mathematically guaranteed correct numbers.

**Core Rule: LLMs are strictly forbidden from performing math.**
Every number comes from deterministic Python calculators. LLMs only reason and communicate.

---

## Architecture
```
User Data (CAS PDF + Bank Statement)
        ↓
Ingestion Agent (casparser + CASParser API)
        ↓
Fiduciary Agent — CA Ramesh Iyer (gatekeeper, calculates truth)
        ↓
Supervisor (routes query to relevant specialists)
        ↓
[Sequential Specialist Agents with memo passing]
├── Debt Agent — Arjun Kapoor
├── Tax Agent — CA Priya Sharma  
├── Insurance Agent — Vikram Singh
├── Retirement Agent — Sunita Krishnan
└── SIP Agent — Priya Mehta
        ↓
Synthesizer (unified financial plan)
```

---

## Why This Beats Generic AI

| Feature | ChatGPT | Fiduciary Vault |
|---------|---------|-----------------|
| Math accuracy | Hallucinated | Deterministic Python |
| Data source | Your description | Real CAS PDF + Bank data |
| Financial decisions | Suggests | Blocks harmful ones |
| Indian context | Generic | SEBI, IRDAI, RBI specific |
| Accountability | Zero | Fiduciary grade |
| Cost | ₹1,700/month | ₹299/month (planned) |

---

## Tech Stack

- **LangGraph** — State machine orchestration
- **Anthropic Claude** — ReAct agents with tool use
- **Pydantic** — Data validation throughout
- **casparser + CASParser API** — PDF ingestion
- **Tavily** — Domain-restricted search (SEBI, IRDAI, RBI, incometax.gov.in)
- **FastAPI** — Backend API (Week 4)
- **PostgreSQL** — Long term memory (Month 2)

---

## Build Journey

| Phase | Status | What was built |
|-------|--------|----------------|
| Week 1 | ✅ Done | Schemas, calculators, LangGraph pipeline |
| Week 2 | ✅ Done | 7 agents, personas, report synthesizer |
| Week 3 | ✅ Done | ReAct loops, tool use, domain search, supervisor routing |
| Week 4 | 🔄 Building | FastAPI, conversation layer, short term memory |
| Month 2 | 📅 Planned | React frontend, PostgreSQL, long term memory |

---

## The Agents

| Agent | Persona | Tools |
|-------|---------|-------|
| Fiduciary | CA Ramesh Iyer — 25yr CA | surplus calculator, debt priority |
| Debt | Arjun Kapoor — Debt Specialist | avalanche calculator, RBI search |
| Tax | CA Priya Sharma — Tax CA | tax calculator, incometax.gov.in search |
| Insurance | Vikram Singh — IRDAI Consultant | gap calculator, IRDAI search |
| Retirement | Sunita Krishnan — CFP | corpus calculator, NPS search |
| SIP | Priya Mehta — MFD | SIP calculator, SEBI/AMFI search |

---

## Sample Output

> User: "Give me a complete financial analysis"
> 
> System runs 6 specialist agents sequentially, each reading previous findings.
> Synthesizer produces unified 3-phase plan: Immediate (30 days) → Short term (6 months) → Long term (5 years)

---

## What's Next

- [ ] FastAPI backend
- [ ] Conversation mode per specialist  
- [ ] Short term memory (session)
- [ ] Long term memory (PostgreSQL)
- [ ] React frontend
- [ ] Spend analysis agent
- [ ] Account Aggregator live integration
- [ ] SEBI RIA compliance layer

---

## Built By

**Nikhil** — B.Tech AI/ML Student, India  
Building India's first fiduciary-grade AI wealth system from scratch.

*Started: March 2026 | Status: Active Development*
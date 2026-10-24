# MasteryLoop — Adaptive Assessment & Learning Intelligence Platform

**Knowledge-Tracing-Driven Adaptive Assessment, Psychometrically-Validated AI Item Generation, and Learning Intelligence Platform**

---

## 1. Executive Summary

MasteryLoop is an educational measurement platform that models what each learner knows and uses that knowledge model to drive personalized learning.
- **Computerized Adaptive Testing (CAT)**: Uses a 2-Parameter Logistic (2PL) Item Response Theory (IRT) engine and Expected A Posteriori (EAP) ability estimation ($\hat\theta$) with Maximum Fisher Information selection to deliver precise ability measurement in $\ge 40\%$ fewer questions than fixed tests.
- **Interactive Coding Execution Sandbox**: Multi-layer isolated subprocess execution environment featuring AST static security screening (banning `os`, `sys`, `subprocess`, `eval`, `exec`, `open`), ephemeral sandboxing, secret-stripped environments, strict 2.0s execution timeouts, and memory-safe stdout truncation.
- **Psychometrically-Validated AI Item Factory**: AI questions drafted with RAG over curriculum content pass through strict automated quality checks (blind solver verification, distractor plausibility, reading-level scoring, deduplication), human-in-the-loop SME review, unscored pilot testing, and IRT statistical calibration before admission into the active bank.
- **Cognitive Retention & Spaced Repetition**: Implements Ebbinghaus exponential memory decay $R(t) = \exp(-t / S)$ and half-life stability modeling to dynamically predict forgetting risk and schedule reviews.
- **Socratic AI Tutor**: Multi-modal pedagogical coaching across 6 modes (*Teach from Basics*, *Hint*, *Debug Mental Model*, *Interview Prep*, *Quick Revision*, *Exam Mode*) and 3 languages (*English*, *Tamil*, *Tanglish*), with curriculum chunk citations.

---

## 2. Architecture & Tech Stack

```
   ┌─────────────────────────────────────────────────────────────┐
   │            MasteryLoop React 19 Frontend (Vite)             │
   │  Dashboard | Curriculum DAG | Adaptive CAT | Tutor | Review  │
   └──────────────────────────────┬──────────────────────────────┘
                                  │ HTTP / JSON
                                  ▼
   ┌─────────────────────────────────────────────────────────────┐
   │                  FastAPI Backend Gateway                     │
   │   Auth (JWT) | Sessions | Mastery | Items | Coding | Tutor   │
   └──────────┬───────────────────┬───────────────────┬──────────┘
              │                   │                   │
              ▼                   ▼                   ▼
    ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
    │  Psychocore IRT  │ │  Coding Sandbox  │ │  Agentic Tutor   │
    │  - 2PL Fisher    │ │  - AST Screening │ │  - RAG Grounding │
    │  - EAP Ability   │ │  - Ephemeral Sub │ │  - Socratic Modes│
    │  - BKT Tracing   │ │  - Timeout Cap   │ │  - Multi-lingual │
    └──────────────────┘ └──────────────────┘ └──────────────────┘
              │                   │                   │
              └───────────────────┼───────────────────┘
                                  │
                                  ▼
   ┌─────────────────────────────────────────────────────────────┐
   │                 Relational & Vector Storage                 │
   │  SQLite / PostgreSQL (Curriculum, Items, Sessions, Mastery)  │
   │  In-Memory / Qdrant Vector DB (Curriculum Knowledge Base)   │
   └─────────────────────────────────────────────────────────────┘
```

- **Backend**: Python 3.11, FastAPI, SQLAlchemy ORM, Pydantic, SQLite / PostgreSQL.
- **Frontend**: React 19, TypeScript, Vite, Tailwind CSS, Lucide Icons, Recharts.
- **Psychometrics**: Pure library `psychocore` implementing 2PL likelihood, Fisher Information, and EAP ability estimation.
- **Security**: Pre-execution AST NodeVisitor, secret-stripped subprocess execution, parameter sanitization ensuring answer keys and explanations are never leaked prior to response.

---

## 3. Quick Startup Guide

### Backend Server
```bash
# Navigate to backend directory
cd backend

# Install dependencies
pip install -r requirements.txt

# Run database migrations and launch FastAPI on port 8000
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```
*The database automatically seeds 11 placement domains, 54 curriculum skills with validated DAG prerequisite edges, the question bank, and Qdrant curriculum chunks on startup.*

### Frontend Application
```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Launch Vite development server on port 5173
npm run dev -- --host 127.0.0.1 --port 5173
```
*Open http://127.0.0.1:5173/ in your browser.*

---

## 4. Testing & Verification

### Running the Test Suite
```bash
# Run all 70 unit and integration tests
cd backend
python -m pytest

# Run the live server end-to-end integration test (requires backend & frontend running)
python tests/live_server_e2e_test.py
```

### Production Frontend Build
```bash
cd frontend
npm run build
```

---

## 5. API Reference

| Endpoint | Method | Description | Auth Required |
|---|---|---|---|
| `/health` | GET | Health probe and database connectivity | None |
| `/api/v1/auth/register` | POST | Register a learner or teacher account | None |
| `/api/v1/auth/login` | POST | Authenticate and obtain JWT Bearer token | None |
| `/api/v1/auth/me` | GET | Retrieve authenticated profile | Learner / Teacher |
| `/api/v1/curriculum/domains` | GET | List 11 placement domains and skill counts | None |
| `/api/v1/curriculum/skills/{id}/prerequisites` | GET | Direct and transitive prerequisite DAG chains | None |
| `/api/v1/sessions` | POST | Start adaptive (CAT) or diagnostic session | Learner |
| `/api/v1/sessions/{id}/respond` | POST | Submit answer, grade, update $\hat\theta$, fetch next item | Learner |
| `/api/v1/sessions/{id}/report` | GET | Complete psychometric diagnostic report | Learner |
| `/api/v1/coding/execute` | POST | Execute code against test cases in sandbox | Learner |
| `/api/v1/mastery/dashboard` | GET | Readiness radar, mastery percentage, next-best actions | Learner |
| `/api/v1/mastery/retention/due` | GET | Ebbinghaus forgetting-risk due review items | Learner |
| `/api/v1/mastery/retention/review` | POST | Record spaced repetition review event | Learner |
| `/api/v1/tutor/chat` | POST | Socratic AI tutor response with citations | Learner |
| `/api/v1/items/review-queue` | GET | Human-in-the-loop SME review queue | Teacher / Admin |
| `/api/v1/items/{id}/review` | POST | Approve, edit, or reject AI-drafted item | Teacher / Admin |
| `/api/v1/items/{id}/lineage` | GET | Psychometric lineage, screening & review audit | Teacher / Admin |

---

## 6. Project Credentials & Default Roles

- **Student User**: `e2e_student_autonomous@masteryloop.ai` / `Password123!` (or register via `/register`).
- **Teacher Reviewer**: Register with `role: "TEACHER"` to access `/teacher/review`.

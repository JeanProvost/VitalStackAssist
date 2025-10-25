# Supplement Optimizer Project Instructions

## Important: This Repository
**This repository (VitalStackAssist) is the Python AI Service - the "Calculator" component** that performs AI-powered supplement interaction analysis. It is a stateless service that receives supplement data from the .NET monolith, processes it using AI/ML models, and returns analysis results. It does NOT access the database directly.

## 1. Vision & Target User
- **Vision:** Empower users to make safe, data-driven decisions about their supplement protocols.
- **Target User:** "Optimizer Alex" – a data-driven individual managing a complex health and supplement regimen.

## 2. Overall Architecture & Technology Stack
- **Architectural Pattern:** "Monolith + 1"
- **Database:** A **single PostgreSQL database** (Amazon RDS).
- **Services:**
  1.  **.NET 9 Monolith (The "Brain"):** The primary backend API. It handles all business logic, user authentication, and data persistence.
  2.  **Python AI Service (The "Calculator"):** A small, separate API (e.g., FastAPI) for specialized AI/ML tasks.

## 3. Critical: Service Responsibilities & Data Flow
This is the most important concept for this project.

### 3.1. .NET Monolith (System of Record)
- This service is **stateful** and **OWNS 100% of the database**.
- It is solely responsible for all database operations (reading, writing, caching).
- It contains all database models (e.g., `Supplements`, `UserStack`, `UserJournal`, `SupplementInteractionCache`).
- It handles all core application logic: user management, stack management, logging, etc.
- It is responsible for all caching logic.

### 3.2. Python AI Service (Stateless Calculator)
- This service is **stateless**.
- It **MUST NOT** access the PostgreSQL database. It is a pure, "dumb" calculator.
- Its only job is to perform a complex calculation (like interaction analysis) on data it is *given* and return a result.
- **Data Models:** The "models" in this service (e.g., in `models.py`) are **API Data Contracts (DTOs)**, *not* database models. They just define the shape of the API's input (request) and output (response).

### 3.3. Core Data Flow (Interaction Check & Caching)
This flow is critical to understand:
1.  **Request:** The React frontend sends a request to the **.NET API** to check for interactions.
2.  **Cache Key:** The **.NET** service generates a canonical cache key (e.g., `"magnesium_vitamin d_zinc"`).
3.  **Cache Read:** The **.NET** service queries *its own* `supplement_interaction_cache` table in the PostgreSQL database.
4.  **Cache Hit:** If data is found, **.NET** returns the cached JSON blob to the user. The Python service is never called.
5.  **Cache Miss:**
    a. The **.NET** service sends a simple JSON list of supplement names (e.g., `{"supplements": ["Magnesium", "Vitamin D", "Zinc"]}`) to the **Python AI service's** `/generate-interactions` endpoint.
    b. The **Python** service receives the list, runs its AI logic, and returns a *single, stateless JSON report* (e.g., `{"summary": "...", "positive_interactions": [...], ...}`).
    c. The **.NET** service receives this JSON report.
    d. The **.NET** service **saves this JSON report** into its `supplement_interaction_cache` table.
    e. The **.NET** service returns the report to the user.

## 4. Key Functional Requirements
- **Supplement & Stack Management:**
  - Users can add supplements to "My Stack" (inventory).
  - Pre-populated database of common supplements; support for custom entries.
  - Specify dosage, brand, and form.
- **Smart Scheduling & Logging:**
  - Generate daily supplement schedule using best practices (e.g., Vitamin D with fatty meal).
  - One-tap logging of intake; view intake history.
- **Safety & Interaction Checker:**
  - Cross-reference new supplements with existing stack for interactions.
  - Display warnings for negative interactions and side effects. (This logic is powered by the Python service).
- **Biomarker & Blood Test Tracking (MVP):**
  - Manual entry of biomarker data (Vitamin D, B12, Iron, Magnesium).
  - Historical charting and overlay with supplement intake history.
- **User Journal:**
  - Daily journal for subjective feelings (energy, sleep, mood).

## 5. Non-Functional Requirements
- **Security & Privacy:**
  - Encrypt all user health data at rest and in transit.
  - Clear privacy policy: no selling/sharing of user data.
- **Performance:**
  - App loads and is interactive within 3 seconds on standard mobile.
  - Supplement interaction queries return in <2 seconds (this is why the cache is critical).
- **Data & Reliability:**
  - Use reputable sources for supplement info (NIH, Examine.com, peer-reviewed studies).
  - Cite sources where appropriate.

## 6. Out-of-Scope (v1.0)
- Barcode scanning for supplement input
- Automated PDF parsing of blood test results
- Advanced integrations (wearables)
- Built-in fasting timer

## 7. Example User Story
> As a health-conscious individual ("Optimizer Alex"), I want to use my own data (supplements, schedules, blood work) to make safe and effective decisions, so that I can feel fully in control of my long-term wellness journey.
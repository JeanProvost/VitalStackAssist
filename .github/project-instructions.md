# Supplement Optimizer Project Instructions

## Important: This Repository
**This repository (VitalStackAssist) is the Python AI Service - the "Insight Engine" component** that performs AI-powered supplement interaction analysis and correlation detection. It is a stateless service that receives supplement data and user context from the .NET monolith, processes it using AI/ML models, and returns actionable insights. It does NOT access the database directly.

## 1. Vision & Target User
- **Vision:** Empower users to make safe, data-driven decisions about their supplement protocols while building sustainable, positive health habits.
- **The Facilitator Model:** We act as the "Facilitator" (Nir Eyal). We use this product ourselves, and our goal is to help the user fulfill their own desire to be healthy using persuasive design (not dark patterns).
- **Target User:** "Optimizer Alex" – a data-driven individual managing a complex health and supplement regimen who craves validation that their effort is working.

## 2. Overall Architecture & Technology Stack
- **Architectural Pattern:** "Monolith + 1"
- **Database:** A **single PostgreSQL database** (Amazon RDS).
- **Services:**
  1.  **.NET 9 Monolith (The "Brain"):** The primary backend API. It handles all business logic, user authentication, data persistence, and the "Investment" phase (storing logs).
  2.  **Python AI Service (The "Insight Engine"):** A small, separate API (e.g., FastAPI) for specialized AI/ML tasks. It generates the "Variable Reward."

## 3. Critical: Service Responsibilities & Data Flow
This is the most important concept for this project.

### 3.1. .NET Monolith (System of Record)
- This service is **stateful** and **OWNS 100% of the database**.
- It is solely responsible for all database operations (reading, writing, caching).
- It contains all database models (e.g., `Supplements`, `UserStack`, `UserJournal`, `SupplementInteractionCache`).
- It handles the Trigger (Notifications), Action (Logging), and Investment (Journaling) phases.
- It is responsible for all caching logic.

### 3.2. Python AI Service (Stateless Insight Engine)
- This service is **stateless**.
- It **MUST NOT** access the PostgreSQL database. It is a pure, "dumb" calculation engine.
- Its job is to perform complex analysis on data it is given (supplements + user history) and return Insights and Scores.
- **Data Models:** The "models" in this service (e.g., in `models.py`) are **API Data Contracts (DTOs)**, *not* database models. They just define the shape of the API's input (request) and output (response).

### 3.3. Core Data Flow (The Hook Loop)
This flow is critical to enable the Variable Reward:
1.  **Request:** The React frontend sends a request to the **.NET API** (e.g., Dashboard load or Log Action).
2.  **Cache Key:** The **.NET** service generates a canonical cache key.
3.  **Cache Read:** The **.NET** service queries *its own* `supplement_interaction_cache` table in the PostgreSQL database.
4.  **Cache Hit:** If data is found, **.NET** returns the cached JSON blob.
5.  **Cache Miss (Calling the Insight Engine):**
   a. The **.NET** service packages a request containing:
     - `supplements`: List of current stack (e.g., `["Magnesium", "Zinc"]`).
     - `user_history`: Recent logs and journal entries (e.g., `"Took Magnesium at 9 PM"`, `"Rated Sleep 8/10"`).
   b. The **Python AI service** runs its logic to find clinical interactions AND behavioral correlations (The Variable Reward).
   c. The **Python** service returns a single, stateless JSON report containing interactions, insights (Variable Rewards), and `vitality_score` (Gamification).
   d. The **.NET** service saves this JSON report into its cache.
   e. The **.NET** service returns the report to the user.

## 4. Key Functional Requirements
- **Supplement & Stack Management:**
  - Users can add supplements to "My Stack" (inventory).
  - Pre-populated database of common supplements; support for custom entries.
  - Specify dosage, brand, and form.
- **Smart Scheduling & Logging (Trigger & Action):**
  - Generate daily supplement schedule using best practices.
  - Contextual Triggers: Notifications must provide context (e.g., "Take with fat for absorption") rather than just time.
  - Action: One-tap logging of intake to reduce friction and ensure the behavior is easier than thinking.
- **The Insight Engine (Variable Reward):**
  - Correlations: The Python service must analyze `user_history` to find patterns (e.g., "Sleep is +15% better when taking Magnesium").
  - Educational Rewards: If no data exists (Cold Start), provide "Did you know?" facts about the specific stack.
  - Vitality Score: Calculate a 0-100 score based on consistency and stack safety to satisfy the "Reward of the Self."
- **Biomarker & Blood Test Tracking (High Investment):**
  - Manual entry of biomarker data (Vitamin D, B12, Iron, Magnesium).
  - Historical charting and overlay with supplement intake history.
- **User Journal (Investment):**
  - Replaces standard journaling with Micro-Interactions (sliders, single-tap mood checks).
  - This data is fed back into the Insight Engine to generate future rewards.

## 5. Non-Functional Requirements
- **Security & Privacy:**
  - Encrypt all user health data at rest and in transit.
  - Clear privacy policy: no selling/sharing of user data.
- **Performance:**
  - App loads and is interactive within 3 seconds on standard mobile.
  - Insight Generation: Queries must return in <2 seconds to ensure the "Reward" feels immediate.
- **Data & Reliability:**
  - Use reputable sources for supplement info (NIH, Examine.com, peer-reviewed studies).
  - Cite sources where appropriate.

## 6. Out-of-Scope (v1.0)
- Barcode scanning for supplement input
- Automated PDF parsing of blood test results
- Advanced integrations (wearables)
- Built-in fasting timer

## 7. Example User Story
> As "Optimizer Alex," I receive a Trigger to take my morning stack. I perform the Action (one tap). I immediately receive a Variable Reward (A "Daily Insight" telling me my sleep quality has improved 10% since starting Zinc). This motivates me to make an Investment (rating my energy level right now), which improves the tailored insights I'll get tomorrow.
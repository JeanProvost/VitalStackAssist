# Supplement Optimizer Project Instructions

## Vision & Target User
- **Vision:** Empower users to make safe, data-driven decisions about their supplement protocols.
- **Target User:** "Optimizer Alex" – a data-driven individual managing a complex health and supplement regimen.

## Key Functional Requirements
- **Supplement & Stack Management:**
  - Users can add supplements to "My Stack" (inventory).
  - Pre-populated database of common supplements; support for custom entries.
  - Specify dosage, brand, and form.
- **Smart Scheduling & Logging:**
  - Generate daily supplement schedule using best practices (e.g., Vitamin D with fatty meal).
  - One-tap logging of intake; view intake history.
- **Safety & Interaction Checker:**
  - Cross-reference new supplements with existing stack for interactions.
  - Display warnings for negative interactions and side effects.
- **Biomarker & Blood Test Tracking (MVP):**
  - Manual entry of biomarker data (Vitamin D, B12, Iron, Magnesium).
  - Historical charting and overlay with supplement intake history.
- **User Journal:**
  - Daily journal for subjective feelings (energy, sleep, mood).

## Non-Functional Requirements
- **Security & Privacy:**
  - Encrypt all user health data at rest and in transit.
  - Clear privacy policy: no selling/sharing of user data.
- **Performance:**
  - App loads and is interactive within 3 seconds on standard mobile.
  - Supplement interaction queries return in <2 seconds.
- **Data & Reliability:**
  - Use reputable sources for supplement info (NIH, Examine.com, peer-reviewed studies).
  - Cite sources where appropriate.

## Out-of-Scope (v1.0)
- Barcode scanning for supplement input
- Automated PDF parsing of blood test results
- Advanced integrations (wearables)
- Built-in fasting timer

## Example User Story
> As a health-conscious individual ("Optimizer Alex"), I want to use my own data (supplements, schedules, blood work) to make safe and effective decisions, so that I can feel fully in control of my long-term wellness journey.

---

**Reference:** See `src/models/supplements/` for supplement data models and `src/core/` for business logic. Supplement interaction logic is likely in `src/services/`.

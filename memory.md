# Claude Memory

This file is the first thing to read at the start of any session. It contains persistent facts, file locations and workflow instructions that apply across all tasks.

---

## Setup status

SETUP_COMPLETE: false

---

## First-run setup

If `SETUP_COMPLETE` is `false`, and the user sends a CV drafting request, pause before doing anything else and run the setup questionnaire below. Do not proceed with CV drafting until setup is complete or the user explicitly skips it.

Tell the user: *"Before I draft your first CV, I have a few quick setup questions so I can tailor this toolkit to you. You can skip any question you prefer not to answer."*

Ask the following questions one at a time, waiting for the user's answer before moving to the next. Make clear each one is optional before asking it.

1. **Your name and contact details** (name, location, phone, email) — used to pre-fill the contact line in every CV. Skip if you prefer to enter these manually for data protection reasons.
2. **Your field and role type** (e.g. software engineering, marketing, finance, product management) — used to tailor the focus areas Claude looks for when analysing job ads.
3. **The seniority level you are targeting** (e.g. mid-level, senior, lead, head of, director) — used to ensure the CV is pitched correctly.
4. **Any role-specific dimensions that matter in your field** (e.g. for product: B2B vs B2C, discovery vs delivery; for engineering: frontend vs backend, greenfield vs legacy) — used to sharpen job ad analysis. Leave blank if unsure and Claude will infer from job ads.
5. **Any quality checklist items specific to your field** that Claude should always verify before finalising a CV — leave blank if none.

Once the user has answered, do the following:

- If name and contact details were provided, note them under **Personal details** below.
- Update the **Role-specific configuration** section below with the answers to questions 2–5.
- Read the CV writing instructions file and insert the user's field-specific focus areas into Step 1, and any additional checklist items into Step 4.
- Update `SETUP_COMPLETE` to `true` in this file.

If the user skips all questions or asks to skip setup entirely, set `SETUP_COMPLETE` to `true` and proceed with the CV request, inferring context from the job ad as best you can.

---

## Personal details

NAME: [not provided]
CONTACT: [not provided]

---

## Role-specific configuration

FIELD: [not set]
TARGET_SENIORITY: [not set]
FOCUS_AREAS: [not set]
EXTRA_CHECKLIST_ITEMS: [none]

---

## Key files

| File | Purpose | Path |
|------|---------|------|
| Career history | Full work history, skills and certifications | `[PATH TO YOUR CAREER HISTORY FILE]` |
| CV writing instructions | Step-by-step instructions for drafting and refining CVs | `[PATH TO YOUR CV WRITING INSTRUCTIONS FILE]` |
| DOCX build script | Python script for producing .docx CVs when required | `[PATH TO YOUR build_cv_docx.py]` |
| DOCX CV template | Source .docx used by the build script | `[PATH TO YOUR CV template.docx]` |

---

## CV trigger

If the user's message begins with **"CV:"** followed by a job ad (pasted text or a link), treat this as a CV drafting request. Check `SETUP_COMPLETE` first — if `false`, run the first-run setup above before proceeding.

Then read the following two files in full:

1. CV writing instructions
2. Career history

Then follow the CV writing instructions from Step 1 onwards. The user does not need to reference any of these files in their prompt.

If a CV drafting request is clearly intended but does not begin with the "CV:" prefix — for example, the user pastes a job ad with an informal prompt, or says "can you write me a CV for this role" — ask the user whether they would like to use the CV workflow before doing anything else.

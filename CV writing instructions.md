# CV Writing Instructions

These instructions apply whenever a CV is to be drafted — triggered by the user providing a job ad.

Before drafting, read the career history file. If it is missing or has been moved, stop and flag the issue before proceeding.

If the job ad references an industry, domain or seniority level not clearly represented in the career history file, ask any clarifying questions in a single message before beginning.

---

## Step 1 — Analyse the job ad

Before writing anything, extract and structure the following from the job ad:

- Core responsibilities
- Required skills and experience (must-haves)
- Nice-to-have skills and experience
- Implied seniority level and fit with target seniority: [TARGET_SENIORITY — inserted by Claude during setup]
- Role-specific focus areas: [FOCUS_AREAS — inserted by Claude during setup]
- Cross-functional expectations
- Likely ATS keywords and phrases

Then answer internally: *What does this company actually need from this hire to be successful in the first 6–12 months?* Use this to guide all drafting decisions.

---

## Step 2 — Select and prioritise experience

From the career history file, select only experience that directly aligns with the context of this role. Prioritise:

- Outcomes (growth, revenue, adoption, retention, efficiency)
- Evidence of ownership (strategy, roadmap, decision-making)
- Cross-functional leadership and stakeholder management

Deprioritise or remove:

- Pure delivery or admin tasks without impact
- Irrelevant domains or tools
- Overly technical or overly commercial detail unless the role requires it

If a bullet does not clearly support this specific role, exclude it.

---

## Step 3 — Draft the CV

The CV must follow the same structure and formatting as the career history file.

**Profile statement**
- Maximum 90 words
- One paragraph only
- Must position the candidate at the correct seniority level for this role

**Key achievements bullets**
- Each bullet must be no longer than 30 words

**Professional Experience bullets (all roles)**
- Begin each bullet with an action verb
- State what was done and what changed as a result — lead with the action, close with the outcome or metric
- Exclude bullets that do not support this specific role

**Certifications**
- Include only certifications that directly match a stated requirement or reinforce the core positioning for this role
- Remove any that are off-topic, that raise questions about focus, or that belong to a different career narrative

**Skills section**
- Remove categories or items irrelevant to the role or that dilute the primary narrative; reorder so the most relevant appear first; rename categories if it better fits the job ad
- Do not repeat specific skills, tools or competencies already clearly evidenced in the professional experience bullets, unless omitting them would leave a material gap for ATS purposes
- Limit to 5 subsections and 30 words per subsection

**ATS keywords**
- Include relevant keywords naturally throughout
- Reflect phrasing from the job ad where it is a genuine match with experience
- Surface tools, frameworks, methodologies and domains clearly in the experience bullets and skills section

**Formatting rules — strictly apply throughout**
- No em dashes
- No Oxford commas, unless omitting one creates genuine ambiguity
- No fabrication or exaggeration of any kind
- Avoid the following terms, which are closely associated with AI-generated content. This list is illustrative, not exhaustive — apply the same judgement to any language that reads as AI-generated filler:
    - "fosters" or "fostering"
    - "delve" or "delving"
    - "Results-driven"
    - "Detail-oriented"
    - "Hard-working"
    - "Dynamic"
    - "Highly motivated"
    - "Passionate"
    - "Strategic thinker"
    - "Multifaceted"

---

## Step 4 — Quality checklist (complete before finalising)

Before the draft is considered complete, review it against the following:

- Does this CV clearly show the candidate can own and evolve their area of responsibility?
- Is there strong evidence of outcomes over outputs?
- Is the seniority level obvious and consistent throughout?
- Would a hiring manager be confident shortlisting this candidate based on the CV alone?
- Does the CV tell a clear story of progression and increasing ownership?
- Is the profile statement within 90 words?
- Are there any em dashes or Oxford commas?
- Are there any terms closely associated with AI-generated content?
- Has anything been fabricated or exaggerated?
- **Skills section:** Does every category and item directly support this specific role? Are the most relevant categories listed first?
- **Certifications section:** Does each certification either directly match a stated requirement or reinforce the core positioning for this role? Remove any that are off-topic or that belong to a different career narrative.
[EXTRA_CHECKLIST_ITEMS — inserted by Claude during setup, or remove this line if none]

---

## Step 5 — Self-review and redraft

This step is always performed automatically — it is not conditional.

Once the draft passes the quality checklist, review the full CV again alongside the job ad and the career history file. Consider:

- Is there anything in the career history that would strengthen this application that has not been included?
- Is there anything in the draft that does not clearly improve the candidate's chances and should be removed?
- Does the CV hold up against the job ad end to end?

Redraft incorporating any improvements identified. Present the final version to the user.

If the CV does not fit within 90 lines after this redraft, remove further bullets from the career experience section. Only remove bullets that are not directly applicable to the job ad — never remove a bullet that addresses a stated requirement or that provides the strongest available evidence for a key part of the role.

---

## Output

For each role, present:

1. A brief heading identifying the role (e.g. **[Job Title] — [Company name]**)
2. The full final CV text, ready to copy

Once the user has reviewed and approved the CV text, produce the final .docx file and save it to the CVs folder inside your job applications folder.

### How to produce the .docx

Use `build_cv_docx.py` as the template. Copy it to the outputs directory, update the CV content section (OUTPUT_FILENAME, NAME, CONTACT, PROFILE, ACHIEVEMENTS, ROLES, SKILLS, CERTIFICATIONS, EDUCATION), then run it via bash. The script resolves session paths dynamically — do not hard-code session names.

```
python3 "/sessions/$(ls /sessions)/mnt/[YOUR FOLDER NAME]/build_cv_docx.py"
```

**Formatting rules — always apply:**
- Every section heading (`add_heading1`, `add_prof_exp_header`) must be followed immediately by `sep()` to insert the page-wide decorative separator line. This applies to all headings without exception: Key Achievements, Professional Experience, Earlier Career, Skills, Certifications, Education.
- Use `/tmp/cv_build_work` as the working directory (not the mounted session outputs folder, which has file permission restrictions).
- Name the output file clearly by role and company, e.g. `Acme Corp - Senior PM.docx`.

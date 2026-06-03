# AI CV Toolkit Project

A personal workflow for tailoring CVs to specific job ads via an LLM (I use Claude and for simplicity sake will refer to this throughout this readme file). Paste in a job ad and Claude analyses the role, selects relevant experience from a career history file, drafts a targeted CV, self-reviews it, and produces a formatted `.docx` file — all in one session.

To keep my documents locally, rather than upload to the Anthropic space, I used Claude Cowork Projects (rather than Claude Chat Projects). Cowork can be found via the Claude app.

For this type of functionality, you will typically need a subscription to your chosen LLM.

---

## What you need to begin

- A .docx CV template: i.e. an example of your CV that is formatted to your taste from which new versions can be created
- A career history file (.txt or .md): I did this by taking all the different types of CVs I've written over time - that is, one example of a CV I've created for each of the different types of roles I've applied for - and dumped all the content in one long document (formatting is not important here). I then asked Claude to read the document, remove exact duplications and combine those that are similar but may contain different details in order to retain as much potentially-relevant detail as possible. Save as .txt or .md . 

---

## How it works

The workflow is triggered by prefixing a message with `CV:` followed by a job ad (pasted text or a URL). Claude then:

1. Analyses the job ad — responsibilities, required skills, seniority, ATS keywords
2. Selects and prioritises experience from your career history file
3. Drafts a tailored CV following the rules in `CV writing instructions.md`
4. Runs a quality checklist and self-review pass
5. Presents the final text for approval
6. Generates a formatted `.docx` using `build_cv_docx.py` and saves it to `CVs/`

---

## Local folder file structure

| File | Purpose |
|------|---------|
| `Your career history file` | Full work history, skills and certifications — the source of truth for all CV content |
| `CV writing instructions.md` | Step-by-step rules Claude follows when drafting and reviewing CVs |
| `build_cv_docx.py` | Python script that builds a formatted `.docx` from structured CV content |
| `Your .docx CV template` | Word document template used as the base for all output files |
| `memory.md` | Persistent session context read by Claude at the start of every session |
| `CVs/` | Output folder for completed `.docx` CV files |

---

## Requirements

- Subscription to an LLM that has a project capability (again, I use Claude, but other LLMs offer similar functionality).
- A folder selected as the workspace to which the docs in this repo have been downloaded
- The `docx` skill installed (for Claude): provides `unpack.py` / `pack.py` used by the build script (may already be installed as part of core capabilities - https://github.com/anthropics/skills/tree/main/skills/docx)
- Python 3 with `lxml` (`pip install lxml`) (your LLM can help with instructions for this)

---

## Usage

Open a Claude session with this folder selected, then send:

```
CV: [paste job ad here]
```

Claude reads `memory.md` automatically at the start of each session, so no further setup is needed.

If this is the first time running this workflow, Claude will ask a short series of questions so it has the right context before generating content.

---

## Output

Completed CVs are saved to the `CVs/` folder as `.docx` files, named by role and company (e.g. `Acme Corp - Senior PM.docx`). The build script resolves session paths dynamically, so it works across Cowork sessions without modification.

---

## Notes

- No CV content is fabricated or exaggerated — Claude is explicitly instructed to work only from the career history file
- The workflow applies a quality checklist before finalising, checking for seniority consistency, outcome focus, ATS coverage and formatting rules
- `build_cv_docx.py` has an empty content section — Claude copies it to a working directory, fills in the CV content, and runs it from there, leaving the source file unchanged

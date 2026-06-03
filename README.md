# Job Applications — Claude Cowork Project

A personal workflow for tailoring CVs to specific job ads, built on top of Claude's Cowork mode. Paste in a job ad and Claude analyses the role, selects relevant experience from a career history file, drafts a targeted CV, self-reviews it, and produces a formatted `.docx` file — all in one session.

---

## How it works

The workflow is triggered by prefixing a message with `CV:` followed by a job ad (pasted text or a URL). Claude then:

1. Analyses the job ad — responsibilities, required skills, seniority, ATS keywords
2. Selects and prioritises experience from `Career history.md`
3. Drafts a tailored CV following the rules in `CV writing instructions.md`
4. Runs a quality checklist and self-review pass
5. Presents the final text for approval
6. Generates a formatted `.docx` using `build_cv_docx.py` and saves it to `CVs/`

---

## File structure

| File | Purpose |
|------|---------|
| `Career history.md` | Full work history, skills and certifications — the source of truth for all CV content |
| `CV writing instructions.md` | Step-by-step rules Claude follows when drafting and reviewing CVs |
| `build_cv_docx.py` | Python script that builds a formatted `.docx` from structured CV content |
| `CV template.docx` | Word document template used as the base for all output files |
| `memory.md` | Persistent session context read by Claude at the start of every session |
| `CVs/` | Output folder for completed `.docx` CV files |

---

## Requirements

- [Claude desktop app](https://claude.ai/download) with Cowork mode enabled
- A folder selected as the workspace (this folder)
- The `docx` skill installed in Cowork (provides `unpack.py` / `pack.py` used by the build script)
- Python 3 with `lxml` (`pip install lxml`)

---

## Usage

Open a Cowork session with this folder selected, then send:

```
CV: [paste job ad here]
```

Claude reads `memory.md` automatically at the start of each session, so no further setup is needed.

---

## Output

Completed CVs are saved to the `CVs/` folder as `.docx` files, named by role and company (e.g. `Acme Corp - Senior PM.docx`). The build script resolves session paths dynamically, so it works across Cowork sessions without modification.

---

## Notes

- No CV content is fabricated or exaggerated — Claude is explicitly instructed to work only from the career history file
- The workflow applies a quality checklist before finalising, checking for seniority consistency, outcome focus, ATS coverage and formatting rules
- The `build_cv_docx.py` script contains a sample CV in its content section (the most recently built CV) — this is overwritten each time a new CV is produced

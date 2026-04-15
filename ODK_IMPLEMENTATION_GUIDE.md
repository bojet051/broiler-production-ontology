# Broiler Production Ontology: ODK Migration Implementation Guide

**Date:** April 15, 2026  
**Repository:** https://github.com/bojet051/broiler-production-ontology  
**Current Commit (as of this guide update):** `2849530` - "Add mkdocs configuration and comprehensive documentation site"

This guide documents the actual step-by-step implementation of the Broiler Production Ontology using the Ontology Development Kit (ODK), including challenges encountered and solutions applied.

---

## Overview

We successfully migrated a standalone Turtle ontology (`Broiler Production.ttl`) into the ODK repository structure, which provides standardized build pipelines, validation, CI/CD templates, and release management.

**Key outcomes:**
- ✅ ODK scaffold generated and integrated into working repository
- ✅ Canonical ontology migrated to `src/ontology/broiler-production-ontology-edit.ttl`
- ✅ `make test` validation: **PASSED** (0 violations)
- ✅ `make prepare_release` build: **PASSED** (release artifacts generated)
- ✅ All changes committed and pushed to `origin/main`

---

## Step-by-Step Implementation

### Step 1: Prepare Bootstrap Workspace

**Purpose:** Keep ODK seed process separate from final repository.

```bash
mkdir -p ~/production_ontology/broiler_odk_bootstrap
cd ~/production_ontology/broiler_odk_bootstrap
```

**Why:** Separates temporary ODK generation artifacts from the actual working repository, making cleanup easier and the repo structure cleaner.

---

### Step 2: Create ODK Config File

**Purpose:** Define ontology metadata and build parameters for ODK seed script.

**File:** `broiler_odk_bootstrap/broiler-odk.yaml`

```yaml
id: broiler-production-ontology
title: Industrial Broiler Production Ontology
github_org: bojet051
repo: broiler-production-ontology
git_main_branch: main
release_artefacts:
  - full
primary_release: full
export_formats:
  - owl
  - ttl
robot_java_args: -Xmx8G
robot_report:
  use_labels: true
  exclude_annotations:
    - owl:versionInfo
```

**Key configuration notes:**
- `id` and `repo` must match exactly (used in file naming and IRI generation)
- `export_formats: [owl, ttl]` ensures both OWL and Turtle release formats
- `robot_java_args: -Xmx8G` ensures sufficient memory for larger ontology builds
- `robot_report` settings control QC report output

---

### Step 3: Generate ODK Scaffold

**Command:**
```bash
cd ~/production_ontology/broiler_odk_bootstrap
sh seed-via-docker.sh -c -C broiler-odk.yaml
```

**What happens:**
1. Docker image `obolibrary/odkfull:latest` is pulled (if not cached)
2. ODK seed process generates a complete repository structure in `target/broiler-production-ontology/`
3. ODK runs initial build and git initialization within the generated scaffold
4. Generated files include Makefiles, CI/CD workflows, SPARQL validation queries, and placeholder ontology files

**Expected output files:**
```
target/broiler-production-ontology/
├── .github/workflows/          (GitHub Actions CI/CD)
├── src/
│   ├── ontology/              (Makefile, catalog, run.sh)
│   ├── sparql/                (SPARQL-based QC checks)
│   ├── scripts/
│   └── metadata/
├── .gitignore
├── CONTRIBUTING.md
├── Makefile (root)
└── README.md
```

**⚠️ Note on failure:** The seed script may exit with code 1 due to an incomplete git commit at the end, but the scaffold is fully generated. This is safe to ignore if files are created successfully.

---

### Step 4: Recover Repository Metadata (If Needed)

**Situation:** If the generated scaffold's `.git` folder overwrites your actual repository metadata, recover it:

```bash
cd ~/production_ontology

# Stash untracked files that belong to your real repo
mkdir -p /tmp/broiler_recover
mv "Broiler ODK Migration Notes.md" /tmp/broiler_recover/
mv "Broiler Production.ttl" /tmp/broiler_recover/
mv broiler_odk_bootstrap/broiler-odk.yaml /tmp/broiler_recover/broiler_odk_bootstrap/
mv broiler_odk_bootstrap/seed-via-docker.sh /tmp/broiler_recover/broiler_odk_bootstrap/

# Restore real repository history from remote
git remote add origin https://github.com/bojet051/broiler-production-ontology.git
git fetch origin main
git checkout -B main origin/main

# Restore your files
cp /tmp/broiler_recover/"Broiler ODK Migration Notes.md" .
cp /tmp/broiler_recover/"Broiler Production.ttl" .
cp /tmp/broiler_recover/broiler_odk_bootstrap/* broiler_odk_bootstrap/
```

---

### Step 5: Merge Scaffold into Working Repository

**Command:**
```bash
cd ~/production_ontology
rsync -a --exclude='.git' broiler_odk_bootstrap/target/broiler-production-ontology/ ./
```

**What it does:**
- Copies all generated scaffold files into the repository root
- `--exclude='.git'` prevents overwriting your real `.git` metadata
- Result: ODK structure (src/, Makefile, .github/, etc.) is now in your working repo alongside your original files

**After merge, your repo contains:**
```
production_ontology/
├── Broiler Production.ttl        (original canonical ontology)
├── Broiler ODK Migration Notes.md (project notes)
├── broiler_odk_bootstrap/         (bootstrap config)
├── src/                           (ODK structure - NEW)
├── .github/                       (CI/CD workflows - NEW)
├── Makefile                       (root build file - NEW)
├── .gitignore                     (NEW)
├── CONTRIBUTING.md                (NEW)
└── src/ontology/                  (ODK ontology workspace)
```

---

### Step 6: Migrate Canonical Ontology into ODK Layout

**Command:**
```bash
cp "Broiler Production.ttl" src/ontology/broiler-production-ontology-edit.ttl
```

**Why:**
- ODK expects the editable source at `src/ontology/{ontid}-edit.{format}`
- Our format is Turtle (`.ttl`), not OWL (default `.owl`)

**Configure ODK to use Turtle:**

Edit `src/ontology/broiler-production-ontology.Makefile` and add:
```makefile
EDIT_FORMAT = ttl
```

This tells ODK to use `broiler-production-ontology-edit.ttl` as the source instead of `.owl`.

---

### Step 7: Connect Repository to GitHub (If Not Already Done)

**Commands:**
```bash
cd ~/production_ontology
git init                          # Only if not already initialized
git branch -M main                 # Rename default branch to main
git remote add origin https://github.com/bojet051/broiler-production-ontology.git
git remote -v                      # Verify remote
git fetch origin main              # Pull remote history
git checkout -B main origin/main   # Track remote
```

**Verification:**
```bash
git status
git log --oneline -n 3
```

---

### Step 8: Validate Ontology with ODK

**Command:**
```bash
cd ~/production_ontology/src/ontology
sh ./run.sh make test
```

**What it tests:**
- **Reasoning:** ELK reasoner checks for logical consistency
- **SPARQL QC:** Runs predefined quality checks:
  - `owldef-self-reference-violation.sparql`
  - `iri-range-violation.sparql`
  - `label-with-iri-violation.sparql`
  - `multiple-replaced_by-violation.sparql`
- **Profile validation:** OWL 2 DL profile compliance

**Expected successful output:**
```
PASS Rule ../sparql/owldef-self-reference-violation.sparql: 0 violation(s)
PASS Rule ../sparql/iri-range-violation.sparql: 0 violation(s)
PASS Rule ../sparql/label-with-iri-violation.sparql: 0 violation(s)
PASS Rule ../sparql/multiple-replaced_by-violation.sparql: 0 violation(s)
Finished running all tests successfully.
```

**Our result:** ✅ All tests PASSED with 0 violations.

---

### Step 9: Build Release Artifacts

**Command:**
```bash
cd ~/production_ontology/src/ontology
sh ./run.sh make prepare_release
```

**What it generates:**
- Preprocesses and reasons over the ontology
- Generates multiple release formats:
  - `broiler-production-ontology.owl` (reasoned, merged)
  - `broiler-production-ontology.ttl` (Turtle version)
  - `broiler-production-ontology-full.owl` (with all imports)
  - `broiler-production-ontology-full.ttl` (full Turtle)
- Generates QC reports:
  - `reports/basic-report.tsv`
  - `reports/edges.tsv`
  - `reports/synonyms.tsv`
  - etc.
- Copies release files to `../../` (repo root)

**Expected successful output:**
```
Repository is up-to-date.
Checking RDF/XML file broiler-production-ontology.owl...
  LightRDF: OK
Checking RDF/XML file broiler-production-ontology-full.owl...
  LightRDF: OK
Release files are now in ../.. - now you should commit, push and make a release
```

**Our result:** ✅ Build PASSED. Release artifacts generated in repo root.

---

### Step 10: Commit and Push Migration

**Commands:**
```bash
cd ~/production_ontology

# Stage all files EXCEPT temporary bootstrap target folder
git add . ':(exclude)broiler_odk_bootstrap/target'

# Commit with descriptive message
git commit -m "Migrate broiler ontology into ODK structure"

# Push to GitHub
git push origin main

# Verify
git status --short
git log --oneline -n 2
```

**What was committed:**
- ODK structure (Makefile, src/, .github/)
- Release artifacts (`.owl` and `.ttl` files in root)
- QC reports (reports/)
- Configuration files (.gitignore, catalog, etc.)

**Result:**
```
[main c87bf7c] Migrate broiler ontology into ODK structure
 45 files changed, 2930 insertions(+)
To https://github.com/bojet051/broiler-production-ontology.git
   0c25d82..c87bf7c  main -> main
```

---

### Step 11: Clean Up Temporary Artifacts

**Commands:**
```bash
cd ~/production_ontology
rm -rf broiler_odk_bootstrap/target
```

**Why:**
- The `target/` folder was only needed during seed generation
- All useful content was already rsync'd into the repo
- Removes unnecessary ~100MB of temporary Docker build output

**Result:** `broiler_odk_bootstrap/` now contains only:
- `broiler-odk.yaml` (configuration for future re-seeding if needed)
- `seed-via-docker.sh` (script for future updates)

---

## Key Differences from Original Instructions

| Original Step | What We Did | Reason |
|---------------|-----------|--------|
| Step 4: `mv target/broiler ~/...` | Used `rsync` with `.git` exclusion | Safer approach to merge scaffold while preserving real repo metadata |
| Step 5: Direct copy | Conditional metadata recovery | The scaffold's auto-generated `.git` would corrupt our real repository history |
| Step 6: Replace entire `.owl` file | Migrated to Turtle source | Our ontology is in Turtle format; added `EDIT_FORMAT = ttl` configuration |
| Step 7: Init bare repo | Connected to existing GitHub repo | We had a pre-existing remote with history |
| Step 10: `make test` from root | Ran from `src/ontology/` | ODK Makefile targets only exist in `src/ontology/` context |

---

## Troubleshooting Reference

### Docker Not Running
**Error:** `docker: Cannot connect to the Docker daemon`
**Solution:** Start Docker Desktop (`open -a Docker` on macOS), wait for whale icon to show ready, then retry seed command.

### Seed Script Exits with Code 1
**Error:** `Exception: Failed: cd target/broiler-production-ontology && git commit -a...`
**Status:** Non-fatal. Scaffold was still generated successfully.
**Action:** Run `git add . && git commit -m "initial build"` in the generated target folder if needed, or proceed with merge.

### Make Test Has No Target
**Error:** `make: *** No rule to make target 'test'. Stop.`
**Solution:** Run from `src/ontology/` directory (not repo root). The Makefile is in `src/ontology/Makefile`.

### Missing Release Files
**Symptom:** No `.owl` or `.ttl` files in repo root after `prepare_release`
**Check:** SPARQL QC violations or reasoning failures in terminal output. Fix ontology issues and rerun `make test` + `make prepare_release`.

**Our status:** All checks passed; all release files generated successfully.

---

## Current Repository State (Final)

**Remote:** https://github.com/bojet051/broiler-production-ontology  
**Branch:** main  
**Latest commit:** `c87bf7c`

### Key Files

- **Source ontology:** [src/ontology/broiler-production-ontology-edit.ttl](src/ontology/broiler-production-ontology-edit.ttl)
- **Build configuration:** [src/ontology/broiler-production-ontology.Makefile](src/ontology/broiler-production-ontology.Makefile)
- **Run script:** [src/ontology/run.sh](src/ontology/run.sh)
- **Release artifacts:**
  - `broiler-production-ontology.owl`
  - `broiler-production-ontology.ttl`
  - `broiler-production-ontology-full.owl`
  - `broiler-production-ontology-full.ttl`
- **QC reports:** `reports/` directory with SPARQL query results
- **CI/CD pipelines:** `.github/workflows/` (qc.yml, docs.yml)

### How to Continue Development

1. **Edit the ontology:**
   ```bash
   cd ~/production_ontology/src/ontology
   # Edit broiler-production-ontology-edit.ttl in your editor
   ```

2. **Validate changes:**
   ```bash
   sh ./run.sh make test
   ```

3. **Build release artifacts:**
   ```bash
   sh ./run.sh make prepare_release
   ```

4. **Commit and push:**
   ```bash
   git add .
   git commit -m "Update broiler ontology: [describe changes]"
   git push
   ```

5. **Update ODK scaffold (if needed):**
   ```bash
   cd broiler_odk_bootstrap
   sh seed-via-docker.sh -c -C broiler-odk.yaml
   ```

---

## Summary

The Broiler Production Ontology is now successfully integrated into ODK's standardized development and release framework, with:
- ✅ Automated validation pipeline (SPARQL QC, reasoning, profile checks)
- ✅ Multi-format release generation (OWL + Turtle)
- ✅ GitHub CI/CD workflows (docs, QC checks on PR)
- ✅ Canonical source in Turtle format
- ✅ Release artifacts published on each commit
- ✅ Full git history and remote tracking configured

All 12 steps completed successfully.

---

## Post-Migration Additions (Completed)

After the initial ODK migration, we added and validated the documentation deployment layer.

### A) Fix docs workflow prerequisites

The ODK-generated docs workflow expected `mkdocs.yaml` to exist. The initial workflow run failed until this file and the docs pages were added.

Added:
- `mkdocs.yaml`
- `docs/index.md`
- `docs/getting-started.md`
- `docs/ontology-structure.md`
- `docs/development.md`
- `docs/contributing.md`
- `docs/releases.md`

Result:
- Docs pipeline in `.github/workflows/docs.yml` is now configured with required inputs.

### B) Keep bootstrap output out of long-term workflow

Temporary ODK seed output under `broiler_odk_bootstrap/target/` was removed after scaffold merge.

Result:
- Bootstrap folder now contains only reusable seed inputs:
  - `broiler_odk_bootstrap/broiler-odk.yaml`
  - `broiler_odk_bootstrap/seed-via-docker.sh`

---

## Next Implementation Plan: LLM-Assisted Ontology Update Loop

This is the practical roadmap for implementing the paper-style approach (manual curation + LLM assistance) in this repository.

### Phase 1 — Define Scope and Metrics

Set boundaries for what the LLM may propose and what must remain human-curated.

Success metrics:
- QC pass rate on PRs (`make test`)
- Number of accepted/rejected LLM suggestions per cycle
- Time from candidate generation to merged update
- Number of ontology terms with complete labels/comments/axioms

### Phase 2 — Design Candidate Schema

Use a structured record for each LLM suggestion, e.g.:
- candidate IRI/local name
- preferred label
- textual definition
- parent class / property target
- proposed axioms/restrictions
- evidence source
- confidence score

Implemented artifacts in this repository:
- `curation/candidate-schema.json` (machine-validated schema)
- `curation/candidate-example.yaml` (filled example record)

Usage:
1. Create one candidate YAML per proposed term/change (following schema fields).
2. Validate candidate completeness against the schema before review.
3. Attach candidate record to the PR that modifies ontology content.

### Phase 3 — Prompt Templates and Guardrails

Create standard prompts that force:
- ontology-consistent naming
- no contradiction with existing restrictions
- no removal of existing semantics unless explicitly requested
- deprecation-first strategy for replacement terms

Implemented artifacts in this repository:
- `curation/prompts/system-prompt.md`
- `curation/prompts/candidate-generation-prompt.md`
- `curation/prompts/self-check-prompt.md`
- `curation/prompts/guardrails.md`
- `curation/prompts/README.md`

Practical use:
1. Run generation with `system-prompt.md` + `candidate-generation-prompt.md`.
2. Run internal QA using `self-check-prompt.md`.
3. Enforce acceptance boundaries via `guardrails.md` before PR merge.

### Phase 4 — Human Review Workflow

Every candidate must pass a checklist before merge:
- semantic fit to domain
- consistency with modeling style
- label/comment quality
- backward compatibility check
- validation outputs reviewed

Implemented artifacts in this repository:
- `.github/PULL_REQUEST_TEMPLATE.md`
- `curation/review-checklist.md`

Workflow:
1. Open PR using the repository PR template.
2. Link candidate file(s) and prompt assets used.
3. Reviewer executes `curation/review-checklist.md` before approval.
4. Merge only after checklist + QC gates pass.

### Phase 5 — Candidate-to-Ontology Update Flow

Operational sequence:
1. Generate candidate set (LLM)
2. Curator triage (accept/revise/reject)
3. Apply accepted changes to `src/ontology/broiler-production-ontology-edit.ttl`
4. Run local validation (`sh ./run.sh make test`)
5. Open PR with candidate evidence + QC outputs

Implemented artifact:
- `scripts/apply_candidate.py` validates a candidate against `curation/candidate-schema.json` and can preview or write a Turtle block for the editable ontology file.

Usage:
1. Validate a candidate only: `python scripts/apply_candidate.py --check src/ontology/broiler-production-ontology-edit.ttl curation/candidate-example.yaml`
2. Apply an accepted candidate in place: `python scripts/apply_candidate.py --write src/ontology/broiler-production-ontology-edit.ttl curation/candidates/<candidate>.yaml`
3. Keep candidate records under `curation/candidates/` for PR-based review.

### Phase 6 — CI/QC Gates

Enforce in PR process:
- CI workflow must pass (`.github/workflows/qc.yml`)
- docs workflow remains green when docs are touched (`.github/workflows/docs.yml`)
- no direct push to main for ontology structural changes without review

Implemented artifact:
- `.github/workflows/curation.yml` validates the schema and runs the candidate application tool in check mode on PRs.

### Phase 7 — Mapping and Alignment

For accepted terms, track potential mappings to related ontologies/resources where relevant.

Minimum mapping metadata:
- mapped term ID
- mapping type (exact/broad/narrow/related)
- source and reviewer

### Phase 8 — Pilot and Iterate

Pilot one subdomain first (e.g., feed management or lifecycle modeling), evaluate outcomes, then scale to additional branches.

---

## Operational Notes

- `src/ontology/run.sh` and CI were generated by ODK seed; they are template-managed assets.
- The editable ontology source remains `src/ontology/broiler-production-ontology-edit.ttl`.
- Keep `EDIT_FORMAT = ttl` in `src/ontology/broiler-production-ontology.Makefile`.
- Use the bootstrap directory only for re-seeding/upgrading ODK templates.
- Use `curation/candidate-schema.json` as the mandatory intake format for LLM-assisted proposals.
- Use `curation/prompts/` as the standard generation + QA prompt pack for every candidate cycle.

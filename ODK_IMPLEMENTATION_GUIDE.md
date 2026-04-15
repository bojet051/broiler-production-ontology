# Broiler Production Ontology: ODK Migration Implementation Guide

**Date:** April 15, 2026  
**Repository:** https://github.com/bojet051/broiler-production-ontology  
**Final Commit:** `c87bf7c` - "Migrate broiler ontology into ODK structure"

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

### Step 2: Create OD K Config File

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

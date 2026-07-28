# SHADE paper

IEEE conference-format draft.

## Easiest path: Overleaf (recommended, no local install)
1. Go to overleaf.com → New Project → Upload Project.
2. Zip and upload this `paper/` folder (or drag `main.tex` + `references.bib`).
3. Menu → Settings → Compiler = **pdfLaTeX**, Main document = `main.tex`.
4. Recompile. Overleaf handles the `IEEEtran` class automatically.

## Local compile (if you prefer)
```powershell
pdflatex main.tex
bibtex main
pdflatex main.tex
pdflatex main.tex
```
(Requires a TeX distribution like MiKTeX with the `IEEEtran` package.)

## How we fill it
Sections carry `% TODO` markers tied to the project phases:
- **Related Work** ← `docs/literature.md` (Week 1)
- **Methodology** ← once the autoencoder + SHAP layers are built (Week 2–3)
- **Results/Tables** ← numbers from `results/metrics.json` (Week 2–4)
- **Abstract** ← written last, once results are final

Figures go in `paper/fig/` (create as needed). Export the architecture diagram and
SHAP plots from `results/` into that folder.

# Deploying the SHADE-IDS dashboard

The dashboard reads the committed figures in `docs/`, so it runs anywhere without
retraining or shipping the dataset.

## Run locally
```powershell
pip install -r requirements-app.txt
streamlit run app.py
```
Opens at <http://localhost:8501>. Because it runs in the browser it works the same on
Windows, macOS and Linux.

## Browser deployment

The [browser demo](https://kanishksigar.me/shade-ids/) runs the same Streamlit
application with Stlite and Pyodide on the portfolio's GitHub Pages site. CSV uploads
are processed in the browser. The first visit downloads the runtime and dependencies.

Build the static files from this checkout:
```sh
sh browser/build.sh /path/to/portfolio/public/shade-ids
```

Use `npm run build` from the portfolio repo to preview or publish its Pages bundle.
Keep the Python app and research figures in this repository as the source of truth.

## Deploy free on Streamlit Community Cloud
1. Go to <https://share.streamlit.io> and sign in with GitHub.
2. **New app** -> repo `KanishkSigar/shade-ids`, branch `main`, main file `app.py`.
3. In **Advanced settings**, set the requirements file to `requirements-app.txt`
   (much faster build than the full stack).
4. Deploy, then paste the resulting `*.streamlit.app` URL into the README.

## Regenerating the figures
```powershell
pip install -r requirements.txt
python -m src.eda          # Week 1 distribution chart
python -m src.train        # Week 2 ROC + metrics
python -m src.hybrid       # Week 3 reconstruction-error plot
python -m src.explain_run  # Week 4 SHAP figures
```
Copy any updated PNGs from `results/` into `docs/` so the dashboard picks them up.

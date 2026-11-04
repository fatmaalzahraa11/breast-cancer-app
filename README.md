# OncoScan AI: Breast Cancer Classification Dashboard

Streamlit app for the Breast Cancer Wisconsin (Original) project: Dataset Exploration, Preprocessing, EDA,
Model Implementation (GridSearchCV) and Model Evaluation, plus a live predictor.

## Run in VS Code
1. Open this folder in VS Code (`File > Open Folder`).
2. Open a terminal (`Ctrl+` `) and create an environment:
   ```
   python -m venv .venv
   .venv\Scripts\activate        # Windows   (Mac/Linux: source .venv/bin/activate)
   pip install -r requirements.txt
   ```
3. Keep the dataset zip inside the `data/` folder (already included).
4. Start the app:
   ```
   streamlit run app.py
   ```
5. In the app: open **Model Training** and press **Start tuning** (Quick about 20 s, Full about 3 min).
   Results are saved in `models/`, so they load instantly next time.

## Files
- `app.py`: Streamlit interface (7 pages)
- `ml_core.py`: the notebook logic (loading, preprocessing, tuning, evaluation, prediction)
- `styles.py`: CSS and the animated hero banner
- `.streamlit/config.toml`: dark theme
- `notebook.ipynb`: the full project notebook (Tasks 1 to 5)

Malignant = 1 is the positive class everywhere. Educational project, not a medical device.

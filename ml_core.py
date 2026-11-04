"""
ml_core.py
Machine-learning core of the Breast Cancer Wisconsin project (Tasks 1 to 5).
Same logic as the notebook: no data leakage, Malignant = 1 is the positive class.
The Streamlit UI (app.py) only calls the functions in this file.
"""
import glob
import os
import time
import zipfile

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score, roc_auc_score,
                             roc_curve)
from sklearn.model_selection import (GridSearchCV, ParameterGrid,
                                     StratifiedKFold, train_test_split)
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

RANDOM_STATE = 42
DATA_FILE = "breast-cancer-wisconsin.data"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS_DIR = os.path.join(BASE_DIR, "models")

COLS = ["id", "Clump_Thickness", "Uniformity_Cell_Size", "Uniformity_Cell_Shape",
        "Marginal_Adhesion", "Single_Epithelial_Cell_Size", "Bare_Nuclei",
        "Bland_Chromatin", "Normal_Nucleoli", "Mitoses", "Class"]
FEATURES = COLS[1:-1]
MODEL_ORDER = ["KNN", "Decision Tree", "Random Forest", "ANN (MLP)", "SVM"]
SCORING = {"accuracy": "accuracy", "precision": "precision",
           "recall": "recall", "f1": "f1", "roc_auc": "roc_auc"}


# ----------------------------------------------------------------- Task 1
def _open_data():
    for folder in [BASE_DIR, os.path.join(BASE_DIR, "data"), ".", "data"]:
        path = os.path.join(folder, DATA_FILE)
        if os.path.exists(path):
            return path
    zips = [f for folder in [BASE_DIR, os.path.join(BASE_DIR, "data"), ".", "data"]
            for f in glob.glob(os.path.join(folder, "*.zip"))
            if "wisconsin" in os.path.basename(f).lower()]
    if not zips:
        raise FileNotFoundError(
            "Dataset not found. Put the UCI zip (its name contains 'wisconsin') "
            "inside the 'data' folder next to app.py.")
    z = zipfile.ZipFile(zips[0])
    member = [n for n in z.namelist() if n.endswith(DATA_FILE)][0]
    return z.open(member)


def load_raw():
    """Raw data: no header in the file, missing values are marked with '?'."""
    return pd.read_csv(_open_data(), header=None, names=COLS, na_values="?")


# ----------------------------------------------------------------- Task 2
def preprocess(df_raw):
    """Duplicates -> drop id -> encode target -> 80:20 stratified split ->
    median imputation and standardization fitted on TRAIN only."""
    df = df_raw.drop_duplicates().reset_index(drop=True)
    n_dup = len(df_raw) - len(df)
    df = df.drop(columns=["id"])
    X = df[FEATURES].copy()
    y = df["Class"].map({2: 0, 4: 1})          # Malignant = 1 (positive class)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=RANDOM_STATE, stratify=y)

    imputer = SimpleImputer(strategy="median").fit(X_train)
    X_train_imp = pd.DataFrame(imputer.transform(X_train), columns=FEATURES, index=X_train.index)
    X_test_imp = pd.DataFrame(imputer.transform(X_test), columns=FEATURES, index=X_test.index)

    scaler = StandardScaler().fit(X_train_imp)
    X_train_scaled = pd.DataFrame(scaler.transform(X_train_imp), columns=FEATURES, index=X_train.index)
    X_test_scaled = pd.DataFrame(scaler.transform(X_test_imp), columns=FEATURES, index=X_test.index)

    return dict(df=df, n_dup=n_dup, X=X, y=y,
                X_train=X_train, X_test=X_test, y_train=y_train, y_test=y_test,
                imputer=imputer, scaler=scaler,
                X_train_imp=X_train_imp, X_test_imp=X_test_imp,
                X_train_scaled=X_train_scaled, X_test_scaled=X_test_scaled)


# ----------------------------------------------------------------- Task 4
def _scaled(model):
    return Pipeline([("imputer", SimpleImputer(strategy="median")),
                     ("scaler", StandardScaler()), ("model", model)])


def _unscaled(model):
    return Pipeline([("imputer", SimpleImputer(strategy="median")), ("model", model)])


def get_models(fast=False):
    """Pipelines + hyperparameter grids. fast=False is exactly the notebook search."""
    if fast:
        knn = {"model__n_neighbors": [3, 5, 7, 9], "model__weights": ["uniform", "distance"],
               "model__metric": ["euclidean"]}
        dt = {"model__criterion": ["gini", "entropy"], "model__max_depth": [3, 4, 6, None],
              "model__min_samples_split": [2, 5], "model__min_samples_leaf": [1, 2]}
        rf = {"model__n_estimators": [100, 200], "model__max_depth": [None, 10],
              "model__min_samples_leaf": [1, 2], "model__max_features": ["sqrt"]}
        ann = {"model__hidden_layer_sizes": [(8,), (16,)], "model__activation": ["relu", "tanh"],
               "model__alpha": [1e-3], "model__learning_rate_init": [0.001, 0.01]}
        svm = [{"model__kernel": ["linear"], "model__C": [0.1, 1, 10]},
               {"model__kernel": ["rbf"], "model__C": [1, 10], "model__gamma": ["scale", 0.1]}]
    else:
        knn = {"model__n_neighbors": [3, 5, 7, 9, 11, 13, 15],
               "model__weights": ["uniform", "distance"],
               "model__metric": ["euclidean", "manhattan"]}
        dt = {"model__criterion": ["gini", "entropy"], "model__max_depth": [3, 4, 5, 6, 8, None],
              "model__min_samples_split": [2, 5, 10], "model__min_samples_leaf": [1, 2, 4]}
        rf = {"model__n_estimators": [100, 200, 300], "model__max_depth": [None, 5, 10],
              "model__min_samples_split": [2, 5], "model__min_samples_leaf": [1, 2],
              "model__max_features": ["sqrt", "log2"]}
        ann = {"model__hidden_layer_sizes": [(8,), (16,), (32,), (16, 8)],
               "model__activation": ["relu", "tanh"], "model__alpha": [1e-4, 1e-3, 1e-2],
               "model__learning_rate_init": [0.001, 0.01]}
        svm = [{"model__kernel": ["linear"], "model__C": [0.01, 0.1, 1, 10, 100]},
               {"model__kernel": ["rbf"], "model__C": [0.1, 1, 10, 100],
                "model__gamma": ["scale", 0.01, 0.1, 1]}]
    return {
        "KNN": (_scaled(KNeighborsClassifier()), knn),
        "Decision Tree": (_unscaled(DecisionTreeClassifier(random_state=RANDOM_STATE)), dt),
        "Random Forest": (_unscaled(RandomForestClassifier(random_state=RANDOM_STATE)), rf),
        "ANN (MLP)": (_scaled(MLPClassifier(max_iter=2000, random_state=RANDOM_STATE)), ann),
        "SVM": (_scaled(SVC(random_state=RANDOM_STATE)), svm),
    }


def grid_sizes(fast=False):
    return {n: len(ParameterGrid(g)) for n, (_, g) in get_models(fast).items()}


def _clean(params):
    return {k.replace("model__", ""): v for k, v in params.items()}


def tune_all(X_train, y_train, fast=False, progress=None):
    """GridSearchCV (5-fold stratified) on the TRAINING set only. Returns a light, picklable dict."""
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    models = get_models(fast)
    out = {}
    for i, (name, (pipe, grid)) in enumerate(models.items()):
        if progress:
            progress(i, len(models), name, "start")
        t0 = time.time()
        gs = GridSearchCV(pipe, grid, cv=cv, scoring=SCORING, refit="f1", n_jobs=-1)
        gs.fit(X_train, y_train)
        r, b = gs.cv_results_, gs.best_index_
        top = pd.DataFrame(r).sort_values("rank_test_f1").head(5)
        out[name] = {
            "estimator": gs.best_estimator_,
            "best_params": _clean(gs.best_params_),
            "cv": {m: (float(r[f"mean_test_{m}"][b]), float(r[f"std_test_{m}"][b])) for m in SCORING},
            "top": [{"params": _clean(p), "f1": float(f), "recall": float(rc)}
                    for p, f, rc in zip(top["params"], top["mean_test_f1"], top["mean_test_recall"])],
            "seconds": time.time() - t0,
            "n_combinations": len(ParameterGrid(grid)),
        }
        if progress:
            progress(i + 1, len(models), name, "done")
    return {"models": out, "fast": fast}


def save_tuning(tuning, fast):
    os.makedirs(MODELS_DIR, exist_ok=True)
    joblib.dump(tuning, os.path.join(MODELS_DIR, f"tuning_{'quick' if fast else 'full'}.joblib"))


def load_tuning(fast):
    p = os.path.join(MODELS_DIR, f"tuning_{'quick' if fast else 'full'}.joblib")
    return joblib.load(p) if os.path.exists(p) else None


# ----------------------------------------------------------------- Task 5
def get_scores(est, X):
    """Continuous malignancy score (probability, or margin for SVM) used for ROC-AUC."""
    return est.predict_proba(X)[:, 1] if hasattr(est, "predict_proba") else est.decision_function(X)


def evaluate(tuning, X_test, y_test):
    """Test-set metrics (Malignant = positive class), ranked by Recall -> F1 -> ROC-AUC."""
    rows, preds, scores, rocs = [], {}, {}, {}
    for name, info in tuning["models"].items():
        est = info["estimator"]
        yp, ys = est.predict(X_test), get_scores(est, X_test)
        preds[name], scores[name] = yp, ys
        tn, fp, fn, tp = confusion_matrix(y_test, yp).ravel()
        fpr, tpr, _ = roc_curve(y_test, ys)
        rocs[name] = (fpr, tpr)
        rows.append({"Model": name,
                     "Accuracy": accuracy_score(y_test, yp),
                     "Precision": precision_score(y_test, yp, pos_label=1),
                     "Recall": recall_score(y_test, yp, pos_label=1),
                     "F1-score": f1_score(y_test, yp, pos_label=1),
                     "ROC-AUC": roc_auc_score(y_test, ys),
                     "TN": int(tn), "FP": int(fp), "FN": int(fn), "TP": int(tp),
                     "CV F1": info["cv"]["f1"][0], "CV Recall": info["cv"]["recall"][0]})
    df = pd.DataFrame(rows).set_index("Model")
    df["F1 gap (CV - test)"] = df["CV F1"] - df["F1-score"]
    df = df.sort_values(["Recall", "F1-score", "ROC-AUC"], ascending=False)
    df.insert(0, "Rank", range(1, len(df) + 1))
    return df, preds, scores, rocs


def predict_one(estimator, values):
    """values: dict feature -> value. Returns (label, malignancy score in [0,1], is_probability)."""
    X = pd.DataFrame([values], columns=FEATURES)
    label = int(estimator.predict(X)[0])
    if hasattr(estimator, "predict_proba"):
        return label, float(estimator.predict_proba(X)[0, 1]), True
    margin = float(estimator.decision_function(X)[0])
    return label, float(1 / (1 + np.exp(-margin))), False

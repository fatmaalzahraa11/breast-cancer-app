"""
OncoScan AI - Breast Cancer Wisconsin classification dashboard (Streamlit).
Covers the five project tasks: Dataset Exploration, Preprocessing, EDA,
Model Implementation (tuning) and Model Evaluation, plus a live predictor.

Run:  streamlit run app.py
"""
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as components

import ml_core as mc
from styles import CSS, hero_html

st.set_page_config(page_title="OncoScan AI | Breast Cancer Classification", page_icon="🧬",
                   layout="wide", initial_sidebar_state="expanded")
st.markdown(f"<style>{CSS}</style>", unsafe_allow_html=True)

BENIGN, MAL, ACC = "#2dd4bf", "#fb7185", "#818cf8"
MODEL_COLORS = {"KNN": "#38bdf8", "Decision Tree": "#fbbf24", "Random Forest": "#34d399",
                "ANN (MLP)": "#fb7185", "SVM": "#a78bfa"}
PRETTY = lambda s: s.replace("_", " ")
QUICK_LABEL = "Quick (about 20 s, smaller grids)"
FULL_LABEL = "Full (notebook grids, about 3 min)"


# ============================================================ helpers
def style_fig(fig, height=430):
    fig.update_layout(template="plotly_dark", height=height, paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", font=dict(family="Inter, sans-serif", size=13),
                      margin=dict(l=20, r=20, t=50, b=30), legend=dict(bgcolor="rgba(0,0,0,0)"))
    fig.update_xaxes(gridcolor="rgba(255,255,255,.07)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,.07)")
    return fig


def show(fig, height=430):
    st.plotly_chart(style_fig(fig, height), use_container_width=True)


def page_header(task, title, subtitle):
    st.markdown(f'<div class="page-head"><span class="task">{task}</span><h1>{title}</h1><p>{subtitle}</p></div>',
                unsafe_allow_html=True)


def section(title):
    st.markdown(f'<div class="sec-title">{title}</div>', unsafe_allow_html=True)


def insight(text, warn=False):
    st.markdown(f'<div class="insight {"warn" if warn else ""}">{text}</div>', unsafe_allow_html=True)


def kpi(label, value, sub="", color="#e6edf7"):
    return (f'<div class="glass kpi"><div class="label">{label}</div>'
            f'<div class="value" style="color:{color}">{value}</div><div class="sub">{sub}</div></div>')


def df_str(df):
    """Make mixed-type frames safe for st.dataframe."""
    return df.fillna("-").astype(str)


# ============================================================ cached data
@st.cache_resource(show_spinner="Loading dataset...")
def get_raw():
    return mc.load_raw()


@st.cache_resource(show_spinner="Preparing data...")
def get_prep():
    return mc.preprocess(get_raw())


def current_tuning():
    fast = st.session_state.get("mode", QUICK_LABEL) == QUICK_LABEL
    key = "tuning_quick" if fast else "tuning_full"
    if key not in st.session_state:
        t = mc.load_tuning(fast)
        if t is not None:
            st.session_state[key] = t
    return st.session_state.get(key), fast


def get_eval(tuning, fast):
    key = f"eval_{'quick' if fast else 'full'}"
    if key not in st.session_state:
        P = get_prep()
        st.session_state[key] = mc.evaluate(tuning, P["X_test"], P["y_test"])
    return st.session_state[key]


def require_training():
    tuning, fast = current_tuning()
    if tuning is None:
        st.markdown('<div class="insight warn"><b>No trained models yet.</b> Open <b>Model Training</b> in the sidebar '
                    'and press <b>Start tuning</b> (Quick mode takes about 20 seconds).</div>', unsafe_allow_html=True)
        st.stop()
    return tuning, fast


# ============================================================ sidebar
PAGES = ["🏠  Home", "🔬  Dataset Exploration", "🧹  Preprocessing", "📊  Exploratory Analysis",
         "🧠  Model Training", "🏆  Model Evaluation", "🩺  Live Prediction"]

with st.sidebar:
    st.markdown('<div class="brand"><div class="logo">🧬</div><div><div class="name">OncoScan AI</div>'
                '<div class="tag">Breast cancer classifier</div></div></div>', unsafe_allow_html=True)
    page = st.radio("Navigation", PAGES, label_visibility="collapsed")
    st.markdown("---")
    st.radio("Hyperparameter search", [QUICK_LABEL, FULL_LABEL], key="mode")
    st.markdown('<div class="side-note"><b>Positive class:</b> Malignant (1)<br><b>Split:</b> 80 / 20 stratified<br>'
                '<b>CV:</b> 5-fold stratified<br><b>Seed:</b> 42<br><br>Educational project. '
                'Not a medical device.</div>', unsafe_allow_html=True)


# ============================================================ HOME
def page_home():
    raw = get_raw()
    components.html(hero_html(len(raw), len(mc.FEATURES), len(mc.MODEL_ORDER)), height=540)

    section("🚀 Project pipeline")
    steps = [("1", "Dataset Exploration", "Structure, types, statistics, missing values, duplicates and the target distribution."),
             ("2", "Preprocessing", "Duplicates removed, 80:20 stratified split, median imputation and scaling fitted on train only."),
             ("3", "Exploratory Analysis", "Distributions, outliers, correlations and the effect of standardization."),
             ("4", "Model Implementation", "KNN, Decision Tree, Random Forest, ANN and SVM tuned with GridSearchCV."),
             ("5", "Model Evaluation", "Accuracy, Precision, Recall, F1, ROC-AUC and confusion matrices with Malignant as positive.")]
    cols = st.columns(5)
    for c, (n, t, d) in zip(cols, steps):
        c.markdown(f'<div class="glass step"><div class="num">{n}</div><h4>{t}</h4><p>{d}</p></div>', unsafe_allow_html=True)

    section("🤖 Models compared")
    st.markdown("".join(f'<span class="chip" style="border-color:{MODEL_COLORS[m]}55">'
                        f'<span class="legend-dot" style="background:{MODEL_COLORS[m]}"></span>{m}</span>'
                        for m in mc.MODEL_ORDER), unsafe_allow_html=True)

    tuning, fast = current_tuning()
    if tuning is not None:
        ev, *_ = get_eval(tuning, fast)
        b = ev.iloc[0]
        section("🏆 Current best model")
        c = st.columns(4)
        c[0].markdown(kpi("Best model", ev.index[0], "Ranked by Recall, F1, ROC-AUC", MODEL_COLORS[ev.index[0]]), unsafe_allow_html=True)
        c[1].markdown(kpi("Recall (Malignant)", f"{b['Recall']:.1%}", f"{int(b['FN'])} missed malignant tumors", MAL), unsafe_allow_html=True)
        c[2].markdown(kpi("F1-score", f"{b['F1-score']:.3f}", f"Precision {b['Precision']:.3f}", ACC), unsafe_allow_html=True)
        c[3].markdown(kpi("ROC-AUC", f"{b['ROC-AUC']:.3f}", f"Accuracy {b['Accuracy']:.1%}", BENIGN), unsafe_allow_html=True)
    else:
        insight("Start with <b>Model Training</b> to tune the five models. After that, <b>Model Evaluation</b> and "
                "<b>Live Prediction</b> unlock automatically.")


# ============================================================ TASK 1
def page_explore():
    page_header("Task 1", "Dataset Exploration",
                "Breast Cancer Wisconsin (Original) from the UCI repository: nine cytology features scored 1 to 10, "
                "labelled Benign or Malignant.")
    df = get_raw().copy()
    missing = int(df.isnull().sum().sum())
    c = st.columns(4)
    c[0].metric("Rows", df.shape[0])
    c[1].metric("Columns", df.shape[1])
    c[2].metric("Missing values", missing)
    c[3].metric("Duplicated rows", int(df.duplicated().sum()))

    t1, t2, t3, t4, t5 = st.tabs(["Preview", "Structure", "Statistics", "Missing and duplicates", "Target"])
    with t1:
        st.dataframe(df.head(25), use_container_width=True, height=420)
        insight("The raw file has <b>no header</b>, so column names were added from the dataset description. "
                "Missing values are marked with <code>?</code> and converted to <code>NaN</code> when loading.")
    with t2:
        info = pd.DataFrame({"dtype": df.dtypes.astype(str), "non-null": df.notna().sum(), "missing": df.isna().sum()})
        st.dataframe(info, use_container_width=True)
        insight("All columns are numeric. <b>Bare_Nuclei</b> is <code>float64</code> because it contains missing values. "
                "<b>Target:</b> <code>Class</code> (2 = Benign, 4 = Malignant). <b>id</b> is only an identifier and will be dropped.")
    with t3:
        st.dataframe(df[mc.FEATURES].describe().T.round(2), use_container_width=True)
        insight("All features share the same 1 to 10 scale. <b>Mitoses</b> is strongly right-skewed (most values are 1). "
                "Standardization is still needed for KNN, SVM and ANN.")
    with t4:
        a, b = st.columns(2)
        miss = df[mc.FEATURES].isnull().sum()
        fig = px.bar(x=[PRETTY(i) for i in miss.index], y=miss.values, labels={"x": "", "y": "Missing values"},
                     color=miss.values, color_continuous_scale=[[0, "#16233d"], [1, MAL]], title="Missing values per feature")
        fig.update_coloraxes(showscale=False)
        with a:
            show(fig, 380)
        with b:
            st.markdown(kpi("Fully duplicated rows", int(df.duplicated().sum()), "Identical in every column, removed in Task 2", MAL), unsafe_allow_html=True)
            st.write("")
            st.markdown(kpi("Repeated id values", int(df["id"].duplicated().sum()),
                            "Kept when the measurements differ", ACC), unsafe_allow_html=True)
        insight("All missing values are in <b>Bare_Nuclei</b> (about 2.3% of rows). Only <b>fully identical rows</b> are "
                "treated as duplicates. Repeated ids with different measurements are different records.")
    with t5:
        counts = df["Class"].map({2: "Benign", 4: "Malignant"}).value_counts()
        fig = go.Figure(go.Pie(labels=counts.index, values=counts.values, hole=.62,
                               marker=dict(colors=[BENIGN if l == "Benign" else MAL for l in counts.index]),
                               textinfo="label+percent", pull=[0, .04]))
        fig.update_layout(title="Class distribution (raw data)", showlegend=False,
                          annotations=[dict(text=f"{len(df)}<br>samples", showarrow=False, font=dict(size=22))])
        show(fig, 420)
        insight("The classes are <b>moderately imbalanced</b> (about 65% Benign, 35% Malignant), so the split is stratified "
                "and models are judged with Recall, Precision and F1, not Accuracy alone.")


# ============================================================ TASK 2
def page_preprocess():
    page_header("Task 2", "Data Preprocessing",
                "Leakage-free preparation: every statistic is learned from the training set only.")
    raw, P = get_raw(), get_prep()
    steps = [("Remove duplicates", f"{P['n_dup']} fully duplicated rows removed (before splitting)"),
             ("Drop identifier", "The id column carries no medical information"),
             ("Encode target", "Benign = 0, Malignant = 1 (positive class)"),
             ("Stratified split", f"{len(P['X_train'])} train / {len(P['X_test'])} test (80:20)"),
             ("Median imputation", f"Bare_Nuclei median from train = {int(P['imputer'].statistics_[mc.FEATURES.index('Bare_Nuclei')])}"),
             ("Standardization", "Mean and std learned from the training set"),
             ("Leakage checks", "Verified below")]
    cols = st.columns(4)
    for i, (t, d) in enumerate(steps):
        cols[i % 4].markdown(f'<div class="glass step" style="margin-bottom:14px"><div class="num">{i + 1}</div>'
                             f'<h4>{t}</h4><p>{d}</p></div>', unsafe_allow_html=True)

    section("📦 Data flow")
    flow = pd.DataFrame({"Step": ["Raw data", "After removing duplicates", "After dropping id", "Train set", "Test set"],
                         "Rows": [len(raw), len(P["df"]), len(P["df"]), len(P["X_train"]), len(P["X_test"])],
                         "Columns": [raw.shape[1], raw.shape[1], P["df"].shape[1], P["X_train"].shape[1], P["X_test"].shape[1]]})
    a, b = st.columns([1, 1])
    with a:
        st.dataframe(flow, use_container_width=True, hide_index=True)
        split = pd.DataFrame({"Set": ["Train", "Test"], "Rows": [len(P["y_train"]), len(P["y_test"])],
                              "Malignant (%)": [round(P["y_train"].mean() * 100, 2), round(P["y_test"].mean() * 100, 2)]})
        st.dataframe(split, use_container_width=True, hide_index=True)
    with b:
        fig = go.Figure(go.Pie(labels=["Train", "Test"], values=[len(P["X_train"]), len(P["X_test"])], hole=.6,
                               marker=dict(colors=[ACC, BENIGN]), textinfo="label+percent"))
        fig.update_layout(title="80:20 stratified split", showlegend=False)
        show(fig, 340)
    insight("<code>stratify=y</code> keeps the malignant ratio almost identical in both sets, and "
            "<code>random_state=42</code> makes the split reproducible.")

    section("🛡️ Data leakage checks")
    c1 = bool(np.allclose(P["scaler"].mean_, P["X_train_imp"].mean().values))
    c2 = bool(np.allclose(P["imputer"].statistics_, P["X_train"].median().values))
    c3 = bool(P["X_train_scaled"].isnull().sum().sum() == 0 and P["X_test_scaled"].isnull().sum().sum() == 0)
    c4 = len(P["X_train_scaled"]) == len(P["y_train"]) and len(P["X_test_scaled"]) == len(P["y_test"])
    cols = st.columns(4)
    for c, (ok, txt) in zip(cols, [(c1, "Scaler fitted on train only"), (c2, "Imputer fitted on train only"),
                                   (c3, "No missing values left"), (c4, "Shapes are consistent")]):
        c.markdown(f'<div class="glass check"><div class="ok {"" if ok else "bad"}">{"✓" if ok else "✕"}</div>'
                   f'<div><b>{txt}</b></div></div>', unsafe_allow_html=True)

    section("📐 Effect of standardization")
    feat = st.selectbox("Feature", mc.FEATURES, format_func=PRETTY)
    a, b = st.columns(2)
    with a:
        fig = px.histogram(P["X_train_imp"], x=feat, nbins=10, title="Before (imputed)", color_discrete_sequence=[ACC])
        show(fig, 340)
    with b:
        fig = px.histogram(P["X_train_scaled"], x=feat, nbins=10, title="After (standardized)", color_discrete_sequence=[BENIGN])
        show(fig, 340)
    stats = pd.DataFrame({"train mean": P["X_train_scaled"].mean().round(3), "train std": P["X_train_scaled"].std(ddof=0).round(3),
                          "test mean": P["X_test_scaled"].mean().round(3), "test std": P["X_test_scaled"].std(ddof=0).round(3)})
    st.dataframe(stats, use_container_width=True)
    insight("Training features have mean 0 and std 1. Test features are close but not exact, which is correct: the test set "
            "is transformed with the training statistics, exactly like new, unseen patients.")


# ============================================================ TASK 3
def page_eda():
    page_header("Task 3", "Exploratory Data Analysis",
                "Distributions, outliers, relationships between features and the effect of scaling.")
    raw, P = get_raw(), get_prep()
    d = P["df"].copy()
    d["Diagnosis"] = d["Class"].map({2: "Benign", 4: "Malignant"})
    cmap = {"Benign": BENIGN, "Malignant": MAL}

    t1, t2, t3, t4, t5 = st.tabs(["Class balance", "Distributions", "Outliers", "Correlation", "Before / after scaling"])
    with t1:
        counts = d["Diagnosis"].value_counts().reset_index()
        counts.columns = ["Diagnosis", "Samples"]
        fig = px.bar(counts, x="Diagnosis", y="Samples", color="Diagnosis", color_discrete_map=cmap, text="Samples")
        fig.update_traces(textposition="outside")
        show(fig, 420)
        insight("After cleaning, the dataset still has about twice as many benign as malignant samples. "
                "The imbalance is moderate, so no oversampling is used.")
    with t2:
        feat = st.selectbox("Feature", mc.FEATURES, format_func=PRETTY, key="eda_f")
        fig = px.histogram(d, x=feat, color="Diagnosis", barmode="overlay", nbins=10, opacity=.78, color_discrete_map=cmap)
        show(fig, 400)
        long = d.melt(id_vars="Diagnosis", value_vars=mc.FEATURES)
        long["variable"] = long["variable"].map(PRETTY)
        fig = px.histogram(long, x="value", color="Diagnosis", facet_col="variable", facet_col_wrap=3, nbins=10,
                           barmode="overlay", opacity=.75, color_discrete_map=cmap, height=760)
        fig.for_each_annotation(lambda a: a.update(text=a.text.split("=")[-1]))
        show(fig, 760)
        insight("Malignant cases concentrate at <b>high values</b> of cell size, cell shape, bare nuclei and chromatin, "
                "while benign cases are concentrated near 1. This is why most models separate the classes so well.")
    with t3:
        long = d.melt(id_vars="Diagnosis", value_vars=mc.FEATURES)
        long["variable"] = long["variable"].map(PRETTY)
        fig = px.box(long, x="variable", y="value", color="Diagnosis", color_discrete_map=cmap, points="outliers")
        fig.update_xaxes(title="", tickangle=-25)
        show(fig, 520)
        insight("Points outside the whiskers are potential outliers. <b>Mitoses</b> has many of them in the malignant class, "
                "but they are valid ordinal scores, so no rows are removed.")
    with t4:
        corr = d[mc.FEATURES].corr().round(2)
        corr.index = [PRETTY(i) for i in corr.index]
        corr.columns = [PRETTY(i) for i in corr.columns]
        fig = px.imshow(corr, text_auto=True, color_continuous_scale="RdBu_r", zmin=-1, zmax=1, aspect="auto")
        show(fig, 640)
        insight("<b>Uniformity of cell size</b> and <b>cell shape</b> are very strongly correlated, so they carry overlapping "
                "information. Tree-based models and regularized models handle this well.")
    with t5:
        a, b = st.columns(2)
        for col, data, title in [(a, P["X_train_imp"], "Before standardization"), (b, P["X_train_scaled"], "After standardization")]:
            long = data.melt()
            long["variable"] = long["variable"].map(PRETTY)
            fig = px.box(long, x="variable", y="value", title=title, color_discrete_sequence=[ACC])
            fig.update_xaxes(title="", tickangle=-45)
            with col:
                show(fig, 460)
        insight("After standardization every feature is centered at zero with unit variance. This matters for "
                "distance-based and gradient-based algorithms: KNN, SVM and ANN.")


# ============================================================ TASK 4
def page_training():
    page_header("Task 4", "Model Implementation",
                "Five scikit-learn pipelines tuned with GridSearchCV and 5-fold stratified cross-validation on the "
                "training set only.")
    P = get_prep()
    tuning, fast = current_tuning()
    sizes = mc.grid_sizes(fast)

    c = st.columns(5)
    for col, m in zip(c, mc.MODEL_ORDER):
        col.markdown(kpi(m, sizes[m], "combinations x 5 folds", MODEL_COLORS[m]), unsafe_allow_html=True)
    insight("Every model is a <code>Pipeline</code> (median imputer, then scaler for KNN/SVM/ANN, then the model) fed with the "
            "<b>raw</b> training data, so preprocessing is re-fitted inside every CV fold. The best configuration is the one "
            "with the highest mean CV <b>F1-score of the malignant class</b>.")

    st.write("")
    run = st.button("⚡ Start tuning" if tuning is None else "🔄 Re-run tuning", type="primary")
    if run:
        bar = st.progress(0.0)
        status = st.empty()

        def cb(i, n, name, state):
            bar.progress(i / n)
            icon = "⏳" if state == "start" else "✅"
            status.markdown(f"{icon} **{name}** ({i if state == 'done' else i + 1}/{n})")

        result = mc.tune_all(P["X_train"], P["y_train"], fast=fast, progress=cb)
        mc.save_tuning(result, fast)
        key = "tuning_quick" if fast else "tuning_full"
        st.session_state[key] = result
        st.session_state.pop(f"eval_{'quick' if fast else 'full'}", None)
        bar.progress(1.0)
        status.success("Tuning finished. Open Model Evaluation to see the test-set results.")
        st.balloons()
        tuning = result

    if tuning is None:
        return
    models = tuning["models"]

    section("🎯 Best hyperparameters")
    bp = pd.DataFrame({n: models[n]["best_params"] for n in mc.MODEL_ORDER}).T
    st.dataframe(df_str(bp), use_container_width=True)

    section("📈 Cross-validation performance (mean ± std, 5 folds)")
    table = pd.DataFrame({n: {lbl: f"{models[n]['cv'][m][0]:.4f} ± {models[n]['cv'][m][1]:.4f}"
                              for m, lbl in zip(mc.SCORING, ["Accuracy", "Precision", "Recall", "F1-score", "ROC-AUC"])}
                          for n in mc.MODEL_ORDER}).T
    st.dataframe(table, use_container_width=True)

    a, b = st.columns(2)
    for col, metric, title in [(a, "f1", "Mean CV F1-score"), (b, "recall", "Mean CV Recall (Malignant)")]:
        fig = go.Figure()
        for n in mc.MODEL_ORDER:
            m, s = models[n]["cv"][metric]
            fig.add_trace(go.Bar(x=[n], y=[m], error_y=dict(type="data", array=[s]), marker_color=MODEL_COLORS[n],
                                 name=n, text=f"{m:.3f}", textposition="outside", showlegend=False))
        fig.update_layout(title=title, yaxis=dict(range=[0.88, 1.04]))
        with col:
            show(fig, 400)

    section("🔍 Top configurations per model")
    pick = st.selectbox("Model", mc.MODEL_ORDER)
    top = pd.DataFrame([{"Rank": i + 1, "CV F1": round(t["f1"], 4), "CV Recall": round(t["recall"], 4),
                         "Params": str(t["params"])} for i, t in enumerate(models[pick]["top"])])
    st.dataframe(top, use_container_width=True, hide_index=True)
    st.caption(f"Tuning time for {pick}: {models[pick]['seconds']:.1f} s")
    insight("Several configurations often tie. That means the model is <b>not sensitive</b> to the exact hyperparameters, "
            "so the result does not depend on a lucky choice.")


# ============================================================ TASK 5
def page_evaluation():
    page_header("Task 5", "Model Evaluation",
                "Final test-set results with Malignant as the positive class. The test set is used once, after tuning.")
    P = get_prep()
    tuning, fast = require_training()
    ev, preds, scores, rocs = get_eval(tuning, fast)
    n_mal, n_ben = int(P["y_test"].sum()), int((P["y_test"] == 0).sum())
    best = ev.index[0]
    b = ev.iloc[0]

    c = st.columns(4)
    c[0].markdown(kpi("Best model", best, f"{len(P['y_test'])} test samples ({n_mal} malignant)", MODEL_COLORS[best]), unsafe_allow_html=True)
    c[1].markdown(kpi("Recall", f"{b['Recall']:.1%}", f"{int(b['FN'])} of {n_mal} malignant missed", MAL), unsafe_allow_html=True)
    c[2].markdown(kpi("F1-score", f"{b['F1-score']:.3f}", f"Precision {b['Precision']:.3f}", ACC), unsafe_allow_html=True)
    c[3].markdown(kpi("ROC-AUC", f"{b['ROC-AUC']:.3f}", f"Accuracy {b['Accuracy']:.1%}", BENIGN), unsafe_allow_html=True)
    st.write("")

    t1, t2, t3, t4, t5 = st.tabs(["Metrics table", "Confusion matrices", "ROC curves", "Comparison charts", "Best model"])
    metric_cols = ["Accuracy", "Precision", "Recall", "F1-score", "ROC-AUC"]

    with t1:
        show_df = ev[["Rank"] + metric_cols + ["TN", "FP", "FN", "TP"]]
        styler = (show_df.style.format({m: "{:.4f}" for m in metric_cols})
                  .highlight_max(subset=metric_cols, color="#115e59")
                  .highlight_min(subset=["FN", "FP"], color="#115e59"))
        st.dataframe(styler, use_container_width=True)
        insight("<b>Recall</b> is the most important metric here: a false negative is a missed cancer. Models are ranked by "
                "<b>Recall, then F1-score, then ROC-AUC</b>. Green cells mark the best value in each column.")
        with st.expander("Metric definitions"):
            st.markdown("- **Accuracy:** share of correct predictions (can look good even when cancers are missed).\n"
                        "- **Precision:** of tumors predicted malignant, how many really are.\n"
                        "- **Recall:** of truly malignant tumors, how many are found.\n"
                        "- **F1-score:** harmonic mean of Precision and Recall.\n"
                        "- **ROC-AUC:** how well the score separates the classes over all thresholds.")
    with t2:
        order = list(ev.index)
        for row in [order[:3], order[3:]]:
            cols = st.columns(3)
            for col, name in zip(cols, row):
                r = ev.loc[name]
                z = [[int(r["TN"]), int(r["FP"])], [int(r["FN"]), int(r["TP"])]]
                fig = px.imshow(z, x=["Pred. Benign", "Pred. Malignant"], y=["True Benign", "True Malignant"],
                                text_auto=True, color_continuous_scale=[[0, "#0e1a30"], [1, MODEL_COLORS[name]]])
                fig.update_coloraxes(showscale=False)
                fig.update_traces(textfont=dict(size=26))
                fig.update_layout(title=f"{name}: FN {int(r['FN'])} | FP {int(r['FP'])}")
                with col:
                    show(fig, 360)
        insight("The most serious error is a <b>False Negative</b> (malignant predicted as benign). "
                "Look at the bottom-left cell of each matrix.")
    with t3:
        zoom = st.toggle("Zoom on the top-left corner", value=False)
        fig = go.Figure()
        for name, (fpr, tpr) in rocs.items():
            fig.add_trace(go.Scatter(x=fpr, y=tpr, mode="lines", line=dict(width=3, color=MODEL_COLORS[name]),
                                     name=f"{name} (AUC {ev.loc[name, 'ROC-AUC']:.3f})"))
        fig.add_trace(go.Scatter(x=[0, 1], y=[0, 1], mode="lines", line=dict(dash="dash", color="#64748b"), name="Random guess"))
        fig.update_layout(xaxis_title="False Positive Rate", yaxis_title="True Positive Rate (Recall of Malignant)")
        if zoom:
            fig.update_xaxes(range=[-0.005, 0.15])
            fig.update_yaxes(range=[0.75, 1.01])
        show(fig, 520)
        insight("All curves hug the top-left corner. Differences between the top models are tiny; the Decision Tree and KNN "
                "reach 100% Recall only at a higher false positive rate.")
    with t4:
        long = ev[metric_cols].reset_index().melt(id_vars="Model", var_name="Metric", value_name="Score")
        fig = px.bar(long, x="Metric", y="Score", color="Model", barmode="group", color_discrete_map=MODEL_COLORS)
        fig.update_yaxes(range=[0.85, 1.0])
        show(fig, 460)
        radar = go.Figure()
        for name in ev.index:
            vals = [float(ev.loc[name, m]) for m in metric_cols]
            radar.add_trace(go.Scatterpolar(r=vals + vals[:1], theta=metric_cols + metric_cols[:1], name=name,
                                            line=dict(color=MODEL_COLORS[name], width=3), fill="toself", opacity=.35))
        radar.update_layout(polar=dict(radialaxis=dict(range=[0.85, 1.0], gridcolor="rgba(255,255,255,.12)"),
                                       bgcolor="rgba(0,0,0,0)"), title="Radar view (axis starts at 0.85)")
        show(radar, 520)
    with t5:
        s = ev.iloc[1]
        gap = float(b["F1 gap (CV - test)"])
        st.markdown(f'<div class="result benign" style="margin-bottom:18px"><div class="big" style="color:{MODEL_COLORS[best]}">'
                    f'🏆 {best}</div><div class="small">Selected by the rule: Recall, then F1-score, then ROC-AUC</div></div>',
                    unsafe_allow_html=True)
        cmp = ev[["Rank", "Recall", "F1-score", "ROC-AUC", "FN", "FP", "CV F1", "F1 gap (CV - test)"]]
        st.dataframe(cmp.style.format({c: "{:.4f}" for c in ["Recall", "F1-score", "ROC-AUC", "CV F1", "F1 gap (CV - test)"]}),
                     use_container_width=True)
        st.markdown(f"""
**Why {best}?**
1. **Recall on the most important class:** {b['Recall']:.1%}, only **{int(b['FN'])} of {n_mal}** malignant tumors missed
   (next best, {ev.index[1]}: {int(s['FN'])} missed).
2. **F1-score {b['F1-score']:.3f}** and **Accuracy {b['Accuracy']:.1%}**, with ROC-AUC {b['ROC-AUC']:.3f}.
3. **Consistency:** CV F1 {b['CV F1']:.3f} vs test F1 {b['F1-score']:.3f} (gap {gap:+.3f}), so the test result is not a lucky split.
""")
        insight(f"<b>Limitations:</b> the test set has only <b>{n_mal} malignant cases</b>, so one patient changes Recall by "
                f"about {100 / n_mal:.1f} percentage points. The top models can be statistically close, and the "
                f"Decision Tree is usually the only clearly weaker one. In practice the decision threshold could be lowered "
                f"to reduce false negatives, and the model should be validated on larger, independent data.", warn=True)


# ============================================================ LIVE PREDICTION
def _load_case(kind):
    P = get_prep()
    mask = P["y_train"] == (1 if kind == "malignant" else 0)
    med = P["X_train_imp"][mask].median()
    for f in mc.FEATURES:
        st.session_state[f"s_{f}"] = int(round(float(med[f])))


def page_predict():
    page_header("Live predictor", "Try a Prediction",
                "Set the nine cell characteristics (1 to 10) and see what each trained model says. "
                "Educational demo only, not a medical device.")
    P = get_prep()
    tuning, fast = require_training()
    ev, *_ = get_eval(tuning, fast)
    names = [n for n in mc.MODEL_ORDER if n in tuning["models"]]

    for f, v in zip(mc.FEATURES, P["imputer"].statistics_):
        st.session_state.setdefault(f"s_{f}", int(v))

    top = st.columns([2, 1, 1])
    choice = top[0].selectbox("Model", names, index=names.index(ev.index[0]),
                              help="Defaults to the best model from the evaluation.")
    top[1].button("Load typical benign case", on_click=_load_case, args=("benign",), use_container_width=True)
    top[2].button("Load typical malignant case", on_click=_load_case, args=("malignant",), use_container_width=True)

    left, right = st.columns([1.15, 1])
    with left:
        section("🎛️ Cell characteristics")
        values = {}
        sc = st.columns(3)
        for i, f in enumerate(mc.FEATURES):
            values[f] = sc[i % 3].slider(PRETTY(f), 1, 10, key=f"s_{f}")

    label, score, is_prob = mc.predict_one(tuning["models"][choice]["estimator"], values)
    with right:
        section("🧪 Result")
        cls = "malignant" if label == 1 else "benign"
        title = "Malignant" if label == 1 else "Benign"
        color = MAL if label == 1 else BENIGN
        st.markdown(f'<div class="result {cls}"><div class="big" style="color:{color}">{title}</div>'
                    f'<div class="small">Predicted by {choice}</div></div>', unsafe_allow_html=True)
        gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=round(score * 100, 1), number=dict(suffix="%", font=dict(size=46)),
            title=dict(text="Malignancy probability" if is_prob else "Malignancy score (from SVM margin)"),
            gauge=dict(axis=dict(range=[0, 100]), bar=dict(color=color), bgcolor="rgba(255,255,255,.04)",
                       steps=[dict(range=[0, 50], color="rgba(45,212,191,.18)"), dict(range=[50, 100], color="rgba(251,113,133,.18)")],
                       threshold=dict(line=dict(color="#e6edf7", width=3), value=50))))
        show(gauge, 330)

    section("🗳️ What every model says")
    rows = []
    for n in names:
        l, s, p = mc.predict_one(tuning["models"][n]["estimator"], values)
        rows.append({"Model": n, "Prediction": "Malignant" if l == 1 else "Benign", "Malignancy score": s})
    vote = pd.DataFrame(rows)
    n_mal = int((vote["Prediction"] == "Malignant").sum())
    a, b = st.columns([1, 1.3])
    with a:
        st.dataframe(vote.style.format({"Malignancy score": "{:.1%}"}), use_container_width=True, hide_index=True)
        insight(f"<b>{n_mal} of {len(vote)}</b> models predict <b>Malignant</b>. The SVM score is a transformed margin, "
                f"not a calibrated probability.")
    with b:
        fig = px.bar(vote, x="Malignancy score", y="Model", orientation="h", color="Prediction",
                     color_discrete_map={"Malignant": MAL, "Benign": BENIGN}, range_x=[0, 1])
        show(fig, 320)


# ============================================================ router
try:
    {PAGES[0]: page_home, PAGES[1]: page_explore, PAGES[2]: page_preprocess, PAGES[3]: page_eda,
     PAGES[4]: page_training, PAGES[5]: page_evaluation, PAGES[6]: page_predict}[page]()
except FileNotFoundError as e:
    st.error(str(e))
    st.info("Copy the UCI zip file (for example `breast_cancer_wisconsin_original.zip`) into the `data` folder.")

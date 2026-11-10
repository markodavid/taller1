"""Gráficas y artefactos de reporte (CRISP-DM: evaluación y comunicación de resultados)."""

from __future__ import annotations

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import ConfusionMatrixDisplay

from taller1.config import PHASE_EVAL_DIR, PREDICTIONS_FILE
from taller1.modeling import EvaluationResult

FIGURE_DPI = 150


def set_headless_backend() -> None:
    """Fuerza el backend ``Agg`` para ejecuciones sin pantalla (CLI, CI)."""
    matplotlib.use("Agg", force=True)


def _finish(fig: plt.Figure, save_path: Path | None) -> plt.Figure:
    fig.tight_layout()
    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=FIGURE_DPI, bbox_inches="tight")
    return fig


def plot_class_distribution(counts: pd.Series, save_path: Path | None = None) -> plt.Figure:
    """Gráfico de barras con la distribución de clases del dataset."""
    fig, ax = plt.subplots(figsize=(8, 4.5))
    counts.plot(kind="bar", ax=ax, color="#4C72B0", edgecolor="white")
    ax.set_title("Distribución de clases - Dry Bean")
    ax.set_xlabel("Variedad de frijol")
    ax.set_ylabel("Cantidad de registros")
    ax.tick_params(axis="x", rotation=45)
    for index, value in enumerate(counts.to_numpy()):
        ax.text(index, value, str(value), ha="center", va="bottom", fontsize=8)
    return _finish(fig, save_path)


def plot_confusion_matrix(result: EvaluationResult, save_path: Path | None = None) -> plt.Figure:
    """Matriz de confusión con etiquetas legibles."""
    fig, ax = plt.subplots(figsize=(7.5, 6))
    display = ConfusionMatrixDisplay(
        confusion_matrix=result.confusion, display_labels=result.labels
    )
    display.plot(ax=ax, cmap="Blues", colorbar=False, values_format="d")
    ax.set_title(f"Matriz de confusión - {result.name}")
    ax.tick_params(axis="x", rotation=45)
    return _finish(fig, save_path)


def plot_feature_importance(
    importance: pd.DataFrame, top_n: int = 10, save_path: Path | None = None
) -> plt.Figure:
    """Top-N variables más importantes según el bosque aleatorio."""
    top = importance.head(top_n).iloc[::-1]
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(top["feature"], top["importance"], color="#55A868")
    ax.set_title(f"Top {top_n} variables más importantes - Random Forest")
    ax.set_xlabel("Importancia (Gini)")
    ax.set_ylabel("Variable")
    return _finish(fig, save_path)


def plot_model_comparison(comparison: pd.DataFrame, save_path: Path | None = None) -> plt.Figure:
    """Comparación de accuracy y F1 macro entre modelos."""
    fig, ax = plt.subplots(figsize=(7, 4))
    comparison.set_index("modelo")[["accuracy", "f1_macro"]].plot(
        kind="bar", ax=ax, color=["#4C72B0", "#DD8452"], edgecolor="white"
    )
    ax.set_title("Comparación de modelos")
    ax.set_xlabel("Modelo")
    ax.set_ylabel("Puntaje")
    ax.set_ylim(0, 1.05)
    ax.tick_params(axis="x", rotation=0)
    ax.legend(["Accuracy", "F1 macro"])
    for container in ax.containers:
        ax.bar_label(container, fmt="%.3f", fontsize=8, padding=2)
    return _finish(fig, save_path)


def save_metrics_table(comparison: pd.DataFrame, path: Path) -> Path:
    """Guarda la tabla comparativa de métricas en CSV."""
    path.parent.mkdir(parents=True, exist_ok=True)
    comparison.to_csv(path, index=False)
    return path


def save_classification_reports(
    results: list[EvaluationResult], reports_dir: Path | None = None
) -> list[Path]:
    """Escribe un ``classification_report`` en texto por cada modelo evaluado."""
    reports_dir = reports_dir or PHASE_EVAL_DIR
    reports_dir.mkdir(parents=True, exist_ok=True)
    paths: list[Path] = []
    for result in results:
        slug = result.name.lower().replace(" ", "_")
        path = reports_dir / f"classification_report_{slug}.txt"
        path.write_text(result.report, encoding="utf-8", newline="\n")
        paths.append(path)
    return paths


def save_predictions(
    X_test: pd.DataFrame,
    y_test: pd.Series,
    y_pred: pd.Series | pd.Index | list[str],
    path: Path | None = None,
) -> Path:
    """Exporta las predicciones junto con la clase real (extensión opcional C)."""
    path = path or PREDICTIONS_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    predictions = X_test.copy()
    predictions["real_class"] = y_test.to_numpy()
    predictions["predicted_class"] = pd.Series(list(y_pred)).to_numpy()
    predictions.to_csv(path, index=False)
    return path

"""Entrenamiento, evaluación y persistencia de modelos (CRISP-DM: modelado y evaluación)."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.base import ClassifierMixin
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from taller1.config import RANDOM_STATE


@dataclass
class EvaluationResult:
    """Resultado reproducible de evaluar un modelo sobre el conjunto de prueba."""

    name: str
    accuracy: float
    f1_macro: float
    f1_weighted: float
    precision_macro: float
    recall_macro: float
    report: str
    report_dict: dict[str, object]
    labels: list[str] = field(default_factory=list)
    confusion: np.ndarray = field(default_factory=lambda: np.empty((0, 0)))
    y_pred: np.ndarray = field(default_factory=lambda: np.empty(0, dtype=object))

    def as_row(self) -> dict[str, object]:
        """Fila lista para la tabla comparativa de modelos."""
        return {
            "modelo": self.name,
            "accuracy": round(self.accuracy, 4),
            "f1_macro": round(self.f1_macro, 4),
            "f1_weighted": round(self.f1_weighted, 4),
            "precision_macro": round(self.precision_macro, 4),
            "recall_macro": round(self.recall_macro, 4),
        }


def build_baseline_model() -> Pipeline:
    """Baseline: estandarización + regresión logística multinomial."""
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(max_iter=1000, random_state=RANDOM_STATE),
            ),
        ]
    )


def build_random_forest(n_estimators: int = 200) -> RandomForestClassifier:
    """Modelo alternativo: bosque aleatorio con pesos balanceados por clase."""
    return RandomForestClassifier(
        n_estimators=n_estimators,
        class_weight="balanced",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )


def train_model(model: ClassifierMixin, X_train: pd.DataFrame, y_train: pd.Series):
    """Ajusta el modelo y lo devuelve (scikit-learn sigue el patrón ``fit`` → ``self``)."""
    return model.fit(X_train, y_train)


def evaluate_model(
    model: ClassifierMixin,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    name: str,
) -> EvaluationResult:
    """Calcula accuracy, F1 macro, métricas por clase y matriz de confusión."""
    y_pred = np.asarray(model.predict(X_test))
    labels = sorted(pd.unique(y_test.astype(str)))
    report_dict = classification_report(y_test, y_pred, output_dict=True, zero_division=0)
    return EvaluationResult(
        name=name,
        accuracy=float(accuracy_score(y_test, y_pred)),
        f1_macro=float(f1_score(y_test, y_pred, average="macro", zero_division=0)),
        f1_weighted=float(f1_score(y_test, y_pred, average="weighted", zero_division=0)),
        precision_macro=float(precision_score(y_test, y_pred, average="macro", zero_division=0)),
        recall_macro=float(recall_score(y_test, y_pred, average="macro", zero_division=0)),
        report=classification_report(y_test, y_pred, zero_division=0),
        report_dict=report_dict,
        labels=labels,
        confusion=confusion_matrix(y_test, y_pred, labels=labels),
        y_pred=y_pred,
    )


def compare_models(results: list[EvaluationResult]) -> pd.DataFrame:
    """Construye la tabla comparativa ordenada por F1 macro (criterio de selección)."""
    table = pd.DataFrame([result.as_row() for result in results])
    return table.sort_values("f1_macro", ascending=False).reset_index(drop=True)


def feature_importance(model: ClassifierMixin, feature_names: list[str]) -> pd.DataFrame:
    """Extrae la importancia de variables del bosque aleatorio, ordenada."""
    importances = getattr(model, "feature_importances_", None)
    if importances is None:
        raise ValueError("El modelo no expone 'feature_importances_'")
    table = pd.DataFrame({"feature": feature_names, "importance": importances})
    return table.sort_values("importance", ascending=False).reset_index(drop=True)


def save_model(model: ClassifierMixin, path: Path) -> Path:
    """Serializa el modelo entrenado con joblib (artefacto reproducible)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, path)
    return path


def load_model(path: Path) -> ClassifierMixin:
    """Carga un modelo previamente serializado con joblib."""
    return joblib.load(path)


def predict_bean_class(model: ClassifierMixin, input_data: pd.DataFrame) -> str:
    """Mini despliegue: predice la variedad de frijol para una o varias filas."""
    prediction = model.predict(input_data)
    return str(prediction[0])

"""Punto de entrada reproducible del laboratorio: ``taller1`` (o ``make pipeline``).

Ejecuta el flujo completo de CRISP-DM sobre el Dry Bean Dataset y deja la evidencia de cada fase
en su carpeta: ``01_comprension_negocio`` … ``06_despliegue``.
"""

from __future__ import annotations

import argparse
import json
import platform
import time
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd

import taller1
from taller1 import data, features, modeling, reporting
from taller1.config import (
    CLASS_PLOT_FILE,
    DEMO_PREDICTION_FILE,
    FINAL_MODEL_FILE,
    METRICS_FILE,
    PHASE_DEPLOY_DIR,
    PHASE_EVAL_DIR,
    PHASE_MODEL_DIR,
    PREDICTIONS_FILE,
    RANDOM_STATE,
    SUMMARY_FILE,
    TEST_SIZE,
    ensure_directories,
)


def run_pipeline(verbose: bool = True) -> dict[str, object]:
    """Ejecuta el pipeline completo y devuelve el resumen de la corrida."""
    reporting.set_headless_backend()
    ensure_directories()
    started = time.perf_counter()

    # 1. Comprensión de datos (bronce → plata) -------------------------------
    raw = data.load_raw_dataset()
    quality_raw = data.data_quality_summary(raw)

    # 2. Preparación: limpieza de duplicados --------------------------------
    clean, removed = data.remove_duplicates(raw)
    quality_clean = data.data_quality_summary(clean)
    data.save_processed(clean)
    manifest = data.build_manifest(clean)
    data.save_manifest(manifest)

    # 3. Separación train/test y capa oro -----------------------------------
    X, y = features.split_features_target(clean)
    X_train, X_test, y_train, y_test = features.split_train_test(X, y)
    data.save_splits(X_train, X_test, y_train, y_test)

    partition = {
        "train": len(X_train),
        "test": len(X_test),
        "test_size": TEST_SIZE,
        "random_state": RANDOM_STATE,
    }
    data.save_profile(
        {
            "crudo": quality_raw,
            "limpio": quality_clean,
            "duplicados_eliminados": removed,
            "particion": partition,
        }
    )

    # 4. Modelado: baseline y modelo alternativo -----------------------------
    baseline = modeling.train_model(modeling.build_baseline_model(), X_train, y_train)
    result_baseline = modeling.evaluate_model(baseline, X_test, y_test, "Logistic Regression")

    forest = modeling.train_model(modeling.build_random_forest(), X_train, y_train)
    result_forest = modeling.evaluate_model(forest, X_test, y_test, "Random Forest")

    # 5. Evaluación y comparación -------------------------------------------
    comparison = modeling.compare_models([result_baseline, result_forest])
    modeling.save_model(baseline, PHASE_MODEL_DIR / "logistic_regression_drybean.joblib")
    modeling.save_model(forest, FINAL_MODEL_FILE)

    reporting.save_metrics_table(comparison, METRICS_FILE)
    reporting.save_classification_reports([result_baseline, result_forest], PHASE_EVAL_DIR)
    reporting.save_predictions(X_test, y_test, result_forest.y_pred, PREDICTIONS_FILE)

    # 6. Gráficas ------------------------------------------------------------
    reporting.plot_class_distribution(data.class_distribution(clean), CLASS_PLOT_FILE)
    reporting.plot_model_comparison(comparison, PHASE_EVAL_DIR / "comparacion_modelos.png")
    reporting.plot_confusion_matrix(
        result_forest, PHASE_EVAL_DIR / "matriz_confusion_random_forest.png"
    )
    reporting.plot_confusion_matrix(
        result_baseline, PHASE_EVAL_DIR / "matriz_confusion_logistic_regression.png"
    )
    importance = modeling.feature_importance(forest, list(X.columns))
    reporting.plot_feature_importance(importance, 10, PHASE_EVAL_DIR / "importancia_variables.png")
    importance.to_csv(PHASE_EVAL_DIR / "importancia_variables.csv", index=False)

    # 7. Despliegue: verificación de carga del artefacto ---------------------
    loaded = modeling.load_model(FINAL_MODEL_FILE)
    sample = X_test.iloc[[0]]
    sample_prediction = modeling.predict_bean_class(loaded, sample)
    demo = {
        "modelo": str(FINAL_MODEL_FILE.relative_to(FINAL_MODEL_FILE.parents[1])),
        "entrada": {key: float(value) for key, value in sample.iloc[0].items()},
        "prediccion": sample_prediction,
        "clase_real": str(y_test.iloc[0]),
    }
    (PHASE_DEPLOY_DIR / "ejemplo_prediccion.json").write_text(
        json.dumps(demo, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n"
    )

    summary: dict[str, object] = {
        "timestamp": datetime.now(UTC).isoformat(timespec="seconds"),
        "duracion_segundos": round(time.perf_counter() - started, 2),
        "dataset": manifest,
        "calidad_datos": {"crudo": quality_raw, "limpio": quality_clean},
        "duplicados_eliminados": removed,
        "particion": partition,
        "metricas": comparison.to_dict(orient="records"),
        "mejor_modelo": str(comparison.iloc[0]["modelo"]),
        "verificacion_despliegue": {
            "muestra_predicha": sample_prediction,
            "clase_real": str(y_test.iloc[0]),
        },
        "entorno": {
            "python": platform.python_version(),
            "pandas": pd.__version__,
            "scikit_learn": sklearn_version(),
            "taller1": taller1.__version__,
        },
    }
    SUMMARY_FILE.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    if verbose:
        _print_summary(summary, comparison)
    return summary


def sklearn_version() -> str:
    """Versión instalada de scikit-learn (trazabilidad TDSP)."""
    import sklearn

    return sklearn.__version__


def _print_summary(summary: dict[str, object], comparison: pd.DataFrame) -> None:
    dataset = summary["dataset"]
    partition = summary["particion"]
    print(f"Dataset: {dataset['filas']} filas x {dataset['columnas']} columnas")
    print(f"Clases: {', '.join(dataset['clases'])}")
    print(f"Train/test: {partition['train']}/{partition['test']} registros")
    print("\nComparación de modelos:")
    print(comparison.to_string(index=False))
    print(f"\nMejor modelo por F1 macro: {summary['mejor_modelo']}")
    print(f"Modelo guardado en: {FINAL_MODEL_FILE.relative_to(FINAL_MODEL_FILE.parents[1])}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="taller1",
        description="Laboratorio Dry Bean: CRISP-DM + TDSP + Scrum ML.",
    )
    subparsers = parser.add_subparsers(dest="command")

    pipeline = subparsers.add_parser("pipeline", help="Ejecuta el flujo completo")
    pipeline.add_argument("--quiet", action="store_true", help="No imprime el resumen")

    predict = subparsers.add_parser("predict", help="Predice variedades desde un CSV")
    predict.add_argument("--input", type=Path, required=True, help="CSV con las 16 variables")
    predict.add_argument("--output", type=Path, help="CSV de salida con la predicción")
    predict.add_argument("--model", type=Path, default=FINAL_MODEL_FILE, help="Modelo .joblib")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "predict":
        model = modeling.load_model(args.model)
        rows = pd.read_csv(args.input)
        predictions = model.predict(rows)
        result = rows.copy()
        result["predicted_class"] = predictions
        destination = args.output or DEMO_PREDICTION_FILE
        destination.parent.mkdir(parents=True, exist_ok=True)
        result.to_csv(destination, index=False)
        print(result[["predicted_class"]].value_counts().to_string())
        print(f"Predicciones guardadas en {destination}")
        return 0

    run_pipeline(verbose=not getattr(args, "quiet", False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

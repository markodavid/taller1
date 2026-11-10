"""Rutas y parámetros globales del proyecto Dry Bean.

La estructura combina dos vistas complementarias:

- **Fases CRISP-DM** (`01_...` a `06_...`): cada carpeta concentra la evidencia de su fase.
- **Capas de datos tipo medallón** (`data/bronze`, `data/silver`, `data/gold`): separan el dato
  crudo, el limpio y el listo para modelar.

Centralizar las rutas evita valores mágicos repartidos por notebooks y scripts, y es una práctica
recomendada por TDSP para mantener el proyecto reproducible.
"""

from __future__ import annotations

from pathlib import Path

# --- Raíz del proyecto -----------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# --- Fases CRISP-DM --------------------------------------------------------
PHASE_BUSINESS_DIR = PROJECT_ROOT / "01_comprension_negocio"
PHASE_DATA_DIR = PROJECT_ROOT / "02_comprension_datos"
PHASE_PREP_DIR = PROJECT_ROOT / "03_preparacion_datos"
PHASE_MODEL_DIR = PROJECT_ROOT / "04_modelado"
PHASE_EVAL_DIR = PROJECT_ROOT / "05_evaluacion"
PHASE_DEPLOY_DIR = PROJECT_ROOT / "06_despliegue"

# --- Capas de datos (medallón) ---------------------------------------------
DATA_DIR = PROJECT_ROOT / "data"
BRONZE_DIR = DATA_DIR / "bronze"  # crudo, inmutable
SILVER_DIR = DATA_DIR / "silver"  # limpio y tipado
GOLD_DIR = DATA_DIR / "gold"  # listo para modelar (splits)

DOCS_DIR = PROJECT_ROOT / "docs"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

# --- Dataset ---------------------------------------------------------------
DATASET_ID = 602
DATASET_NAME = "Dry Bean"
DATASET_PAGE = "https://archive.ics.uci.edu/dataset/602/dry+bean+dataset"
DATASET_URL = "https://archive.ics.uci.edu/static/public/602/data.csv"

RAW_DATA_FILE = BRONZE_DIR / "dry_bean.csv"
PROCESSED_DATA_FILE = SILVER_DIR / "dry_bean_clean.csv"
TRAIN_DATA_FILE = GOLD_DIR / "train.csv"
TEST_DATA_FILE = GOLD_DIR / "test.csv"

TARGET_COLUMN = "Class"

# --- Artefactos por fase ---------------------------------------------------
PROFILE_FILE = PHASE_DATA_DIR / "perfil_datos.json"
CLASS_PLOT_FILE = PHASE_DATA_DIR / "distribucion_clases.png"

MANIFEST_FILE = PHASE_PREP_DIR / "data_manifest.json"

BASELINE_MODEL_FILE = PHASE_MODEL_DIR / "logistic_regression_drybean.joblib"
FINAL_MODEL_FILE = PHASE_MODEL_DIR / "random_forest_drybean.joblib"

METRICS_FILE = PHASE_EVAL_DIR / "metricas_modelos.csv"
PREDICTIONS_FILE = PHASE_EVAL_DIR / "predicciones_drybean.csv"
SUMMARY_FILE = PHASE_EVAL_DIR / "resumen_ejecucion.json"

DEMO_PREDICTION_FILE = PHASE_DEPLOY_DIR / "predicciones_nuevas.csv"

# --- Reproducibilidad ------------------------------------------------------
RANDOM_STATE = 42
TEST_SIZE = 0.2


def ensure_directories() -> None:
    """Crea la estructura de carpetas del proyecto si no existe."""
    for directory in (
        PHASE_BUSINESS_DIR,
        PHASE_DATA_DIR,
        PHASE_PREP_DIR,
        PHASE_MODEL_DIR,
        PHASE_EVAL_DIR,
        PHASE_DEPLOY_DIR,
        BRONZE_DIR,
        SILVER_DIR,
        GOLD_DIR,
        DOCS_DIR,
        NOTEBOOKS_DIR,
    ):
        directory.mkdir(parents=True, exist_ok=True)

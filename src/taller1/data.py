"""Carga, descarga y control de calidad del Dry Bean Dataset (CRISP-DM: comprensión de datos)."""

from __future__ import annotations

import hashlib
import json
import ssl
import urllib.request
from pathlib import Path

import certifi
import pandas as pd

from taller1.config import (
    DATASET_ID,
    DATASET_NAME,
    DATASET_PAGE,
    DATASET_URL,
    MANIFEST_FILE,
    PROCESSED_DATA_FILE,
    PROFILE_FILE,
    PROJECT_ROOT,
    RAW_DATA_FILE,
    TARGET_COLUMN,
    TEST_DATA_FILE,
    TRAIN_DATA_FILE,
)


def download_dataset(destination: Path | None = None, force: bool = False) -> Path:
    """Descarga el CSV oficial del dataset desde UCI y lo guarda en ``data/bronze``.

    Usa ``certifi`` para validar el certificado TLS, lo que evita fallos de
    verificación en entornos donde el almacén de certificados del sistema está
    desactualizado (frecuente en Windows corporativo).
    """
    destination = destination or RAW_DATA_FILE
    if destination.exists() and not force:
        return destination

    destination.parent.mkdir(parents=True, exist_ok=True)
    context = ssl.create_default_context(cafile=certifi.where())
    request = urllib.request.Request(DATASET_URL, headers={"User-Agent": "taller1-drybean/0.1"})
    with urllib.request.urlopen(request, context=context, timeout=120) as response:
        payload = response.read()

    temporary = destination.with_suffix(".tmp")
    temporary.write_bytes(payload)
    temporary.replace(destination)
    return destination


def load_raw_dataset(path: Path | None = None, download_if_missing: bool = True) -> pd.DataFrame:
    """Carga el dataset crudo sin transformarlo.

    Estrategia de reproducibilidad: si el CSV local existe se usa; si no, se
    intenta descargar de UCI (o con ``ucimlrepo`` como último recurso).
    """
    path = path or RAW_DATA_FILE
    if not path.exists():
        if not download_if_missing:
            raise FileNotFoundError(f"No existe el dataset en {path}")
        try:
            download_dataset(path)
        except OSError:
            return _load_with_ucimlrepo()

    df = pd.read_csv(path)
    if TARGET_COLUMN not in df.columns:
        raise ValueError(f"El dataset debe contener la columna objetivo '{TARGET_COLUMN}'")
    return df


def _load_with_ucimlrepo() -> pd.DataFrame:
    """Plan B: descarga mediante la librería oficial ``ucimlrepo``."""
    from ucimlrepo import fetch_ucirepo

    dataset = fetch_ucirepo(id=DATASET_ID)
    features = dataset.data.features
    targets = dataset.data.targets
    if targets is None:
        raise ValueError(f"{DATASET_NAME} no expone variable objetivo en ucimlrepo")
    return pd.concat([features, targets], axis=1)


def remove_duplicates(df: pd.DataFrame) -> tuple[pd.DataFrame, int]:
    """Elimina filas duplicadas exactas y devuelve cuántas se removieron."""
    duplicated = int(df.duplicated().sum())
    return df.drop_duplicates().reset_index(drop=True), duplicated


def data_quality_summary(df: pd.DataFrame) -> dict[str, object]:
    """Resume la calidad de los datos: tamaño, tipos, nulos, duplicados y clases."""
    return {
        "n_registros": int(df.shape[0]),
        "n_columnas": int(df.shape[1]),
        "n_features": int(df.shape[1] - 1) if TARGET_COLUMN in df.columns else int(df.shape[1]),
        "valores_nulos": int(df.isna().sum().sum()),
        "columnas_con_nulos": int((df.isna().sum() > 0).sum()),
        "filas_duplicadas": int(df.duplicated().sum()),
        "columnas_no_numericas": list(df.select_dtypes(exclude="number").columns),
        "clases": sorted(df[TARGET_COLUMN].astype(str).unique().tolist())
        if TARGET_COLUMN in df.columns
        else [],
    }


def class_distribution(df: pd.DataFrame) -> pd.Series:
    """Cuenta registros por clase y los ordena de mayor a menor."""
    counts = df[TARGET_COLUMN].value_counts()
    counts.name = "registros"
    return counts


def dataset_fingerprint(path: Path | None = None) -> dict[str, object]:
    """Calcula SHA-256 y tamaño del archivo crudo para versionar los datos (TDSP)."""
    path = path or RAW_DATA_FILE
    payload = path.read_bytes()
    try:
        nombre = str(path.resolve().relative_to(PROJECT_ROOT))
    except ValueError:
        nombre = str(path)
    return {
        "archivo": nombre,
        "sha256": hashlib.sha256(payload).hexdigest(),
        "bytes": len(payload),
    }


def save_processed(df: pd.DataFrame, path: Path | None = None) -> Path:
    """Guarda el dataset limpio en la capa plata (``data/silver``)."""
    path = path or PROCESSED_DATA_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    return path


def save_splits(
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    train_path: Path | None = None,
    test_path: Path | None = None,
) -> tuple[Path, Path]:
    """Guarda los conjuntos de entrenamiento y prueba en la capa oro (``data/gold``)."""
    train_path = train_path or TRAIN_DATA_FILE
    test_path = test_path or TEST_DATA_FILE
    train_path.parent.mkdir(parents=True, exist_ok=True)

    train = X_train.copy()
    train[TARGET_COLUMN] = y_train.to_numpy()
    test = X_test.copy()
    test[TARGET_COLUMN] = y_test.to_numpy()

    train.to_csv(train_path, index=False)
    test.to_csv(test_path, index=False)
    return train_path, test_path


def save_profile(summary: dict[str, object], path: Path | None = None) -> Path:
    """Persiste el perfil de calidad de los datos en la fase de comprensión."""
    path = path or PROFILE_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def save_manifest(manifest: dict[str, object], path: Path | None = None) -> Path:
    """Persiste el manifiesto del dataset (fuente, hash, dimensiones, clases)."""
    path = path or MANIFEST_FILE
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    return path


def build_manifest(df_clean: pd.DataFrame, raw_path: Path | None = None) -> dict[str, object]:
    """Construye el manifiesto completo del dataset usado en el experimento."""
    fingerprint = dataset_fingerprint(raw_path)
    fingerprint.pop("archivo", None)
    return {
        "dataset": DATASET_NAME,
        "uci_id": DATASET_ID,
        "fuente": DATASET_PAGE,
        "url_descarga": DATASET_URL,
        "sha256": fingerprint["sha256"],
        "bytes": fingerprint["bytes"],
        "filas": int(df_clean.shape[0]),
        "columnas": int(df_clean.shape[1]),
        "clases": sorted(df_clean[TARGET_COLUMN].astype(str).unique().tolist()),
        "distribucion_clases": {
            str(k): int(v) for k, v in df_clean[TARGET_COLUMN].value_counts().items()
        },
    }

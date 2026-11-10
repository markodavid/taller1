"""Pruebas de carga, calidad y persistencia de datos (patrón AAA)."""

from __future__ import annotations

import json

import pandas as pd
import pytest

from taller1 import data


@pytest.fixture
def synthetic_csv(tmp_path):
    """Crea un CSV pequeño con el mismo contrato que el dataset real."""
    rows = []
    for class_name, base in (("ALFA", 1.0), ("BETA", 2.0), ("GAMMA", 3.0)):
        for index in range(10):
            rows.append(
                {
                    "Area": base * 1000 + index,
                    "Perimeter": base * 100 + index,
                    "Class": class_name,
                }
            )
    path = tmp_path / "dry_bean.csv"
    pd.DataFrame(rows).to_csv(path, index=False)
    return path


def test_load_raw_dataset_reads_csv_without_downloading(synthetic_csv):
    # Arrange / Act
    df = data.load_raw_dataset(synthetic_csv, download_if_missing=False)

    # Assert
    assert df.shape == (30, 3)
    assert data.TARGET_COLUMN in df.columns


def test_load_raw_dataset_requires_target_column(tmp_path):
    # Arrange
    path = tmp_path / "sin_objetivo.csv"
    pd.DataFrame({"Area": [1, 2]}).to_csv(path, index=False)

    # Act / Assert
    with pytest.raises(ValueError, match="columna objetivo"):
        data.load_raw_dataset(path, download_if_missing=False)


def test_remove_duplicates_reports_removed_rows(synthetic_csv):
    # Arrange
    df = data.load_raw_dataset(synthetic_csv, download_if_missing=False)
    duplicated = pd.concat([df, df.head(5)], ignore_index=True)

    # Act
    clean, removed = data.remove_duplicates(duplicated)

    # Assert
    assert removed == 5
    assert len(clean) == len(df)
    assert not clean.duplicated().any()


def test_data_quality_summary_detects_missing_and_duplicates(synthetic_csv):
    # Arrange
    df = data.load_raw_dataset(synthetic_csv, download_if_missing=False)
    df.loc[0, "Area"] = None
    df = pd.concat([df, df.head(1)], ignore_index=True)

    # Act
    summary = data.data_quality_summary(df)

    # Assert
    assert summary["n_registros"] == 31
    assert summary["n_features"] == 2
    assert summary["valores_nulos"] == 2
    assert summary["filas_duplicadas"] == 1
    assert summary["columnas_no_numericas"] == ["Class"]
    assert summary["clases"] == ["ALFA", "BETA", "GAMMA"]


def test_class_distribution_is_sorted_descending(synthetic_csv):
    # Arrange
    df = data.load_raw_dataset(synthetic_csv, download_if_missing=False)
    df = pd.concat([df, df[df["Class"] == "GAMMA"]], ignore_index=True)

    # Act
    counts = data.class_distribution(df)

    # Assert
    assert counts.iloc[0] == 20
    assert counts.index[0] == "GAMMA"
    assert counts.name == "registros"


def test_save_processed_and_manifest_roundtrip(synthetic_csv, tmp_path):
    # Arrange
    df = data.load_raw_dataset(synthetic_csv, download_if_missing=False)
    processed_path = tmp_path / "processed.csv"
    manifest_path = tmp_path / "manifest.json"

    # Act
    data.save_processed(df, processed_path)
    manifest = data.build_manifest(df, synthetic_csv)
    data.save_manifest(manifest, manifest_path)

    # Assert
    assert processed_path.exists()
    saved = json.loads(manifest_path.read_text(encoding="utf-8"))
    assert saved["sha256"] == manifest["sha256"]
    assert saved["filas"] == 30
    assert saved["distribucion_clases"] == {"ALFA": 10, "BETA": 10, "GAMMA": 10}

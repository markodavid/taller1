"""Pruebas del análisis exploratorio (patrón AAA)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from taller1 import eda


@pytest.fixture
def toy_frame():
    """Dos clases bien separadas por 'Area' y una variable de ruido."""
    rng = np.random.default_rng(7)
    rows = []
    for class_name, center in (("ALFA", 10.0), ("BETA", 20.0)):
        for _ in range(50):
            rows.append(
                {
                    "Area": rng.normal(center, 0.5),
                    "Perimeter": rng.normal(center * 10, 0.5),
                    "Ruido": rng.normal(0, 1),
                    "Class": class_name,
                }
            )
    return pd.DataFrame(rows)


def test_numeric_profile_has_one_row_per_feature(toy_frame):
    # Act
    profile = eda.numeric_profile(toy_frame, ["Area", "Perimeter", "Ruido"])

    # Assert
    assert list(profile.index) == ["Area", "Perimeter", "Ruido"]
    assert profile.index.name == "variable"
    assert {"asimetria", "curtosis", "coef_variacion"} <= set(profile.columns)
    assert profile.loc["Area", "media"] == pytest.approx(15.0, abs=0.5)


def test_outlier_report_flags_injected_extreme(toy_frame):
    # Arrange
    frame = toy_frame.copy()
    frame.loc[0, "Area"] = 1000.0

    # Act
    report = eda.outlier_report(frame, ["Area"])

    # Assert
    assert report.iloc[0]["n_atipicos"] >= 1
    assert report.iloc[0]["pct_atipicos"] > 0


def test_top_correlations_excludes_diagonal_and_sorts(toy_frame):
    # Act
    correlation = eda.correlation_matrix(toy_frame, ["Area", "Perimeter", "Ruido"])
    pairs = eda.top_correlations(correlation, n=2)

    # Assert
    assert len(pairs) == 2
    assert (pairs["variable_1"] != pairs["variable_2"]).all()
    assert abs(pairs.iloc[0]["correlacion"]) >= abs(pairs.iloc[1]["correlacion"])


def test_class_separation_detects_discriminant_feature(toy_frame):
    # Act
    separation = eda.class_separation(toy_frame, "Class", ["Area", "Perimeter", "Ruido"])
    by_feature = separation.set_index("variable")["eta_cuadrado"]

    # Assert
    assert by_feature["Area"] > 0.95
    assert by_feature["Ruido"] < 0.2
    assert separation["eta_cuadrado"].is_monotonic_decreasing


def test_class_profiles_are_standardized_means(toy_frame):
    # Act
    profiles = eda.class_profiles(toy_frame, "Class", ["Area", "Perimeter"])

    # Assert
    assert list(profiles.index) == ["ALFA", "BETA"]
    assert profiles.index.name == "clase"
    assert profiles.loc["BETA", "Area"] > 0
    assert profiles.loc["ALFA", "Area"] < 0
    assert np.all(np.abs(profiles.to_numpy()) < 5)

"""Pruebas de partición, entrenamiento y evaluación de modelos (patrón AAA)."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from taller1 import features, modeling


@pytest.fixture
def toy_dataset():
    """Dataset sintético separable: tres clases, dos variables."""
    rng = np.random.default_rng(42)
    centers = {"ALFA": (0.0, 0.0), "BETA": (5.0, 5.0), "GAMMA": (10.0, 0.0)}
    records = []
    for class_name, (cx, cy) in centers.items():
        for _ in range(60):
            records.append(
                {
                    "Area": rng.normal(cx, 0.4),
                    "Perimeter": rng.normal(cy, 0.4),
                    "Class": class_name,
                }
            )
    return pd.DataFrame(records)


def test_split_features_target_separates_target(toy_dataset):
    # Act
    X, y = features.split_features_target(toy_dataset)

    # Assert
    assert list(X.columns) == ["Area", "Perimeter"]
    assert y.name == "Class"
    assert len(X) == len(y) == 180


def test_split_train_test_is_stratified(toy_dataset):
    # Arrange
    X, y = features.split_features_target(toy_dataset)

    # Act
    X_train, X_test, y_train, y_test = features.split_train_test(X, y, test_size=0.25)

    # Assert
    assert len(X_train) == 135
    assert len(X_test) == 45
    assert y_train.value_counts().to_dict() == {"ALFA": 45, "BETA": 45, "GAMMA": 45}
    assert y_test.value_counts().to_dict() == {"ALFA": 15, "BETA": 15, "GAMMA": 15}
    assert list(X_train.columns) == list(X_test.columns)


def test_baseline_model_learns_separable_data(toy_dataset):
    # Arrange
    X, y = features.split_features_target(toy_dataset)
    X_train, X_test, y_train, y_test = features.split_train_test(X, y)

    # Act
    model = modeling.train_model(modeling.build_baseline_model(), X_train, y_train)
    result = modeling.evaluate_model(model, X_test, y_test, "Logistic Regression")

    # Assert
    assert result.accuracy > 0.9
    assert result.f1_macro > 0.9
    assert result.labels == ["ALFA", "BETA", "GAMMA"]
    assert result.confusion.shape == (3, 3)
    assert "precision" in result.report


def test_random_forest_is_reproducible(toy_dataset):
    # Arrange
    X, y = features.split_features_target(toy_dataset)
    X_train, X_test, y_train, _ = features.split_train_test(X, y)

    # Act
    first = modeling.train_model(modeling.build_random_forest(n_estimators=25), X_train, y_train)
    second = modeling.train_model(modeling.build_random_forest(n_estimators=25), X_train, y_train)

    # Assert
    assert np.array_equal(first.predict(X_test), second.predict(X_test))


def test_save_and_load_model_roundtrip(toy_dataset, tmp_path):
    # Arrange
    X, y = features.split_features_target(toy_dataset)
    model = modeling.train_model(modeling.build_random_forest(n_estimators=25), X, y)
    path = tmp_path / "model.joblib"

    # Act
    modeling.save_model(model, path)
    loaded = modeling.load_model(path)

    # Assert
    assert path.exists()
    assert np.array_equal(model.predict(X.head(5)), loaded.predict(X.head(5)))


def test_predict_bean_class_returns_string(toy_dataset):
    # Arrange
    X, y = features.split_features_target(toy_dataset)
    model = modeling.train_model(modeling.build_baseline_model(), X, y)

    # Act
    prediction = modeling.predict_bean_class(model, X.head(1))

    # Assert
    assert isinstance(prediction, str)
    assert prediction in {"ALFA", "BETA", "GAMMA"}


def test_compare_models_orders_by_f1_macro():
    # Arrange
    good = modeling.EvaluationResult(
        name="Bueno",
        accuracy=0.9,
        f1_macro=0.92,
        f1_weighted=0.9,
        precision_macro=0.9,
        recall_macro=0.9,
        report="",
        report_dict={},
    )
    weak = modeling.EvaluationResult(
        name="Débil",
        accuracy=0.6,
        f1_macro=0.55,
        f1_weighted=0.6,
        precision_macro=0.6,
        recall_macro=0.6,
        report="",
        report_dict={},
    )

    # Act
    comparison = modeling.compare_models([weak, good])

    # Assert
    assert comparison.iloc[0]["modelo"] == "Bueno"
    assert comparison.iloc[0]["f1_macro"] == 0.92

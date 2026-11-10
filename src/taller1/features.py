"""Separación de variables y partición train/test (CRISP-DM: preparación de datos)."""

from __future__ import annotations

import pandas as pd
from sklearn.model_selection import train_test_split

from taller1.config import RANDOM_STATE, TARGET_COLUMN, TEST_SIZE


def split_features_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Devuelve ``X`` (predictoras) e ``y`` (variable objetivo)."""
    X = df.drop(columns=TARGET_COLUMN)
    y = df[TARGET_COLUMN].astype(str)
    return X, y


def split_train_test(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = TEST_SIZE,
    random_state: int = RANDOM_STATE,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    """Divide los datos manteniendo la proporción de clases (estratificación)."""
    return train_test_split(
        X,
        y,
        test_size=test_size,
        random_state=random_state,
        stratify=y,
    )

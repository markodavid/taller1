"""Análisis exploratorio de datos (CRISP-DM: comprensión de datos).

Complementa el perfil básico (nulos, duplicados, clases) con el análisis que justifica las
decisiones de modelado:

- distribución y asimetría de cada variable;
- valores atípicos por regla IQR;
- correlaciones entre predictoras (multicorrelación);
- perfil de cada clase y **separabilidad** de cada variable (eta cuadrado).
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

FIGURE_DPI = 150


def numeric_profile(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Estadísticas descriptivas ampliadas: dispersión, asimetría, curtosis y CV."""
    description = df[columns].describe().T
    profile = pd.DataFrame(
        {
            "media": description["mean"],
            "desv_std": description["std"],
            "min": description["min"],
            "p25": description["25%"],
            "mediana": description["50%"],
            "p75": description["75%"],
            "max": description["max"],
            "asimetria": df[columns].skew(),
            "curtosis": df[columns].kurt(),
        }
    )
    profile["coef_variacion"] = profile["desv_std"] / profile["media"]
    profile.index.name = "variable"
    return profile.round(4)


def outlier_report(df: pd.DataFrame, columns: list[str], factor: float = 1.5) -> pd.DataFrame:
    """Cuenta valores atípicos por la regla de Tukey (IQR · factor).

    No los elimina: en este dataset los extremos suelen ser granos reales grandes.
    """
    rows = []
    for column in columns:
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - factor * iqr
        upper = q3 + factor * iqr
        mask = (df[column] < lower) | (df[column] > upper)
        rows.append(
            {
                "variable": column,
                "limite_inferior": round(float(lower), 2),
                "limite_superior": round(float(upper), 2),
                "n_atipicos": int(mask.sum()),
                "pct_atipicos": round(100 * float(mask.mean()), 2),
            }
        )
    return pd.DataFrame(rows).sort_values("n_atipicos", ascending=False, ignore_index=True)


def correlation_matrix(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Matriz de correlación de Pearson entre variables predictoras."""
    return df[columns].corr()


def top_correlations(correlation: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """Pares de variables con mayor correlación absoluta (sin repetir ni la diagonal)."""
    columns = list(correlation.columns)
    rows = []
    for i, first in enumerate(columns):
        for second in columns[i + 1 :]:
            rows.append(
                {
                    "variable_1": first,
                    "variable_2": second,
                    "correlacion": float(correlation.loc[first, second]),
                }
            )
    pairs = pd.DataFrame(rows)
    pairs["abs_correlacion"] = pairs["correlacion"].abs()
    return (
        pairs.sort_values("abs_correlacion", ascending=False)
        .head(n)
        .drop(columns="abs_correlacion")
        .reset_index(drop=True)
    )


def class_profiles(df: pd.DataFrame, target: str, columns: list[str]) -> pd.DataFrame:
    """Media de cada variable por clase, estandarizada (z-score) para comparar escalas."""
    standardized = df[columns].apply(lambda series: (series - series.mean()) / series.std())
    standardized[target] = df[target].to_numpy()
    profiles = standardized.groupby(target, observed=True)[columns].mean().round(2)
    profiles.index.name = "clase"
    return profiles


def class_separation(df: pd.DataFrame, target: str, columns: list[str]) -> pd.DataFrame:
    """Eta cuadrado de cada variable: proporción de varianza explicada por la clase.

    Valores cercanos a 1 indican que la variable separa bien las variedades; cercanos a 0,
    que apenas aporta información.
    """
    rows = []
    grand_mean = df[columns].mean()
    total_ss = ((df[columns] - grand_mean) ** 2).sum()
    grouped = df.groupby(target, observed=True)
    for column in columns:
        grand = df[column].mean()
        between_ss = sum(len(group) * (group[column].mean() - grand) ** 2 for _, group in grouped)
        rows.append(
            {
                "variable": column,
                "eta_cuadrado": float(between_ss / total_ss[column]),
            }
        )
    return (
        pd.DataFrame(rows)
        .sort_values("eta_cuadrado", ascending=False)
        .reset_index(drop=True)
        .round(4)
    )


def _finish(figure: plt.Figure, save_path: Path | None) -> plt.Figure:
    figure.tight_layout()
    if save_path is not None:
        save_path.parent.mkdir(parents=True, exist_ok=True)
        figure.savefig(save_path, dpi=FIGURE_DPI, bbox_inches="tight")
    return figure


def plot_feature_histograms(
    df: pd.DataFrame,
    columns: list[str],
    save_path: Path | None = None,
    n_cols: int = 4,
) -> plt.Figure:
    """Cuadrícula de histogramas: forma de la distribución de cada variable."""
    n_rows = int(np.ceil(len(columns) / n_cols))
    figure, axes = plt.subplots(n_rows, n_cols, figsize=(4 * n_cols, 3 * n_rows))
    for axis, column in zip(axes.ravel(), columns, strict=False):
        axis.hist(df[column], bins=40, color="#4C72B0", edgecolor="white")
        axis.set_title(column, fontsize=10)
        axis.tick_params(labelsize=7)
    for axis in axes.ravel()[len(columns) :]:
        axis.set_visible(False)
    figure.suptitle("Distribución de las 16 variables geométricas", fontsize=13)
    return _finish(figure, save_path)


def plot_boxplots_by_class(
    df: pd.DataFrame,
    target: str,
    columns: list[str],
    save_path: Path | None = None,
    n_cols: int = 4,
) -> plt.Figure:
    """Diagramas de caja por clase: solapamiento entre variedades."""
    n_rows = int(np.ceil(len(columns) / n_cols))
    classes = sorted(df[target].astype(str).unique())
    figure, axes = plt.subplots(n_rows, n_cols, figsize=(4.2 * n_cols, 3.2 * n_rows))
    for axis, column in zip(axes.ravel(), columns, strict=False):
        groups = [df.loc[df[target].astype(str) == name, column] for name in classes]
        axis.boxplot(groups, tick_labels=classes, showfliers=False)
        axis.set_title(column, fontsize=10)
        axis.tick_params(axis="x", rotation=60, labelsize=7)
        axis.tick_params(axis="y", labelsize=7)
    for axis in axes.ravel()[len(columns) :]:
        axis.set_visible(False)
    figure.suptitle("Distribución por variedad (sin outliers para legibilidad)", fontsize=13)
    return _finish(figure, save_path)


def plot_correlation_heatmap(
    correlation: pd.DataFrame, save_path: Path | None = None
) -> plt.Figure:
    """Mapa de calor de correlaciones entre predictoras."""
    figure, axis = plt.subplots(figsize=(11, 9))
    image = axis.imshow(correlation.to_numpy(), cmap="coolwarm", vmin=-1, vmax=1)
    labels = list(correlation.columns)
    axis.set_xticks(range(len(labels)), labels, rotation=90, fontsize=8)
    axis.set_yticks(range(len(labels)), labels, fontsize=8)
    figure.colorbar(image, ax=axis, shrink=0.8, label="Correlación de Pearson")
    axis.set_title("Matriz de correlaciones entre variables geométricas")
    return _finish(figure, save_path)


def plot_class_profiles(profiles: pd.DataFrame, save_path: Path | None = None) -> plt.Figure:
    """Mapa de calor de perfiles por clase (z-score de cada variable)."""
    figure, axis = plt.subplots(figsize=(14, 4.5))
    image = axis.imshow(profiles.to_numpy(), cmap="coolwarm", vmin=-2, vmax=2, aspect="auto")
    axis.set_xticks(range(len(profiles.columns)), profiles.columns, rotation=60, fontsize=8)
    axis.set_yticks(range(len(profiles.index)), profiles.index, fontsize=9)
    for row in range(profiles.shape[0]):
        for column in range(profiles.shape[1]):
            axis.text(
                column,
                row,
                f"{profiles.iloc[row, column]:.1f}",
                ha="center",
                va="center",
                fontsize=7,
            )
    figure.colorbar(image, ax=axis, shrink=0.85, label="z-score (media por clase)")
    axis.set_title("Perfil de cada variedad: por encima (+) o debajo (-) del promedio")
    return _finish(figure, save_path)


def plot_separability(separation: pd.DataFrame, save_path: Path | None = None) -> plt.Figure:
    """Barras horizontales con la varianza explicada por la clase (eta cuadrado)."""
    ordered = separation.iloc[::-1]
    figure, axis = plt.subplots(figsize=(8, 6))
    axis.barh(ordered["variable"], ordered["eta_cuadrado"], color="#55A868")
    axis.set_xlabel("Eta cuadrado (varianza explicada por la clase)")
    axis.set_title("Poder discriminante de cada variable")
    axis.set_xlim(0, 1)
    for index, value in enumerate(ordered["eta_cuadrado"]):
        axis.text(value + 0.01, index, f"{value:.2f}", va="center", fontsize=8)
    return _finish(figure, save_path)


def save_tables(
    profile: pd.DataFrame,
    outliers: pd.DataFrame,
    correlations: pd.DataFrame,
    separation: pd.DataFrame,
    paths: dict[str, Path],
) -> dict[str, Path]:
    """Guarda las tablas del EDA en CSV (evidencia auditable de la fase 2)."""
    tables = {
        "profile": profile,
        "outliers": outliers,
        "correlations": correlations,
        "separation": separation,
    }
    saved: dict[str, Path] = {}
    for key, table in tables.items():
        path = paths[key]
        path.parent.mkdir(parents=True, exist_ok=True)
        table.to_csv(path, index=key == "profile")
        saved[key] = path
    return saved

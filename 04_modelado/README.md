# 04 · Modelado

**Fase CRISP-DM 4 — Modeling**

## Modelos entrenados

| Modelo | Configuración | Rol |
|---|---|---|
| Regresión logística | `StandardScaler` + `LogisticRegression(max_iter=1000)` | Baseline |
| Random Forest | `RandomForestClassifier(n_estimators=200, class_weight="balanced")` | Modelo alternativo |

Ambos se entrenan con los datos de `data/gold/train.csv` y se evalúan con
`data/gold/test.csv`. El escalamiento vive dentro de un `Pipeline`, de modo que se ajusta **solo**
con entrenamiento y no filtra información de prueba.

## Por qué estos modelos

- **Baseline:** la regresión logística es simple, rápida e interpretable. Sirve como vara de
  medir; si un modelo complejo no la supera, no se justifica su costo.
- **Alternativo:** el bosque aleatorio captura relaciones no lineales e interacciones entre
  medidas de forma y tamaño. `class_weight="balanced"` compensa el desbalance 7:1.

## Artefactos

| Archivo | Contenido |
|---|---|
| [`logistic_regression_drybean.joblib`](logistic_regression_drybean.joblib) | Baseline serializado |
| [`random_forest_drybean.joblib`](random_forest_drybean.joblib) | Modelo final serializado |

> Los `.joblib` son artefactos binarios: están en `.gitignore` y se regeneran con
> `make pipeline`. Se conservan localmente para la entrega.

## Evidencia

- Notebook: sección **4. Modelado**.
- Reporte: [`docs/reporte_crisp_dm.md`](../docs/reporte_crisp_dm.md), sección 4.

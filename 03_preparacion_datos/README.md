# 03 · Preparación de los datos

**Fase CRISP-DM 3 — Data Preparation**

## Flujo de capas (medallón)

```text
data/bronze/dry_bean.csv        crudo, inmutable, descargado de UCI
        │
        ├── eliminar 68 duplicados
        ▼
data/silver/dry_bean_clean.csv  limpio y tipado
        │
        ├── split 80/20 estratificado (random_state=42)
        ▼
data/gold/train.csv             listo para modelar
data/gold/test.csv              reservado para evaluar
```

## Decisiones y justificación

| Decisión | Justificación |
|---|---|
| Eliminar 68 duplicados | Un registro repetido sesga entrenamiento y evaluación; todos son de `HOROZ` |
| Conservar valores extremos | Son granos reales; recortarlos perdería señal de `BOMBAY` |
| No imputar | No hay valores faltantes |
| Estratificar el split | Mantiene la proporción de las 7 clases en train y test |
| `random_state=42` | Reproducibilidad exigida por TDSP |
| Guardar los splits | Permite reentrenar sin repetir la partición y auditar el experimento |

## Partición

| Conjunto | Registros | Uso |
|---|---:|---|
| Entrenamiento | 10 834 | Ajuste de modelos |
| Prueba | 2 709 | Evaluación sobre datos no vistos |

La proporción de cada clase en prueba coincide con la del dataset completo (por ejemplo,
`DERMASON` 26.2 % y `BOMBAY` 3.8 %).

## Artefactos

| Archivo | Contenido |
|---|---|
| [`data_manifest.json`](data_manifest.json) | Fuente, SHA-256, dimensiones y distribución de clases |
| `../data/silver/dry_bean_clean.csv` | Dataset limpio |
| `../data/gold/train.csv` | Entrenamiento con columna `Class` |
| `../data/gold/test.csv` | Prueba con columna `Class` |

## Evidencia

- Notebook: sección **3. Preparación de los datos**.
- Reporte: [`docs/reporte_crisp_dm.md`](../docs/reporte_crisp_dm.md), sección 3.

# 01 · Comprensión del negocio

**Fase CRISP-DM 1 — Business Understanding**

## Problema

Una empresa agrícola recibe lotes de frijol seco y debe separarlos por variedad antes de
comercializarlos. Hoy parte del proceso es manual: un operario observa el grano y decide su
categoría. El método es lento, subjetivo y difícil de auditar; dos operarios pueden etiquetar el
mismo grano de forma distinta y el error se descubre tarde, cuando el lote ya está empacado.

## Objetivo

Construir un modelo que prediga la **variedad de frijol** a partir de 16 mediciones geométricas
obtenidas por visión por computador, para apoyar el control de calidad y reducir el tiempo de
clasificación manual.

| Elemento | Definición |
|---|---|
| Tipo de problema | Clasificación multiclase supervisada |
| Variable objetivo | `Class` — 7 variedades |
| Métrica principal | **F1 macro** |
| Métrica secundaria | Accuracy y F1 ponderado |
| Criterio de éxito | F1 macro ≥ 0.90 en el conjunto de prueba |
| Uso previsto | Apoyo a la decisión: el operario confirma o corrige |
| Riesgo principal | Confundir variedades de forma y tamaño similares |

## Interesados

| Interesado | Necesidad |
|---|---|
| Área de calidad | Reducir el tiempo de clasificación y estandarizar el criterio |
| Operarios | Una herramienta que sugiera la variedad, no que los reemplace |
| Gerencia | Evidencia de que el modelo es confiable y auditable |
| Equipo de datos | Un problema medible, con datos disponibles y criterio de éxito claro |

## Decisiones registradas

1. Se elige **F1 macro** porque las clases están desbalanceadas y todas las variedades importan
   por igual en el control de calidad.
2. El modelo es de **apoyo**, no autónomo: el costo de un error justifica la revisión humana.
3. El criterio de éxito se acuerda **antes** de modelar (compromiso del Product Owner).

## Evidencia

- Notebook: sección **1. Comprensión del negocio**.
- Reporte: [`docs/reporte_crisp_dm.md`](../docs/reporte_crisp_dm.md), sección 1.
- Historias de usuario y priorización: [`docs/scrum_ml.md`](../docs/scrum_ml.md).

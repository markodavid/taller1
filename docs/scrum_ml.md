# Evidencia Scrum ML — Proyecto Dry Bean

**Equipo:** Marko David García · Alejandro Meneses · Henry Rosenstiehl
**Product Goal:** entregar un modelo reproducible que clasifique variedades de frijol seco con
F1 macro ≥ 0.90 y que el área de calidad pueda probar con datos nuevos.
**Periodo:** 3 sprints de una semana (sesiones del laboratorio).
**Entregable:** 3 de 3 — Evidencia Scrum ML.

---

## 1. Equipo y roles

El plan del curso propone cuatro roles para un equipo de cuatro integrantes. El equipo tiene tres
personas, por lo que **Scrum Master y Data Engineer/Analyst se combinan en una misma persona**.
La decisión se tomó en la primera reunión y se registró aquí para que el reparto sea explícito.

| Integrante | Rol | Responsabilidad | Entregable asociado |
|---|---|---|---|
| Alejandro Meneses | **Product Owner** | Define el valor del modelo, prioriza el backlog, valida criterios de aceptación | Historias de usuario, validación final |
| Henry Rosenstiehl | **Scrum Master** + Data Engineer/Analyst | Facilita el proceso, mantiene el tablero, prepara y valida los datos | Tablero, dataset limpio, EDA |
| Marko David García | **ML Engineer** | Entrena, evalúa, serializa el modelo y expone la predicción | Modelos, métricas, artefactos |

**Acuerdos de equipo**

- Reunión corta (daily) al inicio de cada sesión; duración máxima 10 minutos.
- Un ítem solo pasa a *Hecho* si cumple la Definition of Done y otra persona lo revisa.
- Commits con Conventional Commits; ramas `feature/<tema>` y Pull Request antes de integrar a
  `main`.
- La métrica principal (**F1 macro**) se acordó con el Product Owner **antes** de entrenar.

---

## 2. Product Backlog

Prioridad: **Alta** (necesaria para el objetivo), **Media** (mejora el resultado), **Baja**
(deseable). Estimación en puntos de historia (Fibonacci).

| ID | Historia de usuario | Tarea técnica | Prioridad | SP | Responsable | Criterio de aceptación | Sprint | Estado |
|---|---|---|---|---:|---|---|---|---|
| PB-01 | Como analista quiero cargar datos reales para analizarlos | Descargar y leer el CSV de UCI | Alta | 3 | Henry | El dataframe se carga sin errores y conserva las 17 columnas | 1 | Hecho |
| PB-02 | Como científico de datos quiero revisar la calidad de los datos | Reportar nulos, duplicados y tipos | Alta | 3 | Henry | Hay un resumen de calidad con conteos verificables | 1 | Hecho |
| PB-03 | Como equipo queremos entender la distribución de clases | Tabla y gráfico de `value_counts()` | Alta | 2 | Henry | Se identifica el desbalance y se documenta su efecto | 1 | Hecho |
| PB-04 | Como equipo queremos una base reproducible | Split 80/20 estratificado + pipeline de escalamiento | Alta | 3 | Marko | Partición con `random_state=42` y `stratify=y`; escalado ajustado solo con train | 1 | Hecho |
| PB-05 | Como equipo queremos un modelo base | Entrenar `LogisticRegression` | Alta | 3 | Marko | Se reportan accuracy y F1 macro | 2 | Hecho |
| PB-06 | Como equipo queremos mejorar el desempeño | Entrenar `RandomForestClassifier` balanceado | Alta | 3 | Marko | Se compara contra el baseline con las mismas métricas | 2 | Hecho |
| PB-07 | Como usuario final quiero entender el resultado | Matriz de confusión y reporte por clase | Alta | 3 | Marko / Alejandro | Se documentan las clases que más se confunden | 2 | Hecho |
| PB-08 | Como negocio quiero saber qué variables importan | Importancia de variables del bosque | Media | 2 | Alejandro | Top 10 de variables con interpretación de negocio | 2 | Hecho |
| PB-09 | Como equipo técnico quiero reproducibilidad | Guardar modelo con `joblib` y función de predicción | Alta | 3 | Marko | El modelo se carga desde disco y predice una muestra | 3 | Hecho |
| PB-10 | Como equipo queremos documentación profesional | README + reporte CRISP-DM + evidencia Scrum | Alta | 5 | Alejandro / Henry | Documentos completos y enlazados entre sí | 3 | Hecho |
| PB-11 | Como equipo queremos evitar regresiones | Pruebas con `pytest` y verificación `make check` | Media | 3 | Marko | 13 pruebas en verde y lint sin errores | 3 | Hecho |
| PB-12 | Como estudiantes queremos cerrar la reflexión | Responder las preguntas finales del laboratorio | Media | 2 | Alejandro | Las 7 preguntas respondidas con evidencia del proyecto | 3 | Hecho |

**Total estimado:** 35 puntos de historia.

---

## 3. Planeación de sprints

### Sprint 1 — Comprensión y preparación

- **Sprint Goal:** tener datos confiables y una base reproducible para modelar.
- **Ítems:** PB-01, PB-02, PB-03, PB-04 (11 SP).
- **Entregables:** dataset cargado, resumen de calidad, gráfico de distribución, split
  estratificado y pipeline de preprocesamiento.
- **Riesgo identificado:** la descarga desde UCI podía fallar por red o certificados.

### Sprint 2 — Modelado y evaluación

- **Sprint Goal:** demostrar con métricas qué modelo conviene y por qué.
- **Ítems:** PB-05, PB-06, PB-07, PB-08 (11 SP).
- **Entregables:** baseline, modelo alternativo, tabla comparativa, matriz de confusión,
  importancia de variables.
- **Riesgo identificado:** que el bosque aleatorio no superara al baseline y hubiera que
  justificar su uso (o descartarlo).

### Sprint 3 — Despliegue y documentación

- **Sprint Goal:** dejar el modelo usable y el proyecto auditable.
- **Ítems:** PB-09, PB-10, PB-11, PB-12 (13 SP).
- **Entregables:** modelo `.joblib`, demo de predicción, README, reporte CRISP-DM, pruebas y
  respuestas de reflexión.
- **Riesgo identificado:** que la documentación se escribiera al final sin datos trazables (se
  mitigó generando los artefactos desde el pipeline).

---

## 4. Tablero Scrum (estado final)

| Por hacer | En progreso | Hecho |
|---|---|---|
| — | — | PB-01, PB-02, PB-03, PB-04, PB-05, PB-06, PB-07, PB-08, PB-09, PB-10, PB-11, PB-12 |

### Estado por sprint

| Sprint | Al iniciar (Por hacer) | Durante (En progreso) | Al cerrar (Hecho) |
|---|---|---|---|
| 1 | PB-01 … PB-04 | PB-02, PB-04 | PB-01, PB-02, PB-03, PB-04 |
| 2 | PB-05 … PB-08 | PB-06, PB-07 | PB-05, PB-06, PB-07, PB-08 |
| 3 | PB-09 … PB-12 | PB-10, PB-11 | PB-09, PB-10, PB-11, PB-12 |

**Velocidad:** Sprint 1 = 11 SP · Sprint 2 = 11 SP · Sprint 3 = 13 SP.
**Promedio:** 11.7 SP por sprint, sin ítems arrastrados entre sprints.

---

## 5. Daily Scrum

Formato: qué hice desde la última reunión · qué haré ahora · qué bloqueo tengo.

### Daily del Sprint 1

| Integrante | Qué hice | Qué haré | Bloqueos |
|---|---|---|---|
| Henry | Descargué el CSV y revisé tipos y nulos | Reportar duplicados y distribución de clases | La descarga con `ucimlrepo` falla por certificado TLS |
| Marko | Preparé el entorno con `uv` y la estructura TDSP | Implementar el split estratificado | Ninguno |
| Alejandro | Redacté la historia de usuario y el criterio de éxito | Validar que F1 macro sea la métrica principal | Ninguno |

**Acción sobre el bloqueo:** se reemplazó la descarga de `pandas` por una petición con validación
`certifi` y se versionó el CSV en `data/bronze/`. Bloqueo cerrado el mismo día.

### Daily del Sprint 2

| Integrante | Qué hice | Qué haré | Bloqueos |
|---|---|---|---|
| Marko | Entrené el baseline y el bosque aleatorio | Comparar métricas y revisar errores por clase | Ninguno |
| Alejandro | Revisé el reporte por clase | Priorizar el análisis de la clase con peor F1 | Ninguno |
| Henry | Verifiqué la partición estratificada | Documentar la preparación de datos | Ninguno |

### Daily del Sprint 3

| Integrante | Qué hice | Qué haré | Bloqueos |
|---|---|---|---|
| Marko | Guardé el modelo y probé la carga desde disco | Añadir pruebas automatizadas | Ninguno |
| Henry | Escribí el README y la estructura del repositorio | Completar la evidencia Scrum | Ninguno |
| Alejandro | Redacté las conclusiones de negocio | Responder las preguntas de reflexión | Ninguno |

---

## 6. Sprint Review

### Sprint 1 — revisión

Se demostró la carga del dataset, el resumen de calidad (0 nulos, 68 duplicados) y el gráfico de
distribución de clases. El Product Owner aceptó el incremento y pidió documentar explícitamente el
efecto del desbalance en la elección de métrica; se incorporó al notebook.

### Sprint 2 — revisión

Se presentó la comparación de modelos:

| Modelo | Accuracy | F1 macro |
|---|---:|---:|
| Logistic Regression | 0.9195 | 0.9306 |
| Random Forest | 0.9195 | 0.9310 |

El Product Owner cuestionó si valía la pena el modelo más complejo con una diferencia de 0.0004.
El equipo acordó mantener Random Forest por la importancia de variables y la robustez futura, y
**documentar el empate técnico** como hallazgo. Criterio de éxito (F1 macro ≥ 0.90) cumplido.

### Sprint 3 — revisión

Se demostró la carga del modelo `.joblib` y una predicción correcta sobre una muestra
(`SEKER` predicho, `SEKER` real), además de la exportación de predicciones y la ejecución de
`make check` en verde. Todos los ítems del backlog quedaron en *Hecho*.

---

## 7. Retrospectiva

| Pregunta | Respuesta del equipo |
|---|---|
| **¿Qué salió bien?** | La estructura TDSP evitó reprocesos; cada artefacto quedó en su carpeta y enlazado desde el README. El baseline reveló temprano que el problema era casi lineal y ahorró tiempo de experimentación. |
| **¿Qué fue difícil?** | La descarga del dataset falló por un certificado TLS desactualizado del sistema. También costó acordar la métrica antes de ver resultados. |
| **¿Qué mejoraríamos en el siguiente sprint?** | Congelar el entorno (`uv.lock`) desde el día uno; definir la métrica principal en el refinamiento y no después de entrenar; estimar con más cuidado las tareas de documentación (5 SP se quedaron cortos). |
| **¿Qué aprendizaje técnico obtuvimos?** | Un pipeline de scikit-learn evita fuga de información al escalar; `class_weight="balanced"` y F1 macro son imprescindibles con clases desbalanceadas; `joblib` + manifiesto de datos hacen reproducible un experimento. |

### Tres puntos solicitados por el laboratorio

1. **Qué funcionó:** el flujo TDSP + baseline temprano + revisión por pares de cada entregable.
2. **Qué no funcionó:** la estimación de documentación y la dependencia de la descarga en línea.
3. **Qué mejorarían:** automatizar la validación de datos desde el primer sprint y reservar un
   ítem explícito para el análisis de errores por clase.

---

## 8. Definition of Done — verificación

| Criterio del laboratorio | Evidencia | Estado |
|---|---|---|
| El notebook corre de inicio a fin sin errores | `notebooks/01_laboratorio_drybean.ipynb` ejecutado, 0 celdas con error | ✅ |
| El dataset se descarga o carga correctamente | `data/bronze/dry_bean.csv` + `03_preparacion_datos/data_manifest.json` | ✅ |
| Se reportan valores nulos y duplicados | Notebook §2: 0 nulos, 68 duplicados | ✅ |
| Se entrena un baseline y un modelo alternativo | `LogisticRegression` y `RandomForestClassifier` | ✅ |
| Se comparan modelos con accuracy y F1 macro | `05_evaluacion/metricas_modelos.csv` | ✅ |
| Se incluye matriz de confusión | `05_evaluacion/matriz_confusion_random_forest.png` | ✅ |
| Se guarda el modelo final | `04_modelado/random_forest_drybean.joblib` | ✅ |
| Se explica el resultado en lenguaje comprensible | Notebook §7 y `docs/reporte_crisp_dm.md` | ✅ |
| Se documenta la relación con CRISP-DM, TDSP y Scrum ML | README, reporte y este documento | ✅ |

---

## 9. Trazabilidad de las ceremonias

| Ceremonia | Frecuencia | Evidencia |
|---|---|---|
| Sprint Planning | Al inicio de cada sprint | Sección 3 |
| Daily Scrum | Cada sesión | Sección 5 |
| Sprint Review | Al cierre de cada sprint | Sección 6 |
| Retrospectiva | Al cierre de cada sprint | Sección 7 |
| Refinamiento del backlog | Cuando cambia una prioridad | Sección 2 (prioridad y estado) |

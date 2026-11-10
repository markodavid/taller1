# CONSTITUTION — Taller 1 · Dry Bean ML

> **Verdad central del proyecto.** Este documento define el propósito, el stack, la estructura,
> las convenciones y el flujo de trabajo del laboratorio. Si algo aquí contradice al código, el
> código manda **y este archivo se actualiza en el mismo commit**.

> ⚠️ **Directiva de mantenimiento:** cada cambio significativo (nuevo módulo, cambio de métrica,
> nueva fuente de datos o ajuste de stack) se registra aquí y en el historial de decisiones.

---

## 0. Identidad del proyecto

| Campo | Valor |
|---|---|
| **Nombre** | Taller 1 — Dry Bean ML |
| **Descripción** | Clasificación de 7 variedades de frijol seco con CRISP-DM, TDSP y Scrum ML |
| **Curso** | Gerencia de Proyectos — UAO |
| **Equipo** | Marko David García · Alejandro Meneses · Henry Rosenstiehl |
| **Licencia** | MIT |
| **Rama principal** | `main` |
| **Estado** | Entregable completo (3 de 3) |

## 1. Propósito y no-propósito

### Propósito

Demostrar, con un caso real y reproducible, cómo se estructura un proyecto de Machine Learning
aplicando CRISP-DM (fases), TDSP (organización y trazabilidad) y Scrum ML (gestión del trabajo).
El resultado es un modelo de clasificación de variedades de frijol con métricas verificables y
artefactos auditables.

### No-propósito

No es un sistema en producción, no reemplaza la clasificación manual y no promete generalizar a
imágenes de otras condiciones de captura. Tampoco es un ejercicio de optimización de
hiperparámetros: el objetivo es metodológico y reproducible.

## 2. Alcance

### Dentro del alcance

- Descarga y validación del Dry Bean Dataset (UCI id 602).
- Análisis exploratorio, limpieza y partición estratificada.
- Baseline (regresión logística) y modelo alternativo (Random Forest).
- Evaluación con accuracy, F1 macro, reporte por clase y matriz de confusión.
- Serialización del modelo y predicción por CLI.
- Documentación CRISP-DM y evidencia Scrum ML.

### Fuera del alcance (por ahora)

- Servicio web o API en la nube.
- Reentrenamiento automático y monitoreo de deriva.
- Búsqueda exhaustiva de hiperparámetros (solo validación cruzada como extensión).
- Variables de color o textura (el dataset solo tiene geometría).

## 3. Stack técnico

| Categoría | Tecnología |
|---|---|
| Lenguaje | Python 3.13+ |
| Gestor de entorno | [`uv`](https://docs.astral.sh/uv/) |
| Build backend | `uv_build` (src-layout) |
| Paquete | `taller1` |
| Datos y cálculo | pandas, NumPy |
| Machine Learning | scikit-learn |
| Serialización | joblib |
| Gráficas | Matplotlib |
| Descarga del dataset | `ucimlrepo` + `urllib`/`certifi` |
| Testing | pytest |
| Lint / formato | Ruff |
| Pre-commit | pre-commit |
| CI | GitHub Actions |

> ⚠️ **Regla dura:** la gestión de dependencias y entornos pasa por `uv`. No se usa
> `requirements.txt`. La excepción documentada es el camino `venv` + `pip install -e .` que
> propone el laboratorio; en ese caso las dependencias siguen viviendo en `pyproject.toml`.

## 4. Estructura del repositorio

```text
taller1/
├── 01_comprension_negocio/  # problema, objetivos, criterios de éxito
├── 02_comprension_datos/    # perfil de calidad y distribución
├── 03_preparacion_datos/    # manifiesto y decisiones de limpieza
├── 04_modelado/             # artefactos .joblib
├── 05_evaluacion/           # métricas, matrices, predicciones
├── 06_despliegue/           # demo de predicción
├── data/
│   ├── bronze/              # CSV original de UCI (nunca se modifica)
│   ├── silver/              # dataset limpio, regenerable
│   └── gold/                # train/test listos para modelar
├── notebooks/
│   └── 01_laboratorio_drybean.ipynb
├── src/taller1/
│   ├── config.py            # rutas y parámetros globales
│   ├── data.py              # descarga, calidad, manifiesto
│   ├── features.py          # X/y y partición estratificada
│   ├── modeling.py          # entrenamiento, evaluación, persistencia
│   ├── reporting.py         # gráficas y tablas
│   └── cli.py               # pipeline y predicción
├── tests/                   # pruebas (AAA)
├── docs/                    # reporte CRISP-DM, Scrum ML, reflexión
├── .github/                 # CI, templates, Dependabot
├── CONSTITUTION.md
├── README.md
├── Makefile
└── pyproject.toml
```

## 5. Convenciones de código

- **Estilo:** PEP 8 vía Ruff (`line-length = 100`, comillas dobles).
- **Tipado:** anotaciones en firmas públicas; `from __future__ import annotations`.
- **Nomenclatura:** `snake_case` para funciones y variables, `PascalCase` para clases,
  `UPPER_CASE` para constantes.
- **Docstrings:** en módulos, clases y funciones públicas, en español.
- **Pruebas:** pytest con patrón **AAA** (Arrange, Act, Assert).
- **Idioma:** documentación, comentarios y commits en español; identificadores en inglés.

### Invariantes del dominio

1. `data/bronze/` es inmutable: la limpieza siempre escribe en `data/silver/` y los splits en
   `data/gold/`.
2. La columna objetivo se llama `Class` y nunca se usa como predictora.
3. El escalamiento vive dentro de un `Pipeline` para evitar fuga de información.
4. Toda partición usa `random_state=42` y `stratify=y`.
5. El criterio de selección es **F1 macro**, no accuracy.
6. Ningún artefacto de las fases (`02_` a `06_`) se edita a mano: se regenera con
   `make pipeline`.
7. Cada fase CRISP-DM tiene su carpeta con `README.md` que indexa la evidencia.

## 6. Calidad y automatización

| Herramienta | Rol | Comando |
|---|---|---|
| `uv` | Entornos y dependencias | `uv sync` |
| Ruff | Lint + formato | `make lint` / `make format` |
| pytest | Pruebas | `make test` |
| pre-commit | Hooks antes de cada commit | `make pre-commit` |
| GitHub Actions | CI (lint + formato + pruebas) | `.github/workflows/ci.yml` |

- `make check` debe estar en verde antes de abrir un Pull Request.
- `--no-verify` está prohibido salvo causa justificada y documentada.
- Toda dependencia nueva entra con `uv add` / `uv add --dev`.

## 7. Git y colaboración

- **Estrategia de ramas:** `feat/...`, `fix/...`, `docs/...`, `test/...`, `chore/...`.
- **Commits:** [Conventional Commits](https://www.conventionalcommits.org/) en imperativo.
- **Integración:** Pull Request con checklist (incluye actualizar este documento si aplica).
- **Revisión:** cada PR requiere al menos una revisión de otro integrante.

## 8. Gobernanza de datos y modelos

- **Versionado de datos:** el CSV crudo se versiona en `data/bronze/` y su SHA-256 se registra
  en `03_preparacion_datos/data_manifest.json`.
- **Trazabilidad del experimento:** `05_evaluacion/resumen_ejecucion.json` guarda fecha,
  duración, partición, métricas y versiones de Python/pandas/scikit-learn.
- **Artefactos pesados:** los `.joblib` no se versionan (están en `.gitignore`); se regeneran
  con `make pipeline`.
- **Reproducibilidad:** `uv.lock` se versiona; la semilla es única y global (`42`).

## 9. Definición de terminado (DoD) del proyecto

1. El notebook se ejecuta de inicio a fin sin errores.
2. El dataset se carga o descarga correctamente, con hash registrado.
3. Se reportan nulos y duplicados.
4. Se entrenan baseline y modelo alternativo.
5. Se comparan con accuracy y F1 macro.
6. Se incluye matriz de confusión e interpretación.
7. El modelo final se guarda y se verifica cargándolo desde disco.
8. `make check` está en verde.
9. La documentación (reporte y Scrum ML) está actualizada.

## 10. Historial de decisiones

| Fecha | Decisión | Motivo |
|---|---|---|
| 2026-10-27 | Usar `uv` + src-layout en lugar de `venv` + `requirements.txt` | Reproducibilidad y lockfile determinista |
| 2026-10-28 | Eliminar 68 filas duplicadas (todas de `HOROZ`) | Evitar sesgo por observaciones repetidas |
| 2026-10-28 | Adoptar F1 macro como métrica principal | Clases desbalanceadas 7:1 |
| 2026-10-29 | Descargar el CSV con `certifi` en lugar de `pandas.read_csv` | El certificado del sistema estaba desactualizado |
| 2026-11-03 | Seleccionar Random Forest pese al empate técnico | Importancia de variables y robustez futura, documentando el empate |
| 2026-11-05 | No versionar los `.joblib` | 25 MB por artefacto; se regeneran con `make pipeline` |
| 2026-11-09 | Reorganizar en fases CRISP-DM + capas medallón | La rúbrica premia la trazabilidad por fase; el medallón separa crudo, limpio y listo para modelar |

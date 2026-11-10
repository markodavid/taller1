# AGENTS.md — contexto para agentes

Proyecto académico de Machine Learning (UAO, Gerencia de Proyectos). Antes de tocar código, lee
`CONSTITUTION.md`: es la fuente única de verdad.

## Stack

- Python 3.13 con **uv** (nunca `pip`, nunca `requirements.txt`).
- pandas, NumPy, scikit-learn, Matplotlib, joblib.
- pytest + Ruff + pre-commit.
- src-layout: el paquete vive en `src/taller1/`.

## Comandos

```bash
uv sync
make check        # lint + formato + pruebas
make pipeline     # regenera data/silver, data/gold y la evidencia de cada fase
make notebook     # ejecuta el notebook completo
```

## Reglas del proyecto

1. No modificar `data/bronze/`. La limpieza escribe en `data/silver/` y los splits en
   `data/gold/`.
2. `Class` es la variable objetivo y nunca entra como predictora.
3. El escalamiento va dentro del `Pipeline` (evita fuga de información).
4. Toda partición usa `random_state=42` y `stratify=y`.
5. El criterio de selección es **F1 macro**.
6. Los artefactos de las fases (`02_` a `06_`) se generan; no se editan a mano.
7. Cada cambio significativo actualiza `CONSTITUTION.md` en el mismo commit.

## Búsqueda en el código

Usa `tgrep` en lugar de `grep`/`rg` para búsquedas semánticas en el repositorio
(ver `.opencode/rules/tgrep.md`).

## Documentación viva

- `docs/reporte_crisp_dm.md` — entregable 2.
- `docs/scrum_ml.md` — entregable 3.
- `docs/respuestas_reflexion.md` — anexo de preguntas.
- `README.md` — puerta de entrada pública.

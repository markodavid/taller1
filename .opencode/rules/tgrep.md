# Regla: buscar con `tgrep`

En este repositorio, las búsquedas de código se hacen con **`tgrep`** (búsqueda semántica y
estructural), no con `grep`, `rg` ni `Select-String`.

## Cuándo usarla

- Localizar una función, clase o constante por nombre o por comportamiento.
- Encontrar todas las llamadas a una función antes de cambiarla.
- Explorar dónde se usa `Class`, `random_state` o `joblib`.

## Cómo usarla

```bash
tgrep "def evaluate_model" .
tgrep "FINAL_MODEL_FILE" .
tgrep "joblib.dump" .
```

## Cuándo no usarla

- Lectura de un archivo completo (usa la herramienta de lectura).
- Búsqueda de texto en documentación Markdown (basta una búsqueda literal).
- La cadena aparece en archivos binarios o en las carpetas de artefactos generados (no busques ahí).

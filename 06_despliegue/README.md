# 06 · Despliegue

**Fase CRISP-DM 6 — Deployment**

## Qué se entrega

Una **demo local reproducible**: el modelo final se carga desde disco y clasifica nuevas
mediciones sin reentrenar.

```python
from taller1 import modeling
from taller1.config import FINAL_MODEL_FILE

model = modeling.load_model(FINAL_MODEL_FILE)
variedad = modeling.predict_bean_class(model, fila_con_16_variables)
```

O desde la línea de comandos, para un lote completo:

```bash
uv run taller1 predict --input lote.csv --output 06_despliegue/predicciones_lote.csv
```

## Verificación automática

Cada ejecución de `make pipeline` genera [`ejemplo_prediccion.json`](ejemplo_prediccion.json) con:

- la ruta del modelo usado;
- las 16 medidas de entrada;
- la variedad predicha;
- la clase real, para comparar.

En la última corrida la muestra de prueba se predijo como **SEKER** y su clase real era
**SEKER**.

## Artefactos

| Archivo | Contenido |
|---|---|
| [`ejemplo_prediccion.json`](ejemplo_prediccion.json) | Predicción individual verificada |
| [`predicciones_nuevas.csv`](predicciones_nuevas.csv) | Salida de `taller1 predict` (cuando se ejecuta) |

El modelo binario vive en [`04_modelado/random_forest_drybean.joblib`](../04_modelado/README.md).

## Qué faltaría para producción

1. Validar con imágenes reales de la empresa, no solo con el dataset académico.
2. Definir el costo de cada tipo de error y ajustar el umbral de decisión.
3. Monitorear deriva de datos (cámara, iluminación, calibración).
4. Versionar el modelo y exponerlo como servicio con registro de predicciones.
5. Incorporar color o textura para reducir las confusiones SIRA ↔ DERMASON.

## Evidencia

- Notebook: sección **6. Despliegue**.
- Reporte: [`docs/reporte_crisp_dm.md`](../docs/reporte_crisp_dm.md), sección 6.

# 02 · Comprensión de los datos

**Fase CRISP-DM 2 — Data Understanding**

## Resumen

| Métrica | Valor |
|---|---:|
| Registros originales | 13 611 |
| Variables | 17 (16 numéricas + `Class`) |
| Clases | 7 |
| Valores nulos | 0 |
| Filas duplicadas | 68 (todas de `HOROZ`) |

El dataset crudo se lee desde `data/bronze/dry_bean.csv`. El perfil completo de calidad
—tipos, conteos por clase y estadísticas— queda en [`perfil_datos.json`](perfil_datos.json), y la
distribución visual en [`distribucion_clases.png`](distribucion_clases.png).

## Distribución de clases

| Clase | Registros | % |
|---|---:|---:|
| DERMASON | 3546 | 26.2 % |
| SIRA | 2636 | 19.5 % |
| SEKER | 2027 | 15.0 % |
| HOROZ | 1860 | 13.7 % |
| CALI | 1630 | 12.0 % |
| BARBUNYA | 1322 | 9.8 % |
| BOMBAY | 522 | 3.8 % |

![Distribución de clases](distribucion_clases.png)

## Hallazgos

1. **Sin valores faltantes:** no se requiere imputación.
2. **68 duplicados exactos, todos de `HOROZ`:** al eliminarlos, `HOROZ` pasa de 1928 a 1860
   registros. Es la única clase afectada.
3. **Desbalance 7:1** entre la clase mayoritaria (`DERMASON`) y la minoritaria (`BOMBAY`). Esto
   obliga a estratificar la partición y a usar F1 macro como métrica principal.
4. **Valores extremos legítimos:** los máximos de `Area`, `Perimeter` y `ConvexArea` corresponden
   a granos grandes de `BOMBAY`, no a errores de captura. Se conservan.

## Evidencia

- Notebook: sección **2. Comprensión de los datos**.
- Reporte: [`docs/reporte_crisp_dm.md`](../docs/reporte_crisp_dm.md), sección 2.

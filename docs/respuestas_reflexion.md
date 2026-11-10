# Respuestas de reflexión — Laboratorio Dry Bean

Documento de apoyo al reporte. Cada respuesta se ancla en evidencia concreta del repositorio:
métricas, artefactos o decisiones registradas.

---

## Actividad del Paso 3

1. **¿Cuántas columnas tiene el dataset?** 17: 16 variables predictoras numéricas y la columna
   objetivo `Class`.
2. **¿Cuál es la variable objetivo?** `Class`, que contiene la variedad de frijol.
3. **¿El problema es de clasificación o regresión?** Clasificación multiclase: la salida es una
   de siete categorías, no un valor continuo.

---

## Preguntas del desarrollo

### ¿Las clases están balanceadas? ¿Cómo afecta al entrenamiento?

No. `DERMASON` tiene 3546 registros (26.2 %) y `BOMBAY` 522 (3.8 %): una relación de casi 7 a 1.
El modelo ve muchas más muestras de las clases frecuentes, de modo que aprende mejor sus fronteras
y tiende a predecirlas. Consecuencias y mitigaciones aplicadas:

- La accuracy sola puede ocultar el mal desempeño en la clase minoritaria → se reporta F1 macro.
- La partición es **estratificada** para que train y test conserven la proporción de cada clase.
- El bosque aleatorio usa `class_weight="balanced"` para penalizar más los errores en clases
  pequeñas.

Resultado: `BOMBAY` no queda relegada (F1 = 1.00) y la clase con peor desempeño es `SIRA`
(F1 = 0.87), que no es la minoritaria sino la más parecida a `DERMASON`.

### ¿Por qué F1 macro es más informativo que accuracy cuando las clases no están balanceadas?

Porque promedia el F1 de cada clase con el mismo peso, sin importar cuántos ejemplos tenga. La
accuracy suma aciertos globales: acertar en `DERMASON` (709 casos en prueba) pesa mucho más que
acertar en `BOMBAY` (104). Un modelo que ignorara la clase minoritaria podría mostrar accuracy
alta y, aun así, ser inútil para el control de calidad, donde cada variedad importa por igual.

### ¿Qué clases se confunden más entre sí?

`SIRA` ↔ `DERMASON` (48 y 47 casos), `DERMASON` → `SEKER` (17) y `BARBUNYA` ↔ `CALI` (17 y 11).
La explicación está en las variables de forma y tamaño: `SIRA` y `DERMASON` comparten proporciones
de eje y compacidad; `BARBUNYA` y `CALI` tienen áreas parecidas y difieren sobre todo en el
contorno. `BOMBAY`, mucho más grande, no se confunde con ninguna.

---

## Preguntas finales

### 1. ¿Qué fase de CRISP-DM fue más importante en este laboratorio?

**La comprensión de los datos.** El hallazgo de que los 68 duplicados pertenecían todos a
`HOROZ`, de que no había nulos y de que las clases estaban desbalanceadas 7 a 1 determinó las
decisiones posteriores: limpiar antes de partir, estratificar, usar `class_weight` y elegir F1
macro como métrica principal. Sin esa fase, el equipo habría optimizado accuracy y habría
reportado un resultado engañoso. La segunda más importante fue la **evaluación**, porque el
empate técnico entre los dos modelos obligó a justificar la decisión con criterios de negocio y
no solo con números.

### 2. ¿Qué ventaja ofrece TDSP frente a trabajar con archivos desordenados?

TDSP impone un contrato de carpetas y de artefactos que hace el trabajo **auditable y repetible**:

- `data/bronze` nunca se modifica y su hash queda registrado; `data/silver` es siempre
  reproducible a partir del crudo.
- El código vive en `src/` y no solo en celdas: se puede importar, probar y reutilizar.
- Cada corrida deja métricas, gráficas y un resumen con versiones de librerías en las carpetas de cada fase.
- Cualquier integrante (o el docente) sabe dónde buscar una decisión o un resultado.

Con archivos sueltos, en cambio, cada persona guarda su versión, nadie sabe cuál es el dataset
"bueno" y reproducir un número exige preguntar quién lo obtuvo y cómo.

### 3. ¿Cómo ayuda Scrum ML cuando el resultado del modelo es incierto?

Scrum ML no elimina la incertidumbre: la hace **gestionable**. Los sprints cortos permiten
descubrir temprano que el problema era casi lineal (Sprint 2) y ajustar el esfuerzo en lugar de
descubrirlo al final. El backlog prioriza el baseline antes que el modelo complejo, la Sprint
Review obliga a mostrar evidencia al Product Owner y la retrospectiva convierte los bloqueos
(certificado TLS, estimación de documentación) en acciones concretas para el siguiente ciclo.

### 4. ¿Por qué se usa un modelo baseline?

Porque da un **punto de comparación honesto y barato**. En este proyecto la regresión logística
alcanzó F1 macro 0.9306; el bosque aleatorio, 0.9310. Esa diferencia de 0.0004 demuestra que la
complejidad adicional aporta muy poco y que, si hubiera que priorizar simplicidad y
mantenibilidad, el baseline sería suficiente. Sin baseline, el 0.931 del bosque parecería un
gran logro en lugar de un empate técnico.

### 5. ¿Qué métrica usarías para escoger el mejor modelo y por qué?

**F1 macro**, porque las clases están desbalanceadas y todas las variedades importan por igual en
el control de calidad. Se complementa con la matriz de confusión y el F1 por clase para detectar
si el promedio esconde una clase mal atendida (fue el caso de `SIRA`). La accuracy se reporta
solo como contexto para el negocio.

### 6. ¿Qué harías si una clase tiene muchos más errores que las demás?

1. Revisar la matriz de confusión para identificar **con qué** se confunde.
2. Aumentar el peso de esa clase (`class_weight`) o aplicar sobremuestreo dirigido.
3. Revisar si hay solapamiento real con otra variedad y si faltan variables discriminantes
   (color, textura).
4. Ajustar el umbral de decisión según el costo del error para el negocio.
5. Reportar el F1 por clase y no solo el promedio, para que el problema no quede oculto.

En este proyecto `SIRA` es la clase con peor F1 (0.87) y se confunde con `DERMASON`; la acción
recomendada es incorporar variables de color o textura, no solo reajustar el modelo.

### 7. ¿Qué información necesitarías antes de llevar este modelo a producción?

- **Datos reales de la empresa:** imágenes y mediciones de lotes actuales, para validar que la
  distribución coincide con la del dataset académico.
- **Matriz de costos:** cuánto cuesta cada tipo de error (confundir dos variedades comerciales no
  es lo mismo que rechazar un lote válido).
- **Requisitos operativos:** latencia, formato de entrada, volumen por lote, integración con el
  sistema de calidad.
- **Plan de monitoreo:** deriva de datos por cambios de cámara, iluminación o calibración;
  métricas en producción y alertas.
- **Gobernanza:** versionado del modelo y del dataset, registro de predicciones para auditoría,
  responsable de aprobar actualizaciones.
- **Validación temporal:** desempeño sobre lotes de fechas posteriores, no solo sobre una
  partición aleatoria.

---

## Extensión opcional A — Validación cruzada

La validación cruzada de 3 particiones obtuvo F1 macro **0.9331, 0.9326 y 0.9316**
(media **0.9324**, desviación **0.0006**). La dispersión mínima confirma que el resultado no
depende de una partición afortunada y respalda la decisión de pasar a despliegue.

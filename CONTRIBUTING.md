# Contribuir al proyecto

## 1. Preparar el entorno

```bash
git clone <url-del-repositorio>
cd taller1
uv sync
uv run pre-commit install
make check
```

## 2. Flujo de trabajo

1. Crea una rama desde `main`: `git switch -c feat/mi-aporte`.
2. Haz cambios pequeños y verificables.
3. Ejecuta `make check` (lint + formato + pruebas).
4. Commitea con [Conventional Commits](https://www.conventionalcommits.org/):
   `feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `chore:`.
5. Abre un Pull Request describiendo el cambio, la evidencia y cómo probarlo.
6. Solicita revisión a otro integrante del equipo.

## 3. Estándares

- Ruff impone estilo y orden de imports; no se discute en revisión, se ejecuta `make format`.
- Cada función pública lleva docstring y anotaciones de tipo.
- Las pruebas siguen el patrón AAA y no dependen de internet (datos sintéticos).
- No se modifican archivos de `data/bronze/` ni los artefactos de las fases a mano: se regeneran
  con `make pipeline`.
- Si el cambio altera arquitectura, métricas o stack, actualiza `CONSTITUTION.md` en el mismo
  commit.

## 4. Reportar un problema

Abre un issue con el template correspondiente e incluye:

- Qué esperabas que pasara y qué pasó.
- Comando ejecutado y salida relevante.
- Versión de Python (`uv run python --version`) y sistema operativo.

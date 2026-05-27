#!/usr/bin/env bash
# Ejecuta complementaria all instructor para un mes/año (o rango vía variables de entorno).
#
# Normalmente lo invoca run_complementaria_menu.sh con:
#   COMPLEMENTARIA_ANIOS="2024"
#   COMPLEMENTARIA_MESES="03"

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
PYTHON="${PYTHON:-python3}"

if [[ -n "${COMPLEMENTARIA_ANIOS:-}" ]]; then
  read -r -a ANIOS <<< "$COMPLEMENTARIA_ANIOS"
else
  ANIOS=(2017 2018 2019 2020 2021 2022 2023 2024 2025)
fi

if [[ -n "${COMPLEMENTARIA_MESES:-}" ]]; then
  read -r -a MESES <<< "$COMPLEMENTARIA_MESES"
else
  MESES=(01 02 03 04 05 06 07 08 09 10 11 12)
fi

MAX_REINTENTOS=3

for anio in "${ANIOS[@]}"; do
  anio_corto=${anio: -2}

  for mes in "${MESES[@]}"; do
    periodo="${mes}_${anio_corto}"

    echo "==============================="
    echo "Procesando periodo $periodo (instructor)"
    echo "==============================="

    intento=1
    success=0

    while [[ $intento -le $MAX_REINTENTOS ]]; do
      echo "Ejecutando instructor intento $intento periodo $periodo"

      if "$PYTHON" "$SCRIPT_DIR/script.py" --periodo "$periodo"; then
        echo "OK instructor $periodo"
        success=1
        break
      else
        echo "ERROR instructor $periodo"
        ((intento++)) || true
      fi
    done

    if [[ $success -eq 0 ]]; then
      echo "FALLO DEFINITIVO instructor $periodo"
    fi
  done
done


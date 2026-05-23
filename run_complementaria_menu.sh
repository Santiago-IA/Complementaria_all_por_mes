#!/usr/bin/env bash
# Menú: elige división (all|month|year) y tipo (aprendiz|ficha|instructor), luego hace
#   cd <carpeta_del_módulo>  y  exec python ./script.py ...
# La carpeta es absoluta bajo la raíz del repo (ROOT).
# Uso: ./run_complementaria_menu.sh   |   PYTHON=python3 ./run_complementaria_menu.sh
#
# Si ves: env: 'bash\r': No such file or directory  → el .sh tiene CRLF; en Linux:
#   sed -i 's/\r$//' run_complementaria_menu.sh

set -euo pipefail

PYTHON="${PYTHON:-python}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"

echo "=========================================="
echo "  Complementaria update — menú de ejecución"
echo "  Raíz del repo: $ROOT"
echo "=========================================="
echo ""
echo "División (rango de fechas del script):"
echo "  1) all   — complementaria_update_all"
echo "  2) month — complementaria_update_month"
echo "  3) year  — complementaria_update_year"
read -r -p "Elige [1-3] (Enter = 1): " div_choice
div_choice="${div_choice:-1}"
case "$div_choice" in
  1) DIV="all" ;;
  2) DIV="month" ;;
  3) DIV="year" ;;
  *) echo "Opción no válida."; exit 1 ;;
esac

echo ""
echo "Proceso / entidad:"
echo "  1) aprendiz   — entity 4 (registro académico)"
echo "  2) ficha      — entity 2 (ficha caracterización)"
echo "  3) instructor — entity 6 (instructor x ficha)"
read -r -p "Elige [1-3] (Enter = 2): " type_choice
type_choice="${type_choice:-2}"
case "$type_choice" in
  1) TYPE="aprendiz"; ENTITY=4 ;;
  2) TYPE="ficha"; ENTITY=2 ;;
  3) TYPE="instructor"; ENTITY=6 ;;
  *) echo "Opción no válida."; exit 1 ;;
esac

TARGET_DIR="$ROOT/complementaria_update_${DIV}/complementaria_update_${DIV}_${TYPE}"
if [[ ! -d "$TARGET_DIR" ]]; then
  echo "No existe la carpeta: $TARGET_DIR"
  exit 1
fi
if [[ ! -f "$TARGET_DIR/script.py" ]]; then
  echo "No se encontró script.py en: $TARGET_DIR"
  exit 1
fi

echo ""
echo "Modo de ejecución:"
echo "  1) Proceso interno  — ./script.py --internal=s --entity=... --type_search=..."
echo "  2) Excel            — ./script.py --excel=s"
echo "  3) Índice cambio    — ./script.py --internal=n --entity=... [--ica_id=...]"
read -r -p "Elige [1-3] (Enter = 1): " mode_choice
mode_choice="${mode_choice:-1}"

# Solo argumentos de script.py; el cd a la división se hace al ejecutar.
ARGS=()
case "$mode_choice" in
  1)
    case "$DIV" in
      all)   default_ts="all" ;;
      month) default_ts="month" ;;
      year)  default_ts="year" ;;
      *) default_ts="all" ;;
    esac
    read -r -p "type_search (month|year|all) [${default_ts}]: " TS
    TS="${TS:-$default_ts}"
    ARGS=(--internal=s --entity="$ENTITY" --type_search="$TS")
    if [[ "$DIV" == "month" || "$DIV" == "year" ]]; then
      read -r -p "days (solo month/year) [90]: " DAYS
      DAYS="${DAYS:-90}"
      ARGS+=(--days="$DAYS")
    fi
    ;;
  2)
    ARGS=(--excel=s)
    ;;
  3)
    read -r -p "ica_id [0 = usar máximo ICA en Sofía]: " ICA
    ICA="${ICA:-0}"
    ARGS=(--internal=n --entity="$ENTITY" --ica_id="$ICA")
    ;;
  *)
    echo "Opción no válida."; exit 1 ;;
esac

echo ""
echo "Se hará:"
echo "  cd \"$TARGET_DIR\""
echo "  $PYTHON ./script.py ${ARGS[*]}"
echo ""
read -r -p "¿Ejecutar ahora? [s/N]: " confirm
case "$confirm" in
  s|S|y|Y) ;;
  *) echo "Cancelado."; exit 0 ;;
esac

cd "$TARGET_DIR" || { echo "Error: no se pudo entrar a $TARGET_DIR"; exit 1; }
echo "PWD actual: $(pwd)"
exec "$PYTHON" ./script.py "${ARGS[@]}"

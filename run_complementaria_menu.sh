#!/usr/bin/env bash
# Complementaria update all — ejecutar FICHA por mes
#
# Uso: ./run_complementaria_menu.sh
#   PYTHON=python3 ./run_complementaria_menu.sh
#
# Ver proceso tmux:
#   tmux ls
#   tmux a -t complementaria_ficha

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
FICHA_DIR="$ROOT/complementaria_update_all/complementaria_update_all_ficha"
RUN_SCRIPT="$FICHA_DIR/run_complementaria_all_por_mes_ficha.sh"
PYTHON="${PYTHON:-python3}"
TMUX_SESSION="complementaria_ficha"

if [[ ! -d "$FICHA_DIR" ]]; then
  echo "No existe la carpeta de ficha: $FICHA_DIR"
  exit 1
fi

if [[ ! -f "$FICHA_DIR/script.py" ]]; then
  echo "No se encontró script.py en: $FICHA_DIR"
  exit 1
fi

echo "=============================================="
echo "  Complementaria update all — FICHA"
echo "  $FICHA_DIR"
echo "=============================================="
echo ""
echo "Indica el periodo a procesar (fichas con FIC_FCH_INICIALIZACION en ese mes)."
echo ""

read -r -p "Mes (01-12): " INPUT_MES
if [[ ! "$INPUT_MES" =~ ^(0[1-9]|1[0-2])$ ]]; then
  echo "Mes inválido. Use formato 01-12."
  exit 1
fi

read -r -p "Año (ej: 2024): " INPUT_ANIO
if [[ ! "$INPUT_ANIO" =~ ^(19|20)[0-9]{2}$ ]]; then
  echo "Año inválido. Use 4 dígitos, ej: 2024."
  exit 1
fi

LOG_FILE="log_ficha_${INPUT_MES}_${INPUT_ANIO}.txt"
PERIODO="${INPUT_MES}_${INPUT_ANIO: -2}"

echo ""
echo "Modo de ejecución:"
echo "  1) tmux (segundo plano, guarda log en la carpeta ficha)"
echo "  2) Directo (primer plano)"
read -r -p "Elige [1-2] (Enter = 1): " EXEC_MODE
EXEC_MODE="${EXEC_MODE:-1}"

echo ""
echo "Resumen:"
echo "  División : ficha"
echo "  Periodo  : $PERIODO  (mes ${INPUT_MES}/${INPUT_ANIO})"
echo "  Log      : $FICHA_DIR/$LOG_FILE"
if [[ "$EXEC_MODE" == "1" ]]; then
  echo "  Modo     : tmux ($TMUX_SESSION)"
else
  echo "  Modo     : directo"
fi
echo ""

read -r -p "¿Ejecutar ahora? [S/n]: " CONFIRM
case "${CONFIRM:-S}" in
  s|S|y|Y|"") ;;
  *) echo "Cancelado."; exit 0 ;;
esac

export COMPLEMENTARIA_ANIOS="$INPUT_ANIO"
export COMPLEMENTARIA_MESES="$INPUT_MES"
export PYTHON

if [[ "$EXEC_MODE" == "1" ]]; then
  if ! command -v tmux >/dev/null 2>&1; then
    echo "tmux no está instalado. Ejecutando en primer plano..."
    EXEC_MODE=2
  fi
fi

if [[ "$EXEC_MODE" == "1" ]]; then
  if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
    echo "La sesión tmux '$TMUX_SESSION' ya existe."
    read -r -p "¿Terminarla y relanzar? [s/N]: " KILL_CHOICE
    case "$KILL_CHOICE" in
      s|S|y|Y) tmux kill-session -t "$TMUX_SESSION" ;;
      *) echo "Cancelado."; exit 0 ;;
    esac
  fi

  CMD="cd \"$FICHA_DIR\" && export COMPLEMENTARIA_ANIOS=\"$INPUT_ANIO\" COMPLEMENTARIA_MESES=\"$INPUT_MES\" PYTHON=\"$PYTHON\" && ./run_complementaria_all_por_mes_ficha.sh | tee \"$LOG_FILE\""
  tmux new -d -s "$TMUX_SESSION" bash -lc "$CMD"
  echo ""
  echo "Proceso iniciado en tmux: $TMUX_SESSION"
  echo "Log: $FICHA_DIR/$LOG_FILE"
  echo ""
  echo "Ver sesiones : tmux ls"
  echo "Adjuntarse   : tmux a -t $TMUX_SESSION"
else
  (
    cd "$FICHA_DIR"
    ./run_complementaria_all_por_mes_ficha.sh | tee "$LOG_FILE"
  )
fi

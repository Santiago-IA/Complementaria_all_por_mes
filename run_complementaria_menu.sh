#!/usr/bin/env bash
# Complementaria update all — ejecutar por mes (ficha / aprendiz / instructor)
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
APRENDIZ_DIR="$ROOT/complementaria_update_all/complementaria_update_all_aprendiz"
INSTRUCTOR_DIR="$ROOT/complementaria_update_all/complementaria_update_all_instructor"
PYTHON="${PYTHON:-python3}"
TMUX_SESSION="complementaria_ficha"

echo "=============================================="
echo "  Complementaria update all — por mes"
echo "=============================================="
echo ""
echo "Elige la división a ejecutar:"
echo "  1) ficha"
echo "  2) aprendiz"
echo "  3) instructor"
echo ""

read -r -p "División [1-3] (Enter = 1): " DIV_CHOICE
DIV_CHOICE="${DIV_CHOICE:-1}"

case "$DIV_CHOICE" in
  1)
    DIVISION="ficha"
    TARGET_DIR="$FICHA_DIR"
    RUN_SCRIPT="$FICHA_DIR/run_complementaria_all_por_mes_ficha.sh"
    TMUX_SESSION="complementaria_ficha"
    ;;
  2)
    DIVISION="aprendiz"
    TARGET_DIR="$APRENDIZ_DIR"
    RUN_SCRIPT="$APRENDIZ_DIR/run_complementaria_all_por_mes_aprendiz.sh"
    TMUX_SESSION="complementaria_aprendiz"
    ;;
  3)
    DIVISION="instructor"
    TARGET_DIR="$INSTRUCTOR_DIR"
    RUN_SCRIPT="$INSTRUCTOR_DIR/run_complementaria_all_por_mes_instructor.sh"
    TMUX_SESSION="complementaria_instructor"
    ;;
  *)
    echo "Opción inválida. Use 1, 2 o 3."
    exit 1
    ;;
esac

if [[ ! -d "$TARGET_DIR" ]]; then
  echo "No existe la carpeta de $DIVISION: $TARGET_DIR"
  exit 1
fi

if [[ ! -f "$TARGET_DIR/script.py" ]]; then
  echo "No se encontró script.py en: $TARGET_DIR"
  exit 1
fi

if [[ ! -f "$RUN_SCRIPT" ]]; then
  echo "No se encontró el script de ejecución: $RUN_SCRIPT"
  exit 1
fi

echo ""
echo "División seleccionada: $DIVISION"
echo "Carpeta: $TARGET_DIR"
echo ""
echo "Indica el periodo a procesar (fichas con FIC_FCH_INICIALIZACION en ese mes)."
echo ""

read -r -p "Mes (01-12): " INPUT_MES
if [[ "$INPUT_MES" =~ ^[1-9]$ ]]; then
  INPUT_MES="0$INPUT_MES"
fi
if [[ ! "$INPUT_MES" =~ ^(0[1-9]|1[0-2])$ ]]; then
  echo "Mes inválido. Use 01-12 (también vale 1-9, se convierte a 01-09)."
  exit 1
fi

read -r -p "Año (ej: 2024): " INPUT_ANIO
if [[ ! "$INPUT_ANIO" =~ ^(19|20)[0-9]{2}$ ]]; then
  echo "Año inválido. Use 4 dígitos, ej: 2024."
  exit 1
fi

LOG_FILE="log_${DIVISION}_${INPUT_MES}_${INPUT_ANIO}.txt"
PERIODO="${INPUT_MES}_${INPUT_ANIO: -2}"

echo ""
echo "Modo de ejecución:"
echo "  1) tmux (segundo plano, guarda log en la carpeta ficha)"
echo "  2) Directo (primer plano)"
read -r -p "Elige [1-2] (Enter = 1): " EXEC_MODE
EXEC_MODE="${EXEC_MODE:-1}"

echo ""
echo "Resumen:"
echo "  División : $DIVISION"
echo "  Periodo  : $PERIODO  (mes ${INPUT_MES}/${INPUT_ANIO})"
echo "  Log      : $TARGET_DIR/$LOG_FILE"
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

  CMD="cd \"$TARGET_DIR\" && export COMPLEMENTARIA_ANIOS=\"$INPUT_ANIO\" COMPLEMENTARIA_MESES=\"$INPUT_MES\" PYTHON=\"$PYTHON\" && bash \"./$(basename "$RUN_SCRIPT")\" 2>&1 | tee \"$LOG_FILE\""
  tmux new -d -s "$TMUX_SESSION" bash -c "$CMD"
  sleep 1
  if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
    echo ""
    echo "Proceso iniciado en tmux: $TMUX_SESSION"
    echo "Log: $TARGET_DIR/$LOG_FILE"
    echo ""
    echo "Ver sesiones : tmux ls"
    echo "Adjuntarse   : tmux a -t $TMUX_SESSION"
  else
    echo ""
    echo "ERROR: la sesión tmux terminó al instante. Revisa el log:"
    echo "  tail -50 \"$TARGET_DIR/$LOG_FILE\""
    echo ""
    echo "Causa habitual: scripts .sh subidos con finales Windows (CRLF)."
    echo "  Vuelva a desplegar desde el repositorio (los .sh deben tener solo LF)."
    exit 1
  fi
else
  (
    cd "$TARGET_DIR"
    bash "./$(basename "$RUN_SCRIPT")" 2>&1 | tee "$LOG_FILE"
  )
fi

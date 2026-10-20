#!/usr/bin/env bash
# Complementaria update all — ejecutar por mes (ficha / aprendiz / instructor)
#
# Uso: ./run_complementaria_menu.sh
#   PYTHON=python3 ./run_complementaria_menu.sh
#
# Ver proceso tmux:
#   tmux ls
#   tmux a -t complementaria_all
#   tmux a -t complementaria_ficha

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"
FICHA_DIR="$ROOT/complementaria_update_all/complementaria_update_all_ficha"
APRENDIZ_DIR="$ROOT/complementaria_update_all/complementaria_update_all_aprendiz"
INSTRUCTOR_DIR="$ROOT/complementaria_update_all/complementaria_update_all_instructor"
PYTHON="${PYTHON:-python3}"

# Normaliza un mes a 01-12. Acepta 1-9 o 01-12.
normalize_month() {
  local m="$1"
  if [[ "$m" =~ ^[1-9]$ ]]; then
    m="0$m"
  fi
  if [[ ! "$m" =~ ^(0[1-9]|1[0-2])$ ]]; then
    return 1
  fi
  printf '%s' "$m"
}

# Expande meses: "01" | "1" | "01-12" | "1-12" | "todos" | vacío=todos
expand_months() {
  local raw="${1:-}"
  raw="$(echo "$raw" | tr '[:upper:]' '[:lower:]' | xargs)"

  if [[ -z "$raw" || "$raw" == "todos" || "$raw" == "all" || "$raw" == "*" ]]; then
    printf '%s' "01 02 03 04 05 06 07 08 09 10 11 12"
    return 0
  fi

  if [[ "$raw" =~ ^([0-9]{1,2})-([0-9]{1,2})$ ]]; then
    local start end
    start="$(normalize_month "${BASH_REMATCH[1]}")" || return 1
    end="$(normalize_month "${BASH_REMATCH[2]}")" || return 1
    local s=$((10#$start)) e=$((10#$end))
    if (( s > e )); then
      return 1
    fi
    local out=() m
    for ((m=s; m<=e; m++)); do
      out+=("$(printf '%02d' "$m")")
    done
    printf '%s' "${out[*]}"
    return 0
  fi

  local one
  one="$(normalize_month "$raw")" || return 1
  printf '%s' "$one"
}

# Expande años: "2024" | "2024-2026"
expand_years() {
  local raw="${1:-}"
  raw="$(echo "$raw" | xargs)"

  if [[ "$raw" =~ ^((19|20)[0-9]{2})-((19|20)[0-9]{2})$ ]]; then
    local start="${BASH_REMATCH[1]}"
    local end="${BASH_REMATCH[3]}"
    if (( start > end )); then
      return 1
    fi
    local out=() y
    for ((y=start; y<=end; y++)); do
      out+=("$y")
    done
    printf '%s' "${out[*]}"
    return 0
  fi

  if [[ "$raw" =~ ^(19|20)[0-9]{2}$ ]]; then
    printf '%s' "$raw"
    return 0
  fi

  return 1
}

# Valida que exista carpeta, script.py y runner de una división.
validate_division() {
  local name="$1" dir="$2" run_script="$3"
  if [[ ! -d "$dir" ]]; then
    echo "No existe la carpeta de $name: $dir"
    return 1
  fi
  if [[ ! -f "$dir/script.py" ]]; then
    echo "No se encontró script.py en: $dir"
    return 1
  fi
  if [[ ! -f "$run_script" ]]; then
    echo "No se encontró el script de ejecución: $run_script"
    return 1
  fi
  return 0
}

# Ejecuta un runner de división (directo). Usa variables globales ANIOS_LIST MESES_LIST PYTHON.
run_one_division() {
  local name="$1" dir="$2" run_script="$3" log_file="$4"
  echo ""
  echo "##############################################"
  echo "# División: $name"
  echo "# Log: $dir/$log_file"
  echo "##############################################"
  (
    cd "$dir"
    export COMPLEMENTARIA_ANIOS="$ANIOS_LIST"
    export COMPLEMENTARIA_MESES="$MESES_LIST"
    export PYTHON
    bash "./$(basename "$run_script")" 2>&1 | tee "$log_file"
  )
}

echo "=============================================="
echo "  Complementaria update all — por mes"
echo "=============================================="
echo ""
echo "Elige la división a ejecutar:"
echo "  1) ficha"
echo "  2) aprendiz"
echo "  3) instructor"
echo "  4) todas (ficha → aprendiz → instructor)"
echo ""

read -r -p "División [1-4] (Enter = 4): " DIV_CHOICE
DIV_CHOICE="${DIV_CHOICE:-4}"

JOBS=()  # cada item: name|dir|run_script|tmux_session
case "$DIV_CHOICE" in
  1)
    JOBS+=("ficha|$FICHA_DIR|$FICHA_DIR/run_complementaria_all_por_mes_ficha.sh|complementaria_ficha")
    ;;
  2)
    JOBS+=("aprendiz|$APRENDIZ_DIR|$APRENDIZ_DIR/run_complementaria_all_por_mes_aprendiz.sh|complementaria_aprendiz")
    ;;
  3)
    JOBS+=("instructor|$INSTRUCTOR_DIR|$INSTRUCTOR_DIR/run_complementaria_all_por_mes_instructor.sh|complementaria_instructor")
    ;;
  4)
    JOBS+=("ficha|$FICHA_DIR|$FICHA_DIR/run_complementaria_all_por_mes_ficha.sh|complementaria_ficha")
    JOBS+=("aprendiz|$APRENDIZ_DIR|$APRENDIZ_DIR/run_complementaria_all_por_mes_aprendiz.sh|complementaria_aprendiz")
    JOBS+=("instructor|$INSTRUCTOR_DIR|$INSTRUCTOR_DIR/run_complementaria_all_por_mes_instructor.sh|complementaria_instructor")
    ;;
  *)
    echo "Opción inválida. Use 1, 2, 3 o 4."
    exit 1
    ;;
esac

for job in "${JOBS[@]}"; do
  IFS='|' read -r DIVISION TARGET_DIR RUN_SCRIPT _ <<< "$job"
  validate_division "$DIVISION" "$TARGET_DIR" "$RUN_SCRIPT" || exit 1
done

if [[ "${#JOBS[@]}" -eq 3 ]]; then
  DIVISION_LABEL="todas (ficha → aprendiz → instructor)"
  TMUX_SESSION="complementaria_all"
else
  IFS='|' read -r DIVISION TARGET_DIR RUN_SCRIPT TMUX_SESSION <<< "${JOBS[0]}"
  DIVISION_LABEL="$DIVISION"
fi

echo ""
echo "División seleccionada: $DIVISION_LABEL"
echo ""
echo "Indica el periodo a procesar (fichas con FIC_FCH_INICIALIZACION en ese rango)."
echo ""
echo "Meses — ejemplos:"
echo "  01          → un mes"
echo "  01-12       → todos los meses"
echo "  Enter/todos → todos los meses"
echo ""

read -r -p "Mes(es) [Enter = 01-12]: " INPUT_MES
if ! MESES_LIST="$(expand_months "${INPUT_MES:-}")"; then
  echo "Mes inválido. Use 01, 01-12, o Enter para todos."
  exit 1
fi

echo ""
echo "Años — ejemplos:"
echo "  2024        → un año"
echo "  2024-2026   → rango de años"
echo ""

read -r -p "Año(s) (ej: 2024-2026): " INPUT_ANIO
if ! ANIOS_LIST="$(expand_years "${INPUT_ANIO:-}")"; then
  echo "Año inválido. Use 2024 o 2024-2026."
  exit 1
fi

# Etiqueta corta para el nombre del log
MES_TAG="${MESES_LIST// /_}"
if [[ "$MESES_LIST" == "01 02 03 04 05 06 07 08 09 10 11 12" ]]; then
  MES_TAG="01-12"
elif [[ "$MESES_LIST" == *" "* ]]; then
  first_m="${MESES_LIST%% *}"
  last_m="${MESES_LIST##* }"
  MES_TAG="${first_m}-${last_m}"
fi

ANIO_TAG="${ANIOS_LIST// /_}"
if [[ "$ANIOS_LIST" == *" "* ]]; then
  first_a="${ANIOS_LIST%% *}"
  last_a="${ANIOS_LIST##* }"
  ANIO_TAG="${first_a}-${last_a}"
fi

PERIODO_DESC="meses [${MESES_LIST}] × años [${ANIOS_LIST}]"

echo ""
echo "Modo de ejecución:"
echo "  1) tmux (segundo plano; recomendado para rangos largos)"
echo "  2) Directo (primer plano)"
read -r -p "Elige [1-2] (Enter = 1): " EXEC_MODE
EXEC_MODE="${EXEC_MODE:-1}"

echo ""
echo "Resumen:"
echo "  División : $DIVISION_LABEL"
echo "  Periodo  : $PERIODO_DESC"
echo "  Logs     :"
for job in "${JOBS[@]}"; do
  IFS='|' read -r name dir _ _ <<< "$job"
  echo "             $dir/log_${name}_${MES_TAG}_${ANIO_TAG}.txt"
done
if [[ "$EXEC_MODE" == "1" ]]; then
  echo "  Modo     : tmux ($TMUX_SESSION)"
else
  echo "  Modo     : directo"
fi
echo ""
if [[ "${#JOBS[@]}" -eq 3 ]]; then
  echo "  Orden    : 1) ficha  →  2) aprendiz  →  3) instructor"
fi
echo "  Nota     : corre mes a mes en secuencia (puede tardar horas/días)."
echo ""

read -r -p "¿Ejecutar ahora? [S/n]: " CONFIRM
case "${CONFIRM:-S}" in
  s|S|y|Y|"") ;;
  *) echo "Cancelado."; exit 0 ;;
esac

export COMPLEMENTARIA_ANIOS="$ANIOS_LIST"
export COMPLEMENTARIA_MESES="$MESES_LIST"
export PYTHON

if [[ "$EXEC_MODE" == "1" ]]; then
  if ! command -v tmux >/dev/null 2>&1; then
    echo "tmux no está instalado. Ejecutando en primer plano..."
    EXEC_MODE=2
  fi
fi

# Construye el bloque bash que corre todas las divisiones elegidas en orden.
build_run_block() {
  local block=""
  local job name dir run_script log_file
  for job in "${JOBS[@]}"; do
    IFS='|' read -r name dir run_script _ <<< "$job"
    log_file="log_${name}_${MES_TAG}_${ANIO_TAG}.txt"
    block+="
echo ''
echo '##############################################'
echo '# División: $name'
echo '# Log: $dir/$log_file'
echo '##############################################'
cd \"$dir\"
export COMPLEMENTARIA_ANIOS=\"$ANIOS_LIST\"
export COMPLEMENTARIA_MESES=\"$MESES_LIST\"
export PYTHON=\"$PYTHON\"
bash \"./$(basename "$run_script")\" 2>&1 | tee \"$log_file\"
"
  done
  block+="
echo ''
echo '##############################################'
echo '# FIN — todas las divisiones solicitadas'
echo '##############################################'
"
  printf '%s' "$block"
}

if [[ "$EXEC_MODE" == "1" ]]; then
  if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
    echo "La sesión tmux '$TMUX_SESSION' ya existe."
    read -r -p "¿Terminarla y relanzar? [s/N]: " KILL_CHOICE
    case "$KILL_CHOICE" in
      s|S|y|Y) tmux kill-session -t "$TMUX_SESSION" ;;
      *) echo "Cancelado."; exit 0 ;;
    esac
  fi

  RUN_BLOCK="$(build_run_block)"
  # Log maestro en la raíz del proyecto cuando son todas
  if [[ "${#JOBS[@]}" -eq 3 ]]; then
    MASTER_LOG="$ROOT/log_all_${MES_TAG}_${ANIO_TAG}.txt"
    CMD="cd \"$ROOT\" && { $RUN_BLOCK; } 2>&1 | tee \"$MASTER_LOG\""
  else
    IFS='|' read -r name dir _ _ <<< "${JOBS[0]}"
    MASTER_LOG="$dir/log_${name}_${MES_TAG}_${ANIO_TAG}.txt"
    CMD="{ $RUN_BLOCK; }"
  fi

  tmux new -d -s "$TMUX_SESSION" bash -c "$CMD"
  sleep 1
  if tmux has-session -t "$TMUX_SESSION" 2>/dev/null; then
    echo ""
    echo "Proceso iniciado en tmux: $TMUX_SESSION"
    if [[ "${#JOBS[@]}" -eq 3 ]]; then
      echo "Log maestro: $MASTER_LOG"
    fi
    echo "Logs por división:"
    for job in "${JOBS[@]}"; do
      IFS='|' read -r name dir _ _ <<< "$job"
      echo "  - $dir/log_${name}_${MES_TAG}_${ANIO_TAG}.txt"
    done
    echo ""
    echo "Ver sesiones : tmux ls"
    echo "Adjuntarse   : tmux a -t $TMUX_SESSION"
  else
    echo ""
    echo "ERROR: la sesión tmux terminó al instante."
    if [[ "${#JOBS[@]}" -eq 3 ]]; then
      echo "  tail -50 \"$MASTER_LOG\""
    fi
    echo ""
    echo "Causa habitual: scripts .sh subidos con finales Windows (CRLF)."
    echo "  Vuelva a desplegar desde el repositorio (los .sh deben tener solo LF)."
    exit 1
  fi
else
  for job in "${JOBS[@]}"; do
    IFS='|' read -r name dir run_script _ <<< "$job"
    run_one_division "$name" "$dir" "$run_script" "log_${name}_${MES_TAG}_${ANIO_TAG}.txt"
  done
  echo ""
  echo "FIN — todas las divisiones solicitadas."
fi

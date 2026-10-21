# Complementaria update all — por mes

## Cómo ejecutar

**Solo Linux.** Abre la terminal en **esta carpeta** (donde está `run_complementaria_menu.sh`).

### Primera vez

```bash
chmod +x run_complementaria_menu.sh
# si el .sh vino de Windows:
sed -i 's/\r$//' run_complementaria_menu.sh
```

### Cada vez

```bash
./run_complementaria_menu.sh
```

**Ficha** filtra el periodo por **`FIC_FCH_REGISTRO`**. Aprendiz/instructor siguen con `FIC_FCH_INICIALIZACION`.

Te preguntará:

0. **División** → `1` ficha · `2` aprendiz · `3` instructor · **`4` todas** (recomendado)
1. **Mes(es)** → `01`, `01-12`, o Enter = todos
2. **Año(s)** → `2024` o `2024-2026`
3. **Modo** → `1` = tmux (recomendado para rangos largos) · `2` = directo
4. **¿Ejecutar?** → `S` o Enter

### Ejemplo: depurar 2024–2026 (ficha + aprendiz + instructor)

```
División [1-4] (Enter = 4): 4
Mes(es) [Enter = 01-12]: 01-12
Año(s) (ej: 2024-2026): 2024-2026
Elige [1-2]: 1
¿Ejecutar ahora? [S/n]: S
```

Orden interno: **ficha → aprendiz → instructor**, mes a mes (36 periodos × 3 divisiones).

Ver progreso:

```bash
tmux a -t complementaria_all
```

(salir sin matar: `Ctrl+b` luego `d`)

### Logs

- Maestro (opción 4): `log_all_01-12_2024-2026.txt` (raíz del proyecto)
- Por división:
  - `complementaria_update_all/..._ficha/log_ficha_01-12_2024-2026.txt`
  - `..._aprendiz/log_aprendiz_01-12_2024-2026.txt`
  - `..._instructor/log_instructor_01-12_2024-2026.txt`

Al terminar cada mes verás: `OK <division> MM_YY` (ej: `OK ficha 01_24`)

---

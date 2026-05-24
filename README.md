# Complementaria update all — FICHA por mes

## Cómo ejecutar

**Solo Linux.** Abre la terminal en **esta carpeta** (donde está `run_complementaria_menu.sh`).

### Primera vez

```bash
chmod +x run_complementaria_menu.sh
```

### Cada vez que quieras correr un mes

```bash
./run_complementaria_menu.sh
```

Te preguntará:

1. **Mes** → escribe el mes con 2 números: `01` a `12`  
   (enero = `01`, marzo = `03`, diciembre = `12`)

2. **Año** → escribe el año completo: `2024`, `2025`, etc.

3. **Modo** → `2` si quieres ver todo en pantalla (recomendado). `1` o Enter = segundo plano.

4. **¿Ejecutar?** → `S` o Enter.

### Ejemplo (enero 2024)

```
Mes (01-12): 01
Año (ej: 2024): 2024
Elige [1-2]: 2
¿Ejecutar ahora? [S/n]: S
```

Al terminar bien verás: `OK ficha 01_24`

### No uses

- `01-24` ni `01/2024` en el mes — solo el mes (`01`), el año va aparte.

### Log

```
complementaria_update_all/complementaria_update_all_ficha/log_ficha_01_2024.txt
```
(cambia `01` y `2024` según lo que hayas puesto)

---


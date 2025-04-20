# Análisis de Co-ocurrencia de Partes con Similitud de Coseno

Este repositorio contiene un script en Python para descubrir y visualizar relaciones entre piezas (`part_nbr_MOD`) en transacciones de facturación. Aprovecha técnicas de muestreo de datos, matrices dispersas de co-ocurrencia y similitud de coseno para generar un heatmap de las piezas más frecuentes y un CSV con todas las relaciones cuantificadas.

---

## 🗂 Estructura del Proyecto
```bash
├── README.md              # Documentación del proyecto
├── requirements.txt       # Dependencias necesarias
├── analysis.py            # Script principal de análisis
└── data/
    ├── input.csv          # Datos originales
    ├── heatmap.png        # Heatmap de salida
    └── relations.csv      # CSV con relaciones calculadas
```

---

## 🚀 Requisitos
- Python 3.8 o superior
- pandas
- numpy
- scipy
- scikit-learn
- matplotlib
- seaborn

Instala todas las dependencias con:
```bash
pip install -r requirements.txt
```

---

## ⚙️ Configuración
En `analysis.py`, ajusta los siguientes parámetros antes de ejecutar:

| Variable            | Descripción                                        | Valor por defecto |
|---------------------|----------------------------------------------------|-------------------|
| `file_path`         | Ruta del CSV de entrada                            | `"data/input.csv"` |
| `sample_frac`       | Fracción de filas a tomar (muestra)                | `0.5`             |
| `min_transactions`  | Umbral mínimo de facturas para filtrar piezas      | `50`              |
| `top_n`             | Número de piezas frecuentes a visualizar en heatmap| `10`              |
| `heatmap_path`      | Ruta de salida del gráfico PNG                     | `"data/heatmap.png"`|
| `output_path`       | Ruta de salida del CSV de relaciones               | `"data/relations.csv"`|

---

## 🔍 Flujo de Ejecución
1. **Carga y muestreo**: Se lee el CSV y se toma una muestra aleatoria (`sample_frac`) para reducir memoria y tiempo de cómputo.
2. **Filtrado inicial**: Se descartan filas sin valor en `part_nbr_MOD` y se cuentan transacciones por pieza.
3. **Selección de piezas frecuentes**: Solo se incluyen piezas que aparecen en al menos `min_transactions` facturas.
4. **Matriz dispersa de co-ocurrencia**:
   - Se emplea `scipy.sparse.lil_matrix` para registrar pares de piezas que coexisten en la misma factura.
   - Las matrices dispersas ahorran memoria al almacenar solo elementos no nulos, ideal para datos escasamente conectados.
5. **Cálculo de similitud de coseno**:
   - Se transforman los vectores de co-ocurrencia en una matriz (densa durante el cálculo) y se usa `cosine_similarity` de scikit-learn.
   - La similitud de coseno mide el ángulo entre vectores: 1 = idéntico, 0 = sin correlación.
6. **Generación del heatmap**:
   - Con seaborn, se crea un mapa de calor de la submatriz de `top_n` piezas más frecuentes.
   - Se anota cada celda con el valor de similitud redondeado a dos decimales.
7. **Exportación de relaciones**:
   - Se recorren todas las parejas de piezas para generar un CSV con columnas: `PARTE1`, `PARTE2`, `RELACION` (0.00–1.00) e `INTERPRETACION`:
     - **Fuerte** (≥ 0.7)
     - **Moderada** (0.5 ≤ x < 0.7)
     - **Débil** (< 0.5)

---

## 📈 Ejecución
```bash
python analysis.py
```
Al terminar, verás en consola las rutas a `heatmap.png` y `relations.csv` generados.

---

## 💡 Consideraciones Técnicas
- **Muestreo de datos**: Procesar solo el 50 % de las filas acelera el desarrollo y permite iterar rápidamente con datasets grandes sin comprometer mucho la representatividad.
- **Matrices dispersas**: Dado que la mayoría de pares de piezas no aparecen juntos, una matriz `lil_matrix` de SciPy reduce drásticamente el uso de RAM en comparación con una matriz densa.
- **Similitud de coseno**: Ideal para vectores de conteo, capta la frecuencia relativa de co-ocurrencias independientemente de la magnitud absoluta.
- **Escalabilidad**: Ajusta `sample_frac` y `min_transactions` según el volumen de datos y la memoria disponible.

---

## 🤝 Contribuciones
1. Haz fork de este repositorio.
2. Crea una rama con tu feature: `git checkout -b mi-nueva-funcionalidad`.
3. Realiza tus cambios y haz commit.
4. Envía un pull request describiendo tus mejoras.

---

## 📜 Licencia
Este proyecto está bajo la licencia MIT. Consulta [LICENSE](LICENSE) para más información.


<div align="center">

<h1> 🏋️ Seguimiento de peso y medidas corporales </h1>

*Visualiza en un gráfico la evolución de tu peso y medidas corporales a partir de un Excel.*

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/ruizRojasFel/seguimiento_peso_medidas_corporales/tree/main?tab=MIT-1-ov-file)

</div>

<br>

## Descripción

Script en Python que lee un Excel con tus registros de fecha, peso, torso, cintura y cadera, y genera un gráfico con su evolución en el tiempo.
Muestra el peso (kg) y las medidas (cm) en paneles separados, con el valor inicial y final de cada serie y el cambio total en la leyenda.
El gráfico se puede ver en pantalla o guardar como imagen con la opción `--guardar`.

## Formato del Excel

El repositorio no incluye un Excel de datos: debes crear el tuyo con las siguientes características.

- **Nombre y ubicación por defecto:** `Seguimiento_Peso_Medidas_Corporales.xlsx`, en la misma carpeta que el script. También puedes usar otro nombre o ubicación indicando la ruta al ejecutar el script.
- **Hoja:** los datos se leen de la primera hoja del libro.
- **Encabezados:** en la primera fila, con estas cinco columnas:

  | Columna   | Contenido                  | Ejemplo      |
  |-----------|----------------------------|--------------|
  | `Fecha`   | Fecha de la medición       | `31/08/2026` |
  | `Peso`    | Peso en kilogramos         | `78,5`       |
  | `Torso`   | Contorno de torso en cm    | `106`        |
  | `Cintura` | Contorno de cintura en cm  | `104`        |
  | `Cadera`  | Contorno de cadera en cm   | `100`        |

Consideraciones:

- No importan las mayúsculas, las tildes ni los espacios en los encabezados (`Cintura`, `cintura` y ` CINTURA ` son equivalentes).
- El orden de las columnas es libre y las columnas adicionales se ignoran.
- Las fechas pueden ser celdas de tipo fecha o texto con el formato día/mes/año.
- Los decimales se aceptan con coma o con punto (`78,5` o `78.5`).
- Una celda vacía se omite en esa serie sin cortar la línea del gráfico.
- Las filas con fecha pero sin ninguna medición se ignoran, por lo que puedes dejar fechas futuras planificadas.

Ejemplo:

| Fecha      | Peso  | Torso | Cintura | Cadera |
|------------|-------|-------|---------|--------|
| 31/08/2026 | 78,5  | 106   | 104     | 100    |
| 07/09/2026 | 78,35 | 106   | 104     | 100    |
| 14/09/2026 | 78,15 | 105   | 102     | 100    |
| 21/09/2026 |       |       |         |        |

## Uso

1. Instala las dependencias (idealmente dentro de un entorno virtual):

   ```bash
   pip install -r requirements.txt
   ```

2. Crea tu Excel siguiendo el [formato descrito arriba](#formato-del-excel) y registra tus mediciones.

3. Ejecuta el script:

   ```bash
   # Muestra el gráfico en pantalla
   python seguimiento_peso_medidas_corporales.py

   # Usa otro Excel
   python seguimiento_peso_medidas_corporales.py otro_archivo.xlsx

   # Guarda el gráfico como imagen en vez de mostrarlo
   python seguimiento_peso_medidas_corporales.py --guardar grafico.png
   ```

<br>

---

<div align="center">

<h2> Developer </h2>

<h3> Felipe Andrés Ruiz Rojas </h3>

[![LinkedIn](https://img.shields.io/badge/LinkedIn-linkedin.com%2Fin%2Fruizrojasfel-blue)](https://www.linkedin.com/in/ruizrojasfel) [![Website](https://img.shields.io/badge/Website-felruiz--dev.netlify.app-lightblue)](https://felruiz-dev.netlify.app/)

Copyright © 2026 Fel Ruiz
</div>

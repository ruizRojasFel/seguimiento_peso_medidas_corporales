"""
Grafica la evolución del peso y de las medidas corporales (torso, cintura, cadera)
a partir de un Excel con las columnas: Fecha, Peso, Torso, Cintura, Cadera.

Uso:
    python seguimiento_peso_medidas_corporales.py [ruta_excel] [--guardar grafico.png]
"""
import argparse
import sys
import unicodedata
from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.axes import Axes
from matplotlib.figure import Figure

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------
# Junto al script, para que funcione sin importar desde qué carpeta se ejecute
ARCHIVO_POR_DEFECTO = Path(__file__).resolve().parent / "Seguimiento_Peso_Medidas_Corporales.xlsx"
HOJA_EXCEL = 0  # índice o nombre de la hoja

COLUMNA_FECHA = "fecha"
COLUMNA_PESO = "peso"
COLORES_MEDIDAS = {  # columna -> color de la línea
    "torso": "#1f77b4",
    "cintura": "#d62728",
    "cadera": "#2ca02c",
}
COLOR_PESO = "#6a3d9a"
COLUMNAS_NUMERICAS = [COLUMNA_PESO, *COLORES_MEDIDAS]

FORMATO_FECHA = "%d/%m/%Y"
MAX_FECHAS_EN_EJE = 15  # con más mediciones, matplotlib elige las marcas del eje X


class ErrorDeDatos(Exception):
    """El archivo de entrada no se puede leer o no tiene el formato esperado."""


# ---------------------------------------------------------------------------
# Lectura y limpieza de datos
# ---------------------------------------------------------------------------
def normalizar(texto: str) -> str:
    """Pasa a minúsculas y quita tildes y espacios: ' Cintura ' -> 'cintura'."""
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto.strip().lower()


def leer_excel(ruta: Path) -> pd.DataFrame:
    """Lee la hoja configurada del Excel y normaliza los nombres de columna."""
    if not ruta.exists():
        raise ErrorDeDatos(f"No se encontró el archivo: {ruta}")

    try:
        df = pd.read_excel(ruta, sheet_name=HOJA_EXCEL)
    except ImportError:
        raise ErrorDeDatos("Falta la librería para leer Excel. Instálala con: pip install openpyxl")
    except PermissionError:
        raise ErrorDeDatos(f"No se pudo abrir {ruta.name}. ¿Está abierto en Excel? Ciérralo e intenta de nuevo.")
    except ValueError as error:  # formato no reconocido u hoja inexistente
        raise ErrorDeDatos(f"No se pudo leer {ruta.name} como Excel: {error}")

    df.columns = [normalizar(c) for c in df.columns]
    return df


def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """Valida las columnas, convierte tipos y deja solo las filas con mediciones."""
    requeridas = [COLUMNA_FECHA, *COLUMNAS_NUMERICAS]
    faltantes = [c for c in requeridas if c not in df.columns]
    if faltantes:
        raise ErrorDeDatos(
            f"Faltan columnas en el Excel: {', '.join(faltantes)}\n"
            f"Columnas encontradas: {', '.join(df.columns)}"
        )

    df = df[requeridas].copy()
    df[COLUMNA_FECHA] = pd.to_datetime(df[COLUMNA_FECHA], dayfirst=True, errors="coerce")
    for columna in COLUMNAS_NUMERICAS:
        # Admite decimales con coma (ej. "82,5")
        texto = df[columna].astype(str).str.replace(",", ".", regex=False)
        df[columna] = pd.to_numeric(texto, errors="coerce")

    # Descarta filas sin fecha y fechas planificadas que aún no tienen mediciones
    df = df.dropna(subset=[COLUMNA_FECHA])
    df = df.dropna(subset=COLUMNAS_NUMERICAS, how="all")
    if df.empty:
        raise ErrorDeDatos("El Excel no tiene filas con fecha y mediciones válidas.")

    return df.sort_values(COLUMNA_FECHA).reset_index(drop=True)


def cargar_datos(ruta: Path) -> pd.DataFrame:
    """Lee el Excel y devuelve las mediciones listas para graficar."""
    return limpiar_datos(leer_excel(ruta))


# ---------------------------------------------------------------------------
# Gráfico
# ---------------------------------------------------------------------------
def dibujar_serie(ax: Axes, fechas: pd.Series, valores: pd.Series,
                  nombre: str, unidad: str, color: str) -> None:
    """Dibuja una serie con su cambio total en la leyenda y el valor del primer y último punto."""
    # Se omiten los valores vacíos para que la línea no se corte
    con_dato = valores.notna()
    fechas, valores = fechas[con_dato], valores[con_dato]
    if valores.empty:
        return

    etiqueta = nombre
    if len(valores) > 1:
        cambio = valores.iloc[-1] - valores.iloc[0]
        etiqueta += f" ({cambio:+.1f} {unidad})"

    ax.plot(fechas, valores, marker="o", color=color, linewidth=2, label=etiqueta)

    for i in (0, -1):
        ax.annotate(
            f"{valores.iloc[i]:.1f}",
            xy=(fechas.iloc[i], valores.iloc[i]),
            xytext=(0, 8),
            textcoords="offset points",
            ha="center",
            fontsize=8,
            color=color,
        )


def crear_grafico(df: pd.DataFrame) -> Figure:
    """Crea la figura con el peso (arriba) y las medidas en cm (abajo)."""
    fechas = df[COLUMNA_FECHA]

    fig, (ax_peso, ax_medidas) = plt.subplots(
        2, 1, figsize=(11, 8), sharex=True, gridspec_kw={"height_ratios": [1, 1.4]}
    )
    fig.suptitle("Evolución de peso y medidas", fontsize=15, fontweight="bold")

    dibujar_serie(ax_peso, fechas, df[COLUMNA_PESO], "Peso", "kg", COLOR_PESO)
    for columna, color in COLORES_MEDIDAS.items():
        dibujar_serie(ax_medidas, fechas, df[columna], columna.capitalize(), "cm", color)

    ax_peso.set_ylabel("Peso (kg)")
    ax_medidas.set_ylabel("Medida (cm)")
    ax_medidas.set_xlabel("Fecha")
    for ax in (ax_peso, ax_medidas):
        ax.grid(alpha=0.3)
        ax.margins(y=0.15)  # espacio para las etiquetas de valor
        ax.legend(loc="best")

    # Marca cada medición en el eje X mientras no sean demasiadas
    if len(fechas) <= MAX_FECHAS_EN_EJE:
        ax_medidas.set_xticks(fechas)
    ax_medidas.xaxis.set_major_formatter(mdates.DateFormatter(FORMATO_FECHA))
    fig.autofmt_xdate()
    fig.tight_layout()

    return fig


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------
def parsear_argumentos() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Grafica la evolución de peso y medidas corporales.")
    parser.add_argument(
        "excel", nargs="?", type=Path, default=ARCHIVO_POR_DEFECTO,
        help=f"ruta del Excel (por defecto: {ARCHIVO_POR_DEFECTO.name})",
    )
    parser.add_argument(
        "--guardar", metavar="IMAGEN", type=Path,
        help="guarda el gráfico en un archivo (ej. grafico.png) en vez de mostrarlo",
    )
    return parser.parse_args()


def main() -> int:
    args = parsear_argumentos()

    try:
        df = cargar_datos(args.excel)
    except ErrorDeDatos as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    inicio, fin = df[COLUMNA_FECHA].iloc[0], df[COLUMNA_FECHA].iloc[-1]
    print(f"Se cargaron {len(df)} mediciones ({inicio:{FORMATO_FECHA}} – {fin:{FORMATO_FECHA}}).")

    fig = crear_grafico(df)
    if args.guardar:
        try:
            fig.savefig(args.guardar, dpi=150, bbox_inches="tight")
        except (OSError, ValueError) as error:  # carpeta inexistente o extensión no soportada
            print(f"Error: no se pudo guardar el gráfico: {error}", file=sys.stderr)
            return 1
        print(f"Gráfico guardado en: {args.guardar}")
    else:
        plt.show()

    return 0


if __name__ == "__main__":
    sys.exit(main())

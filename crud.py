import pandas as pd
import pathlib

DATA_DIR = pathlib.Path("data")
ANIME_PATH = DATA_DIR / "anime_dataset.csv"
MANGA_PATH = DATA_DIR / "manga_dataset.csv"

def cargar_datos(ruta):
    if pathlib.Path(ruta).exists():
        return pd.read_csv(ruta)
    return pd.DataFrame()

def guardar_datos(df, ruta):
    df.to_csv(ruta, index=False)
    print(f"Datos guardados en {ruta}")

def agregar_fila(ruta, datos_nuevos):
    df = cargar_datos(ruta)
    nueva_fila = pd.DataFrame([datos_nuevos])
    df = pd.concat([df, nueva_fila], ignore_index=True)
    guardar_datos(df, ruta)
    print(f"Fila agregada")
    return df

def eliminar_fila(ruta, indice):
    df = cargar_datos(ruta)
    df = df.drop(indice).reset_index(drop=True)
    guardar_datos(df, ruta)
    print(f"Fila {indice} eliminada")
    return df

def modificar_fila(ruta, indice, datos_actualizados):
    df = cargar_datos(ruta)
    for columna, valor in datos_actualizados.items():
        if columna in df.columns:
            df.loc[indice, columna] = valor
    guardar_datos(df, ruta)
    print(f"Fila {indice} modificada")
    return df

def ver_datos(ruta):
    df = cargar_datos(ruta)
    print(f"\n{'='*50}")
    print(df)
    print(f"{'='*50}\n")
    return df

if __name__ == "__main__":
    print("CRUD BASICO - Anime Dataset\n")
    print("1. VIENDO DATOS:")
    df = ver_datos(ANIME_PATH)
    print("2. AGREGANDO FILA:")
    nueva_fila = {"name": "Mi Anime", "type": "TV", "episodes": 12, "score": 8.0}
    agregar_fila(ANIME_PATH, nueva_fila)
    df = ver_datos(ANIME_PATH)
    print("3. MODIFICANDO ULTIMA FILA:")
    indice_ultimo = len(df) - 1
    modificar_fila(ANIME_PATH, indice_ultimo, {"score": 9.5})
    df = ver_datos(ANIME_PATH)
    print("4. ELIMINANDO ULTIMA FILA:")
    eliminar_fila(ANIME_PATH, indice_ultimo)
    ver_datos(ANIME_PATH)

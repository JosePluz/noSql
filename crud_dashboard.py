import streamlit as st
import pandas as pd
import pathlib

st.set_page_config(page_title="CRUD Anime & Manga", layout="wide")

DATA_DIR = pathlib.Path("data")
ANIME_PATH = DATA_DIR / "anime_dataset.csv"
MANGA_PATH = DATA_DIR / "manga_dataset.csv"

def cargar_csv(ruta):
    if pathlib.Path(ruta).exists():
        return pd.read_csv(ruta)
    return pd.DataFrame()

def guardar_csv(df, ruta):
    df.to_csv(ruta, index=False)

if "dataset_actual" not in st.session_state:
    st.session_state.dataset_actual = "Anime"

if "modo" not in st.session_state:
    st.session_state.modo = "ver"

with st.sidebar:
    st.title("CRUD Manager")
    
    st.session_state.dataset_actual = st.radio("Dataset:", ["Anime", "Manga"], key="dataset_radio")
    ruta = ANIME_PATH if st.session_state.dataset_actual == "Anime" else MANGA_PATH
    
    st.divider()
    
    if st.button("Agregar", use_container_width=True, key="btn_agregar"):
        st.session_state.modo = "agregar"
        st.rerun()
    
    if st.button("Eliminar", use_container_width=True, key="btn_eliminar"):
        st.session_state.modo = "eliminar"
        st.rerun()
    
    if st.button("Ver datos", use_container_width=True, key="btn_ver"):
        st.session_state.modo = "ver"
        st.rerun()
    
    st.divider()
    
    df = cargar_csv(ruta)
    st.info(f"Total: **{len(df)}** filas")

ruta = ANIME_PATH if st.session_state.dataset_actual == "Anime" else MANGA_PATH
df = cargar_csv(ruta)

st.title(f"{st.session_state.dataset_actual}")

if st.session_state.modo == "ver":
    if not df.empty:
        cols_mostrar = []
        
        if "name" in df.columns:
            cols_mostrar.append("name")
        if "title" in df.columns and "name" not in df.columns:
            cols_mostrar.append("title")
        
        if "type" in df.columns:
            cols_mostrar.append("type")
        
        if "genres" in df.columns:
            cols_mostrar.append("genres")
        if "genre" in df.columns and "genres" not in df.columns:
            cols_mostrar.append("genre")
        
        if "score" in df.columns:
            cols_mostrar.append("score")
        
        if "synopsis" in df.columns:
            cols_mostrar.append("synopsis")
        if "description" in df.columns and "synopsis" not in df.columns:
            cols_mostrar.append("description")
        
        if not cols_mostrar:
            cols_mostrar = df.columns.tolist()
        
        df_mostrar = df[cols_mostrar]
        
        st.subheader("Tabla de datos")
        st.dataframe(df_mostrar, use_container_width=True, height=500)
    else:
        st.warning("No hay datos disponibles")

elif st.session_state.modo == "agregar":
    st.subheader("Agregar nuevo registro")
    
    if df.empty:
        st.warning("Base de datos vacia - No se pueden determinar las columnas")
    else:
        with st.form("form_agregar"):
            col1, col2 = st.columns(2)
            inputs = {}
            
            for i, col in enumerate(df.columns[:8]):
                with col1 if i % 2 == 0 else col2:
                    inputs[col] = st.text_input(f"{col}:")
            
            if st.form_submit_button("Guardar registro", use_container_width=True):
                nueva_fila = pd.DataFrame([inputs])
                df = pd.concat([df, nueva_fila], ignore_index=True)
                guardar_csv(df, ruta)
                st.success("Registro agregado correctamente")
                st.session_state.modo = "ver"
                st.rerun()

elif st.session_state.modo == "eliminar":
    st.subheader("Eliminar registro")
    
    if not df.empty:
        indice = st.number_input("Seleccionar fila a eliminar:", 0, len(df)-1, key="input_eliminar")
        
        st.write("Registro seleccionado:")
        col1, col2 = st.columns(2)
        with col1:
            st.json(df.iloc[indice].to_dict())
        
        with col2:
            if st.button("Confirmar eliminacion", use_container_width=True, key="btn_confirmar_eliminar"):
                df = df.drop(indice).reset_index(drop=True)
                guardar_csv(df, ruta)
                st.success("Registro eliminado correctamente")
                st.session_state.modo = "ver"
                st.rerun()
    else:
        st.warning("No hay registros para eliminar")


#importaciones necesarias para el dashboard
import pathlib
import pandas as pd
import plotly.express as px
import streamlit as st
#Rutas a los datasets
DATA_DIR = pathlib.Path("data")
ANIME_PATH = DATA_DIR / "anime_dataset.csv"
MANGA_PATH = DATA_DIR / "manga_dataset.csv"
#Configuración de la página y estilos personalizados
st.set_page_config(page_title="Anime Dashboard", layout="wide")
#Estilos personalizados para la apariencia del dashboard
st.markdown(
    """
    <style>
    .main {background: linear-gradient(180deg, #071016 0%, #12233b 60%); color: red;}
    .stApp {background: linear-gradient(180deg, #071016 0%, #12233b 60%);color: red;}
    .block-container {padding: 1.2rem 1.5rem 1.5rem;}
    .stButton>button {background-color: #4f8df7; color: red;}
    .stButton>button:hover {background-color: #3b75d1; color: red;}
    .metric-card {background: rgba(255,255,255,0.08); border-radius: 12px; padding: 18px;}
    </style>
    """,
    unsafe_allow_html=True,
)
#Título del dashboard
import pathlib
import pandas as pd
import plotly.express as px
import streamlit as st
#Rutas a los datasets
DATA_DIR = pathlib.Path("data")
ANIME_PATH = DATA_DIR / "anime_dataset.csv"
MANGA_PATH = DATA_DIR / "manga_dataset.csv"
#Configuración de la página y estilos personalizados
st.set_page_config(page_title="Anime Dashboard", layout="wide")
#Estilos personalizados para mejorar la apariencia del dashboard
st.markdown(
    """
    <style>
    .main {background: linear-gradient(180deg, #071016 0%, #12233b 60%); color: red;}
    .stApp {background: linear-gradient(180deg, #071016 0%, #12233b 60%); color: red;}
    .block-container {padding: 1.2rem 1.5rem 1.5rem;}
    .stButton>button {background-color: #4f8df7; color: red;}
    .stButton>button:hover {background-color: #3b75d1; color: red;}
    .metric-card {background: rgba(255,255,255,0.08); border-radius: 12px; padding: 18px;}
    </style>
    """,
    unsafe_allow_html=True,
)
#Título del dashboard
st.title("DATOS NO ESTRUCTURADOS")
#Funciones para cargar y procesar los datos de anime y manga
def load_csv(path: pathlib.Path):
    if not path.exists():
        return None
    df = pd.read_csv(path, low_memory=False)
    df.columns = [str(c).strip() for c in df.columns]
    df = df.fillna("")
    text_columns = [c for c in df.columns if df[c].dtype == object]
    if text_columns:
        df["full_text"] = df[text_columns].astype(str).agg(" ".join, axis=1).str.lower()
    else:
        df["full_text"] = ""
    if "year" in df.columns:
        df["year"] = df["year"].astype(str)
    else:
        df["year"] = ""
    return df
#Función para cargar los datos con caché para mejorar el rendimiento
@st.cache_data
def load_data():
    anime = load_csv(ANIME_PATH)
    manga = load_csv(MANGA_PATH)
    return anime, manga
#Funciones para aplicar filtros personalizados, ordenar por campos numéricos, filtrar por género y año, y obtener consultas predefinidas
def apply_custom_filters(df: pd.DataFrame, search: str, custom_type: str, genre: str, min_score: float):
    if search:
        df = df[df["full_text"].str.contains(search.lower(), na=False)]
    if custom_type and custom_type != "Todos":
        df = df[df["type"].astype(str).str.lower().str.contains(custom_type.lower(), na=False)]
    if genre:
        genre_cols = [c for c in df.columns if c.lower() in {"genres", "genre"}]
        if genre_cols:
            df = df[df[genre_cols[0]].astype(str).str.lower().str.contains(genre.lower(), na=False)]
    if "score" in df.columns and min_score > 0:
        df = df[pd.to_numeric(df["score"], errors="coerce").fillna(0) >= min_score]
    return df
#Funciones para ordenar por campos numéricos, filtrar por género y año, y obtener consultas predefinidas
def numeric_sort(df: pd.DataFrame, field: str, limit: int = 10):
    if field not in df.columns:
        return df.head(0)
    values = pd.to_numeric(df[field], errors="coerce").fillna(0)
    return df.assign(_sort=values).sort_values("_sort", ascending=False).drop(columns=["_sort"]).head(limit)
#Funciones para filtrar por género y año, y obtener consultas predefinidas
def filter_by_genre(df: pd.DataFrame, genre: str):
    if not genre:
        return df
    genre_cols = [c for c in df.columns if c.lower() in {"genres", "genre"}]
    if not genre_cols:
        return df
    return df[df[genre_cols[0]].astype(str).str.lower().str.contains(genre.lower(), na=False)]
#Funciones para filtrar por año y obtener consultas predefinidas
def filter_by_year(df: pd.DataFrame, year: str):
    if not year or "year" not in df.columns:
        return df
    return df[df["year"].astype(str).str.contains(str(year), na=False)]
#Funciones para obtener consultas predefinidas
def get_predefined_query(df: pd.DataFrame, query_name: str, limit: int = 10, genre: str = "", year: str = ""):
    if query_name == "Top 10 más vistos":
        return numeric_sort(df, "members", limit)
    if query_name == "Top 10 mejor puntuados":
        filtered_df = df.copy()
        if "scored_by" in filtered_df.columns:
            filtered_df = filtered_df[pd.to_numeric(filtered_df["scored_by"], errors="coerce").fillna(0) >= 1000]
        return numeric_sort(filtered_df, "score", limit)
    if query_name == "Top 10 con más favoritos":
        return numeric_sort(df, "favorites", limit)
    if query_name == "Top 10 por género":
        genre_df = filter_by_genre(df, genre)
        return numeric_sort(genre_df, "score", limit)
    if query_name == "Top 10 por año":
        year_df = filter_by_year(df, year)
        return numeric_sort(year_df, "score", limit)
    return df.head(0)
#Función para preparar el DataFrame para su visualización en Streamlit, reemplazando cadenas vacías

def sanitize_display_df(df: pd.DataFrame):
    """Prepare DataFrame for Streamlit display: replace empty strings and coerce numeric columns."""
    if df is None or df.empty:
        return df
    df2 = df.copy()
    df2 = df2.replace("", pd.NA)
    for col in df2.columns:
        # try to coerce to numeric when possible
        try:
            coerced = pd.to_numeric(df2[col], errors="coerce")
            if coerced.notna().sum() > 0:
                df2[col] = coerced
        except Exception:
            continue
    return df2
#Carga los datos de anime y manga, mostrando mensajes de error si no se encuentran los archivos Csv
anime, manga = load_data()
if anime is None:
    st.error(f"No se encontró el CSV de anime en: {ANIME_PATH}")
    st.stop()
#El dataset de manga es opcional, se muestra una advertencia si no está disponible pero el dashboard sigue funcionando con el dataset de anime
if manga is None:
    st.warning(f"El dataset de manga no está disponible en: {MANGA_PATH}")
#Controles en la barra lateral para seleccionar el dataset, consultas rápidas y filtros personalizados
with st.sidebar:
    st.header("Controles")
    media_source = st.selectbox("Dataset", ["anime", "manga"] if manga is not None else ["anime"])
    st.markdown("---")
    st.markdown("### Consultas rápidas")
    quick_query = st.selectbox(
        "Selecciona una consulta rápida",
        [
            "Ninguna",
            "Top 10 más vistos",
            "Top 10 mejor puntuados",
            "Top 10 con más favoritos",
            "Top 10 por género",
            "Top 10 por año",
        ],
    )
    quick_genre = ""
    quick_year = ""
    if quick_query == "Top 10 por género":
        quick_genre = st.text_input("Género para consulta rápida", value="Action")
    if quick_query == "Top 10 por año":
        quick_year = st.text_input("Año para consulta rápida", value="2020")
    run_quick = st.button("Ejecutar consulta rápida")
    st.markdown("---")
    st.markdown("### Consulta personalizada")
    custom_search = st.text_input("Buscar palabra o título", value="")
    custom_type = st.selectbox(
        "Filtrar por tipo",
        [
            "Todos",
            "TV",
            "Movie",
            "OVA",
            "Special",
            "ONA",
            "Music",
            "Manga",
            "Novel",
            "One-shot",
            "Manhwa",
            "Manhua",
        ],
    )
    custom_genre = st.text_input("Filtrar por género", value="")
    custom_min_score = st.slider("Mínimo puntuación", 0.0, 10.0, 0.0, 0.1)
    run_custom = st.button("Ejecutar consulta personalizada")
#Selecciona el DataFrame adecuado según la fuente de datos elegida y ejecuta la consulta personalizada o rápida según corresponda
selected_df = manga if media_source == "manga" and manga is not None else anime
custom_results = None
if run_custom:
    custom_results = apply_custom_filters(
        selected_df,
        custom_search,
        custom_type,
        custom_genre,
        custom_min_score,
    )
#Ejecuta la consulta rápida si se ha seleccionado una diferente a "Ninguna" y muestra los resultados de la consulta personalizada o rápida, o un mensaje informativo si no se han encontrado resultados o no se ha ejecutado ninguna consulta
quick_results = None
if run_quick:
    if quick_query == "Ninguna":
        st.info("Selecciona una consulta rápida diferente a 'Ninguna'.")
    else:
        quick_results = get_predefined_query(selected_df, quick_query, genre=quick_genre, year=quick_year)

#Mostrar resultados
st.markdown("## Resultados")
if custom_results is not None:
    if custom_results.empty:
        st.info("No se encontraron resultados para la consulta personalizada.")
    else:
        st.metric("Registros encontrados", len(custom_results))
        st.dataframe(sanitize_display_df(custom_results.reset_index(drop=True)), width='stretch')
elif quick_results is not None:
    if quick_results.empty:
        st.info("No se encontraron registros para la consulta rápida seleccionada.")
    else:
        st.metric("Registros encontrados", len(quick_results))
        st.dataframe(quick_results.reset_index(drop=True), use_container_width=True)
else:
    st.info("Elige una consulta rápida o ejecuta una consulta personalizada.")

st.markdown("---")
st.markdown("## MI CRUD PERSONALIZADO")

CUSTOM_PATH = DATA_DIR / "custom.csv"

def cargar_custom():
    if CUSTOM_PATH.exists():
        df = pd.read_csv(CUSTOM_PATH)
        return df
    return pd.DataFrame(columns=["titulo", "tipo", "genero", "descripcion", "puntuacion"])

def guardar_custom(df):
    df.to_csv(CUSTOM_PATH, index=False)

with st.expander("CRUD - Agregar, Buscar, Modificar, Eliminar", expanded=False):
    
    if "modo_crud" not in st.session_state:
        st.session_state.modo_crud = "ver"
    
    tab_ver, tab_agregar, tab_buscar, tab_modificar, tab_eliminar = st.tabs(
        ["Ver", "Agregar", "Buscar", "Modificar", "Eliminar"]
    )
    
    with tab_ver:
        df_custom = cargar_custom()
        if df_custom.empty:
            st.warning("No hay datos en la base de datos personalizada")
        else:
            st.subheader(f"Datos: {len(df_custom)} registros")
            st.dataframe(df_custom, use_container_width=True, height=400)
    
    with tab_agregar:
        st.subheader("Agregar nuevo registro")
        with st.form("form_agregar_custom"):
            col1, col2 = st.columns(2)
            with col1:
                titulo = st.text_input("Titulo:")
                tipo = st.selectbox("Tipo:", ["Anime", "Manga", "Pelicula", "Serie", "Otro"])
                genero = st.text_input("Genero:")
            with col2:
                puntuacion = st.slider("Puntuacion:", 0.0, 10.0, 5.0, 0.5)
                descripcion = st.text_area("Descripcion:", height=100)
            
            if st.form_submit_button("Guardar", use_container_width=True):
                df_custom = cargar_custom()
                nueva_fila = pd.DataFrame({
                    "titulo": [titulo],
                    "tipo": [tipo],
                    "genero": [genero],
                    "descripcion": [descripcion],
                    "puntuacion": [puntuacion]
                })
                df_custom = pd.concat([df_custom, nueva_fila], ignore_index=True)
                guardar_custom(df_custom)
                st.success(f"'{titulo}' agregado correctamente")
                st.rerun()
    
    with tab_buscar:
        st.subheader("Buscar registros")
        df_custom = cargar_custom()
        
        if df_custom.empty:
            st.warning("No hay datos para buscar")
        else:
            busqueda = st.text_input("Buscar por titulo, tipo o genero:")
            
            if busqueda:
                resultados = df_custom[
                    (df_custom["titulo"].str.contains(busqueda, case=False, na=False)) |
                    (df_custom["tipo"].str.contains(busqueda, case=False, na=False)) |
                    (df_custom["genero"].str.contains(busqueda, case=False, na=False))
                ]
                
                if resultados.empty:
                    st.info("No se encontraron resultados")
                else:
                    st.write(f"Se encontraron {len(resultados)} resultado(s):")
                    st.dataframe(resultados, use_container_width=True)
            else:
                st.info("Escribe algo para buscar")
    
    with tab_modificar:
        st.subheader("Modificar registro")
        df_custom = cargar_custom()
        
        if df_custom.empty:
            st.warning("No hay datos para modificar")
        else:
            indice = st.number_input("Seleccionar fila (0 a {})".format(len(df_custom)-1), 0, len(df_custom)-1)
            
            with st.form("form_modificar_custom"):
                col1, col2 = st.columns(2)
                with col1:
                    titulo_mod = st.text_input("Titulo:", value=df_custom.iloc[indice]["titulo"])
                    tipo_mod = st.selectbox("Tipo:", ["Anime", "Manga", "Pelicula", "Serie", "Otro"], 
                                           index=["Anime", "Manga", "Pelicula", "Serie", "Otro"].index(df_custom.iloc[indice]["tipo"]))
                    genero_mod = st.text_input("Genero:", value=df_custom.iloc[indice]["genero"])
                with col2:
                    puntuacion_mod = st.slider("Puntuacion:", 0.0, 10.0, float(df_custom.iloc[indice]["puntuacion"]), 0.5)
                    descripcion_mod = st.text_area("Descripcion:", value=df_custom.iloc[indice]["descripcion"], height=100)
                
                if st.form_submit_button("Guardar cambios", use_container_width=True):
                    df_custom.loc[indice, "titulo"] = titulo_mod
                    df_custom.loc[indice, "tipo"] = tipo_mod
                    df_custom.loc[indice, "genero"] = genero_mod
                    df_custom.loc[indice, "descripcion"] = descripcion_mod
                    df_custom.loc[indice, "puntuacion"] = puntuacion_mod
                    guardar_custom(df_custom)
                    st.success(f"'{titulo_mod}' modificado correctamente")
                    st.rerun()
    
    with tab_eliminar:
        st.subheader("Eliminar registro")
        df_custom = cargar_custom()
        
        if df_custom.empty:
            st.warning("No hay datos para eliminar")
        else:
            indice = st.number_input("Seleccionar fila para eliminar (0 a {})".format(len(df_custom)-1), 0, len(df_custom)-1, key="input_eliminar_custom")
            
            st.write("Registro a eliminar:")
            st.json(df_custom.iloc[indice].to_dict())
            
            if st.button("Confirmar eliminacion", use_container_width=True):
                df_custom = df_custom.drop(indice).reset_index(drop=True)
                guardar_custom(df_custom)
                st.success("Registro eliminado correctamente")
                st.rerun()


import streamlit as st
import pandas as pd
import os

# ==================================================
# 1. CONFIGURACIÓN GENERAL
# ==================================================

st.set_page_config(
    page_title="SAVE DROVE | Entrena. Mejora. Supérate.",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================================
# 2. INICIALIZACIÓN DE SESIÓN
# ==================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "users_db" not in st.session_state:
    st.session_state.users_db = {"admin": "1234"}


# ==================================================
# 3. ESTILOS VISUALES
# ==================================================

st.markdown("""
<style>
    .main {
        background-color: #11121A;
    }

    [data-testid="stSidebar"] {
        background-color: #191A25;
    }

    .main-title {
        font-size: 48px;
        font-weight: 800;
        color: #00E5CC;
    }

    .subtitle {
        color: #B8B8C8;
        font-size: 18px;
    }

    .hero {
        background: linear-gradient(135deg, #202333, #11121A);
        padding: 35px;
        border-radius: 18px;
        border: 1px solid #34364A;
        margin-bottom: 25px;
    }

    .hero h2 {
        color: white;
    }

    .hero h1 {
        color: #00E5CC;
        font-size: 35px;
    }

    .hero p {
        color: #D0D0D8;
        font-size: 17px;
    }

    h1, h2, h3 {
        color: white;
    }
</style>
""", unsafe_allow_html=True)


# ==================================================
# 4. BARRA LATERAL Y AUTENTICACIÓN
# ==================================================

st.sidebar.markdown("# ⚡ SAVE DROVE")
st.sidebar.markdown("*Entrena · Mejora · Supérate*")
st.sidebar.divider()

if not st.session_state.logged_in:

    st.sidebar.subheader("🔒 Acceso de Usuario")

    tab_login, tab_register = st.sidebar.tabs(
        ["Entrar", "Registro"]
    )

    # INICIO DE SESIÓN

    with tab_login:

        login_user = st.text_input(
            "Usuario",
            key="login_user"
        )

        login_pass = st.text_input(
            "Contraseña",
            type="password",
            key="login_pass"
        )

        if st.button(
            "Iniciar Sesión",
            use_container_width=True
        ):

            if (
                login_user in st.session_state.users_db
                and st.session_state.users_db[login_user] == login_pass
            ):

                st.session_state.logged_in = True
                st.session_state.username = login_user

                st.success("¡Bienvenido a SAVE DROVE!")
                st.rerun()

            else:

                st.error("Usuario o contraseña incorrectos.")

    # REGISTRO DE USUARIO

    with tab_register:

        reg_user = st.text_input(
            "Nuevo Usuario",
            key="reg_user"
        )

        reg_pass = st.text_input(
            "Nueva Contraseña",
            type="password",
            key="reg_pass"
        )

        if st.button(
            "Crear Cuenta Gratuita",
            use_container_width=True
        ):

            reg_user = reg_user.strip()

            if not reg_user:

                st.warning("Introduce un usuario válido.")

            elif reg_user in st.session_state.users_db:

                st.warning("Este usuario ya existe.")

            elif not reg_pass:

                st.warning("Introduce una contraseña.")

            else:

                st.session_state.users_db[reg_user] = reg_pass
                st.session_state.logged_in = True
                st.session_state.username = reg_user

                st.success("¡Cuenta creada exitosamente!")
                st.rerun()

else:

    st.sidebar.success(
        f"👤 Sesión: **{st.session_state.username}**"
    )

    st.sidebar.info("✨ Contenido 100% gratuito.")

    if st.sidebar.button(
        "Cerrar Sesión",
        use_container_width=True
    ):

        st.session_state.logged_in = False
        st.session_state.username = ""

        st.rerun()


# ==================================================
# 5. MENÚ PRINCIPAL
# ==================================================

st.sidebar.divider()
st.sidebar.subheader("📌 Menú Principal")

pagina = st.sidebar.radio(
    "Selecciona una sección:",
    [
        "Inicio",
        "Rutinas",
        "Deportes",
        "Planes",
        "Blog",
        "Nosotros"
    ]
)


# ==================================================
# 6. CONEXIÓN CON EXCEL
# ==================================================

EXCEL_PATH = "base de datos .xlsx"


@st.cache_data
def cargar_datos(path):

    if os.path.exists(path):

        try:

            df = pd.read_excel(
                path,
                sheet_name="Rutinas"
            )

            return df

        except Exception:
            return None

    return None


df_rutinas = cargar_datos(EXCEL_PATH)


# ==================================================
# 7. PÁGINA DE INICIO
# ==================================================

if pagina == "Inicio":

    st.markdown(
        '<p class="main-title">⚡ SAVE DROVE</p>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<p class="subtitle">ENTRENA · MEJORA · SUPÉRATE</p>',
        unsafe_allow_html=True
    )

    st.markdown("""
    <div class="hero">

        <h2>TU RENDIMIENTO, EN UN SOLO LUGAR</h2>

        <h1>
            Rutinas de alto rendimiento
            para todos los deportes
        </h1>

        <p>
            Entrena con planes diseñados para mejorar
            tu condición física, desarrollar tus habilidades,
            alcanzar tus metas y llevar tu rendimiento
            al siguiente nivel.
        </p>

    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Deportes",
            "8+",
            "Disciplinas"
        )

    with col2:
        st.metric(
            "Rutinas",
            "17+",
            "Opciones de entrenamiento"
        )

    with col3:
        st.metric(
            "Costo",
            "$0",
            "100% Gratuito"
        )

    st.divider()

    st.subheader("¿Qué puedes encontrar en SAVE DROVE?")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("### 🏋️ Rutinas")
        st.write(
            "Encuentra entrenamientos según "
            "tu deporte y objetivo."
        )

    with c2:
        st.markdown("### ⚽ Deportes")
        st.write(
            "Explora diferentes disciplinas "
            "y sus necesidades físicas."
        )

    with c3:
        st.markdown("### 📋 Planes")
        st.write(
            "Conoce planes de entrenamiento "
            "para diferentes niveles."
        )


# ==================================================
# 8. PÁGINA DE RUTINAS
# ==================================================

elif pagina == "Rutinas":

    st.title("🏋️ Explorador de Rutinas")

    st.write(
        "Encuentra rutinas de entrenamiento "
        "según tu disciplina y trabajo específico."
    )

    if not st.session_state.logged_in:

        st.warning(
            "🔒 Este contenido es exclusivo para usuarios registrados. "
            "Inicia sesión o crea una cuenta desde la barra lateral."
        )

        st.stop()

    if df_rutinas is None:

        st.error(
            f"No se pudo cargar el archivo '{EXCEL_PATH}'. "
            "Verifica que exista en la carpeta del proyecto "
            "y que tenga una hoja llamada 'Rutinas'."
        )

        st.stop()

    columnas = [
        "Deporte",
        "Trabajo Específico",
        "Rutina"
    ]

    if not all(col in df_rutinas.columns for col in columnas):

        st.error(
            "Faltan columnas en tu Excel. "
            "Necesitas: Deporte, Trabajo Específico y Rutina."
        )

        st.stop()

    # FILTRO DE DEPORTES

    st.sidebar.divider()
    st.sidebar.subheader("🔍 Filtros de Rutinas")

    deportes_disp = (
        ["Todos"]
        + sorted(
            df_rutinas["Deporte"].dropna().unique().tolist()
        )
    )

    dep_sel = st.sidebar.selectbox(
        "Selecciona un deporte:",
        deportes_disp
    )

    if dep_sel == "Todos":

        df_f = df_rutinas.copy()

    else:

        df_f = df_rutinas[
            df_rutinas["Deporte"] == dep_sel
        ]

    # FILTRO DE TRABAJO ESPECÍFICO

    trabajos_disp = (
        ["Todos"]
        + sorted(
            df_f["Trabajo Específico"].dropna().unique().tolist()
        )
    )

    trab_sel = st.sidebar.selectbox(
        "Trabajo específico:",
        trabajos_disp
    )

    if trab_sel != "Todos":

        df_f = df_f[
            df_f["Trabajo Específico"] == trab_sel
        ]

    st.divider()

    st.subheader(
        f"Mostrando {len(df_f)} rutinas disponibles"
    )

    # MOSTRAR RESULTADOS

    if df_f.empty:

        st.info("No se encontraron rutinas con esos filtros.")

    else:

        for idx, row in df_f.iterrows():

            with st.container(border=True):

                col1, col2 = st.columns([3, 1])

                with col1:

                    st.subheader(
                        f"📌 {row['Rutina']}"
                    )

                    st.caption(
                        f"Deporte: {row['Deporte']} "
                        f"| Trabajo: {row['Trabajo Específico']}"
                    )

                with col2:

                    if st.button(
                        "Iniciar",
                        key=f"rutina_{idx}",
                        use_container_width=True
                    ):

                        st.success(
                            f"¡Has seleccionado la rutina {row['Rutina']}!"
                        )


# ==================================================
# 9. PÁGINA DE DEPORTES
# ==================================================

elif pagina == "Deportes":

    st.title("⚽ Disciplinas Deportivas")

    st.write(
        "Conoce los deportes disponibles "
        "en nuestra plataforma."
    )

    deportes_info = {

        "Fútbol":
        "Potencia explosiva, resistencia aeróbica "
        "y prevención de lesiones.",

        "Baloncesto":
        "Salto vertical, agilidad, coordinación "
        "y potencia de piernas.",

        "Natación":
        "Potencia de brazada, coordinación "
        "y resistencia.",

        "Atletismo / Running":
        "Resistencia, velocidad "
        "y potencia de arranque.",

        "Ciclismo de Ruta":
        "Fuerza específica, resistencia "
        "y rendimiento en recorridos.",

        "CrossFit / Funcional":
        "Capacidad física general, coordinación "
        "y fuerza.",

        "Tenis":
        "Desplazamiento lateral, potencia "
        "y resistencia.",

        "Boxeo / MMA":
        "Acondicionamiento físico, coordinación "
        "y fuerza."
    }

    col1, col2 = st.columns(2)

    for i, (dep, desc) in enumerate(deportes_info.items()):

        with (col1 if i % 2 == 0 else col2):

            with st.container(border=True):

                st.subheader(dep)
                st.write(desc)


# ==================================================
# 10. PÁGINA DE PLANES
# ==================================================

elif pagina == "Planes":

    st.title("📋 Planes de Entrenamiento")

    st.write(
        "Planes estructurados para diferentes "
        "niveles y objetivos. 100% gratuitos."
    )

    if not st.session_state.logged_in:

        st.info(
            "💡 Inicia sesión para poder inscribirte "
            "en los planes."
        )

    planes = [

        {
            "titulo": "Plan Arranque Pro",
            "nivel": "Principiante / Intermedio",
            "desc": "Base de resistencia y fuerza general."
        },

        {
            "titulo": "Plan Explosividad Total",
            "nivel": "Avanzado",
            "desc": "Desarrollo de velocidad, coordinación y potencia."
        },

        {
            "titulo": "Plan Movilidad y Recuperación",
            "nivel": "Todos los niveles",
            "desc": "Mejora la movilidad y favorece la recuperación."
        }

    ]

    for plan in planes:

        with st.container(border=True):

            st.subheader(plan["titulo"])

            st.write(
                f"**Nivel:** {plan['nivel']}"
            )

            st.write(plan["desc"])

            if st.button(
                f"Inscribirse a {plan['titulo']}",
                key=f"plan_{plan['titulo']}"
            ):

                if st.session_state.logged_in:

                    st.success(
                        f"¡Te has inscrito en {plan['titulo']}!"
                    )

                else:

                    st.error(
                        "Debes iniciar sesión para inscribirte."
                    )


# ==================================================
# 11. PÁGINA DE BLOG
# ==================================================

elif pagina == "Blog":

    st.title("📰 Blog & Consejos")

    st.write(
        "Información y consejos para mejorar "
        "tu rendimiento deportivo."
    )

    with st.container(border=True):

        st.subheader(
            "1. La importancia del descanso en atletas"
        )

        st.write(
            "El descanso es fundamental para la recuperación "
            "física y mental. Mantener buenos hábitos de sueño "
            "ayuda a mejorar el rendimiento deportivo."
        )

    with st.container(border=True):

        st.subheader(
            "2. Nutrición previa al entrenamiento"
        )

        st.write(
            "Una alimentación equilibrada antes de entrenar "
            "puede ayudarte a mantener tu energía y concentración."
        )

    with st.container(border=True):

        st.subheader(
            "3. La importancia de la hidratación"
        )

        st.write(
            "Mantener una hidratación adecuada ayuda "
            "al funcionamiento del organismo durante "
            "la actividad física."
        )

    with st.container(border=True):

        st.subheader(
            "4. La constancia en el entrenamiento"
        )

        st.write(
            "La práctica constante y una buena planificación "
            "permiten desarrollar habilidades deportivas."
        )


# ==================================================
# 12. PÁGINA NOSOTROS
# ==================================================

elif pagina == "Nosotros":

    st.title("👥 Sobre SAVE DROVE")

    st.markdown(
        "### Entrena · Mejora · Supérate"
    )

    with st.container(border=True):

        st.subheader("Nuestra misión")

        st.write(
            "Nuestra misión es facilitar el acceso "
            "a información y herramientas de entrenamiento "
            "para deportistas de diferentes disciplinas."
        )

        st.divider()

        st.subheader("Nuestra visión")

        st.write(
            "Buscamos convertirnos en una plataforma "
            "que impulse el desarrollo deportivo "
            "mediante rutinas, planes y recursos."
        )

        st.divider()

        st.subheader("Nuestra filosofía")

        st.write(
            "Creemos que cada deportista tiene la oportunidad "
            "de aprender, mejorar y alcanzar sus objetivos "
            "mediante la constancia y la preparación."
        )

    st.divider()

    st.markdown(
        "### ⚡ SAVE DROVE"
    )

    st.caption(
        "Entrena · Mejora · Supérate | Plataforma gratuita."
    )
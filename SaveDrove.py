import streamlit as st
import pandas as pd
import os
# Configuración de la página
st.set_page_config(
   page_title="PERFORM | Entrena. Mejora. Supérate.",
   page_icon="⚡",
   layout="wide",
   initial_sidebar_state="expanded"
)
# --- INICIALIZACIÓN DE ESTADO ---
if "logged_in" not in st.session_state:
   st.session_state.logged_in = False
if "username" not in st.session_state:
   st.session_state.username = ""
if "users_db" not in st.session_state:
   st.session_state.users_db = {"admin": "1234"}
# --- BARRA LATERAL: NAVEGACIÓN Y AUTENTICACIÓN ---
st.sidebar.markdown("# ⚡ PERFORM")
st.sidebar.markdown("*Entrena · Mejora · Supérate*")
st.sidebar.divider()
# Sección de Autenticación
if not st.session_state.logged_in:
   st.sidebar.subheader("🔒 Acceso de Usuario")
   tab_login, tab_register = st.sidebar.tabs(["Entrar", "Registro"])
   with tab_login:
       login_user = st.text_input("Usuario", key="login_user")
       login_pass = st.text_input("Contraseña", type="password", key="login_pass")
       if st.button("Iniciar Sesión", use_container_width=True):
           if login_user in st.session_state.users_db and st.session_state.users_db[login_user] == login_pass:
               st.session_state.logged_in = True
               st.session_state.username = login_user
               st.success("¡Bienvenido!")
               st.rerun()
           else:
               st.error("Datos incorrectos.")
   with tab_register:
       reg_user = st.text_input("Nuevo Usuario", key="reg_user")
       reg_pass = st.text_input("Nueva Contraseña", type="password", key="reg_pass")
       if st.button("Crear Cuenta Gratuita", use_container_width=True):
           if reg_user in st.session_state.users_db:
               st.warning("El usuario ya existe.")
           elif not reg_user.strip():
               st.warning("Introduce un usuario válido.")
           else:
               st.session_state.users_db[reg_user] = reg_pass
               st.session_state.logged_in = True
               st.session_state.username = reg_user
               st.success("¡Cuenta creada!")
               st.rerun()
else:
   st.sidebar.success(f"👤 Sesión: **{st.session_state.username}**")
st.sidebar.info("✨ Contenido 100% gratuito.")
   if st.sidebar.button("Cerrar Sesión", use_container_width=True):
       st.session_state.logged_in = False
       st.session_state.username = ""
       st.rerun()
st.sidebar.divider()
st.sidebar.subheader("📌 Menú Principal")
pagina = st.sidebar.radio(
   "Selecciona una sección:",
   ["Inicio", "Rutinas", "Deportes", "Planes", "Blog", "Nosotros"]
)
# --- CARGA DE DATOS DESDE EXCEL ---
EXCEL_PATH = "base de datos .xlsx"
@st.cache_data
def cargar_datos(path):
   if os.path.exists(path):
       return pd.read_excel(path, sheet_name="Rutinas")
   return None
df_rutinas = cargar_datos(EXCEL_PATH)
# --- VISTAS DE LA APLICACIÓN ---
if pagina == "Inicio":
   st.title("⚡ PERFORM")
   st.markdown("### *ENTRENA · MEJORA · SUPÉRATE*")
   st.markdown("""
<div style="padding: 30px; border-radius: 10px; background-color: #1e1e1e; color: white; margin-bottom: 25px;">
<h2 style="color: #ffffff; margin-top: 0;">TU RENDIMIENTO, EN UN SOLO LUGAR</h2>
<h1 style="color: #00ffcc; font-size: 2.2rem;">Rutinas de alto rendimiento para todos los deportes</h1>
<p style="font-size: 1.1rem; color: #cccccc;">
           Entrena con planes diseñados por expertos, mejora tu condición física, alcanza tus metas y lleva tu rendimiento al siguiente nivel.
</p>
</div>
   """, unsafe_allow_html=True)
   col1, col2, col3 = st.columns(3)
   with col1:
       st.metric("Deportes", "7+", "Disciplinas")
   with col2:
       st.metric("Rutinas", "17+", "Niveles pro")
   with col3:
       st.metric("Costo", "0 $", "100% Gratuito")
elif pagina == "Rutinas":
   st.title("🏋️‍♂️ Explorador de Rutinas")
   st.markdown("Filtra las rutinas de alto rendimiento según tu disciplina y objetivo.")
   if not st.session_state.logged_in:
       st.warning("🔒 **Contenido exclusivo para usuarios registrados.** Inicia sesión o regístrate en la barra lateral para ver y realizar las rutinas.")
       st.stop()
   if df_rutinas is None:
       st.error(f"No se encontró el archivo '{EXCEL_PATH}' en la carpeta del proyecto.")
       st.stop()
   # Filtros interactivos en la barra lateral
   st.sidebar.divider()
   st.sidebar.subheader("🔍 Filtros de Rutinas")
   deportes_disp = ["Todos"] + list(df_rutinas["Deporte"].unique())
   dep_sel = st.sidebar.selectbox("Deporte", deportes_disp)
   df_f = df_rutinas if dep_sel == "Todos" else df_rutinas[df_rutinas["Deporte"] == dep_sel]
   trabajos_disp = ["Todos"] + list(df_f["Trabajo Específico"].unique())
   trab_sel = st.sidebar.selectbox("Trabajo Específico", trabajos_disp)
   if trab_sel != "Todos":
       df_f = df_f[df_f["Trabajo Específico"] == trab_sel]
   st.markdown(f"### Mostrando {len(df_f)} rutinas disponibles")
   for idx, row in df_f.iterrows():
       with st.container(border=True):
           c1, c2 = st.columns([3, 1])
           with c1:
               st.subheader(f"📌 {row['Rutina']}")
               st.caption(f"**Deporte:** {row['Deporte']} | **Enfoque:** {row['Trabajo Específico']}")
           with c2:
               if st.button("Iniciar", key=f"r_{idx}", use_container_width=True):
                   st.success(f"¡Rutina '{row['Rutina']}' iniciada con éxito!")
elif pagina == "Deportes":
   st.title("⚽ Disciplinas Deportivas")
   st.markdown("Conoce los deportes integrados en nuestra plataforma.")
   deportes_info = {
       "Fútbol": "Potencia explosiva, resistencia aeróbica y prevención de lesiones.",
       "Baloncesto": "Salto vertical, agilidad de transición rápida y potencia de piernas.",
       "Natación": "Potencia de brazada, core láctico y resistencia anaeróbica sprint.",
       "Atletismo / Running": "Desarrollo de VAM, umbral anaeróbico y potencia de arranque.",
       "Ciclismo de Ruta": "Fuerza específica en cuesta y mantenimiento de umbral FTP.",
       "CrossFit / Funcional": "Motor de alta capacidad y fuerza cíclica avanzada.",
       "Tenis": "Desplazamiento lateral, potencia unilateral y resistencia de core.",
       "Boxeo / MMA": "Acondicionamiento de combate, fuerza isométrica y agarre."
   }
   c1, c2 = st.columns(2)
   for i, (dep, desc) in enumerate(deportes_info.items()):
       with (c1 if i % 2 == 0 else c2):
           with st.container(border=True):
               st.subheader(dep)
               st.write(desc)
elif pagina == "Planes":
   st.title("📋 Planes de Entrenamiento")
   st.markdown("Planes estructurados diseñados por expertos. **100% Gratuitos.**")
   if not st.session_state.logged_in:
st.info("💡 Inicia sesión en la barra lateral para desbloquear y activar estos planes.")
   planes = [
       {"titulo": "Plan Arranque Pro", "nivel": "Principiante / Intermedio", "desc": "Base sólida de resistencia y fuerza general."},
       {"titulo": "Plan Explosividad Total", "nivel": "Avanzado", "desc": "Enfocado en deportes de alta intensidad."},
       {"titulo": "Plan Movilidad y Recuperación", "nivel": "Todos los niveles", "desc": "Evita lesiones y mejora la flexibilidad."}
   ]
   for plan in planes:
       with st.container(border=True):
           st.subheader(plan["titulo"])
           st.write(f"**Nivel:** {plan['nivel']} — {plan['desc']}")
           if st.button(f"Inscribirse a {plan['titulo']}", key=plan["titulo"]):
               if st.session_state.logged_in:
                   st.success(f"¡Inscrito en {plan['titulo']} exitosamente!")
               else:
                   st.error("Debes iniciar sesión para registrarte en el plan.")
elif pagina == "Blog":
   st.title("📰 Blog & Consejos")
   st.markdown("Artículos cortos para llevar tu rendimiento al siguiente nivel.")
   st.markdown("### 1. La importancia del descanso en atletas")
   st.write("El músculo crece durante el reposo. Optimiza tus horas de sueño.")
   st.divider()
   st.markdown("### 2. Nutrición previa al entrenamiento")
   st.write("Qué consumir para maximizar tu energía explosiva sin pesadez.")
elif pagina == "Nosotros":
   st.title("👥 Sobre PERFORM")
   st.markdown("Nuestra misión es democratizar el entrenamiento de alto rendimiento.")
   with st.container(border=True):
       st.write("Creemos que todo deportista merece acceso a rutinas profesionales basadas en ciencia y datos.")
       st.write("Plataforma **100% gratuita**. ¡Entrena. Mejora. Supérate!")
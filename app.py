import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

from config import settings

st.set_page_config(page_title="Ecosistema UDL - LAB (Diagnóstico)", layout="wide")
st.title("Ecosistema UDL - LAB — Diagnóstico Google Sheets")
st.caption("Solo lectura. Valida conexión, acceso y nombres de hojas.")

# ----------------------------
# Auth / Client
# ----------------------------
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]

def get_gspread_client():
    sa = st.secrets.get("gcp_service_account", None)
    if not sa:
        st.error("No encontré [gcp_service_account] en Secrets. Revisa Settings → Secrets.")
        st.stop()

    creds = Credentials.from_service_account_info(sa, scopes=SCOPES)
    return gspread.authorize(creds)

def list_tabs(sh):
    return [ws.title for ws in sh.worksheets()]

def ws_head(sh, tab_name, n=8):
    ws = sh.worksheet(tab_name)
    values = ws.get_all_values()
    if not values:
        return pd.DataFrame()
    df = pd.DataFrame(values[1:], columns=values[0])
    return df.head(n)

# ----------------------------
# UI
# ----------------------------
client = None
try:
    client = get_gspread_client()
    st.success("✅ Autenticación OK (service account leído desde Secrets).")
except Exception as e:
    st.error(f"❌ Falló autenticación: {e}")
    st.stop()

colA, colB = st.columns(2)

with colA:
    st.subheader("Sheet: Exámenes (LAB_RESPUESTAS_FORMS)")
    exam_id = settings.SHEETS["EXAMENES_SHEET_ID"]
    st.code(exam_id, language="text")

    try:
        sh_exam = client.open_by_key(exam_id)
        tabs = list_tabs(sh_exam)
        st.success(f"✅ Acceso OK. Tabs detectadas: {len(tabs)}")
        st.write(tabs)
    except Exception as e:
        st.error(f"❌ No pude abrir el Sheet de exámenes: {e}")
        st.stop()

with colB:
    st.subheader("Sheet: Accesos + Catálogo (LAB)")
    core_id = settings.SHEETS.get("ACCESOS_CATALOGO_SHEET_ID", "")
    st.code(core_id, language="text")

    if not core_id or "PEGA_AQUI" in core_id:
        st.warning("⚠️ Falta configurar ACCESOS_CATALOGO_SHEET_ID en config/settings.example.py")
    else:
        try:
            sh_core = client.open_by_key(core_id)
            tabs2 = list_tabs(sh_core)
            st.success(f"✅ Acceso OK. Tabs detectadas: {len(tabs2)}")
            st.write(tabs2)
        except Exception as e:
            st.error(f"❌ No pude abrir el Sheet de accesos/catálogo: {e}")

st.divider()
st.subheader("Lectura de prueba (heads)")

# Lectura de tabs del sheet de exámenes
for key, tab in settings.TABS_EXAMENES.items():
    with st.expander(f"Ver primeras filas: {tab}"):
        try:
            df = ws_head(sh_exam, tab, n=10)
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"No pude leer {tab}: {e}")

# Lectura de tabs del sheet core si está configurado
core_id = settings.SHEETS.get("ACCESOS_CATALOGO_SHEET_ID", "")
if core_id and "PEGA_AQUI" not in core_id:
    st.divider()
    st.subheader("Lectura de prueba (core)")

    for key, tab in settings.TABS_CORE.items():
        with st.expander(f"Ver primeras filas: {tab}"):
            try:
                df = ws_head(sh_core, tab, n=10)
                st.dataframe(df, use_container_width=True)
            except Exception as e:
                st.error(f"No pude leer {tab}: {e}")

st.info("Si todo sale en verde, ya podemos integrar el módulo Exámenes v2.")

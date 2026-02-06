import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Ecosistema UDL - LAB (Diagnóstico)", layout="wide")
st.title("Ecosistema UDL - LAB — Diagnóstico Google Sheets")
st.caption("Solo lectura. Valida conexión, acceso y nombres de hojas.")

# ======================================================
# Config LAB (hardcodeado para diagnóstico)
# ======================================================
EXAMENES_SHEET_ID = "1E8BKNLbBaFz0GkMuF-U6La0SAOa_A0BvsGZM0H-r-B4"
ACCESOS_CATALOGO_SHEET_ID = "1D2vmJvxx282BX2C2AcOcn1TL8e6KfdD893Bd4PEGduo"

TABS_EXAMENES = {
    "CAT_FORMULARIOS": "CAT_FORMULARIOS",
    "CATALOGO_EXAMENES": "CATALOGO_EXAMENES",
    "MAPEO_PREGUNTAS": "MAPEO_PREGUNTAS",
    "RESPUESTAS_LARGAS": "RESPUESTAS_LARGAS",
    "BASE_CONSOLIDADA": "BASE_CONSOLIDADA",
}

TABS_CORE = {
    "ACCESOS": "ACCESOS__LAB",
    "CATALOGO_MAESTRO": "CATALOGO_MAESTRO__LAB",
}

# ======================================================
# Auth / Client
# ======================================================
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets.readonly",
    "https://www.googleapis.com/auth/drive.readonly",
]

def _pick_service_account_from_secrets():
    """
    Acepta cualquiera de estas llaves en Secrets:
    - [gcp_service_account]
    - [gcp_service_account_json]
    """
    sa = st.secrets.get("gcp_service_account", None)
    if sa:
        return sa, "gcp_service_account"

    sa = st.secrets.get("gcp_service_account_json", None)
    if sa:
        return sa, "gcp_service_account_json"

    return None, None

def get_gspread_client():
    sa, key_name = _pick_service_account_from_secrets()
    if not sa:
        st.error("No encontré [gcp_service_account] ni [gcp_service_account_json] en Secrets. Revisa Settings → Secrets.")
        st.stop()

    # Validaciones mínimas para detectar secrets incompletos
    required = ["type", "project_id", "private_key", "client_email"]
    missing = [k for k in required if k not in sa or not str(sa.get(k, "")).strip()]
    if missing:
        st.error(f"El bloque [{key_name}] existe, pero le faltan campos: {missing}")
        st.stop()

    pk = str(sa.get("private_key", ""))
    if "BEGIN PRIVATE KEY" not in pk or "END PRIVATE KEY" not in pk:
        st.error("Tu private_key no parece completa (no contiene BEGIN/END). Pega la llave completa en Secrets.")
        st.stop()

    creds = Credentials.from_service_account_info(sa, scopes=SCOPES)
    return gspread.authorize(creds), key_name

def list_tabs(sh):
    return [ws.title for ws in sh.worksheets()]

def ws_head(sh, tab_name, n=8):
    ws = sh.worksheet(tab_name)
    values = ws.get_all_values()
    if not values:
        return pd.DataFrame()
    df = pd.DataFrame(values[1:], columns=values[0])
    return df.head(n)

# ======================================================
# Run
# ======================================================
try:
    client, used_key = get_gspread_client()
    st.success(f"✅ Autenticación OK (Secrets: [{used_key}]).")
except Exception as e:
    st.error(f"❌ Falló autenticación: {e}")
    st.stop()

colA, colB = st.columns(2)

with colA:
    st.subheader("Sheet: Exámenes (LAB_RESPUESTAS_FORMS)")
    st.code(EXAMENES_SHEET_ID, language="text")

    try:
        sh_exam = client.open_by_key(EXAMENES_SHEET_ID)
        tabs = list_tabs(sh_exam)
        st.success(f"✅ Acceso OK. Tabs detectadas: {len(tabs)}")
        st.write(tabs)
    except Exception as e:
        st.error(f"❌ No pude abrir el Sheet de exámenes: {e}")
        st.stop()

with colB:
    st.subheader("Sheet: Accesos + Catálogo (LAB)")
    st.code(ACCESOS_CATALOGO_SHEET_ID, language="text")

    try:
        sh_core = client.open_by_key(ACCESOS_CATALOGO_SHEET_ID)
        tabs2 = list_tabs(sh_core)
        st.success(f"✅ Acceso OK. Tabs detectadas: {len(tabs2)}")
        st.write(tabs2)
    except Exception as e:
        st.error(f"❌ No pude abrir el Sheet de accesos/catálogo: {e}")
        st.stop()

st.divider()
st.subheader("Lectura de prueba (heads)")

# Lectura de tabs del sheet de exámenes
for _, tab in TABS_EXAMENES.items():
    with st.expander(f"Ver primeras filas: {tab}", expanded=False):
        try:
            df = ws_head(sh_exam, tab, n=10)
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"No pude leer {tab}: {e}")

st.divider()
st.subheader("Lectura de prueba (core)")

# Lectura de tabs del sheet core
for _, tab in TABS_CORE.items():
    with st.expander(f"Ver primeras filas: {tab}", expanded=False):
        try:
            df = ws_head(sh_core, tab, n=10)
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"No pude leer {tab}: {e}")

st.info("Si todo sale en verde, ya podemos integrar el módulo Exámenes v2.")

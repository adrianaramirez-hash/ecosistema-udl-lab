# ======================================================
# Configuración general del entorno
# ======================================================
ENV = "LAB"

# ======================================================
# Google Sheets (IDs)
# ======================================================
SHEETS = {
    # Sheet de exámenes (ya confirmado)
    "EXAMENES_SHEET_ID": "1E8BKNLbBaFz0GkMuF-U6La0SAOa_A0BvsGZM0H-r-B4",

    # Sheet donde copiaste ACCESOS + CATALOGO MAESTRO
    # (lo completamos en el siguiente paso)
    "ACCESOS_CATALOGO_SHEET_ID": "PEGA_AQUI_EL_ID",
}

# ======================================================
# Hojas dentro del sheet LAB_RESPUESTAS_FORMS
# ======================================================
TABS_EXAMENES = {
    "CAT_FORMULARIOS": "CAT_FORMULARIOS",
    "CATALOGO_EXAMENES": "CATALOGO_EXAMENES",
    "MAPEO_PREGUNTAS": "MAPEO_PREGUNTAS",
    "RESPUESTAS_LARGAS": "RESPUESTAS_LARGAS",
    "BASE_CONSOLIDADA": "BASE_CONSOLIDADA",
}

# ======================================================
# Hojas dentro del sheet de Accesos / Catálogo (LAB)
# ======================================================
TABS_CORE = {
    "ACCESOS": "ACCESOS__LAB",
    "CATALOGO_MAESTRO": "CATALOGO_MAESTRO__LAB",
}

"""
Desha-Kala Clinical Navigator v2
Enhanced Ayurvedic clinical decision support for physicians.
New in v2:
  - Panchakarma Timing Advisor
  - District-specific Pathya-Apathya with food dataset
  - 7-Day Extended Weather Forecast
  - Ritusandhi Early Warning with scientific insights
  - Dual-District Patient Comparison tab
  - Samhita Reference Auto-Linker (Explainable AI)
"""
import datetime
from io import BytesIO

import plotly.graph_objects as go
import streamlit as st

from src.engine import (
    analyze_rutu_vyapad,
    fetch_weather_7day,
    map_date_to_rutu,
)
from src.utils import (
    load_ayurvedic_knowledge_base,
    load_samhita_reference_corpus,
    find_relevant_samhita_references,
    get_pathya_apathya_excel_path,
)
from src.panchakarma import (
    get_panchakarma_advice,
    calculate_ritusandhi_status,
    PANCHAKARMA_RUTU_MAP,
)
from src.pathya_apathya import get_combined_pathya_apathya
from src.samhita_ref import get_explainable_ai_panel

try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas as rl_canvas
    REPORTLAB_AVAILABLE = True
except Exception:
    REPORTLAB_AVAILABLE = False

# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Desha-Kala Clinical Navigator v2",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

RUTU_SEQUENCE = ["Shishira", "Vasanta", "Grishma", "Varsha", "Sharad", "Hemanta"]
RUTU_DOSHA_PHASES = {
    "Shishira": {"Sanchaya": "Kapha", "Prakopa": "-",     "Prashama": "Pitta"},
    "Vasanta":  {"Sanchaya": "-",     "Prakopa": "Kapha", "Prashama": "-"},
    "Grishma":  {"Sanchaya": "Vata",  "Prakopa": "-",     "Prashama": "Kapha"},
    "Varsha":   {"Sanchaya": "Pitta", "Prakopa": "Vata",  "Prashama": "-"},
    "Sharad":   {"Sanchaya": "-",     "Prakopa": "Pitta", "Prashama": "Vata"},
    "Hemanta":  {"Sanchaya": "Kapha", "Prakopa": "-",     "Prashama": "Pitta"},
}
CONDITION_PROFILES = {
    "Adhoga Amlapitta":   {"doshas": ["Pitta"], "worse_heat": True, "desha_sensitive": ["JANGALA","ANUPA"]},
    "Ajirna":             {"doshas": ["Kapha"], "worse_humidity": True, "worse_rain": True, "desha_sensitive": ["ANUPA"]},
    "Amlapitta":          {"doshas": ["Pitta"], "worse_heat": True, "worse_humidity": True, "desha_sensitive": ["ANUPA"]},
    "Amavata":            {"doshas": ["Vata","Kapha"], "worse_humidity": True, "worse_rain": True, "worse_cold_damp": True, "desha_sensitive": ["ANUPA"]},
    "Anidra":             {"doshas": ["Vata","Pitta"], "worse_heat": True, "worse_dryness": True},
    "Ardhavabhedaka":     {"doshas": ["Vata","Pitta"], "worse_heat": True},
    "Arsha":              {"doshas": ["Vata","Pitta"], "worse_heat": True, "worse_dryness": True, "desha_sensitive": ["JANGALA"]},
    "Atisara":            {"doshas": ["Vata","Pitta"], "worse_rain": True, "worse_humidity": True, "desha_sensitive": ["ANUPA"]},
    "Chittodvega":        {"doshas": ["Vata","Pitta"], "worse_heat": True},
    "Ekakushtha":         {"doshas": ["Vata","Kapha"], "worse_dryness": True, "worse_cold_damp": True, "desha_sensitive": ["JANGALA"]},
    "Grahani":            {"doshas": ["Vata","Pitta"], "worse_humidity": True, "worse_rain": True, "worse_heat": True, "desha_sensitive": ["ANUPA"]},
    "Gridhrasi":          {"doshas": ["Vata"], "worse_dryness": True, "worse_cold_damp": True, "desha_sensitive": ["JANGALA"]},
    "Hridroga":           {"doshas": ["Vata","Kapha"], "worse_cold_damp": True},
    "Kamala":             {"doshas": ["Pitta"], "worse_heat": True, "worse_humidity": True},
    "Karshya":            {"doshas": ["Vata"], "worse_dryness": True, "worse_heat": True, "desha_sensitive": ["JANGALA"]},
    "Kaphaja Kasa":       {"doshas": ["Kapha"], "worse_humidity": True, "worse_cold_damp": True, "desha_sensitive": ["ANUPA"]},
    "Kasa":               {"doshas": ["Vata","Kapha"], "worse_cold_damp": True, "worse_humidity": True, "desha_sensitive": ["ANUPA"]},
    "Katigraha":          {"doshas": ["Vata"], "worse_dryness": True, "worse_cold_damp": True, "desha_sensitive": ["JANGALA"]},
    "Kushtha":            {"doshas": ["Kapha","Pitta"], "worse_humidity": True, "worse_heat": True, "desha_sensitive": ["ANUPA"]},
    "Manyastambha":       {"doshas": ["Vata","Kapha"], "worse_cold_damp": True, "worse_humidity": True, "desha_sensitive": ["ANUPA"]},
    "Madhumeha":          {"doshas": ["Kapha","Vata"], "worse_humidity": True, "desha_sensitive": ["ANUPA"]},
    "Mukhadushika":       {"doshas": ["Kapha","Pitta"], "worse_heat": True, "worse_humidity": True},
    "Pandu":              {"doshas": ["Pitta","Vata"], "worse_heat": True},
    "Parinama Shula":     {"doshas": ["Vata","Pitta"], "worse_heat": True},
    "Pittaja Shirahshula":{"doshas": ["Pitta"], "worse_heat": True},
    "Pratishyaya":        {"doshas": ["Kapha","Vata"], "worse_cold_damp": True, "worse_humidity": True, "desha_sensitive": ["ANUPA"]},
    "Raktapitta":         {"doshas": ["Pitta"], "worse_heat": True},
    "Sandhivata":         {"doshas": ["Vata"], "worse_dryness": True, "worse_cold_damp": True, "desha_sensitive": ["JANGALA"]},
    "Shirahshula":        {"doshas": ["Vata","Pitta"], "worse_heat": True, "worse_dryness": True},
    "Shwasa":             {"doshas": ["Kapha","Vata"], "worse_humidity": True, "worse_rain": True, "desha_sensitive": ["ANUPA"]},
    "Sthaulya":           {"doshas": ["Kapha"], "worse_humidity": True, "desha_sensitive": ["ANUPA"]},
    "Tamaka Shwasa":      {"doshas": ["Kapha","Vata"], "worse_humidity": True, "worse_rain": True, "desha_sensitive": ["ANUPA"]},
    "Urdhwaga Amlapitta": {"doshas": ["Pitta"], "worse_heat": True, "worse_humidity": True, "desha_sensitive": ["ANUPA"]},
    "Vatavyadhi (General)":{"doshas": ["Vata"], "worse_dryness": True, "worse_cold_damp": True, "desha_sensitive": ["JANGALA"]},
    "Vicharchika":        {"doshas": ["Kapha","Pitta"], "worse_humidity": True, "worse_heat": True, "desha_sensitive": ["ANUPA"]},
}

# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def get_upcoming_rutu(current_rutu):
    try:
        idx = RUTU_SEQUENCE.index(current_rutu)
        return RUTU_SEQUENCE[(idx + 1) % len(RUTU_SEQUENCE)]
    except Exception:
        return current_rutu

def gv(d, k, fb="-"):
    v = d.get(k, fb)
    return fb if v is None else v

def get_desha_color(desha_value):
    d = str(desha_value).strip().lower()
    return {"anupa":"#2e7d32","jangala":"#c62828","sadharana":"#1565c0",
            "sadharana-anupa":"#43a047","sadharana-jangala":"#ef6c00"}.get(d,"#546e7a")

def build_dosha_progression_table(current_rutu, upcoming_rutu):
    rows = []
    for dosha in ["Vata","Pitta","Kapha"]:
        cur = RUTU_DOSHA_PHASES.get(current_rutu,{})
        nxt = RUTU_DOSHA_PHASES.get(upcoming_rutu,{})
        cs = "Yes" if cur.get("Sanchaya")==dosha else "-"
        cp = "Yes" if cur.get("Prakopa")==dosha else "-"
        cr = "Yes" if cur.get("Prashama")==dosha else "-"
        ns = "Yes" if nxt.get("Sanchaya")==dosha else "-"
        np_ = "Yes" if nxt.get("Prakopa")==dosha else "-"
        nr = "Yes" if nxt.get("Prashama")==dosha else "-"
        if cp=="Yes" or np_=="Yes":
            takeaway = "Higher flare risk — close symptom watch + diet discipline."
        elif cs=="Yes" or ns=="Yes":
            takeaway = "Accumulation phase — preventive correction early."
        elif cr=="Yes" or nr=="Yes":
            takeaway = "Natural calming window — maintain stabilising routine."
        else:
            takeaway = "Relatively neutral phase."
        rows.append({"Dosha":dosha,
            f"{current_rutu} Sanchaya":cs, f"{current_rutu} Prakopa":cp, f"{current_rutu} Prashama":cr,
            f"{upcoming_rutu} Sanchaya":ns, f"{upcoming_rutu} Prakopa":np_, f"{upcoming_rutu} Prashama":nr,
            "Clinical Takeaway":takeaway})
    return rows

def build_geo_climatic_evidence(district_data):
    return [
        {"Dataset Field":"Latitude / Longitude","District Value":f"{gv(district_data,'Latitude (°N)')} N, {gv(district_data,'Longitude (°E)')} E","Clinical Interpretation":"Defines geo-climatic context for weather alignment and Desha mapping."},
        {"Dataset Field":"Annual Rainfall (mm)","District Value":gv(district_data,"Annual Rainfall (mm)"),"Clinical Interpretation":"Higher values support Anupa tendencies; lower values favour Jangala traits."},
        {"Dataset Field":"Mean Relative Humidity (%)","District Value":gv(district_data,"Mean RH (%)"),"Clinical Interpretation":"Useful to anticipate snigdha/rooksha pressure on Agni and Kapha-Vata behaviour."},
        {"Dataset Field":"Soil Moisture (0-7cm)","District Value":gv(district_data,"Soil Moisture (0–7cm)"),"Clinical Interpretation":"Proxy for near-surface wetness influencing local dampness/dryness exposure."},
        {"Dataset Field":"Atmospheric Drying Potential (mm/yr)","District Value":gv(district_data,"Annual ET₀ (mm)"),"Clinical Interpretation":"Higher = air pulls more moisture from body (greater dryness pressure)."},
        {"Dataset Field":"Mean VPD (kPa)","District Value":gv(district_data,"Mean VPD (kPa)"),"Clinical Interpretation":"Direct dryness stress indicator — helpful for Vata-prone regional behaviour."},
        {"Dataset Field":"Mean Temperature (°C)","District Value":gv(district_data,"Mean Temp (°C)"),"Clinical Interpretation":"Thermal burden context for Pitta load and hydration strategy."},
        {"Dataset Field":"Water Ecology Modifier","District Value":gv(district_data,"Water Ecology Modifier"),"Clinical Interpretation":"Encodes hydrological features that shift Desha signatures."},
        {"Dataset Field":"Vegetation Modifier","District Value":gv(district_data,"Vegetation Modifier"),"Clinical Interpretation":"Biomass cover effects on local heat-moisture buffering."},
    ]

def condition_triggers(district_data, vyapad_results, weather_forecast, condition_choice):
    if condition_choice == "Not Provided":
        return None, []
    c = CONDITION_PROFILES.get(condition_choice, {})
    max_rain = max_temp = max_rh = 0.0
    if weather_forecast is not None and not weather_forecast.empty:
        max_rain = float(weather_forecast["Forecast Rain (mm)"].max())
        max_temp = float(weather_forecast["Forecast Temp (deg C)"].max())
        max_rh   = float(weather_forecast["Forecast RH (%)"].max())
    triggers = []
    if c.get("worse_humidity") and max_rh >= 75:    triggers.append("high humidity")
    if c.get("worse_rain")     and max_rain >= 10:  triggers.append("rain surge")
    if c.get("worse_heat")     and max_temp >= 34:  triggers.append("heat load")
    if c.get("worse_dryness"):
        try:
            if float(gv(district_data,"Mean VPD (kPa)",0)) >= 1.5:
                triggers.append("dryness stress (high VPD)")
        except Exception:
            pass
    if c.get("worse_cold_damp") and "Vyapad" in vyapad_results["status"]:
        triggers.append("seasonal instability")
    desha_full = str(gv(district_data,"Final Desha Classification","")).upper()
    desha_parts = [p.strip() for p in desha_full.split("-")]
    if c.get("desha_sensitive") and any(p in c.get("desha_sensitive",[]) for p in desha_parts):
        triggers.append(f"{desha_full} Desha sensitivity")
    if triggers:
        warning = (f"For **{condition_choice}**, current regional-weather pattern indicates aggravation risk "
                   f"due to: {', '.join(triggers)}. Consider stricter Ahara-Vihara discipline and early symptom monitoring.")
    else:
        warning = None
    return warning, triggers

# ─────────────────────────────────────────────────────────────────────────────
# CSS
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.main{background:linear-gradient(180deg,#f8fbf7 0%,#f3f8f4 100%);}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#1f4a3b 0%,#2f6c57 100%);}
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] .stMarkdown{color:#f7fff7 !important;}
section[data-testid="stSidebar"] div[data-baseweb="select"]>div{background-color:#fff !important;color:#1f2d27 !important;}
section[data-testid="stSidebar"] div[data-baseweb="select"] *{color:#1f2d27 !important;}
.block-container{padding-top:1rem;}
h1,h2,h3{color:#163c2f !important;}
button[data-baseweb="tab"]{background:#eef5f0 !important;border-radius:999px !important;margin-right:6px !important;padding:7px 12px !important;border:1px solid #d5e6da !important;font-size:12px !important;}
button[data-baseweb="tab"][aria-selected="true"]{background:#1f6a4f !important;color:#fff !important;border:1px solid #1f6a4f !important;}
.section-box{background:#fff;border:1px solid #d9eadf;border-radius:12px;padding:14px;margin-top:8px;}
.soft-note{background:linear-gradient(90deg,#eef8f1,#f7fcf8);border-left:4px solid #2e7d32;padding:10px 12px;border-radius:8px;}
.ritusandhi-critical{background:#fff3e0;border-left:5px solid #e65100;padding:12px 16px;border-radius:8px;margin-bottom:12px;}
.ritusandhi-imminent{background:#fff8e1;border-left:5px solid #ffa000;padding:12px 16px;border-radius:8px;margin-bottom:12px;}
.ritusandhi-approaching{background:#f1f8e9;border-left:5px solid #558b2f;padding:12px 16px;border-radius:8px;margin-bottom:12px;}
.samhita-card{background:#fafffe;border:1px solid #b2dfdb;border-radius:10px;padding:12px 16px;margin-bottom:10px;}
.samhita-ref{font-size:11px;color:#00695c;font-weight:600;}
.samhita-text{font-style:italic;color:#37474f;font-size:12px;margin:4px 0;}
.samhita-explain{font-size:11px;color:#546e7a;background:#f5f5f5;border-radius:6px;padding:6px 10px;margin-top:6px;}
.pk-optimal{background:#e8f5e9;border-left:4px solid #2e7d32;border-radius:8px;padding:10px 14px;margin-bottom:8px;}
.pk-beneficial{background:#e3f2fd;border-left:4px solid #1565c0;border-radius:8px;padding:10px 14px;margin-bottom:8px;}
.pk-caution{background:#fff8e1;border-left:4px solid #f57f17;border-radius:8px;padding:10px 14px;margin-bottom:8px;}
.pk-avoid{background:#ffebee;border-left:4px solid #c62828;border-radius:8px;padding:10px 14px;margin-bottom:8px;}
.pa-pathya{background:#e8f5e9;border-radius:8px;padding:10px 14px;margin-bottom:8px;}
.pa-apathya{background:#ffebee;border-radius:8px;padding:10px 14px;margin-bottom:8px;}
.compare-card{background:#fff;border:1px solid #cfd8dc;border-radius:12px;padding:14px;height:100%;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TITLE
# ─────────────────────────────────────────────────────────────────────────────
st.title("🌿 Desha-Kala Clinical Navigator v2")
st.markdown("##### Classical Ayurvedic intelligence · Real-time weather · District-specific Pathya · Samhita references")
st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────
master_df, rutu_df, foundations_df = load_ayurvedic_knowledge_base()
samhita_corpus = load_samhita_reference_corpus()
pathya_excel_path = get_pathya_apathya_excel_path()

if master_df is None or rutu_df is None:
    st.error("Knowledge base not loaded. Please copy 'Rutu_Desha_AI_KnowledgeBase_v1.0.xlsx' into the data/ folder.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — Patient Environment
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("🏥 Patient Environment")
    states = sorted(master_df["State / UT"].unique())
    default_state_idx = states.index("Karnataka") if "Karnataka" in states else 0
    selected_state = st.selectbox("Patient State / UT", states, index=default_state_idx)

    districts_list = sorted(master_df[master_df["State / UT"] == selected_state]["District"].unique())
    default_dist_idx = districts_list.index("Bengaluru Urban") if selected_state=="Karnataka" and "Bengaluru Urban" in districts_list else 0
    selected_district = st.selectbox("Patient District", districts_list, index=default_dist_idx)

    selected_date   = st.date_input("Consultation Date", datetime.date.today())
    prakruti_choice = st.selectbox("Patient Prakruti (Optional)",
        ["Not Provided","Vata","Pitta","Kapha","Vata-Pitta","Pitta-Kapha","Vata-Kapha"], index=0)
    condition_choice = st.selectbox("Clinical Condition (Optional)",
        ["Not Provided"] + sorted(CONDITION_PROFILES.keys()), index=0)

    st.markdown("---")
    st.markdown("### 🗺 Map Filters")
    desha_filter_options = ["Anupa","Jangala","Sadharana","Sadharana-Anupa","Sadharana-Jangala"]
    selected_desha_filters = st.multiselect("Show Desha Classes on Map",
        options=desha_filter_options, default=desha_filter_options)

# ─────────────────────────────────────────────────────────────────────────────
# DISTRICT DATA + CORE COMPUTATIONS
# ─────────────────────────────────────────────────────────────────────────────
matching = master_df[(master_df["State / UT"]==selected_state) & (master_df["District"]==selected_district)]
if matching.empty:
    st.warning("District data not found. Please check the knowledge base.")
    st.stop()

district_data  = matching.iloc[0]
lat = district_data.get("Latitude (°N)", district_data.get("Latitude (Â°N)"))
lon = district_data.get("Longitude (°E)", district_data.get("Longitude (Â°E)"))
current_rutu   = map_date_to_rutu(selected_date)
upcoming_rutu  = get_upcoming_rutu(current_rutu)

local_profile = rutu_df[
    (rutu_df["State"].str.lower() == selected_state.lower()) &
    (rutu_df["District"].str.lower().str.contains(selected_district.lower(), regex=False)) &
    (rutu_df["Rutu (Season)"] == current_rutu)
]

with st.spinner("Fetching 5-day history + 7-day forecast..."):
    weather_history, weather_forecast, weather_compare = fetch_weather_7day(lat, lon)

vyapad_results  = analyze_rutu_vyapad(current_rutu, local_profile, weather_history)
ritusandhi_info = calculate_ritusandhi_status(selected_date)
desha_class     = str(district_data.get("Final Desha Classification","Sadharana"))

# ─────────────────────────────────────────────────────────────────────────────
# TOP METRICS
# ─────────────────────────────────────────────────────────────────────────────
m1, m2, m3, m4, m5 = st.columns(5)
m1.metric("Bhumi Desha", desha_class)
m2.metric("Rutu (Season)", current_rutu)
m3.metric("Upcoming Rutu", upcoming_rutu)
m4.metric("Agni Baseline", local_profile["Agni State"].values[0] if not local_profile.empty else "Manda")
m5.metric("Inherent Bala",  local_profile["Bala Level"].values[0]  if not local_profile.empty else "Madhyama")

# Vyapad status banner
if "Vyapad" in vyapad_results["status"]:
    st.error(f"⚠️ Clinical Alert: {vyapad_results['status']} — {'; '.join(vyapad_results.get('reasons',[]))}")
else:
    st.success("✅ Seasonally Aligned (Prakritistha) — Weather within expected seasonal range")

# ─────────────────────────────────────────────────────────────────────────────
# RITUSANDHI BANNER (persistent across all tabs)
# ─────────────────────────────────────────────────────────────────────────────
rs = ritusandhi_info
if rs["urgency"] != "none":
    urgency_class = {"critical":"ritusandhi-critical","imminent":"ritusandhi-imminent","approaching":"ritusandhi-approaching"}.get(rs["urgency"],"ritusandhi-approaching")
    urgency_emoji = {"critical":"🔴","imminent":"🟠","approaching":"🟡"}.get(rs["urgency"],"🟢")
    transition_str = rs.get("transition_key","").replace("->"," → ")
    days_left = rs["days_to_next_transition"]
    next_date  = rs.get("next_transition_date","")
    insight    = rs.get("insight",{})
    banner_html = f"""
    <div class="{urgency_class}">
      <strong>{urgency_emoji} RITUSANDHI ALERT — {transition_str}</strong>
      &nbsp;|&nbsp; <strong>{days_left} days</strong> to seasonal transition ({next_date})<br/>
      <span style="font-size:12px">{insight.get('description','')}</span>
      &nbsp;·&nbsp; <em style="font-size:11px">{insight.get('classical_ref','')}</em>
    </div>"""
    st.markdown(banner_html, unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📋 Wellness Summary",
    "🏥 Clinical Management",
    "💊 Panchakarma Advisor",
    "🥗 Pathya-Apathya",
    "🌦 7-Day Forecast",
    "⚖️ Dual-District Compare",
    "📖 Samhita References",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — WELLNESS SUMMARY
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("### Health Seeker Wellness Summary")
    st.markdown(f"**Location:** {selected_district}, {selected_state} &nbsp;|&nbsp; **Rutu:** {current_rutu} → {upcoming_rutu} &nbsp;|&nbsp; **Desha:** {desha_class}")

    recos = []
    trust_rows = []
    dosha_tendency = str(gv(district_data, "Classical Dosha Tendency"))
    agni_state = str(local_profile["Agni State"].values[0]) if not local_profile.empty else "Manda"

    recos.append(f"For {selected_district} ({desha_class}), **{current_rutu}** season — baseline attention to **{dosha_tendency}** Dosha tendency.")
    trust_rows.append({"Recommendation":"Baseline seasonal-Desha orientation","Why":"Final Desha Classification="+desha_class+"; Rutu="+current_rutu})
    if "manda" in agni_state.lower():
        recos.append("Prefer warm, freshly cooked, lighter meals. Avoid heavy late-night intake.")
        trust_rows.append({"Recommendation":"Light warm digestive-friendly meals","Why":"Agni State="+agni_state})
    if "Vyapad" in vyapad_results["status"]:
        recos.append("Seasonal aberration active — use short-term protective regimen: digestive support, sleep regularity, hydration monitoring.")
        trust_rows.append({"Recommendation":"Protective regimen (Rutu-Vyapad)","Why":"; ".join(vyapad_results.get("reasons",[]))})

    max_rain = max_temp = max_rh = 0.0
    if weather_forecast is not None and not weather_forecast.empty:
        max_rain = float(weather_forecast["Forecast Rain (mm)"].max())
        max_temp = float(weather_forecast["Forecast Temp (deg C)"].max())
        max_rh   = float(weather_forecast["Forecast RH (%)"].max())
        if max_rain >= 10:
            recos.append("7-day forecast: rain surge ahead — reduce heavy/oily meals, protect from damp-cold.")
            trust_rows.append({"Recommendation":"Rain-surge advisory","Why":f"Max forecast rain={max_rain:.1f} mm"})
        if max_temp >= 34:
            recos.append("7-day forecast: high heat load — emphasise hydration, avoid noon exposure, reduce Ushna-provoking intake.")
            trust_rows.append({"Recommendation":"Heat-load advisory","Why":f"Max forecast temp={max_temp:.1f}°C"})
        if max_rh >= 75:
            recos.append("7-day forecast: high humidity window — keep meals lighter and support digestive fire.")
            trust_rows.append({"Recommendation":"Humidity-Deepana advisory","Why":f"Max forecast RH={max_rh:.1f}%"})

    prakruti_map = {
        "Vata":"Maintain warmth, regular meal timings, avoid fasting.",
        "Pitta":"Favour cooling routine, avoid spicy-fermented foods, maintain hydration.",
        "Kapha":"Prefer light, warm, mobilising routine with regular exercise.",
        "Vata-Pitta":"Balance warmth with cooling hydration; avoid fasting and heat extremes.",
        "Pitta-Kapha":"Keep meals light and cooling, avoid oil-heavy combinations.",
        "Vata-Kapha":"Prefer warm-light diet and daily movement; avoid cold, heavy intake.",
    }
    if prakruti_choice != "Not Provided":
        recos.append(f"Prakruti guidance ({prakruti_choice}): {prakruti_map.get(prakruti_choice,'')}")
        trust_rows.append({"Recommendation":f"Prakruti advice ({prakruti_choice})","Why":"Clinician-provided Prakruti."})

    condition_warning, _ = condition_triggers(district_data, vyapad_results, weather_forecast, condition_choice)
    transition_note = (f"Currently **{current_rutu}** → transitioning to **{upcoming_rutu}**. "
                       f"A 2–3 week pre-transition Ahara-Vihara adjustment is advised.")

    for i, r in enumerate(recos, 1):
        st.markdown(f"{i}. {r}")
    st.markdown(f"**Upcoming Seasonal Note:** {transition_note}")
    if condition_warning:
        st.warning(condition_warning)

    st.markdown("#### 📊 Clinical Reasoning Trail")
    st.dataframe(trust_rows, use_container_width=True, height=240)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — CLINICAL MANAGEMENT
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("### Geo-Climatic Evidence for Clinical Translation")
    st.dataframe(build_geo_climatic_evidence(district_data), use_container_width=True, height=380)

    st.markdown("### Why This Desha Classification Was Concluded")
    rainfall = gv(district_data,"Annual Rainfall (mm)")
    rh_val   = gv(district_data,"Mean RH (%)")
    soil_val = gv(district_data,"Soil Moisture (0–7cm)")
    temp_val = gv(district_data,"Mean Temp (°C)")
    desha_explain = (f"**{desha_class}** — based on: annual rainfall ≈ {rainfall} mm, "
                     f"mean humidity ≈ {rh_val}%, soil moisture ≈ {soil_val}, mean temperature ≈ {temp_val}°C. "
                     "In clinical terms, this region has this Desha tendency year-round, modulated by seasonal changes.")
    st.markdown(f"<div class='soft-note'>{desha_explain}</div>", unsafe_allow_html=True)

    st.markdown("### India Map — District Desha Distribution")
    map_df = master_df.dropna(subset=["Latitude (°N)","Longitude (°E)","Final Desha Classification"]).copy()
    if selected_desha_filters:
        map_df = map_df[map_df["Final Desha Classification"].isin(selected_desha_filters)].copy()
    map_df["desha_color"] = map_df["Final Desha Classification"].apply(get_desha_color)
    fig_map = go.Figure()
    fig_map.add_trace(go.Scattergeo(
        lon=map_df["Longitude (°E)"], lat=map_df["Latitude (°N)"],
        text=map_df["District"]+", "+map_df["State / UT"]+" | "+map_df["Final Desha Classification"],
        mode="markers", marker=dict(size=5, color=map_df["desha_color"], opacity=0.75), name="Districts"))
    fig_map.add_trace(go.Scattergeo(
        lon=[lon], lat=[lat],
        text=[f"{selected_district}, {selected_state} | {desha_class}"],
        mode="markers+text", textposition="top center",
        marker=dict(size=12, color="#111", line=dict(width=1,color="#fff")), name="Selected"))
    fig_map.update_geos(scope="asia", projection_type="mercator", showcountries=True,
        countrycolor="rgb(180,180,180)", lataxis_range=[5,38], lonaxis_range=[67,98],
        showland=True, landcolor="rgb(235,245,236)")
    fig_map.update_layout(height=420, margin=dict(l=0,r=0,t=0,b=0))
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown("**Desha Colours:** <span style='color:#2e7d32'><b>Anupa</b></span> | "
                "<span style='color:#c62828'><b>Jangala</b></span> | "
                "<span style='color:#1565c0'><b>Sadharana</b></span> | "
                "<span style='color:#43a047'><b>Sadharana-Anupa</b></span> | "
                "<span style='color:#ef6c00'><b>Sadharana-Jangala</b></span>", unsafe_allow_html=True)

    st.markdown("### Dosha Progression — Current vs Upcoming Rutu")
    progress_df = build_dosha_progression_table(current_rutu, upcoming_rutu)
    c_cols = ["Dosha", f"{current_rutu} Sanchaya", f"{current_rutu} Prakopa", f"{current_rutu} Prashama", "Clinical Takeaway"]
    u_cols = ["Dosha", f"{upcoming_rutu} Sanchaya", f"{upcoming_rutu} Prakopa", f"{upcoming_rutu} Prashama", "Clinical Takeaway"]
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown(f"**Current: {current_rutu}**")
        st.dataframe([{k:r[k] for k in c_cols} for r in progress_df], use_container_width=True, height=175)
    with col_b:
        st.markdown(f"**Upcoming: {upcoming_rutu}**")
        st.dataframe([{k:r[k] for k in u_cols} for r in progress_df], use_container_width=True, height=175)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — PANCHAKARMA ADVISOR
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("### 💊 Panchakarma Timing Advisor")
    st.markdown(f"*Based on current Rutu: **{current_rutu}** | Vyapad status: {vyapad_results['status']}*")

    pk_advice = get_panchakarma_advice(current_rutu, vyapad_results["status"], prakruti_choice, condition_choice)

    if pk_advice.get("extra_cautions"):
        for caution in pk_advice["extra_cautions"]:
            st.error(caution)

    # Optimal
    if pk_advice.get("optimal"):
        st.markdown("#### ✅ Optimal Panchakarma — Strongly Indicated")
        for item in pk_advice["optimal"]:
            st.markdown(f"""
<div class='pk-optimal'>
<strong>🟢 {item['full_name']}</strong> — <em>Dosha: {item['dosha_target']}</em><br/>
<span style='font-size:12px;color:#1b5e20'><strong>Classical Basis:</strong> {item['classical_basis']}</span><br/><br/>
<table style='width:100%;font-size:12px;'>
<tr><td style='width:160px;font-weight:600;color:#2e7d32'>Poorvakarma</td><td>{item.get('poorvakarma','')}</td></tr>
<tr><td style='font-weight:600;color:#2e7d32'>Pradhana Karma</td><td>{item.get('pradhana_karma','')}</td></tr>
<tr><td style='font-weight:600;color:#2e7d32'>Pashchat Karma</td><td>{item.get('pashchat_karma','')}</td></tr>
<tr><td style='font-weight:600;color:#2e7d32'>Total Duration</td><td>{item.get('duration_total','')}</td></tr>
<tr><td style='font-weight:600;color:#c62828'>Contraindications</td><td>{item.get('contraindications','')}</td></tr>
</table>
</div>""", unsafe_allow_html=True)

    # Beneficial
    if pk_advice.get("beneficial"):
        st.markdown("#### 🔵 Beneficial — Indicated with Appropriate Assessment")
        for item in pk_advice["beneficial"]:
            st.markdown(f"""
<div class='pk-beneficial'>
<strong>🔵 {item['full_name']}</strong> — <em>Dosha: {item['dosha_target']}</em><br/>
<span style='font-size:12px;color:#0d47a1'><strong>Classical Basis:</strong> {item['classical_basis']}</span><br/><br/>
<table style='width:100%;font-size:12px;'>
<tr><td style='width:160px;font-weight:600'>Poorvakarma</td><td>{item.get('poorvakarma','')}</td></tr>
<tr><td style='font-weight:600'>Pradhana Karma</td><td>{item.get('pradhana_karma','')}</td></tr>
<tr><td style='font-weight:600'>Total Duration</td><td>{item.get('duration_total','')}</td></tr>
<tr><td style='font-weight:600;color:#c62828'>Contraindications</td><td>{item.get('contraindications','')}</td></tr>
</table>
</div>""", unsafe_allow_html=True)

    # Use with caution
    if pk_advice.get("use_with_caution"):
        st.markdown("#### 🟡 Use With Caution")
        for item in pk_advice["use_with_caution"]:
            st.markdown(f"<div class='pk-caution'>⚠️ <strong>{item['karma']}</strong> — {item['reason']}</div>", unsafe_allow_html=True)

    # Avoid
    if pk_advice.get("avoid"):
        st.markdown("#### 🔴 Contraindicated This Season")
        for item in pk_advice["avoid"]:
            st.markdown(f"<div class='pk-avoid'>🚫 <strong>{item['karma']}</strong> — {item['reason']}</div>", unsafe_allow_html=True)

    # Agni guidance
    st.markdown("---")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 🔥 Agni Guidance")
        st.info(pk_advice.get("agni_guidance",""))
    with col2:
        st.markdown("#### 🌿 Rasayana Window")
        st.success(pk_advice.get("rasayana_window",""))

    st.markdown("#### 🔬 Contemporary Scientific Insight")
    st.markdown(f"<div class='soft-note'>{pk_advice.get('scientific_insight','')}</div>", unsafe_allow_html=True)

    st.markdown("#### ⏱ Ritusandhi Protocol for This Transition")
    st.markdown(f"<div class='soft-note'>{pk_advice.get('ritusandhi_note','')}</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — PATHYA-APATHYA
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown(f"### 🥗 Pathya-Apathya — {selected_district}, {selected_state}")
    st.markdown(f"*Rutu: **{current_rutu}** | Desha: **{desha_class}** | Condition: **{condition_choice}***")

    pa_data = get_combined_pathya_apathya(
        selected_state, selected_district, desha_class,
        current_rutu, condition_choice, pathya_excel_path
    )

    fp = pa_data["food_profile"]
    rg = pa_data["rutu_guidance"]
    cg = pa_data["condition_guidance"]
    dm = pa_data["desha_modifier"]

    # Food availability
    st.markdown(f"#### 🗺 Locally Available Foods — {selected_district} *(Source: {fp.get('source','')})*")
    if fp.get("geo_zone"):
        st.caption(f"Geo-Zone: {fp['geo_zone']}")

    food_cols = ["cereals","pulses","vegetables","fruits","oils","spices","dairy"]
    food_labels = {"cereals":"🌾 Cereals","pulses":"🫘 Pulses","vegetables":"🥦 Vegetables",
                   "fruits":"🍎 Fruits","oils":"🫙 Oils","spices":"🌶 Spices","dairy":"🥛 Dairy"}
    grid_cols = st.columns(3)
    for i, fkey in enumerate(food_cols):
        val = fp.get(fkey,"")
        if val and val not in ("nan",""):
            with grid_cols[i % 3]:
                st.markdown(f"**{food_labels[fkey]}**")
                for item in val.split(","):
                    item = item.strip()
                    if item:
                        st.markdown(f"• {item}")
    if fp.get("special_items") and fp["special_items"] not in ("nan",""):
        st.markdown(f"**🌟 Special Local Foods:** {fp['special_items']}")

    st.markdown("---")

    # Rutu guidance
    st.markdown(f"#### 🌿 {current_rutu} Pathya (Wholesome Foods for This Season)")
    st.caption(f"*Principle: {rg.get('ahara_principle','')}*")
    if rg.get("pathya"):
        pathya = rg["pathya"]
        pa_grid = st.columns(3)
        cats = [("cereals","🌾 Cereals"),("pulses","🫘 Pulses"),("vegetables","🥦 Vegetables"),
                ("fruits","🍎 Fruits"),("oils","🫙 Oils & Dairy"),("beverages","☕ Beverages")]
        for i, (cat_key, cat_label) in enumerate(cats):
            items = pathya.get(cat_key, [])
            if items:
                with pa_grid[i % 3]:
                    st.markdown(f"<div class='pa-pathya'><strong>{cat_label}</strong><br/>" +
                                "".join(f"• {it}<br/>" for it in items) + "</div>", unsafe_allow_html=True)
        if pathya.get("classical_note"):
            st.markdown(f"<div class='soft-note'>📜 {pathya['classical_note']}</div>", unsafe_allow_html=True)

    st.markdown(f"#### ⛔ {current_rutu} Apathya (Unwholesome Foods This Season)")
    if rg.get("apathya"):
        apathya = rg["apathya"]
        ap_grid = st.columns(3)
        for i, (cat_key, cat_label) in enumerate(cats):
            items = apathya.get(cat_key, [])
            if items:
                with ap_grid[i % 3]:
                    st.markdown(f"<div class='pa-apathya'><strong>{cat_label}</strong><br/>" +
                                "".join(f"• {it}<br/>" for it in items) + "</div>", unsafe_allow_html=True)
        if apathya.get("classical_note"):
            st.markdown(f"<div class='soft-note'>📜 {apathya['classical_note']}</div>", unsafe_allow_html=True)

    # Condition-specific
    if cg:
        st.markdown(f"---\n#### 🏥 Condition-Specific Pathya-Apathya — {condition_choice}")
        col_p, col_a = st.columns(2)
        with col_p:
            st.markdown("**✅ Pathya (Recommended)**")
            st.markdown(f"<div class='pa-pathya'>{cg.get('pathya','')}</div>", unsafe_allow_html=True)
        with col_a:
            st.markdown("**⛔ Apathya (Avoid)**")
            st.markdown(f"<div class='pa-apathya'>{cg.get('apathya','')}</div>", unsafe_allow_html=True)
        if cg.get("seasonal_note"):
            st.info(f"🗓 Seasonal Note: {cg['seasonal_note']}")
        if cg.get("desha_note"):
            st.markdown(f"<div class='soft-note'>🗺 Desha Note: {cg['desha_note']}</div>", unsafe_allow_html=True)

    # Desha modifier
    st.markdown("---")
    st.markdown(f"#### 🌍 Desha Modifier — {desha_class.split('-')[0].upper()} Year-Round Adjustments")
    dm_c1, dm_c2 = st.columns(2)
    with dm_c1:
        st.markdown("**Always Prefer**")
        for item in dm.get("always_prefer",[]):
            st.markdown(f"✅ {item}")
    with dm_c2:
        st.markdown("**Always Reduce**")
        for item in dm.get("always_reduce",[]):
            st.markdown(f"⛔ {item}")
    st.markdown(f"<div class='soft-note'><strong>Principle:</strong> {dm.get('principle','')}</div>", unsafe_allow_html=True)

    # Local specifics from Desha modifier
    local_sp = dm.get("local_specifics",{})
    if local_sp:
        for region, note in local_sp.items():
            if selected_state.lower() in region.lower() or region.lower() in selected_state.lower():
                st.markdown(f"<div class='soft-note'>🌿 <strong>Regional Note ({region}):</strong> {note}</div>", unsafe_allow_html=True)
                break

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — 7-DAY FORECAST
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown(f"### 🌦 7-Day Extended Forecast — {selected_district}, {selected_state}")
    st.markdown("*Past 5 days observed + Next 7 days forecast with Ayurvedic clinical advisory*")

    if weather_history is not None and not weather_history.empty:
        # Combined chart
        st.markdown("#### 📈 Temperature & Humidity — Last 5 Days")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=weather_history["Date"], y=weather_history["Mean Temperature (deg C)"],
            name="Temperature (°C)", line=dict(color="#cf5d36", width=3)))
        fig.add_trace(go.Scatter(x=weather_history["Date"], y=weather_history["Mean Relative Humidity (%)"],
            name="Humidity (%)", line=dict(color="#2b614d", width=3)))
        fig.add_trace(go.Bar(x=weather_history["Date"], y=weather_history["Total Rainfall (mm)"],
            name="Rainfall (mm)", marker_color="#1565c0", opacity=0.5, yaxis="y2"))
        fig.update_layout(height=350, yaxis2=dict(overlaying="y", side="right", title="Rainfall (mm)"),
            legend=dict(orientation="h", y=-0.2), margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig, use_container_width=True)
        st.dataframe(weather_history, use_container_width=True, height=220)
    else:
        st.warning("Weather history unavailable — check network connection.")

    if weather_forecast is not None and not weather_forecast.empty:
        st.markdown("#### 🔭 7-Day Forecast with Clinical Advisories")
        # Forecast chart
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=weather_forecast["Date"], y=weather_forecast["Forecast Temp (deg C)"],
            name="Forecast Temp (°C)", line=dict(color="#e64a19", width=3, dash="dot")))
        fig2.add_trace(go.Scatter(x=weather_forecast["Date"], y=weather_forecast["Forecast RH (%)"],
            name="Forecast RH (%)", line=dict(color="#00838f", width=3, dash="dot")))
        fig2.add_trace(go.Bar(x=weather_forecast["Date"], y=weather_forecast["Forecast Rain (mm)"],
            name="Forecast Rain (mm)", marker_color="#5c6bc0", opacity=0.6, yaxis="y2"))
        fig2.update_layout(height=320, yaxis2=dict(overlaying="y", side="right", title="Rain (mm)"),
            legend=dict(orientation="h", y=-0.2), margin=dict(l=0,r=0,t=20,b=0))
        st.plotly_chart(fig2, use_container_width=True)
        st.dataframe(weather_forecast, use_container_width=True, height=310)
    else:
        st.warning("7-day forecast unavailable.")

    if weather_compare is not None and not weather_compare.empty:
        st.markdown("#### 📊 Year-over-Year Comparison (Current vs Last Year)")
        st.dataframe(weather_compare, use_container_width=True, height=350)

    # Ayurvedic 7-day interpretation
    st.markdown("#### 🌿 Ayurvedic Clinical Interpretation of Forecast Window")
    if weather_forecast is not None and not weather_forecast.empty:
        max_r = float(weather_forecast["Forecast Rain (mm)"].max())
        max_t = float(weather_forecast["Forecast Temp (deg C)"].max())
        max_h = float(weather_forecast["Forecast RH (%)"].max())
        avg_t = float(weather_forecast["Forecast Temp (deg C)"].mean())
        interp = []
        if max_r >= 20:
            interp.append("🌧 **Heavy Rain Surge** — Vata-Pitta aggravation risk. Strict Agni protection (Panchakola Phanta). Avoid raw food, cold water. Basti contraindicated if planned.")
        elif max_r >= 10:
            interp.append("🌦 **Rain in Forecast** — Mild Agni impairment expected. Prefer Kitchari, warm Ushna Jala. Avoid heavy pulses on rainy days.")
        if max_t >= 36:
            interp.append("🌡 **High Heat Alert** — Pitta-Rakta risk. Increase coconut water, tender coconut, Shatavari milk. Avoid Tikshna-Amla-Lavana foods. Reschedule vigorous Svedana procedures.")
        elif max_t >= 33:
            interp.append("☀️ **Moderate Heat** — Maintain cooling routine. Coconut water and Madhura diet.")
        if max_h >= 80:
            interp.append("💧 **Very High Humidity** — Kapha-Ama formation risk. Mandatory Deepana-Pachana (Chitrakadi Vati or Trikatu). Lighter meals, warm water, avoid daytime sleep.")
        elif max_h >= 70:
            interp.append("🌫 **Moderate Humidity** — Keep digestive fire supported. Spiced buttermilk post-meals.")
        if not interp:
            interp.append("✅ **Stable Weather Window** — Favourable for Panchakarma planning and routine Rasayana administration.")
        for line in interp:
            st.markdown(f"<div class='soft-note'>{line}</div>", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 6 — DUAL-DISTRICT COMPARISON
# ══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown("### ⚖️ Dual-District Patient Comparison")
    st.markdown("*Compare two patients from different districts — useful for relocated patients, family consultations, or multi-centre clinical decisions.*")

    cmp_c1, cmp_c2 = st.columns(2)
    with cmp_c1:
        st.markdown("#### 👤 Patient A")
        cmp_state_a = st.selectbox("State A", states, index=states.index(selected_state), key="cmp_state_a")
        cmp_dist_a_list = sorted(master_df[master_df["State / UT"]==cmp_state_a]["District"].unique())
        default_a = cmp_dist_a_list.index(selected_district) if selected_district in cmp_dist_a_list else 0
        cmp_dist_a  = st.selectbox("District A", cmp_dist_a_list, index=default_a, key="cmp_dist_a")
    with cmp_c2:
        st.markdown("#### 👤 Patient B")
        cmp_state_b = st.selectbox("State B", states, index=0, key="cmp_state_b")
        cmp_dist_b_list = sorted(master_df[master_df["State / UT"]==cmp_state_b]["District"].unique())
        cmp_dist_b  = st.selectbox("District B", cmp_dist_b_list, index=0, key="cmp_dist_b")

    # Resolve data for both
    def get_district_summary(state, district, rutu):
        rows = master_df[(master_df["State / UT"]==state) & (master_df["District"]==district)]
        if rows.empty:
            return None, None, None
        dd = rows.iloc[0]
        profile = rutu_df[
            (rutu_df["State"].str.lower()==state.lower()) &
            (rutu_df["District"].str.lower().str.contains(district.lower(), regex=False)) &
            (rutu_df["Rutu (Season)"]==rutu)
        ]
        return dd, profile, rows

    dd_a, prof_a, _ = get_district_summary(cmp_state_a, cmp_dist_a, current_rutu)
    dd_b, prof_b, _ = get_district_summary(cmp_state_b, cmp_dist_b, current_rutu)

    if dd_a is None or dd_b is None:
        st.warning("District data not found for one or both selections.")
    else:
        # Fetch weather for both districts
        lat_a = dd_a.get("Latitude (°N)", dd_a.get("Latitude (Â°N)"))
        lon_a = dd_a.get("Longitude (°E)", dd_a.get("Longitude (Â°E)"))
        lat_b = dd_b.get("Latitude (°N)", dd_b.get("Latitude (Â°N)"))
        lon_b = dd_b.get("Longitude (°E)", dd_b.get("Longitude (Â°E)"))

        with st.spinner("Fetching weather for both districts..."):
            wh_a, wf_a, _ = fetch_weather_7day(lat_a, lon_a)
            wh_b, wf_b, _ = fetch_weather_7day(lat_b, lon_b)

        vyapad_a = analyze_rutu_vyapad(current_rutu, prof_a, wh_a)
        vyapad_b = analyze_rutu_vyapad(current_rutu, prof_b, wh_b)
        rs_a = calculate_ritusandhi_status(selected_date)
        rs_b = calculate_ritusandhi_status(selected_date)  # same date, different Desha context

        def metric_card(label, val_a, val_b, highlight_diff=True):
            same = str(val_a).strip().lower() == str(val_b).strip().lower()
            color = "#f0f7f4" if same else "#fff8e1"
            return (f"<tr style='background:{color}'>"
                    f"<td style='padding:6px 10px;font-weight:600;font-size:12px'>{label}</td>"
                    f"<td style='padding:6px 10px;font-size:12px;text-align:center'>{val_a}</td>"
                    f"<td style='padding:6px 10px;font-size:12px;text-align:center'>{val_b}</td></tr>")

        desha_a = str(gv(dd_a,"Final Desha Classification"))
        desha_b = str(gv(dd_b,"Final Desha Classification"))
        agni_a  = str(prof_a["Agni State"].values[0]) if prof_a is not None and not prof_a.empty else "N/A"
        agni_b  = str(prof_b["Agni State"].values[0]) if prof_b is not None and not prof_b.empty else "N/A"
        bala_a  = str(prof_a["Bala Level"].values[0])  if prof_a is not None and not prof_a.empty else "N/A"
        bala_b  = str(prof_b["Bala Level"].values[0])  if prof_b is not None and not prof_b.empty else "N/A"
        dosha_a = str(gv(dd_a,"Classical Dosha Tendency"))
        dosha_b = str(gv(dd_b,"Classical Dosha Tendency"))
        rain_a  = str(gv(dd_a,"Annual Rainfall (mm)"))
        rain_b  = str(gv(dd_b,"Annual Rainfall (mm)"))
        rh_a    = str(gv(dd_a,"Mean RH (%)"))
        rh_b    = str(gv(dd_b,"Mean RH (%)"))
        temp_a  = str(gv(dd_a,"Mean Temp (°C)"))
        temp_b  = str(gv(dd_b,"Mean Temp (°C)"))
        vyapad_a_str = "✅ Stable" if "Stable" in vyapad_a["status"] else "⚠️ Aberrant"
        vyapad_b_str = "✅ Stable" if "Stable" in vyapad_b["status"] else "⚠️ Aberrant"

        curr_t_a = f"{wh_a['Mean Temperature (deg C)'].mean():.1f}°C" if wh_a is not None and not wh_a.empty else "N/A"
        curr_t_b = f"{wh_b['Mean Temperature (deg C)'].mean():.1f}°C" if wh_b is not None and not wh_b.empty else "N/A"
        curr_rh_a = f"{wh_a['Mean Relative Humidity (%)'].mean():.1f}%" if wh_a is not None and not wh_a.empty else "N/A"
        curr_rh_b = f"{wh_b['Mean Relative Humidity (%)'].mean():.1f}%" if wh_b is not None and not wh_b.empty else "N/A"
        fore_t_a = f"{wf_a['Forecast Temp (deg C)'].mean():.1f}°C" if wf_a is not None and not wf_a.empty else "N/A"
        fore_t_b = f"{wf_b['Forecast Temp (deg C)'].mean():.1f}°C" if wf_b is not None and not wf_b.empty else "N/A"

        table_html = f"""
        <table style='width:100%;border-collapse:collapse;'>
        <thead><tr style='background:#1f6a4f;color:white;'>
            <th style='padding:8px 10px;font-size:12px;text-align:left'>Parameter</th>
            <th style='padding:8px 10px;font-size:12px;text-align:center'>👤 {cmp_dist_a}, {cmp_state_a[:5]}..</th>
            <th style='padding:8px 10px;font-size:12px;text-align:center'>👤 {cmp_dist_b}, {cmp_state_b[:5]}..</th>
        </tr></thead><tbody>
        {metric_card("Desha Classification", desha_a, desha_b)}
        {metric_card("Classical Dosha Tendency", dosha_a, dosha_b)}
        {metric_card("Current Rutu Agni", agni_a, agni_b)}
        {metric_card("Inherent Bala", bala_a, bala_b)}
        {metric_card("Annual Rainfall (mm)", rain_a, rain_b)}
        {metric_card("Mean Humidity (%)", rh_a, rh_b)}
        {metric_card("Mean Temperature (°C)", temp_a, temp_b)}
        {metric_card("Rutu-Vyapad Status", vyapad_a_str, vyapad_b_str)}
        {metric_card("Current 5-Day Avg Temp", curr_t_a, curr_t_b)}
        {metric_card("Current 5-Day Avg RH", curr_rh_a, curr_rh_b)}
        {metric_card("7-Day Forecast Avg Temp", fore_t_a, fore_t_b)}
        </tbody></table>"""
        st.markdown(table_html, unsafe_allow_html=True)
        st.caption("🟡 Yellow rows = parameters that differ between the two districts.")

        # Side-by-side weather charts
        st.markdown("---")
        st.markdown("#### 🌦 Side-by-Side 7-Day Forecast")
        fcol_a, fcol_b = st.columns(2)
        with fcol_a:
            st.markdown(f"**{cmp_dist_a}**")
            if wf_a is not None and not wf_a.empty:
                fa = go.Figure()
                fa.add_trace(go.Scatter(x=wf_a["Date"],y=wf_a["Forecast Temp (deg C)"],name="Temp",line=dict(color="#cf5d36",width=2)))
                fa.add_trace(go.Bar(x=wf_a["Date"],y=wf_a["Forecast Rain (mm)"],name="Rain",marker_color="#1565c0",opacity=0.5,yaxis="y2"))
                fa.update_layout(height=260,yaxis2=dict(overlaying="y",side="right"),margin=dict(l=0,r=0,t=10,b=0),legend=dict(orientation="h",y=-0.25))
                st.plotly_chart(fa, use_container_width=True)
        with fcol_b:
            st.markdown(f"**{cmp_dist_b}**")
            if wf_b is not None and not wf_b.empty:
                fb = go.Figure()
                fb.add_trace(go.Scatter(x=wf_b["Date"],y=wf_b["Forecast Temp (deg C)"],name="Temp",line=dict(color="#2b614d",width=2)))
                fb.add_trace(go.Bar(x=wf_b["Date"],y=wf_b["Forecast Rain (mm)"],name="Rain",marker_color="#7b1fa2",opacity=0.5,yaxis="y2"))
                fb.update_layout(height=260,yaxis2=dict(overlaying="y",side="right"),margin=dict(l=0,r=0,t=10,b=0),legend=dict(orientation="h",y=-0.25))
                st.plotly_chart(fb, use_container_width=True)

        # Clinical difference analysis
        st.markdown("---")
        st.markdown("#### 🩺 Clinical Difference Analysis")
        diffs = []
        if desha_a != desha_b:
            diffs.append(f"**Desha shift** ({desha_a} → {desha_b}): The patient has moved from a {desha_a} environment to a {desha_b} environment. Re-evaluate baseline Dosha tendency and adjust Ahara-Vihara accordingly. Allow 2–3 seasons for adaptation.")
        if agni_a != agni_b and agni_a != "N/A" and agni_b != "N/A":
            diffs.append(f"**Agni difference** ({agni_a} vs {agni_b}): The two districts have different seasonal Agni baselines in {current_rutu}. This affects digestibility calculations for prescriptions.")
        if vyapad_a["status"] != vyapad_b["status"]:
            diffs.append(f"**Vyapad asymmetry**: {cmp_dist_a} is {'aberrant' if 'Vyapad' in vyapad_a['status'] else 'stable'} while {cmp_dist_b} is {'aberrant' if 'Vyapad' in vyapad_b['status'] else 'stable'}. Patients from the aberrant district need extra protective protocol.")
        try:
            rdiff = abs(float(rain_a.replace("-","0")) - float(rain_b.replace("-","0")))
            if rdiff > 500:
                diffs.append(f"**Rainfall difference** (≈{rdiff:.0f} mm/year): Significant moisture environment shift. Patient relocated from {'wetter' if float(rain_a.replace('-','0'))>float(rain_b.replace('-','0')) else 'drier'} to {'drier' if float(rain_a.replace('-','0'))>float(rain_b.replace('-','0')) else 'wetter'} district — adjust Kapha-Vata balance accordingly.")
        except Exception:
            pass
        if diffs:
            for diff in diffs:
                st.markdown(f"<div class='soft-note'>{diff}</div>", unsafe_allow_html=True)
        else:
            st.success("Both districts have similar Ayurvedic environmental profiles — standard seasonal protocol applies to both.")

# ══════════════════════════════════════════════════════════════════════════════
# TAB 7 — SAMHITA REFERENCES (Explainable AI)
# ══════════════════════════════════════════════════════════════════════════════
with tab7:
    st.markdown("### 📖 Samhita Reference Auto-Linker — Explainable AI")
    st.markdown(f"*Every recommendation in this navigator is traceable to a specific classical authority.*")
    st.markdown(f"*Context: **{desha_class}** Desha | **{current_rutu}** Rutu | Condition: **{condition_choice}***")

    # Determine doshas from condition
    cond_doshas = CONDITION_PROFILES.get(condition_choice,{}).get("doshas",[]) if condition_choice!="Not Provided" else []
    is_vyapad = "Vyapad" in vyapad_results["status"]

    # Get explainable AI references
    xai_refs = get_explainable_ai_panel(
        desha=desha_class, rutu=current_rutu,
        dosha_list=cond_doshas, condition=condition_choice, vyapad=is_vyapad
    )

    # Also try external corpus
    root_class = desha_class.split("-")[0].upper()
    ext_refs, source_type = find_relevant_samhita_references(
        samhita_corpus, root_class, current_rutu, condition_choice, top_n=5
    )

    st.markdown(f"**Reference sources active:** Built-in Classical Database" +
                (" + External Samhita Corpus (samhitas_combined_v2.xlsx)" if source_type=="external_corpus" else " *(add samhitas_combined_v2.xlsx to data/ folder to enable external corpus)*"))

    st.markdown("---")
    st.markdown("#### 🏛 Classical References — This Clinical Context")
    st.caption("Each reference explains *why* a specific recommendation was made. This is Ayurveda as Evidence-Based Medicine.")

    for i, ref in enumerate(xai_refs):
        if not isinstance(ref, dict):
            continue
        samhita_name = ref.get("samhita","")
        sthana = ref.get("sthana","")
        chapter = ref.get("chapter","")
        verse = ref.get("verse","")
        sloka_text = ref.get("text","")
        translation = ref.get("translation","")
        clinical_rel = ref.get("clinical_relevance","")
        explain_ctx = ref.get("explain_context","")

        ref_header = f"**{samhita_name}**"
        if sthana:  ref_header += f" | {sthana}"
        if chapter: ref_header += f" | {chapter}"
        if verse:   ref_header += f" | Verse: {verse}"

        with st.expander(f"📜 Reference {i+1}: {samhita_name} — {verse or chapter}", expanded=(i<3)):
            st.markdown(f"<div class='samhita-card'>"
                f"<div class='samhita-ref'>{ref_header}</div>"
                f"<div class='samhita-text'>✍ Sloka: {sloka_text}</div>"
                f"<div class='samhita-text'>🔤 Translation: {translation}</div>"
                f"<hr style='border:0;border-top:1px solid #e0e0e0;margin:8px 0'/>"
                f"<div style='font-size:12px;color:#37474f'><strong>🩺 Clinical Relevance:</strong> {clinical_rel}</div>"
                f"<div class='samhita-explain'><strong>🤖 Why this reference applies here:</strong> {explain_ctx}</div>"
                f"</div>", unsafe_allow_html=True)

    # External corpus results
    if source_type == "external_corpus" and ext_refs is not None and hasattr(ext_refs, 'iterrows'):
        st.markdown("---")
        st.markdown("#### 📚 External Samhita Corpus Matches")
        for _, row in ext_refs.iterrows():
            with st.expander(f"📖 {row.get('Source File','')} | {row.get('Sthana','')} | Sloka {row.get('Sloka No.','')}"):
                st.markdown(f"""
<div class='samhita-card'>
<div class='samhita-ref'>📗 {row.get('Source File','')} | {row.get('Sthana','')} | {row.get('Chapter','')} | Sloka {row.get('Sloka No.','')}</div>
<div class='samhita-text'>✍ {row.get('Sloka Text','')}</div>
<div class='samhita-text'>💬 {row.get('Comments','')}</div>
</div>""", unsafe_allow_html=True)

    # Reference table summary
    st.markdown("---")
    st.markdown("#### 📊 Reference Summary Table")
    table_rows = []
    for ref in xai_refs:
        if isinstance(ref, dict):
            table_rows.append({
                "Samhita": ref.get("samhita",""),
                "Sthana": ref.get("sthana",""),
                "Chapter": ref.get("chapter",""),
                "Verse": ref.get("verse",""),
                "Clinical Relevance": ref.get("clinical_relevance","")[:120]+"..."
            })
    if table_rows:
        st.dataframe(table_rows, use_container_width=True, height=300)

    # Scriptural foundations from KB
    if foundations_df is not None and "Desha Type" in foundations_df.columns:
        st.markdown("---")
        st.markdown("#### 🌿 Classical Foundations from Knowledge Base")
        sub_foundations = foundations_df[foundations_df["Desha Type"].astype(str).str.upper() == root_class]
        if not sub_foundations.empty:
            descriptors = []
            for _, r in sub_foundations.head(8).iterrows():
                t = str(r.get("English Translation","")).strip()
                if t and t.lower() not in ("nan","") :
                    try:
                        float(t)
                    except Exception:
                        descriptors.append(t)
            if descriptors:
                st.markdown(f"For **{selected_district}** ({root_class} Desha), the regional profile is characterised by: {', '.join(descriptors)}.")

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### Data Sources & Methodology")
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    st.markdown("**Weather Data**\n- Open-Meteo Forecast API (5 days history + 7 days forecast)\n- Open-Meteo Archive API (year-over-year comparison)")
with col_f2:
    st.markdown("**Clinical Knowledge Base**\n- Rutu_Desha_AI_KnowledgeBase_v1.0.xlsx\n- District Geo-Climatic data for all India\n- Pathya-Apathya District Diet dataset (v2)")
with col_f3:
    st.markdown("**Classical Sources**\n- Charaka Samhita (CS)\n- Sushruta Samhita (SS)\n- Ashtanga Hridayam (AH)\n- Madhava Nidana (MN)")
st.caption("Desha-Kala Clinical Navigator v2 · For licensed Ayurvedic physician use only · Not a substitute for clinical judgement.")

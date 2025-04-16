
import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Tableau de bord - Dow Jones & DAX", layout="wide")
st.title("📊 Tableau de bord économique - Impact sur Dow Jones 🇺🇸 et DAX 🇩🇪")
st.caption(f"Mise à jour automatique : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

FRED_API_KEY = "6ead261dfa1655d596bab77eeac672df"

def get_fred_data(series_id):
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 1
    }
    try:
        res = requests.get(url, params=params)
        data = res.json()
        obs = data.get("observations", [])
        if obs:
            val = obs[0]["value"]
            date = obs[0]["date"]
            return val, date
    except:
        return "Erreur", "N/A"
    return "N/A", "N/A"

def format_percent(value, base=1.0):
    try:
        return f"{float(value) * base:.2f}%"  # base=100 si déjà en %, sinon 1.0
    except:
        return value

def impact_analysis(label, value, ref=0):
    try:
        val = float(value)
    except:
        return "🔍 À interpréter"

    if "PIB" in label:
        return "📈 Haussier" if val > ref else "📉 Baissier"
    if "Inflation" in label:
        return "📉 Baissier" if val > ref else "📈 Haussier"
    if "chômage" in label.lower():
        return "📈 Haussier" if val < ref else "📉 Baissier"
    if "ventes" in label.lower():
        return "📈 Haussier" if val > ref else "📉 Baissier"
    if "ISM" in label or "IFO" in label:
        return "📈 Haussier" if val >= 50 else "📉 Baissier"
    if "confiance" in label.lower() or "ZEW" in label:
        return "📈 Haussier" if val >= 50 else "📉 Baissier"
    if "balance" in label.lower():
        return "📈 Haussier" if val > 0 else "📉 Baissier"
    if "taux" in label.lower():
        return "📉 Restrictif" if val > 3 else "📈 Accommodant"
    if "résultats" in label.lower():
        return "📈 Haussier" if val > 0 else "📉 Baissier"
    return "🔍 À interpréter"

# ======================= DOW JONES =======================
dow_series = {
    "PIB US (QoQ annualisé)": ("A191RL1Q225SBEA", "%"),
    "Inflation CPI US (YoY)": ("CPIAUCSL", "%"),
    "Taux de chômage US": ("UNRATE", "%"),
    "Ventes au détail US (YoY)": ("RSAFS", "%"),
    "Indice ISM manufacturier US": ("NAPMPI", ""),
    "Taux directeur Fed": ("FEDFUNDS", "%"),
    "Confiance consommateurs UMich": ("UMCSENT", ""),
    "Résultats entreprises S&P 500 (YoY)": ("SP500EARN", "%")
}

dow_data = []
for label, (code, fmt) in dow_series.items():
    val, date = get_fred_data(code)
    val_fmt = format_percent(val, 1 if fmt == "%" else 1)
    impact = impact_analysis(label, val, ref=2 if "Inflation" in label else 0)
    dow_data.append({
        "Indicateur": label,
        "Date": date,
        "Valeur": val_fmt,
        "Impact sur le Dow Jones": impact
    })

df_dow = pd.DataFrame(dow_data)

# ======================= DAX =======================
dax_series = {
    "PIB Allemagne (YoY)": ("CLVMNACSCAB1GQDE", "%"),
    "Inflation IPC Allemagne (YoY)": ("DEUCPALTT01GYM", "%"),
    "Taux de chômage Allemagne": ("LRHUTTTTDEA156S", "%"),
    "Balance commerciale Allemagne": ("XTEXVA01DEM664S", ""),
    "Taux directeur BCE": ("ECBMAIN", "%"),
    "Indice ZEW Allemagne": ("DENGSZEW", ""),
    "Indice IFO climat affaires": ("DEBUSI", ""),
    "Résultats entreprises Allemagne (simulé)": ("BSCICP03DEM665S", "%")
}

dax_data = []
for label, (code, fmt) in dax_series.items():
    val, date = get_fred_data(code)
    val_fmt = format_percent(val, 1 if fmt == "%" else 1)
    impact = impact_analysis(label, val, ref=2 if "Inflation" in label else 0)
    dax_data.append({
        "Indicateur": label,
        "Date": date,
        "Valeur": val_fmt,
        "Impact sur le DAX": impact
    })

df_dax = pd.DataFrame(dax_data)

# ======================= AFFICHAGE =======================
st.subheader("🇺🇸 Données économiques - Impact sur le Dow Jones")
st.dataframe(df_dow, use_container_width=True)

st.subheader("🇩🇪 Données économiques - Impact sur le DAX")
st.dataframe(df_dax, use_container_width=True)

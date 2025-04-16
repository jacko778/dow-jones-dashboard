
import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Indicateurs économiques - Dow Jones & DAX", layout="wide")
st.title("📈 Indicateurs économiques & Impact sur les indices Dow Jones 🇺🇸 et DAX 🇩🇪")
st.caption(f"🕒 Données mises à jour automatiquement - {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

FRED_API_KEY = "6ead261dfa1655d596bab77eeac672df"

# === Fonctions ===

def get_fred_latest(series_id):
    url = "https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": FRED_API_KEY,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 1
    }
    try:
        r = requests.get(url, params=params)
        data = r.json()
        if "observations" in data:
            obs = data["observations"][0]
            return obs["value"], obs["date"]
        else:
            return "N/A", "N/A"
    except:
        return "Erreur", "Erreur"

def analyse_impact_dow(label, value):
    try:
        val = float(value)
    except:
        return "🔍 À interpréter"
    if "PIB" in label:
        return "📈 Haussier" if val > 0 else "📉 Baissier"
    if "Inflation" in label or "CPI" in label:
        return "📉 Baissier" if val > 3 else "📈 Haussier"
    if "chômage" in label.lower():
        return "📈 Haussier" if val < 5 else "📉 Baissier"
    if "ventes" in label.lower():
        return "📈 Haussier" if val > 0 else "📉 Baissier"
    if "ISM" in label:
        return "📈 Haussier" if val >= 50 else "📉 Baissier"
    if "Fed" in label:
        return "📉 Restrictif" if val >= 5 else "📈 Accommodant"
    if "confiance" in label.lower():
        return "📈 Haussier" if val > 70 else "📉 Baissier"
    if "résultats" in label.lower():
        return "📈 Haussier" if val > 0 else "📉 Baissier"
    return "🔍 À interpréter"

def analyse_impact_dax(label, value):
    try:
        val = float(value)
    except:
        return "🔍 À interpréter"
    if "PIB" in label:
        return "📈 Haussier" if val > 0 else "📉 Baissier"
    if "Inflation" in label:
        return "📉 Baissier" if val > 3 else "📈 Haussier"
    if "chômage" in label:
        return "📈 Haussier" if val < 6 else "📉 Baissier"
    if "balance" in label.lower():
        return "📈 Haussier" if val > 0 else "📉 Baissier"
    if "BCE" in label:
        return "📉 Restrictif" if val > 3 else "📈 Accommodant"
    if "ZEW" in label or "IFO" in label:
        return "📈 Haussier" if val > 50 else "📉 Baissier"
    if "résultats" in label.lower():
        return "📈 Haussier" if val > 0 else "📉 Baissier"
    return "🔍 À interpréter"

# === Données Dow Jones ===
dow_series = {
    "PIB réel US (QoQ, annualisé)": "A191RL1Q225SBEA",
    "Inflation CPI (YoY)": "CPIAUCNS",
    "Taux de chômage (US)": "UNRATE",
    "Ventes au détail (YoY)": "RSAFS",
    "Indice ISM manufacturier": "NAPMPI",
    "Taux directeur Fed": "FEDFUNDS",
    "Confiance consommateurs UMich": "UMCSENT",
    "Résultats entreprises S&P 500": "SP500EARN"
}

dow_data = []
for label, sid in dow_series.items():
    value, date = get_fred_latest(sid)
    dow_data.append({
        "Indicateur économique": label,
        "Date": date,
        "Valeur": value,
        "Impact sur le Dow Jones": analyse_impact_dow(label, value)
    })
df_dow = pd.DataFrame(dow_data)

# === Données DAX ===
dax_series = {
    "PIB Allemagne (YoY)": "CLVMNACSCAB1GQDE",
    "Inflation IPC Allemagne (YoY)": "DEUCPALTT01GYM",
    "Taux de chômage Allemagne": "LRHUTTTTDEA156S",
    "Balance commerciale Allemagne": "XTEXVA01DEM664S",
    "Taux directeur BCE": "ECBMAIN",
    "Indice ZEW (Allemagne)": "DENGSZEW",
    "Indice IFO climat des affaires": "DEBUSI",
    "Résultats entreprises Allemagne (simulé)": "BSCICP03DEM665S"  # approximatif
}

dax_data = []
for label, sid in dax_series.items():
    value, date = get_fred_latest(sid)
    dax_data.append({
        "Indicateur économique": label,
        "Date": date,
        "Valeur": value,
        "Impact sur le DAX": analyse_impact_dax(label, value)
    })
df_dax = pd.DataFrame(dax_data)

# === Affichage Streamlit ===
st.subheader("🇺🇸 Données économiques américaines - Impact sur le Dow Jones")
st.dataframe(df_dow, use_container_width=True)

st.subheader("🇩🇪 Données économiques allemandes - Impact sur le DAX")
st.dataframe(df_dax, use_container_width=True)

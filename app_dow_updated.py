
import streamlit as st
import pandas as pd
import requests
from datetime import datetime

st.set_page_config(page_title="Indicateurs Éco - Dow Jones", layout="wide")
st.title("🇺🇸 Indicateurs économiques & Impact sur le Dow Jones")
st.caption(f"Dernière mise à jour automatique : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

FRED_API_KEY = "6ead261dfa1655d596bab77eeac672df"

# Séries FRED étendues pour un tableau plus complet
fred_series = {
    "PIB réel (US, QoQ SAAR)": "A191RL1Q225SBEA",
    "Inflation globale (CPI, YoY)": "CPIAUCNS",
    "Inflation core (Core CPI, YoY)": "CPILFESL",
    "Taux de chômage (US)": "UNRATE",
    "Ventes au détail (YoY)": "RSAFS",
    "Taux directeur Fed Funds": "FEDFUNDS",
    "Indice de confiance des consommateurs (UMich)": "UMCSENT",
    "ISM Manufacturing PMI": "NAPMPI",
    "Indice du dollar américain (DXY)": "DTWEXBGS",
    "Prix du pétrole brut (WTI)": "DCOILWTICO",
    "Indicateur avancé composite (LEI)": "USSLIND",
    "Indices boursiers S&P 500 Earnings (YoY)": "SP500EARN"
}

def get_fred_data(series_id, api_key):
    url = f"https://api.stlouisfed.org/fred/series/observations"
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "sort_order": "desc",
        "limit": 1
    }
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if "observations" in data and data["observations"]:
            obs = data["observations"][0]
            return obs["value"], obs["date"]
    except Exception as e:
        return "Erreur", "N/A"
    return None, None

# Récupération des données FRED
rows = []
for name, series_id in fred_series.items():
    value, date = get_fred_data(series_id, FRED_API_KEY)
    if value and value != ".":
        rows.append({
            "Indicateur économique": name,
            "Date": date,
            "Valeur": value
        })

df = pd.DataFrame(rows)

# Logique d’analyse d’impact
def analyser_impact(row):
    try:
        val = float(row["Valeur"])
    except:
        return "🔍 À interpréter"
    
    label = row["Indicateur économique"]
    if "PIB" in label:
        return "📈 Haussier" if val > 0 else "📉 Baissier"
    if "core" in label.lower():
        return "📉 Baissier" if val > 3 else "📈 Haussier"
    if "Inflation" in label:
        return "📉 Baissier" if val > 3 else "📈 Haussier"
    if "chômage" in label:
        return "📈 Haussier" if val < 5 else "📉 Baissier"
    if "Fed Funds" in label:
        return "📉 Baissier" if val > 4 else "📈 Haussier"
    if "WTI" in label:
        return "📉 Baissier" if val > 90 else "📈 Neutre"
    if "ISM" in label:
        return "📈 Haussier" if val >= 50 else "📉 Baissier"
    if "DXY" in label:
        return "📉 Baissier" if val > 105 else "📈 Haussier"
    if "Earnings" in label:
        return "📈 Haussier" if val > 0 else "📉 Baissier"
    if "LEI" in label:
        return "📈 Haussier" if val > 100 else "📉 Baissier"
    if "confiance" in label.lower():
        return "📈 Haussier" if val > 70 else "📉 Baissier"
    if "ventes" in label.lower():
        return "📈 Haussier" if val > 0 else "📉 Baissier"
    return "🔍 À interpréter"

df["Impact sur le Dow Jones"] = df.apply(analyser_impact, axis=1)

st.subheader("📊 Tableau mis à jour des données économiques américaines")
st.dataframe(df, use_container_width=True)

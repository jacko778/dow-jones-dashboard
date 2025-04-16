
import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# Configuration de la page
st.set_page_config(page_title="Impact Éco - Dow Jones", layout="wide")
st.title("📊 Indicateurs économiques & Impact sur le Dow Jones")
st.caption(f"Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

# Clé API FRED (personnalisée)
FRED_API_KEY = "6ead261dfa1655d596bab77eeac672df"

# Séries FRED à récupérer
fred_series = {
    "PIB (US, QoQ)": "GDP",
    "Inflation (CPI, YoY)": "CPIAUCSL",
    "Taux de chômage (US)": "UNRATE",
    "Taux d'intérêt de la Fed": "FEDFUNDS",
    "Ventes au détail (MoM)": "RSAFS",
    "Indice manufacturier ISM": "NAPM",
    "Confiance des consommateurs (CCI)": "UMCSENT",
    "Indice du dollar américain (DXY)": "DTWEXBGS",
    "Prix du pétrole brut (WTI)": "DCOILWTICO"
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

# Récupération des données
rows = []
for name, fred_id in fred_series.items():
    value, date = get_fred_data(fred_id, FRED_API_KEY)
    if value and value != ".":
        rows.append({
            "Donnée économique": name,
            "Date de publication": date,
            "Valeur": value
        })

df = pd.DataFrame(rows)

# Logique d’impact
def deduire_impact(row):
    econ = row["Donnée économique"]
    try:
        val = float(row["Valeur"])
    except:
        return "À interpréter"

    if econ == "Inflation (CPI, YoY)":
        return "📉 Baissier" if val > 2.5 else "📈 Haussier"
    if econ == "PIB (US, QoQ)":
        return "📈 Haussier" if val > 0 else "📉 Baissier"
    if econ == "Taux de chômage (US)":
        return "📈 Haussier" if val < 5 else "📉 Baissier"
    if econ == "Taux d'intérêt de la Fed":
        return "📉 Baissier" if val > 4 else "📈 Haussier"
    if econ == "Prix du pétrole brut (WTI)":
        return "📉 Baissier" if val > 90 else "📈 Neutre"
    return "🔍 À interpréter"

df["Impact sur le Dow Jones"] = df.apply(deduire_impact, axis=1)

st.subheader("📈 Tableau dynamique des données économiques (FRED)")
st.dataframe(df, use_container_width=True)

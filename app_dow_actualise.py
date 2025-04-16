
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Indicateurs Éco - Dow Jones", layout="wide")
st.title("🇺🇸 Indicateurs économiques & Impact sur le Dow Jones")
st.caption(f"📅 Dernière mise à jour : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")

# Données économiques (exemple statique, à remplacer par source live si besoin)
donnees = {
    "Donnée économique": [
        "PIB (T1 2025, QoQ annualisé)", "Inflation CPI (mars 2025, YoY)", "Chômage (mars 2025)",
        "Ventes au détail (mars 2025)", "ISM Manufacturier (mars 2025)", "Confiance consommateurs (mars 2025)",
        "Taux directeur Fed", "Indice dollar (DXY)", "Résultats entreprises (S&P 500, T1 2025)", "Prix du pétrole (WTI)"
    ],
    "Date de publication": [
        "2025-03-27", "2025-04-10", "2025-04-05", "2025-04-15", "2025-04-01",
        "2025-03-29", "2025-03-20", "2025-04-15", "2025-04-11", "2025-04-15"
    ],
    "Chiffre actuel": [
        "2.4%", "3.1%", "4.2%", "0.7%", "49.2", "67.0", "5.50%", "105.3", "-1.8%", "$74.2"
    ],
    "Prévision": [
        "2.3%", "3.1%", "4.2%", "0.6%", "48.5", "66.0", "5.50%", "105.0", "-1.5%", "$75.0"
    ],
    "Précédent": [
        "3.1%", "3.2%", "4.0%", "0.9%", "47.8", "68.3", "5.50%", "104.8", "-2.0%", "$72.8"
    ]
}

df = pd.DataFrame(donnees)

# Fonction d'impact sur le Dow Jones
def impact(row):
    econ = row["Donnée économique"]
    try:
        current_val = float(row["Chiffre actuel"].replace('%', '').replace('$', ''))
        forecast_val = float(row["Prévision"].replace('%', '').replace('$', ''))
    except:
        return "🔍 À interpréter"

    if "PIB" in econ:
        return "📈 Haussier" if current_val > forecast_val else "📉 Baissier"
    elif "Inflation" in econ:
        return "📉 Baissier" if current_val > forecast_val else "📈 Haussier"
    elif "Chômage" in econ:
        return "📉 Baissier" if current_val > forecast_val else "📈 Haussier"
    elif "Ventes" in econ:
        return "📈 Haussier" if current_val > forecast_val else "📉 Baissier"
    elif "ISM" in econ:
        return "📈 Haussier" if current_val >= 50 else "📉 Baissier"
    elif "Confiance" in econ:
        return "📉 Baissier" if current_val < forecast_val else "📈 Haussier"
    elif "Taux" in econ:
        return "📉 Restrictif" if current_val >= 5 else "📈 Accommodant"
    elif "dollar" in econ:
        return "📉 Baissier" if current_val > 105 else "📈 Haussier"
    elif "Résultats" in econ:
        return "📉 Baissier" if current_val < 0 else "📈 Haussier"
    elif "pétrole" in econ:
        return "📉 Inflationniste" if current_val > 75 else "📈 Neutre"
    else:
        return "🔍 À interpréter"

df["Impact sur le Dow Jones"] = df.apply(impact, axis=1)

# Affichage du tableau
st.subheader("📊 Données économiques récentes et analyse de l'impact")
st.dataframe(df, use_container_width=True)

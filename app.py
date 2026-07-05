import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(page_title="Simulation Acido-Basique", layout="centered")
st.title("🧪 Échelle de pH et Équilibres Acido-Basiques")

# Création de deux onglets pour structurer la séance
onglet1, onglet2 = st.tabs(["1. Relation pH / [H3O+]", "2. Force d'un acide & Taux d'avancement"])

# -----------------------------------------------------------------
# ONGLET 1 : COMPRENDRE LA RELATION LOGARITHMIQUE
# -----------------------------------------------------------------
with onglet1:
    st.header("Visualisation de la fonction logarithme")
    st.write("Faites varier le pH pour observer l'évolution de la concentration $[H_3O^+]$.")
    
    # Curseur de pH
    pH = st.slider("Sélectionner la valeur du pH :", 1.0, 14.0, 3.0, 0.1)
    
    # Calcul de [H3O+]
    h3o = 10**(-pH)
    
    st.metric(label="Concentration [H3O+] correspondante :", value=f"{h3o:.2e} mol/L")
    
    # Graphique de la courbe pH en fonction de [H3O+]
    h3o_axe = np.logspace(-6, -1, 500)
    ph_axe = -np.log10(h3o_axe)
    
    fig1, ax1 = plt.subplots(figsize=(10, 4.5))
    ax1.plot(h3o_axe, ph_axe, color='#2b6cb0', linewidth=2.5, label="$pH = -\\log[H_3O^+]$")
    ax1.plot(h3o, pH, 'ro', markersize=10, label=f"Point sélectionné (pH={pH:.1f})")
    
    ax1.set_xscale('log') # Échelle logarithmique indispensable
    ax1.set_title("Le pH en fonction de la concentration $[H_3O^+]$ (Échelle log)", fontsize=11, fontweight='bold')
    ax1.set_xlabel("Concentration $[H_3O^+]$ (mol/L) - Échelle Logarithmique", fontsize=10)
    ax1.set_ylabel("pH", fontsize=10)
    ax1.grid(True, which="both", linestyle=':', alpha=0.6)
    ax1.legend()
    
    st.pyplot(fig1)
    
    st.info("**Rappel de cours :** Lorsque le pH diminue d'une seule unité (ex: de 4 à 3), la concentration $[H_3O^+]$ ne double pas, elle est **multipliée par 10** !")

# -----------------------------------------------------------------
# ONGLET 2 : EXPÉRIMENTATION ACIDE FORT / ACIDE FAIBLE
# -----------------------------------------------------------------
with onglet2:
    st.header("Étude du taux d'avancement final ($\\tau$)")
    st.write("Modélisons l'état d'équilibre d'un acide de concentration apportée $C$ introduite dans l'eau.")
    
    # Paramètres d'entrée
    C = st.number_input("Concentration apportée en acide C (mol/L) :", min_value=1e-5, max_value=1.0, value=1e-2, format="%.1e")
    pKa = st.slider("pKa du couple acide/base (0 = acide très fort, 10 = acide très faible) :", 0.0, 14.0, 4.8, 0.1)
    
    # Résolution de l'équation du second degré pour trouver [H3O+] à l'équilibre
    # Ka = [H3O+]^2 / (C - [H3O+])  => [H3O+]^2 + Ka*[H3O+] - Ka*C = 0
    Ka = 10**(-pKa)
    delta = Ka**2 - 4 * 1 * (-Ka * C)
    h3o_eq = (-Ka + np.sqrt(delta)) / 2
    
    # Calcul du pH réel et du taux d'avancement tau
    pH_eq = -np.log10(h3o_eq)
    tau = h3o_eq / C
    
    # Affichage des indicateurs
    col1, col2 = st.columns(2)
    col1.metric("pH de la solution à l'équilibre :", f"{pH_eq:.2f}")
    col2.metric("Taux d'avancement final (τ) :", f"{tau*100:.1f} %")
    
    # Représentation visuelle des proportions Acide / Base conjuguée
    labels = ['Acide restant AH', 'Base conjuguée A- formée']
    proportions = [(1 - tau) * 100, tau * 100]
    couleurs = ['#e53e3e', '#319795']
    
    fig2, ax2 = plt.subplots(figsize=(6, 3))
    ax2.barh(labels, proportions, color=couleurs, edgecolor='black', height=0.5)
    ax2.set_xlabel("Proportion au sein de la solution (%)")
    ax2.set_xlim(0, 100)
    ax2.grid(axis='x', linestyle=':', alpha=0.6)
    
    st.pyplot(fig2)
    
    # Interprétation dynamique
    if tau > 0.99:
        st.success("💡 **Conclusion :** $\\tau \\approx 100\\%$. L'acide se dissocie totalement dans l'eau, il s'agit d'un **acide fort** ($pH \\approx -\\log C$).")
    elif tau < 0.05:
        st.warning("💡 **Conclusion :** $\\tau < 5\\%$. L'acide réagit très peu avec l'eau, il s'agit d'un **acide faible très peu dissocié**.")
    else:
        st.info("💡 **Conclusion :** $0 < \\tau < 1$. La transformation est limitée. Un équilibre chimique s'établit entre l'acide faible et sa base conjuguée.")

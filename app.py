import time
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt


# ==========================================================
# CONFIGURATION DE LA PAGE
# ==========================================================

st.set_page_config(
    page_title="Simulation temps réel de signaux",
    page_icon="📡",
    layout="wide"
)


# ==========================================================
# CHOIX DU MODE D'AFFICHAGE
# ==========================================================

theme = st.sidebar.radio(
    "🎨 Mode d'affichage",
    ["Clair", "Sombre"],
    horizontal=True
)

if theme == "Clair":
    app_bg = "#f8fafc"
    text_color = "#0f172a"
    card_bg = "#ffffff"
    border_color = "#cbd5e1"
    help_bg = "#eff6ff"
    help_border = "#93c5fd"
    sidebar_bg = "#ffffff"
    input_bg = "#ffffff"
    input_text = "#0f172a"
else:
    app_bg = "#020617"
    text_color = "#f8fafc"
    card_bg = "#0f172a"
    border_color = "#334155"
    help_bg = "#111827"
    help_border = "#475569"
    sidebar_bg = "#020617"
    input_bg = "#0f172a"
    input_text = "#f8fafc"


# ==========================================================
# STYLE CSS
# ==========================================================

st.markdown(
    f"""
    <style>
    .stApp {{
        background-color: {app_bg};
        color: {text_color};
    }}

    section[data-testid="stSidebar"] {{
        background-color: {sidebar_bg};
        color: {text_color};
    }}

    section[data-testid="stSidebar"] * {{
        color: {text_color};
    }}

    .block-container {{
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }}

    .header-box {{
        background: linear-gradient(135deg, #0f172a, #1e293b);
        padding: 28px 32px;
        border-radius: 18px;
        margin-bottom: 25px;
        border: 1px solid #334155;
        box-shadow: 0px 4px 18px rgba(0,0,0,0.18);
    }}

    .main-title {{
        font-size: 42px;
        font-weight: 800;
        color: white;
        margin-bottom: 0px;
    }}

    .card {{
        background: linear-gradient(135deg, #0f172a, #1e293b);
        padding: 22px;
        border-radius: 18px;
        border: 1px solid #334155;
        box-shadow: 0px 4px 18px rgba(0,0,0,0.15);
    }}

    .metric-title {{
        color: #cbd5e1;
        font-size: 15px;
        font-weight: 600;
    }}

    .metric-value {{
        color: white;
        font-size: 30px;
        font-weight: 800;
        margin-top: 5px;
    }}

    .section-title {{
        color: {text_color};
        font-size: 24px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 10px;
    }}

    .info-box {{
        background-color: {card_bg};
        color: {text_color};
        padding: 18px;
        border-radius: 14px;
        border: 1px solid {border_color};
        font-size: 16px;
        box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
    }}

    .help-box {{
        background-color: {help_bg};
        color: {text_color};
        padding: 16px;
        border-radius: 12px;
        border: 1px solid {help_border};
        font-size: 15px;
        line-height: 1.6;
    }}

    .stButton > button {{
        width: 100%;
        border-radius: 10px;
        height: 45px;
        font-weight: 700;
        background-color: {input_bg};
        color: {input_text};
        border: 1px solid {border_color};
    }}

    .stButton > button:hover {{
        border: 1px solid #38bdf8;
        color: #38bdf8;
    }}

    div[data-baseweb="select"] > div {{
        background-color: {input_bg};
        color: {input_text};
        border-color: {border_color};
    }}

    div[data-baseweb="select"] * {{
        color: {input_text};
    }}

    div[data-baseweb="popover"] {{
        background-color: {input_bg};
    }}

    div[data-baseweb="popover"] * {{
        color: {input_text};
        background-color: {input_bg};
    }}

    input {{
        background-color: {input_bg} !important;
        color: {input_text} !important;
    }}

    div[data-testid="stExpander"] {{
        background-color: {card_bg};
        color: {text_color};
        border: 1px solid {border_color};
        border-radius: 12px;
    }}

    div[data-testid="stExpander"] * {{
        color: {text_color};
    }}

    div[data-testid="stAlert"] {{
        background-color: {help_bg};
        color: {text_color};
        border: 1px solid {help_border};
    }}

    div[data-testid="stAlert"] * {{
        color: {text_color};
    }}

    label {{
        color: {text_color} !important;
    }}

    .stMarkdown {{
        color: {text_color};
    }}
    </style>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# INITIALISATION SESSION
# ==========================================================

def initialiser_session():
    valeurs = {
        "running": False,
        "t": 0.0,
        "temps": [],
        "signal_bruite": [],
        "signal_filtre": [],
        "temps_calculs": [],
        "indices": [],
        "y_precedent": 0.0,
        "nb_echantillons": 0,
        "nb_depassements": 0,
    }

    for cle, valeur in valeurs.items():
        if cle not in st.session_state:
            st.session_state[cle] = valeur


initialiser_session()


# ==========================================================
# FONCTIONS
# ==========================================================

def reset_simulation():
    st.session_state.running = False
    st.session_state.t = 0.0
    st.session_state.temps = []
    st.session_state.signal_bruite = []
    st.session_state.signal_filtre = []
    st.session_state.temps_calculs = []
    st.session_state.indices = []
    st.session_state.y_precedent = 0.0
    st.session_state.nb_echantillons = 0
    st.session_state.nb_depassements = 0


def calculer_signal(t, type_signal, frequence, amplitude):
    if type_signal == "Sinus":
        return amplitude * np.sin(2 * np.pi * frequence * t)

    elif type_signal == "Carré":
        valeur = np.sin(2 * np.pi * frequence * t)
        if valeur >= 0:
            return amplitude
        else:
            return -amplitude

    elif type_signal == "Rampe":
        periode_signal = 1 / frequence
        return amplitude * (2 * ((t % periode_signal) / periode_signal) - 1)

    elif type_signal == "Bruit":
        return amplitude * np.random.randn()

    else:
        return amplitude * np.sin(2 * np.pi * frequence * t)


def filtrer_signal(x, rho):
    y = rho * st.session_state.y_precedent + (1 - rho) * x
    st.session_state.y_precedent = y
    return y


def calculer_fft(signal, points_par_seconde):
    if len(signal) < 8:
        return np.array([]), np.array([])

    x = np.array(signal)
    x = x - np.mean(x)

    N = len(x)

    X = np.fft.fft(x)
    X = np.fft.fftshift(X)

    freq = np.fft.fftfreq(N, d=1 / points_par_seconde)
    freq = np.fft.fftshift(freq)

    module = np.abs(X) / N
    module_log = 20 * np.log10(module + 1e-6)

    return freq, module_log


def ajouter_echantillon(
    type_signal,
    frequence,
    amplitude,
    sigma_bruit,
    rho,
    points_par_seconde,
    delta_t,
    bruit_active,
    filtrage_active
):
    debut = time.time()

    periode_echantillonnage = 1 / points_par_seconde
    t = st.session_state.t

    x = calculer_signal(t, type_signal, frequence, amplitude)

    if bruit_active:
        x_bruite = x + sigma_bruit * np.random.randn()
    else:
        x_bruite = x

    if filtrage_active:
        y = filtrer_signal(x_bruite, rho)
    else:
        y = x_bruite

    nb_points_max = int(delta_t * points_par_seconde)

    st.session_state.temps.append(t)
    st.session_state.signal_bruite.append(x_bruite)
    st.session_state.signal_filtre.append(y)

    st.session_state.temps = st.session_state.temps[-nb_points_max:]
    st.session_state.signal_bruite = st.session_state.signal_bruite[-nb_points_max:]
    st.session_state.signal_filtre = st.session_state.signal_filtre[-nb_points_max:]

    st.session_state.t += periode_echantillonnage
    st.session_state.nb_echantillons += 1

    temps_calcul = time.time() - debut

    st.session_state.indices.append(st.session_state.nb_echantillons)
    st.session_state.temps_calculs.append(temps_calcul)

    st.session_state.indices = st.session_state.indices[-200:]
    st.session_state.temps_calculs = st.session_state.temps_calculs[-200:]

    if temps_calcul > periode_echantillonnage:
        st.session_state.nb_depassements += 1

    return temps_calcul


def appliquer_theme_graphe(ax, theme):
    if theme == "Sombre":
        ax.set_facecolor("#020617")
        ax.figure.set_facecolor("#020617")
        ax.tick_params(colors="#f8fafc")
        ax.xaxis.label.set_color("#f8fafc")
        ax.yaxis.label.set_color("#f8fafc")
        ax.title.set_color("#f8fafc")
        ax.grid(True, color="#334155")

        for spine in ax.spines.values():
            spine.set_color("#475569")

    else:
        ax.set_facecolor("#ffffff")
        ax.figure.set_facecolor("#ffffff")
        ax.tick_params(colors="#0f172a")
        ax.xaxis.label.set_color("#0f172a")
        ax.yaxis.label.set_color("#0f172a")
        ax.title.set_color("#0f172a")
        ax.grid(True, color="#d1d5db")

        for spine in ax.spines.values():
            spine.set_color("#94a3b8")


def tracer_signal(ax, temps, valeurs, type_signal, titre):
    ax.set_title(titre, fontsize=14, fontweight="bold")
    ax.set_xlabel("Temps (s)")
    ax.set_ylabel("Amplitude")
    ax.set_ylim(-3, 3)
    ax.set_xlim(0, 1)

    if len(temps) == 0:
        return

    if type_signal == "Carré":
        ax.step(temps, valeurs, where="post", linewidth=2.2)
    else:
        ax.plot(temps, valeurs, linewidth=2.2)

    if len(temps) > 1:
        ax.set_xlim(temps[0], temps[-1])


# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:
    st.markdown("## ⚙️ Panneau de contrôle")
    st.markdown("---")

    type_signal = st.selectbox(
        "Type de signal",
        ["Sinus", "Carré", "Rampe", "Bruit"]
    )

    frequence = st.slider(
        "Fréquence du signal (Hz)",
        min_value=0.1,
        max_value=5.0,
        value=1.0,
        step=0.1
    )

    amplitude = st.slider(
        "Amplitude",
        min_value=0.5,
        max_value=3.0,
        value=1.0,
        step=0.1
    )

    sigma_bruit = st.slider(
        "Niveau du bruit σ",
        min_value=0.0,
        max_value=1.5,
        value=0.35,
        step=0.05
    )

    rho = st.slider(
        "Coefficient du filtre ρ",
        min_value=0.0,
        max_value=0.98,
        value=0.85,
        step=0.01
    )

    points_par_seconde = st.slider(
        "Points calculés par seconde",
        min_value=10,
        max_value=200,
        value=50,
        step=10
    )

    delta_t = st.slider(
        "Fenêtre d'analyse Δt (s)",
        min_value=3,
        max_value=15,
        value=8,
        step=1
    )

    st.markdown("---")
    st.markdown("### Modules actifs")

    bruit_active = st.checkbox("Bruit blanc gaussien", value=True)
    filtrage_active = st.checkbox("Filtrage passe-bas", value=True)
    fft_active = st.checkbox("Analyse FFT", value=True)
    surveillance_active = st.checkbox("Surveillance temps réel", value=True)

    st.markdown("---")

    col_b1, col_b2 = st.columns(2)

    with col_b1:
        if st.button("▶ Démarrer"):
            st.session_state.running = True

    with col_b2:
        if st.button("⏸ Pause"):
            st.session_state.running = False

    if st.button("↻ Réinitialiser"):
        reset_simulation()

    st.markdown("---")
    st.markdown("## ❓ Aide")

    with st.expander("Comprendre les boutons"):
        st.markdown(
            """
            <div class="help-box">
            <b>▶ Démarrer</b><br>
            Lance la simulation et commence l'affichage des signaux en temps réel.<br><br>

            <b>⏸ Pause</b><br>
            Met la simulation en pause sans supprimer les données affichées.<br><br>

            <b>↻ Réinitialiser</b><br>
            Efface les courbes, remet le temps à zéro et recommence une nouvelle simulation.<br><br>

            <b>Bruit blanc gaussien</b><br>
            Ajoute un bruit aléatoire au signal pour simuler une mesure perturbée.<br><br>

            <b>Filtrage passe-bas</b><br>
            Active un filtre qui réduit les variations rapides du signal bruité.<br><br>

            <b>Analyse FFT</b><br>
            Affiche le spectre fréquentiel du signal pour observer ses composantes en fréquence.<br><br>

            <b>Surveillance temps réel</b><br>
            Mesure le temps de calcul de chaque boucle et vérifie si la contrainte temps réel est respectée.
            </div>
            """,
            unsafe_allow_html=True
        )

    with st.expander("Conseil pour le signal carré"):
        st.markdown(
            """
            <div class="help-box">
            Pour obtenir un signal carré propre :<br><br>
            1. Choisir <b>Carré</b><br>
            2. Désactiver <b>Bruit blanc gaussien</b><br>
            3. Désactiver <b>Filtrage passe-bas</b><br>
            4. Cliquer sur <b>Réinitialiser</b><br>
            5. Cliquer sur <b>Démarrer</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.info("Projet TNS Python - Interface finale")


# ==========================================================
# TITRE PRINCIPAL
# ==========================================================

st.markdown(
    """
    <div class="header-box">
        <div class="main-title">📡 Simulation temps réel de signaux</div>
    </div>
    """,
    unsafe_allow_html=True
)


# ==========================================================
# SIMULATION
# ==========================================================

intervalle_rafraichissement = 0.5
periode_echantillonnage = 1 / points_par_seconde
points_par_rafraichissement = max(1, int(points_par_seconde * intervalle_rafraichissement))

if st.session_state.running:
    temps_total_calcul = 0.0

    for _ in range(points_par_rafraichissement):
        temps_total_calcul += ajouter_echantillon(
            type_signal,
            frequence,
            amplitude,
            sigma_bruit,
            rho,
            points_par_seconde,
            delta_t,
            bruit_active,
            filtrage_active
        )

    if temps_total_calcul > intervalle_rafraichissement:
        etat_temps_reel = "DÉPASSEMENT"
        st.session_state.nb_depassements += 1
    else:
        etat_temps_reel = "OK"
else:
    temps_total_calcul = 0.0
    etat_temps_reel = "PAUSE"


# ==========================================================
# CARTES MÉTRIQUES
# ==========================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
        <div class="card">
            <div class="metric-title">Signal</div>
            <div class="metric-value">{type_signal}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f"""
        <div class="card">
            <div class="metric-title">Fréquence signal</div>
            <div class="metric-value">{frequence:.1f} Hz</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f"""
        <div class="card">
            <div class="metric-title">Temps réel</div>
            <div class="metric-value">{etat_temps_reel}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        f"""
        <div class="card">
            <div class="metric-title">Dépassements</div>
            <div class="metric-value">{st.session_state.nb_depassements}</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# GRAPHES TEMPS RÉEL
# ==========================================================

st.markdown(
    '<div class="section-title">📊 Visualisation temps réel</div>',
    unsafe_allow_html=True
)

# Ligne 1 : signal d'entrée + FFT
graph_col1, graph_col2 = st.columns(2)

# -----------------------
# Haut gauche : Signal temporel bruité en entrée
# -----------------------
with graph_col1:
    fig1, ax1 = plt.subplots(figsize=(7, 4))

    tracer_signal(
        ax1,
        st.session_state.temps,
        st.session_state.signal_bruite,
        type_signal,
        "Signal temporel bruité en entrée"
    )

    appliquer_theme_graphe(ax1, theme)

    st.pyplot(fig1)
    plt.close(fig1)


# -----------------------
# Haut droite : Analyse FFT
# -----------------------
with graph_col2:
    fig2, ax2 = plt.subplots(figsize=(7, 4))

    if fft_active and len(st.session_state.signal_bruite) >= 8:
        freq, module_log = calculer_fft(st.session_state.signal_bruite, points_par_seconde)
        ax2.plot(freq, module_log, linewidth=2.2)

    ax2.set_title("Analyse fréquentielle par FFT centrée", fontsize=14, fontweight="bold")
    ax2.set_xlabel("Fréquence (Hz)")
    ax2.set_ylabel("Module logarithmique")
    ax2.set_xlim(-points_par_seconde / 2, points_par_seconde / 2)
    ax2.set_ylim(-80, 10)

    appliquer_theme_graphe(ax2, theme)

    st.pyplot(fig2)
    plt.close(fig2)


# Ligne 2 : signal de sortie + surveillance temps réel
graph_col3, graph_col4 = st.columns(2)

# -----------------------
# Bas gauche : Signal de sortie
# -----------------------
with graph_col3:
    fig3, ax3 = plt.subplots(figsize=(7, 4))

    ax3.set_title("Signal de sortie après filtrage passe-bas", fontsize=14, fontweight="bold")
    ax3.set_xlabel("Temps (s)")
    ax3.set_ylabel("Amplitude")
    ax3.set_ylim(-3, 3)
    ax3.set_xlim(0, 1)

    if len(st.session_state.temps) > 0:
        if type_signal == "Carré" and not filtrage_active:
            ax3.step(
                st.session_state.temps,
                st.session_state.signal_filtre,
                where="post",
                linewidth=2.2
            )
        else:
            ax3.plot(
                st.session_state.temps,
                st.session_state.signal_filtre,
                linewidth=2.2
            )

        if len(st.session_state.temps) > 1:
            ax3.set_xlim(st.session_state.temps[0], st.session_state.temps[-1])

    appliquer_theme_graphe(ax3, theme)

    st.pyplot(fig3)
    plt.close(fig3)


# -----------------------
# Bas droite : Surveillance temps réel
# -----------------------
with graph_col4:
    fig4, ax4 = plt.subplots(figsize=(7, 4))

    if surveillance_active and len(st.session_state.indices) > 0:
        ax4.plot(
            st.session_state.indices,
            st.session_state.temps_calculs,
            linewidth=2.2
        )
        ax4.axhline(
            periode_echantillonnage,
            linestyle="--",
            linewidth=2,
            label="Limite par point calculé"
        )
        ax4.legend()

    ax4.set_title("Surveillance du temps réel", fontsize=14, fontweight="bold")
    ax4.set_xlabel("Numéro de boucle")
    ax4.set_ylabel("Temps de calcul (s)")
    ax4.set_ylim(0, periode_echantillonnage * 2)

    appliquer_theme_graphe(ax4, theme)

    st.pyplot(fig4)
    plt.close(fig4)


# ==========================================================
# INFORMATIONS TECHNIQUES
# ==========================================================

st.markdown(
    '<div class="section-title">🧠 Informations techniques</div>',
    unsafe_allow_html=True
)

info_col1, info_col2 = st.columns(2)

with info_col1:
    st.markdown(
        f"""
        <div class="info-box">
        <b>Paramètres de simulation</b><br><br>
        Type de signal : {type_signal}<br>
        Fréquence du signal : {frequence:.2f} Hz<br>
        Amplitude : {amplitude}<br>
        Bruit σ : {sigma_bruit}<br>
        Coefficient du filtre ρ : {rho}<br>
        Fenêtre FFT Δt : {delta_t} s
        </div>
        """,
        unsafe_allow_html=True
    )

with info_col2:
    st.markdown(
        f"""
        <div class="info-box">
        <b>Mesures temps réel</b><br><br>
        Points calculés par seconde : {points_par_seconde}<br>
        Points calculés entre deux rafraîchissements : {points_par_rafraichissement}<br>
        Intervalle de rafraîchissement : {intervalle_rafraichissement:.1f} s<br>
        Période entre deux points : {periode_echantillonnage:.3f} s<br>
        Nombre d'échantillons : {st.session_state.nb_echantillons}<br>
        Nombre de dépassements : {st.session_state.nb_depassements}<br>
        État : {etat_temps_reel}
        </div>
        """,
        unsafe_allow_html=True
    )


# ==========================================================
# MESSAGE SIGNAL CARRÉ
# ==========================================================

if type_signal == "Carré":
    st.warning(
        "Pour visualiser un signal carré parfaitement net : désactive le bruit blanc et le filtrage, "
        "puis clique sur Réinitialiser avant de relancer."
    )


# ==========================================================
# RAFRAÎCHISSEMENT AUTOMATIQUE
# ==========================================================

if st.session_state.running:
    time.sleep(intervalle_rafraichissement)
    st.rerun()





import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import html
import json
import math
import hashlib
import tempfile
import uuid
import base64
import zlib
import unicodedata
from pathlib import Path
import streamlit.components.v1 as components

# ─────────────────────────────────────────────
# CONFIGURATION DE LA PAGE
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="Indicateur Socio-Économique",
    page_icon="📊",
    layout="wide"
)

# ─────────────────────────────────────────────
# STYLE
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

.main-title {
    font-size: 2rem;
    font-weight: 700;
    color: #12203f;
    margin-bottom: 0.15rem;
}
.subtitle {
    font-size: 1rem;
    color: #6b7280;
    margin-bottom: 1.5rem;
}

/* ── Bornes visuelles ── */
.bornes-wrap {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-top: 6px;
    flex-wrap: wrap;
}
.borne-group {
    display: flex;
    flex-direction: column;
    gap: 3px;
}
.borne-block {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    border-radius: 7px;
    padding: 4px 10px;
    font-size: 0.8rem;
}
.borne-p5-block {
    background: #f0f9ff;
    border: 1px solid #bae6fd;
}
.borne-p95-block {
    background: #fff7ed;
    border: 1px solid #fed7aa;
}
.borne-reel-block {
    background: #f8fafc;
    border: 1px dashed #cbd5e1;
    cursor: help;
}
.borne-label {
    font-weight: 700;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #64748b;
}
.borne-val {
    font-weight: 700;
    font-size: 0.88rem;
    color: #1e3a5f;
}
.borne-reel-label {
    font-weight: 600;
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: #94a3b8;
}
.borne-reel-val {
    font-size: 0.8rem;
    color: #94a3b8;
}
.borne-expl {
    font-size: 0.73rem;
    color: #64748b;
    font-style: italic;
    margin-top: 1px;
    max-width: 300px;
    line-height: 1.35;
}
.borne-arrow {
    color: #94a3b8;
    font-size: 0.85rem;
    margin-top: 6px;
}
.borne-sep {
    color: #cbd5e1;
    font-size: 0.85rem;
    margin: 0 2px;
    margin-top: 6px;
}

/* ── Alerte valeur extrême ── */
.alerte-extreme {
    background: #fef2f2;
    border: 1.5px solid #fca5a5;
    border-radius: 8px;
    padding: 7px 12px;
    font-size: 0.82rem;
    color: #b91c1c;
    font-weight: 600;
    margin-top: 5px;
    display: flex;
    align-items: center;
    gap: 6px;
}

.var-name {
    font-size: 0.97rem;
    font-weight: 600;
    color: #1e3a5f;
    margin-bottom: 4px;
}
.dim-desc {
    font-size: 0.88rem;
    color: #64748b;
    margin-bottom: 10px;
}
.source-tag {
    display: inline-block;
    font-size: 0.72rem;
    color: #475569;
    background: #f1f5f9;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 1px 7px;
    margin-top: 4px;
}

.score-card {
    background: linear-gradient(135deg, #1e3a5f 0%, #2563eb 100%);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    color: white;
}
.score-label {
    font-size: 0.9rem;
    font-weight: 600;
    opacity: 0.8;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
}
.score-value {
    font-size: 3.2rem;
    font-weight: 700;
    line-height: 1;
}
.score-sub {
    font-size: 0.85rem;
    opacity: 0.65;
    margin-top: 4px;
}

.dim-score-row {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 10px;
}
.dim-score-name {
    width: 160px;
    font-size: 0.82rem;
    font-weight: 600;
    color: #1e3a5f;
    flex-shrink: 0;
}
.dim-score-bar-wrap {
    flex: 1;
    background: #e2e8f0;
    border-radius: 999px;
    height: 10px;
    overflow: hidden;
}
.dim-score-bar {
    height: 10px;
    border-radius: 999px;
    background: linear-gradient(90deg, #2563eb, #38bdf8);
}
.dim-score-val {
    width: 48px;
    text-align: right;
    font-size: 0.82rem;
    font-weight: 700;
    color: #1e3a5f;
}

.step-pill {
    display: inline-block;
    background: #2563eb;
    color: white;
    border-radius: 999px;
    width: 26px;
    height: 26px;
    text-align: center;
    line-height: 26px;
    font-size: 0.82rem;
    font-weight: 700;
    margin-right: 8px;
}

.info-box {
    background: #eff6ff;
    border-left: 4px solid #2563eb;
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    font-size: 0.88rem;
    color: #1e3a5f;
    margin-bottom: 12px;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DONNÉES
# "min"/"max"       → bornes P5/P95 (normalisation)
# "min_reel"/"max_reel" → bornes réelles (limites de saisie)
# "commune_min"/"commune_max" → communes aux valeurs extrêmes réelles
# ─────────────────────────────────────────────

DIMENSIONS = {'Revenus et inégalités': {'emoji': '💶',
                           'description': 'Cette dimension mesure le niveau de vie, la pauvreté et les '
                                          'inégalités monétaires.',
                           'variables': {'Revenu médian': {'min': 20460,
                                                           'max': 34765,
                                                           'min_reel': 14790.0,
                                                           'max_reel': 48010.0,
                                                           'commune_min': 'Grigny (91286)',
                                                           'commune_max': 'Neuilly-sur-Seine (92051)',
                                                           'valeur': 25210,
                                                           'unite': '€',
                                                           'sens': 'positif',
                                                           'source': 'Filosofi 2021, communes '
                                                                     "d'Île-de-France",
                                                           'donnee_auto': 'revenu',
                                                           'fichier_donnees': 'normalisation_robuste_P5_P95_revenu_median_IDF_2021.xlsm',
                                                           'onglet_donnees': 'Données IDF',
                                                           'lien_donnees': 'https://drive.google.com/file/d/1zmKcQqAFHEERIhSgV1HDc7UY8u6E6h5J/view?usp=drivesdk',
                                                           'annee': 2021},
                                         'Taux de pauvreté au seuil de 60 % du revenu médian': {'min': 5,
                                                                                                'max': 29,
                                                                                                'min_reel': 5.0,
                                                                                                'max_reel': 44.0,
                                                                                                'commune_min': '28 '
                                                                                                               'communes, '
                                                                                                               'dont '
                                                                                                               'Bois-le-Roi '
                                                                                                               '(77037)',
                                                                                                'commune_max': 'Grigny '
                                                                                                               '(91286)',
                                                                                                'valeur': 18,
                                                                                                'unite': '%',
                                                                                                'sens': 'negatif',
                                                                                                'source': 'Filosofi '
                                                                                                          '2021, '
                                                                                                          'communes '
                                                                                                          "d'Île-de-France",
                                                                                                'donnee_auto': 'pauvrete',
                                                                                                'fichier_donnees': 'normalisation_robuste_P5_P95_taux_pauvrete_IDF_2021.xlsx',
                                                                                                'onglet_donnees': 'Données '
                                                                                                                  'IDF',
                                                                                                'lien_donnees': 'https://docs.google.com/spreadsheets/d/18mmoLE2msGBNWp2T65LVGSuklibKnq-X/edit?usp=drivesdk&ouid=102919110703194842413&rtpof=true&sd=true',
                                                                                                'annee': 2021},
                                         'Rapport interdécile du revenu disponible D9/D1': {'min': 2.5,
                                                                                            'max': 4.5,
                                                                                            'min_reel': 2.2,
                                                                                            'max_reel': 8.1,
                                                                                            'commune_min': 'Moncourt-Fromonville '
                                                                                                           '(77302)',
                                                                                            'commune_max': 'Neuilly-sur-Seine '
                                                                                                           '(92051)',
                                                                                            'valeur': 4.4,
                                                                                            'unite': '',
                                                                                            'sens': 'negatif',
                                                                                            'source': 'Filosofi '
                                                                                                      '2021, '
                                                                                                      'communes '
                                                                                                      "d'Île-de-France",
                                                                                            'donnee_auto': 'd9d1',
                                                                                            'fichier_donnees': 'normalisation_robuste_P5_P95_d9d1_IDF_2021.xlsx',
                                                                                            'onglet_donnees': 'Données '
                                                                                                              'IDF',
                                                                                            'lien_donnees': 'https://docs.google.com/spreadsheets/d/1TcxDbYEcXMY3PieWXaeMSJzoNMa2zmK9/edit?usp=drivesdk&ouid=102919110703194842413&rtpof=true&sd=true',
                                                                                            'annee': 2021}}},
 'Éducation': {'emoji': '🎓',
               'description': "Cette dimension mesure le niveau de formation, la scolarisation et l'accès "
                              'aux diplômes.',
               'variables': {'Part des diplômés du supérieur (15 ans+ non scolarisés)': {'min': 20.1,
                                                                                         'max': 61.0,
                                                                                         'min_reel': 9.40531511345291,
                                                                                         'max_reel': 74.19503388332967,
                                                                                         'commune_min': 'Mouy-sur-Seine '
                                                                                                        '(77325)',
                                                                                         'commune_max': 'Saint-Aubin '
                                                                                                        '(91538)',
                                                                                         'valeur': 35.0,
                                                                                         'unite': '%',
                                                                                         'sens': 'positif',
                                                                                         'source': 'INSEE, '
                                                                                                   'RP 2021, '
                                                                                                   'base '
                                                                                                   'communale '
                                                                                                   'Diplômes-Formation, '
                                                                                                   'Île-de-France',
                                                                                         'donnee_auto': 'diplomes',
                                                                                         'fichier_donnees': 'normalisation_diplomes_superieur_IDF_2021_corrigee_P5_P95(1).xlsx',
                                                                                         'onglet_donnees': 'Données '
                                                                                                           'IDF',
                                                                                         'lien_donnees': 'https://docs.google.com/spreadsheets/d/18LIU1I8CcPBqXmLLXrQTNhjP26NJ-aXQ/edit?usp=drivesdk&ouid=102919110703194842413&rtpof=true&sd=true',
                                                                                         'annee': 2021},
                             'Part des actifs peu ou pas diplômés parmi les actifs': {'min': 6.2,
                                                                                      'max': 22.8,
                                                                                      'min_reel': 0.9679418279984711,
                                                                                      'max_reel': 46.99616329073984,
                                                                                      'commune_min': 'Milon-la-Chapelle '
                                                                                                     '(78406)',
                                                                                      'commune_max': 'Hautefeuille '
                                                                                                     '(77224)',
                                                                                      'valeur': 20.0,
                                                                                      'unite': '%',
                                                                                      'sens': 'negatif',
                                                                                      'source': 'INSEE, RP '
                                                                                                '2021, base '
                                                                                                'communale '
                                                                                                'Emploi-Population '
                                                                                                'active, '
                                                                                                'Île-de-France',
                                                                                      'donnee_auto': 'peu_diplomes',
                                                                                      'fichier_donnees': 'normalisation_actifs_peu_pas_diplomes_IDF_2021_corrigee.xlsx',
                                                                                      'onglet_donnees': 'Données '
                                                                                                        'IDF',
                                                                                      'lien_donnees': 'https://docs.google.com/spreadsheets/d/1Z0kCfz68KlWRA23uAo4NwS89b7qaUWOU/edit?usp=drivesdk&ouid=102919110703194842413&rtpof=true&sd=true',
                                                                                      'annee': 2021}}},
 'Emploi': {'emoji': '💼',
            'description': "Cette dimension mesure l'accès à l'emploi, le chômage et la stabilité "
                           'professionnelle.',
            'variables': {'Taux de chômage au sens du recensement des 15-64 ans': {'min': 4.8812,
                                                                                   'max': 15.2901,
                                                                                   'min_reel': 0.0,
                                                                                   'max_reel': 22.997057517503197,
                                                                                   'commune_min': '2 '
                                                                                                  'communes, '
                                                                                                  'dont '
                                                                                                  'Montenils '
                                                                                                  '(77304)',
                                                                                   'commune_max': 'La '
                                                                                                  'Courneuve '
                                                                                                  '(93027)',
                                                                                   'valeur': 12.0,
                                                                                   'unite': '%',
                                                                                   'sens': 'negatif',
                                                                                   'source': 'INSEE, RP '
                                                                                             '2021, base '
                                                                                             'communale '
                                                                                             'Emploi-Population '
                                                                                             'active, '
                                                                                             'Île-de-France',
                                                                                   'donnee_auto': 'chomage',
                                                                                   'fichier_donnees': 'normalisation_taux_chomage_IDF_2021_corrigee_P5_P95.xlsx',
                                                                                   'onglet_donnees': 'Données '
                                                                                                     'IDF',
                                                                                   'lien_donnees': 'https://docs.google.com/spreadsheets/d/1CK3w6b0g5aYAgjPrkHGdyDrLFaPOUamz/edit?usp=drivesdk&ouid=102919110703194842413&rtpof=true&sd=true',
                                                                                   'annee': 2021},
                          'Part des salariés en emploi non stable parmi les salariés': {'min': 6.64,
                                                                                        'max': 16.69,
                                                                                        'min_reel': 0.0,
                                                                                        'max_reel': 28.36791982656786,
                                                                                        'commune_min': '3 '
                                                                                                       'communes, '
                                                                                                       'dont '
                                                                                                       'Boisdon '
                                                                                                       '(77036)',
                                                                                        'commune_max': 'Nanteau-sur-Lunain '
                                                                                                       '(77329)',
                                                                                        'valeur': 12.0,
                                                                                        'unite': '%',
                                                                                        'sens': 'negatif',
                                                                                        'source': 'INSEE, RP '
                                                                                                  '2021, '
                                                                                                  'base '
                                                                                                  'communale '
                                                                                                  'Caractéristiques '
                                                                                                  'de '
                                                                                                  "l'emploi, "
                                                                                                  'Île-de-France',
                                                                                        'donnee_auto': 'non_stable',
                                                                                        'fichier_donnees': 'normalisation_robuste_P5_P95_emploi_non_stable_IDF_2021.xlsx',
                                                                                        'onglet_donnees': 'Données '
                                                                                                          'IDF',
                                                                                        'lien_donnees': 'https://docs.google.com/spreadsheets/d/12-OO_NPBG3b5R7S8lzedtKfqdTCgas-h/edit?usp=drivesdk&ouid=102919110703194842413&rtpof=true&sd=true',
                                                                                        'annee': 2021},
                          "Taux d'activité": {'min': 71.1,
                                              'max': 83.52,
                                              'min_reel': 42.47771437221764,
                                              'max_reel': 88.83663021005927,
                                              'commune_min': 'Fleury-Mérogis (91235)',
                                              'commune_max': 'Dhuisy (77157)',
                                              'valeur': 76.0,
                                              'unite': '%',
                                              'sens': 'positif',
                                              'source': 'INSEE, RP 2021, base communale Emploi-Population '
                                                        'active, Île-de-France',
                                              'donnee_auto': 'activite',
                                              'fichier_donnees': 'taux_activite_1564_bornes_IDF_2021.xlsx',
                                              'onglet_donnees': 'Communes_IDF',
                                              'lien_donnees': 'https://docs.google.com/spreadsheets/d/1rY6E88cuwn0Emwi3QLO1SC46pxL-T_wE/edit?usp=drivesdk&ouid=102919110703194842413&rtpof=true&sd=true',
                                              'annee': 2021}}},
 'Santé': {'emoji': '🏥',
           'description': "Cette dimension mesure l'accès potentiel aux soins de médecine générale.",
           'variables': {'Accessibilité potentielle localisée aux médecins généralistes': {'min': 1.3422,
                                                                                           'max': 3.8351,
                                                                                           'min_reel': 0.627,
                                                                                           'max_reel': 5.6,
                                                                                           'commune_min': 'Moisson '
                                                                                                          '(78410)',
                                                                                           'commune_max': "Bois-d'Arcy "
                                                                                                          '(78073)',
                                                                                           'valeur': 2.5,
                                                                                           'unite': 'consult./an/hab. '
                                                                                                    'std.',
                                                                                           'sens': 'positif',
                                                                                           'source': 'DREES, '
                                                                                                     'APL '
                                                                                                     'médecins '
                                                                                                     'généralistes '
                                                                                                     '2021, '
                                                                                                     'Méthode '
                                                                                                     'concertée '
                                                                                                     'V2 '
                                                                                                     '2015-2022 '
                                                                                                     '; '
                                                                                                     'Paris '
                                                                                                     'agrégé '
                                                                                                     'en '
                                                                                                     'commune '
                                                                                                     '75056 '
                                                                                                     'par '
                                                                                                     'population '
                                                                                                     'standardisée '
                                                                                                     '2019',
                                                                                           'donnee_auto': 'apl',
                                                                                           'fichier_donnees': 'recap_APL_sante_2021_paris_agrege.xlsx',
                                                                                           'onglet_donnees': 'Donnees_IDF_communes',
                                                                                           'lien_donnees': 'https://docs.google.com/spreadsheets/d/1GXOj1El6wr3hFZT0GID_OyOs8UlaIizz/edit?usp=drivesdk&ouid=102919110703194842413&rtpof=true&sd=true',
                                                                                           'annee': 2021}}},
 'Logement': {'emoji': '🏠',
              'description': 'Cette dimension mesure les conditions de logement à travers la suroccupation '
                             'des résidences principales.',
              'variables': {'Part des résidences principales suroccupées': {'min': 0.0,
                                                                            'max': 15.85663959361628,
                                                                            'min_reel': 0.0,
                                                                            'max_reel': 33.73270625531563,
                                                                            'commune_min': '290 communes, '
                                                                                           'dont Amponville '
                                                                                           '(77003)',
                                                                            'commune_max': 'Aubervilliers '
                                                                                           '(93001)',
                                                                            'valeur': 3.4,
                                                                            'unite': '%',
                                                                            'sens': 'negatif',
                                                                            'source': 'INSEE, RP 2021, base '
                                                                                      'communale Logement, '
                                                                                      'Île-de-France ; '
                                                                                      'résidences '
                                                                                      'principales hors '
                                                                                      'studios occupés par '
                                                                                      'une personne',
                                                                            'donnee_auto': 'suroccupation',
                                                                            'fichier_donnees': 'normalisation_robuste_P5_P95_residences_principales_suroccupees_IDF_2021_corrigee.xlsx',
                                                                            'onglet_donnees': 'Données_IDF_2021',
                                                                            'lien_donnees': 'https://docs.google.com/spreadsheets/d/1gaKu15K5QyOtxUd8mLXRus2Oa4EY2MzH/edit?usp=drivesdk&ouid=102919110703194842413&rtpof=true&sd=true',
                                                                            'annee': 2021}}},
 'Vulnérabilité sociale': {'emoji': '🤝',
                           'description': 'Cette dimension mesure certaines situations d’isolement et de '
                                          'vulnérabilité relationnelle.',
                           'variables': {'Part des personnes de 65 ans ou plus vivant seules': {'min': 15.78,
                                                                                                'max': 38.5,
                                                                                                'min_reel': 0.0,
                                                                                                'max_reel': 100.0,
                                                                                                'commune_min': '3 '
                                                                                                               'communes, '
                                                                                                               'dont '
                                                                                                               'Chatignonville '
                                                                                                               '(91145)',
                                                                                                'commune_max': '2 '
                                                                                                               'communes, '
                                                                                                               'dont '
                                                                                                               'Montenils '
                                                                                                               '(77304)',
                                                                                                'valeur': 26.24,
                                                                                                'unite': '%',
                                                                                                'sens': 'negatif',
                                                                                                'source': 'INSEE, '
                                                                                                          'RP '
                                                                                                          '2021, '
                                                                                                          'base '
                                                                                                          'communale '
                                                                                                          'Couples-Familles-Ménages, '
                                                                                                          'Île-de-France '
                                                                                                          '; '
                                                                                                          'formule '
                                                                                                          ': '
                                                                                                          '(P21_POP6579_PSEUL '
                                                                                                          '+ '
                                                                                                          'P21_POP80P_PSEUL) '
                                                                                                          '/ '
                                                                                                          '(P21_POP6579 '
                                                                                                          '+ '
                                                                                                          'P21_POP80P) '
                                                                                                          '× '
                                                                                                          '100',
                                                                                                'donnee_auto': 'isolement',
                                                                                                'fichier_donnees': 'normalisation_robuste_P5_P95_vulnerabilite_sociale_IDF_2021.xlsx',
                                                                                                'onglet_donnees': 'Donnees_IDF_2021',
                                                                                                'lien_donnees': 'https://docs.google.com/spreadsheets/d/1Q0G2KauKLhcJnRqwWXMvxssK9Aj9bGp7/edit?usp=drivesdk&ouid=102919110703194842413&rtpof=true&sd=true',
                                                                                                'annee': 2021},
                                         'Part des familles monoparentales parmi les familles': {'min': 3.19,
                                                                                                 'max': 25.64,
                                                                                                 'min_reel': 0.0,
                                                                                                 'max_reel': 100.0,
                                                                                                 'commune_min': '53 '
                                                                                                                'communes, '
                                                                                                                'dont '
                                                                                                                'Amponville '
                                                                                                                '(77003)',
                                                                                                 'commune_max': 'Charmont '
                                                                                                                '(95141)',
                                                                                                 'valeur': 14.28,
                                                                                                 'unite': '%',
                                                                                                 'sens': 'negatif',
                                                                                                 'source': 'INSEE, '
                                                                                                           'RP '
                                                                                                           '2021, '
                                                                                                           'base '
                                                                                                           'communale '
                                                                                                           'Couples-Familles-Ménages, '
                                                                                                           'Île-de-France '
                                                                                                           '; '
                                                                                                           'formule '
                                                                                                           ': '
                                                                                                           'C21_FAMMONO '
                                                                                                           '/ '
                                                                                                           'C21_FAM '
                                                                                                           '× '
                                                                                                           '100',
                                                                                                 'donnee_auto': 'monoparentalite',
                                                                                                 'fichier_donnees': 'normalisation_robuste_P5_P95_vulnerabilite_sociale_IDF_2021.xlsx',
                                                                                                 'onglet_donnees': 'Donnees_IDF_2021',
                                                                                                 'lien_donnees': 'https://docs.google.com/spreadsheets/d/1Q0G2KauKLhcJnRqwWXMvxssK9Aj9bGp7/edit?usp=drivesdk&ouid=102919110703194842413&rtpof=true&sd=true',
                                                                                                 'annee': 2021}}},
 'Environnement': {'emoji': '🌿',
                   'description': 'Cette dimension mesure la qualité du cadre de vie environnemental.',
                   'variables': {'Espaces verts': {'min': 0,
                                                   'max': 80,
                                                   'min_reel': 0,
                                                   'max_reel': 80,
                                                   'commune_min': 'À documenter',
                                                   'commune_max': 'À documenter',
                                                   'valeur': 25,
                                                   'unite': '%',
                                                   'sens': 'positif',
                                                   'source': 'Borne indicative à discuter'},
                                 "Pollution de l'air": {'min': 5,
                                                        'max': 40,
                                                        'min_reel': 5,
                                                        'max_reel': 40,
                                                        'commune_min': 'À documenter',
                                                        'commune_max': 'À documenter',
                                                        'valeur': 20,
                                                        'unite': 'µg/m³',
                                                        'sens': 'negatif',
                                                        'source': 'Borne indicative à discuter'},
                                 'Densité de population': {'min': 50,
                                                           'max': 25000,
                                                           'min_reel': 50,
                                                           'max_reel': 25000,
                                                           'commune_min': 'À documenter',
                                                           'commune_max': 'À documenter',
                                                           'valeur': 5000,
                                                           'unite': 'hab/km²',
                                                           'sens': 'negatif',
                                                           'source': 'Borne indicative à discuter'}}}}

# ─────────────────────────────────────────────
# UTILITAIRES
# ─────────────────────────────────────────────

def fmt_val(v):
    """Formate un nombre : supprime les .0 inutiles, garde les décimales significatives."""
    if isinstance(v, float) and v == int(v):
        return str(int(v))
    if isinstance(v, float):
        # Supprime les zéros de fin après la virgule
        s = f"{v:.4f}".rstrip("0").rstrip(".")
        return s
    return str(v)


def attr_html(v):
    """Protège un texte avant de l'utiliser dans un attribut HTML title."""
    return html.escape(str(v), quote=True)


# ─────────────────────────────────────────────
# FONCTIONS
# ─────────────────────────────────────────────

def normaliser(valeur, vmin, vmax, sens="positif"):
    """Normalise sur [0,1] via les bornes P5/P95 ; plafonne à 0 ou 1 si hors bornes."""
    if vmax == vmin:
        return 0.0
    score = (valeur - vmin) / (vmax - vmin)
    if sens == "negatif":
        score = 1 - score
    return float(np.clip(score, 0, 1))


def moyenne_ponderee(scores, poids):
    scores = np.array(scores, dtype=float)
    poids = np.array(poids, dtype=float)
    if len(scores) == 0 or poids.sum() == 0:
        return 0.0
    return float(np.average(scores, weights=poids))


def calculer_indicateur(dimensions_choisies, variables_choisies, valeurs, poids_variables, poids_dimensions):
    resultats_variables = []
    scores_dimensions = {}

    for nom_dimension in dimensions_choisies:
        variables_dimension = variables_choisies.get(nom_dimension, [])
        if len(variables_dimension) == 0:
            continue

        scores_var_dim = []
        poids_var_dim = []

        for nom_variable in variables_dimension:
            infos = DIMENSIONS[nom_dimension]["variables"][nom_variable]
            valeur = valeurs[nom_variable]
            poids = poids_variables[nom_variable]

            score = normaliser(
                valeur=valeur,
                vmin=infos["min"],
                vmax=infos["max"],
                sens=infos.get("sens", "positif")
            )

            scores_var_dim.append(score)
            poids_var_dim.append(poids)

            hors_bornes = valeur < infos["min"] or valeur > infos["max"]

            resultats_variables.append({
                "Dimension": nom_dimension,
                "Variable": nom_variable,
                "Valeur saisie": valeur,
                "Unité": infos.get("unite", ""),
                "P5": infos["min"],
                "P95": infos["max"],
                "Sens": infos.get("sens", "positif"),
                "Hors bornes P5-P95": "⚠️ Oui" if hors_bornes else "Non",
                "Poids variable": poids,
                "Score normalisé 0-100": round(score * 100, 1),
                "Source": infos.get("source", "")
            })

        score_dimension = moyenne_ponderee(scores_var_dim, poids_var_dim)
        scores_dimensions[nom_dimension] = score_dimension

    if len(scores_dimensions) == 0:
        return resultats_variables, scores_dimensions, 0.0

    indicateur_global = moyenne_ponderee(
        list(scores_dimensions.values()),
        [poids_dimensions[dim] for dim in scores_dimensions.keys()]
    )

    return resultats_variables, scores_dimensions, indicateur_global


def creer_radar(scores_dimensions):
    dimensions = list(scores_dimensions.keys())
    scores = [scores_dimensions[dim] * 100 for dim in dimensions]

    if len(dimensions) == 0:
        return go.Figure()

    dimensions_fermees = dimensions + [dimensions[0]]
    scores_fermes = scores + [scores[0]]

    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=scores_fermes,
        theta=dimensions_fermees,
        fill="toself",
        name="Score des dimensions",
        fillcolor="rgba(37, 99, 235, 0.15)",
        line=dict(color="#2563eb", width=3)
    ))

    fig.update_layout(
        height=400,
        margin=dict(l=60, r=60, t=60, b=60),
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], tickfont=dict(size=11)),
            angularaxis=dict(tickfont=dict(size=12))
        ),
        showlegend=False,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    return fig


def tableau_variables():
    """Tableau synthétique : P5/P95 + min/max réels avec communes."""
    lignes = []
    for nom_dimension, contenu in DIMENSIONS.items():
        for nom_variable, infos in contenu["variables"].items():
            has_reel = infos.get("min_reel") != infos.get("min") or infos.get("max_reel") != infos.get("max")
            commune_min = infos.get("commune_min", "")
            commune_max = infos.get("commune_max", "")
            lignes.append({
                "Dimension": nom_dimension,
                "Variable": nom_variable,
                "P5 (normalisation)": infos["min"],
                "P95 (normalisation)": infos["max"],
                "Min réel": infos.get("min_reel", infos["min"]) if has_reel else "—",
                "Commune min réel": commune_min if (has_reel and commune_min and commune_min != "À documenter") else "—",
                "Max réel": infos.get("max_reel", infos["max"]) if has_reel else "—",
                "Commune max réel": commune_max if (has_reel and commune_max and commune_max != "À documenter") else "—",
                "Unité": infos.get("unite", ""),
                "Sens": "✅ positif" if infos.get("sens") == "positif" else "🔻 négatif",
                "Source": infos.get("source", "")
            })
    return pd.DataFrame(lignes)


def explication_borne(nom_variable, p5, p95, unite, min_reel, max_reel, commune_min, commune_max):
    """Génère une explication pédagogique dynamique des bornes P5/P95."""
    u = f" {unite}" if unite else ""
    p5_fmt = fmt_val(p5)
    p95_fmt = fmt_val(p95)

    texte_p5 = f"Environ 5 % des communes d'Île-de-France ont une valeur inférieure ou égale à {p5_fmt}{u} pour cette variable."
    texte_p95 = f"Environ 5 % des communes d'Île-de-France ont une valeur supérieure ou égale à {p95_fmt}{u} pour cette variable."

    has_reel = (min_reel != p5 or max_reel != p95)
    if has_reel:
        min_reel_fmt = fmt_val(min_reel)
        max_reel_fmt = fmt_val(max_reel)
        cm = f" ({commune_min})" if commune_min and commune_min != "À documenter" else ""
        cM = f" ({commune_max})" if commune_max and commune_max != "À documenter" else ""
        texte_reel = (
            f"Valeurs extrêmes observées : {min_reel_fmt}{u}{cm} → {max_reel_fmt}{u}{cM}. "
        )
    else:
        texte_reel = ""

    return texte_p5, texte_p95, texte_reel


# Données communales intégrées : aucun fichier de données ni accès à Drive
# n'est nécessaire lors de l'utilisation du logiciel.
_DONNEES_EMBARQUEES = (
    'eNqsvctuZFl2pvkqQkx6Imfv+0UzZaqUUiGzJEgFAT0qMCOoCDY8yBDdGajIQj2Axv0GmrSi+iF64Oj36v9b5mZ29j770N0AeUS6'
    'Ukmn02zZPmuvy3/5H998+PaHhx/vv/kL/+ff/PJw//LNXwQX9N+/f3j+/uX+px9++eYvvvmHv/8z+x//7PtPv57+18eHP/v2+ccf'
    'X5/u3z/82f3rnzn/v+tf/aH0zZ9/c/rKw4dv/uJ/fFOzy4X/8nT/44P+qr+/f3n8oD/z8/3719OfeHn4+eHpVT+21+ju3J9/89P9'
    '688vDx/1p33h//+uf+e/+Ytyl/RfH396//wj31fSXcklp56iCy3XrO97eP1v1z/Q7ppLfDnnkIqPVa/rh+cf77/n73V3NVWvb0+9'
    'pdizvvj0/PTfPny8/+P708/N2XlXWkgtVf7y+28/Pv78yIuq7S5Un3x13ufTX3z/0/tv/iLd5ZR7zK6XUHzrerkfXl+ev/329af7'
    'j4/PT/pr4133LYaWnK9e77f9+TePH57fP/z48PRRf0G8C9mF3AL/x+WuH/vj89PzT/cv+vr9e/vpvt/V7nOIIZRQ0//8n3/+Ta3O'
    '+U2I//LbHz79+8vDh3fv79/99fPLp//1cRnv6Hqd4v30+v79Od6f//slnqnehdhLLb10H2Js+4DXUnUAatErj3qjm4CXu+5i6l4v'
    'tOjF87VtvPVZ1dBjIpy59pSGePc7p4/Y11yafnSKn+Pt7yyAU4zjnc+ullj1CZTgkstDjEO8K97Fop+Rq2KY4yrGTmcn5q4Xox/p'
    '4jnIYRvkHx/fvz86ySX6GyKr16SHJLgYvXep9DmwPt8VYhf1cnrUueibyLa7pCMea8tFx7WlObDBxxhT1XHNvpQ2BLbcRZ9C1fn3'
    'js/nc2DjnU7GLrBBgYvBuaQfFYI+hzIEVuey6XPPrhT9kdDKKq76m2N0RR9mq7Xr4ztHNg6R/en56WdF92EdXD09NwQ3xrvovB6W'
    'VEpRFOoiuinqefX6FSJHb5smvFNuSS3HSBLJY3SLvlyL8kPpodUc6ja6Ld/p7Oir+jMKW+6XY5sX0bV3tD2nSUew6kEppTelk5AW'
    '8dQ3nQOYtgF8+u7l4U8P7/8jwhf0VDd9YMnnViNR2MUv3dWaup6Uqkzvt/GrSlWKTtPBrD3oyR/D1+/0GDo92EUHu9qx3oRP+b6V'
    'pnzSeigtt0v4Cn/wS+Fzdz0rixbdKbUlHe71Y64rpBRlet0DTof+HM08RPPp4eM7/bx3f7h/eTo4k92VN4Ia7vpwJPud0r9rCmjn'
    'cdldXZw7XRE5KsUHV3yPQyr1sejzaDkrzdQU5qDmFnXwlNm6HrM+X10lKc0k3Vr60NL5iQ96BPZBTXdBZ68qi+qqjJGPbxti3ZH6'
    'gq6z6EuNaRlhTgAvo+nJ0tkolwd+WxL85csfnxXkL11X3uVbris+XHKf6hY9wTntDq6OX+6px64nV49pqkOQm65xblmdwFxDnB98'
    'hVdJrvIZ9RbjlFYJmb7N5Zh1vK8Pfv26k1td1Yeopz+RKdcnlwokBN23uqeaL+e41iGu3+tbHq0WOMgFvt+SSvXSgle4dJM43Z6L'
    'gxvuPFUVl00m3W6zQbzTKVEm5bZRtiyxzCdXJZGShKLdqKTKkA50JetY6wLKyhiF6+VzUBvF6peCGlS7NL3gpI/c6TNZxVRPKamo'
    'eFV21dd2yQZtiOmPl5i+e3h695uXx4OU4JTbbsiz+U6lY9cTz92oS6fsYtv0+pKeJCWFphszlO1NVe90+ZfcUs7R6x6eYqsD05vz'
    '0Qed9dr8eGJLu1M9F5QTyBjBXSss3fSLCosPT9eiyhW9VsutY15QPkhcujotevzqItj9TmWEPmg9ITrGKsHPse5DrN+oAvKbGXdx'
    'dFWX6rSfftc377NBDZtf24yb1QxsfpUp4yr2UWWAyteuZK6gDCm3BYVLN6juQCWU7K9lgCqOLx/crNp38yusDq6/89tf4XMsvdvG'
    '8vWPDz89Pry8PLz7uz89vz68vHv/8O4fHn56PqpgdWvfcHr1eebagtoD1e96QhdFgp55nV5V3rrOXSrTjabLKuqj0UUfkp9rWKe0'
    'odJYRWpPRH9IC/rYlIPVPui33i4XWuD52JWwKjlz0o1QVe/m3uYkwcOuK7eoFNDxPki8pesPqY/Rp5ry+eD6oQF7/ed/fnjz8OZb'
    'Oq9QlRt0D6npijpgVAO7tKt7Wi9ZybnreNc4FGFqE9UKNWJIYzZGl+ot6qOhZ6HrLFO9oO9y1HdUYVZMfO4Q8iq86rca51yFdNHd'
    'NYa33qmVJrSOjiWtjrJqvlBV8fFJ65Fq+RzdofN6/f7h5QvJVy/6lgCHO50/tWBNaYWbdxdg1TEp0vKr81GghlpByVMhVFrwNJVh'
    'l3p5PFVzN0901PjPFVnXPakbsfMZ1XNFpusuty+mB6W12hVKXZZJiSf1N5sEP3RZr++fnn85qmbDjR2WPjPVsjXpuWh1cTx5RqNu'
    'haInuZPFhuSqBicQH3LD3GPp6WdQ0nxWqaleIE6jAX0e+sQUPl2JlhtOj3+PX06u1lcnqgp9OpGbcxE+9T9Ozbd6PN2PevDPsRwa'
    'rp/11y8jmfx8S+mHXkZaukmHklXHUK8iqOXTvypNV72WXglJUKknN8tg1xpAxVfUg6zvV/UZ9OBOB5EcrAOoZlSFpYtUQZtQVjuI'
    'KitcqSrr2+VRr4vWQD2zcrkSQ8vK5VaObQdZXidCF4ESpBoQt6pgeeRiUMpqemh0NcRLYLe912/u/3hwRMNuVvjmEVWDow6THt5+'
    '94shQGw0+Off8zawqoO2X01p8YTrVyRyynHj9CoyNkuxqO5QWMO1cA38kHlCON3lYwZt6iDoCU6/p+V4UM3H8OvccfkyxPX7p4f7'
    '1/9ube3vnx+fvl9H2cdbalgdQDX00dpt9axK4nOYVc7EkukCdCNl3cF1qmF709lTh9p6K9OMkI8oVZ1PPYXdRhLT8WXIorq5KBe1'
    'Wi6ZoKS+KGHVoHW1BHoVkdosjGlVrWGslIkpqVupZX2APSNkFXc+eL2cc5zbEGfVAL+8+we9w0cbaakCOyq4+tyK9W2i8NMoVsW1'
    '67rzvSIe4mKAoGjoCdfJU6xjHuoBxb6qbddRVT1Q865T0FeqU63RSNa1T/WWTqXStN612ozLLDYoi+87hUIYk7JVYzCYGTBuo6xM'
    '6PWJqUNW3FRgrKKsmCRVPFGtj3JWv5RbfYjy+/dHV1ms/rZKS1FR+lSVr4e1LCLrlSY7wyq9qab2Po7zQpWWRKboSlaCTLu1QlPy'
    '8ZQ3+u6W4lQKeKbcuTIyc9dEEX35mkog+5CYN+gkNevbdtFUrVd0X3bFMzEaP5/Z4IZoPj09f/j47p8oX79Xoji628pNySHo9sl6'
    'TlSfKoOqWE2LHEwJoDSqirPTqo6hpXuq9JtNkfO7QTflInkh6MHuqU49mDpj5cLOtMYGBuf+toXF2MvGWnq1WRV3YDc0BjpRkBY9'
    'Hyp5WlgVDVUXhmeRk/RZBNW050D7IdAvf3w4OLblpu5WsdVL0advv9nMbwytnnkVZ5d/t3GNioG+i7jzX3Yj2qh2zukZVJXlWptS'
    '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'
    'ltRIhwgoRnqCRMQ2xfMLORruH1dyqOzKG5YWskWM6Cu04V/q5CUHqR00D1qBYNtAuUj1LO/OKgtrh+GbLDcng1UvcDc7DnhXQtCB'
    'R1UJji4tSJDJykK5oXlgST9K3dmArFu1UuRc0MVbjN9QS5HaKDufWdfT2jbe7y8g85zQIcrbNi7fbF5i8lrjSLMTcSpNx+xUoO+s'
    '7Y0C8g5DUlazDT3eBFIcJjUymjF+t4IzFN7yMqNZ7qDPXcQ6E9c3ZwXyVjCEBq3MmBjF+45NTRFUFmodOQsQHllixp76v7K8zakg'
    '/8DHk80bB3TB6eaVHVYySiXsK9lNujvFHv7t2rZkNcd/29FRj2ZVbiMFJJm+sa4frLzRwaaEw7gtj1eb/krtKYsJWyo6kizr9CSQ'
    'v2dfwGOb4Yu775c+C75op47Y0HkA5DtAackwxU7kplaTXDx0WS12eqC1HFBwHTzcQzu+ggsKu8yljU6ttxKSG87r2RNSaw9kzzLr'
    'mqNQykBOav9Os5VoMNj76k02ZhGFCp8xMcEjdumpMIit7/iLB6RkyxwSMoRP4OwTYDjRHPLGj1m2yOhjUca2vtsjCUA+dGxlIHYE'
    'xT2lEvdGTVLyEiFjIIX6V3CK0aDOZYienk/WYmcpJHhYM1Yx4+NI3bGR5Gsandao/WI6C5ZXB3g/Hylo97Wtzdre3T+enKtytZza'
    '5VMfkYzqI6rxLChQd2SmAvtKys8prnNoVuJHiNXwnFjj4kLHezKbyf6MPZRAOe8cDrLt/OXecm6aAQUZAReW4yweglCpyRH+Z8w2'
    '04gtbmAAOFIakgQll9zTArsWvfNwf8JWBvL6losrvedFIA8d+XbPQhs4PjVlTNt/udWiM1qAZk9kBg+dNGFXs3gwD4ltyt3IJzis'
    'b6T4yIvwssBhYpjvj1aatQr4VQytn+ZggIWGOUPvR/fPvp7NQfvw6cebpSR6aJa/UAUw/OXnkU85jG5BqVBpDRjDA0d+8q7Egj3i'
    'A4yeWsbxr9rL5LtpgXSFtgiIKpu0Uifo6VkvJ0GNLy8leFV9Tys1LizinYJjpo+TnmrleS2P7cUvPt4dOAN/WoptypCT3urGQmeX'
    'eHIOeIjCZnb7Q5SW6ycT26ERSoctStJptGAbYA2M1xdKVDwrRt91vWaBqg0ctkvGx0ueofqP+r7M+6AAcvkIsMSZTgzi+D2YPjn5'
    'aWqeInV4G5PyxHlUacg9L3Nzf336dM5XLwNb8mzbAq7Cfx8VauzD7NHlmLpbHIRk6BzWN+jxIN8tgCryNSzDERDxJxBQL0VUHIR5'
    'nq9/qoo7ubjXYp4tL5iMrFAlvJ9DhLfn/eSLvFPIqpsOz7ARAicHQy6PIL8vbxMX+cXjz3vX62QLDy7i9RQiqGWH4xXjCIOymXcN'
    'wV2hFwdhrlUzkXpq6UGhNRrSvO17BfrhjuPxHPs5BNwFD+aMY/Ig3a1hIit1amwpzKrlrrf9Dq7IeiqtSoqwuHgfyKUKWdKi9Nyr'
    'hHBsen0hK7xseRnzlkM3MDuR88FHxfbGUXSDGlEOCCS7PnY4KDmGGc5oCZZ7I0qlKAKIaMjnLF31BQxcTly+MM5UcxlParDN+PAi'
    'gIdCGnKV79XmmN8MAVwB1ERI8wEPOcjERBK3mJ5r28Z7+eWVojtfAifXat+yxoYROUgtOtdSEk2gWxDNQlCOitzKrReFUIzIXEq5'
    'goMqmtwZck65FMsoK60Ep/AGIbz6AnuZNG31WWHlDvNB/XOpl/QjXKBmlneKJhzMDmB5eVgAYFbHnfsap2aN7z79eH278ErgyXtD'
    'zWBAih7+PeNu0Uy8/D/fWi6Hv9gurjy+CHCK1O3F9BMeuIsKBUlezT17BVansVnm+K/xesuHf5Xzt24T9/bl9dXjB3hbr5UwrRnf'
    'XsVpyE8ijqKxQUtINJQObRFBVO8EC6AdOeMYVbtBCmKJ0tKYwcoIYpCOglVFIUMP01+kILrnhxNBnixE78UQEWMPShCOUDayt1HV'
    'rbPbjNkLDfmKCDnsa+u6tZW/89ML1xmAprMZju16iWAcEyIxgsrDNGOBuDZimeQ37Chm3qquDaFdtnZMCoGeWAmlIknOpG6NVT8Q'
    'PBjkGC4VmXZ0x4aChzdsiIV1mv3SYnMijz99mvucFmomZKaeCEqYnm7vgTcWn6+uf/Pl9e0Tr/6v1/9cpL5NdvJLbzMAGbKZlFHq'
    'xrrMkYWXNdPQ6ojqeZlj27fqA0Pk7SU7XSohAz3A1X4jYwZFXcR/2nx5TkzyTScvMwpgDYFlyrh4mhGrg2Ra/7Ps52xj8GFNr/8m'
    'm/dqiUjGYPSGPiKJaeQbATjYgqoGdqTsKnyMwcKx982KBpVyJKMB6f0wHXGp08FERF3bqvYL14qaK0pJNqaLCC/72TUGBsNzcntu'
    '247mQl+DrB2cRgkISpo3E4jAQDgkf4TNz4/fxt7DCt+/mLIwiprOn2sejSApEUpMT5P3mjfaVEhRfc++KckoNIoS7TTzql/lAMYI'
    'iiG2btv3wjPiOGBGJhxTpcMsBpJySt6zUJkLr/LQT3HoQ6JYoDNsV81wyMgU3ry8n4vdxunzpda6LxzAwZ2Z213XF1M7FK8xUD/B'
    'TcOawO4xRWV20CnNg2Yx4Q2Gjjuq8gJ/K6NkDtpO7xhoAhYF3uP6P6SZxtkdR9gGzDwIKF3eGHIKi3eYGloqLrdYYGRUvBBpr+41'
    'b2PykQU+ewyXN5W6fPmw2WZo5zVNDl2VMcsDyGqrJTaPYeJjKTuS7AmnwfFd/YCjW74b8olYlTy1ecfQCoqHr3Fhllkq4JdPXcTr'
    'ILFixJDscp5OHUnPwAAgzwe6Ck+r2Zh5vrz+SHr0enYjP92pMrdXiYG342NOdttMw2lAM0SJU1mVdB0oADqRgy+mSJtesO9VlQtF'
    't+TYS8o10sZIYQu58UBtqTPHiXwwmRDlQHfLDtFtsoNBC/3/7Z3bclzHlaZfhdER0+6OGcI7z5mO6JjQgaJsURItUbbcN4wSWCLh'
    'xoEqADpN+AH8Gn0zw77uu7nki836VtVG7cydu8Byt/pqaIm2CRBAZa29ch3+Q8ItsnTxo4gxEBKYtErOtGWc31YWj++/fSPNg5Zk'
    '56uHH11t3v7bzRKX/ZhGIoQTNW/jMUEdYZZ2yYJgj6OWX3XWlRtFJfjC1jSpFYGTFhsBRwpWzG1ibHbngw5ycavJajM6GjwO5f64'
    'lXySVFKZu6rk7vTRqyClfAPc2NH+GQ/WVXH789XlkhXezMn4kAUsPu4AVPDyxDmwU95Kxh/Q8ndk0Vw3ZMAvje5q3dZZtNXTy1jV'
    'yP2F9EBotU2t7nLRzXBqwTRuc23qybMgjsrMwAwqJ9s2ESYxL5arFOdwu7TUMbrLVWpBGsY6IbWS9BqzCwyecMzOITBzRbkR+E72'
    'qcNBcwjmOZj8MZvQDBMibnb4n3D95Dl3Uup0p9LavvgWUR55QALqLfv+jIFVB6Z0gjkVgwJswmYcHgs8lZUpa92s1gGzswVRIUGE'
    'iU2gkxnGuK0QjTu5//NfvccdtsyHiPGYayxR/pUtYd+ppWJb6TrV3+Up2hrCTlnsqoFsMaRXGflG9A1UllSgBsns3IjzssNNjBO8'
    'tmdTN6YeHCFTHwCEsYNxaSYvJJEpvS+IOYRCF6xAIDSCMwZHbMYmOOee0P89he4cm3uwm8AmQpcDJRXVhumiwayOdSGlpdr4lYQt'
    '2RiZenlE51Ndj9MbTpAq7jOTGcpeGToOtOc+lEvo6m4CpsK7JRU6/ZkMjjdUWdJZW04uLVxuTNXwBICvcQcGK7Wjwu233759s5gp'
    'EO5cHpu3QiLlBLsqLjUknIvvQEUdZjGMfpHEaPSPdZ/Gbtx7b+Z7CZRvIwz9hGubaxIFKxhgCx7+SpjY6sZO6aDGUMwIMC9r7doi'
    '802oqgEPqdyF2gFsSohzDBFnrLKjnsjp1ln49rvbtZzqwiUXhuOid1Dcu05EUzA9wyBF2YEPhw1WDXXV0FUSBxePxJ+1Yb6w5Ioz'
    '4BmZ5aSmZgA7hEvFAGxpArezPQ0ntPx5GFit2tLecpnFJ6RD3fB1EzEtRJREDGjb78peUzkyvb9hfIPhyv9d6NDSMceLCApAzqCW'
    'Pzl3qggMm4z0NFYnS75aW5aTAusdIIvBaSbOK19qBAltgN61i3xm4ChvKBtPRcFNiojSkQgwBhmciFwahittboCaIW+0ly7N6HPU'
    'Q9whtaqqvIGZXh4PuJpEbt6+WV2+/d8L1Cln0pFQUQ9RxqjGUsils/iRSj5i9IjjtvWplhOZfmxeRai/bWbHVRAiaq+4QUkpUk7j'
    'ebPv0zqLn7beLSdRsZCkWvrEhSUESCfefrw0RqZUMKbq0xBmOdioAZM6omSIsEUyajn6u++gxwcleG1/VTvKzseaomFAelhqIa40'
    '51t7IPWTdtvf7ywczYnWrHM+T7WH8HNxgIKpwPa3LhXNBQVDyRFvfx+PtxqNbW5/ehcsQ8cl00yvtNAAmqBm8KwYJlQdr3h2kikr'
    'qh1Ih2m84ktGaMJAzh7m7XCg7fSAfOUwm3YYpV/J1VH7PPUwvBMOMR0ecHIDDbs6MOYOI40x3aBbuR0cpddaDDoFZr4ekcgfz7ka'
    '3ty++mnJviYchxFFOMlhCQfk0ve4fqYo4NozVXfZNtoWSf2QVF2oFR7jBmF0awH3omHUdG2ZUXt0umswYdJYlA4HuCBimzFvQBCp'
    '9QZCL9O6qHjJvC0netNd9Gg9HvOANvKYIWyVIW5HAsQBHMPBW8025B2LYn/URp29VdcjiFpXYpx+VO3bp1AcvGtwvkJVc5jJC0lC'
    'HUg8OHupelktwUupjDhBSs7vC94hxR6MgSFN0cvBIhPTNhacGhJkhqF9b5jDggR1VvmJE860dwdcmQStNy8XgneYWyW4ZT2hgncw'
    '2glbQ5q5Rjeau2AyYDDExn7UKiIMR2v4kGUOb8ZDuETKidD6ElM8MQpmgZQUdTZOzG2XU6La0YzbQNgGN8ORDRjtyVtCQ1f6ym4l'
    'qdpmlKdU0vvuWCv5fvVeWr28XN8Tu6Szd24m0B522FRCPNPncq7kD4+fxSMUqEr5prDTIPXqcEaNb1vFUvzgsxsUhNQQ2SU98IIH'
    'rCV4pCc7S9/piU1RJa2s+pLNYhhZQsM6goqc6iD3kSLUhtLQqWr4HXHHVDCnJ6sHctCv2bHds7bkgT+iMoORwNwB9SRpFXtgp4Tm'
    'coEoKs1DqQuJiOON1ZMGcj4rJCRQo3JWPYc9G5+xGTZy9SvW6uBJz0aRAe9iKMCY40TbhetrY8mcFNig48nbna03jbPVYhO8PbB3'
    'vNWaZarpmTaGKsm2nZi+zMrxPVa/9rhmc/+aQf9/51DukB3G2+YcljxOjipOcdXFMFoSCypJpqe4xuSe5QtMtZgbNVzpbNhIDtik'
    'eNNR+LBIJHiU/RTXVjP5JZxx8HFWft9vw0Pn4pHoUWNPdYxpZ4Ys0K3H1lehE10UeMGqQ/ITNVeRq7CM51pnyLf/unWSOTzROibU'
    'Im4Pkzq8O/eG7EqhLJfJoGDayQph/4GSYtux7ipuyYBSRqnhYS1Rc1eLbyG4O2JjBzez9fG+NyQnAVm7oW3hMOvzd4V11uVQbC1V'
    'dRdNKe+8L53dlpwEACzp8BkFxEYsVC8TKUQAecxIX86gHBwVR1Na7KECHgFhSbd9tyZQXaTOJNv4NIDODcwKdNAwjUqdC0DdDdLO'
    'xq7jcjpBI3lLEmDYMgZlGJqzvb5eqIeiPwoVB0jIONiw8rwk25n90TMyI8lSwrGxqpOgy4OBBOrRbXAzgUXq18hcvATvkp2tDZkI'
    '8vjKLbpfw+ahtzaMlLuJdTxtjm21JeQWlJuEAQsuw92dLPtgtURA/G+n28Fb0Rzt95slNtgQjsPLwqIKyM0g9WTmbT6grJIgJQ0s'
    'TquDLZAuVKNERVabYx22q16pEM3WIbVi2BpkC1xWP7v9yE+/wz3XDpAR5c2w4sbQt3SnfAHXDMcOHeGDsbYMftEO8fzt/7l++OSK'
    'c1u6pvIxUymr0q8B93eUDjuy+AXIJaLS2dDHN/LBsOTAsBtQG53ax8jVoOxcH9tKXkqfiLWo5CM0gfZFZg+z5bfr7Cht8qD2VC0b'
    'DN+EAbZF1o33AvowS+qRRhbB2J07LfyG+p56I39nUZzOHZsUJr9M6hSWezCreqHVaknbP41UnV5Ri02jJHf8/p8qKUQ5EUfngJOF'
    'VOd2QrWz70IDBa5Iqs941h+ExkplPz3AcznA+2CFxRxF+aL75fZ28oji8N6zbpDIkHY0q51pE6NsBuEwS7fujWtyAHQbbxD3AENb'
    '3GwBi9we/m3AFSeDEm/j/ceo7ASVu5GIs653jHIrBPDi9LTo+42dTyWb+MHVxcWSrJ/Ngz0OLgQeX9c/WFm4josAaslyhUM+yMk1'
    'AxFFn8IKZdY2dxGw5Eqc+Xzb6wC7ADMBuwEJtjTR9euRZxwbaJ+IXm+GOB86RfQUATU5O/SXKMo2JR+AyHJlfOIrycQPrhBTPTCU'
    'lh75OOYBRknQfRSU3aHU4XyJ6a4BOlUtUQIwZcmWQdG/c91EewKyEZRh8irUXZ2vskNVLN8BrphANjs7KqT3qeJIHdjNN1Bjq67l'
    'jAicQq+6WGOrF6iB4gFbyrnxfKuEcLXBkWhnNfJ0tTm7PlskLx60VW/N+LBWg+eqvH7Xya0GJW55fMEExErRmhkTrMBEUSGtt28L'
    'A+aBdMvoQbagDGxC5cy8DpXcZC6dO06oAMLQ8FKPcZfTTJ1dfo5EtQtCofR3VUndTz3aGyWPCaKS8qoP+UDmTe5IlQhJBIDLEKYI'
    'XdOcAe1/L4FXkOGp+wU5EJaQTp177ZybAMOWdWuRC8qX2Yg6qWUR/C03gXSHDmBA0rRVZIMOcHJLFsdbmOG8oYy0S8BYh/aYwQMc'
    '/tXumCuBng8kS5yu9ZgZ9P3h7Op62cMhH1fjSqcJxrswiBxmq23eCBb/KUuCRdekIeKisRexxzJDnPMTBhU6BKPJiM01u1fWA1I8'
    'a252B1vZ2QWH3C32Hur0p3LtPaRAxKwMXWF05ccknF1zsC/OLlaXp6+WcPM+vvPo1OvoFCgRGBv1q5m1ucjqlcQqm8irjxMEGiae'
    'yN2rBEQbtmikGwYnXNptoysFpsJVDayeCd3D9MRV2XqhGii3hU8tzjCDNd+K7ju7oK3KzlCi2oPhLKO0iSnT5PChIonOVw/fX22W'
    'LPfCDOZi/LJ4bQTlyj5QlTGHnuceQk1AWTgMWwl3qVsA0Ojk/ZZ21TKWpBsadGMN4q45XeBteGYSyXmvHaPzhrluF8BSo8MpAwyz'
    'Dl4GV5hYQmKk4uqDiECJKtKA5v5u/F+m5dmHV8v4oZDNu2OPpdJFtrZwH8C+7WoeWcR9M9t8nbVPVYFVq4+73MHrms8MPTpcUtSr'
    'NEWTbQFV810Lljz7OleVh2d3GtB41WJFftzMkMf6rCvpNi9Iqw4nOjPHzBbs8diMySlPzvXR6vYbgHBLTJpZyNplFb94kiWtY68A'
    'hLDDGGc9EUBQpi0TbipmrdhA3krQW7NaIQYEwHi7cmx8OPOJU8VDXYJbs+cy246majqhouDJkHSeQjuMdcipRSgOSpxUTmsvYCHh'
    'yKPlVUnq7lynNKW3f5Vyd325ZOUdjwjYiIoIXvQB8pWJvQUrzniSDLZ6DakOWRIgAP9QinFmXu8iozzIsRuwarPdCao7DktCKqt9'
    'P6EOlbPDlcyB5RvwzKIo5xoeALrKqkEQhrL9mGVwpywKvHR21a6tMC6PLl++OpMSjBLh/dXZArwbJOoBDEaoDzmUE9QFPewYk1PP'
    'GdJ67FkZw8hhV7cZ6x85YuVeDd6EYV6FMeEHGiF9Ef1AqyfB7Y3EKTvyiU5H7qE2cReTUg+u/XZ6WHfDAHwDgl2D/JfvyyGxK8Gt'
    'qhAS4yLQVlJojyQnbJYcnoJ9d+oXVtjom6PADQijzJs1+WP8r0rQMWFFngkQ6LBnSBLXkhzm6JZB9Qy1A0mNAQa+prCZMBgA3rLv'
    '1hTA3CHYDSoGyiAhhdmahi0Hwzn49mmBXue0kZPUjTrTqCRhKxW0t399jRD7O4wZXTgK64Kstdlva1KPgYtB8/6fRhJNcsz+n04Q'
    'w6EeuDglBFWnshKrJX6Vfgt+Yl/juiG9yyTXTH+FBdbXmGmN65znF69ul7Qj4lFkLweWHVUDjDRtNh03kYyIo2Q5wNOmlgeXy8/g'
    'NRJUpdq2Cxxo4qhNep0xtKKI+ENJsILaiHk/T1TRgvsW1RjJeGWXRPyuunrgQHUCmiC4OQC/uotQ35woa0SFXJy//dcbDMn+41tr'
    'rzI2fvxtrrvueF73EexKbKWUp4DAdpUYFNaq8qamDHMpWno6Cr/9GBxNyNKVNKjFZ6XVmSxBh67Dxd2o1laqcm//ulktOuX52ba7'
    'bghsq1rv2Rg6lVyyuYd8t4A/Bvm6EaBgc0clbmXaLXm2lcU8Y9gzEZNCgv62lTxSsb6gVoQ5hYlBtOm5CTG+NIrWSHrR14MCtESl'
    'cvJq/tXXopaEUBIenA5RGTnz8XCnPcGjZTiFOuQecrTIDR+RuTDEKysh0ZnBYCXCbINJndHKptaSpL/E8xOXTD+fDdAtosVDMTVT'
    '4kHdBRad4lruxompU17FSEsoDR2irY0OD9hnFfPRXSzLvAX1aedxQJIED1lqd6y2VDH78+qQkFQ46B40b7eQiURrDU2BoXMrBZad'
    '0lcxG2FT09xKEF0S/K4hd/0WcJOxgNHlvlVnxoY5R9OOxGXaa1Cbk9SJ2kBWklYaq9ncYFtZM8nLkPdP6kp0HxYqKwuoS+oHsLbx'
    'rrKqYEAfgTTYoTQOjmpDcO9upCmdC/a2yhdRW9bOMcvzTb8/IO7cjGoltiNqEdCGUkfhBFoi/rFbPdkZRRmjRFiHNG/xLrt2aTEF'
    'A78izwuAvyY3WHvC+l3OkCDfQmV6VRaO2/K3JaC4SMfcUOEOMBdbrKvcLIDddNCVm7IKcJADegfSp8TO+hZXzQTrEysg26Cz5VwA'
    '7Zes5rEdtvIgbbPipW0752KcGLBO0c5jv8zpuGcmtvDU/lrcl1n9mhBHGhgKMQjuC3BgHoN/prQPkFHj2H5V4jGKLDqkNmm9Oe5e'
    'Qx2PHSw6r7mn/W+YYUUoc8bGavMIUVz+CPN3BNaVot3aYGU1I0AyI7b3mrxz7K8cYqK5gr93R12IpCbGWFjhNWsGyRDoqEqK0p8k'
    '9zsEskxERsGiMmNGOIKtXLc/2rx9c3FQzE8COB63kJTABeeDF1IxndGMU5uOpJK8Q6UMgcU0a2708aCsmna5S7fgkbkeEOYxzQHr'
    '6FSKUqmnh5gnlMT7K9p0QmGaFY2NPEFvt4uSG9zDAYIK4jbjgfr2QA8tIEGIHLezQfsQ6UG51+akAl61PIopolBmoqkleGCvSjpJ'
    'KOy4+QTRIN4BYIFOosFzFAQJJIqhDQeb9gsbfdxnDa3cBXiKWRVydKnVhtC9G7Z9YHBMn6ysjiFUG/I9y87jRk43Nqf7WkL1akng'
    'yKV394kn2sBhWU1BHf4h9mEQMlAc3smHVF6OdEBRxUj0EmylZ4sEMnqpiP2b2TYsqEV3pJDY6066jqg35DYp6iKFtpspQ8idgZY5'
    'dmGQuoaFXEulAewBP9J8l2tTDcf+SI7sZn2PYwW4uEPKk76h2pci0alCPHRMHTUT1KWgy/Pch1p8w+FYM3CdZedmClLyYhAWlxcF'
    'uq0tFAzSwPgAJbffK6ijw5zemQK6rgBHoTu2o0SHVI3jXY5S2LkF7yvW3Yjaq03SXa7NVfAeUqYGg3fc6MB5CLADotp26LVomMdK'
    'D2dY6unGqTIoBmII891IOdAxZoq6OMDgKtpWAm0An4O7IjyFPVvOvoNussZiAjSKQk3JuS8TEzFJpI/B3HisuiqH18crbJe2o63H'
    'V5fr6wWWhsHbq/FgWsYhqGeOxfbZq4/wLCnoTgfRJjvIO+ZtXSKQUlie4/5g59IFcoMgDo9OOCykukKIMGnkzPHcRunfTwQ9Oxpd'
    '+QTsCJDxQW2YZoLfiL2x37CF1VJYIMNIxsZMRBGnIzHZVoiax9JBHFT7TUcRkx3UProkA0SLjW5Pn0sKSGbjCNs3FroWpvJAjYyI'
    '4txCd0jgFtCJR9fXzBwdfVKFTq75iWB9D+itBrgG14xcdu1kPaVlrgagXDHA6eCkpjIfffz2zeXZAYhSOUp4BwM5HhW5bKwGVw8F'
    '7gHpqsxscLXwDhxVVV7nb/vcSQTsG1izAdBq3RWQzqE8yQwL8mTo3duHydvhrBZ46Kfl0BYJQK0Hhecjy9LnJqCyJLcdyx15VsbT'
    'nV5kB5PBHKpY2y3ZdsyNFhfKuKjmzoc1FtgSDpcMaooChiqDQbm32XYFDiiWmT+mI08A4YdZU0LDjJMsA3o/YCtbJv6YvrOrge0/'
    'qNglPi151pBRjRu8qsKwINiHNmGCqIfDFgy1MetWbmGPr26vrw+mA3r39oiX9VKNVEIkSoORumETN0u4A55XCRZCoeEpjYljMrrO'
    'GRAgTXnuaMXhOjT3tfuqZjaRfKCOQfCMJ+HbAYPKD2rxe5bYk1eYcpipz+L6kZEQBh7W9c61ugAtKgetepnjCVfhuzlDjUeutqfb'
    'efjSznEox+EYkRXmYpE7KyjTcl7tIhiRGKFJ1FeEBnoF6dSDk+fHYrHqZnKeUhUOKIYh9l0XDHlA4gmztQSxuEyxXz0HJqeYBzXf'
    'M9bO6PXY0A+IDgI1c325rq0TjDQ1Oqkfr7VKk+fx5ur6fLXIFnEHwQhhpk6tjnEZHKcSLGczXaThDZJHpBJbA2jgMsASHmBczTT7'
    '8BpFgoNpT4CH1/KSMd22uJqXsl+adxIwwDI8SDNJhYBvIxhOOLZviSVoFyWO0obnhSAgSKm7O9kyxSM8vj27HzIeh+OQ9wA5AvV8'
    'jMWbOci5pJiQ2VGC2OBDY9oo9VpQQbXgZggwe6K0Lyn3pJ6S/ig0+xzQRB7ZOiy+99VutPcj7yUvT4ll+XCRUKbx+fFqs/p+54C5'
    'MEhI4UiXBc/Qjlw5GNOZJMiFI12pakMY1RWZ9guW2Taut0GVMuunvwADMGCcQ24crMAcoIxPB1UqPpMN968at+a5kJgYFuXoUnd0'
    'IAUhomwpFEnOI+jeVfo6H69upbf97fVSFRudP45kjJ4W2CI1pTCd9gsFFYuOb5aWsFIrYbaCdtmgliKlo/INSgNrJbDYqX3iwTig'
    'RiB1Qd7vGXTPNiNzp63leETf3jaq/1I56pIRwQ4gT6Z/tkzcmEgXi3/seLau1p/+eL26Pb9Y4tkcRxABKlkQzg5bHeIeetZQ/Gcc'
    'q5KbVgT2ZKc4Lf0jQ7r2ppLXQxYAhAnU0YR2SBv3mWS/FTf2nbbilfKL7U9iKu7zXaROR4gfv33z4uCkwB3Fh/flBEVOD/HI2bku'
    'J/5zCfKxGVBaSXV3IAGInKRDKNd3TFnR2gPnrOjQ3PiFSqU/sHcl86a9un/I74DTwPEdb20HuWW76lxOnW6YTgk/Xm++QQz98CDL'
    'Iv51aLnYutip+zxTIGlKc+nqyErhXLaK82ZIDZgTQIuhwBr0nm4OEjY25ncDpA9T2oGLAQ5spMDcUnjuljM9hgKbe4PDPSMpk2ey'
    'kSRqcJ5ypmURzZkxSXYqQjUOul1lDipROs6z7r3rjzKxkqJc6n25p+MWTtxGq1E+jQqGhlRtcOMJ8mxoyEJRCGl+TRXgBtKNASNO'
    'sdXmBOTNpJGJ2USWIKZ3UNVizI4qEnJF3oXDwTpdgX989WK9hCxI3h05CMCXdquQGEznSQ8gqvLu99Bsvy1BMYy/h9lkZcttZOyH'
    'jaBvyGBTA8xoDprRsKi0eCskNhdOpXamIBh5Gqqf5X79/jKa0bgKr/XkV9z3D997sbpYoigdtPaYOYcHpb86nAC97fEW2VdEZvUu'
    'VGR7Ba8ryUsVhJydxSZ+R95s1QuKbXeHKHE59arLZYLd8B3cZlBhWCOVLPFoWthmklQExwp+Elu4BWgshmUw7eQbeu/Gw51m2d+B'
    'Nnp4fXV7/RAJ2YUa1R/17GdM6gFu42lkSo/pgb70ANWDcjynNoSh0klq4yzdTNLAOdKZ9OBOLXoaRNygcBOs2CR/psn6sIfgcJFH'
    'SK7UwPKitKNBuXBV+dujd2B6EYzXrVHDLIZzKOnvDrlyW/zd1S3DgIefXt3eSCewsATPw0EJuNJkCXn+LaawIQ4h9Zbgg6WHZ0GF'
    'JlSsl+CQ8lk1IlHkWytmngHST2CXl5g3zW4yu1OuVuHlMY47dnaZxSdUDbk1kXxK83FhUb0nQxHuFm4yGyl+kWmUe9eN9VZlZ/dk'
    '9c0364Pz7XIc9ytJIaUy4aUUM9cfUo/YxFg14I4QS60UA9uDdePgBtNq6aSTgciFGw07pNbdRGEP8ldUodwpujt1VTkoZnCZQnBI'
    'Qt7O9orkIvlmqV8mgJcyQDwSC2KUtHeH60x1uIuSHD7b43LDtJMOucMQ1RVihngdIUM3zko7xHBU+Pvci9W0l05tn2JwKEa1Ihiz'
    'ByX64X5wgQ9dhZjWz2r0lnAVhOvJ2eEhgLNHJlhtxiH4Fq+L+Nkd5r1lShnVZMqmhs8sDSvi/fLkpzQvEVCKGhgjOezaXSOyKRlb'
    'PetJARMqnUmp07hap2uAbNVTNLbgrYROEq4MYJC6yvIsZeX6yaouPCAyMZ5v9fBfXb68XdwXoNJ3nChsiVgpO/wN7LxzlefXMAAk'
    'Q+jGu2bj48QVESiUPiHPjGdU9hyfGNTRWyKdZz0qTaspWLLsTVHeQRIWlgZ6ZQoXkty94PXlgYrAN4AjPmIIXCUTc5BiYOcz1bB4'
    'S7EyAChidFIZ1YWrWb1IHxlVeid59muVvq52pkUqJbMVNxg61Pusojdkvy1VqbqmgtKQkIgwQ84H9TQp7QwloYGnn0yjYIwkC1q7'
    'qH0XRNAX4Jw5skBgroPsxXhRVXC4J7c/rzanrxbNgmcbgbxooSZlILwMx/WKSUDX0h75bxZ2QQGmNYgTTweIxl5u8k6vUKSmSZAe'
    '0RJtzpYcIl1WwY86p7tU2hmxJLh6WDjR0QbfKG9LjMifR10eMdHOfQSn1HNyJ6pVpk/pLm6nVdanq2+/Xc6xchnn4watamULNDYs'
    '7LeB/qCthg5ArcEjPWxgbEITWszMviPBjIGdXaSbkCzedmFgKiR+kOFRbcYxbnsSPAMmnODI5TFyfqbzWNAsTyprUVI3wxbVvkDH'
    'R95H+TQ7nm2ozpY24fCEwM2UdqfrljY1oMc+DCpyIY+vCmXOdeKMatzC9ZLQafz/JM2iBp2ldwx6gTezGObccLUzyTDO3GyxPXCY'
    'fIZhgtGwPaVdz5SFrwKAqPX0QUdaGX4IhZnU5yawiEPyh07uzmJREmJ1wpv1/d4Sx+meOOVosOsE/6MM2uaMUdoJyAiCwBoUTzw1'
    'SWEMA33B+63Z7MwxWEIUJeoYSZ5NsSUdqgVkPyCcsy+2Qsfii/0A7H21CoGM0pJs5V5k75YzlpsLipoDYhyeLXHOd/L8rtLs+RS4'
    '0eXpggSaOTjiavUMgK6xKDVA41RLbGZmi9akLVb1cKqRrHplQKxAnZkTbHvcrHsYp07peaZmgMabDUQ/7LCJnXjp2Yln/mNQaTK5'
    'Vdt1qo7O5Suf4Rc0e4y2JHgzgdeHk7072wphJGd7tuTGjJDyOxtdS4EhfZ7HA4vxf4w9+1W1JNRFai7NjjsjdUq1ibJfnsnLyZMs'
    'ZTNIGsg1bQVWMMkGto2Cyn7YbWNXHxqrCLC5WofPdtwFQ2dpEItZYiawSCishJ0OM+7utQpoJAd7/hNSEX9Y7m7jrMJNy75/BeN5'
    '7lpHieu7Kqi5qB+2QXiw3nNTGrPHjVAGzbxokK8cVYJAsoYNLaCz4DOIFSrE6TwxsOzJoCI/LNW/MzimmZkPs8Li2PMAOPYLBNuI'
    '+gJyNwBThjH1pjor3L54++bm6nZz7wz8yF53Pxz1tl+dsegc/23sk6xOB7b/mrl/EnonSf14WKC154wQLY+A9KFDmVgy+45Iv6WI'
    'ufsV51iNycsweSFDVFzLcb9YYWI+XV8eWogdQw11mj1m9UIrvbfPCvOPtTYz1Ya/nneZk2E66d4jX9zg3gU8cLfGVCPd3u1lGzeK'
    '8fKqsC5yfrcH8IbSkh8S4wnNchbwBwanCfmRjl84wgpQlHQRa+o1g1xf1iaaTZwdUp5zlNAzUSRbtM0+Mai8e8qY2jFgn0xobSc2'
    'ufgHhOuhQvmZtZfT/TmdAzIWeYHBiFw7oj3SPZgy5tgybco+fftmc7Yk5ztf4KRF9hcK8dJfZ2iBdKW9h94X1WHBmCPmem4o1SFU'
    'cBfUuGdmKIN4aWZvJo/iVgJ++szLYQ9qm2BU//+OGdpLrWovC4kpSbR714KI0KlOESk6qeqX7q5BrYNZh6IzF8dz9c253mceEeeu'
    '4WaZ/ZUBuPE8UZGaXnGA6q+cP3tYN8DMrCI34QeIxL7BuLfjiFRY70hZC9rDtMhjVJLQxFdpuL1mQUg9cRNcnDFTwJralJl5BFo7'
    'Uqca0DoLAvwRZhw6eQo0HLNChdN6sn7w6fr6UlqH926/WRLgSOEomfTC5EQ3oYypVHRsZuplB20tLGvWUsGMCpoF6rPrPZOHGciQ'
    '7ab16kmUom3lKFGz1t27c3cKqf5EYQlzk4OwfbdgKZYWPK9LDNVujMgC5oXxN24OBisbwDwjg9FX291PMVdUibkl+5Ny3G7cEZgA'
    'OBHGsJ3cy0/AUL6gPJ2brgxqYoHTBIV8th7DHI/lY1FL9HZsA/htazEhTbWfHK/pJAkJAuhqUT2G7EwlMbFELWQqm/rKMbwFKUZc'
    'PngSRl9FuT2q0728ebneXN2eL3HtbDxucqN+pnJdqxVZx7TSAvPOzEwG1Z6d+q4mcrNHcSvRPLaDG5VfhcUi9VXJM2Y+AERE0qJa'
    '0I03W459d3aHj42Dq1t8OxRToDSsfMnOsW8iYeWTEDSVjCZdUBylPr31zemeMbxRjs1ek3LB/a+0LbDJizQblBmwmMVZOaptcM9X'
    'IieOY0e4tzXs26JQqfRiieZhrlQtfQLjMSauQ1OUAQ/WQbp8+1gmEh2+I44Gjo9tBncr0rxlbtLOYFHe2UK7sDDFQXWTLhqy9DBa'
    '3Hobm9M+l+Nesqfz5tD8xtUjhoAZ3DCoUgR+U36+iGAwThkVyV+NLDD1GeEV4T22UAX5q1hM4GqJgnNud5AG/WV2BeTVyYp36BYT'
    'TOmojHGcMr6dMEhatV6nzFH39b29RGQTBGjVU4HfnW1qzvZiWRxlLt9VuzOHZjIWYcU5NdBLvutSAbVZgobe01bITxo3B38lIjVV'
    'gp37gmJQ5vFbKggUxEb6CH4MUFWT436D5jpFhFy0qCQFvI6gkSfXaqOAdpAfRjJe3HrfdjnkBSgWo36/l1z21f5cT/dqszgdkzf4'
    'kEWdr8s0pmOAZ+TxZG/TNbWQunNQ5VSpZf0MAwJcABMVhiFxPmVgMOwHi3Fe3voAVPrgcvOBPLXgwSdynx2POmiKrH0kwfBmtkg7'
    'SqGCLPSAZ0Fxsd9iGN33wGfHs2s839Kc70ZFP6mGH72+WcIphHIcWmywZmCRK98w6JiqxSmwwmFv59UkuYbaMV0ZAptAOYOmUgPA'
    'i9y81Bo5b+2q6mU6i0Y5XkkTeXATK7X8Ln7t8M2KxYkMdrXtEkhjkbaiyB0d4V2MScENzbFeL5YOFoe4A1Ty1G7TJJiQ2IYp1+ks'
    'DOAFJFEKHhumnugavE2AakrFFn2a29Jx8SDZnGeCKOVE9xCBq87p6vYOGdYpHOQlAfGnTMYw2s2svYLlnpFbUx57s9BYlKBcF4fX'
    'mDHjydZX2e3iKi3641hLTOkSO0bERcs8RCUryTUEOoOxblXtYiefpCcADWtb+rg2g7iEqM6UatTU4gcF0VM2wIOazo4yysV1HdMk'
    'DnEeUelkPyt35VuZIsW3R7d+6LuwkLWID+6WMsr5SIqqz3URTJOOU5WwEJL2v0wvYmPr0zVl5k9/2bl3ELpe8ugjHhUbs6WtuFhU'
    'puew9WVeJo12YOGpnjn2WUrVUG43U/R+2v1+tt5swcvnq4cfXW3e/ttSHkhHeoRAGGZ9IKVNCnO4PQhsvBpoIMD9hVyXB6zTCg5z'
    'vPkptbWXldeEGARKvLn4trB1qNM7HVT6vZni0JWn9Vz+7BeZJri69pIjDEAhM8oY2lj3iy/kWKgtcsZ7Z8yzPlYHfQ2bkS3E6vz8'
    '7Zsl+QN7zJJd3pMAxlKVIfAH77gvG9CDWX48qdKGBicevcHBpuDGNh+WWehvA+5NgExniwi0wmHAoH46kVBNPV2UoNMMk/E7wYKl'
    'TblSfGMqrkyHtNQJSxVEChlUo+nukFN1yFIfnN+3Z4/HIe7cier45O3vOfY0JpAldm7HzvM1Zwz4a1T1GgDpZTY5h47oLF5OFkXh'
    'qkiwfGWQHehjJ7en3SnQ537Dm6m9simH4Pi+EvOSg9ymhYOTR2eOcxEhvSPpC4nOdpICajIOlJrU2EMY6lwLNRRyLQXT0K5zLJbM'
    'BhQg9qxbK6UqJUiZNEjxxpd2cb9Ld7E7tvGDbjiltNrS/KYpAVSPxKhliGGhinchIVTtmAeg8DxCQn0FY/rs6uyQAZ45TkyCE5X7'
    'JDDWzq5TxBbuInn8Ilp6pRGYMShkSYEKRKN1WsBtlndtwCTPxka7Xu9A6nYY/NPKy/ke2JaZEBeD6gTk3NlGBKAQqisy9ME2PuE+'
    'BOjdg7AcjzbWR3t939A8HVuCsYuB80unULoa9h4NY+ky6dMbtybDkJVthXxGT4JKXrC6ZmeG+bmVlyiSHKLUv3K+JuwXE+rrfL+b'
    'KvwgujP0h/qiB4FBr7Qg2A+o9cJ4qNP+67NDuzP5y8fVXQZRCHykQrQdqnhBv1tdbuBrKi6j8lYdUL9IjEazybOpV1RrXskCuF34'
    'FlbjpeqgckDsfz+YiaZX0kbSbkRsUZptVZirRZF4liQUcaCxthuutOe0slsL7N3Bxmki+PxiV4MtlbTmOOwtm0U5HqgLnZGXUSqr'
    'GoHQR9Vr3sDaG5ssIiYNfu4gRBQH2GNx68VUOQuCucfmAsrinuBchvguynPAPAyrwoL1zsIcZuAUbWAWJtX6eJyVNdPn10sDrjib'
    'HZoDZuBoahREpSGyRdNTM/A4CNqAP5szFTRULoCsBk2cozz2cRajfssqSuwJSyOBVLjMYOFbnHNM2YNDuy5BEk/SXSTpntFLDy36'
    'AN8N6VQR+Vyg4yLmFOX7MSOWeA7juVaaJ09XGyQSl+6rsDwmaDaQ3p2oXVrCUDUb24GGDoodlbYJ2osOTirNLjYmKvmKsegcP4OF'
    'FvwmhN5cC1wcEIRCWbGwgjxoXQF+Rm5VXfQwLMht1Qp+DJlRA8+wO9nC7tCopZeNatR6d7QNcfzpenP6arVkLRqOYTd4NlyOIpeZ'
    'JyCCeZ3FSkDus0Sc2aqplXo0aUuQqFmj6ewUqNE8YEF4MW1bgKG8QsaZOe2hdcn03NqY6ERwNmkIiqGo14/qysso0jnt3To+g8ye'
    '8Xhi+YAt7ni8065AzvZ6dbmghDSbFlq3CKzbOi8j4JLk5FyZiyVagJgpqW86iuCDq/c1gIzl3omqnObnmCRWAIO8FsJ+XsTK2yIH'
    '4fVK2N9cqTOM0QmVxyhIC6mhwSRpf54NYmdyfLYPqUGAOXNR8EKkjR9LrQpT8/Rsvdmsz1c/rZeUf/NBVfBadg44vs8q40/f3WE3'
    'JSTtUU6jsC6twInkgwHtXvQ681zgBFAjcr1e6WHtOgytWh41NIWSP7wOk1IVe16AXyqKnGdbBZX7h4DstyT43vlKaUN6ga1yh6yT'
    'DrA63uvTq9cLhUEejisMAtpm8hItGBMbOmcrZSLhicWYd7XgnNweLJgyRIgZHh+nCOQt1HAt7BbjVftVsvoNWYye9s7iJvUE50Dr'
    'Mf0BFLzVFK3PFjoU6tcZ6G/fI9Pi0BuZDZVBAn13tMU0Sfd8fX19BnH3VpLv5sXSCPwgNLS0Bo6DEsOS3LrRpQ77PMkHjRwHKmyp'
    'ntVK0IAYy6qEFvwM1IwpsUS2XLau5ZRufb8syyCpSKf+jbbnl20y066s91JqM28BAEBREdBaCnlBAwmCoFzT3imsfzxj2z/jx6vr'
    '66ub/zhwUZ5i0Fs0q2CsOlVZArWCIrRNqsk/9byyDLKwdUpW8bDt1eYxrynYPkVXk8ukvmWTAussYPk0Qda48i56n/UYOb8DFfJu'
    'kFhc/0zvY0L5eNycKzIcGf9NnfxQYTwbJdVq1tycbEKPEmcK8NDOziiRCu/dYUTzlFbq3mXIhdpSZLtrYP30DrYlze6qsDBUBe7V'
    '5c3V4rzAzoSRzAGRBNUOcWxsMPJNudeFgWECH4DjnGkU1rMbEJMMDhvxMtNPtWBpC+YCfuuvXZcJBq1GDKv8fmljTnJHw57EzT6N'
    'qZqOjtoygZ8CgaUcbSrd7TirSPl2UbUL2XOG8XCnKJqnG51/L8DCfTjIG0mtBE0xCo6XYqzD3C+qfSQ/b5K626s2RDXzRrqGtoME'
    'YTpez2wlMlBjduPtsEt6sqKgsrI10N0Ry3KPWcZK2QBzKmpkOUPfS3zAYy0ohceFoTerYck7iFbbOwmaUIHrnt5K0N7+eB/zSXqi'
    'ZZGPubeFtJKY/6E8kGLupFk4F2r6oq14S4ssmYk+HPLY8dOO2N0Ds5VOv9ZJo1r0+JIkxAHi1ILB9GhPyW5hOFKcqP7vTIvKsEv2'
    'tIMAJvsXWTFWHXbpC92ojhAqC7zxkA8nieTsceLVSJmjFCoBFEMP6lyU8YZqpE9aCk2xByx0HZr3LBfm+CRwyWrAxKC0tReS09Dh'
    'G8OWsK/IouscssRoUYmDqAVDC883gL+wX0PifSFF0FNaSnPp+3cw3FBJfDxZPfjiSu6yh49vf1rStWcicVTFy5vObi9jzxU7fTCm'
    'noAOJN8CNqq6CcOEOsu5I8afO4wHg0mwwcp53kwgZUkSB6E0MXR9h92uR4EU20l0q4qS43sWufLo4K2s7OER2REquNcXgG5/ujct'
    'OHuEtxD5EbdOeSuiPC2uJ5uCT6dTy1UL26PW+JTS3ioJkwl/e7EVqXB9Cep6ZXbOotUuLAyMxaQeMjbt0QixAw8F28ksEhB0gCkw'
    '0wJGC2FQIeDQ11+nAZa8K9/PBNoaNx5yqQ758rvb9eZqGRFaTDxy0QBiDn8MaVZTb5ODjUkYQCWCKqo3OTxkKj0rp9+i6gAkGCLa'
    'B5VHKS11D1nUCO5OgjZNVGlsb5Nj7VZ0H2j4YGZ6n8NW3x7iu+v2v0xDpNYuclFneBIjqze4KT7hy9XLJU/MbI4DNRtk53CSSer0'
    'NyObQiPEZR1F7VJPxXWtNmREdLI3s2MtKPNoow+bMbYeFxwFcaiGsvvetytUyVvvpXiT7+ZKnh1rVN4P/pslK3y6p1QZ1TQbv2/J'
    'QmY81VKd6tnlzcP3N2en66101SHoR5ibC7llXCgIbxtUjZ8RbNczD4kpuTAY15Qa0Wzhc/qgOuMpDR1FhSB1wYBsQgihRdTIRQbg'
    '2wftvvcDsmR6chUZaCqWzwrPn/k9B+b3ZYe+Tv11BCUoOi7waEZSb6iEa7Yn/cH56mxzD27RHYX8QKeYlSsQIsnGNnU6DKl3YIQ7'
    'C4U6N+cMLwlF/6IWhe2eB9FWYHhh+wDP3MekuEYR3yMyOBlElk4VDEbOyU0WdJHnWl3bgYWRuqhB1AwLVbCjspDPTNCHxvrBu/lB'
    '/6QU1Pc2N6/OFtvioxKHCydTDIUrPTNog/a6xY1q62lVAXFB+Kt5KYZYqYWIKrPRgWr0eZaRMTuCi6UeOWaCsXmnxS/rqf1/3MLE'
    'YXeYlX3T9jAfrzffr84WKTv5WIQCPtMlo0E9DN11Gjg4NAT4VFtj8UtSJDR6ImjSzgJWogcvLUwlB7WBaZQUoPkiOem0UD6AUSAD'
    'odqEsEvgbfVt4YC7u9x8SALYBeQdBpVQhyOASErM8ZDD/JA38o2XbMvdDAZST89LU++y40cIyvHzx27qBVSH60rYJo2pIAjOPp47'
    'UuEVvmOprXaYWQPZzKSXIt0sCHms0fet8dDVCuKCcnTHUWENrae2YbNHXVFojBb8SqVClK9OMYk22+6I4zwpPFnf3gtvLPGQAmZo'
    '9muM7K0+0ag0hu7+End3+bF07F3VaPL0WsXLDPAW41wDF0qoosJ9KjOKKp4LFiuI4KdWDUNvMTywPZYDpGCwzSHjnEN/zY5VqjC/'
    '0BrjEBqIGLWqH884zs7409Xm5uzy4Yvbh8/Wm5vN4gyiHJpBxKbXwFWY9gpVctNxJmNKwRpStSr84Gpf6CRlhMRpxKM75zQ3zkq4'
    'DCkmhiFHy//Hf89pkO7B+VjI9GiUEWa/ZBMXtH2Z7TFx9ECnMSIZ6fq1BN2mVHdexZFHSwGpRmdH/fmt3HDnv3rv9uLtvy+JOss1'
    '2a41h2Uamjz6sEVpG+RZsj0WGs453jEPMmloqDxKImEdl6Fs9PIG6HOmiKoc0hAqpboscjzRh2jLdBBRultNhK7wtpUWMTVthwP5'
    'C0qrGGWa9GcROlORzCrPL0nwrmxL8wvw6ebsxwXgoy/LO6HW61ie2qJaAOAziMhOvsBqhLGtNB/ySTV4DOaaZ5kcEBmby+TLlcaY'
    'jo3kViu6Bo9Ject0y2MivwdDW9sTZGFnAj5vkG80NEQ0AjnA5wo48bBc6VMjKM6NkzsEBa+RyxMqLMn2eP94dvPzAsvvIPyxOd/g'
    '1OLNSIcu2ayrNGo8ErV0bzgwmhpMJnc0AGnYE2pE3fJVGUZukY+t0qg6FdJTh+LzEPfzYNdhAyNuzmIP7UwH23SmliuXN+I5YHBM'
    '7PfMYCKojnCyw0BnnFXmOk1cXi5JEVs/c9U6YNMtZRvKZ8HKC8IYNHdKiiRBaTHq5WgbkVwlcUjJ5YLyDuYGD4FdL0Msk7ew3Glm'
    'QDSrqFcjYMD9PMLlrvqgt7TZ8C3lEJvMAApbtaR8VhTkglU3E7cBVRjVrh1LilxnhssbUOZLSB133AAYzyxJZWDTFI40g+9HNXot'
    '9GPO1FoXiLTK35TgI4Zn91v0CqMGTGKdaXeZnnAnjaL/NtEpLz2J3IJCGy4T6Ay2A+CC/YE8QB4olO9PJQo+obT7A7IQKdzFbV0Q'
    'b06XRQJMnGkwuLAI3zMgSBl8I47J6587aukd49G6Mgzuqx2GxawJhzYlfiYzi910ouW8Q2CcdXyF38sQ/zEQk9fq3ERE23U0XtFX'
    'sV73SYh+l0YmgP0mYmXR4HYdFLfRW3AiJYONpVQQYVQqD9Uy/sv1RtLuIcO9FI9s6RBhTmgdywvrKhFHMOf8VAhM1QKPqgseYFRK'
    '2eHmtxq4W0AIYOdyCE1HpzHN4rRIfbaHROc+zIyroeA3yRYjt7caVmUw4KXdMP2igXkJvvY8B6hWj5Z7odJq+XJ9uzSsxDPjOJFn'
    'R/mfwB67jji5Fl0Id3FbsCyr8+7AEDjELQrYzqdo6G575JTUC6UVfaUUKaq+mYbJ0bpeswy+C3Y8WVWKotSmBnng7ZDxR0XF1fXp'
    'U0zQCseLZ8fI7AmVD9SXW0g/s8p7idaHcb6+WWkUuVLVnwjlYN/ZEql4Ks+S1GE0xtXIncPMcKUNpXMIuaMzhk4nLDVk3+ZCmtLr'
    'oSKNMVSeMq1jR27fq2QsYAmnei71rt6COkqkJOrjBQkGS5aBTYAm+/akY7Wp//J2c1BrW8ImHzjeVmff0FtYanJpgHowao/CHJwu'
    'VaoIxtRieVoBMEsu2LXMPcsyODwENjPDi9YULutXpDuLYWKFXlKvggAnKRnHIm+eGwNkDMgxDNC8Y7Sb7BnJqkGXJCXV6R1Pd7qU'
    'e7b6fr1ZAqiHGc639tuzTf5F9h+sbgaU2hMxD0xG8I9VEIGv4xZOnjRCEYcLLe3aOYSUZGAiERpzrfdxUML8gMaF8RMnnp6MUzLq'
    'Dcb1Tz8dZ3g+uOB4WJekK49ed2yoMAw0GtRwduVDrFb0z16p5/zmgKcs9J1j6JWYOaNXzfPJBnten8mtLD8T6wjtb2u4GQ4zkcYX'
    'tmrIc+N5SyOqq57YKGlmddyQugBwiDf7maVKbcyH7EWVUDPMtNx6RKBVB1pIBeCQk+0csfRBcGKSjlLMyBWWoqM64PV/kvyglXoQ'
    '7c/xH9fBUQ+To3Q1fmsG2+lIBC7iyyYOXDa8g/zg9i5ZJk5Ka1ij8569kjNastR0s22wSct4aHcCuTZh2arYidkjToIcoJLAMfF6'
    '/06SJ2yZTP9Guk9zAEOwJIiougqNUhvkBoRzWPTHqTx56dnAYJKCqFxiE2rNTFef28aiqwfxb8GihHlb0D2wGt/sDtdOG4SvlnYR'
    'R3VdjLtwAZYcjwuzMV2naBZ7uD1LkosNugm3BXoh1fyeP9WAd62TV4u6Uis8LBUO+8bEMmziYOZy17QwqrM9Usd+BtHlMpLELT8i'
    'PPcFYjoiFXiZFrb1IzsiVjAR6Oiry5dXt39eQkCD3DyOfwJLAlwSF3ey83lMVuRioXUNpvbWKAg0YgcZkImaqYBggCxVPMonwdUQ'
    '6Kwqw4yCaDt04XU3tI29rjaqvIBFz82pWVcNHQtUpQ6xPWqPftCy6vaggeUhCnfHm+vjlb/4YnEeI2XhcbY6gCYGVDmQbe9NEiXB'
    'ezDrGXZBDdJV4RPnwIgkN/PeckVl+OFYe98UqgWXG8o0DLPixFRHdQPmHRcUGaWNqDxWG7tShOoTgpZsn30iVTmORRHeJNu2MR84'
    'V53t7YtX642E7wJ03x21pKSW98z6pCIHvjW/73GxcBN8uW+076boctUxaI23Kr2QKnipHaUeo6wy8sjvM27piZLXgGafWnOz3hWP'
    'LcvkVxpXZlKy1me6eftmtcBLD/PpoVl01wDf6HVD5uEv264ekGNpqB5t1jUaIPRTW8ditxVWbwpUAKJ4nML7Unuy2mKrbHdohr+7'
    'v/NLr0J1iLTi9o4OXzLtomygHzZQ6aQbsUt4PLJdkodTOvOxPq2gIH+Q8nS11FRhft0c7HDIvCx77C/k/aDiSZ2miuxlJZikGwmu'
    '8oYtrFxoFRmeuFldwOQLfR4qe9fQ/TOzKmoRAEVby95DRtuwsQpKQHSkre/DtvyFl8rotywJuIIiNlyZGBiMWSA053rzanEkq1oS'
    'RyRYzOmxC1TJJNvx3tPddUKBlbs1xAbuEQsma3K3DVCe5mOtQZNSBGrmQ+NirrthCg44N1Or2Ox6PCkPCYPBIYNBfafqJAAihQ0M'
    'xY6JSwKYEb1xubPQMBwzQiVU8Yez1eZiCUwDaOeAPlhuoTTIEyp1m/Vcz5dASknAnQZ4qG+EWzNrN0Q1HCIJca6LyyMfVVcgpBZW'
    'jimBXF9Wu9G9JtCQegIgLKp56qXc8G7ut2NJ8AbzlRSXpJcsOmiZSxD9t/FgY3Ww68vL9f14JZePE8cF/4fgpcvgbToqKxGltZKw'
    'K8H8KVRz2YGef1tdmfnSPJFvnVHD7Fx7GmUm1azYlN6snrSjzLvt1QhyzfJjFjVaM+0ZJ3S42VkyyezKt9JfZ6t+XfIeDfvkUJVf'
    'Z0t6l2Cujqtq0SZA4qNICeQ7uxpClxkhJipafk7nWFE6J5QTmKXMKq+MjqPHdgUsS6uZjVgefnwwA6eEiB6fBweepNqjUjybdoNr'
    'oDpkIjOoU3VfNZAChrqd+k3+5+5Y41AdqzQNuJXc43yqIPijWjPGydLaUAmpZ9Y8+yIQZOBBN4KtUl/RLkkFxjrXzu81uWQLVhbw'
    's31srQ0D63l4zglx/Tt2n+0JBIFGM0HdP0gprSXnIDkmq54q6uSxO24JatbDwBvJxDE/pNAc8nqzSIYo/rhtDYKrziBeZHUBOjvZ'
    'uEVwWbX7q0ZZI6g3YIeYkE6cHe5gOQ1d2aQS2sSAZDwWdUjCT/bktoPcx3LJS3hG1WSG5dBKssmVo9Ky7ON9d9CtpfjAxjAiRGlG'
    'gcaY4ux8r+9PwOGok8bWBhkjqyIUJfSgjgZMBp5RPPONcsgALwH3MqgLbRPB1FBqZuLPkyxsbqeGA2WL1MQl7bVx8QG8n0mZFGer'
    '4p0JakS/IpNaY8Dwgi17vrvYUm4Olv3BsuW0G4ajqrLIqTALw7A4lJ7AlaQsUpvcB6jZ51rxnZjUWhhTwV7FyyxZCQJlaM3kEiTC'
    'Ac52zmbfl+WOIbL0JKDRGJmXhEXa3CxK7SK0LPN9KSaqG6eUvwTyYhwq5KF3wOfrh+8vaIihm9Luyw+MGvGMgvEIP0Te/7k8AKJN'
    'LqDYqGaJrjKNAoCL60DEtBuhvDkBGCs6sGNpx4iayt2QkKgcFJqxv+HURHK+Ls881+zd1QHEzwx7OdqUqSFLX9ki4k0sr4DJGmJI'
    'YxBnu3DGX65Pl8x7j/REdBIT2SnDoe/LZcGB4TjpQGc05iZ3vr2Y+M6gSkrFnHKwJ2HMTG4iUDgmhkCden9maN11Ds7DyzRS//jT'
    'wxdnNw9/d3V+pvZbvJL+jPE4Og/I1MjeC1fRoYec4Xr2kcm4w2ejHjJSvpuoRvbFlLkvn6PEUOcQr61TfZmRSWDfSbi6/ZQxdk5S'
    'Oez0KqQWSrwmIZQTtVo3KF4U1/WcVQdq3IYzcqg5ylX2F05wc8aPWx3i/5ITki98rd/6777QP71+sL55cHb59s1Lvt7bN9xxI3dN'
    'P+HBxds3L85UH+d14PmSglv+Jx4pUKWoMeVL8vmvr67Pbs6+lU+8OLs8u7i94DbeOXdcrH7c/omkyt0bGZ6vf5Rze75Zn67OT2+3'
    'Mo2jJEHpfFS/HR+VmnJzun7+7Rl/Ku/N5kJ+9ms90uebq29ur2/Wz5+G50/li2xf+vOLNS/h+W8//Og5gnEnP55fc/HsvtD1q/Va'
    'TvvvPry6lINYXz+Qz9t/9HYjb9/fvbq5eX39m1//+sXm7Pv1ycurq5fn65PTq4tf81P8+sWvzc8Xn5z+/rv3Pvr40aMvfvvqy5d/'
    'MB9/eJq++lO+jY/iq/C7X39/tv7hf95ev/4n/RLXL/6Fg7p6cfbt2fqFfAP5ueLDIT408ZkZfuMDVAK5N/9ZPmv1/ersfFxpB/OX'
    '6VNw5Hv6bHX744MX6we7L/D2zYPV7YNrpiP8aRwe/LcHL24fbHrvfNi962rhuXvLL9cvV81bHuq32y+912HxfbblyDf5Rl7U8/FI'
    'qjf5x7/xTb46vZ6+x9evN+vVC/0K17zX+eLi6skje3H9+P3P/vjaPovhyR8ef3n7L+dn33xy+d3Dr38t4XZTvdd/f3V79uKf8I2S'
    'Z9lI/UalnXX8+Pebm9dX3/7TzeZ2/ffXL/S/+5ExuGd2kNJI5SOGoYkMuS/+MqbDYx/01evXVxs+erPevHj75lTOfBIGL86uX19d'
    'nsl3efBh+fWHZswEJ2NE+JNwMCQsyIS7kMhMgbtP/+4Lzj+y/QbvHhCcwn9FHDw7/fHDb/706PTrT//knp6t//j1av3pl7/7+eqz'
    'T1dW8kH5pePAduIAYMn0Kqxj4e1fX9yebi+f/zFR7ruRp//6AX/p7b/LU3/Nu399+1pN2243D/7BhAery+v//kDuwQfXp1fncrtc'
    'y6f9492loO8psRB13n/gSih4nCjpWiUvzSQykj8BnYvukAMgnpZuCfojzs+wqbJAobphE3Ebi3K5WoRAFFlyKIjGM3sur3ytL/wu'
    'hp6fXm02Zy/XY4T9g/nHXzK9PPntV+a3+YPTp+9/9/XFkydfb37/7LNXf35q42e/e7j6+ve/RFiVhzY8M16SL6rh0ibNLp6Y/tJW'
    'UUfEFhXSt9cP5O8/uLqV66eKNiloLs4enN992i6sInlje+foqPhAisEtQ8ou6d9SKdnr1n5/CUXiwGCSpNpwvh9XEYcCym42NV61'
    '+fr3EyZWUc1Zi2Ncnw7H1fY1Pefo5HXvw2wWXL9gSP3z8C8ffPtzzJ+c//GL96y7fe/Kf/bDl7l8k75bffXHz7/6ZULK+GdDliLw'
    'N0PsZKpdSN3V3XU0PbqQYzqbVy6nryRo5PO3hcvl9faiOiU0KJo12Ex4GD0ZaxdISBCZMZbAaxaoQQfDaVrEWIUE4odsEtJqZSEx'
    '+a3dLAqFQ4zKBukG0O4noOLPoFrDPQGk9c3umBZT0i8YPB984n6I3wwvw+pP773889PNv3z8+MVPH26efLR6+vlXq4uff8l85Mpv'
    'BvZCph8808bscPzcZaLrFdcXaWd9+WCtn7W91/TLTHLR3SfepSPtyDWG5H+XYyII6Y2ETzWqy0mXLt0MFBm/BiaxOgFYCiB8BuGk'
    'RrbJg+K7jyiPti/6+f7s/itqJfvw88+ff/b0/cfum/BF+jKf/7x+cfPJt9+9ePbBy9X1w1e/TK1k3DNjfjN4gmgxA+2793dJQb/a'
    'ffrbN7u4SOau+snuRF12l8sfz3wAirjT1Z/qet1VxvkkKyUC9iKA8n6UJKWKeVS8rRpTLUQJPwwTtWhQqtaNRh0kmlfGF//chOif'
    'f3O1uZxcTQvx8MHVxcXt7vP+1njY/Ck+yvn09ofL4dHFD2fu908+N19+4OPrH588fPb8h0e/XDw4kgqN6WI8MLCpQwFal77hu1B4'
    '7/QUjcVvzrSXevD66kbunjPYSQ/Or0558uR5eUC80ESvT8/konr59o08RRs+eLMekwokODteTQ4WhTkYP8OJbvLvYiacLOQS/cJm'
    'qaPS7zTs0T65jQ0+9/Xz954+eX4No2175bym7n++erlZvzxUrKx3EXS6C5O/NUQef/35n82j8/jDxr366J+fDY9/++Hzz3/6/Dp/'
    'db767dnPP/9CIRKfmfybEKiDF0OkmePVwfLk6uV2gDe/fDZynZy9WF9K9Dx4vTm7PD17vdK7Zvf1yLK7yBgHYVs1yBAB84OTiTYf'
    'cfM4d5LwPYlW2WiM1nvRsjx1m31zd+QAbny9zyev9/n4etd/Qx189xf+1rh6ufrk1oRPwu9/+vzmx69e5IsnX39xe20/X/lHf7Kf'
    '/vzxLxBXZng4hGfW/kbq4YDkUOzH1WT4W8fUH27PNXmMGef66vRspVD7NsSkd73mIbzWiZ427tpynd9eP/j+7Ht5mhn4ne8zUDhR'
    'cp4moHzPKKcOrpFI1Q8bsN5x8FlRobvyu5OJQExDv4nIxt/XSzXR9b2cynp3KBIo2zN5l2pm/Z8QRr8fHttPVrefPHl1+rvLL777'
    '4Y9ff/r9j9fXn5T3/ly+efw6/RLpKZOe7CC5iTBaTE+zLcHfGkzfri7UzfjB9Cuupx37+Bm7aMLmb2zagxbM/xnRJF81BzmuoXj2'
    'HMYstebo62PdAtNO6pny/6PpPxxNf/nL/wOmHQmK'
)


@st.cache_data
def charger_base_communale():
    return json.loads(zlib.decompress(base64.b64decode(_DONNEES_EMBARQUEES)).decode('utf-8'))


BASE_COMMUNALE = charger_base_communale()


def normaliser_nom_commune(texte):
    """Recherche insensible aux accents, à la casse, aux espaces et aux tirets."""
    texte = unicodedata.normalize('NFKD', str(texte)).casefold()
    return ''.join(caractere for caractere in texte if caractere.isalnum() and not unicodedata.combining(caractere))


def trouver_communes(texte, exact=False):
    recherche = normaliser_nom_commune(texte)
    if not recherche:
        return []
    if recherche in BASE_COMMUNALE['communes']:
        return [recherche]
    correspondances = [
        code for code, commune in BASE_COMMUNALE['communes'].items()
        if normaliser_nom_commune(commune['name']) == recherche
    ]
    if correspondances or exact:
        return correspondances
    return sorted(
        [code for code, commune in BASE_COMMUNALE['communes'].items()
         if recherche in normaliser_nom_commune(commune['name']) or code.startswith(recherche)],
        key=lambda code: (normaliser_nom_commune(BASE_COMMUNALE['communes'][code]['name']), code),
    )


def libelle_commune(code):
    commune = BASE_COMMUNALE['communes'][code]
    return f"{commune['name']} ({code[:2]}) — {code}"


def etat_pour_commune(code, etat):
    """Charge toutes les valeurs d'une commune ; les absences restent vides."""
    commune = BASE_COMMUNALE['communes'][code]
    nouveau = etat.copy()
    nouveau['code_commune'] = code
    nouveau['nom_commune'] = commune['name']
    nouveau['saisie_modifiee'] = False
    for dimension, contenu in DIMENSIONS.items():
        for variable, infos in contenu['variables'].items():
            nouveau[f'valeur_{dimension}_{variable}'] = commune['values'].get(infos.get('donnee_auto'))
    return nouveau


def enregistrer_nom_commune():
    texte = st.session_state['nom_commune']
    correspondances = trouver_communes(texte, exact=True)
    if len(correspondances) == 1:
        nouveau = etat_pour_commune(correspondances[0], st.session_state['_iss_values'])
    else:
        nouveau = st.session_state['_iss_values'].copy()
        nouveau['nom_commune'] = texte
        nouveau['code_commune'] = ''
        nouveau['saisie_modifiee'] = False
        for key in nouveau:
            if key.startswith('valeur_'):
                nouveau[key] = None
    st.session_state.pop('_iss_commune_choice', None)
    modifier_saisies(nouveau)


def choisir_commune():
    code = st.session_state.get('_iss_commune_choice')
    if code in BASE_COMMUNALE['communes']:
        modifier_saisies(etat_pour_commune(code, st.session_state['_iss_values']))


def recharger_commune():
    code = st.session_state['_iss_values']['code_commune']
    if code in BASE_COMMUNALE['communes']:
        modifier_saisies(etat_pour_commune(code, st.session_state['_iss_values']))


# ─────────────────────────────────────────────
# SAISIES, ANNULATION ET SAUVEGARDE LOCALE
# ─────────────────────────────────────────────

# Le composant est embarqué dans ce fichier : aucune bibliothèque JavaScript
# ni service externe n'est nécessaire. Seul son HTML statique est écrit sur
# le serveur ; les saisies persistantes restent dans le navigateur.
_STORAGE_HTML = r'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"></head>
<body style="margin:0;font:13px sans-serif;color:#64748b">
<div id="status" role="status" aria-live="polite"></div>
<script>
(() => {
  const status = document.getElementById('status');
  let loadedNonce = null;
  let lastSaved = null;
  function send(type, values = {}) {
    window.parent.postMessage({isStreamlitMessage:true, type, ...values}, '*');
  }
  function result(value) {
    send('streamlit:setComponentValue', {value, dataType:'json'});
  }
  window.addEventListener('message', event => {
    if (event.source !== window.parent || event.data.type !== 'streamlit:render') return;
    const args = event.data.args;
    if (args.mode === 'session') {
      status.textContent = 'Saisies conservées uniquement pendant cette session.';
      return;
    }
    const page = new URL(document.referrer || location.href).pathname;
    const key = args.storage_key + ':' + page;
    if (args.mode === 'load') {
      if (loadedNonce === args.nonce) return;
      loadedNonce = args.nonce;
      let saved = null;
      let error = null;
      try {
        const raw = localStorage.getItem(key);
        if (raw) saved = JSON.parse(raw);
      } catch (e) {
        error = 'La sauvegarde locale est inaccessible ou illisible.';
      }
      result({kind:'loaded', nonce:args.nonce, saved, error});
    } else {
      try {
        const serialized = JSON.stringify(args.payload);
        if (lastSaved !== serialized) {
          localStorage.setItem(key, serialized);
          lastSaved = serialized;
        }
        status.textContent = '✓ Saisies enregistrées sur ce navigateur.';
        status.style.color = '#64748b';
      } catch (e) {
        status.textContent = 'Sauvegarde indisponible : les dernières saisies ne seront pas restaurées après fermeture.';
        status.style.color = '#b45309';
      }
    }
    send('streamlit:setFrameHeight', {height:40});
  });
  send('streamlit:componentReady', {apiVersion:1});
  send('streamlit:setFrameHeight', {height:40});
})();
</script></body></html>'''


@st.cache_resource
def composant_sauvegarde():
    digest = hashlib.sha256(_STORAGE_HTML.encode()).hexdigest()[:16]
    directory = Path(tempfile.gettempdir()) / ('iss_sauvegarde_' + digest)
    directory.mkdir(parents=True, exist_ok=True)
    frontend = directory / 'index.html'
    if not frontend.exists():
        frontend.write_text(_STORAGE_HTML, encoding='utf-8')
    return components.declare_component('iss_sauvegarde', path=str(directory))


def modele_saisies():
    defaults, limits = {'nom_commune': '', 'code_commune': '', 'saisie_modifiee': False}, {}
    for dimension, contenu in DIMENSIONS.items():
        defaults[f'choix_dimension_{dimension}'] = any('donnee_auto' in infos for infos in contenu['variables'].values())
        defaults[f'poids_dimension_{dimension}'] = 1.0
        limits[f'poids_dimension_{dimension}'] = (0.0, 5.0)
        for variable, infos in contenu['variables'].items():
            defaults[f'actif_{dimension}_{variable}'] = True
            defaults[f'valeur_{dimension}_{variable}'] = None
            defaults[f'poids_variable_{dimension}_{variable}'] = 1.0
            limits[f'valeur_{dimension}_{variable}'] = (
                float(infos.get('min_reel', infos['min'])),
                float(infos.get('max_reel', infos['max'])),
            )
            limits[f'poids_variable_{dimension}_{variable}'] = (0.0, 5.0)
    return defaults, limits


def valider_saisies(raw):
    defaults, limits = modele_saisies()
    if not isinstance(raw, dict):
        return defaults
    for key, default in defaults.copy().items():
        value = raw.get(key, default)
        if isinstance(default, bool):
            if isinstance(value, bool):
                defaults[key] = value
        elif isinstance(default, str):
            if isinstance(value, str):
                defaults[key] = value
        elif value is None and key.startswith('valeur_'):
            defaults[key] = None
        elif isinstance(value, (int, float)) and not isinstance(value, bool):
            low, high = limits[key]
            if math.isfinite(value) and low <= value <= high:
                if key.startswith('poids_') and not float(value * 2).is_integer():
                    continue
                defaults[key] = float(value)
    if defaults['code_commune'] not in BASE_COMMUNALE['communes']:
        defaults['code_commune'] = ''
    return defaults


def modifier_saisies(new_state, garder_historique=True):
    previous = st.session_state['_iss_values']
    if new_state == previous:
        return
    if garder_historique:
        history = st.session_state['_iss_history']
        st.session_state['_iss_history'] = (history + [previous.copy()])[-30:]
    st.session_state['_iss_values'] = new_state.copy()


def enregistrer_modification(key):
    new_state = st.session_state['_iss_values'].copy()
    new_state[key] = st.session_state[key]
    if key.startswith('valeur_') and new_state['code_commune']:
        new_state['saisie_modifiee'] = True
    modifier_saisies(new_state)


def effacer_saisies():
    new_state = st.session_state['_iss_values'].copy()
    new_state['nom_commune'] = ''
    new_state['code_commune'] = ''
    new_state['saisie_modifiee'] = False
    for key in new_state:
        if key.startswith('valeur_'):
            new_state[key] = None
    modifier_saisies(new_state)


def annuler_modification():
    history = st.session_state['_iss_history']
    if history:
        previous = history[-1]
        st.session_state['_iss_history'] = history[:-1]
        modifier_saisies(previous, garder_historique=False)


def continuer_sans_sauvegarde():
    st.session_state['_iss_ready'] = True
    st.session_state['_iss_session_only'] = True


def initialiser_et_synchroniser():
    if '_iss_values' not in st.session_state:
        st.session_state['_iss_values'] = modele_saisies()[0]
        st.session_state['_iss_history'] = []
        st.session_state['_iss_ready'] = False
        st.session_state['_iss_nonce'] = uuid.uuid4().hex
        st.session_state['_iss_session_only'] = False
    ready = st.session_state['_iss_ready']
    result = composant_sauvegarde()(
        mode=('session' if st.session_state['_iss_session_only'] else 'save') if ready else 'load',
        nonce=st.session_state['_iss_nonce'],
        storage_key='iss_communal_idf_automatique_v1',
        payload={'schema':1, 'state':st.session_state['_iss_values'],
                 'history':st.session_state['_iss_history']} if ready else None,
        key='iss_browser_storage', default=None,
    )
    if not ready:
        if (isinstance(result, dict) and result.get('kind') == 'loaded'
                and result.get('nonce') == st.session_state['_iss_nonce']):
            saved = result.get('saved')
            if isinstance(saved, dict) and saved.get('schema') == 1:
                st.session_state['_iss_values'] = valider_saisies(saved.get('state'))
                history = saved.get('history', [])
                if isinstance(history, list):
                    st.session_state['_iss_history'] = [
                        valider_saisies(item) for item in history[-30:] if isinstance(item, dict)
                    ]
            if result.get('error'):
                st.session_state['_iss_storage_notice'] = result['error']
            st.session_state['_iss_ready'] = True
            st.rerun()
        st.info('Restauration des dernières saisies…')
        st.button('Continuer sans sauvegarde', on_click=continuer_sans_sauvegarde)
        st.stop()
    if st.session_state.get('_iss_storage_notice'):
        st.warning(st.session_state.pop('_iss_storage_notice'))
    # Le modèle indépendant des widgets conserve aussi les valeurs masquées.
    # Restaurer avant de créer les widgets, jamais après leur instanciation.
    for key, value in st.session_state['_iss_values'].items():
        st.session_state[key] = value


# ─────────────────────────────────────────────
# EN-TÊTE
# ─────────────────────────────────────────────

st.markdown('<div class="main-title">📊 Indicateur Socio-Économique communal</div>', unsafe_allow_html=True)
initialiser_et_synchroniser()
st.text_input(
    "Nom de la commune",
    placeholder="Ex. : Alfortville ou 94002",
    key='nom_commune',
    on_change=enregistrer_nom_commune,
)
st.caption("Tapez le nom d'une commune ou son code INSEE, puis validez avec Entrée.")
code_commune = st.session_state['_iss_values']['code_commune']
nom_commune = st.session_state['_iss_values']['nom_commune']
if code_commune:
    st.success(f"Données chargées pour {libelle_commune(code_commune)}.")
    if st.session_state['_iss_values']['saisie_modifiee']:
        st.info("Certaines valeurs ont été modifiées manuellement. Vous pouvez recharger les données de la commune.")
    st.button("Recharger les données de la commune", on_click=recharger_commune)
elif nom_commune.strip():
    correspondances = trouver_communes(nom_commune)
    if correspondances:
        st.selectbox(
            "Choisir la commune", options=correspondances, index=None,
            format_func=libelle_commune, placeholder="Sélectionnez une commune",
            key='_iss_commune_choice', on_change=choisir_commune,
        )
    else:
        st.warning("Aucune commune d'Île-de-France ne correspond à cette saisie.")
else:
    st.info("Saisissez une commune pour charger ses valeurs et calculer son score automatiquement.")

col_effacer, col_annuler = st.columns(2)
with col_effacer:
    st.button("Effacer toutes les saisies", on_click=effacer_saisies,
              disabled=(not st.session_state['_iss_values']['nom_commune']
                        and all(v is None for k, v in st.session_state['_iss_values'].items()
                                if k.startswith('valeur_'))))
with col_annuler:
    st.button("Annuler la dernière modification", on_click=annuler_modification,
              disabled=not st.session_state['_iss_history'])

# ─────────────────────────────────────────────
# NOTE MÉTHODOLOGIQUE
# ─────────────────────────────────────────────

with st.expander("ℹ️ Comment fonctionne cet outil ?", expanded=False):
    pass

with st.expander("📋 Informations sur les variables", expanded=False):
    df_all = tableau_variables()
    for colonne in ["Min réel", "Max réel"]:
        df_all[colonne] = df_all[colonne].map(fmt_val)
    st.dataframe(df_all, use_container_width=True, height=340)

# ─────────────────────────────────────────────
# SIDEBAR : poids dimensions
# ─────────────────────────────────────────────

with st.sidebar:
    st.header("⚖️ Poids des dimensions")
    st.caption("Ajustez l'importance de chaque dimension dans le score final (0 = ignorée, 5 = très importante).")

# ─────────────────────────────────────────────
# ÉTAPE 1 : CHOIX DES DIMENSIONS
# ─────────────────────────────────────────────

st.markdown("---")
st.markdown("### <span class='step-pill'>1</span> Dimensions à inclure", unsafe_allow_html=True)
st.caption("Cochez les grandes thématiques que vous souhaitez intégrer à l'indicateur.")

dimensions_disponibles = list(DIMENSIONS.keys())
dimensions_choisies = []

cols = st.columns(4)
for i, nom_dimension in enumerate(dimensions_disponibles):
    emoji = DIMENSIONS[nom_dimension]["emoji"]
    with cols[i % 4]:
        actif = st.checkbox(
            label=f"{emoji} {nom_dimension}",
            key=f"choix_dimension_{nom_dimension}",
            on_change=enregistrer_modification,
            args=(f"choix_dimension_{nom_dimension}",),
        )
        if actif:
            dimensions_choisies.append(nom_dimension)

if len(dimensions_choisies) == 0:
    st.warning("⚠️ Vous devez choisir au moins une dimension pour calculer l'indicateur.")
    st.stop()

# ─────────────────────────────────────────────
# SIDEBAR : sliders poids dimensions
# ─────────────────────────────────────────────

poids_dimensions = {}
with st.sidebar:
    for nom_dimension in dimensions_choisies:
        emoji = DIMENSIONS[nom_dimension]["emoji"]
        poids_dimensions[nom_dimension] = st.slider(
            label=f"{emoji} {nom_dimension}",
            min_value=0.0,
            max_value=5.0,
            step=0.5,
            key=f"poids_dimension_{nom_dimension}",
            on_change=enregistrer_modification,
            args=(f"poids_dimension_{nom_dimension}",),
        )

# ─────────────────────────────────────────────
# ÉTAPE 2 : CHOIX DES VARIABLES ET VALEURS
# ─────────────────────────────────────────────

st.markdown("---")
st.markdown("### <span class='step-pill'>2</span> Variables et valeurs observées", unsafe_allow_html=True)
st.caption("Les valeurs de la commune sont chargées automatiquement. Vous pouvez sélectionner les variables, ajuster les pondérations et modifier les valeurs pour explorer leur effet.")

variables_choisies = {}
valeurs = {}
poids_variables = {}
variables_non_renseignees = []

tabs = st.tabs([f"{DIMENSIONS[d]['emoji']} {d}" for d in dimensions_choisies])

for tab, nom_dimension in zip(tabs, dimensions_choisies):
    with tab:
        contenu_dimension = DIMENSIONS[nom_dimension]
        st.markdown(f'<div class="dim-desc">{contenu_dimension["description"]}</div>', unsafe_allow_html=True)

        variables_choisies[nom_dimension] = []

        for nom_variable, infos in contenu_dimension["variables"].items():

            unite = infos.get("unite", "")
            unite_label = f" ({unite})" if unite else ""
            p5 = infos["min"]
            p95 = infos["max"]
            min_reel = infos.get("min_reel", p5)
            max_reel = infos.get("max_reel", p95)
            commune_min = infos.get("commune_min", "")
            commune_max = infos.get("commune_max", "")

            p5_fmt = fmt_val(p5)
            p95_fmt = fmt_val(p95)
            min_reel_fmt = fmt_val(min_reel)
            max_reel_fmt = fmt_val(max_reel)

            has_reel = (min_reel != p5 or max_reel != p95)

            texte_p5, texte_p95, texte_reel = explication_borne(
                nom_variable, p5, p95, unite, min_reel, max_reel, commune_min, commune_max
            )

            col_check, col_info = st.columns([0.05, 0.95])

            with col_check:
                actif = st.checkbox(
                    label=f"Retenir {nom_variable}",
                    key=f"actif_{nom_dimension}_{nom_variable}",
                    on_change=enregistrer_modification,
                    args=(f"actif_{nom_dimension}_{nom_variable}",),
                    label_visibility="collapsed"
                )

            with col_info:
                # Bornes réelles (si différentes des P5/P95)
                # L'explication des valeurs extrêmes est conservée en infobulle au survol
                # de "Min réel" et "Max réel", afin d'alléger l'affichage principal.
                reel_html = ""
                if has_reel:
                    tooltip_reel = attr_html(texte_reel)
                    reel_html = (
                        f'<span class="borne-sep">|</span>'
                        f'<div class="borne-group">'
                        f'  <span class="borne-block borne-reel-block" title="{tooltip_reel}">'
                        f'    <span class="borne-reel-label">Min réel</span>'
                        f'    <span class="borne-reel-val">{min_reel_fmt}{unite_label}</span>'
                        f'  </span>'
                        f'  <span class="borne-block borne-reel-block" title="{tooltip_reel}">'
                        f'    <span class="borne-reel-label">Max réel</span>'
                        f'    <span class="borne-reel-val">{max_reel_fmt}{unite_label}</span>'
                        f'  </span>'
                        f'</div>'
                    )

                st.markdown(
                    f'<div class="var-name">{nom_variable}</div>'
                    f'<div class="bornes-wrap">'
                    f'  <div class="borne-group">'
                    f'    <span class="borne-block borne-p5-block">'
                    f'      <span class="borne-label">Borne minimale P5</span>'
                    f'      <span class="borne-val">{p5_fmt}{unite_label}</span>'
                    f'    </span>'
                    f'    <div class="borne-expl">{texte_p5}</div>'
                    f'  </div>'
                    f'  <div class="borne-arrow">→</div>'
                    f'  <div class="borne-group">'
                    f'    <span class="borne-block borne-p95-block">'
                    f'      <span class="borne-label">Borne maximale P95</span>'
                    f'      <span class="borne-val">{p95_fmt}{unite_label}</span>'
                    f'    </span>'
                    f'    <div class="borne-expl">{texte_p95}</div>'
                    f'  </div>'
                    f'  {reel_html}'
                    f'</div>',
                    unsafe_allow_html=True
                )

            if actif:

                col_val, col_poids = st.columns([2, 1])

                with col_val:
                    step = 0.1 if isinstance(min_reel, float) or isinstance(max_reel, float) else 1.0
                    fmt_input = "%.1f" if step == 0.1 else "%.0f"

                    valeur_saisie = st.number_input(
                        label=f"Valeur observée{unite_label}",
                        min_value=float(min_reel),
                        max_value=float(max_reel),
                        value=None,
                        placeholder="À renseigner",
                        step=float(step),
                        format=fmt_input,
                        key=f"valeur_{nom_dimension}_{nom_variable}",
                        on_change=enregistrer_modification,
                        args=(f"valeur_{nom_dimension}_{nom_variable}",),
                    )
                    if valeur_saisie is None:
                        variables_non_renseignees.append(nom_variable)
                        if code_commune:
                            st.caption("Donnée communale indisponible — exclue du calcul.")
                        else:
                            st.caption("Non renseignée — exclue du calcul.")
                    else:
                        valeurs[nom_variable] = valeur_saisie
                        variables_choisies[nom_dimension].append(nom_variable)

                    # Alerte rouge si valeur hors bornes P5/P95
                    if valeur_saisie is not None and (valeur_saisie < p5 or valeur_saisie > p95):
                        st.markdown(
                            f'<div class="alerte-extreme">⚠️ Valeur extrême — en dehors des bornes par percentiles '
                            f'(borne min P5 = {p5_fmt}{unite_label}, borne max P95 = {p95_fmt}{unite_label})</div>',
                            unsafe_allow_html=True
                        )

                with col_poids:
                    poids_variables[nom_variable] = st.slider(
                        label="Poids",
                        min_value=0.0,
                        max_value=5.0,
                        step=0.5,
                        key=f"poids_variable_{nom_dimension}_{nom_variable}",
                        on_change=enregistrer_modification,
                        args=(f"poids_variable_{nom_dimension}_{nom_variable}",),
                    )
            else:
                st.caption("_Variable exclue du calcul._")

            st.divider()

# ─────────────────────────────────────────────
# VÉRIFICATION
# ─────────────────────────────────────────────

nombre_variables_retenues = sum(len(v) for v in variables_choisies.values())

if nombre_variables_retenues == 0:
    st.info("Sélectionnez et renseignez au moins une variable pour calculer l’indicateur.")
    st.stop()

# ─────────────────────────────────────────────
# CALCUL
# ─────────────────────────────────────────────

if variables_non_renseignees:
    st.warning(
        f"Résultat partiel : {len(variables_non_renseignees)} variable(s) sélectionnée(s) "
        "non renseignée(s), exclue(s) du calcul : " + ", ".join(variables_non_renseignees)
    )

resultats_variables, scores_dimensions, indicateur_global = calculer_indicateur(
    dimensions_choisies=dimensions_choisies,
    variables_choisies=variables_choisies,
    valeurs=valeurs,
    poids_variables=poids_variables,
    poids_dimensions=poids_dimensions
)

df_resultats = pd.DataFrame(resultats_variables)

# ─────────────────────────────────────────────
# ÉTAPE 3 : RÉSULTATS
# ─────────────────────────────────────────────

st.markdown("---")
st.markdown("### <span class='step-pill'>3</span> Résultats", unsafe_allow_html=True)
if code_commune:
    st.markdown(
        f'<div class="subtitle">{html.escape(BASE_COMMUNALE["communes"][code_commune]["name"])} '
        f'· code INSEE {code_commune}</div>', unsafe_allow_html=True,
    )

col_score, col_bars, col_radar = st.columns([1, 1.4, 2])

with col_score:
    couleur_score = "#16a34a" if indicateur_global >= 0.6 else ("#d97706" if indicateur_global >= 0.35 else "#dc2626")
    st.markdown(f"""
    <div class="score-card" style="background: linear-gradient(135deg, #12203f 0%, {couleur_score} 100%);">
        <div class="score-label">Score global</div>
        <div class="score-value">{indicateur_global * 100:.1f}</div>
        <div class="score-sub">sur 100 points</div>
    </div>
    """, unsafe_allow_html=True)
    st.caption(f"Basé sur **{nombre_variables_retenues} variable(s)** répartie(s) en **{len(scores_dimensions)} dimension(s)**.")

with col_bars:
    st.markdown("**Scores par dimension**")
    for dim, score in scores_dimensions.items():
        pct = score * 100
        emoji = DIMENSIONS[dim]["emoji"]
        st.markdown(f"""
        <div class="dim-score-row">
            <div class="dim-score-name">{emoji} {dim}</div>
            <div class="dim-score-bar-wrap">
                <div class="dim-score-bar" style="width:{pct:.1f}%"></div>
            </div>
            <div class="dim-score-val">{pct:.0f}</div>
        </div>
        """, unsafe_allow_html=True)

with col_radar:
    fig_radar = creer_radar(scores_dimensions)
    st.plotly_chart(fig_radar, use_container_width=True)

# ─────────────────────────────────────────────
# DÉTAIL DES VARIABLES
# ─────────────────────────────────────────────

with st.expander("🔍 Détail du calcul par variable", expanded=False):
    st.caption("Ce tableau montre les variables retenues, leurs bornes P5/P95, poids et score calculé. **Cliquez sur une ligne** pour afficher le détail pédagogique du calcul.")

    # Formatage propre des colonnes numériques
    df_affichage = df_resultats[[
        "Dimension", "Variable", "Valeur saisie", "Unité",
        "P5", "P95",
        "Hors bornes P5-P95",
        "Poids variable", "Score normalisé 0-100", "Source"
    ]].copy()

    for col in ["Valeur saisie", "P5", "P95", "Poids variable", "Score normalisé 0-100"]:
        df_affichage[col] = df_affichage[col].apply(fmt_val)

    selection = st.dataframe(
        df_affichage.style.highlight_between(
            subset=["Valeur saisie"],
            color="#fef9c3"
        ),
        use_container_width=True,
        on_select="rerun",
        selection_mode="single-row",
        key="detail_selection"
    )

    # ── Panneau pédagogique déclenché par la sélection ──
    lignes_sel = selection.selection.get("rows", [])
    if lignes_sel and 0 <= lignes_sel[0] < len(df_resultats):
        idx = lignes_sel[0]
        row = df_resultats.iloc[idx]

        valeur    = row["Valeur saisie"]
        p5        = row["P5"]
        p95       = row["P95"]
        sens      = row["Sens"]
        unite     = row["Unité"]
        score_100 = row["Score normalisé 0-100"]
        variable  = row["Variable"]
        hors      = row["Hors bornes P5-P95"] == "⚠️ Oui"

        u = f" {unite}" if unite else ""
        v_fmt   = fmt_val(valeur)
        p5_fmt  = fmt_val(p5)
        p95_fmt = fmt_val(p95)
        s_fmt   = fmt_val(score_100)

        # Calculs intermédiaires
        amplitude = p95 - p5
        if sens == "positif":
            numerateur = valeur - p5
            formule_gauche = "x - P5"
        else:
            numerateur = p95 - valeur
            formule_gauche = "P95 - x"

        ratio_brut = numerateur / amplitude if amplitude != 0 else 0
        ratio_clamp = max(0.0, min(1.0, ratio_brut))
        score_01 = round(ratio_clamp, 4)

        # Texte sens
        if sens == "positif":
            sens_expl = "**variable favorable** : plus la valeur est élevée, plus le score est élevé."
            application = f"({v_fmt}{u} − {p5_fmt}{u}) ÷ ({p95_fmt}{u} − {p5_fmt}{u})"
        else:
            sens_expl = "**variable défavorable** : plus la valeur est élevée, plus le score est bas (formule inversée)."
            application = f"({p95_fmt}{u} − {v_fmt}{u}) ÷ ({p95_fmt}{u} − {p5_fmt}{u})"

        # Alerte hors bornes
        alerte_hors = ""
        if hors:
            cote = "100" if ratio_brut > 1 else "0"
            alerte_hors = f"\n\n> ⚠️ **Valeur hors bornes P5/P95** — la valeur {v_fmt}{u} est en dehors de l'intervalle [{p5_fmt}{u} ; {p95_fmt}{u}]. Le ratio brut ({round(ratio_brut, 4)}) est plafonné à {'1' if ratio_brut > 1 else '0'}, soit un score final de **{cote}/100**."

        st.markdown("---")
        st.markdown(f"#### 🧮 Calcul détaillé — *{variable}*")

        col_calc, col_schema = st.columns([1.3, 0.7])

        with col_calc:
            st.markdown(f"""
**1. Type de variable :** {sens_expl}

**2. Formule de normalisation :**
""")
            if sens == "positif":
                st.latex(r"\text{score} = \frac{x - P5}{P95 - P5} \times 100")
            else:
                st.latex(r"\text{score} = \frac{P95 - x}{P95 - P5} \times 100")
            st.markdown(f"""
**3. Application numérique :**

| Élément | Valeur |
|---|---|
| Valeur observée (x) | **{v_fmt}{u}** |
| Borne minimale P5 | {p5_fmt}{u} |
| Borne maximale P95 | {p95_fmt}{u} |
| Amplitude (P95 − P5) | {fmt_val(amplitude)}{u} |
| = {application} | = **{round(ratio_brut, 4)}** |
| Après plafonnement [0 ; 1] | **{score_01}** |
| **Score final (× 100)** | **{s_fmt} / 100** |
{alerte_hors}
""")

        with col_schema:
            pct_display = min(100, max(0, score_100))
            couleur_jauge = "#16a34a" if pct_display >= 60 else ("#d97706" if pct_display >= 35 else "#dc2626")
            sens_icon = "🔼 Variable favorable" if sens == "positif" else "🔽 Variable défavorable"
            st.markdown(f"""
<div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:12px;padding:20px;text-align:center;">
  <div style="font-size:0.78rem;font-weight:600;color:#64748b;text-transform:uppercase;letter-spacing:0.06em;margin-bottom:8px;">Score normalisé</div>
  <div style="font-size:2.8rem;font-weight:700;color:{couleur_jauge};line-height:1;">{s_fmt}</div>
  <div style="font-size:0.8rem;color:#94a3b8;margin-bottom:14px;">sur 100</div>
  <div style="background:#e2e8f0;border-radius:999px;height:12px;overflow:hidden;">
    <div style="width:{pct_display:.1f}%;height:12px;border-radius:999px;background:{couleur_jauge};"></div>
  </div>
  <div style="font-size:0.75rem;color:#64748b;margin-top:10px;">{sens_icon}</div>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# EXPORT
# ─────────────────────────────────────────────

with st.expander("📥 Exporter les résultats", expanded=False):
    df_export = df_resultats.copy()
    df_export.insert(0, "Code INSEE", code_commune)
    df_export.insert(1, "Commune", nom_commune)
    df_export.insert(2, "Valeurs modifiées manuellement", st.session_state['_iss_values']['saisie_modifiee'])
    df_export.insert(3, "Variables non renseignées", ", ".join(variables_non_renseignees))
    csv_resultats = df_export.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="📥 Télécharger en CSV",
        data=csv_resultats,
        file_name="resultats_indicateur_socio_economique.csv",
        mime="text/csv"
    )

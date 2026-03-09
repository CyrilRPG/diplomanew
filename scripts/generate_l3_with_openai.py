#!/usr/bin/env python3
"""
Génère des flashcards L3 (UPEC LSPS3 S2) via l'API OpenAI pour:
- Biotechnologie
- Technique de vie et société
- Santé publique (Promotion/Prévention, Économie de la santé, Géographie, Gestion de projet RC)

ATTENTION:
- Ne mets PAS ta clé dans ce fichier.
- Avant d'exécuter:
    export OPENAI_API_KEY="TA_CLE_ICI"

Usage:
    cd ~/Desktop/diploma
    python3 scripts/generate_l3_with_openai.py
"""

import json
import os
from pathlib import Path

from openai import OpenAI  # pip install openai

BASE_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = BASE_DIR / "UPEC_LSPS3_S2"

# Client OpenAI (utilise OPENAI_API_KEY dans l'environnement)
if not os.environ.get("OPENAI_API_KEY"):
    raise SystemExit("OPENAI_API_KEY non défini. Fais: export OPENAI_API_KEY='ta_cle'")
client = OpenAI()

from generate_upec_lsps3_s2 import (  # type: ignore
    build_course_html_lsps3,
    build_menu_html,
    json_to_js_data,
)


COURSES = [
    # Biotechnologie
    ("Biotechnologie", "Biotechnologie", "Biotechnologie/fc1.html", "Introduction à la biotechnologie"),
    ("Biotechnologie", "Biotechnologie", "Biotechnologie/fc2.html", "Reprogrammation cellulaire"),
    ("Biotechnologie", "Biotechnologie", "Biotechnologie/fc3.html", "Drug Repositioning"),
    ("Biotechnologie", "Biotechnologie", "Biotechnologie/fc4.html", "Immunothérapie"),
    ("Biotechnologie", "Biotechnologie", "Biotechnologie/fc5.html", "Principes généraux de la thérapie génique"),
    ("Biotechnologie", "Biotechnologie", "Biotechnologie/fc6.html", "Les vésicules extracellulaires"),
    ("Biotechnologie", "Biotechnologie", "Biotechnologie/fc7.html", "Bioproduction de cellules souches"),
    ("Biotechnologie", "Biotechnologie", "Biotechnologie/fc8.html", "Stratégies vaccinales"),
    ("Biotechnologie", "Biotechnologie", "Biotechnologie/fc9.html", "Édition du génome"),
    ("Biotechnologie", "Biotechnologie", "Biotechnologie/fc10.html", "Biomécanique des biomatériaux"),
    ("Biotechnologie", "Biotechnologie", "Biotechnologie/fc11.html", "Thérapie cellulaire et moelle osseuse"),
    ("Biotechnologie", "Biotechnologie", "Biotechnologie/fc12.html", "Peptides thérapeutiques antimicrobiens"),

    # Technique de vie et société
    ("Technique_Vie_Societe", "Technique de vie et société", "Technique_Vie_Societe/fc1.html", "Vie, technique et société - Introduction"),
    ("Technique_Vie_Societe", "Technique de vie et société", "Technique_Vie_Societe/fc2.html", "L'éthique à l'heure de la civilisation technologique"),
    ("Technique_Vie_Societe", "Technique de vie et société", "Technique_Vie_Societe/fc3.html", "Statut des objets techniques dans le champ de la santé"),
    ("Technique_Vie_Societe", "Technique de vie et société", "Technique_Vie_Societe/fc4.html", "Droits et devoirs des patients et des praticiens"),
    ("Technique_Vie_Societe", "Technique de vie et société", "Technique_Vie_Societe/fc5.html", "Droit à l'information médicale"),
    ("Technique_Vie_Societe", "Technique de vie et société", "Technique_Vie_Societe/fc6.html", "Bio-objets et enjeux juridiques"),
    ("Technique_Vie_Societe", "Technique de vie et société", "Technique_Vie_Societe/fc7.html", "Pensée des bio-objets (Céline Lafontaine)"),
    ("Technique_Vie_Societe", "Technique de vie et société", "Technique_Vie_Societe/fc8.html", "Technicisation médicale et déshumanisation"),
    ("Technique_Vie_Societe", "Technique de vie et société", "Technique_Vie_Societe/fc9.html", "Médecine humaniste vs biomédecine"),
    ("Technique_Vie_Societe", "Technique de vie et société", "Technique_Vie_Societe/fc10.html", "Médecines alternatives"),
    ("Technique_Vie_Societe", "Technique de vie et société", "Technique_Vie_Societe/fc11.html", "Modèle biopsychosocial"),

    # Santé Publique – Promotion / Prévention
    ("SP_Promotion_Prevention", "Santé publique - Promotion et prévention", "SP_Promotion_Prevention/fc1.html", "Généralités en santé publique"),
    ("SP_Promotion_Prevention", "Santé publique - Promotion et prévention", "SP_Promotion_Prevention/fc2.html", "Méthodologie de projet en prévention et promotion de la santé"),
    ("SP_Promotion_Prevention", "Santé publique - Promotion et prévention", "SP_Promotion_Prevention/fc3.html", "Déterminants de santé"),
    ("SP_Promotion_Prevention", "Santé publique - Promotion et prévention", "SP_Promotion_Prevention/fc4.html", "Méthodes de prévention et de dépistage"),
    ("SP_Promotion_Prevention", "Santé publique - Promotion et prévention", "SP_Promotion_Prevention/fc5.html", "Vaccins et promotion de la prévention"),
    ("SP_Promotion_Prevention", "Santé publique - Promotion et prévention", "SP_Promotion_Prevention/fc6.html", "Maladies sexuellement transmissibles"),
    ("SP_Promotion_Prevention", "Santé publique - Promotion et prévention", "SP_Promotion_Prevention/fc7.html", "Initiation aux soins d’urgence"),
    ("SP_Promotion_Prevention", "Santé publique - Promotion et prévention", "SP_Promotion_Prevention/fc8.html", "Sédentarité et activité physique"),
    ("SP_Promotion_Prevention", "Santé publique - Promotion et prévention", "SP_Promotion_Prevention/fc9.html", "Risque cardio-vasculaire"),

    # Santé Publique – Économie de la santé
    ("SP_Economie_Sante", "Santé publique - Économie de la santé", "SP_Economie_Sante/fc1.html", "Analyse économique de la perte d’autonomie (dépendance)"),
    ("SP_Economie_Sante", "Santé publique - Économie de la santé", "SP_Economie_Sante/fc2.html", "Analyse de la perte d’autonomie : handicap"),
    ("SP_Economie_Sante", "Santé publique - Économie de la santé", "SP_Economie_Sante/fc3.html", "Modes de rémunération des médecins libéraux"),
    ("SP_Economie_Sante", "Santé publique - Économie de la santé", "SP_Economie_Sante/fc4.html", "Modes de rémunération des établissements de santé"),
    ("SP_Economie_Sante", "Santé publique - Économie de la santé", "SP_Economie_Sante/fc5.html", "Nutrition, santé et croissance économique"),
    ("SP_Economie_Sante", "Santé publique - Économie de la santé", "SP_Economie_Sante/fc6.html", "Santé et pauvreté"),
    ("SP_Economie_Sante", "Santé publique - Économie de la santé", "SP_Economie_Sante/fc7.html", "Santé, système de santé et égalité"),
    ("SP_Economie_Sante", "Santé publique - Économie de la santé", "SP_Economie_Sante/fc8.html", "Santé et environnement"),

    # Santé Publique – Géographie de la santé
    ("SP_Geographie_Sante", "Santé publique - Géographie de la santé", "SP_Geographie_Sante/fc1.html", "Histoire et concepts de la géographie de la santé"),
    ("SP_Geographie_Sante", "Santé publique - Géographie de la santé", "SP_Geographie_Sante/fc2.html", "Liens villes et santé"),
    ("SP_Geographie_Sante", "Santé publique - Géographie de la santé", "SP_Geographie_Sante/fc3.html", "Inégalités spatiales de l’offre de soins en France"),
    ("SP_Geographie_Sante", "Santé publique - Géographie de la santé", "SP_Geographie_Sante/fc4.html", "Inégalités internationales d’offre de soins"),
    ("SP_Geographie_Sante", "Santé publique - Géographie de la santé", "SP_Geographie_Sante/fc5.html", "Point de vue des patient.es"),
    ("SP_Geographie_Sante", "Santé publique - Géographie de la santé", "SP_Geographie_Sante/fc6.html", "Accès aux soins des personnes vulnérables"),
    ("SP_Geographie_Sante", "Santé publique - Géographie de la santé", "SP_Geographie_Sante/fc7.html", "Alimentation et santé en ville"),
    ("SP_Geographie_Sante", "Santé publique - Géographie de la santé", "SP_Geographie_Sante/fc8.html", "Espaces verts et santé"),
    ("SP_Geographie_Sante", "Santé publique - Géographie de la santé", "SP_Geographie_Sante/fc9.html", "Urbanisme et santé des personnes âgées"),
    ("SP_Geographie_Sante", "Santé publique - Géographie de la santé", "SP_Geographie_Sante/fc10.html", "Urbanisme et santé des enfants"),

    # Santé Publique – Gestion de projet de recherche clinique
    ("SP_Gestion_Projet_RC", "Santé publique - Gestion de projet de recherche clinique", "SP_Gestion_Projet_RC/fc1.html", "Généralités sur les essais cliniques"),
    ("SP_Gestion_Projet_RC", "Santé publique - Gestion de projet de recherche clinique", "SP_Gestion_Projet_RC/fc2.html", "Acteurs de la recherche clinique"),
    ("SP_Gestion_Projet_RC", "Santé publique - Gestion de projet de recherche clinique", "SP_Gestion_Projet_RC/fc3.html", "Vigilance et gestion des EIG"),
    ("SP_Gestion_Projet_RC", "Santé publique - Gestion de projet de recherche clinique", "SP_Gestion_Projet_RC/fc4.html", "Structures de soutien à la recherche clinique"),
    ("SP_Gestion_Projet_RC", "Santé publique - Gestion de projet de recherche clinique", "SP_Gestion_Projet_RC/fc5.html", "Mise en place d’un essai clinique"),
    ("SP_Gestion_Projet_RC", "Santé publique - Gestion de projet de recherche clinique", "SP_Gestion_Projet_RC/fc6.html", "Dossier patient, CRF et bases de données"),
    ("SP_Gestion_Projet_RC", "Santé publique - Gestion de projet de recherche clinique", "SP_Gestion_Projet_RC/fc7.html", "Monitoring et gestion de projet"),
    ("SP_Gestion_Projet_RC", "Santé publique - Gestion de projet de recherche clinique", "SP_Gestion_Projet_RC/fc8.html", "Réglementation sur les échantillons biologiques"),
    ("SP_Gestion_Projet_RC", "Santé publique - Gestion de projet de recherche clinique", "SP_Gestion_Projet_RC/fc9.html", "Démarches auprès du MESRI"),
]


SYSTEM_PROMPT = (
    "Tu es un expert en pédagogie en santé (niveau L3). "
    "Pour chaque cours, tu génères EXACTEMENT 100 flashcards distinctes, utiles à la mémorisation. "
    "Sortie STRICTEMENT en JSON: un objet avec un champ 'cards' qui est une liste de 100 objets "
    '{"question": "...", "answer": "..."}. '
    "Pas de méta-questions (pas de 'plan du cours', pas de 'résume le cours', pas de questions sur le professeur). "
    "Chaque question teste un point de contenu différent ou une nuance différente."
)


def generate_flashcards_for_course(course_title: str) -> list[dict]:
    """Appelle le modèle OpenAI pour générer 100 Q/R pour un cours donné."""
    user_prompt = (
        f"Cours de Licence 3 santé: «{course_title}».\n"
        "Génère 100 flashcards Q/R courtes et précises pour réviser ce cours. "
        "Concentre-toi sur les définitions, mécanismes, indications, contre-indications, exemples concrets, "
        "chiffres/ordres de grandeur importants et grandes notions à retenir. "
        "Évite les questions trop générales ou floues."
    )
    resp = client.chat.completions.create(
        # Adapte le modèle à ce que ton compte supporte (ex: gpt-4.1, gpt-4.1-mini, etc.)
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.4,
    )
    content = resp.choices[0].message.content or ""

    # Parsing robuste: accepte soit une liste brute, soit {"cards": [...]}
    def parse_cards(raw: str) -> list[dict]:
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            # Essaye d'extraire juste le bloc JSON principal
            start = raw.find("{")
            end = raw.rfind("}")
            if start != -1 and end != -1 and end > start:
                data = json.loads(raw[start : end + 1])
            else:
                raise

        if isinstance(data, dict) and isinstance(data.get("cards"), list):
            return data["cards"]
        if isinstance(data, list):
            return data
        raise ValueError("Format JSON inattendu (ni liste, ni objet avec 'cards').")

    cards = parse_cards(content)
    if len(cards) < 80:
        raise ValueError(f"La réponse du modèle ne contient que {len(cards)} cartes (<80).")
    out: list[dict] = []
    for d in cards:
        q = str(d.get("question", "")).strip()
        a = str(d.get("answer", "")).strip()
        if not q or not a:
            continue
        out.append({"question": q, "answer": a})
    if len(out) < 80:
        raise ValueError(f"Seulement {len(out)} flashcards valides générées pour «{course_title}»")
    # On garde les 100 premières valides au cas où il y en aurait plus
    return out[:100]


def build_course_html(matiere_dir: str, matiere_display: str, course_title: str, items: list[dict]) -> str:
    flashcards_js = json_to_js_data(items)
    menu_html = build_menu_html("..")
    # Les cours L3 sont dans UPEC_LSPS3_S2/<matiere>/fcX.html → assets deux niveaux au-dessus
    return build_course_html_lsps3(
        matiere_dir, matiere_display, course_title, flashcards_js, menu_html, asset_prefix="../../"
    )


def main():
    for matiere_dir, matiere_display, rel_path, course_title in COURSES:
        out_path = OUT_DIR / rel_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"=== Génération GPT pour {rel_path} ({course_title}) ===")
        items = generate_flashcards_for_course(course_title)
        html = build_course_html(matiere_dir, matiere_display, course_title, items)
        out_path.write_text(html, encoding="utf-8")
        print(f"OK → {rel_path} ({len(items)} flashcards)")


if __name__ == "__main__":
    main()


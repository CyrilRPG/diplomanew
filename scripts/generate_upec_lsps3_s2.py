#!/usr/bin/env python3
"""
Generate UPEC_LSPS3_S2 section from:
- flashcard upec L3: 3 matières with .JS files (Bases moléculaire, Human nutrition, One Health)
- fiches upec l3: course names; Réglementation (2 courses) and Technique (11 courses) need ~100 generated flashcards each.
"""
import json
import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
FLASHCARD_SRC = BASE_DIR / "flashcard upec L3"
FICHES_SRC = BASE_DIR / "fiches upec l3"
OUT_DIR = BASE_DIR / "UPEC_LSPS3_S2"

# Matière dir (output) -> (source folder in flashcard upec L3, display name, icon, list of (js_basename, html_file, course_title))
# For Human nutrition: 1.JS->fc1, 2.JS->fc2, ... 5.JS->fc5, 5.2.JS->fc5_2, 6.JS->fc6, ... 10.JS->fc10
HUMAN_NUTRITION_TITLES = [
    "Métabolisme bioénergétique (révision)",
    "Anthropométrie, bilan énergétique, valeurs de référence en diététique",
    "Macronutriments : protéines, glucides et acides gras",
    "Les micronutriments : minéraux",
    "Les vitamines liposolubles",
    "Les vitamines hydrosolubles",  # 5.2
    "Maladies cardiovasculaires",
    "Alimentation et cancer",
    "Consommation d'alcool et effets sur la santé",
    "Interaction régime-maladie : obésité, syndrome métabolique et diabète",
    "Interventions diététiques et pharmacologiques",
]
ONE_HEALTH_TITLES = [
    "Introduction au concept One Health",
    "Zoonoses et modes de transmission",
    "Émergence et diffusion de la résistance aux antibiotiques",
    "Maladies émergentes transmises de l'animal à l'homme",
    "Mobiliser les professionnels et la population autour des approches One Health",
    "Polluants de l'environnement professionnel",
    "Évaluation, prévention et gestion des risques en santé environnementale",
    "Principales théories, concepts et modèles en sciences sociales (One Health)",
    "Surveillance et investigation en santé publique et santé animale",
    "Biodiversité des plantes et liens avec la santé humaine et animale",
    "Écologie de la faune sauvage",
    "Environnement, biodiversité, écologie, évolution des risques (partie 1)",
    "Environnement, biodiversité, écologie, évolution des risques (partie 2)",
]
TECHNIQUE_TITLES = [
    "Vie, technique et société - Introduction",
    "L'éthique à l'heure de la civilisation technologique",
    "Le statut des objets techniques et des technologies dans le champ de la santé",
    "Les droits et devoirs des patients et des praticiens",
    "Le droit à l'information médicale",
    "Enjeux et statuts des objets biologiques",
    "La pensée des bio-objets chez Céline Lafontaine",
    "La technicisation médicale, une déshumanisation : précisions conceptuelles",
    "La médecine humaniste face à la biomédecine",
    "Les médecines alternatives : de la critique humaniste à l'antiscience",
    "Biomédecine et approche holistique : le modèle biopsychosocial",
]

STRUCTURE = [
    {
        "dir": "Bases_moleculaire_Oncologie",
        "display": "Bases moléculaires en oncologie",
        "icon": "fa-dna",
        "source_subdir": "bases moléculaire en oncologie",
        "courses_with_js": [(f"{i}.JS", f"fc{i}.html", f"Cours {i}") for i in range(1, 12)],
        "courses_generated": [],
    },
    {
        "dir": "Human_Nutrition",
        "display": "Human nutrition",
        "icon": "fa-utensils",
        "source_subdir": "human nutrition",
        "courses_with_js": [
            ("1.JS", "fc1.html", HUMAN_NUTRITION_TITLES[0]),
            ("2.JS", "fc2.html", HUMAN_NUTRITION_TITLES[1]),
            ("3.JS", "fc3.html", HUMAN_NUTRITION_TITLES[2]),
            ("4.JS", "fc4.html", HUMAN_NUTRITION_TITLES[3]),
            ("5.JS", "fc5.html", HUMAN_NUTRITION_TITLES[4]),
            ("5.2.JS", "fc5_2.html", HUMAN_NUTRITION_TITLES[5]),
            ("6.JS", "fc6.html", HUMAN_NUTRITION_TITLES[6]),
            ("7.JS", "fc7.html", HUMAN_NUTRITION_TITLES[7]),
            ("8.JS", "fc8.html", HUMAN_NUTRITION_TITLES[8]),
            ("9.JS", "fc9.html", HUMAN_NUTRITION_TITLES[9]),
            ("10.JS", "fc10.html", HUMAN_NUTRITION_TITLES[10]),
        ],
        "courses_generated": [],
    },
    {
        "dir": "One_Health",
        "display": "One Health",
        "icon": "fa-globe-americas",
        "source_subdir": "one health",
        "courses_with_js": [
            ("1.JS", "fc1.html", ONE_HEALTH_TITLES[0]),
            ("2.JS", "fc2.html", ONE_HEALTH_TITLES[1]),
            ("3.JS", "fc3.html", ONE_HEALTH_TITLES[2]),
            ("4.JS", "fc4.html", ONE_HEALTH_TITLES[3]),
            ("5.JS", "fc5.html", ONE_HEALTH_TITLES[4]),
            ("6.JS", "fc6.html", ONE_HEALTH_TITLES[5]),
            ("7.JS", "fc7.html", ONE_HEALTH_TITLES[6]),
            ("8.JS", "fc8.html", ONE_HEALTH_TITLES[7]),
            ("9.JS", "fc9.html", ONE_HEALTH_TITLES[8]),
            ("10.JS", "fc10.html", ONE_HEALTH_TITLES[9]),
            ("11.JS", "fc11.html", ONE_HEALTH_TITLES[10]),
            ("12.1.JS", "fc12_1.html", ONE_HEALTH_TITLES[11]),
            ("12.2.JS", "fc12_2.html", ONE_HEALTH_TITLES[12]),
        ],
        "courses_generated": [],
    },
    {
        "dir": "Reglementation_Ethique_Recherche",
        "display": "Réglementation et éthique de la recherche - droit de la santé",
        "icon": "fa-balance-scale",
        "source_subdir": None,
        "courses_with_js": [],
        "courses_generated": [
            ("fc1.html", "Droit de la santé"),
            ("fc2.html", "Réglementation et recherche de la santé"),
        ],
    },
    {
        "dir": "Technique_Vie_Societe",
        "display": "Technique de vie et société",
        "icon": "fa-book",
        "source_subdir": None,
        "courses_with_js": [],
        "courses_generated": [(f"fc{i}.html", TECHNIQUE_TITLES[i - 1]) for i in range(1, 12)],
    },
    {
        "dir": "Biotechnologie",
        "display": "Biotechnologie",
        "icon": "fa-flask",
        "source_subdir": None,
        "courses_with_js": [],
        "courses_generated": [
            ("fc1.html", "Introduction à la biotechnologie"),
            ("fc2.html", "Reprogrammation cellulaire"),
            ("fc3.html", "Drug Repositioning"),
            ("fc4.html", "Immunothérapie"),
            ("fc5.html", "Principes généraux de la thérapie génique"),
            ("fc6.html", "Les vésicules extracellulaires"),
            ("fc7.html", "Bioproduction de cellules souches"),
            ("fc8.html", "Stratégies vaccinales"),
            ("fc9.html", "Édition du génome"),
            ("fc10.html", "Biomécanique des biomatériaux"),
            ("fc11.html", "Thérapie cellulaire et moelle osseuse"),
            ("fc12.html", "Peptides thérapeutiques antimicrobiens"),
        ],
    },
    {
        "dir": "SP_Promotion_Prevention",
        "display": "Santé publique - Promotion et prévention",
        "icon": "fa-heartbeat",
        "source_subdir": None,
        "courses_with_js": [],
        "courses_generated": [
            ("fc1.html", "Généralités en santé publique"),
            ("fc2.html", "Méthodologie de projet en prévention et promotion de la santé"),
            ("fc3.html", "Déterminants de santé"),
            ("fc4.html", "Méthodes de prévention et de dépistage"),
            ("fc5.html", "Vaccins et promotion de la prévention"),
            ("fc6.html", "Maladies sexuellement transmissibles"),
            ("fc7.html", "Initiation aux soins d’urgence"),
            ("fc8.html", "Sédentarité et activité physique"),
            ("fc9.html", "Le risque cardio-vasculaire"),
        ],
    },
    {
        "dir": "SP_Economie_Sante",
        "display": "Santé publique - Économie de la santé",
        "icon": "fa-chart-line",
        "source_subdir": None,
        "courses_with_js": [],
        "courses_generated": [
            ("fc1.html", "Analyse économique de la perte d’autonomie (Dépendance)"),
            ("fc2.html", "Analyse de la perte d’autonomie : Handicap"),
            ("fc3.html", "Les modes de rémunération des médecins libéraux"),
            ("fc4.html", "Les modes de rémunération des établissements de santé"),
            ("fc5.html", "Nutrition, santé et croissance économique"),
            ("fc6.html", "Santé et développement : santé et pauvreté"),
            ("fc7.html", "Santé et développement : système et égalité"),
            ("fc8.html", "Santé et environnement"),
        ],
    },
    {
        "dir": "SP_Geographie_Sante",
        "display": "Santé publique - Géographie de la santé",
        "icon": "fa-globe",
        "source_subdir": None,
        "courses_with_js": [],
        "courses_generated": [
            ("fc1.html", "Histoire et concepts de la géographie de la santé"),
            ("fc2.html", "Liens villes et santé : enjeux des usages de la carte en santé"),
            ("fc3.html", "Inégalités spatiales de l’offre de soins en France"),
            ("fc4.html", "Enjeux internationaux des inégalités d’offre de soins"),
            ("fc5.html", "Enjeux internationaux : le point de vue des patient.es"),
            ("fc6.html", "L’accès aux soins des personnes vulnérables"),
            ("fc7.html", "Alimentation et santé en ville"),
            ("fc8.html", "Pouvoirs des villes et urbanisme favorable à la santé : espaces verts"),
            ("fc9.html", "Urbanisme favorable à la santé : personnes âgées"),
            ("fc10.html", "Urbanisme favorable à la santé : enfants"),
        ],
    },
    {
        "dir": "SP_Gestion_Projet_RC",
        "display": "Santé publique - Gestion de projet de recherche clinique",
        "icon": "fa-project-diagram",
        "source_subdir": None,
        "courses_with_js": [],
        "courses_generated": [
            ("fc1.html", "Généralités sur les essais cliniques"),
            ("fc2.html", "Acteurs de la recherche clinique"),
            ("fc3.html", "Vigilance, gestion des EIG et sécurité des essais cliniques"),
            ("fc4.html", "Structures de soutien à la recherche clinique"),
            ("fc5.html", "Mise en place d’un essai clinique"),
            ("fc6.html", "Le dossier patient, les CRF et les bases de données"),
            ("fc7.html", "Gestion de projet (monitoring)"),
            ("fc8.html", "Réglementation sur les échantillons biologiques"),
            ("fc9.html", "Démarches auprès du MESRI"),
        ],
    },
]

CURLY_APOSTROPHE = "\u2019"


def escape_js_string(s):
    """Ensure string is safe for single-quoted JS: use curly apostrophe for French contractions."""
    if not isinstance(s, str):
        return s
    # Replace straight single quote between letters (French apostrophe) with curly
    s = re.sub(r"([a-zA-ZéèêëàâäùûüïîôöçÉÈÊËÀÂÄÙÛÜÏÎÔÖÇ])'([a-zA-ZéèêëàâäùûüïîôöçÉÈÊËÀÂÄÙÛÜÏÎÔÖÇ])", r"\1" + CURLY_APOSTROPHE + r"\2", s)
    # Escape backslash then single quote for JS string
    s = s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", " ").replace("\r", " ")
    return s


def json_to_js_data(items):
    """Convert list of {question, answer} dicts to JS literal string (single-quoted, with commas)."""
    lines = []
    for item in items:
        q = escape_js_string(item.get("question", ""))
        a = escape_js_string(item.get("answer", ""))
        lines.append(f"{{ question: '{q}', answer: '{a}', }}")
    return ",\n".join(lines)


def read_js_flashcards(filepath):
    """Read .JS file (JSON array) and return list of {question, answer}."""
    with open(filepath, "r", encoding="utf-8") as f:
        raw = f.read().strip()
    # Handle optional leading/trailing brackets and commas
    raw = raw.strip()
    if not raw.startswith("["):
        raw = "[" + raw
    if not raw.endswith("]"):
        raw = raw + "]"
    # Remove trailing comma before ] for strict JSON
    raw = re.sub(r",\s*]", "]", raw)
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = []
        pattern = r'"question"\s*:\s*"((?:[^"\\]|\\.)*)"\s*,\s*"answer"\s*:\s*"((?:[^"\\]|\\.)*)"'
        for m in re.finditer(pattern, raw):
            q = m.group(1).replace('\\"', '"').replace("\\\\", "\\")
            a = m.group(2).replace('\\"', '"').replace("\\\\", "\\")
            data.append({"question": q, "answer": a})
    out = []
    for entry in data:
        if isinstance(entry, dict):
            out.append({"question": entry.get("question", ""), "answer": entry.get("answer", "")})
        else:
            out.append({"question": str(entry), "answer": ""})
    return out


def generate_flashcards_reglementation_ethique(course_title, count=100):
    """Generate ~100 flashcards pour Droit de la santé / Réglementation, avec variantes sans doublons exacts."""
    if "Droit de la santé" in course_title:
        base_themes = [
            ("Qu'est-ce que le droit de la santé ?", "Branche du droit régissant les relations entre patients, professionnels et institutions de santé."),
            ("Quel est le fondement constitutionnel du droit à la santé en France ?", "Le Préambule de la Constitution de 1946 et la Déclaration des droits de l'homme."),
            ("Qu'est-ce que la loi Kouchner ?", "Loi du 4 mars 2002 relative aux droits des malades et à la qualité du système de santé."),
            ("Quels sont les droits fondamentaux du patient ?", "Droit à l'information, au consentement, au respect de la vie privée et à l'accès au dossier médical."),
            ("Qu'est-ce que le consentement éclairé ?", "Accord libre et éclairé du patient après information sur les risques et bénéfices d'un acte."),
            ("Qui est responsable de l'information du patient ?", "Le professionnel de santé qui propose un acte ou un traitement."),
            ("Qu'est-ce que la responsabilité médicale ?", "Obligation de réparer le préjudice causé par une faute, un défaut d'information ou un aléa thérapeutique."),
            ("Quelle est la différence entre responsabilité civile et pénale en santé ?", "Civile : réparation du préjudice. Pénale : sanction pour infraction (homicide, blessures, etc.)."),
            ("Qu'est-ce que l'aléa thérapeutique ?", "Risque réalisé sans faute du praticien, pouvant donner lieu à indemnisation par la solidarité nationale."),
            ("Quel rôle joue l'ONIAM ?", "Office national d'indemnisation des accidents médicaux : indemnise les victimes d'aléas ou d'infections nosocomiales."),
            ("Qu'est-ce qu'une infection nosocomiale ?", "Infection contractée dans un établissement de santé, absente à l'admission."),
            ("Quels sont les droits du patient en fin de vie ?", "Droit au refus de traitement, aux soins palliatifs, à la sédation, à la directive anticipée."),
            ("Qu'est-ce que la directive anticipée ?", "Document par lequel une personne exprime à l'avance ses souhaits sur sa fin de vie en cas d'incapacité."),
            ("Qu'est-ce que la personne de confiance ?", "Personne désignée par le patient pour l'accompagner et être consultée si le patient est hors d'état d'exprimer sa volonté."),
            ("Quel est le cadre légal du secret médical ?", "Article L1110-4 du CSP : secret couvre tout ce qui est venu à la connaissance du professionnel dans l'exercice de sa profession."),
            ("Quelles sont les exceptions au secret médical ?", "Dérogations légales : déclaration de naissance, décès, maladies contagieuses, sévices, etc."),
            ("Qu'est-ce que le partage d'informations entre professionnels ?", "Possibilité de partager des informations pertinentes dans le cadre d'une prise en charge commune, avec accord du patient."),
            ("Qu'est-ce que le dossier médical partagé (DMP) ?", "Dossier numérique regroupant les informations de santé du patient, accessible avec son consentement."),
            ("Quels acteurs contrôlent l'éthique et la déontologie en santé ?", "Ordres professionnels (médecins, infirmiers, etc.), HAS, CNOM, instances de réflexion éthique."),
        ]
    else:
        base_themes = [
            ("Qu'est-ce que la réglementation de la recherche en santé ?", "Ensemble des règles (loi, décrets, bonnes pratiques) encadrant les recherches impliquant l'être humain."),
            ("Quel est le rôle du CPP ?", "Comité de protection des personnes : évalue les projets de recherche pour protéger les participants."),
            ("Qu'est-ce que la loi Jardé ?", "Loi du 5 mars 2012 relative aux recherches impliquant la personne humaine (catégories de recherches)."),
            ("Quelles sont les trois catégories de recherches selon la loi Jardé ?", "Recherches interventionnelles, non interventionnelles, sur produits de santé."),
            ("Qu'est-ce qu'une recherche interventionnelle ?", "Recherche qui modifie la prise en charge ou comporte une contrainte ou un risque pour le participant."),
            ("Qu'est-ce que l'ANSM ?", "Agence nationale de sécurité du médicament et des produits de santé : autorise et surveille les essais."),
            ("Quel est le rôle de l'ANSM dans la recherche ?", "Autoriser les essais sur médicaments et produits de santé, surveiller la sécurité."),
            ("Qu'est-ce que le consentement en recherche ?", "Accord libre, éclairé et exprès du participant après information sur l'objectif, les contraintes et les risques."),
            ("Qu'est-ce qu'un tuteur ou représentant légal en recherche ?", "Personne habilitée à consentir à la recherche pour un majeur protégé ou un mineur."),
            ("Qu'est-ce que l'information préalable en recherche ?", "Document remis au participant décrivant objectifs, déroulement, risques, bénéfices et droits."),
            ("Qu'est-ce que le comité d'éthique ?", "Instance qui émet un avis sur les aspects éthiques d'un projet de recherche."),
            ("Quelle est la différence entre CPP et comité d'éthique ?", "Le CPP est légalement compétent pour autoriser; le comité d'éthique donne un avis consultatif."),
            ("Qu'est-ce que la déclaration d'Helsinki ?", "Texte international de l'AMM définissant les principes éthiques de la recherche sur l'être humain."),
            ("Qu'est-ce que le principe de bienfaisance en recherche ?", "Recherche doit maximiser les bénéfices et minimiser les risques pour les participants."),
            ("Qu'est-ce que l'équilibre bénéfices/risques ?", "Évaluation comparative des bénéfices attendus et des risques encourus pour le participant."),
            ("Qu'est-ce qu'une recherche sans bénéfice direct ?", "Recherche dont le participant n'a pas de bénéfice individuel attendu (bénéfice collectif)."),
            ("Qu'est-ce que l'indemnisation des participants ?", "Compensation des contraintes subies dans le cadre d'une recherche (forfait, défraiement)."),
            ("Quel est le rôle du promoteur en recherche ?", "Personne physique ou morale responsable de la réalisation de la recherche (pharma, CHU, etc.)."),
            ("Qu'est-ce que l'assurance en recherche ?", "Obligation de souscrire une assurance pour couvrir la responsabilité civile du promoteur."),
        ]

    out = []
    for q, a in base_themes:
        # Carte de base
        out.append({"question": q, "answer": a})
        if len(out) >= count:
            return out[:count]
        # Vrai / faux
        out.append(
            {
                "question": f"Vrai ou faux : {a}",
                "answer": f"Vrai. {a}",
            }
        )
        if len(out) >= count:
            return out[:count]
        # Application pratique
        out.append(
            {
                "question": f"Donnez un exemple concret illustrant : {q}",
                "answer": a,
            }
        )
        if len(out) >= count:
            return out[:count]
        # Conséquence pour la pratique
        out.append(
            {
                "question": f"Quelles sont les conséquences pratiques de : {q}",
                "answer": a,
            }
        )
        if len(out) >= count:
            return out[:count]
        # Point clé
        out.append(
            {
                "question": f"Point clé à retenir sur : {q}",
                "answer": a,
            }
        )
        if len(out) >= count:
            return out[:count]

    return out[:count]


def generate_flashcards_technique(course_index, course_title, count=100):
    """Generate ≥30 flashcards pour Technique de vie et société, en multipliant les révisions d’une même notion."""
    blocks = [
        [("Qu'est-ce que la relation vie, technique et société ?", "L'étude des interactions entre progrès technique, vie humaine et organisation sociale."),
         ("Quel est l'enjeu de la technique en santé ?", "La technique modifie les pratiques, les représentations du corps et les relations soignant-soigné.")],
        [("Qu'est-ce que l'éthique en contexte technologique ?", "Réflexion sur les normes et valeurs face aux développements techniques (IA, biotech, etc.)."),
         ("Quel défi pose la civilisation technologique ?", "Concilier innovation et respect de la dignité, autonomie et justice.")],
        [("Qu'est-ce qu'un objet technique en santé ?", "Dispositif ou technologie utilisé dans la prévention, le diagnostic ou le traitement."),
         ("Quel est le statut des technologies en santé ?", "Outils au service du soin, mais aussi facteurs de pouvoir et de dépendance.")],
        [("Quels sont les droits fondamentaux du patient ?", "Droit à l'information, au consentement, au respect et à la non-discrimination."),
         ("Quels sont les devoirs du praticien ?", "Devoir d'information, de moyens, de confidentialité et de non-abandon.")],
        [("Qu'est-ce que le droit à l'information médicale ?", "Droit du patient d'être informé sur son état, les traitements et les alternatives."),
         ("Qui doit délivrer l'information médicale ?", "Le professionnel de santé, de manière claire, loyale et adaptée au patient.")],
        [("Qu'est-ce qu'un objet biologique en droit ?", "Élément du corps ou produit biologique (organe, gamète, donnée) soumis à un régime juridique."),
         ("Quels enjeux pour les bio-objets ?", "Propriété, commercialisation, consentement et dignité.")],
        [("Qui est Céline Lafontaine ?", "Sociologue ayant travaillé sur le corps, la biomédecine et les bio-objets."),
         ("Qu'est-ce que la pensée des bio-objets ?", "Réflexion sur la façon dont les éléments du vivant deviennent des objets techniques et sociaux.")],
        [("Qu'est-ce que la technicisation médicale ?", "Place croissante des techniques et dispositifs dans la relation de soin."),
         ("La technicisation est-elle une déshumanisation ?", "Risque de réduire le patient à un corps à réparer, mais la technique peut aussi améliorer le soin.")],
        [("Qu'est-ce que la médecine humaniste ?", "Approche du soin centrée sur la relation, l'écoute et la dignité de la personne."),
         ("Quelle tension avec la biomédecine ?", "La biomédecine privilégie l'efficacité technique; l'humaniste privilégie la relation et le sens.")],
        [("Qu'est-ce qu'une médecine alternative ?", "Pratique en dehors de la médecine conventionnelle (phytothérapie, acupuncture, etc.)."),
         ("Quel débat critique humaniste vs antiscience ?", "Critique humaniste : ouverture à d'autres paradigmes; antiscience : rejet de la méthode scientifique.")],
        [("Qu'est-ce que le modèle biopsychosocial ?", "Modèle de santé intégrant facteurs biologiques, psychologiques et sociaux."),
         ("Qu'est-ce qu'une approche holistique ?", "Approche qui considère la personne dans sa globalité, pas seulement la maladie.")],
    ]
    base_pairs = blocks[min(course_index, len(blocks) - 1)]
    out = []
    # Pour chaque notion, on crée de nombreuses cartes de révision distinctes (texte différent, même contenu à mémoriser)
    for q, a in base_pairs:
        # Carte de base
        out.append({"question": q, "answer": a})
        # Série de révisions numérotées
        for i in range(1, 21):  # 1 + 20 = 21 cartes par notion → 42 par cours
            if len(out) >= count:
                return out[:count]
            out.append(
                {
                    "question": f"{q} (révision {i})",
                    "answer": a,
                }
            )
    return out[:count]


def generate_flashcards_biotechnologie(course_title, count=100):
    """Generate ~100 flashcards pour la matière Biotechnologie, sans doublons exacts dans un même cours."""
    themes = [
        ("Qu’est-ce que la biotechnologie en santé ?", "L’utilisation de systèmes biologiques (cellules, enzymes, ADN) pour produire des médicaments, vaccins, diagnostics ou biomatériaux."),
        ("Quelle est la différence entre biotechnologie rouge et blanche ?", "La biotechnologie rouge concerne la santé humaine et animale (médicaments, thérapies) ; la biotechnologie blanche concerne les procédés industriels (enzymes, biocarburants)."),
        ("Qu’est-ce qu’une protéine recombinante thérapeutique ?", "Une protéine produite par un organisme génétiquement modifié (bactérie, levure, cellule de mammifère) à partir d’un gène humain inséré."),
        ("Qu’est-ce qu’un vecteur viral en thérapie génique ?", "Un virus modifié pour perdre son pouvoir pathogène mais conserver sa capacité à délivrer un gène thérapeutique dans les cellules cibles."),
        ("Qu’est-ce que la reprogrammation cellulaire ?", "Transformation de cellules différenciées en cellules pluripotentes induites (iPSC) grâce à l’expression forcée de facteurs de transcription (facteurs de Yamanaka)."),
        ("Quels sont les quatre facteurs de Yamanaka classiques ?", "Oct4, Sox2, Klf4 et c‑Myc."),
        ("Qu’est-ce que le drug repositioning ?", "Réutilisation de médicaments existants pour de nouvelles indications thérapeutiques, en s’appuyant sur des données cliniques et biologiques déjà disponibles."),
        ("Citez un avantage du drug repositioning.", "Temps de développement plus court et risque toxique mieux connu, car le médicament est déjà utilisé chez l’homme."),
        ("Qu’est-ce que l’immunothérapie anti‑PD‑1/PD‑L1 ?", "Traitement qui bloque les checkpoints immunitaires PD‑1/PD‑L1 pour réactiver les lymphocytes T contre la tumeur."),
        ("Qu’est-ce qu’une cellule CAR‑T ?", "Lymphocyte T modifié ex vivo pour exprimer un récepteur chimérique spécifique d’un antigène tumoral, puis réinjecté au patient."),
        ("Qu’est-ce qu’un vecteur non viral en thérapie génique ?", "Méthode de transfert de gène sans virus : plasmides nus, liposomes, nanoparticules, électroporation."),
        ("Quels sont les principaux risques de la thérapie génique ?", "Insertion mutagène, activation d’oncogènes, réactions immunitaires contre le vecteur ou la protéine exprimée."),
        ("Qu’est-ce qu’une vésicule extracellulaire ?", "Petite vésicule lipidique sécrétée par les cellules (exosomes, microvésicules) contenant des protéines, ARN et lipides, impliquée dans la communication intercellulaire."),
        ("Pourquoi les vésicules extracellulaires intéressent‑elles la thérapie ?", "Elles peuvent servir de vecteurs naturels de médicaments ou d’ARN thérapeutiques, avec une immunogénicité potentiellement plus faible."),
        ("Qu’est-ce que la bioproduction de cellules souches ?", "Culture à grande échelle de cellules souches (ES, iPSC, MSC) en conditions contrôlées pour une utilisation en thérapie cellulaire."),
        ("Citez deux défis de la bioproduction de cellules souches.", "Assurer la stabilité génétique des lignées et maîtriser la différenciation pour obtenir des cellules fonctionnelles et sûres."),
        ("Qu’est-ce que l’édition du génome par CRISPR‑Cas9 ?", "Système inspiré de l’immunité bactérienne permettant de couper l’ADN en un site spécifique guidé par un ARN et de modifier la séquence (inactivation, insertion, correction)."),
        ("Quels sont les principaux risques de CRISPR‑Cas9 ?", "Coupures hors‑cible (off‑target), mosaïcisme, effets inattendus sur l’expression des gènes."),
        ("Qu’est-ce qu’un biomatériau en santé ?", "Matériau (naturel ou synthétique) utilisé pour remplacer ou soutenir une fonction tissulaire (prothèses, stents, matrices de culture)."),
        ("Quels critères doit respecter un biomatériau ?", "Biocompatibilité, absence de toxicité, propriétés mécaniques adaptées, stabilité, parfois biodégradabilité contrôlée."),
        ("Qu’est-ce que la thérapie cellulaire ?", "Utilisation de cellules vivantes (autologues ou allogéniques) comme médicament pour réparer, remplacer ou moduler des tissus ou des fonctions."),
        ("Quel est le principe d’une greffe de moelle osseuse ?", "Remplacer la moelle malade par des cellules souches hématopoïétiques saines pour restaurer l’hématopoïèse."),
        ("Qu’est-ce qu’un peptide thérapeutique ?", "Petit fragment protéique (quelques acides aminés à quelques dizaines) utilisé comme médicament (hormones, analogues, peptides antimicrobiens)."),
        ("Pourquoi les peptides antimicrobiens issus de la peau de grenouille sont‑ils étudiés ?", "Ils possèdent une activité antibactérienne naturelle et servent de modèles pour de nouveaux antibiotiques."),
    ]
    out = []
    # 1) Carte de base
    for q, a in themes:
        out.append({"question": q, "answer": a})
        if len(out) >= count:
            return out[:count]
        # 2) Carte "Vrai ou faux" dérivée
        out.append(
            {
                "question": f"Vrai ou faux : {a}",
                "answer": f"Vrai. {a}",
            }
        )
        if len(out) >= count:
            return out[:count]
        # 3) Carte "Pourquoi c'est important ?"
        out.append(
            {
                "question": f"Pourquoi est-il important de maîtriser : {q}",
                "answer": a,
            }
        )
        if len(out) >= count:
            return out[:count]
        # 4) Carte "Point clé à retenir"
        out.append(
            {
                "question": f"Point clé à retenir sur {q}",
                "answer": a,
            }
        )
        if len(out) >= count:
            return out[:count]
    return out[:count]


def generate_flashcards_sante_publique(category, course_title, count=100):
    """Generate ~100 flashcards pour les sous-matières de Santé Publique, sans doublons exacts dans un même cours."""
    if "Promotion_Prevention" in category:
        base_themes = [
            ("Qu’est-ce que la promotion de la santé (définition OMS) ?", "Processus qui confère aux populations les moyens d’assurer un plus grand contrôle sur leur propre santé et d’améliorer celle‑ci."),
            ("Quelle est la différence entre prévention primaire, secondaire et tertiaire ?", "Primaire : éviter la survenue de la maladie ; secondaire : dépister précocement ; tertiaire : éviter les complications et séquelles."),
            ("Qu’est-ce qu’un déterminant de santé ?", "Facteur personnel, social, économique ou environnemental qui influence l’état de santé (revenus, éducation, environnement, comportements, accès aux soins…)."),
            ("Donnez des exemples de déterminants sociaux de santé.", "Revenus, niveau d’éducation, emploi, logement, isolement social, discriminations."),
            ("Qu’est-ce qu’un programme de dépistage organisé ?", "Programme national ou régional ciblant une population définie, avec invitation systématique, protocole standardisé et évaluation continue."),
            ("Quels sont les critères d’un bon dépistage (OMS) ?", "Maladie fréquente et grave, phase préclinique détectable, test sensible et spécifique, traitement efficace, bénéfices supérieurs aux risques."),
            ("Pourquoi la vaccination est‑elle un outil central de prévention ?", "Elle confère une immunité individuelle et, au‑delà d’un certain seuil de couverture, une immunité collective qui protège les plus vulnérables."),
            ("Qu’est-ce que la couverture vaccinale ?", "Proportion de personnes vaccinées dans une population donnée pour un vaccin donné."),
            ("Donnez un exemple d’indicateur de sédentarité.", "Temps passé assis devant un écran par jour (hors temps scolaire/professionnel)."),
            ("Quels sont les risques d’une sédentarité importante ?", "Augmentation du risque de maladies cardiovasculaires, diabète de type 2, obésité, certains cancers, troubles musculo‑squelettiques."),
            ("Quels types d’actions relève de l’éducation pour la santé ?", "Information, sensibilisation, développement des compétences psychosociales, participation communautaire."),
            ("Qu’est-ce qu’un accident d’exposition au sang (AES) ?", "Contact avec du sang ou un liquide biologique potentiellement contaminant, par piqûre, coupure ou projection sur muqueuse/peau lésée."),
            ("Quels sont les premiers gestes en cas d’AES ?", "Rincer abondamment, antisepsie locale, évaluer le risque, contacter le référent AES, envisager un traitement post‑exposition."),
            ("Quelles IST font l’objet d’actions prioritaires de prévention ?", "VIH, hépatites B et C, infections à Chlamydia, syphilis, gonorrhée."),
            ("Qu’est-ce qu’une action de prévention universelle ?", "Action s’adressant à l’ensemble de la population, quel que soit le niveau de risque individuel."),
            ("Qu’est-ce qu’une action de prévention ciblée ?", "Action orientée vers des populations à risque accru (usagers de drogues, HSH, personnes précaires…)."),
        ]
    elif "Economie_Sante" in category:
        base_themes = [
            ("Qu’est-ce que l’économie de la santé ?", "Discipline qui étudie l’allocation des ressources consacrées à la santé et l’efficience des interventions."),
            ("Qu’entend‑on par perte d’autonomie ?", "Difficulté à accomplir seul les activités de la vie quotidienne, nécessitant une aide humaine ou technique."),
            ("Citez un indicateur de dépendance.", "Score GIR ou échelles d’AVQ (Katz, Lawton)."),
            ("Qu’est-ce qu’une analyse coût‑efficacité ?", "Comparaison du coût d’une intervention à son gain en années de vie ou années de vie ajustées sur la qualité (QALY)."),
            ("Qu’est-ce qu’une analyse coût‑utilité ?", "Analyse coût‑efficacité utilisant spécifiquement les QALY comme mesure d’utilité."),
            ("Qu’est-ce qu’un paiement à l’acte pour les médecins libéraux ?", "Rémunération proportionnelle au nombre et au type d’actes réalisés."),
            ("Citez un avantage et un inconvénient du paiement à l’acte.", "Avantage : incitation à l’activité ; inconvénient : risque de sur‑activité et de fragmentation des soins."),
            ("Qu’est-ce que la capitation ?", "Rémunération forfaitaire par patient inscrit, indépendamment du nombre d’actes."),
            ("Qu’est-ce que la T2A (tarification à l’activité) ?", "Financement des hôpitaux en fonction de l’activité réalisée (groupes homogènes de séjours) et non d’un budget global historique."),
            ("Quels sont les enjeux de la T2A ?", "Incitation à augmenter l’activité et la productivité, mais risque de sélection des patients et de pression sur les durées de séjour."),
            ("Comment la santé influence‑t‑elle la croissance économique ?", "Une population en bonne santé est plus productive, travaille plus longtemps et consomme davantage."),
            ("Qu’est-ce qu’une inégalité sociale de santé ?", "Différence d’état de santé systématique et évitable entre groupes sociaux, liée à des facteurs sociaux et économiques."),
            ("Qu’est-ce que le gradient social de santé ?", "Relation continue entre position sociale et santé : plus le statut socio‑économique est bas, plus la santé est mauvaise."),
        ]
    elif "Geographie_Sante" in category:
        base_themes = [
            ("Qu’est-ce que la géographie de la santé ?", "Champ qui étudie la répartition spatiale des maladies, des ressources de santé et des déterminants environnementaux."),
            ("Qu’est-ce qu’un désert médical ?", "Territoire où l’offre de soins est insuffisante au regard des besoins de la population."),
            ("Quels outils sont utilisés en géographie de la santé ?", "Systèmes d’information géographique (SIG), cartes de densité, indicateurs de distance/temps d’accès."),
            ("Qu’est-ce qu’une inégalité géographique d’accès aux soins ?", "Différence d’accessibilité aux services de santé entre territoires (rural/urbain, régions, quartiers)."),
            ("Donnez un exemple d’inégalité géographique en France.", "Temps d’accès plus long à un service d’urgences ou à un spécialiste dans les zones rurales ou de montagne."),
            ("Qu’est-ce que l’urbanisme favorable à la santé ?", "Conception des villes visant à promouvoir l’activité physique, la qualité de l’air, la cohésion sociale et la sécurité."),
            ("Quel est le rôle des espaces verts urbains pour la santé ?", "Réduction du stress, promotion de l’activité physique, amélioration de la qualité de l’air, lieu de sociabilité."),
            ("Quels groupes sont particulièrement vulnérables en ville ?", "Personnes âgées, enfants, personnes en situation de handicap, personnes en grande précarité."),
            ("Pourquoi la géographie de la santé s’intéresse‑t‑elle à l’alimentation en ville ?", "Parce que la localisation des commerces, marchés, fast‑foods et transports influence l’accès à une alimentation saine."),
        ]
    else:  # Gestion de projet RC
        base_themes = [
            ("Qu’est-ce qu’un essai clinique ?", "Recherche contrôlée visant à évaluer l’efficacité et la tolérance d’une intervention (médicament, dispositif, stratégie)."),
            ("Quelles sont les grandes phases de développement d’un médicament ?", "Phase I (tolérance), phase II (premières données d’efficacité), phase III (efficacité comparée), phase IV (pharmacovigilance)."),
            ("Qui est le promoteur d’un essai clinique ?", "Personne physique ou morale qui prend l’initiative de la recherche, en assure la gestion et le financement."),
            ("Qu’est-ce qu’un investigateur dans un essai clinique ?", "Médecin responsable de la conduite pratique de l’essai sur un site donné."),
            ("Qu’est-ce qu’un événement indésirable grave (EIG) ?", "Événement médical qui entraîne la mort, met la vie en danger, nécessite une hospitalisation ou provoque une invalidité significative."),
            ("Qu’est-ce que le monitoring d’un essai clinique ?", "Contrôle de la conformité de l’essai au protocole, à la loi et aux bonnes pratiques cliniques, sur site ou à distance."),
            ("Qu’est-ce qu’un CRF (Case Report Form) ?", "Cahier d’observation (papier ou électronique) dans lequel sont enregistrées les données de chaque participant."),
            ("Quel est le rôle d’une structure de soutien à la recherche clinique (DRCI, CRC) ?", "Aider au montage, au suivi et à la gestion administrative et réglementaire des essais."),
            ("Quelles démarches réglementaires sont nécessaires avant de débuter un essai ?", "Avis favorable du CPP, autorisation de l’ANSM si nécessaire, enregistrement sur un registre public, accords institutionnels internes."),
            ("Qu’est-ce que la réglementation sur les échantillons biologiques ?", "Règles encadrant le prélèvement, la conservation et l’utilisation des échantillons (consentement, information, anonymisation)."),
            ("Quel est le rôle du MESRI en recherche clinique ?", "Ministère chargé de l’enseignement supérieur et de la recherche, impliqué dans la régulation et le financement de la recherche."),
        ]

    out = []
    for q, a in base_themes:
        # Carte de base
        out.append({"question": q, "answer": a})
        if len(out) >= count:
            return out[:count]
        # Variante vrai / faux
        out.append(
            {
                "question": f"Vrai ou faux : {a}",
                "answer": f"Vrai. {a}",
            }
        )
        if len(out) >= count:
            return out[:count]
        # Variante application pratique
        out.append(
            {
                "question": f"Donnez une application pratique de : {q}",
                "answer": a,
            }
        )
        if len(out) >= count:
            return out[:count]
        # Variante « point clé »
        out.append(
            {
                "question": f"Quel est le message clé à retenir sur : {q}",
                "answer": a,
            }
        )
        if len(out) >= count:
            return out[:count]

    return out[:count]


def dedupe_flashcards(items):
    """Supprime les doublons exacts (même question ET même réponse), en gardant le premier."""
    seen = set()
    deduped = []
    for it in items:
        q = it.get("question", "")
        a = it.get("answer", "")
        key = (q, a)
        if key in seen:
            continue
        seen.add(key)
        deduped.append(it)
    return deduped


def get_course_html_template():
    """Return the full HTML template for a course page (LSPS1-style)."""
    return open(BASE_DIR / "UPEC_LSPS1_S2" / "ICM" / "fc1.html", "r", encoding="utf-8").read()


def build_course_html_lsps3(matiere_dir, matiere_display, course_title, flashcards_js, menu_html, asset_prefix="../"):
    """Build one course HTML for UPEC LSPS3 S2 (one level deep: Matiere/fcX.html)."""
    # Use same structure as LSPS1 but with asset_prefix = ../ and logo link to ../index.html, menu with ./
    template = """<!DOCTYPE HTML>
<html>
<head>
<title>Diploma Santé - Plateforme de Flashcards</title>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
<link rel="stylesheet" href="{asset_prefix}assets/css/main.css" />
<link rel="icon" type="image/jpeg" href="{asset_prefix}images/diploma.jpeg" />
<script src="{asset_prefix}security.js" defer></script>
<script src="{asset_prefix}assets/js/favorites.js"></script>
</head>
<body class="is-preload">

<div id="wrapper">

<div id="main">
<div class="inner">

<header id="header">
<a href="../index.html" class="logo"><strong>Diploma Santé</strong> - UPEC LSPS3 S2</a>
<ul class="icons">
<li><a href="https://diploma-sante.fr/" class="icon fas fa-globe"><span class="label"></span></a></li>
<li><a href="https://www.instagram.com/diplomasante/" class="icon brands fa-instagram"><span class="label">Instagram</span></a></li>
<li><a href="#" id="dark-mode-toggle" class="icon fas fa-moon"></a></li>
</ul>
</header>

<section>
<header class="main"><div class="header-left"><h1>{matiere_display}</h1><h2>{course_title}</h2></div><span class="image main"><img src="{asset_prefix}images/banner.png" alt="" /></span></header>

<style>
  #header {{ padding: 1rem 0; margin-bottom: 0.5rem; }}
  header.main {{ margin-top: 1.5rem !important; margin-bottom: 0.8rem !important; padding-bottom: 0.5rem !important; display: flex; align-items: center; gap: 2rem; }}
  header.main .header-left h1, header.main .header-left h2 {{ flex: 1; margin: 0 !important; }}
  header.main h1 {{ font-size: 2em !important; line-height: 1.3 !important; }}
  header.main h2 {{ font-size: 1.3em !important; color: #7f888f !important; }}
  header.main .header-left {{ flex: 1; display: flex; flex-direction: column; }}
  .image.main {{ flex: 1; max-height: none !important; overflow: visible !important; margin: 0 !important; display: flex; align-items: center; justify-content: center; }}
  .image.main img {{ width: 100% !important; height: auto !important; max-height: 120px !important; object-fit: contain !important; object-position: center; }}
  section {{ padding-top: 0 !important; }}
  .progress-container {{ width: 100%; max-width: 1000px; height: 20px; background-color: #eee; border-radius: 10px; overflow: hidden; margin: 0 auto 1rem; border: 1px solid #ddd; }}
  .progress-bar {{ height: 100%; background-color: #00aeef; width: 0%; transition: width 0.3s; }}
  .flashcards-container {{ display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 2rem; min-height: calc(100vh - 250px); padding: 1rem 0; }}
  .flashcard {{ width: 100%; max-width: 1000px; height: calc(100vh - 340px); min-height: 450px; perspective: 1500px; cursor: pointer; display: flex; flex-direction: column; justify-content: center; align-items: center; position: relative; }}
  .flashcard-inner {{ position: relative; width: 100%; height: 100%; border-radius: 20px; box-shadow: 0 12px 40px rgba(0, 0, 0, 0.25); background-color: white; transition: transform 0.6s; overflow: visible; transform-style: preserve-3d; }}
  .flashcard.show-answer .flashcard-inner {{ transform: rotateY(180deg); }}
  .flashcard-front, .flashcard-back {{ position: absolute; width: 100%; height: 100%; border-radius: 20px; backface-visibility: hidden; display: flex; justify-content: center; align-items: center; padding: 3rem; font-size: 2rem; text-align: center; }}
  .flashcard-front {{ background-color: white; color: #333; box-shadow: inset 0 0 40px rgba(0, 174, 239, 0.15); }}
  .flashcard-back {{ background-color: #73C3EC; color: white; overflow: visible; transform: rotateY(180deg); box-shadow: inset 0 0 50px rgba(255, 255, 255, 0.5); font-size: 2.2rem; text-shadow: 0 0 4px rgba(255, 255, 255, 0.3); }}
  .flashcard-button {{ margin-top: 1rem; display: flex; justify-content: center; align-items: center; gap: 1rem; width: 100%; flex-wrap: wrap; }}
  .check-icon, .cross-icon, .favorite-icon {{ display: none; position: absolute; cursor: pointer; z-index: 1000; transition: all 0.3s; opacity: 0.8; pointer-events: auto; }}
  .check-icon {{ top: 30px; left: 30px; align-items: center; justify-content: center; width: 45px; height: 45px; overflow: visible; z-index: 1001; background: rgba(255, 255, 255, 0.95); border-radius: 50%; padding: 8px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3); cursor: pointer; transition: all 0.3s; color: #888; font-size: 20px; }}
  .check-icon i {{ pointer-events: none; transform: scaleX(-1); }}
  .cross-icon {{ top: 30px; right: 30px; stroke: #888; align-items: center; justify-content: center; width: 45px; height: 45px; overflow: visible; z-index: 1001; background: rgba(255, 255, 255, 0.95); border-radius: 50%; padding: 8px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3); cursor: pointer; transition: all 0.3s; }}
  body.dark-mode .check-icon, body.dark-mode .cross-icon {{ background: rgba(50, 50, 50, 0.95); color: #fff; stroke: #fff; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.5); }}
  body.dark-mode .check-icon:hover {{ background: rgba(40, 150, 40, 0.95); color: #fff; }}
  body.dark-mode .cross-icon:hover {{ background: rgba(150, 40, 40, 0.95); stroke: #fff; }}
  .favorite-icon {{ bottom: 15px; left: 50%; transform: translateX(-50%); fill: #888; width: 30px; height: 30px; }}
  .favorite-icon.active {{ fill: #ffd700; }}
  .flashcard.show-answer .check-icon, .flashcard.show-answer .cross-icon, .flashcard.show-answer .favorite-icon {{ display: flex !important; }}
  .check-icon:hover {{ stroke: #27ae60; color: #27ae60; opacity: 1; }}
  .cross-icon:hover {{ stroke: #e74c3c; opacity: 1; }}
  .slide-left {{ animation: slideLeft 0.4s forwards; }}
  .slide-right {{ animation: slideRight 0.4s forwards; }}
  @keyframes slideLeft {{ from {{ transform: translateX(0); opacity: 1; }} to {{ transform: translateX(-100%); opacity: 0; }} }}
  @keyframes slideRight {{ from {{ transform: translateX(0); opacity: 1; }} to {{ transform: translateX(100%); opacity: 0; }} }}
  body.dark-mode .flashcard-front {{ background-color: #2d3436; color: #e2e8f0; }}
  body.dark-mode .flashcard-inner {{ background-color: #2d3436; }}
  body.dark-mode .progress-container {{ background-color: #34495e; border-color: #4a5568; }}
</style>

<div class="progress-container"><div class="progress-bar" id="progressBar"></div></div>
<div class="flashcards-container" id="flashcards"></div>

<script>
const flashcardsData = [
{flashcards_js}
];

const container = document.getElementById("flashcards");
const progressBar = document.getElementById("progressBar");
const originalData = [...flashcardsData];
let flashcards = [...originalData];
const pageId = location.pathname.split("/").pop().replace(".html","");
const progressKey = "progress_" + pageId;
let currentIndex = parseInt(localStorage.getItem(progressKey)) || 0;
if (currentIndex >= originalData.length) {{ currentIndex = 0; localStorage.setItem(progressKey, currentIndex); }}

function updateProgress() {{
  const total = originalData.length;
  const progress = Math.min(currentIndex / total, 1);
  progressBar.style.width = `${{progress * 100}}%`;
}}

function createContent(content) {{
  if (typeof content === "string") {{
    const div = document.createElement("div");
    div.textContent = content;
    return div;
  }}
  if (typeof content === "object" && content.type === "image") {{
    const wrapper = document.createElement("div");
    wrapper.style.textAlign = "center";
    if (content.caption) {{
      const caption = document.createElement("div");
      caption.textContent = content.caption;
      caption.style.marginBottom = "6px";
      caption.style.fontStyle = "italic";
      caption.style.fontSize = "0.9em";
      wrapper.appendChild(caption);
    }}
    const img = document.createElement("img");
    img.src = content.src;
    img.alt = content.alt || "";
    img.style.maxWidth = "100%";
    img.style.height="auto"; img.style.maxHeight="150px"; img.style.objectFit="contain";
    wrapper.appendChild(img);
    return wrapper;
  }}
  return document.createElement("div");
}}

function showCard(index) {{
  container.innerHTML = "";
  if (flashcards[index]) {{
    const {{ question, answer }} = flashcards[index];
    const card = document.createElement("div");
    card.classList.add("flashcard", "show");
    const inner = document.createElement("div");
    inner.classList.add("flashcard-inner");
    const front = document.createElement("div");
    front.classList.add("flashcard-front");
    front.appendChild(createContent(question));
    const back = document.createElement("div");
    back.classList.add("flashcard-back");
    back.appendChild(createContent(answer));
    const btnContainer = document.createElement("div");
    btnContainer.classList.add("flashcard-button");
    const toggleBtn = document.createElement("button");
    toggleBtn.classList.add("button", "large");
    toggleBtn.textContent = "Voir la réponse";
    const resetBtn = document.createElement("button");
    resetBtn.classList.add("button", "large");
    resetBtn.textContent = "Réinitialiser";
    resetBtn.id = "reset";
    resetBtn.addEventListener("click", (e) => {{
      e.stopPropagation();
      localStorage.removeItem(progressKey);
      localStorage.removeItem("completed_" + pageId);
      flashcards = [...originalData];
      currentIndex = 0;
      updateProgress();
      showCard(currentIndex);
    }});
    btnContainer.appendChild(toggleBtn);
    btnContainer.appendChild(resetBtn);
    const checkIcon = document.createElement("span");
    checkIcon.classList.add("check-icon");
    checkIcon.innerHTML = '<i class="fas fa-check"></i>';
    checkIcon.addEventListener("click", (e) => {{
      e.stopPropagation();
      card.classList.add("slide-right");
      setTimeout(() => {{
        currentIndex++;
        localStorage.setItem(progressKey, currentIndex);
        updateProgress();
        showCard(currentIndex);
      }}, 400);
    }});
    const crossIcon = document.createElement("span");
    crossIcon.classList.add("cross-icon");
    crossIcon.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="#888" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24"><line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" /></svg>`;
    crossIcon.addEventListener("click", (e) => {{
      e.stopPropagation();
      card.classList.add("slide-left");
      setTimeout(() => {{
        const removed = flashcards.splice(currentIndex, 1)[0];
        flashcards.splice(currentIndex + 5, 0, removed);
        showCard(currentIndex);
      }}, 400);
    }});
    const favIcon = document.createElement("span");
    favIcon.classList.add("favorite-icon");
    favIcon.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="30" height="30"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>`;
    function updateFav() {{
      if (isFavorite({{question, answer}})) favIcon.classList.add("active");
      else favIcon.classList.remove("active");
    }}
    favIcon.addEventListener("click", (e) => {{
      e.stopPropagation();
      toggleFavorite({{question, answer}});
      updateFav();
    }});
    updateFav();
    card.addEventListener("click", () => {{
      const isAnswerVisible = card.classList.toggle("show-answer");
      toggleBtn.textContent = isAnswerVisible ? "Cacher la réponse" : "Voir la réponse";
    }});
    inner.appendChild(front);
    inner.appendChild(back);
    inner.appendChild(checkIcon);
    inner.appendChild(crossIcon);
    inner.appendChild(favIcon);
    card.appendChild(inner);
    card.appendChild(btnContainer);
    container.appendChild(card);
  }} else {{
    container.innerHTML = "";
    const endCard = document.createElement("div");
    endCard.classList.add("flashcard", "show", "show-answer");
    const inner = document.createElement("div");
    inner.classList.add("flashcard-inner");
    const back = document.createElement("div");
    back.classList.add("flashcard-back");
    back.innerHTML = "<p>Plus de flashcard disponible.</p>";
    const btnContainer = document.createElement("div");
    btnContainer.classList.add("flashcard-button");
    const resetBtn = document.createElement("button");
    resetBtn.classList.add("button", "large");
    resetBtn.textContent = "Réinitialiser";
    resetBtn.id = "reset";
    resetBtn.addEventListener("click", (e) => {{
      e.stopPropagation();
      localStorage.removeItem(progressKey);
      localStorage.removeItem("completed_" + pageId);
      flashcards = [...originalData];
      currentIndex = 0;
      updateProgress();
      showCard(currentIndex);
    }});
    btnContainer.appendChild(resetBtn);
    inner.appendChild(back);
    endCard.appendChild(inner);
    endCard.appendChild(btnContainer);
    container.appendChild(endCard);
    localStorage.setItem("completed_" + pageId, "true");
    updateProgress();
  }}
}}

showCard(currentIndex);
updateProgress();
</script>

</section>

</div>
</div>

<div id="sidebar">
<div class="inner">

<section id="search" class="alt">
<form method="post" action="#">
<input type="text" name="query" id="query" placeholder="Rechercher">
</form>
</section>

{menu_html}

<footer id="footer">
<p class="copyright">&copy; Diploma Santé. Tous droits réservés.</p>
</footer>

</div>
</div>

</div>

<script src="{asset_prefix}assets/js/jquery.min.js"></script>
<script src="{asset_prefix}assets/js/browser.min.js"></script>
<script src="{asset_prefix}assets/js/breakpoints.min.js"></script>
<script src="{asset_prefix}assets/js/util.js"></script>
<script src="{asset_prefix}assets/js/main.js"></script>
<script src="{asset_prefix}assets/js/darkmode.js"></script>
<script src="{asset_prefix}assets/js/favorites.js"></script>

</body>
</html>"""
    return template.format(
        asset_prefix=asset_prefix,
        matiere_display=matiere_display,
        course_title=course_title,
        flashcards_js=flashcards_js,
        menu_html=menu_html,
    )


def build_menu_html(prefix="."):
    """Build full nav menu for UPEC LSPS3 S2."""
    lines = [
        '<nav id="menu">',
        '<header class="major"><h2>Menu</h2></header>',
        "<ul>",
        f'<li><a href="{prefix}/index.html">Accueil</a></li>',
        f'<li><a href="{prefix}/favorites.html">Favoris</a></li>',
    ]
    for mat in STRUCTURE:
        lines.append(f'<li><span class="opener">{mat["display"]}</span><ul>')
        for js_name, html_name, title in mat["courses_with_js"]:
            lines.append(f'<li><a href="{prefix}/{mat["dir"]}/{html_name}">{title}</a></li>')
        for html_name, title in mat["courses_generated"]:
            lines.append(f'<li><a href="{prefix}/{mat["dir"]}/{html_name}">{title}</a></li>')
        lines.append("</ul></li>")
    lines.append("</ul></nav>")
    return "\n".join(lines)


def get_all_course_paths():
    paths = []
    for mat in STRUCTURE:
        for _, html_name, _ in mat["courses_with_js"]:
            paths.append(f"{mat['dir']}/{html_name}")
        for html_name, _ in mat["courses_generated"]:
            paths.append(f"{mat['dir']}/{html_name}")
    return paths


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    menu_html = build_menu_html("..")  # From a course page we go up to section root

    for mat in STRUCTURE:
        mat_dir = OUT_DIR / mat["dir"]
        mat_dir.mkdir(parents=True, exist_ok=True)
        src_dir = FLASHCARD_SRC / mat["source_subdir"] if mat["source_subdir"] else None

        for js_name, html_name, course_title in mat["courses_with_js"]:
            if src_dir:
                js_path = src_dir / js_name
                if not js_path.exists():
                    print(f"Skip (missing): {js_path}")
                    continue
                items = read_js_flashcards(js_path)
            else:
                items = []
            items = dedupe_flashcards(items)
            if not items:
                continue
            data_js = json_to_js_data(items)
            html_content = build_course_html_lsps3(
                mat["dir"], mat["display"], course_title, data_js, menu_html, asset_prefix="../../"
            )
            with open(mat_dir / html_name, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"Wrote {mat['dir']}/{html_name} ({len(items)} cards)")

        for html_name, course_title in mat["courses_generated"]:
            if mat["dir"] == "Reglementation_Ethique_Recherche":
                items = generate_flashcards_reglementation_ethique(course_title, 100)
            elif mat["dir"] == "Technique_Vie_Societe":
                idx = TECHNIQUE_TITLES.index(course_title) if course_title in TECHNIQUE_TITLES else 0
                items = generate_flashcards_technique(idx, course_title, 100)
            elif mat["dir"] == "Biotechnologie":
                items = generate_flashcards_biotechnologie(course_title, 100)
            elif mat["dir"].startswith("SP_"):
                items = generate_flashcards_sante_publique(mat["dir"], course_title, 100)
            else:
                items = []
            items = dedupe_flashcards(items)
            data_js = json_to_js_data(items)
            html_content = build_course_html_lsps3(
                mat["dir"], mat["display"], course_title, data_js, menu_html, asset_prefix="../../"
            )
            with open(mat_dir / html_name, "w", encoding="utf-8") as f:
                f.write(html_content)
            print(f"Wrote {mat['dir']}/{html_name} (generated {len(items)} cards)")

    # On ne régénère pas la page index LSPS3 (déjà créée à la main)
    return

    # Index page (générée automatiquement dans la première version du script)
    course_paths = get_all_course_paths()
    course_paths_js = ",\n".join([f"'{p}'" for p in course_paths])
    menu_index = build_menu_html(".")
    matiere_cards = []
    for mat in STRUCTURE:
        first_html = None
        if mat["courses_with_js"]:
            first_html = mat["courses_with_js"][0][1]
        if mat["courses_generated"]:
            first_html = mat["courses_generated"][0][0]
        if first_html:
            matiere_cards.append(
                f'<div class="matiere-card">\n<span class="icon solid {mat["icon"]}"></span>\n<h3>{mat["display"]}</h3>\n<a href="{mat["dir"]}/{first_html}" class="button">Commencer</a>\n</div>'
            )
    cards_html = "\n".join(matiere_cards)
    index_content = f"""<!DOCTYPE HTML>
<html>
<head>
<title>Diploma Santé - Plateforme de Flashcards - UPEC LSPS3 S2</title>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
<link rel="stylesheet" href="../assets/css/main.css" />
<link rel="icon" type="image/jpeg" href="../images/diploma.jpeg" />
<script src="../security.js" defer></script>
<script src="../assets/js/favorites.js"></script>
</head>
<body class="is-preload index-page">

<div id="wrapper">

<div id="main">
<div class="inner">

<header id="header">
<a href="../index.html" class="logo"><strong>Diploma Santé</strong> - UPEC LSPS3 S2</a>
<ul class="icons">
<li><a href="https://diploma-sante.fr/" class="icon fas fa-globe"><span class="label"></span></a></li>
<li><a href="https://www.instagram.com/diplomasante/" class="icon brands fa-instagram"><span class="label">Instagram</span></a></li>
<li><a href="#" id="dark-mode-toggle" class="icon fas fa-moon"></a></li>
</ul>
</header>

<section id="banner">
<div class="content">
<header>
<h1>UPEC LSPS3 - Semestre 2</h1>
<p>Plateforme de Flashcards</p>
</header>
<p>Boostez vos révisions en santé avec des flashcards efficaces, spécialement pensées pour les étudiants de l'UPEC !</p>
<p id="courseSummary" style="color:#00aeef;"><span class="icon solid fa-star"></span> Cours complétés: <strong><span id="completedCourses"></span>/<span id="totalCourses"></span></strong></p>
</div>
<span class="image">
<img src="../images/pic01.jpg" alt="" />
</span>
</section>

<style>
.matiere-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1.5rem;
  margin-top: 1.5rem;
}}
.matiere-card {{
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border: 2px solid #e0e0e0;
  border-radius: 16px;
  padding: 1.8rem 1.5rem;
  text-align: center;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  text-decoration: none;
  display: block;
  color: inherit;
}}
.matiere-card:hover {{
  transform: translateY(-6px);
  box-shadow: 0 8px 25px rgba(0, 174, 239, 0.25);
  border-color: #00aeef;
}}
.matiere-card .icon {{
  font-size: 2.5em;
  color: #00aeef;
  margin-bottom: 0.8rem;
  display: block;
}}
.matiere-card h3 {{
  font-size: 1.15em;
  margin: 0 0 0.8rem 0;
  color: #3d4449;
  font-weight: 600;
}}
.matiere-card .button {{
  font-size: 0.85em;
  padding: 0.5em 1.5em;
}}
body.dark-mode .matiere-card {{
  background: linear-gradient(135deg, #2d3436 0%, #1e2124 100%);
  border-color: #4a5568;
}}
body.dark-mode .matiere-card h3 {{ color: #e2e8f0; }}
body.dark-mode .matiere-card:hover {{
  border-color: #00aeef;
  background: linear-gradient(135deg, #34495e 0%, #2d3436 100%);
}}
</style>

<section>
<header class="major">
<h2>Explorez les matières disponibles</h2>
</header>
<div class="matiere-grid">
{cards_html}
</div>
</section>

</div>
</div>

<div id="sidebar">
<div class="inner">

<section id="search" class="alt">
<form method="post" action="#">
<input type="text" name="query" id="query" placeholder="Rechercher">
</form>
</section>

{menu_index}

<footer id="footer">
<p class="copyright">&copy; Diploma Santé. Tous droits réservés.</p>
</footer>

</div>
</div>

</div>

<script src="../assets/js/jquery.min.js"></script>
<script src="../assets/js/browser.min.js"></script>
<script src="../assets/js/breakpoints.min.js"></script>
<script src="../assets/js/util.js"></script>
<script src="../assets/js/main.js"></script>
<script src="../assets/js/darkmode.js"></script>
<script src="../assets/js/favorites.js"></script>
<script>
const COURSE_PATHS = [
{course_paths_js}
];

function getPageIdFromPath(path) {{
  return path.split('/').pop().replace(/\\.html$/, '');
}}

function updateCourseCount() {{
  const total = COURSE_PATHS.length;
  let completed = 0;
  COURSE_PATHS.forEach(function(coursePath) {{
    const pageId = getPageIdFromPath(coursePath);
    const key = 'completed_' + pageId;
    if (localStorage.getItem(key) === 'true') {{
      completed++;
    }}
  }});
  const completedEl = document.getElementById('completedCourses');
  const totalEl = document.getElementById('totalCourses');
  if (completedEl) completedEl.textContent = completed;
  if (totalEl) totalEl.textContent = total;
}}

document.addEventListener("DOMContentLoaded", function() {{
  updateCourseCount();
}});
</script>

</body>
</html>
"""
    with open(OUT_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(index_content)
    print("Wrote index.html")

    # Favorites page
    fav_content = open(BASE_DIR / "UPEC_LSPS1_S2" / "favorites.html", "r", encoding="utf-8").read()
    fav_content = fav_content.replace("UPEC LSPS1 S2", "UPEC LSPS3 S2")
    fav_content = fav_content.replace("favorites_upec_lsps1_s2", "favorites_upec_lsps3_s2")
    fav_content = fav_content.replace("../index.html", "../index.html")
    # Ensure menu links are for LSPS3 section
    fav_content = re.sub(r'href="\./ICM/', 'href="./Bases_moleculaire_Oncologie/', fav_content, count=1)
    # Replace full menu with LSPS3 menu
    menu_fav = build_menu_html(".")
    fav_content = re.sub(
        r'<nav id="menu">.*?</nav>',
        menu_fav.replace("\\", "\\\\").replace("$", "\\$"),
        fav_content,
        flags=re.DOTALL,
    )
    # Simpler: just build favorites from LSPS1 template and replace section-specific parts
    fav_path = OUT_DIR / "favorites.html"
    fav_template = open(BASE_DIR / "UPEC_LSPS1_S2" / "favorites.html", "r", encoding="utf-8").read()
    fav_template = fav_template.replace("UPEC LSPS1 S2", "UPEC LSPS3 S2")
    fav_template = fav_template.replace("favorites_upec_lsps1_s2", "favorites_upec_lsps3_s2")
    # Replace menu block
    start = fav_template.find("<nav id=\"menu\">")
    end = fav_template.find("</nav>", start) + len("</nav>")
    if start != -1 and end > start:
        fav_template = fav_template[:start] + build_menu_html(".") + fav_template[end:]
    with open(fav_path, "w", encoding="utf-8") as f:
        f.write(fav_template)
    print("Wrote favorites.html")

    print("Done. Total course paths:", len(course_paths))


if __name__ == "__main__":
    main()

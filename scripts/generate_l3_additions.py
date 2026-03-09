#!/usr/bin/env python3
"""Generate Biotechnologie + Santé Publique courses for UPEC_LSPS3_S2."""
import os
import re
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUT_DIR = BASE_DIR / "UPEC_LSPS3_S2"

CURLY = "\u2019"

def esc(s):
    if not isinstance(s, str):
        return s
    s = re.sub(r"([a-zA-ZéèêëàâäùûüïîôöçÉÈÊËÀÂÄÙÛÜÏÎÔÖÇœŒæÆ])'([a-zA-ZéèêëàâäùûüïîôöçÉÈÊËÀÂÄÙÛÜÏÎÔÖÇœŒæÆ])", r"\1" + CURLY + r"\2", s)
    s = s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace("\r", "")
    return s

def flashcards_js(items):
    lines = []
    for q, a in items:
        lines.append(f"  {{ question: '{esc(q)}', answer: '{esc(a)}' }}")
    return ",\n".join(lines)

# ── Existing subjects (for sidebar) ──
EXISTING_SUBJECTS = [
    ("Bases_moleculaire_Oncologie", "Bases moléculaires en oncologie", [
        ("fc1.html", "Introduction au cancer"),
        ("fc2.html", "Bases cellulaires et moléculaires pour comprendre l\u2019oncologie"),
        ("fc3.html", "Oncogenèse des lymphomes T"),
        ("fc4.html", "Exploration des anomalies moléculaires dans les tumeurs"),
        ("fc5.html", "Mécanismes de réparation de l\u2019ADN et cancer"),
        ("fc6.html", "Oncogenèse digestive"),
        ("fc7.html", "Bases de thérapeutique du cancer"),
        ("fc8.html", "Mutation du gène BRAF dans les mélanomes"),
        ("fc9.html", "Lymphome diffus à grandes cellules (DLBCL)"),
        ("fc10.html", "Bases de données"),
        ("fc11.html", "Cancer du sein : perspective de l\u2019oncogénétique"),
    ]),
    ("Human_Nutrition", "Human nutrition", [
        ("fc1.html", "Métabolisme bioénergétique (révision)"),
        ("fc2.html", "Anthropométrie, bilan énergétique, valeurs de référence en diététique"),
        ("fc3.html", "Macronutriments : protéines, glucides et acides gras"),
        ("fc4.html", "Les micronutriments : minéraux"),
        ("fc5.html", "Les vitamines liposolubles"),
        ("fc5_2.html", "Les vitamines hydrosolubles"),
        ("fc6.html", "Maladies cardiovasculaires"),
        ("fc7.html", "Alimentation et cancer"),
        ("fc8.html", "Consommation d\u2019alcool et effets sur la santé"),
        ("fc9.html", "Interaction régime-maladie : obésité, syndrome métabolique et diabète"),
        ("fc10.html", "Interventions diététiques et pharmacologiques"),
    ]),
    ("One_Health", "One Health", [
        ("fc1.html", "Introduction au concept One Health"),
        ("fc2.html", "Zoonoses et modes de transmission"),
        ("fc3.html", "Émergence et diffusion de la résistance aux antibiotiques"),
        ("fc4.html", "Maladies émergentes transmises de l\u2019animal à l\u2019homme"),
        ("fc5.html", "Mobiliser les professionnels et la population autour des approches One Health"),
        ("fc6.html", "Polluants de l\u2019environnement professionnel"),
        ("fc7.html", "Évaluation, prévention et gestion des risques en santé environnementale"),
        ("fc8.html", "Principales théories, concepts et modèles en sciences sociales (One Health)"),
        ("fc9.html", "Surveillance et investigation en santé publique et santé animale"),
        ("fc10.html", "Biodiversité des plantes et liens avec la santé humaine et animale"),
        ("fc11.html", "Écologie de la faune sauvage"),
        ("fc12_1.html", "Environnement, biodiversité, écologie, évolution des risques (partie 1)"),
        ("fc12_2.html", "Environnement, biodiversité, écologie, évolution des risques (partie 2)"),
    ]),
    ("Reglementation_Ethique_Recherche", "Réglementation et éthique de la recherche - droit de la santé", [
        ("fc1.html", "Droit de la santé"),
        ("fc2.html", "Réglementation et recherche de la santé"),
    ]),
    ("Technique_Vie_Societe", "Technique de vie et société", [
        ("fc1.html", "Vie, technique et société - Introduction"),
        ("fc2.html", "L\u2019éthique à l\u2019heure de la civilisation technologique"),
        ("fc3.html", "Le statut des objets techniques et des technologies dans le champ de la santé"),
        ("fc4.html", "Les droits et devoirs des patients et des praticiens"),
        ("fc5.html", "Le droit à l\u2019information médicale"),
        ("fc6.html", "Enjeux et statuts des objets biologiques"),
        ("fc7.html", "La pensée des bio-objets chez Céline Lafontaine"),
        ("fc8.html", "La technicisation médicale, une déshumanisation : précisions conceptuelles"),
        ("fc9.html", "La médecine humaniste face à la biomédecine"),
        ("fc10.html", "Les médecines alternatives : de la critique humaniste à l\u2019antiscience"),
        ("fc11.html", "Biomédecine et approche holistique : le modèle biopsychosocial"),
    ]),
]

# ── New subjects ──
NEW_SUBJECTS = [
    ("Biotechnologie", "Biotechnologie", "fa-flask", [
        ("fc1.html", "Introduction à la biotechnologie"),
        ("fc2.html", "Reprogrammation cellulaire"),
        ("fc3.html", "Drug Repositioning"),
        ("fc4.html", "Immunothérapie"),
        ("fc5.html", "Principes généraux de la thérapie génétique"),
        ("fc6.html", "Les vésicules extracellulaires"),
        ("fc7.html", "Bioproduction de cellules souches"),
        ("fc8.html", "Stratégies vaccinales"),
        ("fc9.html", "Édition du génome"),
        ("fc10.html", "Biomécanique des biomatériaux"),
        ("fc11.html", "Thérapie cellulaire et moelle osseuse"),
        ("fc12.html", "Peptides thérapeutiques antimicrobiens"),
    ]),
    ("SP_Promotion_Prevention", "Santé Publique - Promotion et prévention", "fa-heartbeat", [
        ("fc1.html", "Généralités en santé publique"),
        ("fc2.html", "Méthodologie de projet en prévention et promotion de la santé"),
        ("fc3.html", "Déterminants de santé"),
        ("fc4.html", "Méthodes de prévention et de dépistage"),
        ("fc5.html", "Vaccins et promotion de la prévention"),
        ("fc6.html", "Maladies sexuellement transmissibles"),
        ("fc7.html", "Initiation aux soins d\u2019urgence"),
        ("fc8.html", "Sédentarité et activité physique"),
        ("fc9.html", "Le risque cardio-vasculaire"),
    ]),
    ("SP_Economie_Sante", "Santé Publique - Économie de la santé", "fa-chart-line", [
        ("fc1.html", "Analyse économique de la perte d\u2019autonomie (Dépendance)"),
        ("fc2.html", "Analyse de la perte d\u2019autonomie : Handicap"),
        ("fc3.html", "Les modes de rémunération des médecins libéraux"),
        ("fc4.html", "Les modes de rémunération des établissements de santé"),
        ("fc5.html", "Nutrition, santé et croissance économique"),
        ("fc6.html", "Santé et développement : Santé et pauvreté"),
        ("fc7.html", "Santé et développement : Système et égalité"),
        ("fc8.html", "Santé et environnement"),
    ]),
    ("SP_Geographie_Sante", "Santé Publique - Géographie de la santé", "fa-map-marked-alt", [
        ("fc1.html", "Histoire et concepts de la géographie de la santé"),
        ("fc2.html", "Liens villes et santé : enjeux des usages de la carte en santé"),
        ("fc3.html", "Inégalités spatiales de l\u2019offre de soins en France"),
        ("fc4.html", "Enjeux internationaux des inégalités d\u2019offre de soins"),
        ("fc5.html", "Enjeux internationaux : le point de vue des patients"),
        ("fc6.html", "L\u2019accès aux soins des personnes vulnérables"),
        ("fc7.html", "Alimentation et santé en ville"),
        ("fc8.html", "Pouvoirs des villes et urbanisme favorable à la santé : espaces verts"),
        ("fc9.html", "Urbanisme favorable à la santé : personnes âgées"),
        ("fc10.html", "Urbanisme favorable à la santé : enfants"),
    ]),
    ("SP_Gestion_Projet_RC", "Santé Publique - Gestion de projet de recherche clinique", "fa-clipboard-list", [
        ("fc1.html", "Généralités sur les essais cliniques"),
        ("fc2.html", "Acteurs de la recherche clinique"),
        ("fc3.html", "Vigilance, gestion des EIG et sécurité des essais cliniques"),
        ("fc4.html", "Structures de soutien à la recherche clinique"),
        ("fc5.html", "Mise en place d\u2019un essai clinique"),
        ("fc6.html", "Le dossier patient, les CRF et les bases de données"),
        ("fc7.html", "Gestion de projet (Le monitoring)"),
        ("fc8.html", "Réglementation sur les échantillons biologiques"),
        ("fc9.html", "Démarches auprès du MESRI"),
    ]),
]

ALL_SUBJECTS = EXISTING_SUBJECTS + [(s[0], s[1], s[3]) for s in NEW_SUBJECTS]

def build_sidebar(prefix="./"):
    lines = ['<nav id="menu">\n<header class="major"><h2>Menu</h2></header>\n<ul>\n<li><a href="' + prefix + 'index.html">Accueil</a></li>\n<li><a href="' + prefix + 'favorites.html">Favoris</a></li>']
    for dir_name, display, courses in ALL_SUBJECTS:
        lines.append(f'<li><span class="opener">{display}</span><ul>')
        for fname, title in courses:
            lines.append(f'<li><a href="{prefix}{dir_name}/{fname}">{title}</a></li>')
        lines.append('</ul></li>')
    lines.append('</ul></nav>')
    return "\n".join(lines)

def get_all_course_paths():
    paths = []
    for dir_name, _, courses in ALL_SUBJECTS:
        for fname, _ in courses:
            paths.append(f"'{dir_name}/{fname}'")
    return paths

def build_course_html(subject_display, course_title, flashcards_data, page_id):
    sidebar = build_sidebar("../")
    js_data = flashcards_js(flashcards_data)
    return f'''<!DOCTYPE HTML>
<html>
<head>
<title>Diploma Santé - Plateforme de Flashcards</title>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
<link rel="stylesheet" href="../../assets/css/main.css" />
<link rel="icon" type="image/jpeg" href="../../images/diploma.jpeg" />
<script src="../../assets/js/favorites.js"></script>
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
<header class="main"><div class="header-left"><h1>{subject_display}</h1><h2>{course_title}</h2></div><span class="image main"><img src="../../images/banner.png" alt="" /></span></header>

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
  .check-icon:hover {{ color: green; }}
  .cross-icon:hover {{ stroke: red; }}
  body.dark-mode .flashcard-front {{ background-color: #2d3436; color: #e2e8f0; box-shadow: inset 0 0 40px rgba(0, 174, 239, 0.1); }}
  body.dark-mode .flashcard-inner {{ background-color: #2d3436; box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4); }}
  body.dark-mode .flashcard-back {{ background-color: #1a6fa0; }}
  body.dark-mode .progress-container {{ background-color: #4a5568; border-color: #2d3748; }}
  @media (max-width: 736px) {{
    .flashcard-front, .flashcard-back {{ font-size: 1.3rem; padding: 1.5rem; }}
    .flashcard {{ min-height: 320px; height: calc(100vh - 300px); }}
    .check-icon, .cross-icon {{ width: 35px; height: 35px; top: 15px; }}
    .check-icon {{ left: 15px; }}
    .cross-icon {{ right: 15px; }}
    .favorite-icon {{ width: 24px; height: 24px; }}
    header.main {{ flex-direction: column; gap: 1rem; }}
    header.main h1 {{ font-size: 1.5em !important; }}
    header.main h2 {{ font-size: 1.1em !important; }}
  }}
</style>

<div id="progress-text" style="text-align:center;font-size:1rem;color:#00aeef;font-weight:600;margin-bottom:0.3rem;"></div>
<div class="progress-container"><div class="progress-bar" id="progress-bar"></div></div>

<div class="flashcards-container">
<div class="flashcard" id="flashcard" onclick="toggleAnswer()">
<div class="flashcard-inner">
<div class="flashcard-front" id="flashcard-question"></div>
<div class="flashcard-back" id="flashcard-answer"></div>
<div class="check-icon" id="check-icon" onclick="event.stopPropagation(); markCorrect()"><i class="fas fa-check"></i></div>
<svg class="cross-icon" id="cross-icon" onclick="event.stopPropagation(); markWrong()" viewBox="0 0 24 24" fill="none" stroke-width="2.5" stroke-linecap="round"><line x1="4" y1="4" x2="20" y2="20"/><line x1="20" y1="4" x2="4" y2="20"/></svg>
<svg class="favorite-icon" id="favorite-icon" onclick="event.stopPropagation(); toggleFavorite()" viewBox="0 0 24 24"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>
</div>
</div>
<div class="flashcard-button">
<button class="button small" onclick="previousCard()" aria-label="Carte précédente"><i class="fas fa-chevron-left"></i></button>
<button class="button small" onclick="nextCard()" aria-label="Carte suivante"><i class="fas fa-chevron-right"></i></button>
<button class="button small" onclick="shuffleCards()"><i class="fas fa-random"></i></button>
<button class="button small" onclick="resetProgress()"><i class="fas fa-redo"></i></button>
</div>
</div>

</section>
</div>
</div>

<div id="sidebar">
<div class="inner">
<section id="search" class="alt"><form method="post" action="#"><input type="text" name="query" id="query" placeholder="Rechercher"></form></section>
{sidebar}
<footer id="footer"><p class="copyright">&copy; Diploma Santé. Tous droits réservés.</p></footer>
</div>
</div>

</div>

<script src="../../assets/js/jquery.min.js"></script>
<script src="../../assets/js/browser.min.js"></script>
<script src="../../assets/js/breakpoints.min.js"></script>
<script src="../../assets/js/util.js"></script>
<script src="../../assets/js/main.js"></script>
<script src="../../assets/js/darkmode.js"></script>
<script>
const PAGE_ID = '{page_id}';
const SECTION = 'LSPS3_S2';

const flashcardsData = [
{js_data}
];

let currentIndex = 0;
let showingAnswer = false;
let progress = {{}};
let cardOrder = [];

function loadProgress() {{
  try {{ progress = JSON.parse(localStorage.getItem('progress_' + PAGE_ID) || '{{}}'); }} catch(e) {{ progress = {{}}; }}
  cardOrder = [];
  for (let i = 0; i < flashcardsData.length; i++) cardOrder.push(i);
}}

function saveProgress() {{
  localStorage.setItem('progress_' + PAGE_ID, JSON.stringify(progress));
  checkCompletion();
}}

function checkCompletion() {{
  const total = flashcardsData.length;
  let correct = 0;
  for (let k in progress) if (progress[k] === 'correct') correct++;
  if (correct === total) localStorage.setItem('completed_' + PAGE_ID, 'true');
  else localStorage.removeItem('completed_' + PAGE_ID);
}}

function updateProgress() {{
  const total = flashcardsData.length;
  let answered = 0;
  for (let k in progress) if (progress[k]) answered++;
  const pct = Math.round((answered / total) * 100);
  document.getElementById('progress-bar').style.width = pct + '%';
  document.getElementById('progress-text').textContent = answered + ' / ' + total + ' (' + pct + '%)';
}}

function displayCard() {{
  const idx = cardOrder[currentIndex];
  const card = flashcardsData[idx];
  document.getElementById('flashcard-question').innerHTML = card.question;
  document.getElementById('flashcard-answer').innerHTML = card.answer;
  document.getElementById('flashcard').classList.remove('show-answer');
  showingAnswer = false;
  const state = progress[idx];
  const ci = document.getElementById('check-icon');
  const xi = document.getElementById('cross-icon');
  ci.style.color = (state === 'correct') ? 'green' : '#888';
  xi.style.stroke = (state === 'wrong') ? 'red' : '#888';
  if (typeof updateFavoriteIcon === 'function') updateFavoriteIcon(idx);
  updateProgress();
}}

function toggleAnswer() {{ document.getElementById('flashcard').classList.toggle('show-answer'); showingAnswer = !showingAnswer; }}
function nextCard() {{ currentIndex = (currentIndex + 1) % cardOrder.length; displayCard(); }}
function previousCard() {{ currentIndex = (currentIndex - 1 + cardOrder.length) % cardOrder.length; displayCard(); }}
function markCorrect() {{ progress[cardOrder[currentIndex]] = 'correct'; saveProgress(); nextCard(); }}
function markWrong() {{ progress[cardOrder[currentIndex]] = 'wrong'; saveProgress(); nextCard(); }}
function shuffleCards() {{ for (let i = cardOrder.length - 1; i > 0; i--) {{ const j = Math.floor(Math.random() * (i + 1)); [cardOrder[i], cardOrder[j]] = [cardOrder[j], cardOrder[i]]; }} currentIndex = 0; displayCard(); }}
function resetProgress() {{ if (confirm('Réinitialiser la progression ?')) {{ progress = {{}}; localStorage.removeItem('progress_' + PAGE_ID); localStorage.removeItem('completed_' + PAGE_ID); displayCard(); }} }}

document.addEventListener('DOMContentLoaded', function() {{
  loadProgress();
  displayCard();
  initFavorites(PAGE_ID, SECTION, flashcardsData);
}});

document.addEventListener('keydown', function(e) {{
  if (e.key === 'ArrowRight') nextCard();
  else if (e.key === 'ArrowLeft') previousCard();
  else if (e.key === ' ') {{ e.preventDefault(); toggleAnswer(); }}
}});
</script>

</body>
</html>'''

# Import flashcard data files
import importlib.util

def load_data_module(path):
    spec = importlib.util.spec_from_file_location("data", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def main():
    scripts_dir = Path(__file__).resolve().parent

    # Load all flashcard data
    data_files = sorted(scripts_dir.glob("l3_data_*.py"))
    all_flashcards = {}
    for df in data_files:
        mod = load_data_module(str(df))
        if hasattr(mod, 'FLASHCARDS'):
            all_flashcards.update(mod.FLASHCARDS)

    print(f"Loaded {len(all_flashcards)} courses from {len(data_files)} data files")

    # Create directories
    for subj_dir, _, _, _ in NEW_SUBJECTS:
        (OUT_DIR / subj_dir).mkdir(parents=True, exist_ok=True)

    # Generate course HTML files
    total_files = 0
    total_cards = 0
    for subj_dir, subj_display, _, courses in NEW_SUBJECTS:
        for fname, title in courses:
            key = f"{subj_dir}/{fname}"
            if key not in all_flashcards:
                print(f"  WARNING: No flashcard data for {key}")
                continue
            cards = all_flashcards[key]
            page_id = "lsps3_" + key.replace(".html", "").replace("/", "_")
            html = build_course_html(subj_display, title, cards, page_id)
            outpath = OUT_DIR / subj_dir / fname
            outpath.write_text(html, encoding="utf-8")
            print(f"  Wrote {subj_dir}/{fname} ({len(cards)} cards) - {title}")
            total_files += 1
            total_cards += len(cards)

    # Update existing course sidebars
    update_existing_sidebars()

    # Update index.html
    update_index()

    # Update favorites.html
    update_favorites()

    print(f"\nDone! Generated {total_files} new course files with {total_cards} total flashcards.")

def update_existing_sidebars():
    """Update sidebar in all existing course HTML files."""
    new_sidebar = build_sidebar("../")
    count = 0
    for subj_dir, _, _ in ALL_SUBJECTS:
        dir_path = OUT_DIR / subj_dir
        if not dir_path.exists():
            continue
        for html_file in dir_path.glob("*.html"):
            content = html_file.read_text(encoding="utf-8")
            # Replace the nav#menu block
            pattern = r'<nav id="menu">.*?</nav>'
            if re.search(pattern, content, re.DOTALL):
                new_content = re.sub(pattern, new_sidebar, content, flags=re.DOTALL)
                if new_content != content:
                    html_file.write_text(new_content, encoding="utf-8")
                    count += 1
    print(f"  Updated sidebar in {count} existing files")

def update_index():
    """Update UPEC_LSPS3_S2/index.html with new matière cards and course paths."""
    idx_path = OUT_DIR / "index.html"
    content = idx_path.read_text(encoding="utf-8")

    # Build new matière cards HTML
    new_cards = ""
    for subj_dir, subj_display, icon, courses in NEW_SUBJECTS:
        new_cards += f'''<div class="matiere-card">
<span class="icon solid {icon}"></span>
<h3>{subj_display}</h3>
<a href="{subj_dir}/{courses[0][0]}" class="button">Commencer</a>
</div>
'''

    # Insert before </div></section>
    content = content.replace('</div>\n</section>', new_cards + '</div>\n</section>')

    # Replace sidebar
    new_sidebar = build_sidebar("./")
    content = re.sub(r'<nav id="menu">.*?</nav>', new_sidebar, content, flags=re.DOTALL)

    # Replace COURSE_PATHS
    all_paths = get_all_course_paths()
    paths_js = ",\n".join(all_paths)
    content = re.sub(
        r"const COURSE_PATHS = \[.*?\];",
        f"const COURSE_PATHS = [\n{paths_js}\n];",
        content,
        flags=re.DOTALL
    )

    idx_path.write_text(content, encoding="utf-8")
    print(f"  Updated index.html ({len(all_paths)} course paths)")

def update_favorites():
    """Update favorites.html sidebar."""
    fav_path = OUT_DIR / "favorites.html"
    if not fav_path.exists():
        return
    content = fav_path.read_text(encoding="utf-8")
    new_sidebar = build_sidebar("./")
    content = re.sub(r'<nav id="menu">.*?</nav>', new_sidebar, content, flags=re.DOTALL)
    fav_path.write_text(content, encoding="utf-8")
    print("  Updated favorites.html sidebar")

if __name__ == "__main__":
    main()

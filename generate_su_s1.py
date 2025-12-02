#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de génération de la plateforme SU_S1 à partir des fichiers JavaScript
du dossier "flashcard su/"
"""

import os
import re
import json
from pathlib import Path
from collections import defaultdict

# Mapping des dossiers source vers les dossiers cibles
MATIERE_MAPPING = {
    'anatomie': 'Anatomie_Socle',
    'biocell': 'Biologie_Cellulaire',
    'biochimie': 'Biochimie_Socle',
    'bdd': 'Biologie_Developpement',
    'BDR': 'Biologie_Reproduction',
    'histologie': 'Histologie'
}

# Mapping des préfixes de fichiers HTML
FILE_PREFIX_MAPPING = {
    'anatomie': 'anat',
    'biocell': 'biocell',
    'biochimie': 'bioch',
    'bdd': 'bdd',
    'BDR': 'bdr',
    'histologie': 'hist'
}

# Mapping des noms de matières pour les titres
MATIERE_TITLES = {
    'anatomie': 'Anatomie',
    'biocell': 'Biologie cellulaire',
    'biochimie': 'Biochimie',
    'bdd': 'Biologie du développement',
    'BDR': 'Biologie de la reproduction',
    'histologie': 'Histologie'
}

# Icônes pour les matières dans index.html
MATIERE_ICONS = {
    'anatomie': 'fa-user-md',
    'biocell': 'fa-dna',
    'biochimie': 'fa-flask',
    'bdd': 'fa-seedling',
    'BDR': 'fa-heartbeat',
    'histologie': 'fa-microscope'
}

def parse_flashcard_file(file_path):
    """Parse un fichier JS et extrait les flashcards"""
    flashcards = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern pour matcher les objets flashcard avec gestion des apostrophes échappées
        # Format: { question: '...', answer: '...', }
        # On utilise un pattern plus robuste qui gère les apostrophes simples et doubles
        pattern = r"\{\s*question:\s*['\"](.*?)(?<!\\)['\"],\s*answer:\s*['\"](.*?)(?<!\\)['\"],\s*\}"
        
        # Essayer d'abord avec le pattern simple
        matches = list(re.finditer(pattern, content, re.DOTALL))
        
        if not matches:
            # Si ça ne marche pas, essayer ligne par ligne
            lines = content.split('\n')
            for line in lines:
                line = line.strip()
                if not line or line.startswith('//') or not line.startswith('{'):
                    continue
                
                # Pattern pour une ligne complète
                line_pattern = r"\{\s*question:\s*['\"](.*?)['\"],\s*answer:\s*['\"](.*?)['\"],\s*\}"
                match = re.search(line_pattern, line, re.DOTALL)
                if match:
                    question = match.group(1)
                    answer = match.group(2)
                    # Déséchapper les apostrophes
                    question = question.replace("\\'", "'").replace('\\"', '"')
                    answer = answer.replace("\\'", "'").replace('\\"', '"')
                    flashcards.append({
                        'question': question,
                        'answer': answer
                    })
        else:
            for match in matches:
                question = match.group(1)
                answer = match.group(2)
                # Déséchapper les apostrophes
                question = question.replace("\\'", "'").replace('\\"', '"')
                answer = answer.replace("\\'", "'").replace('\\"', '"')
                flashcards.append({
                    'question': question,
                    'answer': answer
                })
        
    except Exception as e:
        print(f"Erreur lors du parsing de {file_path}: {e}")
        import traceback
        traceback.print_exc()
    
    return flashcards

def extract_course_title(filename):
    """Extrait et formate le titre du cours depuis le nom du fichier"""
    # Enlever l'extension .js
    name = filename.replace('.js', '')
    
    # Enlever les numéros au début (ex: "1 ", "2.1 ", "5.1 ")
    name = re.sub(r'^\d+\.?\d*\s*', '', name)
    
    # Remplacer les underscores par des espaces
    name = name.replace('_', ' ')
    
    # Capitaliser chaque mot (title case)
    words = name.split()
    capitalized_words = []
    for word in words:
        if word:
            # Capitaliser la première lettre
            word = word[0].upper() + word[1:].lower()
            capitalized_words.append(word)
    name = ' '.join(capitalized_words)
    
    # Corriger quelques mots courants
    name = name.replace(' A ', ' à ')
    name = name.replace(' De ', ' de ')
    name = name.replace(' Du ', ' du ')
    name = name.replace(' Des ', ' des ')
    name = name.replace(' La ', ' la ')
    name = name.replace(' Le ', ' le ')
    name = name.replace(' Les ', ' les ')
    name = name.replace(' Et ', ' et ')
    name = name.replace(' Ou ', ' ou ')
    
    # Gérer les parties (ex: "partie 1", "Partie 2")
    if 'partie' in name.lower():
        name = re.sub(r'(\w+)\s+partie\s+(\d+)', r'\1 (Partie \2)', name, flags=re.IGNORECASE)
    
    # Capitaliser la première lettre du titre complet
    if name:
        name = name[0].upper() + name[1:]
    
    return name

def normalize_filename(filename):
    """Normalise le nom de fichier pour créer un nom HTML"""
    # Enlever l'extension
    name = filename.replace('.js', '')
    
    # Extraire le numéro
    match = re.match(r'^(\d+)\.?(\d*)\s*', name)
    if match:
        num = match.group(1)
        if match.group(2):
            num += '_' + match.group(2).replace('.', '_')
        return num
    return '1'

def get_template_html():
    """Retourne le template HTML de base"""
    return '''<!DOCTYPE HTML>
<html>
<head>
<title>Diploma Santé - Plateforme de Flashcards</title>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
<link rel="stylesheet" href="../../assets/css/main.css" />
<link rel="icon" type="image/jpeg" href="../../images/diploma.jpeg" />
    <script src="../../security.js" defer></script>
    <script src="../../assets/js/favorites.js"></script>
</head>
<body class="is-preload">

<!-- Wrapper -->
<div id="wrapper">

<!-- Main -->
<div id="main">
<div class="inner">

<!-- Header -->
<header id="header">
<a href="../../index.html" class="logo"><strong>Diploma Santé</strong>- Plateforme de Flashcards</a>
<ul class="icons">
<li><a href="https://diploma-sante.fr/" class="icon fas fa-globe"><span class="label"></span></a></li>
<li><a href="https://www.instagram.com/diplomasante/" class="icon brands fa-instagram"><span class="label">Instagram</span></a></li>
        <li><a href="#" id="dark-mode-toggle" class="icon fas fa-moon"></a></li>
</ul>
</header>

<!-- Content -->
<section>
<header class="main"><div class="header-left"><h1>{MATIERE_TITLE}</h1><h2>{COURSE_TITLE}</h2></div><span class="image main"><img src="../../images/banner.png" alt="" /></span></header>

					<style>  /* Header minimal avec contrôles accessibles */
  #header {
    padding: 1rem 0;
    margin-bottom: 0.5rem;
  }

  /* Section contenu compacte en 2 colonnes */
  header.main {
    margin-top: 1.5rem !important;
    margin-bottom: 0.8rem !important;
    padding-bottom: 0.5rem !important;
    display: flex;
    align-items: center;
    gap: 2rem;
  }
  
  header.main .header-left h1,
  header.main .header-left h2 {
    flex: 1;
    margin: 0 !important;
  }
  
  header.main h1 {
    font-size: 2em !important;
    line-height: 1.3 !important;
  }
  
  header.main h2 {
    font-size: 1.3em !important;
    color: #7f888f !important;
  }
  header.main .header-left {
    flex: 1;
    display: flex;
    flex-direction: column;
  }
  
  header.main .header-left h1,
  header.main .header-left h2 {
    margin: 0 !important;
  }

  
  .image.main {
    flex: 1;
    max-height: none !important;
    overflow: visible !important;
    margin: 0 !important;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .image.main img {
    width: 100% !important;
    height: auto !important;
    max-height: 120px !important;
    object-fit: contain !important;
    object-position: center;
  }
  
  section {
    padding-top: 0 !important;
  }

  /* Barre de progression cohérente */
  .progress-container {
    width: 100%;
    max-width: 1000px;
    height: 20px;
    background-color: #eee;
    border-radius: 10px;
    overflow: hidden;
    margin: 0 auto 1rem;
    border: 1px solid #ddd;
  }

  .progress-bar {
    height: 100%;
    background-color: #00aeef;
    width: 0%;
    transition: width 0.3s;
  }



  /* Flashcards plein écran optimisées */
  .flashcards-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 2rem;
    min-height: calc(100vh - 250px);
    padding: 1rem 0;
  }

  .flashcard {
    width: 100%;
    max-width: 1000px;
    height: calc(100vh - 340px);
    min-height: 450px;
    perspective: 1500px;
    cursor: pointer;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    position: relative;
  }

  .flashcard-inner {
    position: relative;
    width: 100%;
    height: 100%;
    border-radius: 20px;
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.25);
    background-color: white;
    transition: transform 0.6s;
    transform-style: preserve-3d;
  }

  .flashcard.show-answer .flashcard-inner {
    transform: rotateY(180deg);
  }

  .flashcard-front,
  .flashcard-back {
    position: absolute;
    width: 100%;
    height: 100%;
    border-radius: 20px;
    backface-visibility: hidden;
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 3rem;
    font-size: 2rem;
    text-align: center;
  }

  .flashcard-front {
    background-color: white;
    color: #333;
    box-shadow: inset 0 0 40px rgba(0, 174, 239, 0.15);
  }

  .flashcard-back {
    background-color: #73C3EC;
    color: white;
    transform: rotateY(180deg);
    box-shadow: inset 0 0 50px rgba(255, 255, 255, 0.5);
    font-size: 2.2rem;
    text-shadow: 0 0 4px rgba(255, 255, 255, 0.3);
  }

  .flashcard-button {
    margin-top: 1rem;
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    width: 100%;
    flex-wrap: wrap;
  }

  /* Boutons repositionnés DANS flashcard-inner */
  .check-icon,
  .cross-icon,
  .favorite-icon {
    display: none;
    position: absolute;
    font-size: 2.5rem;
    cursor: pointer;
    z-index: 100;
    transition: all 0.3s;
    opacity: 0.8;
  }

  .check-icon {
    top: 15px;
    right: 15px;
    stroke: #888;
  }

  .cross-icon {
    top: 15px;
    left: 15px;
    stroke: #888;
  }

  .favorite-icon {
    top: 15px;
    left: 50%;
    transform: translateX(-50%);
    fill: #888;
    width: 30px;
    height: 30px;
  }

  .favorite-icon.active {
    fill: #ffd700;
  }

  .flashcard.show-answer .check-icon,
  .flashcard.show-answer .cross-icon,
  .flashcard.show-answer .favorite-icon {
    display: block;
  }

  .check-icon:hover {
    stroke: #27ae60;
    opacity: 1;
  }

  .cross-icon:hover {
    stroke: #e74c3c;
    opacity: 1;
  }

  .favorite-icon:hover {
    opacity: 1;
    transform: translateX(-50%) scale(1.1);
  }

  .slide-left {
    animation: slideLeft 0.4s forwards;
  }

  .slide-right {
    animation: slideRight 0.4s forwards;
  }

  @keyframes slideLeft {
    from {
      transform: translateX(0);
      opacity: 1;
    }
    to {
      transform: translateX(-100%);
      opacity: 0;
    }
  }

  @keyframes slideRight {
    from {
      transform: translateX(0);
      opacity: 1;
    }
    to {
      transform: translateX(100%);
      opacity: 0;
    }
  }

  /* Dark mode support */
  body.dark-mode .flashcard-front {
    background-color: #2d3436;
    color: #e2e8f0;
  }

  body.dark-mode .flashcard-inner {
    background-color: #2d3436;
  }

  body.dark-mode .progress-container {
    background-color: #34495e;
    border-color: #4a5568;
  }

  @media screen and (max-width: 768px) {
    .flashcard {
      width: 95vw;
      height: calc(100vh - 180px);
      min-height: 450px;
    }
    
    ul.actions {
      padding-right: 0;
      text-align: center;
    }
  }
</style>

</head>
<body>
<div class="progress-container">
  <div class="progress-bar" id="progressBar"></div>
</div>
 <div class="flashcards-container" id="flashcards"></div>
 

 <script>

const flashcardsData =
[
{FLASHCARDS_DATA}
]
;
    
const container = document.getElementById("flashcards");
const progressBar = document.getElementById("progressBar");
const originalData = [...flashcardsData];
let flashcards = [...originalData];
const pageId = location.pathname.split("/" ).pop().replace(".html","");
const progressKey = "progress_" + pageId;
let currentIndex = parseInt(localStorage.getItem(progressKey)) || 0;

function updateProgress() {
  const total = originalData.length;
  const progress = Math.min(currentIndex / total, 1);
  progressBar.style.width = `${progress * 100}%`;
}

function createContent(content) {
  if (typeof content === "string") {
    // Texte simple
    const div = document.createElement("div");
    div.textContent = content;
    return div;
  }
  if (typeof content === "object" && content.type === "image") {
    // Contenu image avec option caption
    const wrapper = document.createElement("div");
    wrapper.style.textAlign = "center";

    if (content.caption) {
      const caption = document.createElement("div");
      caption.textContent = content.caption;
      caption.style.marginBottom = "6px";
      caption.style.fontStyle = "italic";
      caption.style.fontSize = "0.9em";
      wrapper.appendChild(caption);
    }

    const img = document.createElement("img");
    img.src = content.src;
    img.alt = content.alt || "";
    img.style.maxWidth = "100%";
    img.style.height="auto"; img.style.maxHeight="150px"; img.style.objectFit="contain";

    wrapper.appendChild(img);
    return wrapper;
  }
  // Par défaut : rien
  return document.createElement("div");
}

function showCard(index) {
  container.innerHTML = "";

  if (flashcards[index]) {
    const { question, answer } = flashcards[index];

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
    resetBtn.addEventListener("click", (e) => {
      e.stopPropagation();
      localStorage.removeItem(progressKey);
      localStorage.removeItem("completed_" + pageId);
      flashcards = [...originalData];
      currentIndex = 0;
      updateProgress();
      showCard(currentIndex);
    });

    btnContainer.appendChild(toggleBtn);
    btnContainer.appendChild(resetBtn);


    const checkIcon = document.createElement("span");
    checkIcon.classList.add("check-icon");
    checkIcon.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="none" stroke="#888" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
        <polyline points="20 6 9 17 4 12" />
      </svg>
    `;
    checkIcon.addEventListener("click", (e) => {
      e.stopPropagation();
      card.classList.add("slide-right");
      setTimeout(() => {
        currentIndex++;
        localStorage.setItem(progressKey, currentIndex);
        updateProgress();
        showCard(currentIndex);
      }, 400);
    });

    const crossIcon = document.createElement("span");
    crossIcon.classList.add("cross-icon");
    crossIcon.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" width="30" height="30" fill="none" stroke="#888" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
        <line x1="18" y1="6" x2="6" y2="18" />
        <line x1="6" y1="6" x2="18" y2="18" />
      </svg>
    `;
    crossIcon.addEventListener("click", (e) => {
      e.stopPropagation();
      card.classList.add("slide-left");
      setTimeout(() => {
        // On fait tourner la carte : on la met 5 cartes plus loin
        const removed = flashcards.splice(currentIndex, 1)[0];
        flashcards.splice(currentIndex + 5, 0, removed);
        showCard(currentIndex);
      }, 400);
    });

        const favIcon = document.createElement("span");
    favIcon.classList.add("favorite-icon");
    favIcon.innerHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="30" height="30"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"/></svg>`;
    function updateFav() {
      if (isFavorite({question, answer})) favIcon.classList.add("active");
      else favIcon.classList.remove("active");
    }
    favIcon.addEventListener("click", (e) => {
      e.stopPropagation();
      toggleFavorite({question, answer});
      updateFav();
    });
    updateFav();
card.addEventListener("click", () => {
      const isAnswerVisible = card.classList.toggle("show-answer");
      toggleBtn.textContent = isAnswerVisible ? "Cacher la réponse" : "Voir la réponse";
    });

    inner.appendChild(front);
    inner.appendChild(back);
    inner.appendChild(checkIcon);
    inner.appendChild(crossIcon);
    inner.appendChild(favIcon);
    card.appendChild(inner);
    card.appendChild(btnContainer);

    container.appendChild(card);
  } else {
    container.innerHTML = "<p>Plus de flashcards disponibles.</p>";
    localStorage.setItem("completed_" + pageId, "true");
    updateProgress();
  }
}



showCard(currentIndex);
updateProgress();



</script>




</section>

</div>
</div>

<!-- Sidebar -->
<div id="sidebar">
<div class="inner">

<!-- Menu -->
<!-- Menu -->
<section id="search" class="alt">
<form method="post" action="#">
<input type="text" name="query" id="query" placeholder="Rechercher">
</form>
</section>
<nav id="menu">
                  <header class="major">
                    <h2>Menu</h2>
                  </header>
                  <ul>
                    <li><a href="../../index.html">Accueil</a></li>
                    <li><a href="../../favorites.html">Favoris</a></li>
{MENU_ITEMS}
                  </ul>
                </nav>


<!-- Footer -->
<footer id="footer">
<p class="copyright">&copy; Diploma Santé. Tous droits réservés.</p>
</footer>

</div>
</div>

</div>

<!-- Scripts -->
<script src="../../assets/js/jquery.min.js"></script>
<script src="../../assets/js/browser.min.js"></script>
<script src="../../assets/js/breakpoints.min.js"></script>
<script src="../../assets/js/util.js"></script>
<script src="../../assets/js/main.js"></script>
<script src="../../assets/js/darkmode.js"></script>
<script src="../../assets/js/favorites.js"></script>

</body>
</html>'''

def escape_js_string(s):
    """Échappe une chaîne pour JavaScript"""
    # Remplacer dans l'ordre: d'abord les backslashes, puis les apostrophes
    s = s.replace('\\', '\\\\')
    s = s.replace("'", "\\'")
    s = s.replace('\n', '\\n')
    s = s.replace('\r', '\\r')
    return s

def format_flashcards_data(flashcards):
    """Formate les flashcards en JavaScript"""
    lines = []
    for card in flashcards:
        q = escape_js_string(card['question'])
        a = escape_js_string(card['answer'])
        lines.append(f"  {{ question: '{q}', answer: '{a}' }}")
    return ',\n'.join(lines)

def main():
    base_dir = Path(__file__).parent
    source_dir = base_dir / 'flashcard su'
    target_dir = base_dir / 'SU_S1'
    
    # Créer le dossier SU_S1
    target_dir.mkdir(exist_ok=True)
    
    # Structure pour stocker tous les cours par matière
    all_courses = defaultdict(list)
    
    # Parcourir tous les fichiers JS
    for matiere_dir in source_dir.iterdir():
        if not matiere_dir.is_dir():
            continue
        
        matiere_name = matiere_dir.name
        if matiere_name not in MATIERE_MAPPING:
            print(f"Matière non mappée ignorée: {matiere_name}")
            continue
        
        target_matiere_dir = target_dir / MATIERE_MAPPING[matiere_name]
        target_matiere_dir.mkdir(exist_ok=True)
        
        # Lister tous les fichiers JS dans ce dossier
        js_files = sorted([f for f in matiere_dir.iterdir() if f.suffix == '.js'])
        
        file_counter = 1
        for js_file in js_files:
            print(f"Traitement de {js_file}...")
            
            # Parser les flashcards
            flashcards = parse_flashcard_file(js_file)
            
            if not flashcards:
                print(f"  Avertissement: Aucune flashcard trouvée dans {js_file}")
                continue
            
            # Extraire le titre du cours
            course_title = extract_course_title(js_file.name)
            
            # Générer le nom du fichier HTML
            file_prefix = FILE_PREFIX_MAPPING[matiere_name]
            html_filename = f"{file_prefix}{file_counter}.html"
            html_path = target_matiere_dir / html_filename
            
            # Générer le contenu HTML
            flashcards_data = format_flashcards_data(flashcards)
            matiere_title = MATIERE_TITLES[matiere_name]
            
            # Pour le menu, on va le générer plus tard
            menu_items = "<!-- Menu généré dans index.html -->"
            
            # Utiliser replace au lieu de format pour éviter les problèmes avec les accolades CSS
            html_content = get_template_html()
            html_content = html_content.replace('{MATIERE_TITLE}', matiere_title)
            html_content = html_content.replace('{COURSE_TITLE}', course_title)
            html_content = html_content.replace('{FLASHCARDS_DATA}', flashcards_data)
            html_content = html_content.replace('{MENU_ITEMS}', menu_items)
            
            # Écrire le fichier HTML
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"  Créé: {html_path} ({len(flashcards)} flashcards)")
            
            # Stocker les infos pour le menu
            all_courses[matiere_name].append({
                'filename': html_filename,
                'title': course_title,
                'path': f"{MATIERE_MAPPING[matiere_name]}/{html_filename}"
            })
            
            file_counter += 1
    
    # Générer l'index.html
    print("\nGénération de index.html...")
    generate_index_html(target_dir, all_courses)
    
    # Mettre à jour les menus dans tous les fichiers HTML
    print("\nMise à jour des menus dans les fichiers HTML...")
    update_menus_in_html_files(target_dir, all_courses)
    
    print("\nGénération terminée!")

def generate_index_html(target_dir, all_courses):
    """Génère le fichier index.html"""
    # Lire le template USPN_S1/index.html
    template_path = Path(__file__).parent / 'USPN_S1' / 'index.html'
    
    with open(template_path, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Remplacer USPN par SU
    content = template_content.replace('USPN S1', 'SU S1')
    content = content.replace('USPN - Semestre 1', 'SU - Semestre 1')
    content = content.replace("étudiants de l'USPN", "étudiants de SU")
    
    # Générer la section features
    features_html = []
    for matiere_name in ['anatomie', 'biocell', 'biochimie', 'bdd', 'BDR', 'histologie']:
        if matiere_name not in all_courses or not all_courses[matiere_name]:
            continue
        
        matiere_title = MATIERE_TITLES[matiere_name]
        icon = MATIERE_ICONS[matiere_name]
        first_course = all_courses[matiere_name][0]
        first_path = first_course['path']
        
        features_html.append(f'''										<article>
											<span class="icon solid {icon}"></span>
											<div class="content">
												<h3>{matiere_title}</h3>
												<ul class="actions">
													<li><a href="{first_path}" class="button big">Commencer</a></li>
												</ul>
											</div>
										</article>''')
    
    # Remplacer la section features
    features_pattern = r'<div class="features">.*?</div>\s*</section>'
    new_features = f'<div class="features">\n' + '\n'.join(features_html) + '\n									</div>\n								</section>'
    content = re.sub(features_pattern, new_features, content, flags=re.DOTALL)
    
    # Générer le menu
    menu_html = []
    for matiere_name in ['anatomie', 'biocell', 'biochimie', 'bdd', 'BDR', 'histologie']:
        if matiere_name not in all_courses or not all_courses[matiere_name]:
            continue
        
        matiere_title = MATIERE_TITLES[matiere_name]
        courses = all_courses[matiere_name]
        
        menu_items = []
        for course in courses:
            menu_items.append(f'<li><a href="{course["path"]}">{course["title"]}</a></li>')
        
        menu_html.append(f'''									<li>
										<span class="opener">{matiere_title}</span>
										<ul>
{chr(10).join(menu_items)}
										</ul>
									</li>''')
    
    # Remplacer le menu
    menu_pattern = r'<ul>\s*<li><a href="index.html">Accueil</a></li>.*?</ul>\s*</nav>'
    new_menu = f'''<ul>
									<li><a href="index.html">Accueil</a></li>
									<li><a href="../favorites.html">Favoris</a></li>
{chr(10).join(menu_html)}
								</ul>'''
    content = re.sub(menu_pattern, new_menu, content, flags=re.DOTALL)
    
    # Calculer le total de cours
    total_courses = sum(len(courses) for courses in all_courses.values())
    content = content.replace('const total = 79;', f'const total = {total_courses};')
    
    # Écrire le fichier
    index_path = target_dir / 'index.html'
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"  Créé: {index_path}")

def update_menus_in_html_files(target_dir, all_courses):
    """Met à jour les menus dans tous les fichiers HTML"""
    # Générer le menu complet
    menu_html = []
    for matiere_name in ['anatomie', 'biocell', 'biochimie', 'bdd', 'BDR', 'histologie']:
        if matiere_name not in all_courses or not all_courses[matiere_name]:
            continue
        
        matiere_title = MATIERE_TITLES[matiere_name]
        courses = all_courses[matiere_name]
        
        menu_items = []
        for course in courses:
            menu_items.append(f'<li><a href="../{course["path"]}">{course["title"]}</a></li>')
        
        menu_html.append(f'''                    <li>
                      <span class="opener">{matiere_title}</span>
                      <ul>
{chr(10).join(menu_items)}
                      </ul>
                    </li>''')
    
    full_menu = f'''                    <li><a href="../../index.html">Accueil</a></li>
                    <li><a href="../../favorites.html">Favoris</a></li>
{chr(10).join(menu_html)}'''
    
    # Parcourir tous les fichiers HTML et mettre à jour le menu
    for html_file in target_dir.rglob('*.html'):
        if html_file.name == 'index.html':
            continue
        
        with open(html_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remplacer le menu
        menu_pattern = r'<ul>\s*<li><a href="../../index.html">Accueil</a></li>.*?</ul>\s*</nav>'
        new_menu = f'<ul>\n{full_menu}\n                  </ul>'
        content = re.sub(menu_pattern, new_menu, content, flags=re.DOTALL)
        
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == '__main__':
    main()


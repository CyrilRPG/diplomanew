#!/usr/bin/env python3
"""Generate UVSQ_S2 section from Contenu UVSQ/ .docx files."""
import os
import re
from pathlib import Path

import docx

BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR / "Contenu UVSQ"
OUT_DIR = BASE_DIR / "UVSQ_S2"

CURLY_APOSTROPHE = "\u2019"


def escape_js_string(s):
    if not isinstance(s, str):
        return s
    s = re.sub(r"([a-zA-ZéèêëàâäùûüïîôöçÉÈÊËÀÂÄÙÛÜÏÎÔÖÇœŒæÆ])'([a-zA-ZéèêëàâäùûüïîôöçÉÈÊËÀÂÄÙÛÜÏÎÔÖÇœŒæÆ])", r"\1" + CURLY_APOSTROPHE + r"\2", s)
    s = s.replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace("\r", "")
    return s


def json_to_js_data(items):
    lines = []
    for item in items:
        q = escape_js_string(item["question"])
        a = escape_js_string(item["answer"])
        lines.append(f"  {{ question: '{q}', answer: '{a}' }}")
    return ",\n".join(lines)


def parse_docx_qa(filepath):
    """Extract Q&A pairs from a .docx file."""
    doc = docx.Document(filepath)
    items = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        # Split on newline to get Q and A parts
        lines = text.split("\n")
        q_text = None
        a_text = None
        for line in lines:
            line = line.strip()
            # Match "Question : ..." / "QUESTION : ..." etc.
            m_q = re.match(r'question\s*[:：]\s*(.*)', line, re.IGNORECASE)
            m_a = re.match(r'r[eéè]ponse\s*[:：]\s*(.*)', line, re.IGNORECASE)
            if m_q:
                q_text = m_q.group(1).strip()
            elif m_a:
                a_text = m_a.group(1).strip()
        if q_text and a_text:
            items.append({"question": q_text, "answer": a_text})
    return items


def extract_file_number(filename):
    """Extract number from filename like '1. Oreille.docx' -> '1' or '4.1 Appareil...' -> '4.1'"""
    m = re.match(r'^(\d+(?:\.\d+)?)\s*[-.]?\s*(.*?)\.docx$', filename, re.IGNORECASE)
    if m:
        return m.group(1), m.group(2).strip()
    return None, filename.replace('.docx', '')


def number_to_htmlname(num_str):
    """Convert '1' -> 'fc1', '4.1' -> 'fc4_1', '18.2' -> 'fc18_2'"""
    return 'fc' + num_str.replace('.', '_')


def scan_subject_dir(subject_dir):
    """Scan a subject directory and return sorted list of (docx_path, html_name, title)."""
    courses = []
    for f in sorted(os.listdir(subject_dir)):
        if not f.endswith('.docx'):
            continue
        num_str, title = extract_file_number(f)
        if num_str is None:
            continue
        html_name = number_to_htmlname(num_str) + '.html'
        # Clean up title
        title = title.strip(' -.')
        if not title:
            title = f"Cours {num_str}"
        courses.append((subject_dir / f, html_name, title))
    # Sort by numeric value
    def sort_key(item):
        num = item[1].replace('fc', '').replace('.html', '').replace('_', '.')
        try:
            parts = num.split('.')
            return (int(parts[0]), int(parts[1]) if len(parts) > 1 else 0)
        except:
            return (999, 0)
    courses.sort(key=sort_key)
    return courses


# Define structure
SUBJECTS = [
    {"dir": "Anatomie", "display": "Anatomie", "icon": "fa-user-md", "src": "Anatomie"},
    {"dir": "Anglais", "display": "Anglais médical", "icon": "fa-language", "src": "Anglais"},
    {"dir": "ICM", "display": "ICM", "icon": "fa-pills", "src": "ICM"},
    {"dir": "Physiologie", "display": "Physiologie", "icon": "fa-heartbeat", "src": "Physiologie"},
    {"dir": "SHS", "display": "SHS", "icon": "fa-book", "src": "SHS"},
]


def build_menu_html(subjects_data, prefix=".."):
    """Build full nav menu for UVSQ S2."""
    lines = [
        '<nav id="menu">',
        '<header class="major"><h2>Menu</h2></header>',
        '<ul>',
        f'<li><a href="{prefix}/index.html">Accueil</a></li>',
        f'<li><a href="{prefix}/favorites.html">Favoris</a></li>',
    ]
    for subj in subjects_data:
        lines.append(f'<li><span class="opener">{subj["display"]}</span><ul>')
        for _, html_name, title in subj["courses"]:
            lines.append(f'<li><a href="{prefix}/{subj["dir"]}/{html_name}">{title}</a></li>')
        lines.append('</ul></li>')
    lines.append('</ul></nav>')
    return "\n".join(lines)


def build_course_html(matiere_display, course_title, flashcards_js, menu_html, asset_prefix="../../"):
    template = """<!DOCTYPE HTML>
<html>
<head>
<title>Diploma Santé - {course_title}</title>
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
<a href="{asset_prefix}index.html" class="logo"><strong>Diploma Santé</strong> - UVSQ S2</a>
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
  @media screen and (max-width: 768px) {{ .flashcard {{ width: 95vw; height: calc(100vh - 180px); min-height: 450px; }} }}
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
  progressBar.style.width = (progress * 100) + "%";
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
    img.style.height = "auto";
    img.style.maxHeight = "150px";
    img.style.objectFit = "contain";
    wrapper.appendChild(img);
    return wrapper;
  }}
  return document.createElement("div");
}}

function showCard(index) {{
  container.innerHTML = "";
  if (flashcards[index]) {{
    const card = flashcards[index];
    const question = card.question;
    const answer = card.answer;
    const cardEl = document.createElement("div");
    cardEl.classList.add("flashcard", "show");
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
    resetBtn.addEventListener("click", function(e) {{
      e.stopPropagation();
      localStorage.removeItem(progressKey);
      localStorage.removeItem("completed_" + pageId);
      flashcards = originalData.slice();
      currentIndex = 0;
      updateProgress();
      showCard(currentIndex);
    }});
    btnContainer.appendChild(toggleBtn);
    btnContainer.appendChild(resetBtn);
    const checkIcon = document.createElement("span");
    checkIcon.classList.add("check-icon");
    checkIcon.innerHTML = "<i class=\\"fas fa-check\\"></i>";
    checkIcon.addEventListener("click", function(e) {{
      e.stopPropagation();
      cardEl.classList.add("slide-right");
      setTimeout(function() {{
        currentIndex++;
        localStorage.setItem(progressKey, currentIndex);
        updateProgress();
        showCard(currentIndex);
      }}, 400);
    }});
    const crossIcon = document.createElement("span");
    crossIcon.classList.add("cross-icon");
    crossIcon.innerHTML = "<svg xmlns=\\"http://www.w3.org/2000/svg\\" width=\\"24\\" height=\\"24\\" fill=\\"none\\" stroke=\\"#888\\" stroke-width=\\"3\\" stroke-linecap=\\"round\\" stroke-linejoin=\\"round\\" viewBox=\\"0 0 24 24\\"><line x1=\\"18\\" y1=\\"6\\" x2=\\"6\\" y2=\\"18\\"/><line x1=\\"6\\" y1=\\"6\\" x2=\\"18\\" y2=\\"18\\"/></svg>";
    crossIcon.addEventListener("click", function(e) {{
      e.stopPropagation();
      cardEl.classList.add("slide-left");
      setTimeout(function() {{
        const removed = flashcards.splice(currentIndex, 1)[0];
        flashcards.splice(currentIndex + 5, 0, removed);
        showCard(currentIndex);
      }}, 400);
    }});
    const favIcon = document.createElement("span");
    favIcon.classList.add("favorite-icon");
    favIcon.innerHTML = "<svg xmlns=\\"http://www.w3.org/2000/svg\\" viewBox=\\"0 0 24 24\\" width=\\"30\\" height=\\"30\\"><polygon points=\\"12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2\\"/></svg>";
    function updateFav() {{
      if (typeof isFavorite === "function" && isFavorite({{ question: question, answer: answer }})) favIcon.classList.add("active");
      else favIcon.classList.remove("active");
    }}
    favIcon.addEventListener("click", function(e) {{
      e.stopPropagation();
      if (typeof toggleFavorite === "function") toggleFavorite({{ question: question, answer: answer }});
      updateFav();
    }});
    updateFav();
    cardEl.addEventListener("click", function() {{
      const isAnswerVisible = cardEl.classList.toggle("show-answer");
      toggleBtn.textContent = isAnswerVisible ? "Cacher la réponse" : "Voir la réponse";
    }});
    inner.appendChild(front);
    inner.appendChild(back);
    inner.appendChild(checkIcon);
    inner.appendChild(crossIcon);
    inner.appendChild(favIcon);
    cardEl.appendChild(inner);
    cardEl.appendChild(btnContainer);
    container.appendChild(cardEl);
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
    resetBtn.addEventListener("click", function(e) {{
      e.stopPropagation();
      localStorage.removeItem(progressKey);
      localStorage.removeItem("completed_" + pageId);
      flashcards = originalData.slice();
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


def build_index_html(subjects_data, menu_html):
    course_paths = []
    for subj in subjects_data:
        for _, html_name, _ in subj["courses"]:
            course_paths.append(f"{subj['dir']}/{html_name}")
    course_paths_js = ",\n".join([f"  '{p}'" for p in course_paths])

    matiere_cards = []
    for subj in subjects_data:
        if subj["courses"]:
            first_html = subj["courses"][0][1]
            matiere_cards.append(
                f'<div class="matiere-card">\n<span class="icon solid {subj["icon"]}"></span>\n'
                f'<h3>{subj["display"]}</h3>\n'
                f'<a href="{subj["dir"]}/{first_html}" class="button">Commencer</a>\n</div>'
            )
    cards_html = "\n".join(matiere_cards)

    return f"""<!DOCTYPE HTML>
<html>
<head>
<title>Diploma Santé - Plateforme de Flashcards - UVSQ S2</title>
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
<a href="../index.html" class="logo"><strong>Diploma Santé</strong> - UVSQ S2</a>
<ul class="icons">
<li><a href="https://diploma-sante.fr/" class="icon fas fa-globe"><span class="label"></span></a></li>
<li><a href="https://www.instagram.com/diplomasante/" class="icon brands fa-instagram"><span class="label">Instagram</span></a></li>
<li><a href="#" id="dark-mode-toggle" class="icon fas fa-moon"></a></li>
</ul>
</header>

<section id="banner">
<div class="content">
<header>
<h1>UVSQ - Semestre 2</h1>
<p>Plateforme de Flashcards</p>
</header>
<p>Boostez vos révisions en santé avec des flashcards efficaces, spécialement pensées pour les étudiants de l\u2019UVSQ !</p>
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

{menu_html}

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


def build_favorites_html(menu_html):
    return f"""<!DOCTYPE HTML>
<html>
<head>
<title>Diploma Santé - Favoris - UVSQ S2</title>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
<link rel="stylesheet" href="../assets/css/main.css" />
<link rel="icon" type="image/jpeg" href="../images/diploma.jpeg" />
<script src="../security.js" defer></script>
<script src="../assets/js/favorites.js"></script>
</head>
<body class="is-preload">

<div id="wrapper">

<div id="main">
<div class="inner">

<header id="header">
<a href="../index.html" class="logo"><strong>Diploma Santé</strong> - UVSQ S2</a>
<ul class="icons">
<li><a href="https://diploma-sante.fr/" class="icon fas fa-globe"><span class="label"></span></a></li>
<li><a href="https://www.instagram.com/diplomasante/" class="icon brands fa-instagram"><span class="label">Instagram</span></a></li>
<li><a href="#" id="dark-mode-toggle" class="icon fas fa-moon"></a></li>
</ul>
</header>

<section>
<header class="main">
<h1>Mes Favoris</h1>
</header>

<style>
.favorites-container {{
  display: flex;
  flex-direction: column;
  gap: 1rem;
  max-width: 800px;
  margin: 0 auto;
}}
.favorite-card {{
  background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%);
  border: 2px solid #e0e0e0;
  border-radius: 15px;
  padding: 1.5rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  cursor: pointer;
  transition: all 0.3s ease;
}}
.favorite-card:hover {{
  transform: translateY(-3px);
  box-shadow: 0 6px 20px rgba(0, 174, 239, 0.2);
  border-color: #00aeef;
}}
.favorite-card .question {{
  font-weight: 600;
  color: #3d4449;
  margin-bottom: 0.5rem;
}}
.favorite-card .answer {{
  color: #7f888f;
  display: none;
}}
.favorite-card.show .answer {{
  display: block;
}}
.favorite-card .remove-btn {{
  float: right;
  color: #e74c3c;
  cursor: pointer;
  font-size: 1.2em;
}}
body.dark-mode .favorite-card {{
  background: linear-gradient(135deg, #2d3436 0%, #1e2124 100%);
  border-color: #4a5568;
}}
body.dark-mode .favorite-card .question {{ color: #e2e8f0; }}
body.dark-mode .favorite-card .answer {{ color: #a0aec0; }}
.no-favorites {{
  text-align: center;
  color: #7f888f;
  padding: 3rem;
  font-size: 1.2em;
}}
</style>

<div class="favorites-container" id="favoritesContainer">
</div>

<script>
function getFavoritesKey() {{
  return 'favorites_UVSQ_S2';
}}

function loadFavorites() {{
  const container = document.getElementById('favoritesContainer');
  const key = getFavoritesKey();
  const favs = JSON.parse(localStorage.getItem(key) || '[]');

  if (favs.length === 0) {{
    container.innerHTML = '<div class="no-favorites"><p>Aucun favori pour le moment.</p><p>Cliquez sur l\\u2019étoile d\\u2019une flashcard pour l\\u2019ajouter à vos favoris !</p></div>';
    return;
  }}

  container.innerHTML = '';
  favs.forEach(function(fav, index) {{
    const card = document.createElement('div');
    card.classList.add('favorite-card');

    const removeBtn = document.createElement('span');
    removeBtn.classList.add('remove-btn');
    removeBtn.innerHTML = '&times;';
    removeBtn.addEventListener('click', function(e) {{
      e.stopPropagation();
      favs.splice(index, 1);
      localStorage.setItem(key, JSON.stringify(favs));
      loadFavorites();
    }});

    const questionDiv = document.createElement('div');
    questionDiv.classList.add('question');
    questionDiv.textContent = fav.question;

    const answerDiv = document.createElement('div');
    answerDiv.classList.add('answer');
    answerDiv.textContent = typeof fav.answer === 'string' ? fav.answer : JSON.stringify(fav.answer);

    card.appendChild(removeBtn);
    card.appendChild(questionDiv);
    card.appendChild(answerDiv);

    card.addEventListener('click', function() {{
      card.classList.toggle('show');
    }});

    container.appendChild(card);
  }});
}}

document.addEventListener('DOMContentLoaded', loadFavorites);
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

<script src="../assets/js/jquery.min.js"></script>
<script src="../assets/js/browser.min.js"></script>
<script src="../assets/js/breakpoints.min.js"></script>
<script src="../assets/js/util.js"></script>
<script src="../assets/js/main.js"></script>
<script src="../assets/js/darkmode.js"></script>
<script src="../assets/js/favorites.js"></script>

</body>
</html>
"""


def main():
    # Scan source directories
    subjects_data = []
    for subj in SUBJECTS:
        src_path = SRC_DIR / subj["src"]
        if not src_path.exists():
            print(f"WARNING: Source dir not found: {src_path}")
            subjects_data.append({**subj, "courses": []})
            continue
        courses = scan_subject_dir(src_path)
        subjects_data.append({**subj, "courses": courses})
        print(f"Found {len(courses)} courses in {subj['src']}")

    # Build menu HTML
    menu_course = build_menu_html(subjects_data, prefix="..")
    menu_index = build_menu_html(subjects_data, prefix=".")

    # Create output directories and generate course HTML files
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    total_cards = 0
    total_files = 0

    for subj in subjects_data:
        out_subj_dir = OUT_DIR / subj["dir"]
        out_subj_dir.mkdir(parents=True, exist_ok=True)

        for docx_path, html_name, title in subj["courses"]:
            items = parse_docx_qa(docx_path)
            if not items:
                print(f"WARNING: No Q&A found in {docx_path.name}")
                continue

            flashcards_js = json_to_js_data(items)
            html_content = build_course_html(
                subj["display"], title, flashcards_js, menu_course, asset_prefix="../../"
            )

            out_path = out_subj_dir / html_name
            with open(out_path, "w", encoding="utf-8") as f:
                f.write(html_content)

            total_cards += len(items)
            total_files += 1
            print(f"  Wrote {subj['dir']}/{html_name} ({len(items)} cards) - {title}")

    # Generate index.html
    index_html = build_index_html(subjects_data, menu_index)
    with open(OUT_DIR / "index.html", "w", encoding="utf-8") as f:
        f.write(index_html)
    print("Wrote index.html")

    # Generate favorites.html
    fav_html = build_favorites_html(menu_index)
    with open(OUT_DIR / "favorites.html", "w", encoding="utf-8") as f:
        f.write(fav_html)
    print("Wrote favorites.html")

    print(f"\nDone! Generated {total_files} course files with {total_cards} total flashcards.")


if __name__ == "__main__":
    main()

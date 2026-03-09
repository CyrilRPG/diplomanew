"""
Shared HTML template for flashcard generation.
Uses the correct template from introduction_ethique_medicale.html (working flip + space bar).
"""

def esc(s):
    """Escape apostrophes and special chars for JS string embedding."""
    return s.replace("\\", "\\\\").replace("'", "\u2019").replace('"', '\\"').replace("\n", "\\n")


def get_course_html(title_h1, title_h2, page_id, flashcards, sidebar_html, asset_prefix="../../"):
    """
    Generate complete HTML for a flashcard course page.

    Args:
        title_h1: Main title (e.g. "Biotechnologie")
        title_h2: Subtitle (e.g. "Introduction à la biotechnologie (FC1)")
        page_id: Unique page identifier for localStorage
        flashcards: List of (question, answer) tuples
        sidebar_html: Complete sidebar nav HTML
        asset_prefix: Relative path to assets (e.g. "../../")
    """
    # Build flashcardsData JS array
    fc_lines = []
    for q, a in flashcards:
        fc_lines.append(f'  {{ question: "{esc(q)}", answer: "{esc(a)}" }}')
    fc_data = ",\n".join(fc_lines)

    return f'''<!DOCTYPE HTML>
<html>
<head>
<title>Diploma Santé - {esc(title_h2.split(" (")[0])}</title>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
<link rel="stylesheet" href="{asset_prefix}assets/css/main.css" />
<link rel="icon" type="image/jpeg" href="{asset_prefix}images/diploma.jpeg" />
    <script src="{asset_prefix}assets/js/favorites.js"></script>
</head>
<body class="is-preload">

<!-- Wrapper -->
<div id="wrapper">

<!-- Main -->
<div id="main">
<div class="inner">

<!-- Header -->
<header id="header">
<a href="{asset_prefix}index.html" class="logo"><strong>Diploma Santé</strong>- Plateforme de Flashcards</a>
<ul class="icons">
<li><a href="https://diploma-sante.fr/" class="icon fas fa-globe"><span class="label"></span></a></li>
<li><a href="https://www.instagram.com/diplomasante/" class="icon brands fa-instagram"><span class="label">Instagram</span></a></li>
        <li><a href="#" id="dark-mode-toggle" class="icon fas fa-moon"></a></li>
</ul>
</header>

<!-- Content -->
<section>
<header class="main"><div class="header-left"><h1>{title_h1}</h1><h2>{title_h2}</h2></div><span class="image main"><img src="{asset_prefix}images/banner.png" alt="" /></span></header>

\t\t\t\t\t<style>  /* Header minimal avec contrôles accessibles */
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
  .check-icon {{ top: 30px; left: 30px; width: 45px; height: 45px; z-index: 1001; background: rgba(255, 255, 255, 0.95); border-radius: 50%; padding: 8px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3); color: #888; font-size: 20px; }}
  .cross-icon {{ top: 30px; right: 30px; stroke: #888; width: 45px; height: 45px; z-index: 1001; background: rgba(255, 255, 255, 0.95); border-radius: 50%; padding: 8px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.3); }}
  body.dark-mode .check-icon, body.dark-mode .cross-icon {{ background: rgba(50, 50, 50, 0.95); color: #fff; stroke: #fff; }}
  .favorite-icon {{ bottom: 15px; left: 50%; transform: translateX(-50%); fill: #888; width: 30px; height: 30px; }}
  .favorite-icon.active {{ fill: #ffd700; }}
  .flashcard.show-answer .check-icon, .flashcard.show-answer .cross-icon, .flashcard.show-answer .favorite-icon {{ display: flex !important; }}
  .slide-left {{ animation: slideLeft 0.4s forwards; }}
  .slide-right {{ animation: slideRight 0.4s forwards; }}
  @keyframes slideLeft {{ from {{ transform: translateX(0); opacity: 1; }} to {{ transform: translateX(-100%); opacity: 0; }} }}
  @keyframes slideRight {{ from {{ transform: translateX(0); opacity: 1; }} to {{ transform: translateX(100%); opacity: 0; }} }}
  body.dark-mode .flashcard-front {{ background-color: #2d3436; color: #e2e8f0; }}
  body.dark-mode .flashcard-inner {{ background-color: #2d3436; }}
  body.dark-mode .progress-container {{ background-color: #34495e; border-color: #4a5568; }}
  @media screen and (max-width: 768px) {{ .flashcard {{ width: 95vw; height: calc(100vh - 180px); min-height: 450px; }} }}
</style>

</head>
<body>
<div class="progress-container">
  <div class="progress-bar" id="progressBar"></div>
</div>
 <div class="flashcards-container" id="flashcards"></div>

 <script>

const flashcardsData = [
{fc_data}
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

<!-- Sidebar -->
<div id="sidebar">
<div class="inner">

<section id="search" class="alt">
<form method="post" action="#">
<input type="text" name="query" id="query" placeholder="Rechercher">
</form>
</section>
{sidebar_html}
<footer id="footer"><p class="copyright">&copy; Diploma Santé. Tous droits réservés.</p></footer>
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
</html>'''

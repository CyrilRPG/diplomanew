#!/usr/bin/env python3
"""
Master generation script.
Reads all data_*.py flashcard data files, generates HTML using the correct template,
updates sidebars, and restructures UPEC index for unified Santé Publique.
"""
import os, sys, re, importlib.util

DIPLOMA_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(DIPLOMA_ROOT, "scripts")

# Add scripts dir to path
sys.path.insert(0, SCRIPTS_DIR)
from html_template import get_course_html

# ─────────────────────────────────────────────
# SIDEBAR DEFINITIONS
# ─────────────────────────────────────────────

UPEC_SIDEBAR = '''<nav id="menu">
<header class="major"><h2>Menu</h2></header>
<ul>
<li><a href="./index.html">Accueil</a></li>
<li><a href="./favorites.html">Favoris</a></li>
<li><span class="opener">Bases moléculaires en oncologie</span><ul>
<li><a href="./Bases_moleculaire_Oncologie/fc1.html">Introduction au cancer</a></li>
<li><a href="./Bases_moleculaire_Oncologie/fc2.html">Bases cellulaires et moléculaires pour comprendre l\u2019oncologie</a></li>
<li><a href="./Bases_moleculaire_Oncologie/fc3.html">Oncogenèse des lymphomes T</a></li>
<li><a href="./Bases_moleculaire_Oncologie/fc4.html">Exploration des anomalies moléculaires dans les tumeurs</a></li>
<li><a href="./Bases_moleculaire_Oncologie/fc5.html">Mécanismes de réparation de l\u2019ADN et cancer</a></li>
<li><a href="./Bases_moleculaire_Oncologie/fc6.html">Oncogenèse digestive</a></li>
<li><a href="./Bases_moleculaire_Oncologie/fc7.html">Bases de thérapeutique du cancer</a></li>
<li><a href="./Bases_moleculaire_Oncologie/fc8.html">Mutation du gène BRAF dans les mélanomes</a></li>
<li><a href="./Bases_moleculaire_Oncologie/fc9.html">Lymphome diffus à grandes cellules (DLBCL)</a></li>
<li><a href="./Bases_moleculaire_Oncologie/fc10.html">Bases de données</a></li>
<li><a href="./Bases_moleculaire_Oncologie/fc11.html">Cancer du sein : perspective de l\u2019oncogénétique</a></li>
</ul></li>
<li><span class="opener">Human nutrition</span><ul>
<li><a href="./Human_Nutrition/fc1.html">Métabolisme bioénergétique (révision)</a></li>
<li><a href="./Human_Nutrition/fc2.html">Anthropométrie, bilan énergétique, valeurs de référence en diététique</a></li>
<li><a href="./Human_Nutrition/fc3.html">Macronutriments : protéines, glucides et acides gras</a></li>
<li><a href="./Human_Nutrition/fc4.html">Les micronutriments : minéraux</a></li>
<li><a href="./Human_Nutrition/fc5.html">Les vitamines liposolubles</a></li>
<li><a href="./Human_Nutrition/fc5_2.html">Les vitamines hydrosolubles</a></li>
<li><a href="./Human_Nutrition/fc6.html">Maladies cardiovasculaires</a></li>
<li><a href="./Human_Nutrition/fc7.html">Alimentation et cancer</a></li>
<li><a href="./Human_Nutrition/fc8.html">Consommation d\u2019alcool et effets sur la santé</a></li>
<li><a href="./Human_Nutrition/fc9.html">Interaction régime-maladie : obésité, syndrome métabolique et diabète</a></li>
<li><a href="./Human_Nutrition/fc10.html">Interventions diététiques et pharmacologiques</a></li>
</ul></li>
<li><span class="opener">One Health</span><ul>
<li><a href="./One_Health/fc1.html">Introduction au concept One Health</a></li>
<li><a href="./One_Health/fc2.html">Zoonoses et modes de transmission</a></li>
<li><a href="./One_Health/fc3.html">Émergence et diffusion de la résistance aux antibiotiques</a></li>
<li><a href="./One_Health/fc4.html">Maladies émergentes transmises de l\u2019animal à l\u2019homme</a></li>
<li><a href="./One_Health/fc5.html">Mobiliser les professionnels et la population autour des approches One Health</a></li>
<li><a href="./One_Health/fc6.html">Polluants de l\u2019environnement professionnel</a></li>
<li><a href="./One_Health/fc7.html">Évaluation, prévention et gestion des risques en santé environnementale</a></li>
<li><a href="./One_Health/fc8.html">Principales théories, concepts et modèles en sciences sociales (One Health)</a></li>
<li><a href="./One_Health/fc9.html">Surveillance et investigation en santé publique et santé animale</a></li>
<li><a href="./One_Health/fc10.html">Biodiversité des plantes et liens avec la santé humaine et animale</a></li>
<li><a href="./One_Health/fc11.html">Écologie de la faune sauvage</a></li>
<li><a href="./One_Health/fc12_1.html">Environnement, biodiversité, écologie, évolution des risques (partie 1)</a></li>
<li><a href="./One_Health/fc12_2.html">Environnement, biodiversité, écologie, évolution des risques (partie 2)</a></li>
</ul></li>
<li><span class="opener">Réglementation et éthique de la recherche</span><ul>
<li><a href="./Reglementation_Ethique_Recherche/fc1.html">Droit de la santé</a></li>
<li><a href="./Reglementation_Ethique_Recherche/fc2.html">Réglementation et recherche de la santé</a></li>
</ul></li>
<li><span class="opener">Technique de vie et société</span><ul>
<li><a href="./Technique_Vie_Societe/fc1.html">Vie, technique et société - Introduction</a></li>
<li><a href="./Technique_Vie_Societe/fc2.html">L\u2019éthique à l\u2019heure de la civilisation technologique</a></li>
<li><a href="./Technique_Vie_Societe/fc3.html">Le statut des objets techniques et des technologies dans le champ de la santé</a></li>
<li><a href="./Technique_Vie_Societe/fc4.html">Les droits et devoirs des patients et des praticiens</a></li>
<li><a href="./Technique_Vie_Societe/fc5.html">Le droit à l\u2019information médicale</a></li>
<li><a href="./Technique_Vie_Societe/fc6.html">Enjeux et statuts des objets biologiques</a></li>
<li><a href="./Technique_Vie_Societe/fc7.html">La pensée des bio-objets chez Céline Lafontaine</a></li>
<li><a href="./Technique_Vie_Societe/fc8.html">La technicisation médicale, une déshumanisation</a></li>
<li><a href="./Technique_Vie_Societe/fc9.html">La médecine humaniste face à la biomédecine</a></li>
<li><a href="./Technique_Vie_Societe/fc10.html">Les médecines alternatives : de la critique humaniste à l\u2019antiscience</a></li>
<li><a href="./Technique_Vie_Societe/fc11.html">Biomédecine et approche holistique : le modèle biopsychosocial</a></li>
</ul></li>
<li><span class="opener">Biotechnologie</span><ul>
<li><a href="./Biotechnologie/fc1.html">Introduction à la biotechnologie</a></li>
<li><a href="./Biotechnologie/fc2.html">Reprogrammation cellulaire</a></li>
<li><a href="./Biotechnologie/fc3.html">Drug Repositioning</a></li>
<li><a href="./Biotechnologie/fc4.html">Immunothérapie</a></li>
<li><a href="./Biotechnologie/fc5.html">Principes généraux de la thérapie génétique</a></li>
<li><a href="./Biotechnologie/fc6.html">Les vésicules extracellulaires</a></li>
<li><a href="./Biotechnologie/fc7.html">Bioproduction de cellules souches</a></li>
<li><a href="./Biotechnologie/fc8.html">Stratégies vaccinales</a></li>
<li><a href="./Biotechnologie/fc9.html">Édition du génome</a></li>
<li><a href="./Biotechnologie/fc10.html">Biomécanique des biomatériaux</a></li>
<li><a href="./Biotechnologie/fc11.html">Thérapie cellulaire et moelle osseuse</a></li>
<li><a href="./Biotechnologie/fc12.html">Peptides thérapeutiques antimicrobiens</a></li>
</ul></li>
<li><span class="opener">Santé Publique</span><ul>
<li>
<span class="opener">Promotion et prévention</span>
<ul>
<li><a href="./SP_Promotion_Prevention/fc1.html">Généralités en santé publique</a></li>
<li><a href="./SP_Promotion_Prevention/fc2.html">Méthodologie de projet en prévention et promotion de la santé</a></li>
<li><a href="./SP_Promotion_Prevention/fc3.html">Déterminants de santé</a></li>
<li><a href="./SP_Promotion_Prevention/fc4.html">Méthodes de prévention et de dépistage</a></li>
<li><a href="./SP_Promotion_Prevention/fc5.html">Vaccins et promotion de la prévention</a></li>
<li><a href="./SP_Promotion_Prevention/fc6.html">Maladies sexuellement transmissibles</a></li>
<li><a href="./SP_Promotion_Prevention/fc7.html">Initiation aux soins d\u2019urgence</a></li>
<li><a href="./SP_Promotion_Prevention/fc8.html">Sédentarité et activité physique</a></li>
<li><a href="./SP_Promotion_Prevention/fc9.html">Le risque cardio-vasculaire</a></li>
</ul>
</li>
<li>
<span class="opener">Économie de la santé</span>
<ul>
<li><a href="./SP_Economie_Sante/fc1.html">Analyse économique de la perte d\u2019autonomie (Dépendance)</a></li>
<li><a href="./SP_Economie_Sante/fc2.html">Analyse de la perte d\u2019autonomie : Handicap</a></li>
<li><a href="./SP_Economie_Sante/fc3.html">Les modes de rémunération des médecins libéraux</a></li>
<li><a href="./SP_Economie_Sante/fc4.html">Les modes de rémunération des établissements de santé</a></li>
<li><a href="./SP_Economie_Sante/fc5.html">Nutrition, santé et croissance économique</a></li>
<li><a href="./SP_Economie_Sante/fc6.html">Santé et développement : Santé et pauvreté</a></li>
<li><a href="./SP_Economie_Sante/fc7.html">Santé et développement : Système et égalité</a></li>
<li><a href="./SP_Economie_Sante/fc8.html">Santé et environnement</a></li>
</ul>
</li>
<li>
<span class="opener">Géographie de la santé</span>
<ul>
<li><a href="./SP_Geographie_Sante/fc1.html">Histoire et concepts de la géographie de la santé</a></li>
<li><a href="./SP_Geographie_Sante/fc2.html">Liens villes et santé : enjeux des usages de la carte en santé</a></li>
<li><a href="./SP_Geographie_Sante/fc3.html">Inégalités spatiales de l\u2019offre de soins en France</a></li>
<li><a href="./SP_Geographie_Sante/fc4.html">Enjeux internationaux des inégalités d\u2019offre de soins</a></li>
<li><a href="./SP_Geographie_Sante/fc5.html">Enjeux internationaux : le point de vue des patients</a></li>
<li><a href="./SP_Geographie_Sante/fc6.html">L\u2019accès aux soins des personnes vulnérables</a></li>
<li><a href="./SP_Geographie_Sante/fc7.html">Alimentation et santé en ville</a></li>
<li><a href="./SP_Geographie_Sante/fc8.html">Pouvoirs des villes et urbanisme favorable à la santé : espaces verts</a></li>
<li><a href="./SP_Geographie_Sante/fc9.html">Urbanisme favorable à la santé : personnes âgées</a></li>
<li><a href="./SP_Geographie_Sante/fc10.html">Urbanisme favorable à la santé : enfants</a></li>
</ul>
</li>
<li>
<span class="opener">Gestion de projet de recherche clinique</span>
<ul>
<li><a href="./SP_Gestion_Projet_RC/fc1.html">Généralités sur les essais cliniques</a></li>
<li><a href="./SP_Gestion_Projet_RC/fc2.html">Acteurs de la recherche clinique</a></li>
<li><a href="./SP_Gestion_Projet_RC/fc3.html">Vigilance, gestion des EIG et sécurité des essais cliniques</a></li>
<li><a href="./SP_Gestion_Projet_RC/fc4.html">Structures de soutien à la recherche clinique</a></li>
<li><a href="./SP_Gestion_Projet_RC/fc5.html">Mise en place d\u2019un essai clinique</a></li>
<li><a href="./SP_Gestion_Projet_RC/fc6.html">Le dossier patient, les CRF et les bases de données</a></li>
<li><a href="./SP_Gestion_Projet_RC/fc7.html">Gestion de projet (Le monitoring)</a></li>
<li><a href="./SP_Gestion_Projet_RC/fc8.html">Réglementation sur les échantillons biologiques</a></li>
<li><a href="./SP_Gestion_Projet_RC/fc9.html">Démarches auprès du MESRI</a></li>
</ul>
</li>
</ul></li>
</ul></nav>'''

SU_S2_SIDEBAR = '''<nav id="menu">
\t\t\t\t\t\t\t\t<header class="major">
\t\t\t\t\t\t\t\t\t<h2>Menu</h2>
\t\t\t\t\t\t\t\t</header>
\t\t\t\t\t\t\t\t<ul>
\t\t\t\t\t\t\t\t\t<li><a href="../index.html">Accueil</a></li>
\t\t\t\t\t\t\t\t\t<li><a href="../favorites.html">Favoris</a></li>
\t\t\t\t\t\t\t\t\t<li>
\t\t\t\t\t\t\t\t\t\t<span class="opener">Physiologie</span>
\t\t\t\t\t\t\t\t\t\t<ul>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Physiologie/fc1.html">Introduction a la physiologie cardio-vasculaire</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Physiologie/fc2.html">Adaptation de l\u2019apport d\u2019oxygène</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Physiologie/fc3.html">Organisation du système cardiovasculaire</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Physiologie/fc4.html">Adaptations à l\u2019effort</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Physiologie/fc5.html">Introduction à la neurophysiologie</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Physiologie/fc6.html">Adaptation rénale</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Physiologie/fc7.html">Bilan de l\u2019eau</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Physiologie/fc8.html">Contrôle de la croissance</a></li>
\t\t\t\t\t\t\t\t\t\t</ul>
\t\t\t\t\t\t\t\t\t</li>
\t\t\t\t\t\t\t\t\t<li>
\t\t\t\t\t\t\t\t\t\t<span class="opener">Anatomie</span>
\t\t\t\t\t\t\t\t\t\t<ul>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Anatomie/tete_cou.html">Tête et cou</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Anatomie/petit_bassin.html">Le petit bassin</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Anatomie/odontologie.html">Odontologie</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Anatomie/appareil_reproducteur.html">Appareil reproducteur</a></li>
\t\t\t\t\t\t\t\t\t\t</ul>
\t\t\t\t\t\t\t\t\t</li>
\t\t\t\t\t\t\t\t\t<li>
\t\t\t\t\t\t\t\t\t\t<span class="opener">Biophysique</span>
\t\t\t\t\t\t\t\t\t\t<ul>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Biophysique/fc1.html">Physique pour la biophysique</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Biophysique/fc2.html">Solutions et transport</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Biophysique/fc3.html">Compartiments liquidiens</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Biophysique/fc4.html">Transfert electrodiffusif</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Biophysique/fc5.html">Potentiel de membrane</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Biophysique/fc6.html">ECG</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Biophysique/fc7.html">Acide base</a></li>
\t\t\t\t\t\t\t\t\t\t</ul>
\t\t\t\t\t\t\t\t\t</li>
\t\t\t\t\t\t\t\t\t<li>
\t\t\t\t\t\t\t\t\t\t<span class="opener">Pharmacologie</span>
\t\t\t\t\t\t\t\t\t\t<ul>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Pharmacologie/fc1.html">Introduction à la pharmacologie</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Pharmacologie/fc2.html">Règles de prescription</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Pharmacologie/fc3.html">Les phases de développement clinique</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Pharmacologie/fc4.html">Encadrement réglementaire de la recherche clinique</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Pharmacologie/fc5.html">Pharmacocinétique descriptive (FC5)</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Pharmacologie/fc6.html">Pharmacodynamie</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Pharmacologie/fc7.html">Pharmscocinétique quantitative</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Pharmacologie/fc8.html">Causes pharmacocinétiques de variabilité</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Pharmacologie/fc9.html">Cibles et mécanismes d\u2019actions</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Pharmacologie/fc10.html">Iatrogénie</a></li>
\t\t\t\t\t\t\t\t\t\t</ul>
\t\t\t\t\t\t\t\t\t</li>
\t\t\t\t\t\t\t\t\t<li>
\t\t\t\t\t\t\t\t\t\t<span class="opener">Biostatistiques</span>
\t\t\t\t\t\t\t\t\t\t<ul>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Biostatistiques/fc1.html">Probabilité</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Biostatistiques/fc2.html">Tests diagnostiques</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Biostatistiques/fc3.html">Variables aléatoires</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Biostatistiques/fc4.html">Distribution usuelles</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Biostatistiques/fc5.html">Échantillon, population et théorème central</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Biostatistiques/fc6.html">Théorie des tests et degré de signification</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Biostatistiques/fc7.html">Test de comparaison</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Biostatistiques/fc8.html">X2</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../Biostatistiques/fc9.html">Principaux types d\u2019études</a></li>
\t\t\t\t\t\t\t\t\t\t</ul>
\t\t\t\t\t\t\t\t\t</li>
\t\t\t\t\t\t\t\t\t<li>
\t\t\t\t\t\t\t\t\t\t<span class="opener">UEDS Biologie</span>
\t\t\t\t\t\t\t\t\t\t<ul>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../UEDS_Biologie/fc1.html">Acides aminés</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../UEDS_Biologie/fc2_1.html">Enzymologie (FC2.1)</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../UEDS_Biologie/fc2_2.html">Enzymologie (FC2.2)</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../UEDS_Biologie/fc3_1.html">Glucides (FC3.1)</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../UEDS_Biologie/fc3_2.html">Glucides (FC3.2)</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../UEDS_Biologie/fc4.html">Réplication procaryote</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../UEDS_Biologie/fc5.html">Transcription</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../UEDS_Biologie/fc6.html">Analyse cellulaire et moléculaire</a></li>
\t\t\t\t\t\t\t\t\t\t</ul>
\t\t\t\t\t\t\t\t\t</li>
\t\t\t\t\t\t\t\t\t<li>
\t\t\t\t\t\t\t\t\t\t<span class="opener">UEDL IGHL</span>
\t\t\t\t\t\t\t\t\t\t<ul>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../UEDL_IGHL/fc1.html">La syntaxe</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../UEDL_IGHL/fc2.html">Morphologie</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../UEDL_IGHL/fc3.html">Introduction à l\u2019histoire de la langue</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../UEDL_IGHL/fc4.html">Ancien français</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../UEDL_IGHL/fc5.html">Le moyen français</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../UEDL_IGHL/fc6.html">Français classique, post classique et moderne</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../UEDL_IGHL/fc7.html">Les voyelles</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../UEDL_IGHL/fc8.html">Les consonnes</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../UEDL_IGHL/fc9.html">Le groupe nominal</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../UEDL_IGHL/fc10.html">Le groupe verbal et le système pronominal</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../UEDL_IGHL/fc11.html">Lexicologie historique</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../UEDL_IGHL/fc12.html">Sémantique historique</a></li>
\t\t\t\t\t\t\t\t\t\t\t<li><a href="../UEDL_IGHL/fc13.html">Dialectologie gallo-romane</a></li>
\t\t\t\t\t\t\t\t\t\t</ul>
\t\t\t\t\t\t\t\t\t</li>
\t\t\t\t\t\t\t\t\t<li>
\t\t\t\t\t\t\t\t\t\t<span class="opener">SHS</span>
\t\t\t\t\t\t\t\t\t\t<ul>
\t\t\t\t\t\t\t\t\t\t\t<li>
\t\t\t\t\t\t\t\t\t\t\t\t<span class="opener">Santé numérique</span>
\t\t\t\t\t\t\t\t\t\t\t\t<ul>
\t\t\t\t\t\t\t\t\t\t\t\t\t<li><a href="../SHS/definition_acteurs_strategies.html">Définition, acteurs et stratégies nationales</a></li>
\t\t\t\t\t\t\t\t\t\t\t\t\t<li><a href="../SHS/outils_pratiques_numeriques.html">Outils et pratiques numériques en santé</a></li>
\t\t\t\t\t\t\t\t\t\t\t\t\t<li><a href="../SHS/traitement_donnees_sante.html">Traitement des données de santé</a></li>
\t\t\t\t\t\t\t\t\t\t\t\t</ul>
\t\t\t\t\t\t\t\t\t\t\t</li>
\t\t\t\t\t\t\t\t\t\t\t<li>
\t\t\t\t\t\t\t\t\t\t\t\t<span class="opener">Éthique et droit</span>
\t\t\t\t\t\t\t\t\t\t\t\t<ul>
\t\t\t\t\t\t\t\t\t\t\t\t\t<li><a href="../SHS/introduction_droit_sante.html">Introduction au droit de la santé</a></li>
\t\t\t\t\t\t\t\t\t\t\t\t\t<li><a href="../SHS/introduction_ethique_medicale.html">Introduction à l\u2019éthique médicale (FC2)</a></li>
\t\t\t\t\t\t\t\t\t\t\t\t\t<li><a href="../SHS/principisme_fin_de_vie.html">Principisme et fin de vie (FC3)</a></li>
\t\t\t\t\t\t\t\t\t\t\t\t\t<li><a href="../SHS/progres_techniques_amp.html">Progrès techniques et AMP (FC4)</a></li>
\t\t\t\t\t\t\t\t\t\t\t\t</ul>
\t\t\t\t\t\t\t\t\t\t\t</li>
\t\t\t\t\t\t\t\t\t\t\t<li>
\t\t\t\t\t\t\t\t\t\t\t\t<span class="opener">Psychologie médicale</span>
\t\t\t\t\t\t\t\t\t\t\t\t<ul>
\t\t\t\t\t\t\t\t\t\t\t\t\t<li><a href="../SHS/psycho_emotion_comportement.html">Émotion et comportement (FC1)</a></li>
\t\t\t\t\t\t\t\t\t\t\t\t\t<li><a href="../SHS/psycho_prevention_suicidaires.html">Prévention des conduites suicidaires (FC2)</a></li>
\t\t\t\t\t\t\t\t\t\t\t\t\t<li><a href="../SHS/psycho_representations_corps.html">Les représentations du corps (FC3)</a></li>
\t\t\t\t\t\t\t\t\t\t\t\t\t<li><a href="../SHS/psycho_stress_psychotraumatisme.html">Stress et psycho-traumatisme (FC4)</a></li>
\t\t\t\t\t\t\t\t\t\t\t\t\t<li><a href="../SHS/psycho_developpement_affectif.html">Développement affectif et intellectuel (FC5)</a></li>
\t\t\t\t\t\t\t\t\t\t\t\t</ul>
\t\t\t\t\t\t\t\t\t\t\t</li>
\t\t\t\t\t\t\t\t\t\t</ul>
\t\t\t\t\t\t\t\t\t</li>
\t\t\t\t\t\t\t\t</ul>
\t\t\t\t\t\t\t</nav>'''


# Folder name mapping: agents may use short names, remap to correct ones
FOLDER_MAP = {
    "SP_Economie": "SP_Economie_Sante",
    "SP_Geographie": "SP_Geographie_Sante",
    "SP_Gestion": "SP_Gestion_Projet_RC",
    "SP_Promotion": "SP_Promotion_Prevention",
}


def load_data_module(filepath):
    """Dynamically load a data_*.py module and return its COURSES list."""
    spec = importlib.util.spec_from_file_location("data_mod", filepath)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    courses = mod.COURSES
    # Fix folder names if needed
    for c in courses:
        if c["folder"] in FOLDER_MAP:
            c["folder"] = FOLDER_MAP[c["folder"]]
    return courses


def get_upec_sidebar_for_course(course_folder):
    """Return sidebar HTML for an UPEC course file (adjusting paths with ./)."""
    return UPEC_SIDEBAR.replace('href="./', 'href="../')


def get_su_sidebar():
    """Return sidebar HTML for SU S2 course files."""
    return SU_S2_SIDEBAR


def generate_upec_courses():
    """Generate all UPEC LSPS3 S2 course HTML files from data files."""
    upec_root = os.path.join(DIPLOMA_ROOT, "UPEC_LSPS3_S2")
    upec_data_files = sorted([
        f for f in os.listdir(SCRIPTS_DIR)
        if f.startswith("data_biotech") or f.startswith("data_sp_")
    ])

    sidebar = UPEC_SIDEBAR.replace('href="./', 'href="../')
    total_generated = 0

    for df in upec_data_files:
        filepath = os.path.join(SCRIPTS_DIR, df)
        try:
            courses = load_data_module(filepath)
        except Exception as e:
            print(f"  ERROR loading {df}: {e}")
            continue

        for course in courses:
            folder = course["folder"]
            filename = course["filename"]
            outdir = os.path.join(upec_root, folder)
            os.makedirs(outdir, exist_ok=True)
            outpath = os.path.join(outdir, filename)

            html = get_course_html(
                title_h1=course["title_h1"],
                title_h2=course["title_h2"],
                page_id=course["id"],
                flashcards=course["flashcards"],
                sidebar_html=sidebar,
                asset_prefix="../../"
            )
            with open(outpath, "w", encoding="utf-8") as f:
                f.write(html)
            total_generated += 1
            print(f"  [{total_generated}] {folder}/{filename}: {len(course['flashcards'])} flashcards")

    return total_generated


def generate_su_courses():
    """Generate SU S2 SHS course HTML files from data files."""
    su_root = os.path.join(DIPLOMA_ROOT, "SU_S2")
    su_data_files = sorted([
        f for f in os.listdir(SCRIPTS_DIR)
        if f.startswith("data_su_shs")
    ])

    sidebar = SU_S2_SIDEBAR
    total_generated = 0

    for df in su_data_files:
        filepath = os.path.join(SCRIPTS_DIR, df)
        try:
            courses = load_data_module(filepath)
        except Exception as e:
            print(f"  ERROR loading {df}: {e}")
            continue

        for course in courses:
            folder = course["folder"]
            filename = course["filename"]
            outdir = os.path.join(su_root, folder)
            os.makedirs(outdir, exist_ok=True)
            outpath = os.path.join(outdir, filename)

            html = get_course_html(
                title_h1=course["title_h1"],
                title_h2=course["title_h2"],
                page_id=course["id"],
                flashcards=course["flashcards"],
                sidebar_html=sidebar,
                asset_prefix="../../"
            )
            with open(outpath, "w", encoding="utf-8") as f:
                f.write(html)
            total_generated += 1
            print(f"  [{total_generated}] SHS/{filename}: {len(course['flashcards'])} flashcards")

    return total_generated


def update_existing_su_sidebars():
    """Update sidebars in all existing SU_S2 HTML course files."""
    su_root = os.path.join(DIPLOMA_ROOT, "SU_S2")
    updated = 0
    for dirpath, dirnames, filenames in os.walk(su_root):
        for fname in filenames:
            if not fname.endswith(".html") or fname in ("index.html", "favorites.html"):
                continue
            fpath = os.path.join(dirpath, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            if '<nav id="menu">' in content:
                new_content = re.sub(
                    r'<nav id="menu">.*?</nav>',
                    SU_S2_SIDEBAR,
                    content,
                    flags=re.DOTALL
                )
                if new_content != content:
                    with open(fpath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    updated += 1
    return updated


def update_existing_upec_sidebars():
    """Update sidebars in all existing UPEC_LSPS3_S2 HTML course files."""
    upec_root = os.path.join(DIPLOMA_ROOT, "UPEC_LSPS3_S2")
    sidebar = UPEC_SIDEBAR.replace('href="./', 'href="../')
    updated = 0
    for dirpath, dirnames, filenames in os.walk(upec_root):
        for fname in filenames:
            if not fname.endswith(".html") or fname in ("index.html", "favorites.html"):
                continue
            fpath = os.path.join(dirpath, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            if '<nav id="menu">' in content:
                new_content = re.sub(
                    r'<nav id="menu">.*?</nav>',
                    sidebar,
                    content,
                    flags=re.DOTALL
                )
                if new_content != content:
                    with open(fpath, "w", encoding="utf-8") as f:
                        f.write(new_content)
                    updated += 1
    return updated


if __name__ == "__main__":
    print("=" * 60)
    print("DIPLOMA SANTÉ - Regeneration of flashcards")
    print("=" * 60)

    # List available data files
    data_files = sorted([f for f in os.listdir(SCRIPTS_DIR) if f.startswith("data_") and f.endswith(".py")])
    print(f"\nFound {len(data_files)} data files:")
    for df in data_files:
        print(f"  - {df}")

    # Generate UPEC courses
    print("\n--- Generating UPEC LSPS3 S2 courses ---")
    upec_count = generate_upec_courses()
    print(f"Generated {upec_count} UPEC course files")

    # Generate SU courses
    print("\n--- Generating SU S2 SHS courses ---")
    su_count = generate_su_courses()
    print(f"Generated {su_count} SU SHS course files")

    # Update existing sidebars
    print("\n--- Updating existing SU S2 sidebars ---")
    su_updated = update_existing_su_sidebars()
    print(f"Updated {su_updated} SU S2 sidebar(s)")

    print("\n--- Updating existing UPEC sidebars ---")
    upec_updated = update_existing_upec_sidebars()
    print(f"Updated {upec_updated} UPEC sidebar(s)")

    print(f"\n{'=' * 60}")
    print(f"TOTAL: {upec_count + su_count} course files generated, {su_updated + upec_updated} sidebars updated")
    print(f"{'=' * 60}")

#!/usr/bin/env python3
"""Helper script: appends additional flashcards to l3_data_promo.py"""
import re

TARGET = "/Users/cyrilwisa/Desktop/diploma/scripts/l3_data_promo.py"

# Additional flashcards for fc1 (need 1 more to reach 100)
fc1_extra = [
    ("Qu\u2019est-ce que la prévention combinée ?", "L\u2019association de plusieurs stratégies de prévention (comportementale, biomédicale, structurelle) pour maximiser l\u2019efficacité de la protection contre une maladie."),
]

# Additional flashcards for fc2 (need 32 more to reach 100)
fc2_extra = [
    ("Qu\u2019est-ce que l\u2019analyse SWOT dans un projet de prévention ?", "Un outil d\u2019analyse identifiant les Forces (Strengths), Faiblesses (Weaknesses), Opportunités (Opportunities) et Menaces (Threats) d\u2019un projet."),
    ("Qu\u2019est-ce qu\u2019un diagramme de Gantt dans la planification d\u2019un projet ?", "Un outil visuel représentant le calendrier du projet avec les différentes tâches, leur durée et leur enchaînement dans le temps."),
    ("Qu\u2019est-ce que le concept de « pair-éducation » en prévention ?", "Une stratégie où des personnes formées interviennent auprès de leurs pairs (même âge, même milieu) pour transmettre des messages de prévention."),
    ("Pourquoi la pair-éducation est-elle efficace ?", "Les pairs sont perçus comme plus crédibles et proches, facilitant l\u2019identification et l\u2019appropriation des messages de prévention par la population cible."),
    ("Qu\u2019est-ce que le « nudge » en promotion de la santé ?", "Une incitation douce modifiant l\u2019architecture des choix pour orienter les comportements vers des options plus saines, sans contrainte ni interdiction."),
    ("Donnez un exemple de nudge en santé.", "Placer les fruits à hauteur des yeux à la cantine pour favoriser leur consommation, ou peindre des escaliers en couleurs pour encourager leur utilisation."),
    ("Qu\u2019est-ce que la théorie sociale cognitive de Bandura ?", "Une théorie postulant que le comportement résulte de l\u2019interaction entre facteurs personnels, comportementaux et environnementaux, avec un rôle central du sentiment d\u2019auto-efficacité."),
    ("Qu\u2019est-ce que le sentiment d\u2019auto-efficacité ?", "La croyance d\u2019un individu en sa capacité à réaliser une action avec succès. Plus il est élevé, plus la personne est susceptible d\u2019adopter un comportement de santé."),
    ("Qu\u2019est-ce que l\u2019évaluation formative dans un projet ?", "Une évaluation réalisée pendant le déroulement du projet pour ajuster les actions en cours et corriger les dysfonctionnements identifiés."),
    ("Qu\u2019est-ce que l\u2019évaluation sommative dans un projet ?", "Une évaluation réalisée à la fin du projet pour mesurer l\u2019atteinte des objectifs et produire un bilan global des résultats et de l\u2019impact."),
    ("Qu\u2019est-ce que la triangulation des données en évaluation ?", "L\u2019utilisation de plusieurs sources de données (quantitatives et qualitatives) et de méthodes pour croiser les informations et renforcer la validité des conclusions."),
    ("Qu\u2019est-ce qu\u2019un groupe de travail thématique dans un projet ?", "Un sous-groupe de participants chargé de travailler sur un aspect spécifique du projet (communication, logistique, évaluation, partenariats)."),
    ("Qu\u2019est-ce que le concept de « compétence culturelle » en prévention ?", "La capacité des professionnels à adapter leurs interventions aux spécificités culturelles de la population cible pour une meilleure efficacité."),
    ("Pourquoi la durabilité est-elle un enjeu des projets de prévention ?", "Un projet ponctuel a un impact limité. La pérennisation permet de maintenir les bénéfices dans le temps et de renforcer les acquis de la population."),
    ("Qu\u2019est-ce qu\u2019une revue de littérature dans la conception d\u2019un projet ?", "L\u2019analyse systématique des publications scientifiques existantes sur le sujet pour fonder le projet sur les données probantes les plus récentes."),
    ("Qu\u2019est-ce que le cadre logique d\u2019un projet ?", "Un tableau synthétique présentant la hiérarchie des objectifs, les indicateurs, les sources de vérification et les hypothèses/risques du projet."),
    ("Qu\u2019est-ce que l\u2019analyse des parties prenantes ?", "L\u2019identification et la caractérisation de tous les acteurs concernés par le projet : leurs intérêts, leur pouvoir d\u2019influence et leur rôle potentiel."),
    ("Qu\u2019est-ce qu\u2019un indicateur de résultat ?", "Une mesure quantifiable permettant d\u2019évaluer si un objectif spécifique a été atteint (ex : pourcentage de participants ayant modifié un comportement)."),
    ("Qu\u2019est-ce qu\u2019un indicateur de processus ?", "Une mesure permettant de suivre le déroulement du projet : nombre d\u2019ateliers réalisés, taux de participation, respect du calendrier."),
    ("Qu\u2019est-ce que la mobilisation sociale en prévention ?", "L\u2019engagement actif de la société civile (associations, citoyens, médias) autour d\u2019une cause de santé publique pour créer un mouvement collectif."),
    ("Qu\u2019est-ce que le concept de « capacitation » en santé ?", "Synonyme d\u2019empowerment : processus par lequel les individus développent leur capacité à agir sur leur santé et leur environnement."),
    ("Qu\u2019est-ce que la communication pour la santé ?", "L\u2019utilisation de stratégies de communication (médias, réseaux sociaux, supports écrits) pour diffuser des messages de prévention et promouvoir la santé."),
    ("Qu\u2019est-ce que l\u2019approche participative en projet de santé ?", "Une démarche impliquant les bénéficiaires dans toutes les phases du projet (diagnostic, conception, mise en œuvre, évaluation) pour garantir l\u2019adéquation aux besoins."),
    ("Pourquoi faut-il réaliser un état des lieux avant de lancer un projet ?", "Pour connaître les problèmes de santé, les ressources existantes, les interventions déjà menées et éviter de dupliquer des actions inefficaces."),
    ("Qu\u2019est-ce que l\u2019acceptabilité d\u2019une intervention de prévention ?", "Le degré auquel la population cible considère l\u2019intervention comme appropriée, adaptée à ses valeurs et praticable dans son contexte de vie."),
    ("Qu\u2019est-ce que la transférabilité d\u2019une intervention ?", "La possibilité d\u2019adapter et de reproduire une intervention efficace dans un autre contexte ou auprès d\u2019une autre population, en tenant compte des spécificités locales."),
    ("Qu\u2019est-ce que le suivi (monitoring) d\u2019un projet ?", "La collecte continue de données sur le déroulement du projet pour s\u2019assurer que les activités sont réalisées conformément au plan et identifier les ajustements nécessaires."),
    ("Qu\u2019est-ce qu\u2019un compte-rendu intermédiaire de projet ?", "Un document faisant le bilan des activités réalisées à mi-parcours, analysant les écarts par rapport au plan initial et proposant des ajustements."),
    ("Qu\u2019est-ce que la reproductibilité d\u2019un projet de prévention ?", "La capacité du projet à être reproduit dans des conditions similaires en obtenant des résultats comparables."),
    ("Qu\u2019est-ce que la valorisation d\u2019un projet de prévention ?", "La diffusion des résultats et des enseignements tirés du projet auprès des professionnels, décideurs et communautés pour enrichir les pratiques."),
    ("Qu\u2019est-ce qu\u2019un retour d\u2019expérience (RETEX) en santé publique ?", "L\u2019analyse structurée a posteriori d\u2019une action ou d\u2019un événement pour en tirer des enseignements et améliorer les pratiques futures."),
    ("Pourquoi l\u2019implication des usagers est-elle essentielle dans un projet ?", "Elle garantit que le projet répond aux besoins réels, améliore l\u2019adhésion de la population et renforce la légitimité des actions menées."),
]

# FC3 extra (need 39 more to reach 100)
fc3_extra = [
    ("Qu\u2019est-ce que la mortalité évitable liée à la prévention ?", "Les décès qui auraient pu être évités par des actions de prévention primaire (ex : décès par cancer du poumon lié au tabac, accident de la route)."),
    ("Qu\u2019est-ce que le rapport Lalonde (1974) ?", "Un rapport canadien fondateur identifiant quatre grands déterminants de santé : biologie humaine, environnement, habitudes de vie et organisation des soins de santé."),
    ("Pourquoi le rapport Lalonde est-il considéré comme précurseur ?", "Il a été le premier document officiel à reconnaître que la santé dépend largement de facteurs extérieurs au système de soins, orientant vers la prévention."),
    ("Qu\u2019est-ce que la notion de « gradient social » en santé ?", "La relation linéaire et continue entre position socio-économique et état de santé : plus on est bas dans l\u2019échelle sociale, plus la santé se dégrade."),
    ("Qu\u2019est-ce que l\u2019universalisme proportionné ?", "Une stratégie combinant des actions universelles (pour tous) avec des actions proportionnelles aux besoins des groupes les plus défavorisés."),
    ("Pourquoi l\u2019universalisme proportionné est-il préférable au ciblage ?", "Il évite la stigmatisation des populations vulnérables tout en leur accordant des ressources supplémentaires proportionnelles à leurs besoins."),
    ("Qu\u2019est-ce que l\u2019épigénétique en lien avec les déterminants de santé ?", "L\u2019étude des modifications de l\u2019expression des gènes causées par l\u2019environnement (stress, pollution, alimentation), sans changement de la séquence ADN."),
    ("Qu\u2019est-ce que les « 1000 premiers jours » en santé publique ?", "La période de la conception aux 2 ans de l\u2019enfant, considérée comme cruciale car les déterminants environnementaux et sociaux y ont un impact majeur sur la santé future."),
    ("Qu\u2019est-ce que la précarité énergétique comme déterminant de santé ?", "L\u2019incapacité de chauffer correctement son logement, entraînant des pathologies respiratoires, cardiovasculaires et des troubles de la santé mentale."),
    ("Comment l\u2019urbanisme influence-t-il la santé ?", "L\u2019aménagement urbain (espaces verts, pistes cyclables, transport en commun) favorise l\u2019activité physique et réduit la pollution, améliorant la santé des habitants."),
    ("Qu\u2019est-ce que la santé au travail comme déterminant ?", "Les conditions de travail (charge physique, stress, horaires, exposition aux toxiques) influencent directement la santé physique et mentale des travailleurs."),
    ("Qu\u2019est-ce que le burn-out ou syndrome d\u2019épuisement professionnel ?", "Un état d\u2019épuisement physique, émotionnel et mental causé par un stress professionnel prolongé, caractérisé par la fatigue, le cynisme et la perte d\u2019efficacité."),
    ("Qu\u2019est-ce que la pollution atmosphérique comme déterminant environnemental ?", "L\u2019exposition aux particules fines (PM2,5, PM10), à l\u2019ozone et au dioxyde d\u2019azote, responsable de maladies respiratoires, cardiovasculaires et de cancers."),
    ("Combien de décès prématurés la pollution de l\u2019air cause-t-elle en France ?", "Environ 40 000 à 48 000 décès prématurés par an en France sont attribués à la pollution de l\u2019air extérieur (particules fines)."),
    ("Qu\u2019est-ce que la précarité alimentaire comme déterminant ?", "L\u2019impossibilité d\u2019accéder à une alimentation suffisante et de qualité, favorisant l\u2019obésité, le diabète et les carences nutritionnelles."),
    ("Comment le niveau d\u2019éducation influence-t-il la santé ?", "Un niveau d\u2019éducation plus élevé est associé à une meilleure compréhension des messages de santé, à de meilleures habitudes de vie et à un accès facilité aux soins."),
    ("Qu\u2019est-ce que l\u2019isolement social comme déterminant de santé ?", "Le manque de liens sociaux et de soutien communautaire, associé à un risque accru de dépression, de maladies cardiovasculaires et de mortalité prématurée."),
    ("Qu\u2019est-ce que le concept de « santé dans toutes les politiques » ?", "L\u2019intégration de la dimension santé dans toutes les décisions politiques (transport, logement, éducation, environnement) et pas seulement dans le secteur sanitaire."),
    ("Comment les conditions de travail agissent-elles comme déterminant social ?", "Les emplois précaires, le chômage, le travail de nuit et les horaires décalés augmentent les risques de troubles musculo-squelettiques, cardiovasculaires et psychiques."),
    ("Qu\u2019est-ce que l\u2019accès géographique aux soins comme déterminant ?", "La distance entre le domicile et les structures de soins influence le recours aux soins préventifs et curatifs, créant des inégalités territoriales."),
    ("Qu\u2019est-ce que le renoncement aux soins ?", "Le fait de ne pas recourir à des soins nécessaires pour des raisons financières, géographiques ou de délai d\u2019attente. Il touche davantage les populations défavorisées."),
    ("Quel lien existe entre revenus et santé ?", "Les personnes à faibles revenus ont une espérance de vie plus courte, un accès réduit aux soins et une plus grande exposition aux facteurs de risque."),
    ("Qu\u2019est-ce que la notion de « double peine » en santé ?", "Les populations les plus défavorisées sont à la fois plus exposées aux facteurs de risque et moins bien prises en charge par le système de santé."),
    ("Comment la culture influence-t-elle les comportements de santé ?", "Les normes culturelles façonnent les habitudes alimentaires, les pratiques corporelles, le rapport au soin et la perception de la maladie."),
    ("Qu\u2019est-ce que les inégalités environnementales de santé ?", "Les différences d\u2019exposition aux risques environnementaux (pollution, bruit, habitat insalubre) selon la catégorie socio-économique."),
    ("Qu\u2019est-ce que le concept d\u2019exposome ?", "L\u2019ensemble des expositions environnementales (chimiques, physiques, biologiques, psychosociales) auxquelles un individu est soumis tout au long de sa vie."),
    ("Pourquoi les déterminants sont-ils souvent « imbriqués » ?", "Un déterminant en influence d\u2019autres : par exemple, la précarité économique entraîne un logement insalubre, une alimentation de mauvaise qualité et un accès réduit aux soins."),
    ("Qu\u2019est-ce que l\u2019effet « cumulatif » des déterminants ?", "L\u2019accumulation de facteurs défavorables (pauvreté + pollution + stress + mauvaise alimentation) multiplie les risques pour la santé de manière non linéaire."),
    ("Qu\u2019est-ce que la résilience individuelle face aux déterminants de santé ?", "La capacité d\u2019un individu à faire face aux adversités et à maintenir un bon état de santé malgré des conditions défavorables."),
    ("Quel rôle joue le soutien social comme déterminant protecteur ?", "Les réseaux sociaux et communautaires offrent un soutien émotionnel, pratique et informatif qui protège contre les effets négatifs du stress et de la précarité."),
    ("Qu\u2019est-ce que l\u2019intersectorialité dans l\u2019action sur les déterminants ?", "La collaboration entre secteurs (santé, éducation, urbanisme, emploi) pour agir de manière coordonnée sur les multiples déterminants de santé."),
    ("Pourquoi agir sur les déterminants est-il plus efficace que traiter les maladies ?", "Agir en amont sur les causes fondamentales permet de réduire l\u2019incidence des maladies pour l\u2019ensemble de la population, pas seulement pour les malades."),
    ("Qu\u2019est-ce que la théorie de la « cause des causes » de Michael Marmot ?", "Les inégalités sociales sont la cause fondamentale des inégalités de santé. Agir sur les conditions sociales est indispensable pour améliorer la santé."),
    ("Qui est Michael Marmot et quelle est sa contribution ?", "Épidémiologiste britannique connu pour ses travaux sur les inégalités de santé, notamment l\u2019étude Whitehall montrant le gradient social de mortalité chez les fonctionnaires."),
    ("Qu\u2019est-ce que l\u2019étude Whitehall ?", "Une étude de cohorte sur les fonctionnaires britanniques montrant que la mortalité augmente à chaque échelon inférieur de la hiérarchie professionnelle, indépendamment des facteurs classiques."),
    ("Comment les politiques fiscales agissent-elles sur les déterminants ?", "La taxation du tabac, de l\u2019alcool et des boissons sucrées modifie les comportements de consommation en augmentant le prix des produits nocifs."),
    ("Qu\u2019est-ce que le « paradoxe français » en matière de déterminants ?", "La France dispose d\u2019un bon système de soins mais présente des inégalités sociales de santé parmi les plus élevées d\u2019Europe occidentale."),
    ("Pourquoi les enfants de milieux défavorisés sont-ils plus touchés par l\u2019obésité ?", "L\u2019accès limité à une alimentation de qualité, le manque d\u2019infrastructures sportives, la sédentarité liée aux écrans et le stress familial favorisent la prise de poids."),
    ("Qu\u2019est-ce que la notion de « capabilité » de Sen en lien avec la santé ?", "La capacité réelle d\u2019un individu à choisir et réaliser des modes de vie valorisés, dépendant des ressources disponibles et de l\u2019environnement social."),
]

# Read current file
with open(TARGET, 'r') as f:
    content = f.read()

# Remove trailing closing brace
content = content.rstrip()
if content.endswith('}'):
    content = content[:-1]

# Find the end of fc1 list and insert extra
def insert_extra_before_closing_bracket(content, key, extras):
    """Insert extra tuples before the closing ] of a given key's list."""
    idx = content.find(f'"{key}"')
    # Find the closing ] for this list
    bracket_start = content.find('[', idx)
    depth = 0
    for i in range(bracket_start, len(content)):
        if content[i] == '[': depth += 1
        elif content[i] == ']': depth -= 1
        if depth == 0:
            bracket_end = i
            break
    # Build extra tuples string
    extra_str = ""
    for q, a in extras:
        q_escaped = q.replace('\\', '\\\\').replace('"', '\\"')
        a_escaped = a.replace('\\', '\\\\').replace('"', '\\"')
        # Unescape the unicode that we want to keep
        extra_str += f'    ("{q}", "{a}"),\n'
    # Insert before closing bracket
    content = content[:bracket_end] + extra_str + content[bracket_end:]
    return content

content = insert_extra_before_closing_bracket(content, "SP_Promotion_Prevention/fc1.html", fc1_extra)
content = insert_extra_before_closing_bracket(content, "SP_Promotion_Prevention/fc2.html", fc2_extra)
content = insert_extra_before_closing_bracket(content, "SP_Promotion_Prevention/fc3.html", fc3_extra)

# Add closing brace back
content = content.rstrip() + "\n}\n"

with open(TARGET, 'w') as f:
    f.write(content)

# Verify counts
import re
for key in ['fc1', 'fc2', 'fc3']:
    pattern = f'{key}.html'
    idx = content.find(pattern)
    bracket_start = content.find('[', idx)
    depth = 0
    for i in range(bracket_start, len(content)):
        if content[i] == '[': depth += 1
        elif content[i] == ']': depth -= 1
        if depth == 0:
            bracket_end = i
            break
    section = content[bracket_start:bracket_end+1]
    tuples = re.findall(r'\("', section)
    print(f'{key}: {len(tuples)} flashcards')

print("Done inserting extras for fc1-fc3")

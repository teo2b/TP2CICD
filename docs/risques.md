### R1 — Déploiement non contrôlé sur `main` sans tests ni revue de code

* **Catégorie :** Fiabilité / Qualité logicielle (CI/CD)
* **Source dans le scénario et la carte contexte :**
  * *Anciennes pratiques :* « Tout le monde poussait directement sur la branche principale »[cite: 1], « un workflow construisait l'image (...) et la déployait sans tests en SSH à chaque push »[cite: 1], « les tests existaient à peine et personne ne les lançait »[cite: 1].
  * *Incident fondateur :* Déploiement un vendredi à 19 h ayant bloqué les commandes pendant 14 heures en pleine saison touristique[cite: 1].
  * *Carte contexte et parties prenantes :* Équipe restreinte de 3 développeurs (dont 1 freelance à mi-temps payé à l'heure qui ne veut pas attendre de relecture)[cite: 2] et pression du Product Owner pour livrer rapidement les améliorations demandées par les restaurateurs[cite: 2].

* **Scénario concret de défaillance :**
  1. Sous la pression du Product Owner pour livrer une évolution avant le week-end[cite: 2], le freelance (en fin de demi-journée) ou l'un des deux développeurs internes pousse une modification directement sur `main` sans suite de tests ni relecture[cite: 1, 2].
  2. Le pipeline déclenche immédiatement le *build* et le déploiement en production sans aucune barrière de qualité (*quality gate*)[cite: 1].
  3. Une régression sur la route critique `POST /orders` passe en production un vendredi soir[cite: 1, 3]. L'équipe étant réduite et le freelance n'étant plus sur son créneau de mi-temps, personne n'intervient rapidement : la prise de commande est paralysée pendant 14 heures en pleine période d'affluence[cite: 1].

* **Gravité : Critique (4/4)**
  * *Justification :* Interruption totale du cœur de métier (prise de commandes) en période critique[cite: 1], perte directe de chiffre d'affaires, et atteinte majeure à la crédibilité de la plateforme auprès des producteurs et des restaurateurs (point rouge de la CEO : *« Plus jamais un mois d'août comme celui-là »*)[cite: 1, 2].

* **Mesures de traitement dans le futur socle :**
  1. **Verrouillage de `main` (*Branch Protection Rules*) :** Interdiction technique de tout `git push` direct (y compris pour les administrateurs) et obligation de passer par une Pull Request (PR)[cite: 3].
  2. **Automatisation des tests bloquants (CI) :** Mise en place d'un workflow GitHub Actions exécutant systématiquement un *linter* et les tests automatisés (unitaires et d'intégration sur `/health`, `GET /products`, `POST /orders`) à chaque ouverture ou mise à jour de PR[cite: 3]. Le bouton *Merge* est bloqué tant que la CI n'est pas au vert.
  3. **Revue de code calibrée (1 relecteur) :** Exigence d'au moins **1 approbation humaine** d'un développeur interne avant fusion, afin de garantir un double regard sans créer de goulot d'étranglement dans une équipe de 2,5 ETP[cite: 2].
  4. **Fenêtre de déploiement maîtrisée :** Interdiction des mises en production le vendredi après-midi ou veille de week-end (sauf *hotfix* critique approuvé), et séparation entre le *merge* sur `main` (staging) et le déploiement en production (soumis à approbation humaine)[cite: 3, 4].

* **Positionnement sur la matrice Gravité / Effort :**
  * **Gravité :** Critique
  * **Effort :** Moyen
  * **Justification :** Bien que la configuration des protections GitHub soit rapide, ce risque demande d'écrire une première base de tests automatisés fiables[cite: 1, 3] et d'ancrer une discipline de revue de code dans une petite équipe[cite: 2]. L'impact sur la stabilité de la production en fait une priorité absolue (**P1**).
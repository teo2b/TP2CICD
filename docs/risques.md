### Risque 1 — Déploiement direct sur `main` sans tests ni relecture

* **Catégorie :** Fiabilité / Qualité logicielle
* **Origine :**
  * Les développeurs poussent directement sur la branche principale et le déploiement se fait sans tests à chaque push.
  * L'incident d'août (déploiement un vendredi à 19 h, commandes bloquées pendant 14 h).
  * Notre équipe est réduite (3 développeurs dont 1 freelance à mi-temps), avec une forte pression du Product Owner pour livrer vite et un freelance qui ne veut pas attendre de relecture.

* **Scénario de défaillance :**
  Pour répondre à une demande urgente des restaurateurs avant le week-end, un développeur (ou le freelance en fin de demi-journée) pousse une modification directement sur `main`. Le déploiement se lance automatiquement sans vérification. Un bug sur `POST /orders` passe en production un vendredi soir. L'équipe étant restreinte et le freelance absent sur l'autre moitié de la semaine, personne ne réagit à temps et les commandes restent bloquées tout le week-end.

* **Gravité : Critique**
  Arrêt total de la prise de commande en pleine saison touristique, perte directe de chiffre d'affaires et perte de confiance des clients.

* **Mesures de traitement :**
  * **Protection de la branche `main` :** blocage des pushs directs sur GitHub et obligation de passer par une Pull Request.
  * **Tests automatiques bloquants :** lancement d'une suite de tests sur l'API via GitHub Actions à chaque Pull Request. La fusion est impossible si les tests échouent.
  * **Relecture obligatoire (1 personne) :** validation requise par au moins un développeur interne avant de fusionner, afin de sécuriser le code sans ralentir notre petite équipe.
  * **Déploiement en production contrôlé :** pas de mise en production automatique au merge, et interdiction de déployer le vendredi après-midi sauf urgence critique.

* **Positionnement Gravité / Effort :**
  * **Gravité :** Critique | **Effort :** Moyen
  * **Justification :** Le verrouillage de GitHub est rapide, mais écrire des tests fiables et installer l'habitude des relectures dans une équipe de 2,5 ETP demande un peu de mise en place. C'est la priorité n°1 pour éviter un nouvel incident comme celui d'août.
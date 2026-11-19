# ADR 0001 : Adoption de GitHub Flow comme stratégie de branches

## Contexte
L'équipe est composée de 3 développeurs internes à temps plein (dont une Lead Dev) et d'un développeur freelance à mi-temps (4 personnes au total). Auparavant, tout le monde poussait directement sur la branche principale sans tests ni relecture, ce qui a provoqué une interruption des commandes de 14 heures en août.
Nous devons pouvoir livrer régulièrement les évolutions demandées par le Product Owner tout en sécurisant la production et en évitant de bloquer le freelance sur ses créneaux de travail à mi-temps.

## Décision
Nous adoptons **GitHub Flow** avec une séparation claire entre les droits d'intégration sur le code (`main`) et les droits de mise en production.

### Structure et règles de gestion
* **Branche `main` :** Elle représente en permanence l'état prêt pour la production. Elle est déployée automatiquement en environnement de staging à chaque fusion, puis promue en production après approbation humaine. Aucun push direct n'est autorisé.
* **Branches de travail :** Pour chaque tâche (nouvelle fonctionnalité ou correction), le développeur crée une branche courte directement depuis `main` en respectant la convention `feat/<nom-tache>` ou `fix/<nom-bug>`.
* **Répartition des rôles (qui fait quoi) :**
  * **Les 3 développeurs internes :** Ils créent leurs branches, ouvrent des Pull Requests (PR), assurent les revues de code et possèdent les droits de fusion (*merge*) sur `main`. L'auto-validation est interdite : un interne ne peut merger que la PR d'un collègue ou du freelance après l'avoir relue.
  * **Le développeur freelance :** Il crée ses branches sur ses tâches dédiées et ouvre des PR, mais il n'a pas les droits pour approuver ni merger sur `main`. L'un des 3 développeurs internes doit obligatoirement valider et fusionner son travail.
  * **Validation de la production (CD) :** Si les 3 internes peuvent merger dans `main` (pour garder de la fluidité), l'approbation finale déclenchant le déploiement en production est réservée à la **Lead Dev** (avec un second interne désigné comme backup en cas d'absence).
* **Cycle de vie d'une PR :** Dès que la suite de tests automatisés (CI) passe au vert et qu'un développeur interne a approuvé la PR, celle-ci est fusionnée dans `main` (via *Squash and merge* pour conserver un historique linéaire lisible) et la branche temporaire est immédiatement supprimée.

## Justification par rapport aux risques
* **R1 (Déploiement non contrôlé sur `main`) :** Le passage obligatoire par une branche dédiée et une Pull Request permet d'imposer l'exécution bloquante des tests et une relecture humaine avant toute intégration sur `main`.
* **R5 (Goulot d'étranglement et contournement des règles) :** 
  * Nous avons écarté GitFlow, trop lourd pour notre effectif, au profit d'une seule branche permanente (`main`).
  * Nous avons refusé de restreindre le droit de merge à une seule personne afin d'éviter un point de défaillance unique (SPOF) : avec 3 internes habilités à relire et merger, le freelance à mi-temps n'est jamais bloqué en attente de validation, ce qui répond à l'exigence de rapidité du Product Owner sans sacrifier le contrôle sur la production.

## Procédure pour un correctif urgent (Hotfix)
En cas d'anomalie critique détectée en production :
1. Un développeur interne crée immédiatement une branche `hotfix/<description-courte>` à partir de `main`.
2. Il développe le correctif accompagné d'un test de non-régression reproduisant l'erreur.
3. Il ouvre une PR vers `main`. La CI doit valider les tests et un autre développeur interne effectue une relecture prioritaire (en cas d'indisponibilité exceptionnelle des deux autres internes, une dérogation explicite est documentée dans la description de la PR).
4. Après fusion sur `main`, le pipeline déploie le correctif en staging, puis la Lead Dev (ou son backup) approuve le déploiement immédiat en production.
5. **Réintégration dans le travail en cours :** Comme toutes les branches de fonctionnalités partent directement de `main`, les autres développeurs n'ont qu'à mettre à jour leur branche locale (`git pull origin main` ou `git rebase main`) pour récupérer le correctif. Il n'y a aucune double fusion à gérer.

## Signaux de remise en cause de ce choix
Cette stratégie devra être réévaluée si l'un des signaux suivants se manifeste :
* **Augmentation de la taille de l'équipe :** Au-delà de 6 à 8 développeurs actifs en parallèle, les conflits d'intégration sur `main` et l'engorgement de la file de CI ralentiront les livraisons (nécessitera d'introduire des *merge queues* ou une branche d'intégration).
* **Maintenance de versions multiples :** Si différents clients (restaurateurs ou producteurs) exigent d'utiliser des versions distinctes de l'API simultanément, il faudra migrer vers une stratégie avec des branches de support par version (type *Release Flow* ou *GitFlow*).
* **Blocage des livraisons par des fonctionnalités inachevées :** Si des développements longs empêchent régulièrement de livrer des correctifs prêts sur `main`, il faudra soit découper davantage les tâches, soit mettre en place des *feature flags*.
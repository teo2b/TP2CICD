# Analyse des risques

> **Carte contexte tirée** : équipe de **3 développeurs** + **1 freelance** qui peut partir ou augmenter ses tarifs à tout moment. Les risques propres à cette carte sont marqués **[carte]** (R7, R8, R9, R10).

Légende gravité : 🔴 critique (arrêt du métier / fuite) · 🟠 majeure · 🟡 modérée.
Légende effort : S (< 1 h) · M (< 1 journée) · L (> 1 journée).

| # | Risque | Origine |
|---|---|---|
| R1 | Push direct sur `main` | Anciennes pratiques |
| R2 | Déploiement automatique sans tests, image `latest` | Anciennes pratiques |
| R3 | Secrets versionnés (`.env`) | Anciennes pratiques |
| R4 | Migrations de base lancées à la main | Anciennes pratiques |
| R5 | Impossible de savoir quelle version tourne / pas de rollback | Incident d'août |
| R6 | Déploiement vendredi 19 h sans garde-fou humain | Incident d'août |
| R7 | Relecteur unique absent → blocage ou contournement | Lead dev / carte (3 devs) |
| R8 | Freelance : accès trop large, ou revues contournées | Carte (freelance) |
| R9 | Départ soudain du freelance : savoir perdu, accès non révoqués | Carte (freelance) |
| R10 | Hausse de tarifs / dépendance économique au freelance | Carte (freelance) |

## Détail

### R1 — Push direct sur `main`
- **Scénario** : un dev pousse un correctif non relu un vendredi ; il casse `POST /orders`.
- **Gravité** : 🟠 — toute erreur part directement vers la production.
- **Mesure** : protection de branche `main` (PR obligatoire, 1 review, CI verte, pas de force-push, règle appliquée aux admins). Voir CONTRIBUTING §3.

### R2 — Déploiement sans tests, tag `latest`
- **Scénario** : un push déclenche build + déploiement SSH sans test ; `latest` pointe vers une image cassée, impossible de dire laquelle était la précédente.
- **Gravité** : 🔴 — c'est la cause directe de l'incident des 14 h.
- **Mesure** : CI bloquante (tests + build) avant merge ; déploiement uniquement sur tag `vX.Y.Z` ; images taguées par version + sha, **jamais `latest`**.

### R3 — Secrets dans le dépôt
- **Scénario** : le dépôt (même privé) fuite ou un ancien collaborateur le clone ; mots de passe et clés d'API sont exposés dans l'historique.
- **Gravité** : 🔴 — fuite de données producteurs/clients.
- **Mesure** : `.env` ignoré (`.gitignore`, `.dockerignore`), `.env.example` sans valeur réelle, secrets dans GitHub Environments + `.env` chmod 600 sur le VPS, *secret scanning + push protection* activés.

### R4 — Migrations manuelles
- **Scénario** : on « oublie » la migration, l'API démarre sur un schéma ancien et plante au premier ordre.
- **Gravité** : 🟠
- **Mesure** : schéma et migrations versionnés (`db/`), exécutés **par le script de déploiement**, idempotents ; étape de déploiement échouée si le script échoue.

### R5 — Version inconnue, pas de rollback
- **Scénario** : la prod est en panne, personne ne sait quelle version tourne ni vers laquelle revenir.
- **Gravité** : 🔴 — durée d'indisponibilité multipliée.
- **Mesure** : SemVer + tags Git ; `/health` renvoie la version ; images immuables dans GHCR ; workflow `Rollback` (< 5 min). Voir [pipeline.md](pipeline.md).

### R6 — Déploiement sans garde-fou humain
- **Scénario** : un merge de fin de journée part en prod sans que personne ne regarde.
- **Gravité** : 🟠
- **Mesure** : environnement `production` avec *required reviewers* ; staging + smoke test avant ; règle d'équipe « pas de mise en prod le vendredi après 16 h sauf correctif urgent » (règle de discipline, non imposable par l'outil).

### R7 — Relecteur unique absent **[carte]**
- **Scénario** : avec seulement 3 devs, un absent = un tiers de l'équipe en moins ; la PR urgente attend ou est mergée sans revue.
- **Gravité** : 🟡 organisationnel.
- **Mesure** : 1 relecteur **de n'importe quel interne** + CODEOWNERS en simple suggestion ; si urgence et personne dispo : 2e membre en visio, contournement documenté dans la PR.

### R8 — Freelance : accès trop large ou revues contournées **[carte]**
- **Scénario** : le freelance, payé à l'heure, pousse sans revue pour aller vite, ou détient des accès admin / des secrets de production dont il n'a pas besoin.
- **Gravité** : 🟠 — un compte externe avec trop de droits est une porte d'entrée (R1, R3).
- **Mesure** : collaborateur avec droit *Write* (pas *Admin*), **aucun accès aux secrets de production** ; mêmes règles que tout le monde (PR + 1 review, la protection de branche s'applique à lui) ; revue sous 4 h ouvrées pour ne pas le bloquer ; PR petites.

### R9 — Départ soudain du freelance **[carte]**
- **Scénario** : il part du jour au lendemain en plein développement : son code n'est que dans sa tête ou sur sa branche locale, sa fonctionnalité est à moitié faite, et ses accès (GitHub, VPS, clé SSH) restent actifs.
- **Gravité** : 🟠 — perte de savoir et risque de sécurité.
- **Mesure** : (1) tout travail passe par des branches poussées et des PR courtes (< 2 jours) : rien ne reste en local ; (2) revue obligatoire par un membre de l'équipe interne : au moins 1 dev interne connaît chaque morceau de code ; (3) décisions et choix techniques écrits (ADR, README, descriptions de PR) ; (4) checklist de départ : retirer le collaborateur GitHub, révoquer sa clé SSH sur le VPS, et faire tourner tout secret auquel il aurait eu accès ; (5) le freelance ne détient seul aucun accès critique (déploiement, secrets) : voir R3.

### R10 — Hausse de tarifs / dépendance économique **[carte]**
- **Scénario** : le freelance augmente ses prix et l'équipe, qui dépend de lui pour livrer, n'a pas de marge de négociation ni de plan B.
- **Gravité** : 🟡 — risque de budget, pas d'arrêt du service.
- **Mesure** : limiter la dépendance par la même mesure que R9 (savoir partagé, documentation) ; lui confier des tâches **bien délimitées et estimées** (issues avec périmètre clair) plutôt que du « temps libre » ; prévoir qu'un dev interne peut reprendre n'importe quelle tâche ; suivre le coût des tâches freelance pour décider vite d'internaliser ou non. *(Mesure surtout organisationnelle : l'outil GitHub ne peut pas la faire respecter.)*

## Matrice gravité × effort

| | Effort S | Effort M | Effort L |
|---|---|---|---|
| 🔴 Critique | **R2**, **R3**, **R5** (mesures de base) | R5 (rollback complet) | — |
| 🟠 Majeure | **R1**, R6 (approbation), **R8** (droits Write, pas d'accès aux secrets) | R4, **R9** (checklist de départ + branches courtes) | — |
| 🟡 Modérée | — | R7, R10 (tâches délimitées, savoir partagé) | — |

**Justification** : R1, R2, R3 sont à la fois critiques et peu coûteux (quelques réglages GitHub + un workflow) → à faire en premier. R5 se fait en deux temps : versionnage immédiat (S), rollback automatisé ensuite (M). R4 demande de structurer le script de déploiement (M). R8 se règle en quelques minutes dans GitHub (droits du collaborateur), donc effort S malgré une gravité majeure. R9 est plus grave que R10 car il mêle perte de savoir et sécurité ; il demande de la discipline continue (M). R7 et R10 sont organisationnels : moins graves, traités par des règles écrites plutôt que par de l'outillage.
# CONTRIBUTING

Ce document applique l'[ADR 0001](docs/adr/0001-strategie-branches.md) (GitHub Flow) à notre équipe : **3 développeurs internes (dont la Lead Dev) + 1 développeur freelance à mi-temps**.

> Chaque règle cite le risque qu'elle traite (voir [docs/risques.md](docs/risques.md)).
> ✅ = imposé par la configuration GitHub · 🧍 = repose sur la discipline de l'équipe (voir §9).

## 1. Rôles

| Rôle | Qui | Crée des branches / PR | Relit et approuve | Merge dans `main` | Approuve la production |
|---|---|---|---|---|---|
| Développeur interne | 3 personnes | oui | oui | oui | non |
| Lead Dev | 1 des 3 internes | oui | oui | oui | **oui** |
| Backup production | 1 interne désigné : | oui | oui | oui | **oui** (si la Lead Dev est absente) |
| Freelance | 1 personne | oui | non (il peut commenter) | non | non |


## 2. Relecteurs (R1, R7)

- **1 relecteur** par PR, forcément un **développeur interne** autre que l'auteur ✅ (un auteur ne peut pas approuver sa propre PR ; `CODEOWNERS` fait que seule l'approbation d'un interne compte, donc celle du freelance n'est pas valable).
- Pas besoin que ce soit l'expert du sujet : la CI porte la vérification technique, le relecteur vérifie lisibilité, sécurité et cohérence.
- **Délai cible : 4 h ouvrées** 🧍 (R8 : le freelance, à mi-temps, ne doit pas rester bloqué).
- **Quand le seul relecteur compétent est absent** (R7) : n'importe quel autre interne relit. Si **aucun** autre interne n'est joignable, la PR peut être mergée avec une **dérogation écrite dans la PR** (qui, quand, pourquoi) et une relecture a posteriori sous 24 h 🧍.
- Un interne ne merge que la PR d'un collègue ou du freelance, après l'avoir relue 🧍.

## 3. Nommage

- **Branches** (minuscules, tirets) :
  - `feat/<nom-tache>` : nouvelle fonctionnalité. Ex. `feat/stock-migration`.
  - `fix/<nom-bug>` : correction non urgente. Ex. `fix/prix-negatif`.
  - `hotfix/<description-courte>` : correctif urgent en production.
  - `docs/<sujet>` et `chore/<sujet>` : documentation, CI, config (ajoutés aux conventions de l'ADR pour les PR qui ne touchent pas le code métier).
- **Commits** (Conventional Commits) : `feat: ajoute la colonne stock`, `fix: refuse commande hors stock`, `docs: …`, `chore: …`, `test: …`. 🧍
- **Titre de PR** = message du commit de squash.
- Branche supprimée automatiquement après merge ✅.

## 4. Configuration GitHub (captures dans `docs/config/`)

- **Protection de `main`** ✅ (R1, R2, R7, R8) :
  - PR obligatoire, aucun push direct ;
  - 1 approbation requise, **approbation d'un propriétaire du code obligatoire** (`.github/CODEOWNERS` = les 3 internes) ;
  - checks `Tests` et `Build image` obligatoires ;
  - branche à jour avec `main` avant merge ;
  - pas de force-push, pas de suppression de `main` ;
  - règle valable aussi pour les administrateurs.
- **Merge** ✅ : *squash merge* uniquement ; suppression automatique de la branche après merge.
- **Environnements** ✅ (R6) :
  - `staging` : déploiement automatique à chaque merge dans `main` ;
  - `production` : **Required reviewers = Lead Dev + backup**.
- **Secret scanning + push protection** activés ✅ (R3).
- **Freelance** ✅ (R8) : collaborateur avec le rôle **Write** (jamais Admin). L'approbation d'un interne reste nécessaire pour merger.

## 5. Definition of Done

Une tâche est **terminée** quand :
1. la PR est mergée dans `main` (CI verte, 1 approbation d'un interne) ;
2. des tests couvrent le comportement ajouté ;
3. la documentation concernée est à jour (README, `docs/`) ;
4. le changement est déployé en staging et le smoke test (`/health` + parcours concerné) est OK ;
5. s'il fait partie d'une livraison : la production est approuvée, déployée, et `/health` affiche la bonne version.

## 6. Versionnage (R5)

- SemVer `MAJEUR.MINEUR.CORRECTIF`. La version est posée (tag Git `vX.Y.Z` + release GitHub) au moment de la **promotion en production** approuvée par la Lead Dev ou son backup.
- **Savoir en 10 secondes quelle version tourne** : `curl https://<prod>/health` renvoie `{"status":"ok","version":"X.Y.Z"}`. En staging, la version affichée est `sha-<7 caractères>`.
- Images GHCR taguées par version ou par `sha`. **Jamais `latest`.**

## 7. Secrets (R3)

- **Où** : secrets GitHub des environnements (`staging`, `production`) pour la CI ; fichier `.env` (chmod 600) sur le VPS pour Postgres. Jamais dans Git, jamais dans l'image, jamais dans un message de PR ou de chat.
- **Qui y a accès** : la Lead Dev et le backup (administrateurs du dépôt et du VPS). **Le freelance n'y a pas accès.**
- **Si un secret fuit** :
  1. le révoquer et en créer un nouveau immédiatement ;
  2. mettre à jour GitHub et le VPS, puis redéployer ;
  3. chercher des usages suspects dans les logs ;
  4. purger l'historique Git si nécessaire (`git filter-repo`), en considérant le secret comme compromis de toute façon ;
  5. consigner l'incident dans `docs/incidents.md`.

## 8. Que fait-on du freelance ? (R8, R9, R10)

- **Droits** : Write, sans accès aux secrets ni à la production ; ses PR sont relues et mergées par un interne.
- **Travail visible** : il pousse ses branches sur le dépôt principal (pas de travail uniquement en local) et ouvre une PR **avant la fin de chaque créneau de travail**, même en brouillon (*Draft*) (R9, R10).
- **Tâches délimitées** : il reçoit des issues avec un périmètre et une estimation, pas du « temps libre » (R10).
- **Savoir partagé** : toute PR du freelance est relue par un interne, donc au moins un interne connaît chaque morceau de son code (R9).
- **Départ** (R9) : retirer le collaborateur GitHub, révoquer sa clé SSH éventuelle, vérifier qu'aucune branche n'est restée non poussée, et faire tourner tout secret qu'il aurait pu connaître.
- **Hausse de tarifs** (R10) : décision hors outil ; la règle précédente permet à un interne de reprendre n'importe laquelle de ses tâches.

## 9. Ce que GitHub ne peut pas imposer (discipline) 🧍

- **Qui merge** : sur un dépôt personnel, GitHub ne permet pas de réserver le bouton *Merge* aux internes. Le freelance ne peut pas merger sans l'approbation d'un interne (✅ via `CODEOWNERS`), mais l'engagement « un interne ne merge que la PR d'un collègue ou du freelance » repose sur la discipline.
- **Délai de revue de 4 h ouvrées** (R8).
- **Dérogation** (aucun interne joignable) : la documenter dans la PR (qui, quand, pourquoi) et faire relire sous 24 h.
- **Pas de mise en production le vendredi après 16 h**, sauf correctif urgent approuvé (R6).
- **PR petites** (environ 300 lignes modifiées maximum) et branches poussées chaque jour (R9).
- **Commits conventionnels** et noms de branche conformes.
- **Rotation d'un secret** après le départ du freelance.
# Plan de livraison — US-42 Gestion du stock

## Découpage en tâches

Chaque membre développeur interne a une tâche visible dans l'historique Git.

| Membre | Tâche | Livrables attendus |
|---|---|---|
| Téo | Modélisation et gestion du stock des produits | Champ `stock` disponible par produit, gestion de sa valeur initiale |
| Jean Pascal | Contrôle des commandes | L'API refuse une commande dépassant le stock avec un message clair |
| Hanafi | Tests et validation | Tests du stock suffisant, insuffisant et du produit absent |

## Règles de réalisation

- Chaque tâche est réalisée sur une branche conforme à `CONTRIBUTING.md`.
- Chaque branche passe par une pull request avec un relecteur interne.
- Le freelance ne reçoit pas de tâche d'implémentation sur ce découpage.
- La validation finale couvre les tests, le déploiement en staging et l'approbation de production.

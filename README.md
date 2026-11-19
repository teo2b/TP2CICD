# TP2 CICD

## Carte contexte

- **Equipe** : 3 développeurs internes dont la Lead Dev, + 1 développeur freelance à mi-temps.
- Le freelance peut partir ou augmenter ses tarifs.

## API

- `GET /health`
- `GET /products`
- `POST /orders`
- `PUT /products/{product_id}/stock`

## Lancer le projet localement

1. Copier les variables locales :

   ```powershell
   Copy-Item .env.example .env
   ```

2. Remplacer `POSTGRES_PASSWORD` dans `.env`, puis lancer :

   ```powershell
   docker compose up --build
   ```

3. Vérifier l'API :

   ```powershell
   Invoke-RestMethod http://localhost:8000/health
   Invoke-RestMethod http://localhost:8000/products
   ```

Le démarrage de l'API crée les tables et initialise 1 200 produits. Le script est aussi disponible avec :

```powershell
python scripts/seed.py
```
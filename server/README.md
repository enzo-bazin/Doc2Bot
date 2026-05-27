# Doc2Bot Server - Tests API

## Demarrage rapide

1) Activer le venv si besoin
2) Installer les deps
3) Lancer le serveur

Exemples (depuis la racine du projet) :

```bash
# Option 1
python server/Core/mainloop.py

# Option 2
uvicorn server.Core.mainloop:app --reload --host 0.0.0.0 --port 8000
```

Base URL : http://localhost:8000
Docs OpenAPI : http://localhost:8000/docs

## Etat actuel (middleware actif + routes montees)

Le middleware AuthentificationMiddleware est actif dans l app.
Cela veut dire :

- Toutes les routes sont protegees par un Bearer token
- Sauf celles listees dans PUBLIC_ROUTES dans server/Core/handle_event/middleware.py

Par defaut, PUBLIC_ROUTES = ["/auth/register", "/auth/login"].

Routes montees via server/Routes/router.py :

- /auth/register
- /auth/login
- /recharge
- /ping
- /session/create
- /session/disconnect
- /chatbot/chat

Astuce : si tu veux utiliser Swagger, ajoute aussi /docs et /openapi.json
aux routes publiques.

## Auth rapide (obtenir un token)

### Register

Route : POST /auth/register

```json
{"username": "demo", "password": "demo"}
```

### Login

Route : POST /auth/login

```json
{"username": "demo", "password": "demo"}
```

Reponse :

```json
{"token": "..."}
```

Utilise ensuite :

```
Authorization: Bearer <token>
```

## Tester la route upload PDF (prioritaire)

Route : POST /session/create

- multipart/form-data
- Champ attendu : file
- Auth : Bearer token requis (sauf si /session/create est publique)

Exemple (Windows, avec token) :

```bash
curl.exe -X POST http://localhost:8000/session/create ^
  -H "Authorization: Bearer <token>" ^
  -F "file=@C:\path\to\document.pdf"
```

Exemple (Windows, sans token si route publique) :

```bash
curl.exe -X POST -F "file=@C:\path\to\document.pdf" http://localhost:8000/session/create
```

Reponse attendue :

```json
{"detail": "processing your session..."}
```

Verification : le fichier est enregistre dans server/Upload/temp_anonymous/.

## Autres routes

### Chatbot

Route : POST /chatbot/chat
Auth : Bearer token requis

Corps :

```json
{"message": "Bonjour"}
```

Exemple :

```bash
curl.exe -X POST http://localhost:8000/chatbot/chat ^
  -H "Authorization: Bearer <token>" ^
  -H "Content-Type: application/json" ^
  -d "{\"message\":\"Bonjour\"}"
```

### Ping

Route : POST /ping
Auth : Bearer token requis

### Session disconnect

Route : POST /session/disconnect
Auth : Bearer token requis

### Recharge

Route : POST /recharge
Auth : Bearer token requis

```json
{"euro_paid": 10}
```

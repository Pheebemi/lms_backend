# Support Chat, Admin Handoff Email & MySQL — Setup

Three features added to this project. Everything is env-driven; the code needs
no changes between local and production.

---

## Part 1 — AI Support Chat

Floating widget → Django (`/api/support/chat/`) → AI provider (Groq by default,
any OpenAI-chat-compatible endpoint). The browser never sees the key; nothing is
stored. If the key is empty the endpoint returns `503` and the widget offers the
contact form instead.

**Env (`.env`):**
```
SUPPORT_AI_API_KEY=gsk_...            # Groq key (required for chat to work)
SUPPORT_AI_API_URL=https://api.groq.com/openai/v1/chat/completions   # optional
SUPPORT_AI_MODEL=llama-3.3-70b-versatile                              # optional
```
Any OpenAI-compatible provider works by swapping URL + model + key.

Edit the assistant's knowledge in `support/knowledge.py` — it answers **only**
from those facts and routes anything else to "Talk to a human". Update it
whenever a service, price or flow changes.

Rate limit: `support_chat = 15/minute` per IP (in `REST_FRAMEWORK` settings).

---

## Part 2 — Contact → Admin + Email

"Talk to a human" (or a plain contact form) saves a `support.Contact` row and
emails the admins an alert with the message, the chat transcript, and a link
straight to the admin record. The endpoint **always returns 201** — the message
is saved even if the email fails.

**Recipients:** `ADMIN_ALERT_EMAILS` if set, otherwise every active superuser.

**Env (`.env`):**
```
ADMIN_ALERT_EMAILS=you@example.com,ops@example.com   # optional; else superusers
BASE_URL=https://pheedev.pythonanywhere.com          # builds the admin link
# Email uses the existing EMAIL_HOST_USER / EMAIL_HOST_PASSWORD / DEFAULT_FROM_EMAIL
```

Handoffs appear in Django admin under **Support → Contacts** (read-only, status
editable, filter by status/source).

Rate limit: `support_contact = 5/hour` per IP.

---

## Part 3 — SQLite → MySQL

`settings.py` picks the DB by env: **if `MYSQL_DATABASE` is set → MySQL**
(utf8mb4, strict mode); otherwise → SQLite. No code change to switch.

Driver: MySQL needs `mysqlclient` in the server virtualenv
(`pip install mysqlclient`). It's already available on PythonAnywhere. Leave
`MYSQL_*` unset locally so local stays on SQLite (no driver needed on Windows).

**Steps (order matters):**

1. **Create the MySQL DB as `utf8mb4`** (PythonAnywhere → Databases tab creates
   one; confirm charset). If created as 3-byte utf8, emoji in any text field
   throw `Incorrect string value`:
   ```sql
   ALTER DATABASE `pheedev$default` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. **Export from SQLite FIRST**, before `MYSQL_*` is set:
   ```bash
   python manage.py dumpdata --natural-foreign --natural-primary \
     --exclude contenttypes --exclude auth.permission \
     --exclude admin.logentry --exclude sessions.session \
     --exclude token_blacklist > data.json
   ```
   ⚠️ No `print()` in `settings.py` — it corrupts `data.json` (must start with `[`).

3. **Set the `MYSQL_*` env vars** on the server `.env`:
   ```
   MYSQL_DATABASE=pheedev$default
   MYSQL_USER=pheedev
   MYSQL_PASSWORD=...
   MYSQL_HOST=pheedev.mysql.pythonanywhere-services.com
   MYSQL_PORT=3306
   ```
   Keep the **local** `.env` without these (stays on SQLite).

4. `python manage.py migrate` → builds the tables as utf8mb4.
5. `python manage.py loaddata data.json` → `Installed N objects`.
6. Reload the web app; verify login + data.
7. Keep the old `db.sqlite3` as a snapshot. **Never delete the `MYSQL_*` lines**
   from the server `.env` — it would silently fall back to the empty SQLite.

---

## Deploy checklist (after pulling)

```bash
cd ~/lms_backend
git pull                      # if using git; otherwise upload
source venv/bin/activate
python3.10 manage.py migrate  # applies support.0001 (support_contacts table)
```
Then reload the web app. Set the new env vars above as needed. Frontend (Vercel)
redeploys the chat widget on push — it's mounted globally in `app/layout.tsx`.

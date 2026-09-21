# FutureForge Labs — STEAM Education Platform

**"Building Skills. Engineering the Future."**

Django + PostgreSQL platform for a STEAM/Robotics/AI/Electronics training organization.

## ⚙️ Status: Phase 5 complete

What exists now (on top of Phases 1–4):
- Full project scaffolding, environment-driven settings, complete models, Django Admin
- All public views/URLs/forms, base template, CSS/JS design system, every public page template
- `seed_demo_data` management command populating realistic sample content
- A fully working custom admin dashboard with Create/Edit/Delete for every content type
- **SEO**: dynamic per-page `<title>` and meta description on every template, canonical URLs,
  Open Graph + Twitter Card meta (with real per-page images on Programs/Projects/Blog posts,
  falling back to a generated default share image), a live `sitemap.xml` covering Programs,
  Technologies, Projects, Services and Blog Posts, and a `robots.txt` that disallows the
  dashboard/accounts/django-admin paths while pointing crawlers to the sitemap.
- **Dashboard-wide global search**: a search box in the dashboard topbar (`/dashboard/search/`)
  that searches across Programs, Technologies, Institutions, Projects, Services, Team Members,
  Blog Posts, Media, Messages and Training Requests simultaneously, with direct links to each
  result's edit page.
- Verified end-to-end: `robots.txt` and `sitemap.xml` both render correctly with real seeded
  URLs; per-page Open Graph images were confirmed present on real Program/Blog/Project pages;
  the dashboard global search was confirmed to find real seeded records across categories; and
  a full regression sweep of all 35 public + dashboard + SEO URLs returned 200 with zero
  breakage from earlier phases.

**Not yet done:** a final production-deployment pass (systemd/gunicorn/nginx configuration
guidance) and a last documentation/testing checklist pass — both straightforward once you're
ready to deploy to a real server.

## Setup

```bash
python -m venv venv
source venv/bin/activate        # venv\Scripts\activate on Windows
pip install -r requirements.txt

cp .env.example .env            # then edit DB credentials + SECRET_KEY

# Create the PostgreSQL database & user first, e.g.:
#   createdb futureforge_db
#   createuser futureforge_user --pwprompt

python manage.py migrate
python manage.py seed_demo_data     # populates realistic sample content + creates an admin user
python manage.py collectstatic
python manage.py runserver
```

Seeded admin login: **username `admin`, password `FutureForge2026!`** — change this immediately
in a real deployment. Visit `http://127.0.0.1:8000/` for the public site, `/accounts/login/` then
`/dashboard/` for the full custom CRUD dashboard (with global search at `/dashboard/search/`), or
`/django-admin/` for the built-in Django Admin (useful for bulk edits or advanced fields like the
project image gallery and team social links).

If you'd rather create your own superuser instead of using the seeded one:
```bash
python manage.py createsuperuser
```


## Project layout

See the architecture summary in the project conversation / `docs/` (to be added).

## License

Proprietary — © 2026 FutureForge Labs. All Rights Reserved.

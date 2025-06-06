# PyData RomaCapitale ‑ website

> Static site powered by **[Pelican](https://getpelican.com/)**, deployed on **GitHub Pages**.

* **ProductionURL**: [https://pydataromacapitale.github.io](https://pydataromacapitale.github.io)
* **Sourcecode**: `main`branch (this repo)
* **Builtsite**: `gh-pages`branch (published automatically)

---

## 📁Repo layout

| Path                 | What it contains                                                                         |
| -------------------- |------------------------------------------------------------------------------------------|
| `content/`           | Markdown/ReST pages **plus** meet‑up stubs auto‑generated by the `meetup_events` plug‑in |
| `output/`            | *Built site* — clean HTML/CSS/JS ready to serve (git‑ignored locally; committed by CI)   |
| `plugins/`           | Custom Pelican plug‑ins (currently only the Meetup sync)                                 |
| `themes/roma/`       | Bootstrap 5.3 theme tailored to PyData Roma colours                                      |
| `pelicanconf.py`     | Dev config – relative links, drafts enabled                                              |
| `publishconf.py`     | Prod config – absolute links pointing at GitHub Pages                                    |
| `.github/workflows/` | CI pipeline that builds + deploys on every commit to **`main`**                          |

---

## 🛠Environment

```bash
# Python ≥3.11 is recommended
python -m venv .venv && source .venv/bin/activate

# install deps with the team‑standard package manager
pip install uv
uv sync
```

> **Why uv?**It is a drop‑in for `pip` that resolves and installs
> dependencies \~10× faster. You may still `pip install -r requirements.txt`
> if you prefer.

---

## 🚴‍♂️Local workflow

### 1.Fast dev server

```bash
# live‑reload server on http://localhost:8001/
pelican --listen --autoreload -p 8001 \
        --settings pelicanconf.py
```

This uses **relative URLs** so everything renders correctly on localhost.

### 2.Production build preview

```bash
pelican content \
       --settings publishconf.py \
       --output output
python -m http.server --directory output 8002
# open http://localhost:8002/website/  ← note the /website/ path
```

`publishconf.py` writes **absolute URLs** rooted at
`https://pydataromacapitale.github.io/website`, so when you preview the
prod build locally you need the extra sub‑folder in the URL.

---

## 🔌Meetup event auto‑sync

On every build the `meetup_events` plug‑in:

1. Fetches the public iCal feed of
   `https://www.meetup.com/pydata-roma-capitale/`
2. Creates/updates one Markdown file per **future** event under
   `content/events/`, containing only:

   * Title
   * Datetime (UTC) in front‑matter
   * One‑line “RSVP on Meetup” link
3. Deletes stubs for past events.

This keeps the homepage “Upcoming events” card in sync with the actual
Meetup schedule with zero manual work.

---

## 🚢CI· GitHub Pages deploy

The workflow <kbd>.github/workflows/deploy.yaml</kbd> does the heavylifting:

```yaml
on: [push, workflow_dispatch]
permissions:
  contents: write  # allow push to gh‑pages

jobs:
  build:
    runs-on: ubuntu-latest
    defaults:
      run:
        shell: bash
        working-directory: pydata_roma_website  # <- this folder houses pelicanconf.py
    steps:
      - uses: actions/checkout@v4

      - name: Install uv & deps
        run: |
          pip install uv
          uv sync

      - name: Build site
        run: |
          uv run pelican content \
                 --settings publishconf.py \
                 --output   output

      - name: Deploy
        uses: peaceiris/actions-gh-pages@v4
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_branch: gh-pages
          publish_dir: pydata_roma_website/output
          enable_jekyll: false  # drop .nojekyll
```

The first run creates the `gh-pages` branch; GitHub Pages is then
configured (Settings → Pages) to serve from that branch at the repo
root. Links work because `publishconf.py`’s `SITEURL` already matches the
final address.

---

## 🤝Contributing

* **Fix a typo?** Open a quick PR.
* **Hack on the theme?** Tweak the SCSS/JS in
  `themes/roma/static/`— we ❤️ improvements.

All contributions must respect the
[PyData Code of Conduct](https://pydataconf.global/coc).

---

## 📝License

Code, themes and docs are released under the MIT License (see
`LICENSE`).  Images may have separate licences; check individual files
before reuse.

---

©2025 PyDataRomaCapitale

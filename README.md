# PyData Roma Capitale Website

Welcome! This repository hosts the source for **[PyData Roma Capitale](https://pydata-roma.github.io)** — the official website of the Rome PyData chapter built with [Pelican](https://getpelican.com/).

---

## 📂 What’s inside?

| Folder         | Purpose                                                  |
| -------------- | -------------------------------------------------------- |
| `content/`     | Markdown/ReST pages & auto-generated event posts         |
| `output/`      | **Built site** — static HTML/CSS/JS ready for deployment |
| `plugins/`     | Custom Pelican plug-ins (e.g. Meetup event sync)         |
| `themes/roma/` | Bootstrap-based Pelican theme                            |
| `tasks.py`     | *(Optional)* Invoke helpers wrapping Pelican commands    |

---

## 🛠 Prerequisites

* **Python ≥ 3.10** (manage with `pyenv`, virtualenv, etc.)
* **[uv](https://github.com/astral-sh/uv)** — blazingly-fast package manager (a drop-in replacement for `pip`)

```bash
uv sync
```

You can still fall back to `pip install -r requirements.txt`, but the team standard is **uv** for its speed and deterministic resolver.

---

## 🚀 Local development with Pelican CLI

```bash
# one-off build (draft mode)
pelican content \
       --output output \
       --settings pelicanconf.py

# serve & live-reload on http://localhost:8001
pelican --listen --autoreload -p 8001 \
        --settings pelicanconf.py
```

### Production build

```bash
pelican content \
       --output output \
       --settings publishconf.py
```


## 🔌 Automatic Meetup event syncing

The `meetup_events` plug-in fetches upcoming public events from the group’s iCal feed and writes minimal Markdown stubs in `content/events/` containing only:

* **Title**
* **Event date/time** (UTC) in the front-matter
* A single *RSVP on Meetup* link

Stubs for past events are deleted on every run, so the homepage always lists only future meet-ups.

Configuration (see `pelicanconf.py`):

```python
MEETUP_GROUP = "pydata-roma-capitale"
PLUGINS = ["meetup_events"]
```

---

## 🖌️ The *Roma* theme

A minimalist Bootstrap 5.3 theme with colours inspired by Rome — terracotta orange, Tiber-blue accents, and warm beige backgrounds. Tweak CSS variables in `static/css/style.css` or extend the Jinja2 templates in `templates/`.

---

## 🚢 Deploying to GitHub Pages

1. **Production build**

   ```bash
   pelican content --settings publishconf.py --output output
   ```
2. Commit (or copy) the contents of `output/` to the `gh-pages` branch **or** let a GitHub Action run the command above and push the artefacts for you.
3. In *Repository Settings → Pages* select `gh-pages` as the source (root).

`publishconf.py` already contains:

```python
SITEURL = "https://pydata-roma.github.io"
RELATIVE_URLS = False
```

so generated links are absolute in production.

---

## 🤝 Contributing

Pull requests are welcome! If you spot a typo, want to add your talk, or improve the theme, fork the project and open a PR.

Please respect the [PyData Code of Conduct](https://pydataconf.global/coc).

---

## 📝 License

Source code and theme are released under the [MIT License](LICENSE). Some images may carry different licences — check each file header before reuse.

---

© 2025 PyData Roma Capitale

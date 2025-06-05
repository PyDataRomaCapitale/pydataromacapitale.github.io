# PyData Roma Capitale – Pelican site starter

## Quick start

```bash
python -m venv .venv && source .venv/bin/activate
pip install pelican markdown typogrify

pelican --listen --autoreload
# open http://localhost:8000
```

* Edit Markdown in `content/`  
* Theme files live in `themes/roma/`  
* Deploy by pushing `output/` to GitHub Pages **or** add a workflow that runs `pelican content` on push.
# website

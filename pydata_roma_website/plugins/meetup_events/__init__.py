"""
Sync upcoming public Meetup events to Markdown in content/events/,
but keep only the title and an RSVP link.

Needs:  pip install requests ics pytz
"""
from __future__ import annotations
import os, re, datetime as dt, tempfile, shutil
import logging
import requests, pytz
from ics import Calendar, Event
from pelican import signals

MEETUP_GROUP   = "pydata-roma-capitale"          # overridden from pelicanconf.py
EVENT_DIR      = "content/events"
ICS_URL        = "https://www.meetup.com/{group}/events/ical"
LINK_TPL       = "https://www.meetup.com/{group}/events/{event_id}"

FRONTMATTER = """Title: {title}
Date: {date:%Y-%m-%d %H:%M}
Tags: event
Category: misc
Slug: meetup-{slug}

"""

slug_pat = re.compile(r"[^\w\-]+")

def slugify(text: str) -> str:
    return slug_pat.sub("-", text.lower()).strip("-")

def fetch_events(group: str) -> dict[str, Event]:
    """Return upcoming events for the given Meetup group.

    In case the remote request fails (e.g. due to lack of network
    connectivity), an empty dictionary is returned and the error is
    logged instead of raising an exception.  This keeps the site build
    from aborting when the feed is temporarily unreachable.
    """

    url = ICS_URL.format(group=group)
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as exc:
        logging.warning("Could not fetch Meetup events: %s", exc)
        return {}

    cal = Calendar(resp.text)
    now = dt.datetime.now(pytz.UTC)
    return {ev.uid: ev for ev in cal.events if ev.begin > now}

def write_md(ev: Event, path: str, group: str):
    slug = slugify(ev.uid)
    meetup_id = ev.uid.split("@")[0].replace('event_', '')  # part before "@meetup.com"
    link  = LINK_TPL.format(group=group, event_id=meetup_id)

    body = (
        FRONTMATTER.format(
            title=ev.name,
            date=ev.begin.datetime.replace(tzinfo=None),
            slug=slug,
        )
        + f"[RSVP on Meetup]({link})\n"
    )

    tmp = tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8")
    tmp.write(body)
    tmp.close()
    shutil.move(tmp.name, path)

def sync(pelican):
    group = pelican.settings.get("MEETUP_GROUP", MEETUP_GROUP)
    os.makedirs(EVENT_DIR, exist_ok=True)

    live = fetch_events(group)
    wanted = set()

    # create / refresh
    for uid, ev in live.items():
        slug = slugify(uid)
        fn   = f"meetup-{slug}.md"
        path = os.path.join(EVENT_DIR, fn)
        wanted.add(fn)

        write_md(ev, path, group)

    # remove obsolete files
    for fn in os.listdir(EVENT_DIR):
        if fn.startswith("meetup-") and fn.endswith(".md") and fn not in wanted:
            os.remove(os.path.join(EVENT_DIR, fn))

def register():
    signals.initialized.connect(sync)

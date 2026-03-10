"""
Sync upcoming public Meetup events to Markdown in content/events/,
but keep only the title and an RSVP link.

Needs:  pip install requests ics
"""

from __future__ import annotations
import logging
import datetime as dt
import os
import re
import shutil
import tempfile

import requests
from ics import Calendar, Event
from pelican import signals

MEETUP_GROUP = "pydata-roma-capitale"  # overridden from pelicanconf.py
ICS_URL = "https://www.meetup.com/{group}/events/ical"
LINK_TPL = "https://www.meetup.com/{group}/events/{event_id}"

slug_pat = re.compile(r"[^\w\-]+")
event_id_pat = re.compile(r"(\d+)")


def slugify(text: str) -> str:
    return slug_pat.sub("-", text.lower()).strip("-")


def clean_text(value: str | None) -> str:
    if not value:
        return ""

    return " ".join(value.replace("\r", " ").replace("\n", " ").split())


def event_identity(ev: Event) -> tuple[str, dt.datetime]:
    begin = ev.begin.datetime.astimezone(dt.timezone.utc).replace(second=0, microsecond=0)
    return (ev.name.strip().casefold(), begin)


def event_priority(ev: Event) -> tuple[int, str]:
    match = event_id_pat.search(ev.uid)
    event_id = int(match.group(1)) if match else -1
    return (event_id, ev.uid)


def fetch_events(group: str) -> dict[str, Event] | None:
    """Return upcoming events for the given Meetup group.

    In case the remote request fails (e.g. due to lack of network
    connectivity), ``None`` is returned and the error is logged instead
    of raising an exception. This keeps the site build from aborting
    and avoids deleting already-synced events when the feed is
    temporarily unreachable.
    """

    url = ICS_URL.format(group=group)
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as exc:
        logging.warning("Could not fetch Meetup events: %s", exc)
        return None

    cal = Calendar(resp.text)
    now = dt.datetime.now(dt.timezone.utc)
    deduped: dict[tuple[str, dt.datetime], Event] = {}

    for ev in cal.events:
        if ev.begin <= now:
            continue

        key = event_identity(ev)
        current = deduped.get(key)

        if current is None or event_priority(ev) > event_priority(current):
            deduped[key] = ev

    duplicate_count = len([ev for ev in cal.events if ev.begin > now]) - len(deduped)
    if duplicate_count > 0:
        logging.info("Deduplicated %s duplicate Meetup event(s)", duplicate_count)

    return {ev.uid: ev for ev in deduped.values()}


def write_md(ev: Event, path: str, group: str):
    slug = slugify(ev.uid)
    meetup_id = ev.uid.split("@")[0].replace("event_", "")  # part before "@meetup.com"
    link = LINK_TPL.format(group=group, event_id=meetup_id)
    location = clean_text(getattr(ev, "location", None))
    summary = "Join the PyData Roma Capitale community for this upcoming meetup in Rome."

    if location:
        summary = f"Join the PyData Roma Capitale community for an upcoming meetup at {location}."

    frontmatter_lines = [
        f"Title: {clean_text(ev.name)}",
        f"Date: {ev.begin.datetime.replace(tzinfo=None):%Y-%m-%d %H:%M}",
        "Tags: event",
        "Category: misc",
        f"Slug: meetup-{slug}",
        f"Summary: {summary}",
        f"Event_Link: {link}",
    ]

    if location:
        frontmatter_lines.append(f"Location: {location}")

    body_sections = []

    if location:
        body_sections.append(f"Venue: **{location}**.")

    body_sections.append(
        "Check the Meetup listing for the latest agenda, attendance updates, and any last-minute access notes."
    )

    body = (
        "\n".join(frontmatter_lines)
        + "\n\n"
        + "\n\n".join(body_sections)
        + "\n"
    )

    tmp = tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8")
    tmp.write(body)
    tmp.close()
    shutil.move(tmp.name, path)


def sync(pelican):
    group = pelican.settings.get("MEETUP_GROUP", MEETUP_GROUP)
    event_dir = os.path.join(pelican.settings["PATH"], "events")
    os.makedirs(event_dir, exist_ok=True)

    live = fetch_events(group)
    if live is None:
        return

    wanted = set()

    # create / refresh
    for uid, ev in live.items():
        slug = slugify(uid)
        fn = f"meetup-{slug}.md"
        path = os.path.join(event_dir, fn)
        wanted.add(fn)

        write_md(ev, path, group)

    # remove obsolete files
    for fn in os.listdir(event_dir):
        if fn.startswith("meetup-") and fn.endswith(".md") and fn not in wanted:
            os.remove(os.path.join(event_dir, fn))


def register():
    signals.initialized.connect(sync)

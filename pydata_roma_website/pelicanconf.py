# Pelican configuration for PyData Roma Capitale
import datetime

AUTHOR = "PyData Roma Capitale"
SITENAME = "PyData Roma Capitale"
SITESUBTITLE = "Python • Data • Community"
SITEURL = "http://localhost:8000"
RELATIVE_URLS = True

PATH = "content"
TIMEZONE = "Europe/Rome"
DEFAULT_LANG = "en"
THEME = "themes/roma"

MENUITEMS = [
    ("About", "/#about"),
    ("Events", "/#event"),
    ("Code of Conduct", "https://pydata.org/code-of-conduct/"),
]

BOARD_MEMBERS = [
    {
        "name": "Egon",
        "photo": f"{SITEURL}/images/people/Egon.jpg",
        "linkedin": "#",
        "role": "Board Member",
        "tagline": "Update description",
    },
    {
        "name": "Vincenzo",
        "photo": f"{SITEURL}/images/people/Vincenzo.jpg",
        "linkedin": "https://www.linkedin.com/in/vincenzoventriglia/",
        "role": "Organizer",
        "tagline": "ML Engineer & Data Scientist @ INGV",
    },
    {
        "name": "Carmela",
        "photo": f"{SITEURL}/images/people/Carmela.jpg",
        "linkedin": "#",
        "role": "Board Member",
        "tagline": "Update description",
    },
    {
        "name": "Francesco",
        "photo": f"{SITEURL}/images/people/Francesco.jpg",
        "linkedin": "#",
        "role": "Board Member",
        "tagline": "Update description",
    },
    {
        "name": "Carlo",
        "photo": f"{SITEURL}/images/people/Carlo.jpg",
        "linkedin": "#",
        "role": "Board Member",
        "tagline": "Update description",
    },
    {
        "name": "Marco",
        "photo": f"{SITEURL}/images/people/Marco.jpg",
        "linkedin": "#",
        "role": "Board Member",
        "tagline": "Update description",
    },
    {
        "name": "Vanessa",
        "photo": f"{SITEURL}/images/people/Vanessa.jpg",
        "linkedin": "#",
        "role": "Board Member",
        "tagline": "Update description",
    },
]

PLUGIN_PATHS = ["plugins"]
PLUGINS = ["meetup_events"]
MEETUP_GROUP = "pydata-roma-capitale"

SOCIAL = [
    ("Telegram", "https://t.me/pydataroma"),
    ("LinkedIn", "https://www.linkedin.com/company/pydata-roma"),
    ("Meetup", "https://www.meetup.com/pydata-roma-capitale"),
    ("GitHub", "https://github.com/PyDataRomaCapitale"),
]

JINJA_GLOBALS = {
    "now": datetime.datetime.utcnow,
}

MEETUP_LINK = "https://www.meetup.com/pydata-roma-capitale"
CFP_LINK = "https://forms.gle/nrXLNhDJcdCyvkrY8"
GOOGLE_ANALYTICS = ""

# mark folders to copy as-is
STATIC_PATHS = ["images", "extra/favicon/favicon.ico"]

# where to place extra files
EXTRA_PATH_METADATA = {
    "extra/favicon/favicon.ico": {"path": "favicon.ico"}
}

DEFAULT_PAGINATION = False

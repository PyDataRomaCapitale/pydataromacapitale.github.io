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
        "name": "Egon Ferri",
        "photo": "https://media.licdn.com/dms/image/v2/D4D03AQFsaWSiEKPu6w/profile-displayphoto-shrink_800_800/B4DZdLGfZoH4Ag-/0/1749311683005?e=1755129600&v=beta&t=UtH8tmsltsf-vpSTAm49JbCho1fmUFxS7bBSMuQF3zI",
        "linkedin": "https://www.linkedin.com/in/egon-ferri/",
        "role": "Organizer",
        "tagline": "CV Engineer @ Immobiliare.it",
    },
    {
        "name": "Carmela Salandria",
        "photo": "https://media.licdn.com/dms/image/v2/D4E03AQEiqgoMnc6EGA/profile-displayphoto-shrink_800_800/profile-displayphoto-shrink_800_800/0/1669741594156?e=1752710400&v=beta&t=8OLrev9-axaKDFdyFKkeFWqdfSrKP-bxyXAObxD6x_c",
        "linkedin": "https://www.linkedin.com/in/carmela-salandr%C3%ACa-843162178/",
        "role": "Organizer",
        "tagline": "Data Engineer @ ELIS Innovation Hub ",
    },
    {
        "name": "Vincenzo Ventriglia",
        "photo": "https://media.licdn.com/dms/image/v2/D4D03AQG7zQIGoOAtNg/profile-displayphoto-shrink_400_400/profile-displayphoto-shrink_400_400/0/1689435365433?e=1752710400&v=beta&t=fgVFRkk8lN3a7jJpikA-eooKhvQFgOqZJWrh7lkrpsE",
        "linkedin": "https://www.linkedin.com/in/vincenzoventriglia/",
        "role": "Organizer",
        "tagline": "ML Engineer & Data Scientist @ INGV",
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

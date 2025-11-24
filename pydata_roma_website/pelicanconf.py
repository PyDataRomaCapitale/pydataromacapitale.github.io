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
        "photo": "images/people/Egon.jpg",
        "linkedin": "https://www.linkedin.com/in/egon-ferri/",
        "role": "Organizer",
        "tagline": "CV Engineer @ Immobiliare.it",
    },
    {
        "name": "Vincenzo Ventriglia",
        "photo": "images/people/Vincenzo.jpg",
        "linkedin": "https://www.linkedin.com/in/vincenzoventriglia/",
        "role": "Organizer",
        "tagline": "ML Engineer & Data Scientist @ INGV",
    },
    {
        "name": "Carmela Salandria",
        "photo": "images/people/Carmela.jpg",
        "linkedin": "https://www.linkedin.com/in/carmela-salandr%C3%ACa-843162178/",
        "role": "Organizer",
        "tagline": "Data Engineer @ ELIS Innovation Hub ",
    },
    {
        "name": "Francesco Conti",
        "photo": "images/people/Francesco.jpg",
        "linkedin": "https://www.linkedin.com/in/francesco-conti-32913b135/",
        "role": "Organizer",
        "tagline": "Data Scientist @ Agile lab",
    },
    {
        "name": "Carlo A. Venditti",
        "photo": "images/people/Carlo.jpg",
        "linkedin": "#",
        "role": "Organizer",
        "tagline": "Freelance Software Engineer",
    },
    {
        "name": "Marco",
        "photo": "images/people/Marco.jpg",
        "linkedin": "https://www.linkedin.com/in/marcosciacovelli/",
        "role": "Organizer",
        "tagline": "Data Platform Specialist @Verisure",
    },
    {
        "name": "Vanessa Iannozzi",
        "photo": "images/people/Vanessa.jpg",
        "linkedin": "#",
        "role": "Organizer",
        "tagline": "Data Scientist presso ELIS Innovation Hub",
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
EXTRA_PATH_METADATA = {"extra/favicon/favicon.ico": {"path": "favicon.ico"}}

DEFAULT_PAGINATION = False

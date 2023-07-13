AUTHOR = 'Hephzibah Pon Cellat Arulprakash'
SITENAME = 'poncellat\'s Blog'
SITESUBTITLE = 'coping data from brain to disk :relieved:'
SITEURL = 'https://poncellat.github.io'

GITHUB_URL = 'https://github.com/poncellat/'

FEED_ALL_RSS = 'feeds/all.rss.xml'
CATEGORY_FEED_RSS = 'feeds/{slug}.rss.xml'

TIMEZONE = 'Asia/Dubai'

SOCIAL = (('linkedin', 'https://linkedin.com/in/hephzibahponcellat'),
          ('github', 'https://github.com/poncellat'),)

STATIC_PATHS = [
    'images',
    ]

READERS = {'html': None}
PYGMENTS_RST_OPTIONS = {'linenos': 'table'}

NEWEST_FIRST_ARCHIVES = True
ARTICLE_EXCLUDES = ['drafts']
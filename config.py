"""
Configuration for Pegasus Info - News Intelligence System
"""

# RSS Feed Sources (Free/Open)
RSS_SOURCES = {
    'health': [
        'https://www.who.int/rss-feeds/news-english.xml',
        'https://www.cdc.gov/api/v2/resources/rss/742226',
        'http://feeds.feedburner.com/healthcentral/News',
    ],
    'military': [
        'https://feeds.feedburner.com/WarNewsUpdates',
        'http://feeds.feedburner.com/DefenseNews',
    ],
    'economy': [
        'https://feeds.finance.yahoo.com/rss/2.0/headline',
        'http://feeds.reuters.com/news/wealth',
    ],
    'general': [
        'http://feeds.bbci.co.uk/news/rss.xml',
        'https://feeds.npr.org/1001/rss.xml',
        'http://feeds.reuters.com/reuters/topNews',
    ]
}

# Keywords for classification
HEALTH_KEYWORDS = [
    'who', 'outbreak', 'virus', 'vaccine', 'hospital', 'disease', 'epidemic',
    'pandemic', 'health', 'medical', 'doctor', 'patient', 'symptom', 'treatment',
    'drug', 'medicine', 'covid', 'flu', 'infection', 'contagious', 'quarantine',
    'cdc', 'fda', 'clinic', 'emergency', 'public health', 'mortality', 'morbidity'
]

MILITARY_KEYWORDS = [
    'missile', 'army', 'drone', 'navy', 'defense', 'military', 'conflict', 'war',
    'weapon', 'tank', 'soldier', 'troops', 'air force', 'marine', 'combat',
    'attack', 'invasion', 'exercise', 'alutsista', 'geopolitik', 'securit',
    'conflict', 'battle', 'strike', 'bombing', 'artillery', 'helicopter', 'jet',
    'submarine', 'aircraft carrier', 'peacekeeping', 'ceasefire', 'treaty'
]

ECONOMY_KEYWORDS = [
    'inflation', 'bitcoin', 'bank', 'dollar', 'market', 'stock', 'crypto', 'currency',
    'economy', 'economic', 'finance', 'financial', 'investment', 'trading', 'exchange',
    'rate', 'interest rate', 'central bank', 'recession', 'growth', 'gdp', 'fund',
    'price', 'cost', 'tax', 'budget', 'debt', 'credit', 'loan', 'saham', 'pasar',
    'keuangan', 'bank sentral', 'rupiah', 'ekonomi', 'investasi', 'uang'
]

# Sensitive topic alerts
SENSITIVE_TOPICS = {
    'health': ['outbreak', 'epidemic', 'pandemic', 'new virus', 'contagious'],
    'military': ['nuclear', 'war declaration', 'invasion', 'attack', 'conflict escalation'],
    'economy': ['crisis', 'collapse', 'recession', 'crash', 'bankruptcy', 'default']
}

# Trending detection thresholds
TRENDING_THRESHOLD = 3  # Minimum occurrences to consider trending
TIME_WINDOW_HOURS = 24  # Time window for trending detection

# Summary settings
SUMMARY_MAX_LENGTH = 500  # Maximum characters for summary
SUMMARY_MIN_LENGTH = 150  # Minimum characters for summary

# Export settings
EXPORT_DIR = 'exports'
EXPORT_FORMATS = ['json', 'csv', 'markdown']

# Rate limiting
REQUEST_DELAY = 1  # Seconds between requests
MAX_RETRIES = 3
TIMEOUT = 30

# Logging
LOG_LEVEL = 'INFO'
LOG_FILE = 'pegasus_info.log'

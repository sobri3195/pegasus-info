# Pegasus Info - Complete Documentation

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Module Details](#module-details)
4. [API Reference](#api-reference)
5. [Configuration](#configuration)
6. [Examples](#examples)
7. [Troubleshooting](#troubleshooting)

---

## Overview

Pegasus Info is a comprehensive news intelligence system that:
- Scrapes news from free public RSS feeds
- Classifies articles into categories (Health, Military, Economy)
- Detects trending topics
- Analyzes context and impact
- Generates summaries and insights
- Exports to multiple formats (JSON, CSV, Markdown)

### Core Features

| Feature | Description |
|----------|-------------|
| **News Scraping** | Free RSS feeds from major news sources |
| **Classification** | Automatic categorization using keyword matching |
| **Trending Detection** | Identifies popular topics within time windows |
| **Context Analysis** | Assess impact level and sentiment |
| **Auto Summary** | Generates concise summaries |
| **Sensitive Alerts** | Flags topics requiring attention |
| **Export** | JSON, CSV, and Markdown formats |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Pegasus Info Core                      │
│                    (pegasus_info.py)                      │
└─────────────────────────────────────────────────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│   Scraper    │  │  Classifier  │  │  Trending    │
│  scraper.py  │  │classifier.py │  │ trending.py  │
└──────────────┘  └──────────────┘  └──────────────┘
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│  Analyzer    │  │  Summarizer  │  │   Exporter   │
│ analyzer.py  │  │summarizer.py │  │ exporter.py  │
└──────────────┘  └──────────────┘  └──────────────┘
```

---

## Module Details

### 1. Scraper (scraper.py)

**Purpose:** Fetches news articles from RSS feeds

**Key Classes:**
- `NewsScraper`: Main scraper class

**Key Methods:**
```python
# Fetch from single RSS feed
fetch_rss_feed(url, category='general') -> List[Dict]

# Fetch from all configured feeds
fetch_all_feeds() -> List[Dict]

# Filter by date
filter_by_date(articles, hours=24) -> List[Dict]

# Scrape full article content
scrape_article_content(url) -> Optional[str]
```

**Article Structure:**
```python
{
    'title': str,
    'link': str,
    'summary': str,
    'published_date': datetime,
    'category': str,
    'source': str,
    'content_length': int,
    'fetched_at': datetime
}
```

---

### 2. Classifier (classifier.py)

**Purpose:** Categorizes articles and detects sensitive topics

**Key Classes:**
- `NewsClassifier`: Classifies articles into categories

**Key Methods:**
```python
# Classify single article
classify_article(article) -> Dict

# Classify multiple articles
classify_articles(articles) -> List[Dict]

# Get category statistics
get_category_stats(articles) -> Dict
```

**Categories:**
- `health`: Health, diseases, vaccines, WHO, hospitals
- `military`: Conflicts, weapons, defense, army, navy
- `economy`: Inflation, banks, crypto, stocks, market
- `general`: Everything else

**Sensitive Topics:**
- Health: outbreaks, epidemics, pandemics
- Military: nuclear attacks, invasions
- Economy: crises, collapses, crashes

---

### 3. Trending (trending.py)

**Purpose:** Detects trending topics from articles

**Key Classes:**
- `TrendingDetector`: Identifies popular topics

**Key Methods:**
```python
# Detect trending topics
detect_trending(articles) -> Dict

# Extract keywords from text
extract_keywords(text, min_length=3) -> List[str]

# Extract phrases from text
extract_phrases(text, min_phrase_length=2) -> List[str]

# Get trending score for an article
get_article_trending_score(article, trending_data) -> float
```

**Trending Data Structure:**
```python
{
    'trending_keywords': [(keyword, count), ...],
    'trending_phrases': [(phrase, count), ...],
    'trending_by_category': {
        'category': [(keyword, count), ...]
    },
    'time_window_hours': int,
    'total_articles_analyzed': int,
    'threshold': int
}
```

---

### 4. Analyzer (analyzer.py)

**Purpose:** Analyzes articles for impact, sentiment, and entities

**Key Classes:**
- `NewsAnalyzer`: Analyzes article context

**Key Methods:**
```python
# Analyze single article
analyze_article(article) -> Dict

# Analyze multiple articles
analyze_articles(articles) -> List[Dict]

# Get analysis summary
get_analysis_summary(articles) -> Dict
```

**Analysis Fields:**
- `impact_level`: high, medium, low
- `sentiment`: positive, negative, neutral
- `entities`: {
    `locations`: List[str],
    `organizations`: List[str],
    `countries`: List[str]
}

---

### 5. Summarizer (summarizer.py)

**Purpose:** Generates summaries and insights

**Key Classes:**
- `NewsSummarizer`: Creates summaries and insights

**Key Methods:**
```python
# Generate summary
generate_summary(article) -> str

# Generate insight
generate_insight(article) -> str

# Generate summaries for multiple articles
summarize_articles(articles) -> List[Dict]

# Generate category summary
generate_category_summary(articles, category) -> str
```

**Insight Format:**
```
⚠️ SENSITIVE: This {category} news requires attention. {sentiment} information.
```

---

### 6. Exporter (exporter.py)

**Purpose:** Exports data to various formats

**Key Classes:**
- `NewsExporter`: Handles data export

**Key Methods:**
```python
# Export to JSON
export_json(articles, filename=None) -> str

# Export to CSV
export_csv(articles, filename=None) -> str

# Export to Markdown
export_markdown(articles, filename=None) -> str

# Export to all formats
export_all_formats(articles, filename=None) -> Dict[str, str]

# Export trending report
export_trending_report(trending_data, filename=None) -> str
```

**Export Directory:** `exports/` (auto-created)

---

## API Reference

### PegasusInfo Class

Main interface for the news intelligence system.

**Constructor:**
```python
pegasus = PegasusInfo()
```

**Methods:**

#### run_full_pipeline(hours=24, export=True)
Run the complete intelligence pipeline.

**Parameters:**
- `hours` (int): Number of hours to look back
- `export` (bool): Whether to export results

**Returns:**
```python
{
    'started_at': datetime,
    'completed_at': datetime,
    'status': str,  # 'success' or 'error'
    'articles': List[Dict],
    'trending': Dict,
    'analysis': Dict,
    'exports': Dict[str, str]
}
```

#### fetch_and_classify(hours=24)
Quick fetch and classify articles.

**Parameters:**
- `hours` (int): Number of hours to look back

**Returns:**
- List[Dict]: Classified articles

#### get_trending(hours=24)
Get trending topics.

**Parameters:**
- `hours` (int): Number of hours to look back

**Returns:**
- Dict: Trending data

---

## Configuration

### config.py

Edit `config.py` to customize behavior:

```python
# RSS Feed Sources
RSS_SOURCES = {
    'health': ['url1', 'url2'],
    'military': ['url1', 'url2'],
    'economy': ['url1', 'url2'],
    'general': ['url1', 'url2']
}

# Classification Keywords
HEALTH_KEYWORDS = ['who', 'outbreak', ...]
MILITARY_KEYWORDS = ['missile', 'army', ...]
ECONOMY_KEYWORDS = ['inflation', 'bank', ...]

# Sensitive Topics
SENSITIVE_TOPICS = {
    'health': ['outbreak', 'epidemic'],
    'military': ['nuclear', 'war declaration'],
    'economy': ['crisis', 'collapse']
}

# Trending Detection
TRENDING_THRESHOLD = 3  # Minimum mentions
TIME_WINDOW_HOURS = 24  # Time window

# Export Settings
EXPORT_DIR = 'exports'
EXPORT_FORMATS = ['json', 'csv', 'markdown']
```

### Environment Variables

Create `.env` file from `.env.example`:

```bash
LOG_LEVEL=INFO
LOG_FILE=pegasus_info.log

REQUEST_DELAY=1
MAX_RETRIES=3
TIMEOUT=30

TRENDING_THRESHOLD=3
TIME_WINDOW_HOURS=24

SUMMARY_MAX_LENGTH=500
SUMMARY_MIN_LENGTH=150
```

---

## Examples

### Example 1: Basic Usage

```python
from pegasus_info import PegasusInfo

# Initialize
pegasus = PegasusInfo()

# Run full pipeline
results = pegasus.run_full_pipeline(hours=24, export=True)

# Access results
articles = results['articles']
trending = results['trending']
```

### Example 2: Custom Classification

```python
from classifier import NewsClassifier

classifier = NewsClassifier()

# Classify custom article
article = {
    'title': 'New vaccine approved',
    'summary': 'FDA approves new COVID-19 vaccine',
    'category': 'general'
}

classified = classifier.classify_article(article)
print(f"Category: {classified['primary_category']}")
print(f"Sensitive: {classified['is_sensitive']}")
```

### Example 3: Trending Analysis

```python
from trending import TrendingDetector

detector = TrendingDetector()

# Get trending topics
trending = detector.detect_trending(articles)

# Display top keywords
for keyword, count in trending['trending_keywords'][:5]:
    print(f"{keyword}: {count} mentions")
```

### Example 4: Custom Analysis

```python
from analyzer import NewsAnalyzer

analyzer = NewsAnalyzer()

# Analyze article
analyzed = analyzer.analyze_article(article)

# Check impact
if analyzed['impact_level'] == 'high':
    print("High impact article!")

# Check sentiment
print(f"Sentiment: {analyzed['sentiment']}")

# Check entities
print(f"Organizations: {analyzed['entities']['organizations']}")
```

### Example 5: Export to Custom Format

```python
from exporter import NewsExporter

exporter = NewsExporter()

# Export specific format
json_path = exporter.export_json(articles, 'my_news')
csv_path = exporter.export_csv(articles, 'my_news')
md_path = exporter.export_markdown(articles, 'my_news')

print(f"Exported to: {json_path}, {csv_path}, {md_path}")
```

---

## Troubleshooting

### Common Issues

#### 1. No articles fetched

**Problem:** Zero articles from RSS feeds

**Solution:**
- Check internet connection
- Verify RSS feed URLs in `config.py`
- Increase timeout in `config.py`
- Check logs for specific errors

#### 2. Classification errors

**Problem:** Articles not classified correctly

**Solution:**
- Add more keywords to categories in `config.py`
- Check article summaries for proper text content
- Adjust `TRENDING_THRESHOLD`

#### 3. Memory issues with large datasets

**Problem:** Out of memory errors

**Solution:**
- Process articles in batches
- Reduce time window (fewer hours)
- Filter articles before processing

#### 4. Export failures

**Problem:** Export errors

**Solution:**
- Check `exports/` directory permissions
- Ensure disk space available
- Check file paths are valid

#### 5. Slow performance

**Problem:** Processing takes too long

**Solution:**
- Increase `REQUEST_DELAY` to avoid rate limiting
- Reduce number of RSS feeds
- Filter articles by date before processing

### Debug Mode

Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Or modify `config.py`:

```python
LOG_LEVEL = 'DEBUG'
```

---

## Performance Tips

1. **Reduce API calls**: Filter articles early
2. **Use caching**: Store results for reuse
3. **Batch processing**: Process articles in groups
4. **Selective scraping**: Only fetch needed feeds
5. **Optimize time windows**: Smaller windows = faster processing

---

## Best Practices

1. **Always check article dates**: Filter by date before processing
2. **Handle exceptions**: Use try-except for network calls
3. **Monitor rate limits**: Respect RSS feed policies
4. **Validate data**: Check article structure before use
5. **Regular updates**: Keep RSS feed URLs current

---

## License

Free for educational and research use.

---

## Support

For issues and questions:
- Check logs in `pegasus_info.log`
- Review this documentation
- Examine example code in `example.py`

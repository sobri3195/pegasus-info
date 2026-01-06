# Quick Start Guide - Pegasus Info

Get started with Pegasus Info in 5 minutes!

---

## Installation

### 1. Install Dependencies

```bash
pip3 install --break-system-packages -r requirements.txt
```

Or use the setup script:

```bash
chmod +x setup.sh
./setup.sh
```

### 2. Run Tests

Verify installation:

```bash
python3 test_basic.py
```

Expected output:
```
✅ ALL TESTS PASSED
```

---

## Basic Usage

### Run Full Pipeline

```bash
python3 pegasus_info.py
```

This will:
1. Fetch news from RSS feeds (last 24 hours)
2. Classify articles
3. Detect trending topics
4. Analyze impact and sentiment
5. Generate summaries
6. Export results to JSON, CSV, and Markdown

### Command Line Options

```bash
# Last 12 hours instead of 24
python3 pegasus_info.py --hours 12

# Don't export files
python3 pegasus_info.py --no-export

# View all options
python3 pegasus_info.py --help
```

---

## Python API Usage

### Example 1: Quick Start

```python
from pegasus_info import PegasusInfo

# Initialize
pegasus = PegasusInfo()

# Run pipeline
results = pegasus.run_full_pipeline(hours=24, export=True)

# Check results
print(f"Articles processed: {len(results['articles'])}")
print(f"Status: {results['status']}")
```

### Example 2: Fetch and Classify

```python
# Get classified articles
articles = pegasus.fetch_and_classify(hours=48)

# Show some articles
for article in articles[:5]:
    print(f"Title: {article['title']}")
    print(f"Category: {article['primary_category']}")
    print("-" * 60)
```

### Example 3: Get Trending Topics

```python
# Get trending
trending = pegasus.get_trending(hours=24)

# Display top topics
for keyword, count in trending['trending_keywords'][:5]:
    print(f"{keyword}: {count} mentions")
```

### Example 4: Filter by Category

```python
# Get all articles
articles = pegasus.fetch_and_classify(hours=24)

# Filter health news
health_news = [
    a for a in articles
    if a['primary_category'] == 'health'
]

print(f"Health articles: {len(health_news)}")
```

### Example 5: Find Sensitive Topics

```python
# Get articles
articles = pegasus.fetch_and_classify(hours=24)

# Find sensitive
sensitive = [
    a for a in articles
    if a.get('is_sensitive', False)
]

# Display alerts
for article in sensitive:
    print(f"⚠️ SENSITIVE: {article['title']}")
    print(f"   Topics: {', '.join(article['sensitive_topics'])}")
    print(f"   Impact: {article['impact_level']}")
    print()
```

---

## Understanding the Output

### Article Fields

Each article contains:

| Field | Description |
|-------|-------------|
| `title` | Headline |
| `link` | URL |
| `summary` | Brief summary |
| `published_date` | Publication time |
| `source` | News source |
| `primary_category` | Main category |
| `impact_level` | high/medium/low |
| `sentiment` | positive/negative/neutral |
| `is_sensitive` | If needs attention |
| `insight` | Quick analysis |

### Categories

- **Health**: Diseases, vaccines, WHO, hospitals
- **Military**: Conflicts, weapons, defense
- **Economy**: Inflation, banks, crypto, stocks
- **General**: Everything else

### Impact Levels

- **High**: Requires immediate attention
- **Medium**: Important but not urgent
- **Low**: Routine information

### Export Files

All exports go to `exports/` folder:

```
exports/
├── news_20240115_103000.json  # Full data
├── news_20240115_103000.csv   # Spreadsheet format
├── news_20240115_103000.md    # Readable report
└── trending_20240115_103000.md # Trending report
```

---

## Common Use Cases

### Monitor Health News

```python
pegasus = PegasusInfo()
articles = pegasus.fetch_and_classify(hours=24)

health_news = [
    a for a in articles
    if a['primary_category'] == 'health'
]

# Find high impact
critical = [
    a for a in health_news
    if a['impact_level'] == 'high'
]

print(f"Critical health news: {len(critical)}")
for article in critical:
    print(f"  - {article['title']}")
```

### Track Economic Indicators

```python
articles = pegasus.fetch_and_classify(hours=24)

economy_news = [
    a for a in articles
    if a['primary_category'] == 'economy'
]

# Check sentiment
sentiments = [a['sentiment'] for a in economy_news]
negative_count = sum(1 for s in sentiments if s == 'negative')

if negative_count > len(economy_news) * 0.5:
    print("⚠️ Negative sentiment dominates economy news")
```

### Detect Emerging Conflicts

```python
articles = pegasus.fetch_and_classify(hours=12)

military_news = [
    a for a in articles
    if a['primary_category'] == 'military'
]

# Find sensitive topics
conflicts = [
    a for a in military_news
    if a.get('is_sensitive', False)
    and 'conflict' in a.get('sensitive_topics', [])
]

if conflicts:
    print("🚨 Emerging conflicts detected:")
    for article in conflicts:
        print(f"  - {article['title']}")
```

### Daily News Summary

```python
pegasus = PegasusInfo()

# Run pipeline with export
results = pegasus.run_full_pipeline(hours=24, export=True)

# Print summary
analysis = results['analysis']
print(f"\n📰 Daily Summary")
print(f"Total Articles: {len(results['articles'])}")
print(f"High Impact: {analysis['high_impact_count']}")
print(f"Negative Sentiment: {analysis['negative_sentiment_count']}")

# Show top trending
trending = results['trending']
print(f"\n🔥 Top Topics:")
for keyword, count in trending['trending_keywords'][:3]:
    print(f"  {keyword}: {count} mentions")
```

---

## Next Steps

1. **Customize Feeds**: Edit `config.py` to add RSS sources
2. **Adjust Thresholds**: Modify `TRENDING_THRESHOLD` for sensitivity
3. **Schedule Runs**: Use cron to run automatically
4. **Monitor Alerts**: Set up notifications for sensitive topics
5. **Explore Data**: Use pandas for advanced analysis

---

## Troubleshooting

### Issue: No articles fetched

**Check:**
```bash
# Test internet connection
ping -c 3 google.com

# Test specific feed
curl -I https://www.who.int/rss-feeds/news-english.xml
```

### Issue: Import errors

**Solution:**
```bash
# Reinstall dependencies
pip3 install --break-system-packages -r requirements.txt --force-reinstall
```

### Issue: Slow performance

**Solution:**
```python
# Reduce time window
results = pegasus.run_full_pipeline(hours=6)  # Instead of 24
```

---

## Getting Help

1. Read full documentation: `DOCUMENTATION.md`
2. Check examples: `example.py`
3. Review configuration: `config.py`
4. Check logs: `pegasus_info.log`

---

## Tips

1. **Start small**: Use 6-12 hour windows for testing
2. **Monitor logs**: Check `pegasus_info.log` for issues
3. **Export regularly**: Keep archives for trend analysis
4. **Customize keywords**: Add domain-specific terms to `config.py`
5. **Use examples**: See `example.py` for more patterns

---

**Ready to go!** 🚀

Run `python3 pegasus_info.py` to get started.

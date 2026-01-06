"""
News Scraper Module - Fetches news from RSS feeds and public sources
"""

import feedparser
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import time
import logging
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from config import RSS_SOURCES, REQUEST_DELAY, MAX_RETRIES, TIMEOUT

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NewsScraper:
    """Scrapes news from various free sources"""

    def __init__(self):
        self.articles = []

    def fetch_rss_feed(self, url: str, category: str = 'general') -> List[Dict]:
        """
        Fetch articles from an RSS feed

        Args:
            url: RSS feed URL
            category: News category for classification

        Returns:
            List of articles
        """
        articles = []
        retries = 0

        while retries < MAX_RETRIES:
            try:
                logger.info(f"Fetching RSS feed: {url}")
                feed = feedparser.parse(url)

                if feed.bozo:
                    logger.warning(f"RSS feed parse warning for {url}")

                for entry in feed.entries:
                    article = self._parse_rss_entry(entry, category)
                    if article:
                        articles.append(article)

                logger.info(f"Fetched {len(articles)} articles from {url}")
                break

            except Exception as e:
                retries += 1
                logger.error(f"Error fetching RSS feed {url} (attempt {retries}): {str(e)}")
                if retries < MAX_RETRIES:
                    time.sleep(REQUEST_DELAY * retries)

        time.sleep(REQUEST_DELAY)
        return articles

    def _parse_rss_entry(self, entry, category: str) -> Optional[Dict]:
        """Parse a single RSS entry into an article dictionary"""
        try:
            published_date = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                published_date = datetime(*entry.published_parsed[:6])

            summary = ''
            if hasattr(entry, 'summary'):
                summary = BeautifulSoup(entry.summary, 'lxml').get_text(strip=True)
            elif hasattr(entry, 'description'):
                summary = BeautifulSoup(entry.description, 'lxml').get_text(strip=True)

            article = {
                'title': entry.get('title', ''),
                'link': entry.get('link', ''),
                'summary': summary,
                'published_date': published_date,
                'category': category,
                'source': entry.get('source', {}).get('title', self._extract_domain(entry.link)),
                'content_length': len(summary),
                'fetched_at': datetime.now()
            }

            return article

        except Exception as e:
            logger.error(f"Error parsing RSS entry: {str(e)}")
            return None

    def _extract_domain(self, url: str) -> str:
        """Extract domain name from URL"""
        try:
            from urllib.parse import urlparse
            parsed = urlparse(url)
            return parsed.netloc.replace('www.', '')
        except:
            return 'unknown'

    def fetch_all_feeds(self) -> List[Dict]:
        """
        Fetch articles from all configured RSS feeds

        Returns:
            List of all articles
        """
        all_articles = []

        for category, feeds in RSS_SOURCES.items():
            logger.info(f"Fetching {category} feeds...")
            for feed_url in feeds:
                articles = self.fetch_rss_feed(feed_url, category)
                all_articles.extend(articles)

        # Remove duplicates based on link
        unique_articles = self._remove_duplicates(all_articles)

        logger.info(f"Total unique articles fetched: {len(unique_articles)}")
        return unique_articles

    def _remove_duplicates(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles based on link"""
        seen_links = set()
        unique_articles = []

        for article in articles:
            if article['link'] not in seen_links:
                seen_links.add(article['link'])
                unique_articles.append(article)

        return unique_articles

    def filter_by_date(self, articles: List[Dict], hours: int = 24) -> List[Dict]:
        """
        Filter articles by publication date

        Args:
            articles: List of articles
            hours: Number of hours to look back

        Returns:
            Filtered list of recent articles
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)

        filtered = [
            article for article in articles
            if article['published_date'] and article['published_date'] >= cutoff_time
        ]

        logger.info(f"Articles from last {hours} hours: {len(filtered)}")
        return filtered

    def scrape_article_content(self, url: str) -> Optional[str]:
        """
        Scrape full article content from URL

        Args:
            url: Article URL

        Returns:
            Article content text
        """
        try:
            response = requests.get(url, timeout=TIMEOUT)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'lxml')

            # Remove unwanted elements
            for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
                element.decompose()

            # Extract text from paragraphs
            paragraphs = soup.find_all('p')
            content = ' '.join([p.get_text(strip=True) for p in paragraphs])

            return content[:2000]  # Limit content length

        except Exception as e:
            logger.error(f"Error scraping article content from {url}: {str(e)}")
            return None

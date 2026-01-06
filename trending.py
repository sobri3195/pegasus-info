"""
Trending Detection Module - Identifies trending topics
"""

from typing import List, Dict
from collections import Counter, defaultdict
import re
from datetime import datetime, timedelta
import logging

from config import TRENDING_THRESHOLD, TIME_WINDOW_HOURS

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TrendingDetector:
    """Detects trending topics from articles"""

    def __init__(self, threshold: int = TRENDING_THRESHOLD):
        self.threshold = threshold

    def extract_keywords(self, text: str, min_length: int = 3) -> List[str]:
        """
        Extract meaningful keywords from text

        Args:
            text: Text to extract keywords from
            min_length: Minimum keyword length

        Returns:
            List of keywords
        """
        # Remove special characters and split into words
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())

        # Filter out common stop words
        stop_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had',
            'her', 'was', 'one', 'our', 'out', 'with', 'this', 'that', 'have',
            'from', 'they', 'will', 'would', 'there', 'their', 'what', 'which',
            'when', 'make', 'like', 'into', 'year', 'your', 'just', 'over', 'also',
            'such', 'because', 'these', 'first', 'being', 'after', 'most', 'than',
            'said', 'has', 'been', 'were', 'was', 'its', 'his', 'her', 'she',
            'him', 'them', 'been', 'being', 'says', 'say', 'said', 'new', 'time'
        }

        keywords = [word for word in words if word not in stop_words and len(word) >= min_length]

        return keywords

    def extract_phrases(self, text: str, min_phrase_length: int = 2) -> List[str]:
        """
        Extract meaningful phrases (2-3 word combinations)

        Args:
            text: Text to extract phrases from
            min_phrase_length: Minimum phrase length in words

        Returns:
            List of phrases
        """
        words = self.extract_keywords(text)
        phrases = []

        if len(words) >= 2:
            # Extract 2-word phrases
            for i in range(len(words) - 1):
                phrase = f"{words[i]} {words[i+1]}"
                phrases.append(phrase)

        if len(words) >= 3:
            # Extract 3-word phrases
            for i in range(len(words) - 2):
                phrase = f"{words[i]} {words[i+1]} {words[i+2]}"
                phrases.append(phrase)

        return phrases

    def detect_trending(self, articles: List[Dict]) -> Dict[str, any]:
        """
        Detect trending topics from articles

        Args:
            articles: List of articles

        Returns:
            Dictionary with trending information
        """
        # Filter articles within time window
        cutoff_time = datetime.now() - timedelta(hours=TIME_WINDOW_HOURS)
        recent_articles = [
            a for a in articles
            if a.get('published_date') and a['published_date'] >= cutoff_time
        ]

        if not recent_articles:
            logger.info("No recent articles found for trending detection")
            return {
                'trending_topics': [],
                'trending_by_category': {},
                'time_window_hours': TIME_WINDOW_HOURS,
                'total_articles': 0
            }

        # Extract all keywords and phrases
        all_keywords = []
        all_phrases = []
        keywords_by_category = defaultdict(list)

        for article in recent_articles:
            text = f"{article.get('title', '')} {article.get('summary', '')}"

            keywords = self.extract_keywords(text)
            phrases = self.extract_phrases(text)

            all_keywords.extend(keywords)
            all_phrases.extend(phrases)

            category = article.get('primary_category', 'general')
            keywords_by_category[category].extend(keywords)

        # Count frequencies
        keyword_counts = Counter(all_keywords)
        phrase_counts = Counter(all_phrases)

        # Filter by threshold
        trending_keywords = [
            (keyword, count) for keyword, count in keyword_counts.items()
            if count >= self.threshold
        ]

        trending_phrases = [
            (phrase, count) for phrase, count in phrase_counts.items()
            if count >= self.threshold
        ]

        # Sort by frequency (descending)
        trending_keywords.sort(key=lambda x: x[1], reverse=True)
        trending_phrases.sort(key=lambda x: x[1], reverse=True)

        # Detect trending by category
        trending_by_category = {}
        for category, keywords in keywords_by_category.items():
            category_counts = Counter(keywords)
            trending_by_category[category] = [
                (keyword, count) for keyword, count in category_counts.items()
                if count >= self.threshold
            ]

        result = {
            'trending_keywords': trending_keywords[:10],  # Top 10 keywords
            'trending_phrases': trending_phrases[:5],  # Top 5 phrases
            'trending_by_category': {
                cat: items[:5] for cat, items in trending_by_category.items()
            },
            'time_window_hours': TIME_WINDOW_HOURS,
            'total_articles_analyzed': len(recent_articles),
            'threshold': self.threshold
        }

        self._log_trending_results(result)

        return result

    def _log_trending_results(self, result: Dict):
        """Log trending detection results"""
        logger.info(f"Trending Detection Results (last {result['time_window_hours']}h):")
        logger.info(f"  Articles analyzed: {result['total_articles_analyzed']}")
        logger.info(f"  Threshold: {result['threshold']}")

        if result['trending_keywords']:
            logger.info("  Top trending keywords:")
            for keyword, count in result['trending_keywords'][:5]:
                logger.info(f"    - {keyword}: {count} mentions")

        if result['trending_by_category']:
            logger.info("  Trending by category:")
            for category, items in result['trending_by_category'].items():
                if items:
                    logger.info(f"    {category}: {len(items)} topics")

    def get_article_trending_score(self, article: Dict, trending_data: Dict) -> float:
        """
        Calculate a trending score for an article based on trending topics

        Args:
            article: Article to score
            trending_data: Trending detection results

        Returns:
            Trending score (0.0 to 1.0)
        """
        text = f"{article.get('title', '')} {article.get('summary', '')}".lower()
        keywords = self.extract_keywords(text)

        # Count matches with trending keywords
        trending_keywords_set = set(k for k, v in trending_data.get('trending_keywords', []))
        matches = sum(1 for k in keywords if k in trending_keywords_set)

        # Normalize score
        if matches == 0:
            return 0.0
        else:
            # Cap at 5 matches
            score = min(matches / 5.0, 1.0)
            return round(score, 2)

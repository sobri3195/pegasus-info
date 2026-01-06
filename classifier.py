"""
News Classifier Module - Categorizes news articles
"""

import re
from typing import Dict, List, Set
from collections import Counter
import logging

from config import HEALTH_KEYWORDS, MILITARY_KEYWORDS, ECONOMY_KEYWORDS, SENSITIVE_TOPICS

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NewsClassifier:
    """Classifies news articles into categories"""

    def __init__(self):
        self.category_keywords = {
            'health': set(word.lower() for word in HEALTH_KEYWORDS),
            'military': set(word.lower() for word in MILITARY_KEYWORDS),
            'economy': set(word.lower() for word in ECONOMY_KEYWORDS),
        }

    def classify_article(self, article: Dict) -> Dict[str, any]:
        """
        Classify a single article

        Args:
            article: Article dictionary with title, summary, etc.

        Returns:
            Article with added classification fields
        """
        text = f"{article.get('title', '')} {article.get('summary', '')}".lower()

        scores = self._calculate_category_scores(text)
        primary_category, secondary_categories = self._determine_categories(scores)

        sensitive_topics = self._detect_sensitive_topics(text, primary_category)

        article.update({
            'primary_category': primary_category,
            'secondary_categories': secondary_categories,
            'category_scores': scores,
            'sensitive_topics': sensitive_topics,
            'is_sensitive': len(sensitive_topics) > 0
        })

        return article

    def _calculate_category_scores(self, text: str) -> Dict[str, int]:
        """Calculate keyword match scores for each category"""
        words = re.findall(r'\b\w+\b', text)

        scores = {}
        for category, keywords in self.category_keywords.items():
            score = sum(1 for word in words if word in keywords)
            scores[category] = score

        return scores

    def _determine_categories(self, scores: Dict[str, int]) -> tuple:
        """
        Determine primary and secondary categories

        Returns:
            Tuple of (primary_category, list_of_secondary_categories)
        """
        # Filter out zero scores
        nonzero_scores = {k: v for k, v in scores.items() if v > 0}

        if not nonzero_scores:
            return 'general', []

        # Sort by score (descending)
        sorted_scores = sorted(nonzero_scores.items(), key=lambda x: x[1], reverse=True)

        primary = sorted_scores[0][0]
        secondary = [cat for cat, score in sorted_scores[1:] if score > 0]

        return primary, secondary

    def _detect_sensitive_topics(self, text: str, category: str) -> List[str]:
        """Detect sensitive topics that need alerts"""
        detected_topics = []

        if category in SENSITIVE_TOPICS:
            for topic in SENSITIVE_TOPICS[category]:
                if topic.lower() in text:
                    detected_topics.append(topic)

        return detected_topics

    def classify_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        Classify multiple articles

        Args:
            articles: List of article dictionaries

        Returns:
            List of classified articles
        """
        classified = []
        for article in articles:
            classified_article = self.classify_article(article)
            classified.append(classified_article)

        logger.info(f"Classified {len(classified)} articles")

        # Log category distribution
        self._log_category_distribution(classified)

        return classified

    def _log_category_distribution(self, articles: List[Dict]):
        """Log the distribution of article categories"""
        distribution = Counter([a.get('primary_category', 'general') for a in articles])

        logger.info("Category distribution:")
        for category, count in distribution.most_common():
            logger.info(f"  {category}: {count}")

    def get_category_stats(self, articles: List[Dict]) -> Dict[str, Dict]:
        """
        Get statistics about article classifications

        Returns:
            Dictionary with statistics for each category
        """
        stats = {
            'total': len(articles),
            'by_category': {},
            'sensitive_count': 0,
            'multi_category_count': 0
        }

        category_counts = Counter()
        sensitive_count = 0
        multi_category_count = 0

        for article in articles:
            primary = article.get('primary_category', 'general')
            category_counts[primary] += 1

            if article.get('is_sensitive', False):
                sensitive_count += 1

            if len(article.get('secondary_categories', [])) > 0:
                multi_category_count += 1

        stats['by_category'] = dict(category_counts)
        stats['sensitive_count'] = sensitive_count
        stats['multi_category_count'] = multi_category_count

        return stats

"""
Summary Module - Auto-generates news summaries
"""

from typing import List, Dict
import re
from collections import Counter
import logging

from config import SUMMARY_MAX_LENGTH, SUMMARY_MIN_LENGTH

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NewsSummarizer:
    """Generates summaries for news articles"""

    def __init__(self, max_length: int = SUMMARY_MAX_LENGTH):
        self.max_length = max_length

    def generate_summary(self, article: Dict) -> str:
        """
        Generate a summary for a single article

        Args:
            article: Article dictionary

        Returns:
            Summary text
        """
        # Use existing summary if available
        if article.get('summary') and len(article['summary']) <= self.max_length:
            return article['summary']

        # Generate summary from title and existing summary
        text = f"{article.get('title', '')} {article.get('summary', '')}"

        # Clean and truncate
        summary = self._clean_text(text)
        summary = self._truncate_text(summary)

        return summary

    def _clean_text(self, text: str) -> str:
        """Clean text for summarization"""
        # Remove special characters and extra whitespace
        text = re.sub(r'[^\w\s.,;:-]', '', text)
        text = re.sub(r'\s+', ' ', text).strip()

        return text

    def _truncate_text(self, text: str) -> str:
        """Truncate text to maximum length while keeping it readable"""
        if len(text) <= self.max_length:
            return text

        # Find the last complete sentence before the max length
        sentences = re.split(r'[.!?]', text)
        result = ''
        total_length = 0

        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue

            if total_length + len(sentence) + 1 <= self.max_length:
                result += sentence + '. '
                total_length += len(sentence) + 1
            else:
                break

        if not result:
            # Fallback: simple truncation
            result = text[:self.max_length].rsplit(' ', 1)[0] + '...'

        return result.strip()

    def generate_insight(self, article: Dict) -> str:
        """
        Generate a short insight about the article

        Args:
            article: Article dictionary

        Returns:
            Insight text
        """
        category = article.get('primary_category', 'general')
        impact = article.get('impact_level', 'unknown')
        sentiment = article.get('sentiment', 'neutral')
        sensitive = article.get('is_sensitive', False)

        # Build insight based on category and analysis
        if sensitive:
            insight = f"⚠️ SENSITIVE: This {category} news requires attention. "
        else:
            insight = f"📊 {impact.upper()} impact {category} update. "

        # Add sentiment context
        if sentiment == 'positive':
            insight += "Positive developments indicated. "
        elif sentiment == 'negative':
            insight += "Concerning trend noted. "
        else:
            insight += "Neutral information. "

        # Add entities if available
        entities = article.get('entities', {})
        if entities.get('countries'):
            insight += f"Affects {', '.join(entities['countries'][:2])}. "

        return insight.strip()

    def generate_batch_insights(self, articles: List[Dict]) -> List[str]:
        """
        Generate insights for multiple articles

        Args:
            articles: List of articles

        Returns:
            List of insights
        """
        insights = []
        for article in articles:
            insight = self.generate_insight(article)
            insights.append(insight)

        return insights

    def generate_category_summary(self, articles: List[Dict], category: str) -> str:
        """
        Generate a summary for a specific category

        Args:
            articles: List of articles
            category: Category to summarize

        Returns:
            Category summary text
        """
        # Filter articles by category
        category_articles = [
            a for a in articles
            if a.get('primary_category') == category
        ]

        if not category_articles:
            return f"No articles found for category: {category}"

        # Get top keywords
        from trending import TrendingDetector
        detector = TrendingDetector()
        all_text = ' '.join([
            f"{a.get('title', '')} {a.get('summary', '')}"
            for a in category_articles
        ])
        keywords = detector.extract_keywords(all_text)
        keyword_counts = Counter(keywords).most_common(5)

        # Get impact distribution
        from collections import Counter
        impact_dist = Counter([a.get('impact_level', 'unknown') for a in category_articles])

        # Build summary
        summary = f"## {category.title()} News Summary\n\n"
        summary += f"**Total Articles:** {len(category_articles)}\n"
        summary += f"**High Impact:** {impact_dist.get('high', 0)}\n"
        summary += f"**Medium Impact:** {impact_dist.get('medium', 0)}\n"
        summary += f"**Low Impact:** {impact_dist.get('low', 0)}\n\n"

        if keyword_counts:
            summary += f"**Top Topics:**\n"
            for keyword, count in keyword_counts:
                summary += f"  - {keyword.title()}: {count} articles\n"

        return summary

    def summarize_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        Add summaries to multiple articles

        Args:
            articles: List of article dictionaries

        Returns:
            List of articles with summaries
        """
        for article in articles:
            article['summary'] = self.generate_summary(article)
            article['insight'] = self.generate_insight(article)

        logger.info(f"Generated summaries for {len(articles)} articles")

        return articles

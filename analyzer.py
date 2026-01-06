"""
Analysis Module - Analyzes news articles for context and impact
"""

from typing import List, Dict
from collections import defaultdict
import re
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NewsAnalyzer:
    """Analyzes news articles for context and impact"""

    def __init__(self):
        self.impact_keywords = {
            'high': ['crisis', 'emergency', 'disaster', 'deadly', 'fatal', 'severe',
                    'collapse', 'critical', 'urgent', 'warning', 'threat', 'attack'],
            'medium': ['significant', 'major', 'important', 'serious', 'concern',
                      'issue', 'problem', 'challenge', 'risk', 'developing'],
            'low': ['update', 'report', 'statement', 'announcement', 'minor',
                   'small', 'slight', 'normal', 'routine']
        }

    def analyze_article(self, article: Dict) -> Dict[str, any]:
        """
        Analyze a single article

        Args:
            article: Article dictionary

        Returns:
            Article with analysis fields added
        """
        text = f"{article.get('title', '')} {article.get('summary', '')}".lower()

        impact_level = self._assess_impact(text)
        entities = self._extract_entities(text)
        sentiment = self._assess_sentiment(text)

        article.update({
            'impact_level': impact_level,
            'entities': entities,
            'sentiment': sentiment
        })

        return article

    def _assess_impact(self, text: str) -> str:
        """Assess the potential impact level of an article"""
        high_score = sum(1 for kw in self.impact_keywords['high'] if kw in text)
        medium_score = sum(1 for kw in self.impact_keywords['medium'] if kw in text)

        if high_score > 0:
            return 'high'
        elif medium_score > 1:
            return 'medium'
        else:
            return 'low'

    def _extract_entities(self, text: str) -> Dict[str, List[str]]:
        """
        Extract named entities from text (simple pattern matching)

        Returns:
            Dictionary with entity types and values
        """
        entities = {
            'locations': self._extract_locations(text),
            'organizations': self._extract_organizations(text),
            'countries': self._extract_countries(text)
        }

        return entities

    def _extract_locations(self, text: str) -> List[str]:
        """Extract location names (simplified)"""
        location_patterns = [
            r'\b(New York|Washington|London|Paris|Tokyo|Beijing|Moscow|Berlin|Rome)\b',
            r'\b(United States|USA|US|UK|Russia|China|India|Brazil|Australia)\b',
            r'\b(California|Texas|Florida|New York)\b',
        ]

        locations = []
        for pattern in location_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            locations.extend(matches)

        return list(set(locations))

    def _extract_organizations(self, text: str) -> List[str]:
        """Extract organization names (simplified)"""
        org_patterns = [
            r'\b(WHO|CDC|FDA|United Nations|NATO|World Bank|IMF)\b',
            r'\b(Federal Reserve|European Central Bank)\b',
        ]

        organizations = []
        for pattern in org_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            organizations.extend(matches)

        return list(set(organizations))

    def _extract_countries(self, text: str) -> List[str]:
        """Extract country names (simplified list)"""
        countries = [
            'afghanistan', 'albania', 'algeria', 'argentina', 'australia',
            'austria', 'bangladesh', 'belgium', 'brazil', 'bulgaria',
            'canada', 'chile', 'china', 'colombia', 'croatia', 'cuba',
            'czech republic', 'denmark', 'egypt', 'estonia', 'finland',
            'france', 'germany', 'greece', 'hungary', 'iceland', 'india',
            'indonesia', 'iran', 'iraq', 'ireland', 'israel', 'italy',
            'japan', 'jordan', 'kazakhstan', 'kenya', 'kuwait', 'latvia',
            'lebanon', 'lithuania', 'luxembourg', 'malaysia', 'mexico',
            'morocco', 'myanmar', 'netherlands', 'new zealand', 'nigeria',
            'north korea', 'norway', 'pakistan', 'peru', 'philippines',
            'poland', 'portugal', 'qatar', 'romania', 'russia', 'saudi arabia',
            'serbia', 'singapore', 'slovakia', 'slovenia', 'south africa',
            'south korea', 'spain', 'sweden', 'switzerland', 'syria', 'taiwan',
            'thailand', 'turkey', 'ukraine', 'united arab emirates', 'ukraine',
            'united kingdom', 'uk', 'vietnam', 'yemen'
        ]

        found = []
        for country in countries:
            if country in text:
                found.append(country.title())

        return found

    def _assess_sentiment(self, text: str) -> str:
        """Assess the sentiment of the article"""
        positive_words = ['improvement', 'growth', 'success', 'positive', 'benefit',
                         'recovery', 'increase', 'boost', 'advantage', 'gain']
        negative_words = ['decline', 'loss', 'crisis', 'failure', 'negative',
                         'decrease', 'fall', 'threat', 'risk', 'danger', 'concern']

        pos_count = sum(1 for word in positive_words if word in text)
        neg_count = sum(1 for word in negative_words if word in text)

        if neg_count > pos_count:
            return 'negative'
        elif pos_count > neg_count:
            return 'positive'
        else:
            return 'neutral'

    def analyze_articles(self, articles: List[Dict]) -> List[Dict]:
        """
        Analyze multiple articles

        Args:
            articles: List of article dictionaries

        Returns:
            List of analyzed articles
        """
        analyzed = []
        for article in articles:
            analyzed_article = self.analyze_article(article)
            analyzed.append(analyzed_article)

        logger.info(f"Analyzed {len(analyzed)} articles")

        # Log analysis statistics
        self._log_analysis_stats(analyzed)

        return analyzed

    def _log_analysis_stats(self, articles: List[Dict]):
        """Log analysis statistics"""
        from collections import Counter

        impact_dist = Counter([a.get('impact_level', 'unknown') for a in articles])
        sentiment_dist = Counter([a.get('sentiment', 'unknown') for a in articles])

        logger.info("Impact Level Distribution:")
        for impact, count in impact_dist.items():
            logger.info(f"  {impact}: {count}")

        logger.info("Sentiment Distribution:")
        for sentiment, count in sentiment_dist.items():
            logger.info(f"  {sentiment}: {count}")

    def get_analysis_summary(self, articles: List[Dict]) -> Dict[str, any]:
        """
        Get a summary of the analysis

        Returns:
            Analysis summary dictionary
        """
        from collections import Counter

        impact_dist = Counter([a.get('impact_level', 'unknown') for a in articles])
        sentiment_dist = Counter([a.get('sentiment', 'unknown') for a in articles])

        # Collect all entities
        all_entities = defaultdict(list)
        for article in articles:
            for entity_type, entities in article.get('entities', {}).items():
                all_entities[entity_type].extend(entities)

        # Count entities
        entity_counts = {}
        for entity_type, entities in all_entities.items():
            entity_counts[entity_type] = dict(Counter(entities).most_common(10))

        summary = {
            'total_articles': len(articles),
            'impact_distribution': dict(impact_dist),
            'sentiment_distribution': dict(sentiment_dist),
            'top_entities': entity_counts,
            'high_impact_count': impact_dist.get('high', 0),
            'negative_sentiment_count': sentiment_dist.get('negative', 0)
        }

        return summary

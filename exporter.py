"""
Export Module - Exports news data to various formats
"""

import json
import csv
import os
from datetime import datetime
from typing import List, Dict
import logging

from config import EXPORT_DIR, EXPORT_FORMATS

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NewsExporter:
    """Exports news data to various formats"""

    def __init__(self, export_dir: str = EXPORT_DIR):
        self.export_dir = export_dir
        self._ensure_export_dir()

    def _ensure_export_dir(self):
        """Create export directory if it doesn't exist"""
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)
            logger.info(f"Created export directory: {self.export_dir}")

    def _get_timestamp(self) -> str:
        """Get current timestamp for filenames"""
        return datetime.now().strftime('%Y%m%d_%H%M%S')

    def _format_datetime(self, dt) -> str:
        """Format datetime for export"""
        if dt:
            return dt.isoformat()
        return ''

    def export_json(self, articles: List[Dict], filename: str = None) -> str:
        """
        Export articles to JSON format

        Args:
            articles: List of article dictionaries
            filename: Optional filename (without extension)

        Returns:
            Path to exported file
        """
        if filename is None:
            filename = f"news_{self._get_timestamp()}"

        filepath = os.path.join(self.export_dir, f"{filename}.json")

        # Prepare data for JSON export
        export_data = {
            'metadata': {
                'exported_at': datetime.now().isoformat(),
                'total_articles': len(articles),
                'format': 'json'
            },
            'articles': []
        }

        for article in articles:
            article_copy = article.copy()

            # Convert datetime objects to strings
            article_copy['published_date'] = self._format_datetime(article.get('published_date'))
            article_copy['fetched_at'] = self._format_datetime(article.get('fetched_at'))

            export_data['articles'].append(article_copy)

        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)

        logger.info(f"Exported {len(articles)} articles to JSON: {filepath}")
        return filepath

    def export_csv(self, articles: List[Dict], filename: str = None) -> str:
        """
        Export articles to CSV format

        Args:
            articles: List of article dictionaries
            filename: Optional filename (without extension)

        Returns:
            Path to exported file
        """
        if filename is None:
            filename = f"news_{self._get_timestamp()}"

        filepath = os.path.join(self.export_dir, f"{filename}.csv")

        if not articles:
            logger.warning("No articles to export to CSV")
            return filepath

        # Determine all fields
        all_fields = set()
        for article in articles:
            all_fields.update(article.keys())

        fieldnames = sorted(list(all_fields))

        # Write to CSV
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)

            writer.writeheader()

            for article in articles:
                row = article.copy()

                # Convert datetime objects to strings
                for field in ['published_date', 'fetched_at']:
                    if field in row and row[field]:
                        row[field] = self._format_datetime(row[field])

                # Convert lists to strings
                for field, value in row.items():
                    if isinstance(value, (list, dict)):
                        row[field] = json.dumps(value)

                writer.writerow(row)

        logger.info(f"Exported {len(articles)} articles to CSV: {filepath}")
        return filepath

    def export_markdown(self, articles: List[Dict], filename: str = None) -> str:
        """
        Export articles to Markdown format

        Args:
            articles: List of article dictionaries
            filename: Optional filename (without extension)

        Returns:
            Path to exported file
        """
        if filename is None:
            filename = f"news_{self._get_timestamp()}"

        filepath = os.path.join(self.export_dir, f"{filename}.md")

        # Build markdown content
        lines = []
        lines.append("# Pegasus Info News Report")
        lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Total Articles:** {len(articles)}")
        lines.append("\n---\n")

        # Group by category
        from collections import defaultdict, Counter
        category_groups = defaultdict(list)
        for article in articles:
            category = article.get('primary_category', 'general')
            category_groups[category].append(article)

        # Sort by category
        for category in sorted(category_groups.keys()):
            articles_in_category = category_groups[category]

            lines.append(f"\n## {category.title()}")
            lines.append(f"**Articles:** {len(articles_in_category)}")
            lines.append("\n---\n")

            for i, article in enumerate(articles_in_category, 1):
                lines.append(f"### {i}. {article.get('title', 'No Title')}")
                lines.append(f"**Source:** {article.get('source', 'Unknown')}")
                lines.append(f"**Date:** {self._format_datetime(article.get('published_date'))}")
                lines.append(f"**Link:** {article.get('link', 'No link')}")

                if article.get('primary_category'):
                    lines.append(f"**Category:** {article.get('primary_category').title()}")

                if article.get('impact_level'):
                    impact_emoji = {
                        'high': '🔴',
                        'medium': '🟡',
                        'low': '🟢'
                    }
                    lines.append(f"**Impact:** {impact_emoji.get(article['impact_level'], '')} {article['impact_level'].title()}")

                if article.get('is_sensitive'):
                    lines.append(f"**Status:** ⚠️ SENSITIVE")

                lines.append(f"\n**Summary:**\n{article.get('summary', 'No summary')}")

                if article.get('insight'):
                    lines.append(f"\n**Insight:**\n{article.get('insight')}")

                if article.get('entities'):
                    entities = article.get('entities', {})
                    entity_list = []
                    for entity_type, items in entities.items():
                        if items:
                            entity_list.append(f"{entity_type.title()}: {', '.join(items[:3])}")
                    if entity_list:
                        lines.append(f"\n**Entities:** {', '.join(entity_list)}")

                lines.append("\n---\n")

        # Write to file
        content = '\n'.join(lines)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Exported {len(articles)} articles to Markdown: {filepath}")
        return filepath

    def export_all_formats(self, articles: List[Dict], filename: str = None) -> Dict[str, str]:
        """
        Export articles to all available formats

        Args:
            articles: List of article dictionaries
            filename: Optional filename (without extension)

        Returns:
            Dictionary mapping format to filepath
        """
        results = {}

        for format_type in EXPORT_FORMATS:
            try:
                if format_type == 'json':
                    filepath = self.export_json(articles, filename)
                elif format_type == 'csv':
                    filepath = self.export_csv(articles, filename)
                elif format_type == 'markdown':
                    filepath = self.export_markdown(articles, filename)
                else:
                    logger.warning(f"Unknown export format: {format_type}")
                    continue

                results[format_type] = filepath

            except Exception as e:
                logger.error(f"Error exporting to {format_type}: {str(e)}")

        return results

    def export_trending_report(self, trending_data: Dict, filename: str = None) -> str:
        """
        Export trending report to Markdown

        Args:
            trending_data: Trending detection results
            filename: Optional filename

        Returns:
            Path to exported file
        """
        if filename is None:
            filename = f"trending_{self._get_timestamp()}"

        filepath = os.path.join(self.export_dir, f"{filename}.md")

        # Build markdown content
        lines = []
        lines.append("# Trending Topics Report")
        lines.append(f"\n**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append(f"**Time Window:** Last {trending_data.get('time_window_hours', 24)} hours")
        lines.append(f"**Articles Analyzed:** {trending_data.get('total_articles_analyzed', 0)}")
        lines.append("\n---\n")

        # Top trending keywords
        if trending_data.get('trending_keywords'):
            lines.append("## 🔥 Top Trending Keywords\n")
            for keyword, count in trending_data['trending_keywords']:
                lines.append(f"- **{keyword.title()}**: {count} mentions")
            lines.append("\n---\n")

        # Top trending phrases
        if trending_data.get('trending_phrases'):
            lines.append("## 🔥 Top Trending Phrases\n")
            for phrase, count in trending_data['trending_phrases']:
                lines.append(f"- **{phrase.title()}**: {count} mentions")
            lines.append("\n---\n")

        # Trending by category
        if trending_data.get('trending_by_category'):
            lines.append("## 📊 Trending by Category\n")
            for category, items in trending_data['trending_by_category'].items():
                if items:
                    lines.append(f"\n### {category.title()}\n")
                    for keyword, count in items:
                        lines.append(f"- {keyword.title()}: {count} mentions")
            lines.append("\n---\n")

        # Write to file
        content = '\n'.join(lines)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"Exported trending report: {filepath}")
        return filepath

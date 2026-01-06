"""
Pegasus Info - News Intelligence System
Main Application Entry Point
"""

import logging
from typing import List, Dict
from datetime import datetime

from scraper import NewsScraper
from classifier import NewsClassifier
from trending import TrendingDetector
from analyzer import NewsAnalyzer
from summarizer import NewsSummarizer
from exporter import NewsExporter

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('pegasus_info.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class PegasusInfo:
    """
    Pegasus Info - Main intelligence system for news gathering and analysis
    """

    def __init__(self):
        self.scraper = NewsScraper()
        self.classifier = NewsClassifier()
        self.trending_detector = TrendingDetector()
        self.analyzer = NewsAnalyzer()
        self.summarizer = NewsSummarizer()
        self.exporter = NewsExporter()

        logger.info("=" * 60)
        logger.info("PEGASUS INFO - News Intelligence System")
        logger.info("Initialized successfully")
        logger.info("=" * 60)

    def run_full_pipeline(self, hours: int = 24, export: bool = True) -> Dict[str, any]:
        """
        Run the complete news intelligence pipeline

        Args:
            hours: Number of hours to look back for articles
            export: Whether to export results

        Returns:
            Dictionary with all results
        """
        logger.info("\n" + "=" * 60)
        logger.info("STARTING FULL PIPELINE")
        logger.info("=" * 60 + "\n")

        results = {
            'started_at': datetime.now(),
            'articles': [],
            'trending': None,
            'analysis': None,
            'exports': {}
        }

        try:
            # Step 1: Fetch articles
            logger.info("\n[1/6] Fetching news articles...")
            all_articles = self.scraper.fetch_all_feeds()

            # Filter by date
            recent_articles = self.scraper.filter_by_date(all_articles, hours)
            logger.info(f"Recent articles (last {hours} hours): {len(recent_articles)}")

            if not recent_articles:
                logger.warning("No recent articles found. Pipeline stopped.")
                return results

            results['articles'] = recent_articles

            # Step 2: Classify articles
            logger.info("\n[2/6] Classifying articles...")
            classified_articles = self.classifier.classify_articles(recent_articles)
            results['articles'] = classified_articles

            # Step 3: Detect trending topics
            logger.info("\n[3/6] Detecting trending topics...")
            trending_data = self.trending_detector.detect_trending(classified_articles)
            results['trending'] = trending_data

            # Step 4: Analyze articles
            logger.info("\n[4/6] Analyzing articles...")
            analyzed_articles = self.analyzer.analyze_articles(classified_articles)
            results['articles'] = analyzed_articles

            # Step 5: Generate summaries
            logger.info("\n[5/6] Generating summaries and insights...")
            summarized_articles = self.summarizer.summarize_articles(analyzed_articles)
            results['articles'] = summarized_articles

            # Step 6: Generate analysis summary
            analysis_summary = self.analyzer.get_analysis_summary(summarized_articles)
            results['analysis'] = analysis_summary

            # Step 7: Export results
            if export:
                logger.info("\n[6/6] Exporting results...")
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')

                # Export articles
                export_results = self.exporter.export_all_formats(
                    summarized_articles,
                    filename=f"news_{timestamp}"
                )
                results['exports']['articles'] = export_results

                # Export trending report
                trending_filepath = self.exporter.export_trending_report(
                    trending_data,
                    filename=f"trending_{timestamp}"
                )
                results['exports']['trending'] = trending_filepath

            logger.info("\n" + "=" * 60)
            logger.info("PIPELINE COMPLETED SUCCESSFULLY")
            logger.info(f"Total articles processed: {len(summarized_articles)}")
            logger.info("=" * 60 + "\n")

            # Print summary
            self._print_summary(results)

            results['completed_at'] = datetime.now()
            results['status'] = 'success'

        except Exception as e:
            logger.error(f"Error in pipeline: {str(e)}", exc_info=True)
            results['status'] = 'error'
            results['error'] = str(e)

        return results

    def fetch_and_classify(self, hours: int = 24) -> List[Dict]:
        """
        Quick fetch and classify articles

        Args:
            hours: Number of hours to look back

        Returns:
            List of classified articles
        """
        articles = self.scraper.fetch_all_feeds()
        recent = self.scraper.filter_by_date(articles, hours)
        classified = self.classifier.classify_articles(recent)
        return classified

    def get_trending(self, hours: int = 24) -> Dict[str, any]:
        """
        Get trending topics

        Args:
            hours: Number of hours to look back

        Returns:
            Trending data dictionary
        """
        articles = self.fetch_and_classify(hours)
        trending = self.trending_detector.detect_trending(articles)
        return trending

    def _print_summary(self, results: Dict):
        """Print a summary of the results"""
        articles = results.get('articles', [])
        analysis = results.get('analysis', {})
        trending = results.get('trending', {})

        print("\n" + "=" * 60)
        print("PEGASUS INFO - SUMMARY REPORT")
        print("=" * 60)

        print(f"\n📰 Total Articles: {len(articles)}")

        if analysis:
            print(f"\n📊 Impact Distribution:")
            print(f"   High: {analysis.get('high_impact_count', 0)}")
            print(f"   Negative Sentiment: {analysis.get('negative_sentiment_count', 0)}")

        if trending:
            print(f"\n🔥 Top Trending Keywords:")
            for keyword, count in trending.get('trending_keywords', [])[:5]:
                print(f"   - {keyword.title()}: {count} mentions")

        if results.get('exports'):
            print(f"\n💾 Exported Files:")
            for format_type, filepath in results['exports'].get('articles', {}).items():
                print(f"   {format_type.upper()}: {filepath}")

        print("\n" + "=" * 60)


def main():
    """Main entry point for command line usage"""
    import argparse

    parser = argparse.ArgumentParser(
        description='Pegasus Info - News Intelligence System'
    )
    parser.add_argument(
        '--hours',
        type=int,
        default=24,
        help='Hours to look back for articles (default: 24)'
    )
    parser.add_argument(
        '--no-export',
        action='store_true',
        help='Skip exporting results'
    )
    parser.add_argument(
        '--category',
        type=str,
        choices=['health', 'military', 'economy', 'general'],
        help='Filter by category'
    )

    args = parser.parse_args()

    # Initialize Pegasus Info
    pegasus = PegasusInfo()

    # Run the pipeline
    results = pegasus.run_full_pipeline(
        hours=args.hours,
        export=not args.no_export
    )

    # Print results
    if results['status'] == 'success':
        print("\n✅ Pipeline completed successfully!")
    else:
        print(f"\n❌ Pipeline failed: {results.get('error', 'Unknown error')}")


if __name__ == '__main__':
    main()

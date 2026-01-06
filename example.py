"""
Example usage of Pegasus Info
Demonstrates how to use the system
"""

from pegasus_info import PegasusInfo
from scraper import NewsScraper
from classifier import NewsClassifier
from trending import TrendingDetector
from analyzer import NewsAnalyzer
from summarizer import NewsSummarizer

def example_basic_usage():
    """Example 1: Basic usage with full pipeline"""
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Basic Usage - Full Pipeline")
    print("=" * 60)

    # Initialize Pegasus Info
    pegasus = PegasusInfo()

    # Run full pipeline
    results = pegasus.run_full_pipeline(hours=24, export=True)

    # Print summary
    if results['status'] == 'success':
        articles = results['articles']
        print(f"\n✅ Processed {len(articles)} articles")

        # Show first 3 articles
        print("\nTop 3 Articles:")
        for i, article in enumerate(articles[:3], 1):
            print(f"\n{i}. {article['title']}")
            print(f"   Category: {article.get('primary_category', 'N/A')}")
            print(f"   Impact: {article.get('impact_level', 'N/A')}")
            print(f"   Sentiment: {article.get('sentiment', 'N/A')}")
            if article.get('is_sensitive'):
                print(f"   ⚠️ SENSITIVE TOPIC")


def example_fetch_classify():
    """Example 2: Fetch and classify only"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Fetch and Classify Only")
    print("=" * 60)

    pegasus = PegasusInfo()

    # Fetch and classify
    classified = pegasus.fetch_and_classify(hours=48)

    print(f"\nFetched and classified {len(classified)} articles")

    # Show category distribution
    from collections import Counter
    categories = Counter([a.get('primary_category', 'general') for a in classified])

    print("\nCategory Distribution:")
    for category, count in categories.most_common():
        print(f"  {category}: {count}")


def example_trending_topics():
    """Example 3: Get trending topics"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Trending Topics Detection")
    print("=" * 60)

    pegasus = PegasusInfo()

    # Get trending topics
    trending = pegasus.get_trending(hours=24)

    print(f"\nArticles analyzed: {trending['total_articles_analyzed']}")
    print(f"Time window: {trending['time_window_hours']} hours")

    print("\n🔥 Top 5 Trending Keywords:")
    for keyword, count in trending['trending_keywords'][:5]:
        print(f"  {keyword.title()}: {count} mentions")

    print("\n🔥 Top 3 Trending Phrases:")
    for phrase, count in trending['trending_phrases'][:3]:
        print(f"  {phrase.title()}: {count} mentions")


def example_detailed_article_analysis():
    """Example 4: Detailed article analysis"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Detailed Article Analysis")
    print("=" * 60)

    # Create sample article
    sample_article = {
        'title': 'WHO announces new vaccine rollout for global distribution',
        'link': 'https://example.com/who-vaccine',
        'summary': 'The World Health Organization announced today the launch of a new vaccine distribution program to combat the recent outbreak in Southeast Asia. This initiative aims to reach millions of people in affected regions within the next six months.',
        'published_date': None,
        'category': 'health',
        'source': 'WHO'
    }

    print(f"\nOriginal Article:")
    print(f"Title: {sample_article['title']}")
    print(f"Summary: {sample_article['summary']}")

    # Classify
    classifier = NewsClassifier()
    classified = classifier.classify_article(sample_article)
    print(f"\n✅ Classification:")
    print(f"  Primary Category: {classified['primary_category']}")
    print(f"  Secondary Categories: {classified['secondary_categories']}")
    print(f"  Is Sensitive: {classified['is_sensitive']}")
    if classified['sensitive_topics']:
        print(f"  Sensitive Topics: {', '.join(classified['sensitive_topics'])}")

    # Analyze
    analyzer = NewsAnalyzer()
    analyzed = analyzer.analyze_article(classified)
    print(f"\n✅ Analysis:")
    print(f"  Impact Level: {analyzed['impact_level']}")
    print(f"  Sentiment: {analyzed['sentiment']}")
    print(f"  Entities: {analyzed['entities']}")

    # Summarize
    summarizer = NewsSummarizer()
    analyzed_list = summarizer.summarize_articles([analyzed])
    analyzed = analyzed_list[0]
    print(f"\n✅ Summary & Insight:")
    print(f"  Summary: {analyzed['summary']}")
    print(f"  Insight: {analyzed['insight']}")


def example_sensitive_alerts():
    """Example 5: Detect sensitive topics"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Sensitive Topic Detection")
    print("=" * 60)

    pegasus = PegasusInfo()

    # Fetch and classify
    classified = pegasus.fetch_and_classify(hours=72)

    # Filter sensitive articles
    sensitive_articles = [
        a for a in classified if a.get('is_sensitive', False)
    ]

    print(f"\nTotal articles: {len(classified)}")
    print(f"Sensitive articles: {len(sensitive_articles)}")

    if sensitive_articles:
        print("\n⚠️ Sensitive Topics Found:")
        for article in sensitive_articles[:5]:
            print(f"\n  Title: {article['title']}")
            print(f"  Category: {article['primary_category']}")
            print(f"  Sensitive Topics: {', '.join(article.get('sensitive_topics', []))}")
            print(f"  Impact: {article['impact_level']}")
    else:
        print("\n✅ No sensitive topics detected")


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("PEGASUS INFO - USAGE EXAMPLES")
    print("=" * 60)

    try:
        # Example 1: Basic usage
        # example_basic_usage()

        # Example 2: Fetch and classify
        example_fetch_classify()

        # Example 3: Trending topics
        example_trending_topics()

        # Example 4: Detailed analysis
        example_detailed_article_analysis()

        # Example 5: Sensitive alerts
        example_sensitive_alerts()

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")

    print("\n" + "=" * 60)
    print("EXAMPLES COMPLETED")
    print("=" * 60)


if __name__ == '__main__':
    main()

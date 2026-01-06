"""
Simple test script to verify Pegasus Info basic functionality
"""

import sys

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")

    try:
        import config
        print("✅ config module imported")
    except Exception as e:
        print(f"❌ config module failed: {e}")
        return False

    try:
        from scraper import NewsScraper
        print("✅ scraper module imported")
    except Exception as e:
        print(f"❌ scraper module failed: {e}")
        return False

    try:
        from classifier import NewsClassifier
        print("✅ classifier module imported")
    except Exception as e:
        print(f"❌ classifier module failed: {e}")
        return False

    try:
        from trending import TrendingDetector
        print("✅ trending module imported")
    except Exception as e:
        print(f"❌ trending module failed: {e}")
        return False

    try:
        from analyzer import NewsAnalyzer
        print("✅ analyzer module imported")
    except Exception as e:
        print(f"❌ analyzer module failed: {e}")
        return False

    try:
        from summarizer import NewsSummarizer
        print("✅ summarizer module imported")
    except Exception as e:
        print(f"❌ summarizer module failed: {e}")
        return False

    try:
        from exporter import NewsExporter
        print("✅ exporter module imported")
    except Exception as e:
        print(f"❌ exporter module failed: {e}")
        return False

    try:
        from pegasus_info import PegasusInfo
        print("✅ pegasus_info module imported")
    except Exception as e:
        print(f"❌ pegasus_info module failed: {e}")
        return False

    return True


def test_basic_functionality():
    """Test basic functionality with sample data"""
    print("\n" + "=" * 60)
    print("Testing basic functionality...")
    print("=" * 60)

    # Sample article
    sample_article = {
        'title': 'WHO announces new health initiative',
        'link': 'https://example.com/who-initiative',
        'summary': 'The World Health Organization launched a new initiative to combat infectious diseases in developing regions.',
        'published_date': None,
        'category': 'general',
        'source': 'test'
    }

    # Test classifier
    try:
        from classifier import NewsClassifier
        classifier = NewsClassifier()
        classified = classifier.classify_article(sample_article)

        assert 'primary_category' in classified
        assert classified['primary_category'] == 'health'
        print("✅ Classifier works correctly")
    except Exception as e:
        print(f"❌ Classifier failed: {e}")
        return False

    # Test analyzer
    try:
        from analyzer import NewsAnalyzer
        analyzer = NewsAnalyzer()
        analyzed = analyzer.analyze_article(classified)

        assert 'impact_level' in analyzed
        assert 'sentiment' in analyzed
        print("✅ Analyzer works correctly")
    except Exception as e:
        print(f"❌ Analyzer failed: {e}")
        return False

    # Test summarizer
    try:
        from summarizer import NewsSummarizer
        summarizer = NewsSummarizer()
        # Use summarize_articles method which adds fields to the dictionary
        analyzed_list = summarizer.summarize_articles([analyzed])
        analyzed = analyzed_list[0]

        assert 'summary' in analyzed
        assert 'insight' in analyzed
        print("✅ Summarizer works correctly")
    except Exception as e:
        print(f"❌ Summarizer failed: {e}")
        return False

    # Test trending detector
    try:
        from trending import TrendingDetector
        detector = TrendingDetector()
        keywords = detector.extract_keywords(sample_article['title'])

        assert len(keywords) > 0
        print("✅ Trending detector works correctly")
    except Exception as e:
        print(f"❌ Trending detector failed: {e}")
        return False

    # Test exporter
    try:
        from exporter import NewsExporter
        exporter = NewsExporter()

        # Test JSON export
        json_path = exporter.export_json([analyzed], filename='test_export')
        assert json_path.endswith('test_export.json')
        print(f"✅ JSON export works: {json_path}")

        # Test CSV export
        csv_path = exporter.export_csv([analyzed], filename='test_export')
        assert csv_path.endswith('test_export.csv')
        print(f"✅ CSV export works: {csv_path}")

        # Test Markdown export
        md_path = exporter.export_markdown([analyzed], filename='test_export')
        assert md_path.endswith('test_export.md')
        print(f"✅ Markdown export works: {md_path}")

    except Exception as e:
        print(f"❌ Exporter failed: {e}")
        return False

    return True


def test_pegasus_init():
    """Test PegasusInfo initialization"""
    print("\n" + "=" * 60)
    print("Testing PegasusInfo initialization...")
    print("=" * 60)

    try:
        from pegasus_info import PegasusInfo
        pegasus = PegasusInfo()
        print("✅ PegasusInfo initialized successfully")
        return True
    except Exception as e:
        print(f"❌ PegasusInfo initialization failed: {e}")
        return False


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("PEGASUS INFO - TEST SUITE")
    print("=" * 60)

    all_passed = True

    # Test imports
    if not test_imports():
        all_passed = False

    # Test basic functionality
    if not test_basic_functionality():
        all_passed = False

    # Test PegasusInfo initialization
    if not test_pegasus_init():
        all_passed = False

    print("\n" + "=" * 60)
    if all_passed:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 60)

    return 0 if all_passed else 1


if __name__ == '__main__':
    sys.exit(main())

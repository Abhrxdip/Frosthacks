def test_sentiment_analyzer():
    from sentiment_analyzer import analyze_sentiment
    assert analyze_sentiment("I love programming!") == "positive"
    assert analyze_sentiment("I hate bugs!") == "negative"
    assert analyze_sentiment("It's okay.") == "neutral"
import pytest

@pytest.fixture
def sample_data():
    return "This is a sample input for testing."

@pytest.fixture
def sentiment_analyzer():
    from your_module import SentimentAnalyzer
    return SentimentAnalyzer()
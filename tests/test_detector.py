# Add src to path
import sys
sys.path.append('../src')
from hangover_lib import hangover_detector

def test_hangover_detector():
    detector = hangover_detector()
    test_url = "https://t4.ftcdn.net/jpg/01/58/86/39/360_F_158863947_9kRfTbvp6ZaFOG55GlWAidfZEjZvMG0L.jpg"
    prob, description = detector.detect(test_url)
    assert prob > 0.5
    assert description is not None

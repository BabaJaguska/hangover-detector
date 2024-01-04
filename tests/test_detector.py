# Add src to path
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.abspath(os.path.join(current_dir, "..", "src"))
sys.path.append(src_dir)

from hangover_lib import hangover_detector

# make a fixture
import pytest


@pytest.fixture
def detector():
    det = hangover_detector()
    yield det


def test_fixture(detector):
    assert detector is not None


# test detector
def test_hangover_person(detector):
    test_url = "https://t4.ftcdn.net/jpg/01/58/86/39/360_F_158863947_9kRfTbvp6ZaFOG55GlWAidfZEjZvMG0L.jpg"
    class_, probs, description = detector.detect(test_url)
    assert class_ == "A person with a hangover"
    assert probs[0] > 0.5
    assert description is not None


def test_not_hangover_person():
    detector = hangover_detector()
    test_url = "https://img.freepik.com/free-photo/handsome-cheerful-man-with-happy-smile_176420-18028.jpg"
    class_, probs, description = detector.detect(test_url)
    assert probs[0] < 0.5
    assert description is not None
    assert class_ == "A person feeling ok"


def test_not_person():
    detector = hangover_detector()
    test_url = "https://images.all-free-download.com/images/graphiclarge/nature_backdrop_picture_flying_butterflies_flower_6930710.jpg"
    class_, probs, description = detector.detect(test_url)
    assert probs[0] < 0.5
    assert description is not None
    assert class_ == "Still-life"

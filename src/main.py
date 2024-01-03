from hangover_lib import hangover_detector


def main():
    detector = hangover_detector()
    test_url = "https://t4.ftcdn.net/jpg/01/58/86/39/360_F_158863947_9kRfTbvp6ZaFOG55GlWAidfZEjZvMG0L.jpg"
    prob, description = detector.detect(test_url)
    print(f"Probability of hangover: {prob:.2f}")
    print(f"Description: {description}")


if __name__ == "__main__":
    main()

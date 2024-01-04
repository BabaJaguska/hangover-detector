import streamlit as st


def main():
    print("Loading model, this may take a while...")
    from hangover_lib import hangover_detector

    detector = hangover_detector()
    test_url = "https://t4.ftcdn.net/jpg/01/58/86/39/360_F_158863947_9kRfTbvp6ZaFOG55GlWAidfZEjZvMG0L.jpg"
    class_, probs, description = detector.detect(test_url)
    print(f"Probability of hangover: {probs[0]:.2f}")
    print(f"Description: {description}")
    print(f"Class: {class_}")


def streamlit_main():
    st.title("Hangover Detector")
    st.write("This is a demo of the hangover detector.")
    st.write(
        "Provide an image URL and the detector will tell you if it's a hangover or not."
    )
    url = st.text_input("Image URL")
    detect_button = st.button("Detect")
    from hangover_lib import hangover_detector

    if detect_button:
        st.write("Detecting...")
        # Show image
        st.image(url, width=300)
        detector = hangover_detector()
        _, probs, description = detector.detect(url)
        st.write(f"Description: {description}")
        st.write(f"Probability of hangover: {probs[0]:.2f}")


if __name__ == "__main__":
    # streamlit_main()
    streamlit_main()

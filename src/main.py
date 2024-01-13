import streamlit as st
from hangover_lib import get_image_from_file, get_image_from_url


def main():
    print("Loading model, this may take a while...")
    from hangover_lib import hangover_detector

    detector = hangover_detector()
    test_url = "https://t4.ftcdn.net/jpg/01/58/86/39/360_F_158863947_9kRfTbvp6ZaFOG55GlWAidfZEjZvMG0L.jpg"
    try:
        class_, probs, description = detector.detect(test_url)
        print(f"Probability of hangover: {probs[0]:.2f}")
        print(f"Description: {description}")
        print(f"Class: {class_}")
    except Exception as e:
        print("Oops, something went wrong.")
        print("Error:", e)


def streamlit_main():
    st.title("Hangover Detector")
    st.write(
        "Provide an image URL or upload an image to see if you have a hangover."
    )
    left_column, right_column = st.columns(2)
    with left_column:
        url = st.text_input("Image URL")
        detect_url_button = st.button("Detect from URL")
        file = st.file_uploader(
            "Upload an image", type=["jpg", "jpeg", "png", "tif", "tiff"]
        )
        detect_upload_button = st.button("Detect from file")

    from hangover_lib import hangover_detector

    img = None
    status = st.empty()

    if detect_upload_button:
        status.write("Thinking...")
        if file is not None:
            image_bytes = file.getvalue()
            with right_column:
                try:
                    st.image(image_bytes, width=300)
                except:
                    st.write("Could not display image")

            try:
                img = get_image_from_file(image_bytes)
                detector = hangover_detector()
                _, probs, description = detector.detect(img)
                with left_column:
                    status.write("")
                    st.write(f"Description: {description}")
                    st.write(f"Probability of hangover: {probs[0]:.2f}")
                print(probs)
            except Exception as e:
                status.write(f"Oops, something went wrong.")
                print("Error:", e)
        else:
            status.write("Please upload an image")

    if detect_url_button:
        status.write("Thinking...")
        if url:
            with right_column:
                try:
                    st.image(url, width=300)
                except:
                    st.write("Could not display image")
            try:
                img = get_image_from_url(url)
                detector = hangover_detector()
                _, probs, description = detector.detect(img)
                status.write("")
                with left_column:
                    st.write(f"Description: {description}")
                    st.write(f"Probability of hangover: {probs[0]:.2f}")
                print(probs)
            except Exception as e:
                status.write(f"Oops, something went wrong.")
                print("Error:", e)
        else:
            status.write("Please provide a URL")


if __name__ == "__main__":
    streamlit_main()

import streamlit as st
from rembg import remove, new_session
from PIL import Image
import io
import time

session = new_session("u2net")

st.set_page_config(page_title="Background Remover", page_icon="BR", layout="centered")

st.title("Background Remover")
st.write("Upload an image and remove its background instantly.")

# File uploader
uploaded_file = st.file_uploader("Upload your image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Show original image
    st.subheader("Original Image")
    st.image(uploaded_file, use_container_width=True)

    if st.button("Remove Background"):
        with st.spinner("Processing your image..."):
            # Load image
            input_image = Image.open(uploaded_file)

            # Resize moderately to balance speed + quality
            max_size = (800, 800)
            input_image.thumbnail(max_size)

            # Progress bar
            progress = st.progress(0)
            time.sleep(0.3)
            progress.progress(30)

            # Use u2net model
            output_image = remove(input_image, session=session)

            progress.progress(70)

            # Edge smoothing (remove semi-transparent pixels)
            output_image = output_image.convert("RGBA")
            datas = output_image.getdata()
            newData = []
            for item in datas:
                if item[3] < 50:  # remove fuzzy edges
                    newData.append((255, 255, 255, 0))
                else:
                    newData.append(item)
            output_image.putdata(newData)

            progress.progress(100)

            # Convert output to bytes
            img_bytes = io.BytesIO()
            output_image.save(img_bytes, format="PNG")
            img_bytes.seek(0)

        # Show result
        st.success("Background removed successfully!")
        st.subheader("Output Image (Sharpened)")
        st.image(output_image, use_container_width=True)

        # Download button
        st.download_button(
            label="Download Image",
            data=img_bytes,
            file_name="background_removed.png",
            mime="image/png"
        )

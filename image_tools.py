import streamlit as st
from PIL import Image
import io

def show_image_tools():
    st.title("🖼️ AI Image Tools")

    st.write("Upload an image to preview, compress, resize, or analyze in future updates.")

    uploaded = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if uploaded:
        # Display image
        image = Image.open(uploaded)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        st.subheader("Image Info")
        st.write(f"Format: {image.format}")
        st.write(f"Size: {image.size[0]} x {image.size[1]}")
        st.write(f"Mode: {image.mode}")

        # Simple compress (save in memory)
        if st.button("Compress Image"):
            buf = io.BytesIO()
            image.save(buf, format="JPEG", optimize=True, quality=40)
            st.success("Image Compressed Successfully!")

            st.download_button(
                label="📥 Download Compressed Image",
                data=buf.getvalue(),
                file_name="compressed.jpg",
                mime="image/jpeg",
            )

        # Resize feature
        new_width = st.number_input("Resize Width", min_value=50, max_value=2000, value=image.size[0])
        new_height = st.number_input("Resize Height", min_value=50, max_value=2000, value=image.size[1])

        if st.button("Resize Image"):
            resized = image.resize((int(new_width), int(new_height)))
            st.image(resized, caption="Resized Image", use_column_width=True)

            buf = io.BytesIO()
            resized.save(buf, format="JPEG")
            st.download_button(
                label="📥 Download Resized Image",
                data=buf.getvalue(),
                file_name="resized.jpg",
                mime="image/jpeg",
            )

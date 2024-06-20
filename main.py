import streamlit as st
from PIL import Image
import io

def main():
    # Title of the app
    st.title("Internship Task")

    # Upload the image
    upload_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    processed_image = None


    if upload_image is not None:
        # Open the uploaded image
        image = Image.open(upload_image)
        
        col1 , col2 = st.columns(2)

        with col1:
            # Display the original image
            st.image(image, caption='Uploaded Image' , use_column_width=True , )


        if st.button("Analyse Image"):
            # Analyze the Image

            with col2:
                # Display the processed image
                st.image(processed_image, caption='Processed Image' , use_column_width=True , )

            # Provide a download button for the processed image
            buf = io.BytesIO()
            processed_image.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.download_button(
                label="Download Processed Image",
                data=byte_im,
                file_name="processed_image.png",
                mime="image/png"
            )

if __name__ == "__main__":
    main()

import streamlit as st
from PIL import Image
import io

from components_detector import detect_objects , draw_boxes , load_model , detector

def main():
    # Title of the app
    st.title("Internship Task")

    # Upload the image
    upload_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    analysed_image = None


    if upload_file is not None:
        # Open the uploaded image
        upload_image = Image.open(upload_file)
        
        col1 , col2 = st.columns(2)

        with col1:
            # Display the original image
            st.image(upload_image, caption='Uploaded Image' , use_column_width=True , )


        if st.button("Analyse Image"):
            objects = detect_objects(upload_image , detector)
            class_names = [ obj[0] for obj in objects ]
            
            analysed_image = draw_boxes(upload_image, objects)
            with col2:
                # Display the processed image
                st.image(analysed_image, caption='Analysed Image' , use_column_width=True , )

            st.write(f"Detected objects: {class_names}")

            # Provide a download button for the processed image
            buf = io.BytesIO()
            analysed_image.save(buf, format="PNG")
            byte_im = buf.getvalue()
            
            st.download_button(
                label="Download Analysed Image",
                data=byte_im,
                file_name="processed_image.png",
                mime="image/png"
            )

if __name__ == "__main__":
    detector = load_model() # Load the pre-trained model
    main()

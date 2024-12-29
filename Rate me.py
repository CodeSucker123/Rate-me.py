import os
import streamlit as st
from PIL import Image
import json

# Inject custom CSS for a persistent black background
st.markdown(
    """
    <style>
    /* Force black background */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stApp"] {
        background-color: black !important;
        color: white; /* Change text color to white for contrast */
    }
    .red-stripe {
        background-color: red; /* Create the red stripe */
        height: 20px;
        width: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Add the red stripe
st.markdown('<div class="red-stripe"></div>', unsafe_allow_html=True)

# Create directories for uploads and ratings
if not os.path.exists("uploads"):
    os.makedirs("uploads")
if not os.path.exists("ratings.json"):
    with open("ratings.json", "w") as f:
        json.dump({}, f)  # Initialize empty ratings

# Load existing ratings
with open("ratings.json", "r") as f:
    ratings = json.load(f)

# Set the title of the app
st.title("Rate me / Northbrook HS")

# Let users upload an image
uploaded_file = st.file_uploader("Upload a selfie", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Save the uploaded image
    file_path = os.path.join("uploads", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Open and display the uploaded image
    image = Image.open(file_path)
    st.image(image, caption="Uploaded Selfie", use_column_width=True)
    st.success(f"Image uploaded successfully and saved as {uploaded_file.name}!")

# Display previously uploaded images with rating options
st.subheader("Rate Uploaded Images")
for file_name in os.listdir("uploads"):
    file_path = os.path.join("uploads", file_name)
    st.image(file_path, caption=file_name, use_column_width=True)

    # Show average rating
    file_ratings = ratings.get(file_name, [])
    if file_ratings:
        avg_rating = sum(file_ratings) / len(file_ratings)
        st.write(f"Average Rating (out of 10): {avg_rating:.1f} ({len(file_ratings)} ratings)")
    else:
        st.write("No ratings yet.")

    # Show the rating slider
    user_rating = st.slider(f"Rate {file_name}", 1, 10, value=0)
    if user_rating > 0:
        # Add the rating and save it
        if file_name not in ratings:
            ratings[file_name] = []
        ratings[file_name].append(user_rating)
        with open("ratings.json", "w") as f:
            json.dump(ratings, f)
        st.success(f"Your rating for {file_name} has been recorded!")

import streamlit as st
import pandas as pd
import pickle
from downloader import download_file_from_google_drive

st.title("Welcome to Smartphone Recommender System")

# Downloading similarity matrix from google drive
download_file_from_google_drive("1HmW__R9xvVsp9xYV9gEe7EmerVr743nQ", "similarity_matrix.pkl")

with open("phones_with_image_path.pkl", "rb") as file:
    df = pickle.load(file)
with open("similarity_matrix.pkl", "rb") as file:
    similarity_matrix = pickle.load(file)


def recommend(smartphone):
    idx = df[df['name'].str.lower() == smartphone.lower()].index[0]
    similarity_scores = similarity_matrix[idx]
    similarity_scores = sorted(list(enumerate(similarity_scores)), key=lambda x: x[1], reverse=True)
    top_indices = [similar[0] for similar in similarity_scores[:6]]
    recommended_phones = df.loc[
        top_indices, ['name', 'link', 'price', 'ram_gb', 'rom_gb', 'rear_primary_mp', 'front_primary_mp', 'image_path']]
    return recommended_phones


phone_names_list = df['name'].unique()
phone_name = st.selectbox("Enter the name of the smartphone", phone_names_list)
similar_phones = recommend(phone_name)

if st.button("Recommend"):
    for i in range(0, len(similar_phones), 2):
        cols = st.columns(2)
        for j in range(2):
            row = similar_phones.iloc[i + j]
            with cols[j]:
                st.markdown(f"### {row['name']}")
                # st.image(row['image_path'], width = 150)
                st.markdown(f"""
                <a href = "{row['link']}" target = "_blank">
                    <img src = "{row['image_path']}" width = "150">
                </a>
                """, unsafe_allow_html=True)
                st.markdown(f"""
                - 💰 **Price:** ₹{int(row['price'])}
                - 🧠 **RAM:** {row['ram_gb']} GB
                - 💾 **ROM:** {row['rom_gb']} GB
                - 🔋 **Rear Primary Camera:** {float(row['rear_primary_mp'])} MP
                - 📱 **Front Primary Camera:** {float(row['front_primary_mp'])} MP
                """)
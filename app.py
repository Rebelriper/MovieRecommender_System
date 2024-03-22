import pickle 
import streamlit as st
import requests
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Custom CSS for styling
css = """
<style>
body {
    background-image: url('https://tse3.mm.bing.net/th?id=OIP.6bFWZyRfx79-GqDgNwI3yAHaEK&pid=Api&P=0&h=180');
    background-size: cover;
    background-repeat: no-repeat;
    color: #fff; /* Text color */
    font-family: Arial, sans-serif;
}
.container {
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
}
h1 {
    color: #fff; /* Header color */
    text-align: center;
}
.movie-list {
    list-style-type: none;
    padding: 0;
}
.movie-list li {
    margin-bottom: 10px;
}
.movie-name {
    font-size: 1.2em;
    font-weight: bold;
}
.movie-poster {
    max-width: 100%;
    height: auto;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.3); /* Shadow effect */
}
</style>

"""

# Display custom CSS
st.markdown(css, unsafe_allow_html=True)



# Load data
dt = pd.read_csv('Movies_dataset.csv')
movies = pickle.load(open('artifacts/movie_name.pkl','rb'))
similarity = pickle.load(open('artifacts/similarity.pkl','rb'))

# Function to fetch movie poster
def fetch_poster(title):
    url = "https://www.omdbapi.com/?t={}&apikey=39c59a65".format(title)
    response = requests.get(url)
    data = response.json()
    if 'Poster' in data:
        poster_url = data['Poster']
    else:
        poster_url = 'https://via.placeholder.com/150'  # Default placeholder image
    return poster_url

# Function to recommend movies
def recommend(title):
    df = dt[dt['title'].str.lower() == title.lower()]
    if df.empty:
        return "Movie not found", None
    idx = df.index[0]
    sim_scores = list(enumerate(similarity[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:6]
    movie_indices = [i[0] for i in sim_scores]
    recommended_movies = dt['title'].iloc[movie_indices].values
    poster_urls = [fetch_poster(dt['title'].iloc[idx]) for idx in movie_indices]  # Use movie_indices here
    return recommended_movies, poster_urls

# Display the movie list
st.title("Movie Recommender System")
selected_movie = st.selectbox('Select a movie to get recommendations', movies)
if st.button('Recommend'):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie)
    st.markdown('## Recommended Movies:')
    col1, col2, col3, col4, col5 = st.columns(5)
    for i in range(5):
        with eval(f"col{i+1}"):
            st.image(recommended_movies_poster[i], width=150, caption=recommended_movies_name[i])

import pickle
import streamlit as st
import pandas as pd
import requests


def fetch_poster(id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{id}?api_key=1a2edcecce984f0f3496b2fbadb4b4e8&language=en-US')
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"  # Placeholder image if no poster is found


def recommend(movie):
    movie_index = movies[movies['original_title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movie_poster = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]]['original_title'])
        recommended_movie_poster.append(fetch_poster(movie_id))
    
    return recommended_movies, recommended_movie_poster


st.title('Movie Recommender System')

# Load data
movies_dict = pickle.load(open('C:\\Users\\HP\\Desktop\\movie recommendation\\movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('C:\\Users\\HP\\Desktop\\movie recommendation\\similarity.pkl', 'rb'))

# Movie selection
selected_movie_name = st.selectbox(
    'Select a movie to get recommendations:',
    movies['original_title'].values
)

# Show recommendations
if st.button('Show Recommendations'):
    names, posters = recommend(selected_movie_name)
    
    cols = st.columns(5)
    for i, col in enumerate(cols):
        with col:
            st.text(names[i])
            st.image(posters[i])

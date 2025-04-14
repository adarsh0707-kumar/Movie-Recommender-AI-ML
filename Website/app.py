import streamlit as st
import pickle
import requests



def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=a7dda73ba27d7681335c73730e9a646a&language=en-US'
    )
    data = response.json()

    # Safe access to poster_path
    poster_path = data.get('poster_path')

    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        # Return a placeholder image if no poster is found
        return "https://via.placeholder.com/500x750?text=No+Image+Available"



def recommend(movie):
  movie_index = movies[movies['title'] == movie].index[0]
  distances = cosine[movie_index]
  movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

  recommended_movies = []
  recommended_movies_poster = []

  for i in movies_list:

    movie_id = movies.iloc[i[0]]['id']
    

    recommended_movies.append(movies.iloc[i[0]].title)

    # fetch poster from api
    recommended_movies_poster.append(fetch_poster(movie_id))

  return recommended_movies, recommended_movies_poster

movies = pickle.load(open('../movie_dict.pkl', 'rb'))
movies_list = movies['title'].values
cosine = pickle.load(open('../similarity.pkl', 'rb'))




st.title("Movie Recommendation System")

selected_movie_name = st.selectbox(
    'Select a movie:',
    movies_list
)

if st.button('Recommend'):
  
  names, posters = recommend(selected_movie_name)
  
  col1, col2, col3, col4, col5 = st.columns(5)
  with col1:
    st.text(names[0])
    st.image(posters[0])
  with col2:  
    st.text(names[1])
    st.image(posters[1])
  with col3:
    st.text(names[2])
    st.image(posters[2])
  with col4:
    st.text(names[3])
    st.image(posters[3])
  with col5:
    st.text(names[4])
    st.image(posters[4])
  st.text("Recommended Movies:")  


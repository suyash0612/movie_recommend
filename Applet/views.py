from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import pandas as pd
import numpy as np
import json , requests
import urllib.request, json 



# Create your views here.
def index(request):
    return render(request,'home.html')

def test(request):
    try:
        global title_copy
        title = request.GET.get('name')
        title = "+".join( title.split() )
        api_key = 'http://www.omdbapi.com/?t='+str(title)+'&apikey=30b15bb0'
        with urllib.request.urlopen(api_key) as url:
            data = json.loads(url.read().decode())
        df = pd.DataFrame(data)
        Title = df['Title'][0]
        Year = df['Year'][0]
        Rated = df['Rated'][0]
        Released = df['Released'][0]
        Runtime = df['Runtime'][0]
        Genre = df['Genre'][0]
        Director = df['Director'][0]
        Writer = df['Writer'][0]
        Actors = df['Actors'][0]
        Plot = df['Plot'][0]
        Language = df['Language'][0]
        Country = df['Country'][0]
        Awards = df['Awards'][0]
        Poster = df['Poster'][0]
        Ratings = df['Ratings'][0]
        Metascore = df['Metascore'][0]
        imdbRating = df['imdbRating'][0]
        imdbVotes = df['imdbVotes'][0]
        imdbID = df['imdbID'][0]
        Type = df['Type'][0]
        BoxOffice = df['BoxOffice'][0]
        Production = df['Production'][0]
        Response = df['Response'][0]


        title_copy = Title
        # reviews_url = 'https://www.imdb.com/title/'+str(imdbID)+'/'
        # page=requests.get(reviews_url)
        # soup = BeautifulSoup(page.content, 'html.parser')
        # results = soup.find('div',class_ = 'slate_wrapper')
        # img=results.find('img')
        # img=img.get('src')

        global params
        params = {}
        
        
        params = {'Title':Title, 'Year':Year, 'Rated':Rated, 'Released':Released, 'Runtime':Runtime, 'Genre':Genre, 'Director':Director,
        'Writer':Writer, 'Actors':Actors, 'Plot':Plot, 'Language':Language, 'Country':Country, 'Awards':Awards, 'Poster':Poster,
        'Ratings':Ratings, 'Metascore':Metascore, 'imdbRating':imdbRating, 'imdbVotes':imdbVotes, 'imdbID':imdbID, 'Type':Type,
        'BoxOffice':BoxOffice, 'Production':Production,  'Response':Response ,'Poster':Poster}
        return render(request,'index.html',params)

    except (ValueError, TypeError):
        params = params = {'Title':"Sorry we could not find the movie..... :("}
        return render(request,'duplicate.html',params)

def request_data(request):
    import os
    from bs4 import BeautifulSoup
    try:
        reviews_url = 'https://www.imdb.com/title/'+params['imdbID']+'/reviews'
        page=requests.get(reviews_url)
        soup = BeautifulSoup(page.content, 'html.parser')
        results = soup.find(class_ = 'lister-list')
        review=results.findAll('div',class_='text show-more__control')
        review_result = [r.text for r in review]
        context = {'review_result':review_result}
    except urllib.error.HTTPError as exc:
        content = exc.read()
        print(content)
        time.sleep(1) # wait 10 seconds and then make http request again

    return render(request,'review.html',context)


   
def request_choice(request):
    import pandas as pd 
    import numpy as np 
    df2 = pd.read_csv('static/data.csv')

    from sklearn.feature_extraction.text import TfidfVectorizer

    #Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
    tfidf = TfidfVectorizer(stop_words='english')

    #Replace NaN with an empty string
    df2['overview'] = df2['overview'].fillna('')

    #Construct the required TF-IDF matrix by fitting and transforming the data
    tfidf_matrix = tfidf.fit_transform(df2['overview'])

    #Output the shape of tfidf_matrix
    tfidf_matrix.shape

    from sklearn.metrics.pairwise import linear_kernel

    # Compute the cosine similarity matrix
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(df2.index, index=df2['title']).drop_duplicates()

    def get_recommendations(title, cosine_sim=cosine_sim):
        # Get the index of the movie that matches the title
        idx = indices[title]

        # Get the pairwsie similarity scores of all movies with that movie
        sim_scores = list(enumerate(cosine_sim[idx]))

        # Sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the 10 most similar movies
        sim_scores = sim_scores[1:11]

        # Get the movie indices
        movie_indices = [i[0] for i in sim_scores]

        # Return the top 10 most similar movies
        return df2['title'].iloc[movie_indices]

    def get_recommendations(title, cosine_sim=cosine_sim):
        # Get the index of the movie that matches the title
        idx = indices[title]

        # Get the pairwsie similarity scores of all movies with that movie
        sim_scores = list(enumerate(cosine_sim[idx]))

        # Sort the movies based on the similarity scores
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

        # Get the scores of the 10 most similar movies
        sim_scores = sim_scores[1:11]

        # Get the movie indices
        movie_indices = [i[0] for i in sim_scores]

        # Return the top 10 most similar movies
        return df2['title'].iloc[movie_indices]

    from ast import literal_eval

    features = ['cast', 'crew', 'keywords', 'genres']
    for feature in features:
        df2[feature] = df2[feature].apply(literal_eval)

    def get_director(x):
        for i in x:
            if i['job'] == 'Director':
                return i['name']
        return np.nan

    def get_list(x):
        if isinstance(x, list):
            names = [i['name'] for i in x]
            #Check if more than 3 elements exist. If yes, return only first three. If no, return entire list.
            if len(names) > 3:
                names = names[:3]
            return names

        #Return empty list in case of missing/malformed data
        return []

    df2['director'] = df2['crew'].apply(get_director)

    features = ['cast', 'keywords', 'genres']
    for feature in features:
        df2[feature] = df2[feature].apply(get_list)

    def clean_data(x):
        if isinstance(x, list):
            return [str.lower(i.replace(" ", "")) for i in x]
        else:
            #Check if director exists. If not, return empty string
            if isinstance(x, str):
                return str.lower(x.replace(" ", ""))
            else:
                return ''

    features = ['cast', 'keywords', 'director', 'genres']

    for feature in features:
        df2[feature] = df2[feature].apply(clean_data)

    def create_soup(x):
        return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])
    df2['soup'] = df2.apply(create_soup, axis=1)

    from sklearn.feature_extraction.text import CountVectorizer

    count = CountVectorizer(stop_words='english')
    count_matrix = count.fit_transform(df2['soup'])

    from sklearn.metrics.pairwise import cosine_similarity

    cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

    df2 = df2.reset_index()
    indices = pd.Series(df2.index, index=df2['title'])
    l=[]
    try:
       l =[i for i in  get_recommendations(str(title_copy), cosine_sim2)]
    except(KeyError):
        l= ['sorry we are facing issues :(']
        print(l)
        

    movies = {'l':l}
    return render(request,'choice.html',movies) 
    
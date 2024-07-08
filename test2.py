from flask import Flask, request, jsonify, render_template
import numpy as np
import pandas as pd
import pickle
import streamlit as st

popular_df = pickle.load(open('popular.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
pt = pickle.load(open('pt.pkl', 'rb'))
app = Flask(__name__)

@app.route('/')
def index():
    #  value = list(popular_df['avg_rating'].values)
    #  float_value = float(value)  # Convert to float
    #  rounded_value = round(float_value, 1) 
    return render_template('index.html',
                           book_name = list(popular_df['book_title'].values),
                           author=list(popular_df['book_author'].values),
                           image=list(popular_df['image_url_m'].values),
                           votes=list(popular_df['num_ratings'].values),
                          
                           
                           rating=list(popular_df['avg_rating'].values)

                           )

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    query = request.args.get('query')
    suggestions = list(pt.index[pt.index.str.contains(query, case=False, na=False)])
    return jsonify(suggestions)

@app.route('/rec1')
def recommend_ui():
    return render_template('rec1.html')

@app.route('/recommend_books', methods=['POST'])
def recommend():
    user_input = request.form.get('user_input')
    
    if user_input in pt.index:
        index = np.where(pt.index == user_input)[0][0]
        similar_items = sorted(list(enumerate(similarity_scores[index])), key=lambda x: x[1], reverse=True)[1:9]
        
        data = []
        for i in similar_items:
            item = []
            temp_df = books[books['book_title'] == pt.index[i[0]]]
            item.extend(list(temp_df.drop_duplicates('book_title')['book_title'].values))
            item.extend(list(temp_df.drop_duplicates('book_title')['book_author'].values))
            item.extend(list(temp_df.drop_duplicates('book_title')['image_url_m'].values))
            
            data.append(item)
        
        return render_template('rec1.html', data=data)
    else:
        return render_template('rec1.html', data=None)

if __name__ == '__main__':
    app.run(debug=True)

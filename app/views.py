# views.py


from flask import Flask, flash, redirect, render_template, request,\
    session, url_for
from functools import wraps
from speech.locate_word import run_word_loc, get_words, locate_keywords
import os

app = Flask(__name__)
app.config.from_object('config')



@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'GET':
        return render_template('index.html')
    if request.method == 'POST':
        empty_results = False
        youtube_url = request.form['youtube_url']
        keyword = request.form['keyword']
        if 'example.json' in os.listdir('speech/'): 
            times = locate_keywords(get_words('speech/example.json'), [keyword]) 
        else:
            times = run_word_loc(youtube_url, app.config['SPEECHMATICS_API_KEY'], [keyword]) 
        youtube_urls = [youtube_url.replace('watch?v=', 'embed/') + "?start=" + str(time_loc + 5) for time_loc in times]
        if not youtube_urls:
            empty_results = True 
        return render_template('youtube_embed.html', 
            youtube_urls=youtube_urls,
            keyword=keyword,
            empty_results=empty_results)

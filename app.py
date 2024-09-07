#!/usr/bin/env python3
from flask import Flask, jsonify, render_template, request
from hebrew_letters_frequency import HebrewLetterCounter
from urllib.parse import urlparse

app = Flask(__name__)

_cache = {}


def validate_and_format_url(url):
    parsed_url = urlparse(url)

    if url == '':
        raise Exception('Empty URL')

    if not parsed_url.scheme:
        url = 'http://' + url
        parsed_url = urlparse(url)

    if parsed_url.scheme not in ['http', 'https']:
        raise Exception("Only HTTP and HTTPS are supported")

    return url

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/count_letters', methods=['POST'])
def do_count_letters():
    try:
        url = validate_and_format_url(request.form['url'])
    except:
        return jsonify({'error': 'Check the URL'}), 400

    if url in _cache:
        return jsonify({'output': _cache[url]})

    try:
        counter = HebrewLetterCounter()
        output = counter.count_letters(url)
    except:
        return jsonify({'error': 'Bad URL or network error'}), 500

    _cache[url] = output
    return jsonify({'output': output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

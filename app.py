from flask import Flask, jsonify, render_template, request
from hebrew_letters_frequency import count_letters

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/count_letters', methods=['POST'])
def do_count_letters():
    try:
        url = request.form['url']
        if url == '':
            raise Exception('Empty URL')
    except:
        return jsonify({'error' : 'Check the URL'}), 400

    try:
        output = count_letters(url)
    except:
        return jsonify({'error' : 'Bad URL or network error'}), 500

    return jsonify({'output': output})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
from flask import Flask, render_template, request
from database import init_db
from recommender import get_recommendations

app = Flask(__name__)

# Initialise database on startup
with app.app_context():
    init_db()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/recommend', methods=['POST'])
def recommend():
    topic = request.form.get('topic', '').strip()
    difficulty = request.form.get('difficulty', 'All')

    if not topic:
        return render_template('index.html', error="Please enter a topic.")

    results = get_recommendations(topic, difficulty_filter=difficulty, top_n=5)
    return render_template('results.html', results=results, topic=topic, difficulty=difficulty)

if __name__ == '__main__':
    app.run(debug=True)
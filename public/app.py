import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

leaderboard = []
public_shaming = []

@app.route('/')
def index():
    # Renders the index.html template in 'templates' folder
    return render_template('index.html')

@app.route('/get_data', methods=['GET'])
def get_data():
    # Returns the current leaderboard and public_shaming lists
    return jsonify({
        'leaderboard': leaderboard,
        'public_shaming': public_shaming
    })

@app.route('/start_game', methods=['POST'])
def start_game():
    # Generate a random delay between 3 and 10 seconds
    delay = random.randint(3, 10)
    return jsonify({"delay": delay})

@app.route('/record_time', methods=['POST'])
def record_time():
    data = request.json
    name = data.get('name')
    reaction_time = data.get('reaction_time')

    if name and reaction_time is not None:
        leaderboard.append({'name': name, 'reaction_time': reaction_time})
        # Sort the leaderboard ascending by reaction_time
        leaderboard.sort(key=lambda x: x['reaction_time'])
        # Keep only the top 10 times
        leaderboard[:] = leaderboard[:10]

    # Return the updated leaderboard
    return jsonify({'leaderboard': leaderboard})

@app.route('/too_early', methods=['POST'])
def too_early():
    data = request.json
    name = data.get('name')

    if name:
        public_shaming.append(name)

    # Return the updated public_shaming list
    return jsonify({'public_shaming': public_shaming})

if __name__ == '__main__':
    app.run(debug=True)

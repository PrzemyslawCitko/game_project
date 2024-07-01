from flask import Flask, request, render_template, jsonify
from waitress import serve

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('map.html')



@app.route('/clicked', methods=['POST'])
def clicked():
    data = request.json
    if data is None:
        return jsonify({'status': 'error', 'message': 'No JSON data received'}), 400
    
    country = data.get('country')
    if country is None:
        return jsonify({'status': 'error', 'message': 'No country provided'}), 400
    
    print(f'Clicked country: {country}')
    return jsonify({'status': 'success', 'country': country})

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
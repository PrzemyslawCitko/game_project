from flask import Flask, request, render_template, jsonify
from waitress import serve
from calculation import load_coordinates, draw_capital, create_distances, find_closest_capital


app = Flask(__name__)



coordinates = load_coordinates()
drawn_capital = draw_capital(coordinates)
distances = create_distances(drawn_capital, coordinates)
closest = find_closest_capital(distances)
exclude_countries = [drawn_capital.country]
game_over = False


@app.route('/')
def index():
    return render_template('map.html', drawn_capital=drawn_capital.country)


@app.route('/clicked', methods=['POST'])
def clicked():
    global distances, closest, game_over

    if game_over:
        return jsonify({'status': 'failure'}), 400

    data = request.json
    country = data.get('country')
    if country == closest.another_country:
        print('OK')
        exclude_countries.append(country)
        next_country = next((c for c in coordinates if c.country == closest.another_country), None)
        if next_country:
            distances = create_distances(next_country, coordinates, exclude_countries)
            if not distances:
                print('You won!')
                game_over = True
            else:
                closest = find_closest_capital(distances)
    else:
        print('Wrong answer.')
        game_over = True

    return jsonify({'status': 'success', 'country': country})
    
    
if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)
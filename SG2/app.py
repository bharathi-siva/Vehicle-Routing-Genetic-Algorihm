from flask import Flask, render_template, request, redirect, url_for, session
import pandas as pd
from vrplatlon import calculate_optimal_route

app = Flask(__name__)
app.secret_key = 'your_secret_key'
users = {'user': 'password'}

@app.route('/')
def home():
    if 'username' in session:
        return render_template('home.html')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'admin':
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return 'Invalid credentials'
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/calculate', methods=['POST'])
@app.route('/calculate', methods=['POST'])
def calculate():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    file = request.files['file']
    depot_id = request.form['depot_id']
    if file and depot_id:
        df = pd.read_excel(file)
        best_route, best_distance, best_fitness = calculate_optimal_route(df, depot_id)
        return render_template('result.html', best_route=best_route, best_distance=best_distance, best_fitness=best_fitness)
    return 'No file uploaded or depot ID provided', 400



if __name__ == '__main__':
    app.run(debug=True)




# import folium
# from flask import Flask, render_template, request, redirect, url_for, session
# import pandas as pd
# from vrplatlon import calculate_optimal_route

# app = Flask(__name__)
# app.secret_key = 'your_secret_key'
# users = {'user': 'password'}

# @app.route('/')
# def home():
#     if 'username' in session:
#         return render_template('home.html')
#     return redirect(url_for('login'))

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         if username == 'admin' and password == 'admin':
#             session['username'] = username
#             return redirect(url_for('home'))
#         else:
#             return 'Invalid credentials'
#     return render_template('login.html')

# @app.route('/logout')
# def logout():
#     session.pop('username', None)
#     return redirect(url_for('login'))

# @app.route('/calculate', methods=['POST'])
# @app.route('/calculate', methods=['POST'])
# @app.route('/uploader', methods=['GET', 'POST'])
# def uploader_file():
#     if request.method == 'POST':
#         f = request.files['file']
#         df = pd.read_excel(f)
#         depot_id = df['CustomerId'][0]  # Assuming the first entry is the depot
#         best_route, best_distance, best_fitness, route_coords, route_names = calculate_optimal_route(df, depot_id)
        
#           # Create map using Folium
#         m = folium.Map(location=route_coords[0], zoom_start=13)
#         folium.Marker(location=route_coords[0], popup=f'Depot: {route_names[0]}', icon=folium.Icon(color='green')).add_to(m)
        
#         for coord, name in zip(route_coords[1:-1], route_names[1:-1]):
#             folium.Marker(location=coord, popup=name, icon=folium.Icon(color='blue')).add_to(m)
        
#         folium.Marker(location=route_coords[-1], popup=f'Depot: {route_names[-1]}', icon=folium.Icon(color='red')).add_to(m)
#         folium.PolyLine(locations=route_coords, color='blue').add_to(m)
        
#         map_html = m._repr_html_()
        
#         return render_template('result.html', best_route=best_route, best_distance=best_distance, best_fitness=best_fitness, map_html=map_html)


# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request
from sqlalchemy import create_engine
import pandas as pd


app = Flask(__name__)

# Connect to the SQLite database
engine = create_engine('sqlite:///imdb_data_exercise.db')

@app.route('/', methods=['GET'])
def index(): 
    return render_template('index.html')

# Route to handle the search form submission
@app.route('/results', methods=['POST'])
def results():
    movies = []
    if request.method == 'POST':
        search_ = request.form.get('content', ' ').strip() # Default to a space if no input is provided and strip whitespace

        query = """
        SELECT Movie.title, Genre.name AS genre, Movie.year, Movie.rating, Country.name AS country, Person.name AS director, p.name AS actor
        FROM Movie
        JOIN M_Genre ON Movie.MID = M_Genre.MID
        JOIN Genre ON M_Genre.GID = Genre.GID  
        JOIN M_Country ON Movie.MID = M_Country.MID
        JOIN Country ON M_Country.CID = Country.CID 
        JOIN M_Director ON Movie.MID = M_Director.MID
        JOIN Person ON M_Director.PID = Person.PID     
        JOIN m_cast mc  ON trim(mc.mid) = Movie.mid
        JOIN person p   ON p.pid = trim(mc.pid)
        WHERE Movie.title LIKE ?
        OR Genre.name LIKE ?
        OR Country.name LIKE ?
        OR Person.name LIKE ?
        OR p.name LIKE ?
        GROUP BY movie.mid
        ORDER BY Movie.rating DESC;
        """
        # prepare the filters for the sql query
        filters = [f"%{search_}%", f"%{search_}%", f"%{search_}%", f"%{search_}%", f"%{search_}%"] 
        df = pd.read_sql_query(query, engine, params=(filters[0], filters[1], filters[2], filters[3], filters[4])) 
        movies = df.to_dict(orient='records')
        print(movies)
    
    # render the results template with the movies data
    return render_template('results.html', movies=movies)
 
# runs the app in debug mode
if __name__ == '__main__':
    app.run(debug=True)

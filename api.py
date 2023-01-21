import sqlite3
from flask import Flask, request, jsonify

app = Flask(__name__)

# Connect to the database
conn = sqlite3.connect("movies.db", check_same_thread=False)
cursor = conn.cursor()

# Create the movies table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS movies
                  (id INTEGER PRIMARY KEY, name TEXT, year INTEGER, genre TEXT)''')

# Get all movies
@app.route("/movies", methods=["GET"])
def get_all_movies():
    cursor.execute("SELECT * FROM movies")
    movies = cursor.fetchall()
    return jsonify(movies)

# Get movie by id
@app.route("/movies/<int:id>", methods=["GET"])
def get_movie(id):
    cursor.execute("SELECT * FROM movies WHERE id=?", (id,))
    movie = cursor.fetchone()
    return jsonify(movie) if movie else jsonify({"error": "Movie not found"}), 404

# Add a new movie
@app.route("/movies", methods=["POST"])
def add_movie():
    movie = request.get_json()
    cursor.execute("INSERT INTO movies (name, year, genre) VALUES (?,?,?)",
                   (movie["name"], movie["year"], movie["genre"]))
    conn.commit()
    return jsonify(movie), 201

# Update movie
@app.route("/movies/<int:id>", methods=["PUT"])
def update_movie(id):
    movie = request.get_json()
    cursor.execute("UPDATE movies SET name=?, year=?, genre=? WHERE id=?",
                   (movie["name"], movie["year"], movie["genre"], id))
    conn.commit()
    return jsonify(movie)

# Delete movie
@app.route("/movies/<int:id>", methods=["DELETE"])
def delete_movie(id):
    cursor.execute("DELETE FROM movies WHERE id=?", (id,))
    conn.commit()
    return jsonify({"message": "Movie has been deleted"})

if __name__ == "__main__":
    app.run()

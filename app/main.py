import csv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:5500"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins="*",
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["Content-Type"],
)

def read_csv_file(file_path):
    with open(file_path, mode="r", encoding="utf-8") as file:
        csv_reader = csv.DictReader(file)
        movies = [row for row in csv_reader]
    return movies


@app.get("/list_all_movies")
async def get_movies(
    name: str = None,
    min_point: float = None,
    max_point: float = None,
    min_year: float = None,
    max_year: float = None
):
    file_path = "./data/movies.csv"
    movies = read_csv_file(file_path)

    filtered_movies = []

    for movie in movies:
        if name and name.lower() not in movie['Name'].lower():
            continue
        if min_point and float(movie['Point']) < min_point:
            continue
        if max_point and float(movie['Point']) > max_point:
            continue
        if min_year and float(movie['Year']) < min_year:
            continue
        if max_year and float(movie['Year']) > max_year:
            continue
        filtered_movies.append(movie)

    return filtered_movies

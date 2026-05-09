#!/usr/bin/env python3
"""
Simple Movie Finder - Search movies using TMDB API.
"""

import sys
import requests

# TMDB base URL
BASE_URL = "https://api.themoviedb.org/3"

def search_movies(api_key, query):
    """Search for movies by title."""
    url = f"{BASE_URL}/search/movie"
    params = {
        "api_key": api_key,
        "query": query,
        "language": "en-US"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        sys.exit(1)

def get_movie_details(api_key, movie_id):
    """Get full details for a specific movie."""
    url = f"{BASE_URL}/movie/{movie_id}"
    params = {
        "api_key": api_key,
        "language": "en-US"
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        sys.exit(1)

def display_results(results, query):
    """Show search results."""
    total = results.get("total_results", 0)
    if total == 0:
        print(f"No movies found for '{query}'.")
        return
    print(f"\nFound {total} movies for '{query}':\n")
    for idx, movie in enumerate(results.get("results", [])[:10], start=1):  # limit to 10
        title = movie.get("title", "Unknown")
        year = movie.get("release_date", "")[:4]
        rating = movie.get("vote_average", 0)
        print(f"{idx}. {title} ({year}) - Rating: {rating}")

def display_details(movie):
    """Show detailed info for a movie."""
    print("\n" + "=" * 60)
    print(f"Title: {movie.get('title')}")
    print(f"Release Date: {movie.get('release_date', 'Unknown')}")
    print(f"Rating: {movie.get('vote_average')}/10 ({movie.get('vote_count')} votes)")
    print(f"Runtime: {movie.get('runtime', 'Unknown')} minutes")
    genres = [g["name"] for g in movie.get("genres", [])]
    print(f"Genres: {', '.join(genres) if genres else 'N/A'}")
    print(f"Overview: {movie.get('overview', 'No overview.')}")
    print("=" * 60)

def main():
    # Get API key from command line or environment
    api_key = None
    if len(sys.argv) > 1 and sys.argv[1] == "--apikey" and len(sys.argv) > 2:
        api_key = sys.argv[2]
        sys.argv = sys.argv[3:]  # remove the --apikey and its value
    else:
        import os
        api_key = os.environ.get("TMDB_API_KEY")

    if not api_key:
        print("Please provide your TMDB API key:")
        print("  Option 1: export TMDB_API_KEY='your_key'")
        print("  Option 2: python movie_finder.py --apikey YOUR_KEY --search 'Inception'")
        sys.exit(1)

    # Simple argument parsing
    if len(sys.argv) < 3:
        print("Usage:")
        print("  Search:  python movie_finder.py --search 'movie title'")
        print("  Details: python movie_finder.py --id 12345")
        sys.exit(1)

    if sys.argv[1] == "--search":
        query = " ".join(sys.argv[2:])
        results = search_movies(api_key, query)
        display_results(results, query)
    elif sys.argv[1] == "--id" and len(sys.argv) == 3:
        movie_id = int(sys.argv[2])
        details = get_movie_details(api_key, movie_id)
        display_details(details)
    else:
        print("Invalid arguments. Use --search or --id")

if __name__ == "__main__":
    main()

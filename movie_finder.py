import sys
import requests

API_KEY = "your_api_key_here"   # <-- CHANGE THIS
BASE_URL = "https://api.themoviedb.org/3"

def search_movies(query):
    resp = requests.get(f"{BASE_URL}/search/movie", params={"api_key": API_KEY, "query": query})
    resp.raise_for_status()
    return resp.json()

def show_results(data, query):
    total = data.get("total_results", 0)
    if total == 0:
        print(f"No movies found for '{query}'.")
        return
    print(f"\nFound {total} movies for '{query}':\n")
    for i, m in enumerate(data["results"][:10], 1):
        print(f"{i}. {m['title']} ({m.get('release_date','')[:4]}) - ⭐ {m['vote_average']}")

def movie_details(movie_id):
    resp = requests.get(f"{BASE_URL}/movie/{movie_id}", params={"api_key": API_KEY})
    resp.raise_for_status()
    m = resp.json()
    print("\n" + "="*60)
    print(f"Title: {m['title']}\nReleased: {m.get('release_date','Unknown')}\nRating: {m['vote_average']}/10\nRuntime: {m.get('runtime','?')} min\nGenres: {', '.join([g['name'] for g in m.get('genres',[])])}\n\nOverview: {m.get('overview','No overview.')}")
    print("="*60)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:\n  python movie_finder.py --search 'Movie Name'\n  python movie_finder.py --id 12345")
        sys.exit(1)
    if sys.argv[1] == "--search":
        show_results(search_movies(" ".join(sys.argv[2:])), sys.argv[2])
    elif sys.argv[1] == "--id":
        movie_details(int(sys.argv[2]))

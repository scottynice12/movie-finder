import requests

BASE_URL = "https://imdb.iamidiotareyoutoo.com"

def search_movies(query):
    url = f"{BASE_URL}/search?q={query.replace(' ', '+')}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"\nError: {e}")
        print("The free API might be busy. Try again in a few seconds.\n")
        return None

def display_movies(data, query):
    if not data or 'description' not in data:
        print(f"\nNo movies found for '{query}'. Try a different title.\n")
        return

    results = data.get('description', [])
    if not results:
        print(f"\nNo movies found for '{query}'.\n")
        return

    print(f"\nFound {len(results)} results for '{query}':\n")
    for i, movie in enumerate(results[:10]):
        title = movie.get("#TITLE", "Unknown")
        year = movie.get("#YEAR", "N/A")
        imdb_id = movie.get("#IMDB_ID", "N/A")
        print(f"{i+1}. {title} ({year}) - IMDB ID: {imdb_id}")

def get_movie_details(imdb_id):
    url = f"{BASE_URL}/search?q={imdb_id}"
    try:
        res = requests.get(url)
        return res.json()
    except Exception:
        return None

def display_details(movie_data):
    if not movie_data or 'short' not in movie_data:
        print("Could not retrieve details for that ID. Try again.\n")
        return
    m = movie_data['short']
    print("\n" + "="*70)
    print(f"Title: {m.get('name', 'N/A')}")
    print(f"Year: {m.get('dateCreated', {}).get('value', 'N/A')[:4]}")
    print(f"Rating: {m.get('aggregateRating', {}).get('ratingValue', 'N/A')}/10")
    genres = m.get('genre', [])
    print(f"Genres: {', '.join(genres) if genres else 'N/A'}")
    print(f"Overview: {m.get('description', 'No description available.')[:500]}...")
    print("="*70 + "\n")

def main():
    print("\nWelcome to the Movie Finder!")
    while True:
        print("\nMain Menu:")
        print("1. Search for a movie")
        print("2. Get movie details by IMDB ID")
        print("3. Exit")
        choice = input("Choose (1/2/3): ").strip()
        if choice == '1':
            query = input("\nEnter movie title: ").strip()
            if query:
                data = search_movies(query)
                display_movies(data, query)
            else:
                print("Please enter a title.\n")
        elif choice == '2':
            imdb_id = input("\nEnter IMDB ID (e.g., tt1375666 for Inception): ").strip()
            if imdb_id:
                data = get_movie_details(imdb_id)
                display_details(data)
            else:
                print("Please enter a valid ID.\n")
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter 1, 2, or 3.\n")

if __name__ == "__main__":
    main()
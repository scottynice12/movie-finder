# 🎬 Simple Movie Finder

A minimal command-line tool to search movies and get details using [TMDB API](https://www.themoviedb.org/).

## Requirements

- Python 3.6+
- `requests` library (install with `pip install requests`)

## Setup

1. **Get a free API key** from [TMDB](https://www.themoviedb.org/signup) (click your profile → Settings → API → Request an API key).

2. **Set your API key** (choose one method):

   - As environment variable:  
     `export TMDB_API_KEY="your_key_here"` (Linux/macOS)  
     `set TMDB_API_KEY=your_key_here` (Windows CMD)

   - Or pass it each time with `--apikey`:  
     `python movie_finder.py --apikey YOUR_KEY --search "Inception"`

## Usage

### Search for a movie
```bash
python movie_finder.py --search "The Matrix"

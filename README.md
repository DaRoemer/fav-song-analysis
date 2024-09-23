# Analysis of liked Spotify songs
I created this project to help me manage and analyze my liked songs on Spotify using Python. I wanted to investigate  Here, I'll explain how you can do the same using the `LikedSongs.ipynb` Jupyter Notebook.

## Getting Started

### Prerequisites

- Python 3.x
- Jupyter Notebook
- Spotify Developer Account

### Installation

1. Clone my repository:
    ```sh
    git clone https://github.com/DaRoemer/fav-song-analysis.git
    cd fav-song-analysis
    ```

2. Install the required Python packages using conda:
    ```sh
    conda env create -f spotify-env.yml
    ```

3. Open the Jupyter Notebook:
    ```sh
    jupyter notebook LikedSongs.ipynb
    ```

## Configuration

To access Spotify's API, you'll need to set up your credentials. Follow these steps:

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/applications) and log in.
2. Click on "Create an App" and fill in the required details.
3. Once the app is created, you'll get a `Client ID` and `Client Secret`.
4. Create a file named `config.py` in the project directory and add the following content:
    ```python
    SPOTIFY_CLIENT_ID = 'your_client_id'
    SPOTIFY_CLIENT_SECRET = 'your_client_secret'
    SPOTIFY_REDIRECT_URI = 'your_redirect_uri'
    ```

Replace `'your_client_id'`, `'your_client_secret'`, and `'your_redirect_uri'` with your actual Spotify credentials.

## Usage

1. Run the cells in the `LikedSongs.ipynb` notebook to authenticate with Spotify and fetch your liked songs.
2. Analyze and manage your liked songs using the provided functions.

## Contributing

Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.

## Acknowledgments

- [Spotify Web API](https://developer.spotify.com/documentation/web-api/)
- [Spotipy](https://spotipy.readthedocs.io/)

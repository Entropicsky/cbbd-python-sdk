# CFBD Python SDK Demo App

This Streamlit application demonstrates the capabilities of the CFBD Python SDK, providing a user-friendly interface to explore college basketball data through the SDK.

## Features

- Team information and rosters
- Game results and schedules
- Team and player statistics
- Advanced analysis and visualizations
- Rankings and ratings data
- Play-by-play information

## Installation

1. Ensure you have Python 3.8+ installed
2. Install the required packages:

```bash
pip install -r requirements.txt
```

3. You'll also need to install the CFBD Python SDK:

```bash
pip install cfbd-python-sdk
```

## Usage

1. Get an API key from [collegefootballdata.com](https://collegefootballdata.com)
2. Create a `.env` file in the same directory as app.py with the following content:

```
CFBD_API_KEY=your_api_key_here
```

3. Run the Streamlit app:

```bash
streamlit run app.py
```

4. Navigate to the URL displayed in your terminal (typically http://localhost:8501)

## Screenshots

![Home Page](screenshots/home.png)
![Teams Page](screenshots/teams.png)
![Games Page](screenshots/games.png)

## Contributing

Feel free to open issues or submit pull requests to improve the app. 
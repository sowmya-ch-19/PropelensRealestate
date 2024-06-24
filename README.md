# Real Estate Project Finder

This project is designed to find nearby real estate projects and provide detailed descriptions using the Overpass API, OpenStreetMap Nominatim API, and OpenAI's GPT-3.5-turbo model.

## Features

- Find nearby real estate projects based on location and radius
- Fetch detailed project information including name and address
- Generate descriptive summaries of projects using GPT-3.5-turbo

## Prerequisites

- Python 3.x
- Requests library
- OpenAI library

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/real-estate-project-finder.git
    cd real-estate-project-finder
    ```

2. Install the required packages:
    ```bash
    pip install requests openai
    ```

3. Set your OpenAI API key:
    ```python
    openai.api_key = 'your-openai-api-key'
    ```

## Usage

1. Update the latitude, longitude, and radius values in the `main` function at the bottom of the script:
    ```python
    if __name__ == "__main__":
        latitude = 17.3933  # Latitude of Kothapet, Hyderabad
        longitude = 78.3411  # Longitude of Kothapet, Hyderabad
        radius = 2000  # Example radius in meters
        main(latitude, longitude, radius)
    ```

2. Run the script:
    ```bash
    python your_script.py
    ```

3. The script will output the summaries of nearby real estate projects.

## Functions

- `find_nearby_projects(latitude, longitude, radius=1000)`: Finds nearby real estate projects using the Overpass API.
- `fetch_project_details(lat, lon)`: Fetches project details (name and address) using the OpenStreetMap Nominatim API.
- `generate_project_descriptions(projects)`: Generates project descriptions using the GPT-3.5-turbo model.
- `summarize_projects(projects, descriptions)`: Summarizes project information.

## Example

```python
if __name__ == "__main__":
    latitude = 17.3933  # Latitude of Kothapet, Hyderabad
    longitude = 78.3411  # Longitude of Kothapet, Hyderabad
    radius = 2000  # Example radius in meters

    main(latitude, longitude, radius)

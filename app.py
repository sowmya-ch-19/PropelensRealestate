import requests
import openai

# Set your OpenAI API key
openai.api_key = 'your-openai-api-key'


# Function to find nearby real estate projects using Overpass API
def find_nearby_projects(latitude, longitude, radius=1000):
    overpass_url = "http://overpass-api.de/api/interpreter"
    overpass_query = f"""
    [out:json];
    (
      node(around:{radius},{latitude},{longitude})["building"~"apartments|residential|commercial|retail|house|detached|hotel|office|industrial|warehouse|dormitory"];
      way(around:{radius},{latitude},{longitude})["building"~"apartments|residential|commercial|retail|house|detached|hotel|office|industrial|warehouse|dormitory"];
      relation(around:{radius},{latitude},{longitude})["building"~"apartments|residential|commercial|retail|house|detached|hotel|office|industrial|warehouse|dormitory"];
    );
    out center;
    """
    response = requests.get(overpass_url, params={'data': overpass_query})
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError as e:
        print(f"Error decoding JSON response from Overpass API: {e}")
        print("Response content:", response.text)
        return []

    if 'elements' not in data:
        print("No nearby projects found.")
        return []

    nearby_projects = []
    for element in data['elements']:
        if 'tags' in element and 'name' in element['tags']:
            name = element['tags']['name']
            lat = element.get('lat') or (element['center']['lat'] if 'center' in element else None)
            lon = element.get('lon') or (element['center']['lon'] if 'center' in element else None)
            if lat and lon:
                nearby_projects.append({'name': name, 'latitude': lat, 'longitude': lon})

    print("Nearby projects found:", nearby_projects)
    return nearby_projects

# Function to fetch project details (name and address) using OpenStreetMap Nominatim API
def fetch_project_details(lat, lon):
    endpoint = 'https://nominatim.openstreetmap.org/reverse'
    params = {
        'format': 'json',
        'lat': lat,
        'lon': lon,
        'zoom': 18,
    }

    headers = {
        'User-Agent': 'MyRealEstateApp/1.0 (cherukupally.sowmya19@gmail.com)'  # Replace with your application name and email
    }

    response = requests.get(endpoint, params=params, headers=headers)
    try:
        data = response.json()
    except requests.exceptions.JSONDecodeError as e:
        print(f"Error decoding JSON response from Nominatim API: {e}")
        print("Response content:", response.text)
        return None

    if 'error' in data:
        print(f"Error: {data['error']}")
        return None

    name = data.get('display_name', '')
    address = data.get('address', {}).get('suburb', '')  # Customize based on available data

    project_details = {
        'name': name,
        'address': address,
    }
    print("Project details fetched:", project_details)
    return project_details

# Function to generate project descriptions using GPT-3.5-turbo model
def generate_project_descriptions(projects):
    descriptions = []
    for project in projects:
        messages = [
            {"role": "system", "content": "You are a helpful assistant that provides detailed descriptions of real estate projects."},
            {"role": "user", "content": f"Project: {project['name']}. Address: {project['address']}."}
        ]
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            max_tokens=100,
        )
        description = response['choices'][0]['message']['content'].strip()
        descriptions.append(description)
    print("Generated project descriptions:", descriptions)
    return descriptions

# Function to summarize project information
def summarize_projects(projects, descriptions):
    summaries = []
    for i, project in enumerate(projects):
        summary = f"Name: {project['name']}, Address: {project['address']}\nDescription: {descriptions[i]}"
        summaries.append(summary)
    return "\n".join(summaries)

# Main function integrating all functionalities
def main(latitude, longitude, radius=1000):
    # Step 1: Find nearby projects
    nearby_projects = find_nearby_projects(latitude, longitude, radius)
    if not nearby_projects:
        print("No nearby projects found.")
        return

    # Step 2: Fetch details for each nearby project
    detailed_projects = []
    for project in nearby_projects:
        details = fetch_project_details(project['latitude'], project['longitude'])
        if details:
            detailed_projects.append(details)

    # Check if detailed projects are fetched
    if not detailed_projects:
        print("No detailed project information available.")
        return

    # Step 3: Generate project descriptions using GPT-3.5-turbo
    descriptions = generate_project_descriptions(detailed_projects)

    # Step 4: Summarize project information
    summary = summarize_projects(detailed_projects, descriptions)
    print("\nProject Summaries:\n", summary)

# Example usage:
if __name__ == "__main__":
    latitude = 17.3933  # Latitude of Kothapet, Hyderabad
    longitude = 78.3411  # Longitude of Kothapet, Hyderabad
    radius = 2000  # Example radius in meters

    main(latitude, longitude, radius)

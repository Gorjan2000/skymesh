from bs4 import BeautifulSoup
from datetime import datetime


def scrape_soil_parameters(html_code):
    # Create a BeautifulSoup object with the HTML code
    soup = BeautifulSoup(html_code, 'html.parser')

    # Find all the card titles and their corresponding values
    cards = soup.find_all('div', class_='card-body')

    # Initialize a dictionary to store the soil parameters and their values
    soil_parameters = {}

    for card in cards:
        title = card.find('h5', class_='card-title').text.strip()
        value = card.find('h6').text.strip()
        soil_parameters[title] = value

    # Add a timestamp to the soil parameters
    timestamp = datetime.now().strftime('%H:%M:%S %d-%m-%Y')
    soil_parameters['Timestamp'] = timestamp

    return soil_parameters

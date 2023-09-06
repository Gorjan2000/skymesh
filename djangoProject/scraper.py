from bs4 import BeautifulSoup
from datetime import datetime


#
#
# def scrape_soil_parameters(html_code):
#     # Create a BeautifulSoup object with the HTML code
#     soup = BeautifulSoup(html_code, 'html.parser')
#
#     # Find all the card titles and their corresponding values
#     cards = soup.find_all('div', class_='card-body')
#
#     # Initialize a dictionary to store the soil parameters and their values
#     soil_parameters = {}
#
#     # Extracting latitude and longitude
#     latitude_full = soup.select_one(".card-title:contains('Location') + div h6:nth-of-type(1)").text.strip()
#     longitude_full = soup.select_one(".card-title:contains('Location') + div h6:nth-of-type(2)").text.strip()
#     latitude = latitude_full.split(":")[1].strip()
#     longitude = longitude_full.split(":")[1].strip()
#
#     datetime_str = soup.select_one(".card-title:contains('Node ID') + div p.text-dark").text.strip()
#     datetime_obj = datetime.strptime(datetime_str, "Last update:\n%d-%m-%Y %H:%M:%S")
#     formatted_datetime = datetime_obj.strftime("%H:%M %d-%m-%Y")
#
#     for card in cards:
#         title = card.find('h5', class_='card-title').text.strip()
#         value = card.find('h6').text.strip()
#         soil_parameters[title] = value
#
#     soil_parameters["DateTime"] = formatted_datetime
#     soil_parameters["Latitude"] = latitude
#     soil_parameters["Longitude"] = longitude
#
#     return soil_parameters

def scrape_soil_parameters(html_code):
    # Create BeautifulSoup object
    soup = BeautifulSoup(html_code, 'html.parser')

    # Find the specific <ul> element with the ID 'ID1'
    ul_element = soup.find('ul', id='ID1')

    # Initialize an empty dictionary to store the parameters and their values
    soil_parameters = {}

    # Extracting latitude and longitude
    latitude_full = soup.select_one(".card-title:contains('Location') + div h6:nth-of-type(1)").text.strip()
    longitude_full = soup.select_one(".card-title:contains('Location') + div h6:nth-of-type(2)").text.strip()
    latitude = latitude_full.split(":")[1].strip()
    longitude = longitude_full.split(":")[1].strip()

    datetime_str = soup.select_one(".card-title:contains('Node ID') + div p.text-dark").text.strip()
    datetime_obj = datetime.strptime(datetime_str, "Last update:\n%d-%m-%Y %H:%M:%S")
    formatted_datetime = datetime_obj.strftime("%H:%M %d-%m-%Y")

    # Extract the parameter names and values from the <ul> element
    for element in ul_element.find_all('h5', class_='card-title'):
        parameter_name = element.text.strip()
        parameter_value = element.find_next('h6').text.strip()
        soil_parameters[parameter_name] = parameter_value

    soil_parameters["DateTime"] = formatted_datetime
    soil_parameters["Latitude"] = latitude
    soil_parameters["Longitude"] = longitude

    return soil_parameters

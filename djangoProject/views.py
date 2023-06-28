import requests
from django.db import connections
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from djangoProject.scraper import scrape_soil_parameters
from django.shortcuts import render
from .models import *
import json
from django.core.serializers import serialize


def test_connection(request):
    # Get the 'default' database connection
    connection = connections['mysqlFixigo']

    # Test the connection
    try:
        connection.ensure_connection()
        connection_status = "Connection successful!"
    except Exception as e:
        connection_status = f"Connection failed: {str(e)}"

    # Prepare the context data to be passed to the template
    context = {
        'connection_status': connection_status
    }

    # Render the template with the context data
    return render(request, 'test_connection.html', context)


@login_required
@method_decorator(csrf_exempt, name='dispatch')
def index(request):
    url = 'https://eu1.cloud.thethings.network/api/v3/as/applications/ligh-intensity-sensor/devices/eui-2cf7f1c04490006e/packages/storage/uplink_message'
    headers = {
        'Authorization': 'Bearer NNSXS.ZNIKUUYTYSYI7XUIYQQNM63B5FHIVA7QPWTV5SA.KQY7DDVJDZYL4HHR2WHDT7PFMJDMRGAUC6RIFPZCGTGCT2KTXMNQ',
        'Accept': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        json_data = response.text

        latest_received_at = None
        latest_light_intensity = None

        light_intensities = [(json.loads(line)["result"]["uplink_message"]["decoded_payload"].get("lightIntensity"),
                              datetime.strptime(json.loads(line)["result"].get("received_at")[:-4],
                                                '%Y-%m-%dT%H:%M:%S.%f').strftime('%H:%M:%S %d-%m-%Y'))
                             for line in json_data.splitlines() if
                             json.loads(line)["result"]["uplink_message"]["decoded_payload"].get(
                                 "lightIntensity") is not None]

        for value in light_intensities:
            if value[0] and value[1]:
                received_at = datetime.strptime(value[1], '%H:%M:%S %d-%m-%Y')
                if latest_received_at is None or received_at > latest_received_at:
                    latest_received_at = received_at
                    latest_light_intensity = value[0]

        light_intensities = sorted(light_intensities, key=lambda x: datetime.strptime(x[1], '%H:%M:%S %d-%m-%Y'),
                                   reverse=True)

        if latest_received_at is not None or latest_light_intensity is not None:
            context = {
                'latest_light_intensity': latest_light_intensity,
                'latest_received_at': latest_received_at.strftime('%H:%M:%S %d-%m-%Y'),
                'light_intensity': light_intensities
            }
        else:
            context = {

            }

        return render(request, 'index.html', context)

    else:
        error_message = f"Error: {response.status_code}"
        return render(request, 'error.html', {'error_message': error_message})


@login_required
def scrape_view(request):
    # URL of the website to scrape
    url = "http://fixigoweb.somee.com"

    # Send a GET request to the website
    response = requests.get(url)

    if response.status_code == 200:
        # Extract the HTML code from the response
        html_code = response.content

        # Call the scrape_soil_parameters function
        soil_parameters = scrape_soil_parameters(html_code)

        # Pass the parameters to the template
        context = {'soil_parameters': soil_parameters}
        return render(request, 'scrape_template.html', context)
    else:
        # Handle the case when the website is not accessible or returns an error
        error_message = f"Failed to fetch HTML: {response.status_code} {response.reason}"
        return render(request, 'error_template.html', {'error_message': error_message})


def location(request):
    locations = Location.objects.using('mysqlFixigo').all()
    context = {
        'locations': locations
    }
    return render(request, 'location.html', context)


def location_map(request):
    locations = Location.objects.using('mysqlFixigo').all()
    locations_json = serialize('json', locations)
    context = {'locations_json': locations_json}
    return render(request, 'location_map.html', context)

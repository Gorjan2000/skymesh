import requests
import json
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


# @login_required
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

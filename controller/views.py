# Create your views here.

import requests
from django.shortcuts import render
from django.utils.safestring import SafeString

from controller.url_maps import COVID_API, DISTRICT_MAP


def get_key_for_map(data, key):
    if key == 'district':
        return DISTRICT_MAP.get(data.get(key))
    return f'NP.{data.get(key)}'


def build_data(key, value):
    reference = 'x'
    map_for = ['province', 'district', 'municipality']
    if key in map_for:
        reference = 'id'
    response_data = list(
        map(
            lambda x: {
                reference: get_key_for_map(x, key) if key in map_for else x.get(key).title() if x.get(key) else 'Undefined',
                'value': x.get('count') if x.get('count') else 0
            },
            value
        )
    )
    # return json.dumps(response_data)
    return response_data


def get_summary_data_for_province(type_, data):
    response = {}
    for key, value in data.items():
        response.update({
            key: build_data(type_, value)
        })
    return response


def view_home(request, *args, **kwargs):
    covid_data = requests.get(COVID_API.get('summary'))
    context = {}
    for key, value in covid_data.json().items():
        if isinstance(value, dict):
            value = get_summary_data_for_province(
                data=value,
                type_='age' if key == 'age_group' else key
            )
        if isinstance(value, list):
            value = build_data('currentState', value)
        context.update({key: value})
    return render(request, 'controller/home.html', {'ctx': SafeString(context)})

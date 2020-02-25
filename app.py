import requests

from jsonrpc import JSONRPCResponseManager, dispatcher
from pymongo import MongoClient, GEOSPHERE
from werkzeug.serving import run_simple
from werkzeug.wrappers import Request, Response

client = MongoClient('mongodb', 27017)

db = client.pharmacies
db.pharmacy.drop()
data = requests.post('https://dati.regione.campania.it/catalogo/resources/Elenco-Farmacie.geojson').json()
db.pharmacy.insert_many(data['features'])
db.pharmacy.create_index([('geometry', GEOSPHERE)])


@dispatcher.add_method
def SearchNearestPharmacy(**kwargs):

    pharmacies = []

    for doc in db.pharmacy.aggregate([
            {
                '$geoNear': {
                    'near': {'type': 'Point', 'coordinates': [kwargs['currentLocation']['longitude'], kwargs['currentLocation']['latitude']]},
                    'distanceField': 'dist.calculated',
                    'distanceMultiplier': 100,
                    'maxDistance': kwargs['range'],
                    'query': {'type': 'Feature'},
                    'spherical': True
                }
            },
            {'$limit': kwargs['limit']}
        ]
    ):

        pharmacies.append({
            'name': doc['properties']['Descrizione'],
            'distance': int(doc['dist']['calculated']/100),
            'location':
                {
                    'latitude': doc['geometry']['coordinates'][1],
                    'longitude': doc['geometry']['coordinates'][0],
                }
        })

    return {'pharmacies': pharmacies}


@Request.application
def application(request):
    response = JSONRPCResponseManager.handle(request.get_data(cache=False, as_text=True), dispatcher)
    return Response(response.json, mimetype='application/json')


if __name__ == '__main__':
    run_simple('0.0.0.0', 5000, application, passthrough_errors=True)

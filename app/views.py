from django.apps import apps
from django.http import JsonResponse
from . import logic
from . import utils
from django.conf import settings


def start_timer_view(request):
    session_id = request.GET.get('session_id')
    logic.start_timer(session_id)
    return JsonResponse({'status': 'success'})


def calculate_score_view(request):
    response_data = {
        'session_id': request.GET.get('session_id'),
        'correct': request.GET.get('correct'),
        'total': request.GET.get('total')
    }
    db_handle, client = utils.get_db_handle(
        db_name=settings.MONGO_DB_NAME,
        uri='mongodb+srv://doadmin:26Ou9E7yP8a13lf5@db-mongodb-nyc3-83293-a22f7971.mongo.ondigitalocean.com/admin?tls=true&authSource=admin'
    )
    score = logic.calculate_score(int(response_data['correct']), int(response_data['total']))
    collection = db_handle['data_collection']
    result = collection.insert_one({
        'session_id': response_data['session_id'],
        'score': score
    })
    print(result)
    client.close()
    return JsonResponse({'score': score})


# def calculate_score_view(request):
#     response_data = {
#         'session_id': request.GET.get('session_id'),
#         'correct': request.GET.get('correct'),
#         'total': request.GET.get('total')
#     }
#     return JsonResponse(response_data)


def end_timer_view(request):
    session_id = request.GET.get('session_id')
    time_taken = logic.end_timer(session_id)

    db_handle, client = utils.get_db_handle(
        db_name=settings.MONGO_DB_NAME,
        uri='mongodb+srv://doadmin:26Ou9E7yP8a13lf5@db-mongodb-nyc3-83293-a22f7971.mongo.ondigitalocean.com/admin?tls=true&authSource=admin'
    )

    collection = db_handle['data_collection']
    result = collection.update_one(
        {'session_id': session_id},  # Query document
        {'$set': {'time_taken': time_taken}},  # Update operation
        upsert=False  # Do not insert a new document if one doesn't exist
    )
    print(result)
    client.close()
    return JsonResponse({'time_taken': time_taken})


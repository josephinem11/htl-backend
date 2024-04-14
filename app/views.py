from django.apps import apps
from django.http import JsonResponse
from . import logic
from . import utils
from django.conf import settings


def start_timer_view(request):
    session_id = request.GET.get('session_id')
    logic.start_timer(session_id)
    db_handle, client = utils.get_db_handle(
        db_name=settings.MONGO_DB_NAME,
        uri=settings.MONGO_DB_URL
    )
    collection = db_handle['data_collection']
    collection.insert_one({
        'session_id': session_id,
        'score': 0,
        'completed': False,
        'time_taken': 0
    })
    return JsonResponse({'status': 'success'})


def calculate_score_view(request):
    response_data = {
        'session_id': request.GET.get('session_id'),
        'correct': request.GET.get('correct'),
        'total': request.GET.get('total')
    }
    db_handle, client = utils.get_db_handle(
        db_name=settings.MONGO_DB_NAME,
        uri=settings.MONGO_DB_URL
    )
    score = logic.calculate_score(int(response_data['correct']), int(response_data['total']))
    collection = db_handle['data_collection']
    collection.update_one(
        {'session_id': response_data['session_id']},  # Query that matches the document to update
        {'$set': {'score': score, 'completed': True}}  # Update operation
    )
    client.close()
    return JsonResponse({'score': score})


def end_timer_view(request):
    session_id = request.GET.get('session_id')
    time_taken = logic.end_timer(session_id)

    db_handle, client = utils.get_db_handle(
        db_name=settings.MONGO_DB_NAME,
        uri=settings.MONGO_DB_URL
    )

    collection = db_handle['data_collection']
    collection.update_one(
        {'session_id': session_id},  # Query document
        {'$set': {'time_taken': time_taken}},  # Update operation
        upsert=False  # Do not insert a new document if one doesn't exist
    )
    client.close()
    return JsonResponse({'time_taken': time_taken})


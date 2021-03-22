import csv
from django.shortcuts import render
from django.http import HttpResponse
from .models import Score

def export_csv(request):
    response = HttpResponse(content_type = 'text/csv')

    writer = csv.writer(response)
    writer.writerow(['id', 'data_created', 'sender', 'receiver', 'score_technical', 'score_social', 'scoresUser_id'])

    for score in Score.objects.all().values_list('id', 'data_created', 'sender', 'receiver', 'score_technical', 'score_social', 'scoresUser_id'):
        writer.writerow(score)

    # tell the browser what to do with the reponse
    response['Content-Disposition'] = 'attachment; filename="d3-score.csv"'

    return response
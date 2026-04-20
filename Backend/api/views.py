from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response

import csv
from django.http import JsonResponse
from django.conf import settings
import os

# Create your views here.


@api_view(['GET'])
def hello(request):
    return Response({"message": "Hello from Django backend!"})

def get_services(request):
    file_path = os.path.join(settings.BASE_DIR, "services.csv")

    services = []

    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:  # avoid empty rows
                services.append(row[0])

    return JsonResponse({"services": services})
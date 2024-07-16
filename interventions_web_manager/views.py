from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from .utils.read_csv import read_csv
from .utils.get_latitude_longitude import get_location
import os
# Create your views here.
# geopy documentation : https://geopy.readthedocs.io/en/stable/
# Rajouter la ville dans le csv ou la region

def index(request):
    '''
    Homepage
    '''
    return render(request, 'index.html')

@api_view(['GET'])
def interventions_list(request):
    '''
    API endpoint to list interventions
    '''
    file_path = 'database/interventions_db.csv'
    if os.path.exists(file_path):
        csv_data = read_csv(file_path)
        geocoded_data = get_location(csv_data)
        return Response(geocoded_data)
    else:
        return Response({"error": "File not found"}, status=404)

def interventions_view(request):
    '''
    View to render the interventions template
    '''
    return render(request, 'interventions.html')

def update_interventions(request):
    '''
    update interventions
    get request of new data from interventions.html
    update csv file (database)
    '''
    return render(request, 'interventions.html')


def backup_interventions_db(request):
    '''
    before updating create a copy of the db in its current state
    filename has date and time as well as version number of database
    '''
    
    
def list_backup_interventions_db(request):
    '''
    list all backups
    allow download
    '''
    return render(request, 'backup_interventions_list.html')
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render
from interventions_web_manager.utils import read_csv
from geopy.geocoders import Nominatim
# Create your views here.
# geopy documentation : https://geopy.readthedocs.io/en/stable/
def index(request):
    '''
    Homepage
    '''
    return render(request, 'index.html')

def interventions(request):
    '''
    list interventions
    read our database : "Base de données - Interventions Strasbourg - Test recrutement.csv"
    translate adresses into coordinates
    populate django template with data from csv file
    '''
    interventions = []
    geolocator = Nominatim
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
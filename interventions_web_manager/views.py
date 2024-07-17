from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import csv
import os
from .utils.read_csv import read_csv
from .utils.get_latitude_longitude import get_location
from django.shortcuts import redirect

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

@api_view(['POST'])
def update_intervention_status(request):
    '''
    API endpoint to update the status of an intervention
    '''
    address = request.data.get('Adresse')
    intervention_type = request.data.get('Type d\'intervention')
    intervention_precision = request.data.get('Précision de l\'intervention')
    date = request.data.get('Date de l\'intervention')
    new_status = request.data.get('Statut de l\'intervention')
    
    file_path = 'database/interventions_db.csv'
    updated_data = []
    print('writing1')

    if os.path.exists(file_path):
        with open(file_path, mode='r', newline='') as file:
            print('writing2')
            reader = csv.DictReader(file)
            for row in reader:
                if (row['Adresse'] == address and 
                    row['Type d\'intervention'] == intervention_type and 
                    row['Précision de l\'intervention'] == intervention_precision and
                    row['Date de l\'intervention'] == date):
                    row['Statut de l\'intervention'] = new_status
                updated_data.append(row)
        
        with open(file_path, mode='w', newline='') as file:
            print('writing')
            writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(updated_data)
            print('writing')

        
        return redirect('/interventions')
    else:
        return Response({"error": "File not found"}, status=404)

def interventions_view(request):
    '''
    View to render the interventions template
    '''
    return render(request, 'interventions.html')




@api_view(['POST'])
def add_intervention(request):
    new_intervention = {
        'Adresse': request.data.get('Adresse'),
        'Type d\'intervention': request.data.get('Type d\'intervention'),
        'Précision de l\'intervention': request.data.get('Précision de l\'intervention'),
        'Statut de l\'intervention': request.data.get('Statut de l\'intervention'),
        'Date de l\'intervention': request.data.get('Date de l\'intervention')
    }
    
    file_path = 'database/interventions_db.csv'
    
    if os.path.exists(file_path):
        with open(file_path, mode='a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=new_intervention.keys())
            writer.writerow(new_intervention)
        
        return render(request, 'interventions.html')
    else:
        return Response({"error": "File not found"}, status=404)


@api_view(['POST'])
def delete_intervention(request):
    address = request.data.get('Adresse')
    intervention_type = request.data.get('Type d\'intervention')
    intervention_precision = request.data.get('Précision de l\'intervention')
    date = request.data.get('Date de l\'intervention')
    
    file_path = 'database/interventions_db.csv'
    updated_data = []

    if os.path.exists(file_path):
        with open(file_path, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not (row['Adresse'] == address and 
                        row['Type d\'intervention'] == intervention_type and 
                        row['Précision de l\'intervention'] == intervention_precision and
                        row['Date de l\'intervention'] == date):
                    updated_data.append(row)
        
        with open(file_path, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
            writer.writeheader()
            writer.writerows(updated_data)
            print("delete finished")
        return render(request, 'interventions.html')
    else:
        return Response({"error": "File not found"}, status=404)

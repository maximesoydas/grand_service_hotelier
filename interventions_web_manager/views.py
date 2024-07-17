from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import csv
import os
from .utils.read_csv import read_csv
from .utils.get_latitude_longitude import get_location
from django.shortcuts import redirect
# from geopy.geocoders import Nominatim
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
        update_csv(file_path, geocoded_data)  # Update the CSV file with new geolocation data to gain loading speed
        return Response(geocoded_data)
    else:
        return Response({"error": "File not found"}, status=404)
    
def update_csv(file_path, csv_data):
    fieldnames = csv_data[0].keys()
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_data)

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
    '''
    API endpoint to add a new intervention
    '''
    address = request.data.get('Adresse')
    intervention_type = request.data.get('Type d\'intervention')
    intervention_precision = request.data.get('Précision de l\'intervention')
    datetime_intervention = request.data.get('Date de l\'intervention')
    status = request.data.get('Statut de l\'intervention')
    
    file_path = 'database/interventions_db.csv'
    
    # Ensure the new intervention has latitude and longitude
    # geolocator = Nominatim(user_agent="interventions_web_manager")
    # location = geolocator.geocode(f"{address}, 67000 Strasbourg")
    
    # if location:
    new_intervention = {
        'Adresse': address,
        'Type d\'intervention': intervention_type,
        'Précision de l\'intervention': intervention_precision,
        'Statut de l\'intervention': status,
        'Date de l\'intervention': datetime_intervention,
        # 'latitude': location.latitude,
        # 'longitude': location.longitude
    }
    
    # Append the new intervention to the CSV file
    fieldnames = list(new_intervention.keys())
    with open(file_path, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(new_intervention)
    
    return Response({"message": "Intervention added successfully"})
    # else:
    #     return Response({"error": "Could not geocode address"}, status=400)

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

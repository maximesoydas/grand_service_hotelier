# Grand Service Hotelier

## Introduction

This is a Django project for managing interventions. The project includes functionalities to view, add, update, and delete interventions on a map interface.

## Docker Installation

### Prerequisites

- Docker ([Linux](https://docs.docker.com/engine/install/ubuntu/), [Windows](https://docs.docker.com/desktop/install/windows-install/))
### Steps

1. **Clone the repository**

    ```bash
    git clone <repository_url>
    cd GRAND_SERVICE_HOTELIER
    ```
2. **Build and Run the Docker Containers**

    ```bash
    docker build -t interventions_manager .
    ```
    ```bash
    docker run -p 8000:8000 interventions_manager
    ```

3. **Access the Application**

    Open your web browser and navigate to `http://127.0.0.1:8000/` to view the application.

4. **Stop Application**

    ```bash
    docker ps
    ```
    ```bash
    docker stop <CONTAINER_ID>

    or

    docker stop <NAMES>
    ```
## Local Installation (Repository)

### Prerequisites

Ensure you have the following installed on your system:
- Python 3.x
- `pip` (Python package installer)
- `virtualenv` (Python virtual environment tool)

### Steps

1. **Clone the repository**

    ```bash
    git clone <repository_url>
    cd GRAND_SERVICE_HOTELIER
    ```

2. **Set up the virtual environment**

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4. **Install the required packages**

    ```bash
    pip install -r requirements.txt
    ```

5. **Run the initial migrations**

    ```bash
    python manage.py migrate
    ```

6. **Run the development server**

    ```bash
    python manage.py runserver
    ```

7. **Access the application**

    Open your web browser and navigate to `http://127.0.0.1:8000/` to view the application.

## Usage

### Viewing Interventions

1. Navigate to the interventions page at `http://127.0.0.1:8000/interventions/`
2. View the map with the interventions marked on it.
3. Click on any marker on the map to view details of the intervention.
4. Click on the table rows to view and update the status of the interventions.

### Adding Interventions

1. Click the "Ajouter une intervention" button.
2. Fill in the required fields in the modal form.
3. Submit the form to add the intervention.

### Updating Interventions

1. Click on any intervention in the table or on the map.
2. Update the status using the modal form.
3. Submit the form to save changes.

### Deleting Interventions

1. Click on any intervention in the table or on the map.
2. Use the "Supprimer" button in the modal to delete the intervention.

## Directory Structure

- `database`: Contains the CSV file with intervention data.
- `grand_service_hotelier`: Main Django project directory.
- `interventions_web_manager`: Django app for managing interventions.
- `venv`: Virtual environment directory.
- `requirements.txt`: File containing the list of required Python packages.
- `README.md`: This file.

## Troubleshooting

- Ensure the virtual environment is activated when running commands.
- Check if all required packages are installed.
- Ensure the database file (`interventions_db.csv`) is in the correct location.

## Improvement Points

Here are some suggested improvements that could be made to enhance the project:

1. **Database Optimization**
   - Transition from using CSV for data storage to a more robust database system like PostgreSQL or MySQL to handle larger datasets efficiently.
   - Implement database indexing for faster query performance.

2. **Enhanced UI/UX**
   - Improve the UI/UX by using a frontend framework like React or Vue.js for a more dynamic and responsive interface.
   - Add user authentication and authorization to ensure data security and personalized user experiences.

3. **Error Handling and Validation**
   - Implement comprehensive error handling and form validation both on the frontend and backend to improve reliability and user experience.
   - Provide user-friendly error messages and feedback.

4. **Performance Optimization**
   - Optimize the performance of the map and table rendering, especially when dealing with a large number of interventions.
   - Implement caching mechanisms to reduce load times and improve responsiveness.

5. **Testing and CI/CD**
   - Add unit tests, integration tests, and end-to-end tests to ensure the stability and reliability of the application.
   - Implement Continuous Integration/Continuous Deployment (CI/CD) pipelines to automate testing and deployment processes.

6. **API Enhancements**
   - Enhance the API endpoints with features such as pagination, filtering, and sorting to handle larger datasets and provide more flexibility in data retrieval.
   - Implement API rate limiting and authentication to secure the endpoints.

7. **Geolocation Enhancement**
   - Optimize the geolocation process by calling the geopy library only when new entries are added. This will ensure quicker response times when loading the intervention page since the geolocation data will already be available in the CSV file.

8. **Deploy on a VPS**

    - If necessary we can easily deploy on a vps over https with nginx
## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

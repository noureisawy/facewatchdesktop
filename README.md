This repository contains the code for the desktop application of the Facewatch project, which is a health monitoring system using facial recognition and machine learning algorithms. The desktop application allows users to capture images, view reports, and update their profile information.

To get started with the desktop application, follow the installation and setup instructions below.

## Installation

Follow these steps to set up the backend project:

1. **Clone the Repository:**
2. **Create Virtual Environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate Virtual Environment:**

   On Windows:

   ```bash
   venv\Scripts\activate
   ```

   On macOS/Linux:

   ```bash
   source venv/bin/activate
   ```

4. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up Database:**

   ```bash
   python manage.py migrate
   ```

6. **Create Superuser (Optional):**

   ```bash
   python manage.py createsuperuser
   ```

7. **Run the Development Server:**

   ```bash
   python manage.py runserver
   ```



Contributing:
If you would like to contribute to the desktop application, please follow the guidelines outlined in the CONTRIBUTING.md file in the repository.

Quick Document for the Whole Project

The Facewatch project is a health monitoring system that utilizes facial recognition and machine learning algorithms to detect and predict various health conditions. The project consists of a backend server and a desktop application.

The backend server is responsible for accepting shared images from the user and updating the deep learning models with the new data. It uses version control to track changes in the model weights and allows for efficient model updates.

The desktop application allows users to capture images, view reports, and update their profile information. It provides a user-friendly interface for interacting with the health monitoring system.

The project aims to provide accurate predictions for the level of alertness, emotions, and potential medical diseases using facial recognition and machine learning techniques. The system continuously analyzes and tracks these factors, providing valuable insights into users' well-being and overall health status.

Future work for the project includes expanding the dataset for disease predictions, improving facial expression analysis under challenging conditions, and offering personalized health insights to users based on their specific health profile and historical data.

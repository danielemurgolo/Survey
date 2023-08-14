# Survey Data Collection System
Welcome to the Survey Data Collection System! This system aims to efficiently gather crucial data using a web-based questionnaire (implemented in Django) addressing various groups' questions. Participants can access the questionnaire, and submit their responses anonymously, facilitating the data collection process. This collected data is fed to a mathematical model, the Network Scale-Up method, allowing us to estimate the scale of affected individuals.

## Key Features
1. **Web-based Questionnaire**: participants easily access and respond to the questionnaire online.
2. **Estimation Model**: We employ the innovative Network Scale-up Method (NSUM) to estimate hard-to-reach sub-populations based on social network connections.

Our mission is to provide a robust system that generates valuable insights, aiding in effective decision-making to manage the problem at hand.

## Installation

1. Clone the repository:
   
   ```
   git clone https://github.com/danielemurgolo/Survey.git
   cd Survey
   ```
   
2. Create a virtual environment (recommended but optional):
   ```
   python -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Apply database migration:

   ```
   python manage.py makemigrations
   python manage.py migrate
   python manage.py cities_light
   ```
   This step may take some minutes, don't worry if the installation gets stuck.

5. Create superuser (Admin):
   ```
   python manage.py createsuperuser
   ```

6. Start server:
   ```
   python manage.py runserver
   ```
   With this command, the server runs on localhost:8000. If wanted, you can deploy using your IP or deploy using [Heroku](https://devcenter.heroku.com/articles/deploying-python)
   
## Usage

When accessing the web application, for example at http://localhost:8000, the empty home page should look like this:



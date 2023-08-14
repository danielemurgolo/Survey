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

For this tutorial, we are going show the steps you need to take to create your own survey. We are going to consider the URL of the web app as HTTP:localhost:8000, you should replace it with your own URL.

### Home Page

When accessing the web application, i.e. http://localhost:8000, the empty home page should look like this:

![survey_home_empty](https://github.com/danielemurgolo/Survey/assets/98823551/93f594c1-5002-4ac1-961b-fa4638da5ffb)


### Admin Page

The first step to take is to go to the admin page, http://localhost:8000/admin, you should be prompted with a log in page like the following:

![admin_login](https://github.com/danielemurgolo/Survey/assets/98823551/8df183c2-091b-47a7-b0bf-d450749576b5)


You should log in using the credentials you created using the command ```python manage.py createsuperuser```. After logging in, the admin page looks like this:

![admin_page](https://github.com/danielemurgolo/Survey/assets/98823551/a337614c-02a7-4b67-bf1b-2d505a1b028d)


### Creating a Survey

Now, to create a survey you can press on ```Surveys``` and then press the ```Add Survey``` button. Here you can fill in the form to create the survey. After creating the survey you can edit it and delete it as shown in the video below. 

https://github.com/danielemurgolo/Survey/assets/98823551/11dd3d76-d5bc-4438-acc8-343d8c3fe200

### Creating a Question





# Survey Data Collection System
Welcome to the Survey Data Collection System! This system aims to efficiently gather crucial data using a web-based questionnaire (implemented in Django) addressing various groups' questions. Participants can access the questionnaire, and submit their responses anonymously, facilitating the data collection process. This collected data is fed to a mathematical model, the Network Scale-Up method, allowing us to estimate the scale of affected individuals.

## Table of contents
- [Key Features](#key-features)
- [Installation](#installation)
- [Usage](#usage)
   - [Home Page](#home-page)
   - [Admin Page](#admin-page)
   - [Creating a Survey](#creating-a-survey)
   - [Creating a Question](#creating-a-question)
   - [Complete Example](#complete-example)
- [License](#license)
- [Contact](#contact)

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

For this tutorial, we are going to show the steps you need to take to create your survey. We are going to consider the URL of the web app as HTTP:localhost:8000, you should replace it with your own URL.

### Home Page

When accessing the web application, i.e. http://localhost:8000, the empty home page should look like this:

![survey_home_empty](https://github.com/danielemurgolo/Survey/assets/98823551/93f594c1-5002-4ac1-961b-fa4638da5ffb)


### Admin Page

The first step to take is to go to the admin page, http://localhost:8000/admin, you should be prompted with a login page like the following:

![admin_login](https://github.com/danielemurgolo/Survey/assets/98823551/8df183c2-091b-47a7-b0bf-d450749576b5)


You should log in using the credentials you created using the command ```python manage.py createsuperuser```. After logging in, the admin page looks like this:

![admin_page](https://github.com/danielemurgolo/Survey/assets/98823551/a337614c-02a7-4b67-bf1b-2d505a1b028d)


### Creating a Survey

Once you are logged in go to the "Surveys" page, click the "Add Survey" button to create a new survey. Fill in the name and description fields and then click "Save". This will create a new survey entry.
After creating a survey, you can click on its name in the list to view its details. From the detail view, you can edit the survey's information and save your changes. If you want to delete a survey, you can do so from the survey's detail page as well.

https://github.com/danielemurgolo/Survey/assets/98823551/11dd3d76-d5bc-4438-acc8-343d8c3fe200

### Creating a Question

You can create three different types of questions:
* Country Question: This question serves to determine both the respondent's country and region. This approach facilitates data collection while maintaining a satisfactory level of user anonymity.
* Integer Question: This question helps identify the number of individuals within the respondent's network who possess a specific trait. For instance, one might ask, "How many people do you know who have experienced Fever?"
* Radio Question: This question assists in collecting pertinent information about the population, enhancing the study's relevance. For example, a query such as "What is your gender?" falls under this category.

To create, modify, and delete each question, you can perform the same operations as demonstrated for the Survey. The only exception is that you will need to choose the specific Survey to which you want to assign the question. Furthermore, when dealing with Radio Questions, you will be required to craft "Radio Answers" for each one and subsequently allocate them to the corresponding Radio Question. Here are concise examples illustrating how to create each type of question:



https://github.com/danielemurgolo/Survey/assets/98823551/2c9d8e62-3de3-40bc-b1d1-064cdeee0c34




https://github.com/danielemurgolo/Survey/assets/98823551/f0a1258d-79e2-453b-8228-1e9bc378c3ca




https://github.com/danielemurgolo/Survey/assets/98823551/75437f2f-e097-478f-8e0c-176fc123c06c


### Complete Example




https://github.com/danielemurgolo/Survey/assets/98823551/4554895e-d658-4e06-ae06-60426f170cbc


## License

This project is licensed under the GNU General Public License v3.0 - see the [`LICENSE`](./LICENSE) file for details.

## Contact

If you have any questions about the project, feel free to contact us at [Daniele Murgolo](mailto:murgolo@chalmers.se?subject=[GitHub]%20Django%20Survey%20NSUM) and [Tomas Vu](mailto:gusvutoy@student.gu.se?subject=[GitHub]%20Django%20Survey%20NSUM).








<a name="readme-top"></a>
<!--
Citation for this README:
https://github.com/othneildrew/Best-README-Template#readme
-->

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <h3 align="center">UVA CS3240 Project: CavCourses</h3>

  <p align="left">
    This is my semester long project for UVA's Advanced Software Development (CS3240) course. I worked in a group of 5 and used the Agile Scrum Methodology to reimagine the much beloved "Lous List" website with some new features. In my role as DevOps Manager I oversaw our workflow, Github actions, and deployment of the App via Heroku.
    <br />
</div>
<div align="center">
    <br />
    <a href="https://f22.cs3240.org/project.html">Project Page</a>
    ·
    <a href="https://f22.cs3240.org/lutherslist.html">Luther's List API</a>
    ·
    <a href="https://louslist.org/">Original Lous List</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
      <ul>
        <li><a href="#important-notes">Important Notes</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li><a href="#team-members">Team Members</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This is for the University of Virginia's CS 3240 (Advanced Software Development) course. Our team chose to build a Web App modeling the University of Virginia's beloved <a href="https://louslist.org/">Lous List</a>.

Here are the Lou's List Specific Requirements:
* Students must be ablte to view an search classes, separeated into logical catagories.
* Students must be able to save a prospective schedule for a given semester. The system should prevent time conflicts and prevent signing up for multiple sections of the same course.
* Students should be able to “friend” other students to see their schedule and leave a comment on their schedule.

Here are the Projects General Requirements:
* All projects must incorporate Google user accounts as the primary way that someone logs into the system.
* All users must have an account of some kind where they can store their personal information relevant to the app.
* All users must be able to maintain a list of “friends” in the app, where they can view key information about the other user. See the project options for details.
* All projects must incorporate the SIS / Class Listing API that we will provide, which will contain (mostly) up-to-date data from SIS that mirrors what you would currently see from Lou’s List.
* All projects must be built using the prescribed language (Python 3), framework (Django 4), build environment (GitHub Actions CI), source control management (GitHub), and cloud hosting (Heroku).
* You must use the PostgreSQL database engine for production on Heroku and continuous integration (on GitHub Actions).

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Built With

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Bootstrap](https://img.shields.io/badge/bootstrap-%23563D7C.svg?style=for-the-badge&logo=bootstrap&logoColor=white)
![HTML](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white)
![CSS](https://img.shields.io/badge/css-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white)

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Important Notes

This project is not flawless. Due to unforseen tragic events during the semester and their effects on the university and student body, as well as the time constraints imposed by final exams, this website was never fully finished. There are still plenty of bugs here and there if you care to look for them, notably one that prevents certain accounts from adding classes to their schedule during a slicing issue.

Known bugs:
* Query issue that prevents some accounts from adding classes to their schedule
* A user can send multiple friend requests to the same user.
* A user can accept multiple friend requests from another user
* The schedule does not allow an override to have classes at the same time (some students, including myself, have waivers that allow them to have concurrent classes)
* Some users profile pictures have trouble rendering.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- GETTING STARTED -->
## Getting Started

Due to the fact that Heroku no longer provides free hosting, the app hosted on Heroku has been taken down. However, you can see a copy of the app locally using Django's development server.

### Prerequisites

* Django <a href="https://docs.djangoproject.com/en/4.1/topics/install/"> (Django Installation Directions) </a>
* A Virtual Environment <a href="https://www.javatpoint.com/django-virtual-environment-setup"> (Venv Installation Directions) </a>

### Directions

1. Clone this repository locally <a href="https://www.google.com/url?sa=t&rct=j&q=&esrc=s&source=web&cd=&cad=rja&uact=8&ved=2ahUKEwjqrIGs-_n7AhUdGVkFHfBFAEEQFnoECBAQAQ&url=https%3A%2F%2Fdocs.github.com%2Fen%2Frepositories%2Fcreating-and-managing-repositories%2Fcloning-a-repository&usg=AOvVaw1A0BC2W4ipC0YHVzLxQPgS"> (How to clone repos) </a>
2. Activate your virtual environment
```bash
source your-venv-name/bin/activate
```
3. Install the requirements
```bash
pip install -r requirements.txt
```
4. Run the server locally
```bash
python manage.py runserver
```
5. Go to the URL listed in the terminal output to see the app.
6. To close the app, exit out of that tap and hit Ctl+C in your terminal
7. Deactivate your virtual environment.
```bash
deactivate your-venv-name
```

<!-- CONTACT -->
## Team Members

* Megan Kuo           - mlk6une (Scrum Master)
* Connor Wilson       - crw8eg  (DevOps)
* Srini Chelimilla    - slc8kf  (UI/UX)
* Johnny Lindsey      - jbl5xq  (Requirements)
* Nathaniel Hershel   - nth5pdk (Testing)

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Many thanks to both Professor Sheriff and Professor McBurney for creating the Luther's List API (linked at top of page) and enabling this project as part of their curriculum. 

<p align="right">(<a href="#readme-top">back to top</a>)</p>

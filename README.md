<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/github_username/repo_name">
    <img src="https://sharepointmaven.com/wp-content/uploads/2016/08/tag-icon.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">Tag-me</h3>

  <p align="center">
    Rest-API for image tagging system
    <br />
    <br />
    <a href="https://youtu.be/NY68Grl0v7c">View Demo</a>
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#initialmigration">InitialMigration</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#deployment">Deployment</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

System that use for tag images.

### Built With

* Backend - [Python Django](https://www.djangoproject.com/)
* Database - [PostgreSQL](https://www.postgresql.org/)

<!-- GETTING STARTED -->

## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

1. [Docker Compose](https://docs.docker.com/compose/install/)

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/Nipuna-saga/tag-me.git
   ```
2. Build and Up
   ```sh
   docker-compose up --build
   ```
3. Follow the steps in usage section

### InitialMigration

1. Connect to the docker container
   ```sh
   docker exec -it tag-me_web_1 bash
   ```
2. Create migration files
   ```sh
   python manage.py makemigrations
   ```
3. Apply database migrations
   ```sh
   python manage.py migrate
   ```
4. Create super-user
   ```sh
   python manage.py createsuperuser
   ```
5. Run unit tests
   ```sh
   python manage.py test
   ```
<!-- USAGE EXAMPLES -->

## Usage

Please watch the demo [video](https://youtu.be/NY68Grl0v7c) to see usage of the system.


## Deployment

Because of the nature of this system, serverless architecture can be used to host it. AWS lambda can be used with 
AWS API gateway and AWS S3 buckets to store images. And also AWS code pipelines can be used for auto deployments.


<!-- CONTACT -->

## Contact

Nipuna Shanthidewa - [email](https://mail.google.com/mail/?view=cm&fs=1&to=nipunashanthidewa16@gmail.com&su=Github_project_tag-me)

Project Link: [https://github.com/Nipuna-saga/tag-me.git](https://github.com/Nipuna-saga/tag-me.git)



<!-- ACKNOWLEDGEMENTS -->

## Acknowledgements

* [Github - Best-README-Template](https://github.com/othneildrew/Best-README-Template.git)

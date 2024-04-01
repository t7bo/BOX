# Box Office Prediction WebsAIte

## Introduction

This student project aims to develop a decision-making tool for the manager of the "New is always better" cinema. This manager seeks to optimize the selection of films to screen using a more efficient approach than their current method based on intuition and experience.

## Project Description

The manager of the "New is always better" cinema typically selects films to screen based on monitoring new releases and participation in festivals such as Cannes and Deauville. However, this time-consuming approach has prompted consideration for partial automation. The cinema has a unique policy: only screening new releases during their first week, with weekly refreshes.

The project involves developing a tool using artificial intelligence to estimate attendance for new releases from their first week. The goal is to predict which films will attract the most viewers, optimizing scheduling and maximizing revenue. Ideally, these predictions should be available as early as possible. The manager envisions this tool being accessible via a web or mobile application, easy to use without requiring specific skills in computer science or AI.

## Technologies Used

- **Python**, **SQLite**, **PostGres**
- **Pandas**, **Matplotlib**, **Seaborn** Used for Data Analysis & Visualisation.
- **Machine Learning:** Used to train models for predicting film attendance.
- **Django:** Web framework used for developing the web application.
- **FastAPI:** Framework for rapid web API development, used to create interfaces between different components of the system.
- **Docker:** Used for containerizing different parts of the application, ensuring portability and ease of deployment.
- **Azure:** Cloud platform used for deploying the application and storing data.
- **Scrapy:** Framework used for web scraping data on new films from various sources.
- **Airflow/cron:** Used for scheduling and automating tasks for data collection, model training, and prediction deployment.
- **Jira:** Used for project management and task tracking.
- **MLflow:** Used for tracking and managing machine learning experiments, including metric tracking, model management, and versioning.

## 1. Collect all kind of necessary data for the predictive A.I model

- **Scrapy** : Used to scrap data from different basic websites.
- **Selenium** : Used to scrap data from various JS websites.
- **User Agent** : Specify it in *settings.py* & into fetch() command within **Scrapy Shell**.
- **Chrome Driver** : Download it & put in the scraper project dir (same dir as *scrapy.cfg* )

## 2. Create a database with a collection of tables created with SQLite & all the data scraped

- **Scrapy/Spider Pipelines** - *pipelines.py* : Used to clean scraped data.
- **SQLite** : Used to create a DB, tables and stock data.

## 3. Request APIs to get more data

- **YouTube Tutorial** : https://youtu.be/DqtlR0y0suo?si=IADGFI-VIFtVv7_H
- **Insomnia**

## 4. Use a PostGres Docker Image instead of SQLite
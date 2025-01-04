#Redbus Data Scraping with Selenium & Dynamic Filtering using Streamlit

Overview

This project provides a comprehensive solution to scrape, analyze, and visualize bus travel data from Redbus. It leverages Selenium for web scraping, SQL for data storage, and Streamlit for developing an interactive application to filter and display the data. The primary goal is to enhance data-driven decision-making in the transportation domain.

Skills Acquired

Web Scraping: Selenium
Backend: Python, SQL
Frontend: Streamlit
Data Analysis

Domain

Transportation

Problem Statement
The project aims to revolutionize the transportation industry by:

Automating the extraction of bus travel data such as routes, schedules, prices, and seat availability.
Developing a user-friendly interface for dynamic filtering and data visualization.
Enabling better planning, analysis, and decision-making in the transportation sector.

Business Use Cases
Travel Aggregators: Real-time schedules and seat availability for customers.
Market Analysis: Insights into travel trends and patterns.
Customer Service: Personalized travel recommendations.
Competitor Analysis: Comparison of pricing and services.

Approach

1. Data Scraping
Tool: Selenium
Data collected:
Bus routes, links, schedules, prices, seat availability, and ratings.

3. Data Storage
Database: SQL
Structured schema to store and query the data.

5. Streamlit Application
Filters: Bus type, route, price range, star rating, availability.
Interactive and user-friendly design.

4. Data Analysis
SQL queries to retrieve and filter data.
Streamlit for visualization and interaction.

Results
Successfully scrape data for at least 10 Government State Transport and selected private routes.
Store data in a structured SQL database.
Create an interactive and efficient Streamlit application for filtering and analysis.
Project Deliverables
Source Code: Python scripts for scraping, database interaction, and Streamlit app.
Documentation: Explanation of code, usage instructions, and database schema.
Database Schema: SQL scripts to create and populate the database.
Streamlit Application: Screenshots or a hosted app showcasing functionality.
Database Schema
Table Name: bus_routes

Column Name	Data Type	Description
id	INT	Primary Key (Auto-increment)
route_name	TEXT	Bus route information
route_link	TEXT	Link to route details
busname	TEXT	Name of the bus
bustype	TEXT	Bus type (Sleeper/Seater/AC/Non-AC)
departing_time	TIME	Scheduled departure time
duration	TEXT	Journey duration
reaching_time	TIME	Expected arrival time
star_rating	FLOAT	Passenger rating
price	DECIMAL	Ticket price
seats_available	INT	Number of seats available

References
Selenium Documentation
Streamlit Documentation
SQL Connection Guide

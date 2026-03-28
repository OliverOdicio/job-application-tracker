# Job Application Tracker

## Description
Job Application Tracker is a full-stack web application built with Flask and MySQL to help users organize and manage their job search process.

The application allows users to track:
- Companies
- Jobs
- Contacts
- Applications

It also includes a dashboard with statistics and a job match feature based on user-entered skills.

---

## Features

### CRUD Functionality
The application supports full CRUD operations for all main tables:

- **Companies** → Add, View, Edit, Delete
- **Jobs** → Add, View, Edit, Delete
- **Contacts** → Add, View, Edit, Delete
- **Applications** → Add, View, Edit, Delete

### Dashboard
The dashboard displays:
- Total number of companies
- Total number of jobs
- Total number of contacts
- Total number of applications
- Application status summary
- Recent applications

### Job Match Feature
Users can enter skills such as:
- Python
- SQL
- Data
- AI

The system compares those skills with job titles and returns a match percentage.

---

## Technologies Used
- Python
- Flask
- MySQL
- HTML
- CSS
- Git/GitHub

---

## Project Structure

```bash
job_tracker/
│
├── app.py
├── database.py
├── schema.sql
├── README.md
├── AI_USAGE.md
├── requirements.txt
│
├── templates/
│   ├── dashboard.html
│   ├── companies.html
│   ├── edit_company.html
│   ├── jobs.html
│   ├── edit_job.html
│   ├── contacts.html
│   ├── edit_contact.html
│   ├── applications.html
│   ├── edit_application.html
│   ├── job_match.html
│   ├── add_company.html
│   ├── add_job.html
│   ├── add_contact.html
│   └── add_application.html
│
└── static/
    └── style.css
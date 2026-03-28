from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Jff231621$",
        database="job_tracker"
    )

@app.route("/")
def dashboard():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) AS total FROM companies")
    companies = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM jobs")
    jobs = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM contacts")
    contacts = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM applications")
    applications = cursor.fetchone()["total"]

    conn.close()

    return render_template(
        "dashboard.html",
        companies=companies,
        jobs=jobs,
        contacts=contacts,
        applications=applications
    )

@app.route("/companies")
def list_companies():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("companies.html", companies=companies)


@app.route("/add_company", methods=["GET", "POST"])
def add_company():
    if request.method == "POST":
        company_name = request.form["company_name"]
        location = request.form["location"]

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO companies (company_name, location) VALUES (%s, %s)",
            (company_name, location)
        )

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("list_companies"))

    return render_template("add_company.html")

@app.route("/delete_company/<int:company_id>")
def delete_company(company_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM companies WHERE company_id = %s",
        (company_id,)
    )

    conn.commit()

    cursor.close()
    conn.close()

    return redirect(url_for("list_companies"))

@app.route("/edit_company/<int:company_id>", methods=["GET", "POST"])
def edit_company(company_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        company_name = request.form["company_name"]
        location = request.form["location"]

        cursor.execute(
            "UPDATE companies SET company_name=%s, location=%s WHERE company_id=%s",
            (company_name, location, company_id)
        )

        conn.commit()

        cursor.close()
        conn.close()

        return redirect(url_for("list_companies"))

    cursor.execute("SELECT * FROM companies WHERE company_id = %s", (company_id,))
    company = cursor.fetchone()

    cursor.close()
    conn.close()

    return render_template("edit_company.html", company=company)

@app.route("/jobs")
def list_jobs():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT jobs.*, companies.company_name
        FROM jobs
        JOIN companies ON jobs.company_id = companies.company_id
    """)

    jobs = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("jobs.html", jobs=jobs)

@app.route("/add_job", methods=["GET", "POST"])
def add_job():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        company_id = request.form["company_id"]
        job_title = request.form["job_title"]

        cursor.execute(
            "INSERT INTO jobs (company_id, job_title) VALUES (%s,%s)",
            (company_id, job_title)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("list_jobs"))

    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()

    conn.close()

    return render_template("add_job.html", companies=companies)


@app.route("/edit_job/<int:job_id>", methods=["GET", "POST"])
def edit_job(job_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":
        company_id = request.form["company_id"]
        job_title = request.form["job_title"]

        cursor.execute(
            "UPDATE jobs SET company_id=%s, job_title=%s WHERE job_id=%s",
            (company_id, job_title, job_id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("list_jobs"))

    cursor.execute("SELECT * FROM jobs WHERE job_id = %s", (job_id,))
    job = cursor.fetchone()

    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()

    conn.close()

    return render_template("edit_job.html", job=job, companies=companies)


@app.route("/delete_job/<int:job_id>")
def delete_job(job_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM jobs WHERE job_id = %s",
        (job_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("list_jobs"))

@app.route("/contacts")
def list_contacts():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT contacts.*, companies.company_name
        FROM contacts
        JOIN companies ON contacts.company_id = companies.company_id
    """)

    contacts = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("contacts.html", contacts=contacts)

@app.route("/add_contact", methods=["GET", "POST"])
def add_contact():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        contact_name = request.form["contact_name"]
        email = request.form["email"]
        company_id = request.form["company_id"]

        cursor.execute(
            "INSERT INTO contacts (contact_name, email, company_id) VALUES (%s,%s,%s)",
            (contact_name, email, company_id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("list_contacts"))

    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()

    conn.close()

    return render_template("add_contact.html", companies=companies)

@app.route("/edit_contact/<int:contact_id>", methods=["GET", "POST"])
def edit_contact(contact_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        contact_name = request.form["contact_name"]
        email = request.form["email"]
        company_id = request.form["company_id"]

        cursor.execute(
            "UPDATE contacts SET contact_name=%s, email=%s, company_id=%s WHERE contact_id=%s",
            (contact_name, email, company_id, contact_id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("list_contacts"))

    cursor.execute("SELECT * FROM contacts WHERE contact_id = %s", (contact_id,))
    contact = cursor.fetchone()

    cursor.execute("SELECT * FROM companies")
    companies = cursor.fetchall()

    conn.close()

    return render_template("edit_contact.html", contact=contact, companies=companies)


@app.route("/delete_contact/<int:contact_id>")
def delete_contact(contact_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM contacts WHERE contact_id = %s",
        (contact_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("list_contacts"))



@app.route("/applications")
def list_applications():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT applications.*, jobs.job_title
        FROM applications
        JOIN jobs ON applications.job_id = jobs.job_id
    """)

    applications = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("applications.html", applications=applications)

@app.route("/add_application", methods=["GET","POST"])
def add_application():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        job_id = request.form["job_id"]
        status = request.form["status"]
        application_date = request.form["application_date"]

        cursor.execute(
            "INSERT INTO applications (job_id, status, application_date) VALUES (%s,%s,%s)",
            (job_id, status, application_date)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("list_applications"))

    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()

    conn.close()

    return render_template("add_application.html", jobs=jobs)

@app.route("/edit_application/<int:application_id>", methods=["GET", "POST"])
def edit_application(application_id):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == "POST":

        job_id = request.form["job_id"]
        status = request.form["status"]
        application_date = request.form["application_date"]

        cursor.execute(
            "UPDATE applications SET job_id=%s, status=%s, application_date=%s WHERE application_id=%s",
            (job_id, status, application_date, application_id)
        )

        conn.commit()
        conn.close()

        return redirect(url_for("list_applications"))

    cursor.execute("SELECT * FROM applications WHERE application_id = %s", (application_id,))
    application = cursor.fetchone()

    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()

    conn.close()

    return render_template("edit_application.html", application=application, jobs=jobs)


@app.route("/delete_application/<int:application_id>")
def delete_application(application_id):

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM applications WHERE application_id = %s",
        (application_id,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("list_applications"))

@app.route("/job_match", methods=["GET", "POST"])
def job_match():

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    matches = []

    if request.method == "POST":

        skills = request.form["skills"].lower().split(",")

        cursor.execute("SELECT job_title FROM jobs")
        jobs = cursor.fetchall()

        for job in jobs:

            title = job["job_title"].lower()

            match_count = 0

            for skill in skills:
                skill = skill.strip()
                if skill in title:
                    match_count += 1

            percentage = int((match_count / len(skills)) * 100)

            matches.append({
                "title": job["job_title"],
                "percentage": percentage
            })

    conn.close()

    return render_template("job_match.html", matches=matches)

if __name__ == "__main__":
    app.run(debug=True)
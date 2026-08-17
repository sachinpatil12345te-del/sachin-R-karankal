import os
from flask import Flask, jsonify, render_template, request, send_from_directory
from pymongo import MongoClient
from pymongo.errors import PyMongoError

app = Flask(__name__)

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(mongo_uri)

def get_database():
    try:
        client.admin.command("ping")
        return client["resume_db"]
    except PyMongoError:
        return None

DEFAULT_PROFILE = {
    "name": "Sachin R Karankal",
    "mobile": "+91 9226313805",
    "whatsapp": "+91 9226313805",
    "instagram": "@patil_sachin_sg",
    "email": "sachinpatil12345te@gmail.com",
    "tagline": "Career-focused and results-driven professional",
    "summary": "Dedicated and professional individual with strong communication skills, a passion for growth, and a commitment to delivering quality work. I have practical exposure to AI & ML, Power BI, and data-driven thinking.",
    "education": [
        "Diploma in Computer Engineering",
        "R C Patel College of Engineering and Polytechnic, Shirpur",
        "Currently in 3rd year of study"
    ],
    "skills": [
        "Communication", "Leadership", "Problem Solving", "Time Management",
        "Teamwork", "Customer Support", "Adaptability", "Professionalism",
        "AI & ML", "Power BI", "Python", "Data Analysis"
    ],
    "internship": "Internship in AI & ML",
    "internship_details": "Completed internship training in Artificial Intelligence and Machine Learning, gaining practical exposure to modern technology, model concepts, and data-driven problem solving.",
    "projects": [
        {
            "title": "Fashion Intelligence Hub",
            "description": "Developed a style prediction and best marketplace recommendation system that helps users discover fashion trends and suitable products based on their preferences."
        },
        {
            "title": "Credit Card Fraud Detection Dashboard",
            "description": "Built a dashboard that predicts credit card fraud and displays all relevant transaction and fraud-related information for analysis and decision-making."
        }
    ],
    "availability": "Available for opportunities"
}


def load_profile():
    db = get_database()
    if db is None:
        return DEFAULT_PROFILE
    profile = db.profile.find_one()
    if profile is None:
        db.profile.insert_one(DEFAULT_PROFILE)
        return DEFAULT_PROFILE
    return profile


@app.route("/")
def index():
    profile = load_profile()
    return render_template("home.html", profile=profile)


@app.route("/resume")
def resume_page():
    profile = load_profile()
    return render_template("resume.html", profile=profile)


@app.route("/skills")
def skills_page():
    profile = load_profile()
    return render_template("skills.html", profile=profile)


@app.route("/contact")
def contact_page():
    profile = load_profile()
    return render_template("contact.html", profile=profile)


@app.route("/Sachin_R_Karankal_CV.docx")
def download_cv():
    return send_from_directory(
        os.path.abspath(os.path.dirname(__file__)),
        "Sachin_R_Karankal_CV.docx",
        as_attachment=True,
        download_name="Sachin_R_Karankal_CV.docx"
    )


@app.route("/download-cv")
def download_cv_alias():
    return download_cv()


@app.route("/api/profile")
def profile_api():
    return jsonify(load_profile())


@app.route("/api/profile", methods=["POST"])
def save_profile():
    payload = request.get_json(silent=True) or {}
    db = get_database()
    if db is None:
        return jsonify({"status": "warning", "message": "MongoDB not connected. Data not saved."})

    db.profile.update_one({}, {"$set": payload}, upsert=True)
    return jsonify({"status": "success", "data": payload})


if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=int(os.getenv("PORT", "5000")))

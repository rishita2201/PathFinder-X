from flask import Flask, render_template, request, redirect, session, jsonify
from ai_engine import analyze_profile, extract_skills_from_file
import datetime

app = Flask(__name__)
app.secret_key = "super_secret_key"

USERNAME = "admin"
PASSWORD = "1234"

def log_audit(skills, career):
    with open("audit_log.txt", "a") as f:
        f.write(f"{datetime.datetime.now()} | {skills} | {career}\n")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] == USERNAME and request.form["password"] == PASSWORD:
            session["user"] = USERNAME
            return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")

@app.route("/")
def index():
    if "user" not in session:
        return redirect("/login")
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    skills = request.form.get("skills", "").lower()

    if "resume" in request.files and request.files["resume"].filename != "":
        file = request.files["resume"]
        skills += " " + extract_skills_from_file(file)

    data = analyze_profile(skills)

    log_audit(skills, data["results"][0]["career"])

    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
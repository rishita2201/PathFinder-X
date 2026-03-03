import pickle
import json
import PyPDF2
import docx
from sklearn.metrics.pairwise import cosine_similarity
from roadmaps import generate_roadmap

model = pickle.load(open("career_model.pkl", "rb"))
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))

with open("industry_trends.json") as f:
    industry_trends = json.load(f)

with open("career_insights.json") as f:
    career_insights = json.load(f)

career_skills = {
    "Data Scientist": ["python","statistics","machine learning","sql"],
    "AI Engineer": ["python","deep learning","neural networks","math"],
    "Web Developer": ["html","css","javascript","react"],
    "Cybersecurity Analyst": ["networking","linux","security","python"],
    "Cloud Engineer": ["aws","docker","kubernetes","linux"],
    "Software Developer": ["java","python","dsa","oop","git"],
    "DevOps Engineer": ["docker","kubernetes","ci/cd","linux","python"]
}

def extract_skills_from_file(file):
    text = ""

    if file.filename.endswith(".pdf"):
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            if page.extract_text():
                text += page.extract_text().lower()

    elif file.filename.endswith(".docx"):
        doc = docx.Document(file)
        for para in doc.paragraphs:
            text += para.text.lower()

    return text

def analyze_profile(skills_text):
    vec = vectorizer.transform([skills_text])
    probs = model.predict_proba(vec)[0]
    careers = model.classes_

    career_vectors = vectorizer.transform(careers)
    similarities = cosine_similarity(vec, career_vectors)[0]

    weighted = []

    for career, p, sim in zip(careers, probs, similarities):
        weight = industry_trends.get(career, 1.0)

        hybrid_score = (p * 0.6) + (sim * 0.4)
        final_score = hybrid_score * weight

        weighted.append((career, final_score))

    top3 = sorted(weighted, key=lambda x: x[1], reverse=True)[:3]

    results = []

    for career, score in top3:
        req = career_skills.get(career, [])

        matched = [s for s in req if s in skills_text]
        missing = [s for s in req if s not in skills_text]

        coverage = round((len(matched) / len(req)) * 100, 2) if req else 0

        insight = career_insights.get(career, {})

        results.append({
            "career": career,
            "confidence": round(score * 100, 2),
            "coverage": coverage,
            "missing": missing,
            "salary": insight.get("salary", "N/A"),
            "growth": insight.get("growth", "N/A"),
            "roadmap": generate_roadmap(missing)
        })

    resume_score = round(sum([r["coverage"] for r in results]) / len(results), 2)

    return {
        "results": results,
        "resume_score": resume_score
    }
from flask import Flask, render_template, request, redirect, url_for, session
import json, re
from difflib import SequenceMatcher

app = Flask(__name__)
app.secret_key = "supersecret"

# Quizzes laden
with open("quizzes.json", "r", encoding="utf-8") as f:
    quizzes = json.load(f)

# Benutzerstand speichern
def load_users():
    try:
        with open("users.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f)

def normalize(text):
    return re.sub(r"[^\w\s]", "", text.lower()).strip()

def is_correct(user_answer, correct_answer):
    return SequenceMatcher(None, normalize(user_answer), normalize(correct_answer)).ratio() > 0.8

# Startseite / Login
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        username = request.form["username"]
        session["username"] = username
        users = load_users()
        if username not in users:
            users[username] = {"money":0}
            save_users(users)
        return redirect(url_for("choose_topic"))
    return render_template("index.html")

# Themenauswahl
@app.route("/topics")
def choose_topic():
    if "username" not in session:
        return redirect(url_for("index"))
    return render_template("topics.html", quizzes=quizzes.keys())

# Quizseite
@app.route("/quiz/<topic>", methods=["GET","POST"])
def quiz(topic):
    if "username" not in session:
        return redirect(url_for("index"))
    fragen = quizzes[topic]
    index = int(request.args.get("index",0))
    
    if "score" not in session:
        session["score"] = 0

    if request.method == "POST":
        user_answer = request.form["answer"]
        if is_correct(user_answer, fragen[index]["antwort"]):
            session["score"] += 1
        index += 1
        if index < len(fragen):
            return redirect(url_for("quiz", topic=topic, index=index))
        else:
            users = load_users()
            username = session["username"]
            users[username]["money"] += session["score"] * 10
            save_users(users)
            score = session["score"]
            session.pop("score")
            return render_template("result.html", score=score, total=len(fragen), money=users[username]["money"])
    
    frage = fragen[index]["frage"]
    return render_template("quiz.html", topic=topic, frage=frage, index=index+1, total=len(fragen))

# Shopseite
@app.route("/shop")
def shop():
    if "username" not in session:
        return redirect(url_for("index"))
    users = load_users()
    money = users[session["username"]]["money"]
    items = [
        {"name":"Sticker", "price":50},
        {"name":"Hintergrundbild", "price":100},
        {"name":"Avatar", "price":150}
    ]
    return render_template("shop.html", money=money, items=items)

if __name__ == "__main__":
    app.run(debug=True)
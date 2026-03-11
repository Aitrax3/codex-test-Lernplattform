from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session
import json, re, secrets, random
from difflib import SequenceMatcher
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "supersecret"

# Quizzes laden
with open("quizzes.json", "r", encoding="utf-8") as f:
    quizzes = json.load(f)

SHOP_ITEMS = [
    {"name": "Sticker", "price": 50, "description": "Gib deinem Profil einen glitzernden Sticker.", "type": "sticker"},
    {"name": "Hintergrundbild", "price": 100, "description": "Versetze den Hintergrund in sanfte Farben.", "type": "background"},
    {"name": "Avatar", "price": 150, "description": "Schalte ein neues Avatar-Design frei und rüste es direkt aus.", "type": "avatar"},
]

STICKER_TIERS = [
    {"min_level": 1, "name": "Anfänger", "icons": ["🌟", "🎯", "🚀", "💡"]},
    {"min_level": 5, "name": "Fortgeschritten", "icons": ["🧠", "⚡", "🌀", "🌈"]},
    {"min_level": 10, "name": "Premium", "icons": ["🧬", "🪐", "🔥", "🧿"]},
    {"min_level": 15, "name": "Legendär", "icons": ["👑", "🫀", "🌌", "🔮"]},
]
AVATAR_SYMBOLS = ["★", "☀", "⚡", "❄", "♣"]
SYMBOL_POOL = ["☆","✦","✹","✺","✪","✖","✜","✿","❂","❉","✶","✵","✩","⚑","☘","❖","✧","✻","✸","✽"]
AVATAR_PRESETS = [
    {"label": "Aurora", "color": "#ec4899", "shape": "hexagon", "symbol": "⚡"},
    {"label": "Saphir", "color": "#3b82f6", "shape": "circle", "symbol": "★"},
    {"label": "Sonnenaufgang", "color": "#f97316", "shape": "square", "symbol": "☀"},
    {"label": "Nachtgrün", "color": "#047857", "shape": "circle", "symbol": "☾"},
    {"label": "Frost", "color": "#38bdf8", "shape": "hexagon", "symbol": "❄"},
]

EXPERIENCE_PER_CORRECT = 12
LEVEL_STEP = 100

ACHIEVEMENT_RULES = [
    ("Erstes Quiz abgeschlossen", lambda user: user.get("progress", {}).get("completed_quizzes", 0) >= 1),
    ("Sticker-Sammler", lambda user: len(user.get("stickers", [])) >= 5),
    ("Shop-Profi", lambda user: len(user.get("purchases", [])) >= 3),
    ("Reich", lambda user: user.get("money", 0) >= 200),
]

TOPIC_DESCRIPTIONS = {
    "Mathematik": "Kopfrechnen, Multiplikationen und leichte Gleichungen trainieren.",
    "Geografie": "Hauptstädte, Länder und Kontinente auf einen Blick.",
    "Informatik": "Abkürzungen und Grundbegriffe aus der digitalen Welt.",
    "Wissenschaft": "Physik, Chemie und Alltag aus der Naturwissenschaft.",
}

SUBTOPIC_DESCRIPTIONS = {
    "Mathematik": {
        "Arithmetik": "Addition, Subtraktion und grundlegende Rechnungen.",
        "Multiplikation": "Zahlenreihen und Multiplikationen von 5 bis 20.",
        "Division": "Einfache Divisionen mit geraden Ergebnissen.",
        "Gleichungen": "Lineare Gleichungen mit einer Unbekannten lösen.",
    },
    "Geografie": {
        "Hauptstädte": "Europa- und Welt-Hauptstädte plus berühmte Städte.",
        "Weltwissen": "Flüsse, Kontinente, Inseln und Ländergrenzen.",
    },
    "Informatik": {
        "Abkürzungen": "HTML, CSS, API und andere Kürzel deuten.",
        "Grundbegriffe": "Router, Browser, Cloud und andere Kernbegriffe.",
    },
    "Wissenschaft": {
        "Physik & Chemie": "Einheiten, Kräfte und physikalische Phänomene.",
        "Biologie & Alltag": "Natur, Körper und Alltagsthemen der Biologie.",
    },
}

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
    return re.sub(r"[^\w\säöüß]", "", text.lower()).strip()


def is_correct(user_answer, correct_answer, aliases=None):
    normalized_answer = normalize(user_answer)
    candidates = [correct_answer] + (aliases or [])
    for candidate in candidates:
        normalized_candidate = normalize(candidate)
        if normalized_answer == normalized_candidate:
            return True
        if normalized_answer.replace(" ", "") == normalized_candidate.replace(" ", ""):
            return True
        if SequenceMatcher(None, normalized_answer, normalized_candidate).ratio() > 0.7:
            return True
        candidate_words = set(normalized_candidate.split())
        answer_words = set(normalized_answer.split())
        if candidate_words and candidate_words.issubset(answer_words):
            return True
    return False


def default_avatar_state(label="Starter"):
    return {"label": label, "color": "#2563eb", "shape": "circle", "symbol": "★"}


def ensure_user_profile(users, username):
    user = users.setdefault(username, {})
    user.setdefault("money", 0)
    user.setdefault("purchases", [])
    user.setdefault("stickers", [])
    if "avatar" not in user:
        user["avatar"] = default_avatar_state()
    if "avatar_collection" not in user or not user["avatar_collection"]:
        user["avatar_collection"] = [default_avatar_state()]
    user.setdefault("symbol_library", AVATAR_SYMBOLS.copy())
    user.setdefault("avatar_counter", len(user.get("avatar_collection", [])))
    user.setdefault("progress", {"experience": 0, "level": 1, "completed_quizzes": 0})
    user.setdefault("achievements", [])
    user.setdefault("quiz_history", [])
    user.setdefault("last_quiz", None)
    user.setdefault("reset_code", None)
    return user


def recent_stickers(users, username, limit=20):
    user = ensure_user_profile(users, username)
    return user["stickers"][-limit:]


def unlocked_sticker_icons(level):
    icons = []
    for tier in sorted(STICKER_TIERS, key=lambda entry: entry["min_level"]):
        if level >= tier["min_level"]:
            icons.extend(tier["icons"])
    return icons or STICKER_TIERS[0]["icons"]


def next_sticker_tier(level):
    for tier in sorted(STICKER_TIERS, key=lambda entry: entry["min_level"]):
        if level < tier["min_level"]:
            return tier
    return None


def choose_new_symbol(user):
    library = user.setdefault("symbol_library", AVATAR_SYMBOLS.copy())
    candidates = [symbol for symbol in SYMBOL_POOL if symbol not in library]
    symbol = random.choice(candidates if candidates else SYMBOL_POOL)
    library.append(symbol)
    return symbol


def unlock_avatar(user):
    collection = user.setdefault("avatar_collection", [])
    owned_labels = {entry.get("label") for entry in collection}
    candidates = [preset for preset in AVATAR_PRESETS if preset["label"] not in owned_labels]
    selected = random.choice(candidates if candidates else AVATAR_PRESETS)
    user["avatar_counter"] = user.get("avatar_counter", 0) + 1
    symbol = choose_new_symbol(user)
    entry = {
        "label": f"{selected['label']} #{user['avatar_counter']}",
        "color": selected["color"],
        "shape": selected["shape"],
        "symbol": symbol,
    }
    collection.append(entry.copy())
    user["avatar"] = entry.copy()
    return entry


def build_topic_cards():
    cards = []
    for topic, subtopics in quizzes.items():
        total = sum(len(questions) for questions in subtopics.values())
        card = {
            "name": topic,
            "total_questions": total,
            "description": TOPIC_DESCRIPTIONS.get(topic, "Frische Fragen aus mehreren Untergruppen."),
            "subtopics": [],
        }
        for subtopic, questions in subtopics.items():
            card["subtopics"].append({
                "name": subtopic,
                "count": len(questions),
                "description": SUBTOPIC_DESCRIPTIONS.get(topic, {}).get(subtopic, "Frische Fragen, kein Frage-Dupe."),
            })
        cards.append(card)
    return cards


def create_user(users, username, password):
    if username in users:
        return False, "Benutzername existiert bereits."
    users[username] = {"password_hash": generate_password_hash(password, method="pbkdf2:sha256")}
    ensure_user_profile(users, username)
    return True, "Account erstellt."


def authenticate(users, username, password):
    user = users.get(username)
    if not user:
        return False
    password_hash = user.get("password_hash")
    if not password_hash:
        return False
    return check_password_hash(password_hash, password)


def award_experience(user, correct_count):
    progress = user.setdefault("progress", {"experience": 0, "level": 1, "completed_quizzes": 0})
    points = correct_count * EXPERIENCE_PER_CORRECT
    progress["experience"] += points
    progress["completed_quizzes"] += 1
    progress["level"] = 1 + progress["experience"] // LEVEL_STEP


def update_achievements(user):
    achievements = set(user.get("achievements", []))
    progress = user.get("progress", {})
    for name, condition in ACHIEVEMENT_RULES:
        if name not in achievements and condition(user):
            achievements.add(name)
    user["achievements"] = sorted(achievements)


def record_quiz_history(user, topic, subtopic, results, score):
    entry = {
        "topic": topic,
        "subtopic": subtopic,
        "results": results,
        "score": score,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }
    user["last_quiz"] = entry
    history = user.setdefault("quiz_history", [])
    history.append(entry)
    if len(history) > 12:
        history[:] = history[-12:]


def generate_reset_code():
    return secrets.token_hex(3)

# Startseite / Login
@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        users = load_users()
        if not username or not password:
            message = "Benutzername und Passwort ausfüllen."
        elif username not in users or not authenticate(users, username, password):
            message = "Ungültiger Benutzername oder Passwort."
        else:
            ensure_user_profile(users, username)
            session["username"] = username
            save_users(users)
            return redirect(url_for("choose_topic"))
    return render_template("index.html", message=message)


@app.route("/register", methods=["GET", "POST"])
def register():
    message = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        if not username or not password:
            message = "Benutzername und Passwort erforderlich."
        elif password != confirm:
            message = "Passwörter stimmen nicht überein."
        else:
            users = load_users()
            success, info = create_user(users, username, password)
            save_users(users)
            message = info
            if success:
                return redirect(url_for("index"))
    return render_template("register.html", message=message)


@app.route("/reset", methods=["GET", "POST"])
def reset_request():
    message = None
    code = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        users = load_users()
        if username not in users:
            message = "Benutzer nicht gefunden."
        else:
            code = generate_reset_code()
            users[username]["reset_code"] = code
            save_users(users)
            message = "Notiere dir den folgenden Code zur Bestätigung."
    return render_template("reset_request.html", message=message, code=code)


@app.route("/reset/confirm", methods=["GET", "POST"])
def reset_confirm():
    message = None
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        code = request.form.get("code", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        users = load_users()
        user = users.get(username)
        if not user:
            message = "Benutzer nicht gefunden."
        elif not code or code != user.get("reset_code"):
            message = "Falscher Code."
        elif not password or password != confirm:
            message = "Passwörter stimmen nicht überein."
        else:
            user["password_hash"] = generate_password_hash(password, method="pbkdf2:sha256")
            user["reset_code"] = None
            save_users(users)
            message = "Passwort wurde aktualisiert."
    return render_template("reset_confirm.html", message=message)


@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("score", None)
    session.pop("quiz_state", None)
    return redirect(url_for("index"))

# Themenauswahl
@app.route("/topics")
def choose_topic():
    if "username" not in session:
        return redirect(url_for("index"))
    users = load_users()
    username = session["username"]
    ensure_user_profile(users, username)
    stickers = recent_stickers(users, username)
    topic_cards = build_topic_cards()
    return render_template("topics.html", topic_cards=topic_cards, stickers=stickers)

# Quizseite
@app.route("/quiz/<topic>/<subtopic>", methods=["GET","POST"])
def quiz(topic, subtopic):
    if "username" not in session:
        return redirect(url_for("index"))
    index = int(request.args.get("index",0))
    quiz_state = session.get("quiz_state", {})
    topic_data = quizzes.get(topic)
    if not topic_data or subtopic not in topic_data:
        return redirect(url_for("choose_topic"))
    if quiz_state.get("topic") != topic or quiz_state.get("subtopic") != subtopic:
        available = topic_data[subtopic]
        count = min(10, len(available))
        questions = random.sample(available, k=count)
        quiz_state = {"topic": topic, "subtopic": subtopic, "questions": questions, "results": []}
        session["quiz_state"] = quiz_state
        session["score"] = 0
    fragen = quiz_state["questions"]
    users = load_users()
    username = session["username"]
    ensure_user_profile(users, username)
    stickers = recent_stickers(users, username)
    
    if "score" not in session:
        session["score"] = 0

    if request.method == "POST":
        user_answer = request.form["answer"]
        current_question = fragen[index]
        correct = is_correct(user_answer, current_question["antwort"], current_question.get("alias"))
        if correct:
            session["score"] += 1
        quiz_state.setdefault("results", []).append({
            "frage": current_question["frage"],
            "answer": user_answer,
            "expected": current_question["antwort"],
            "correct": correct
        })
        session["quiz_state"] = quiz_state
        index += 1
        if index < len(fragen):
            return redirect(url_for("quiz", topic=topic, subtopic=subtopic, index=index))
        else:
            user = users[username]
            user["money"] += session["score"] * 10
            total_questions = len(fragen)
            sticker_threshold = min(8, total_questions)
            sticker_awarded = session["score"] >= sticker_threshold
            if sticker_awarded:
                available = unlocked_sticker_icons(user["progress"]["level"])
                sticker = random.choice(available)
                user["stickers"].append(sticker)
            correct_count = sum(1 for entry in quiz_state.get("results", []) if entry["correct"])
            award_experience(user, correct_count)
            update_achievements(user)
            results = quiz_state.get("results", [])
            record_quiz_history(user, topic, subtopic, results, session["score"])
            save_users(users)
            score = session["score"]
            session.pop("score")
            stickers = recent_stickers(users, username)
            session.pop("quiz_state", None)
            return render_template(
                "result.html",
                score=score,
                total=total_questions,
                money=user["money"],
                stickers=stickers,
                sticker_awarded=sticker_awarded,
                results=results,
                sticker_threshold=sticker_threshold,
                topic=topic,
                subtopic=subtopic,
            )
    
    frage = fragen[index]["frage"]
    return render_template("quiz.html", topic=topic, subtopic=subtopic, frage=frage, index=index+1, total=len(fragen), stickers=stickers)

# Shopseite
@app.route("/shop", methods=["GET", "POST"])
def shop():
    if "username" not in session:
        return redirect(url_for("index"))
    users = load_users()
    username = session["username"]
    ensure_user_profile(users, username)
    stickers = recent_stickers(users, username)
    message = None
    user = users[username]
    if request.method == "POST":
        item_name = request.form.get("item")
        item = next((i for i in SHOP_ITEMS if i["name"] == item_name), None)
        if item is None:
            message = "Ungültiger Artikel."
        elif users[username]["money"] < item["price"]:
            message = "Du hast nicht genug Punkte für diesen Kauf."
        else:
            user["money"] -= item["price"]
            record = {
                "name": item["name"],
                "price": item["price"],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            user["purchases"].append(record)
            if item.get("type") == "avatar":
                new_avatar = unlock_avatar(user)
                message = f"Avatar {new_avatar['label']} freigeschaltet und direkt ausgerüstet!"
            else:
                message = f"{item['name']} erfolgreich gekauft!"
            save_users(users)
            stickers = recent_stickers(users, username)
    return render_template(
        "shop.html",
        money=users[username]["money"],
        items=SHOP_ITEMS,
        purchases=list(reversed(users[username]["purchases"][-5:])),
        message=message,
        avatar=users[username]["avatar"],
        stickers=stickers,
    )

@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("index"))
    users = load_users()
    username = session["username"]
    user = ensure_user_profile(users, username)
    purchases = list(reversed(user["purchases"]))
    total_spent = sum(p["price"] for p in user["purchases"])
    progress = user["progress"]
    next_level_exp = progress["level"] * LEVEL_STEP
    percent = int(min(100, progress["experience"] / max(next_level_exp, 1) * 100))
    available_stickers = unlocked_sticker_icons(progress["level"])
    upcoming_tier = next_sticker_tier(progress["level"])
    return render_template(
        "dashboard.html",
        money=user["money"],
        purchases=purchases,
        total_spent=total_spent,
        avatar=user["avatar"],
        stickers=recent_stickers(users, username),
        progress=progress,
        percent=percent,
        next_level_exp=next_level_exp,
        achievements=user["achievements"],
        last_quiz=user.get("last_quiz"),
        available_stickers=available_stickers,
        upcoming_tier=upcoming_tier,
    )

@app.route("/leaderboard")
def leaderboard():
    if "username" not in session:
        return redirect(url_for("index"))
    users = load_users()
    rankings = sorted(
        [
            {
                "name": name,
                "money": data.get("money", 0),
                "badges": len(data.get("stickers", [])),
                "purchases": len(data.get("purchases", [])),
            }
            for name, data in users.items()
        ],
        key=lambda entry: entry["money"],
        reverse=True,
    )
    username = session["username"]
    ensure_user_profile(users, username)
    return render_template(
        "leaderboard.html",
        rankings=rankings,
        stickers=recent_stickers(users, username),
    )

@app.route("/review")
def review():
    if "username" not in session:
        return redirect(url_for("index"))
    users = load_users()
    username = session["username"]
    user = ensure_user_profile(users, username)
    last_quiz = user.get("last_quiz")
    return render_template(
        "review.html",
        last_quiz=last_quiz,
        stickers=recent_stickers(users, username),
    )

@app.route("/avatar", methods=["GET", "POST"])
def avatar_design():
    if "username" not in session:
        return redirect(url_for("index"))
    users = load_users()
    username = session["username"]
    ensure_user_profile(users, username)
    message = None
    user = users[username]
    collection = user.setdefault("avatar_collection", [])
    if request.method == "POST":
        equip_label = request.form.get("equip_avatar")
        if equip_label:
            selection = next((entry for entry in collection if entry.get("label") == equip_label), None)
            if selection:
                user["avatar"] = selection.copy()
                message = f"Avatar {selection['label']} ausgerüstet."
        else:
            color = request.form.get("color", "#2563eb")
            shape = request.form.get("shape", "circle")
            symbol = request.form.get("symbol", "★")
            if symbol not in AVATAR_SYMBOLS:
                symbol = AVATAR_SYMBOLS[0]
            user["avatar"].update({"color": color, "shape": shape, "symbol": symbol})
            current_label = user["avatar"].get("label")
            for entry in collection:
                if entry.get("label") == current_label:
                    entry.update(user["avatar"])
            message = "Avatar gespeichert"
        save_users(users)
    return render_template(
        "avatar.html",
        avatar=user["avatar"],
        collection=collection,
        symbols=user.get("symbol_library", AVATAR_SYMBOLS),
        message=message,
        stickers=recent_stickers(users, username),
    )

if __name__ == "__main__":
    app.run(debug=True)

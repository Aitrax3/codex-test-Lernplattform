import os
from datetime import datetime, timedelta
from flask import Flask, render_template, render_template_string, request, redirect, url_for, session, jsonify
import json, re, secrets, random
import requests
from difflib import SequenceMatcher
from werkzeug.security import generate_password_hash, check_password_hash
from jinja2 import TemplateNotFound

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
QUIZZES_PATH = os.path.join(BASE_DIR, "quizzes.json")
USERS_PATH = os.path.join(BASE_DIR, "users.json")
CLASSES_PATH = os.path.join(BASE_DIR, "classes.json")

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)
app.secret_key = "supersecret"

NAV_MENU = [
    {"endpoint": "dashboard", "label": "Dashboard"},
    {"endpoint": "choose_topic", "label": "Themen", "roles": ["student"]},
    {"endpoint": "leaderboard", "label": "Rangliste", "roles": ["student"]},
    {"endpoint": "review", "label": "Review", "roles": ["student"]},
    {
        "endpoint": "teacher_portal",
        "label": "Feedback",
        "roles": ["teacher"],
        "fragment": "feedback",
        "view": "feedback-register",
    },
    {
        "endpoint": "teacher_portal",
        "label": "Klassenregister",
        "roles": ["teacher"],
        "fragment": "class-overview",
        "view": "class-register",
    },
    {
        "endpoint": "teacher_portal",
        "label": "Lehrer-Modus",
        "roles": ["teacher"],
        "fragment": "teacher-hub",
        "view": "teacher-hub",
    },
    {"endpoint": "shop", "label": "Shop"},
    {"endpoint": "avatar_design", "label": "Avatar"},
    {"endpoint": "logout", "label": "Abmelden"},
]


@app.context_processor
def inject_nav_links():
    username = session.get("username")
    user = None
    if username:
        users = load_users()
        user = users.get(username)
    nav_links = []
    for entry in NAV_MENU:
        roles = entry.get("roles")
        if roles and (not user or user.get("role") not in roles):
            continue
        url = entry.get("url")
        if not url:
            url = url_for(entry["endpoint"], **entry.get("params", {}))
            fragment = entry.get("fragment")
            if fragment:
                url = f"{url}#{fragment}"
        nav_links.append(
            {
                "url": url,
                "label": entry["label"],
                "view": entry.get("view"),
            }
        )
    return {"nav_links": nav_links}

# Quizzes laden
with open(QUIZZES_PATH, "r", encoding="utf-8") as f:
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

MODE_ORDER = ["leicht", "mittel", "schwer"]

MODE_LABELS = {
    "leicht": "Leicht",
    "mittel": "Mittel",
    "schwer": "Schwer",
}

GRACE_PERIOD = timedelta(minutes=5)

OPENAI_API_URL = os.getenv("OPENAI_API_URL", "https://api.openai.com/v1/chat/completions")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
OPENAI_TIMEOUT = int(os.getenv("OPENAI_TIMEOUT", "20"))

TOPIC_DESCRIPTIONS = {
    "Mathematik": "Rechentricks und Denksport in drei Schwierigkeitsstufen.",
    "Geografie": "Landkarten, Hauptstädte und Flüsse mit klaren Modus-Beschreibungen.",
    "Englisch": "Vokabeln, Verben und Phrasen sezierter Sprachwelten im Grundwortschatz.",
    "Geschichte": "Epochen, Entdeckungen und Weltgeschichte mit klaren Modi und Kontext-Hooks.",
}

# Benutzerstand speichern
def load_users():
    try:
        with open(USERS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_users(users):
    with open(USERS_PATH, "w", encoding="utf-8") as f:
        json.dump(users, f)


def load_classes():
    try:
        with open(CLASSES_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


def save_classes(classes):
    with open(CLASSES_PATH, "w", encoding="utf-8") as f:
        json.dump(classes, f, ensure_ascii=False, indent=2)

def normalize(text):
    text = (text or "").strip()
    return re.sub(r"[^\w\säöüß]", "", text.lower()).strip()


def resolve_question_answer(question):
    if not isinstance(question, dict):
        return None
    if question.get("antwort"):
        return question["antwort"]
    for key in ("answer", "translation", "word", "phrase", "country", "river", "location"):
        if question.get(key):
            return question[key]
    return None


def openai_configured():
    return bool(OPENAI_API_KEY)


def _extract_json_payload(text):
    if not text:
        return {}
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(text[start : end + 1])
            except json.JSONDecodeError:
                pass
    return {}


def _build_openai_prompt(topic, subtopic, mode, hint):
    context = f" Thema: {topic}, Unterthema: {subtopic}, Modus: {mode}." if topic else ""
    hint_text = f" Weitere Hinweise: {hint}." if hint else ""
    return (
        "Bitte formuliere eine altersgerechte Quizfrage auf Deutsch, mache sie klar und knapp und liefere die korrekte Antwort. "
        "Bitte gib ausschließlich ein JSON-Objekt zurück mit mindestens den Schlüsseln 'frage' und 'antwort'. "
        "Optional kannst du 'aliases' oder 'synonyme' als Liste ergänzen."
        " Gib keine weiteren Erklärungen außerhalb dieses JSON-Objekts."
        f"{context}{hint_text}"
    )


def build_live_quiz_questions(topic, subtopic, mode, count=10, hint=None):
    questions = []
    for i in range(count):
        question = generate_openai_question(topic, subtopic, mode, hint)
        question["id"] = secrets.token_hex(3)
        question.setdefault("source", "openai")
        questions.append(question)
    return questions


def generate_openai_question(topic="Allgemein", subtopic="Allgemein", mode="leicht", hint=None):
    if not openai_configured():
        raise RuntimeError("OPENAI_API_KEY fehlt. Setze die Umgebungsvariable.")
    messages = [
        {
            "role": "system",
            "content": (
                "Du bist ein Quizautor für Lernplattformen, der präzise deutsche Fragen erstellt und JSON zurückgibt."
                " Halte dich strikt an die Vorgabe, nur JSON ohne erklärenden Text zu liefern."
            ),
        },
        {"role": "user", "content": _build_openai_prompt(topic, subtopic, mode, hint)},
    ]
    payload = {
        "model": OPENAI_MODEL,
        "messages": messages,
        "temperature": 0.4,
        "max_tokens": 200,
    }
    try:
        response = requests.post(
            OPENAI_API_URL,
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=OPENAI_TIMEOUT,
        )
    except requests.RequestException as exc:
        raise RuntimeError(f"OpenAI-Anfrage fehlgeschlagen: {exc}") from exc
    response.raise_for_status()
    data = response.json()
    choices = data.get("choices") or []
    if not choices:
        raise RuntimeError("OpenAI hat keine Antwort geliefert.")
    content = ""
    message = choices[0].get("message") or {}
    if isinstance(message, dict):
        content = message.get("content", "")
    else:
        content = choices[0].get("text", "")
    parsed = _extract_json_payload(content)
    frage = parsed.get("frage") or parsed.get("question") or parsed.get("prompt")
    antwort = parsed.get("antwort") or parsed.get("answer")
    aliases = parsed.get("aliases") or parsed.get("synonyme") or parsed.get("alternatives")
    if not frage or not antwort:
        raise RuntimeError("OpenAI hat keine gültige Frage/Antwort zurückgegeben.")
    return {
        "frage": frage,
        "antwort": antwort,
        "aliases": normalize_list(aliases),
    }

def is_correct(user_answer, correct_answer, aliases=None):
    normalized_answer = normalize(user_answer)
    candidates = [candidate for candidate in ([correct_answer] + (aliases or [])) if candidate]
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


def normalize_list(value):
    if isinstance(value, list):
        return value
    if isinstance(value, (tuple, set)):
        return list(value)
    if value is None:
        return []
    return [value]


def ensure_user_profile(users, username):
    user = users.setdefault(username, {})
    user.setdefault("role", "student")
    user.setdefault("class_code", None)
    user.setdefault("classes", [])
    user.setdefault("money", 0)
    user.setdefault("purchases", [])
    user.setdefault("stickers", [])
    avatar = user.get("avatar")
    if not isinstance(avatar, dict):
        avatar = default_avatar_state()
    user["avatar"] = avatar
    avatar_collection = normalize_list(user.get("avatar_collection"))
    if not avatar_collection:
        avatar_collection = [default_avatar_state()]
    user["avatar_collection"] = avatar_collection
    symbol_library = normalize_list(user.get("symbol_library")) or AVATAR_SYMBOLS.copy()
    user["symbol_library"] = symbol_library
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
        total = sum(len(mode_data["questions"]) for subtopic in subtopics.values() for mode_data in subtopic["modes"].values())
        card = {
            "name": topic,
            "total_questions": total,
            "description": TOPIC_DESCRIPTIONS.get(topic, "Entdecke neue Quiz-Modi in jedem Thema."),
            "subtopics": [],
        }
        for subtopic_name, subtopic_data in subtopics.items():
            modes = []
            for mode in MODE_ORDER:
                mode_data = subtopic_data["modes"].get(mode)
                if not mode_data:
                    continue
                modes.append({
                    "key": mode,
                    "label": MODE_LABELS.get(mode, mode.title()),
                    "description": mode_data.get("description", ""),
                    "count": len(mode_data["questions"]),
                })
            card["subtopics"].append({
                "name": subtopic_name,
                "modes": modes,
            })
        cards.append(card)
    return cards


def build_quiz_questions(topic, subtopic, mode, count=10):
    if openai_configured():
        try:
            return build_live_quiz_questions(topic, subtopic, mode, count=count)
        except RuntimeError:
            pass
    topic_data = quizzes.get(topic, {})
    subtopic_data = topic_data.get(subtopic, {})
    mode_data = subtopic_data.get("modes", {}).get(mode, {})
    question_pool = mode_data.get("questions", [])
    if len(question_pool) <= count:
        questions = question_pool.copy()
    else:
        questions = random.sample(question_pool, k=count)
    for entry in questions:
        entry.setdefault("source", "static")
    return questions


def create_user(users, username, password, role="student", class_code=None):
    if username in users:
        return False, "Benutzername existiert bereits."
    entry = {
        "password_hash": generate_password_hash(password, method="pbkdf2:sha256"),
        "role": role,
    }
    if class_code:
        entry["class_code"] = class_code
    users[username] = entry
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


def record_quiz_history(user, topic, subtopic, mode, results, score):
    entry = {
        "topic": topic,
        "subtopic": subtopic,
        "mode": mode,
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


def parse_deadline(value):
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def format_deadline_display(value):
    if not value:
        return "ohne Deadline"
    parsed = parse_deadline(value)
    if parsed:
        return parsed.strftime("%d.%m.%Y %H:%M")
    return value


def deadline_grace_end(deadline):
    parsed = parse_deadline(deadline)
    if not parsed:
        return None
    return parsed + GRACE_PERIOD


def assignment_start_allowed(assignment, username):
    if not assignment:
        return False
    starts = assignment.get("starts", {})
    if username in starts:
        return True
    deadline = assignment.get("deadline")
    if not deadline:
        return True
    end = deadline_grace_end(deadline)
    if not end:
        return True
    return datetime.now() <= end


def grace_remaining_display(assignment):
    deadline = assignment.get("deadline")
    end = deadline_grace_end(deadline)
    if not end:
        return None
    remaining = end - datetime.now()
    if remaining.total_seconds() <= 0:
        return None
    minutes = int(remaining.total_seconds() // 60)
    if minutes <= 0:
        return "weniger als 1 Minute"
    return f"{minutes} Minuten"


def is_deadline_open(value):
    parsed = parse_deadline(value)
    if not parsed:
        return True
    return datetime.now() <= parsed


def assignment_is_visible(assignment):
    if not assignment:
        return False
    if is_deadline_open(assignment.get("deadline")):
        return True
    starts = assignment.get("starts") or {}
    return bool(starts)


def cleanup_class_assignments(class_data):
    if not class_data:
        return False
    assignments = class_data.get("assignments", [])
    updated = False
    visible = []
    for assignment in assignments:
        if assignment_is_visible(assignment):
            visible.append(assignment)
        else:
            updated = True
    if updated:
        class_data["assignments"] = visible
    return updated


def cleanup_all_classes(classes):
    changed = False
    for class_data in classes.values():
        if cleanup_class_assignments(class_data):
            changed = True
    return changed




def generate_class_code(existing):
    while True:
        code = secrets.token_hex(3).upper()
        if code not in existing:
            return code


def build_student_stats(students, users):
    stats = []
    for student in sorted(students):
        user = users.get(student)
        if not user:
            continue
        progress = user.get("progress", {})
        last_quiz = user.get("last_quiz") or {}
        stats.append({
            "name": student,
            "quizzes": progress.get("completed_quizzes", 0),
            "experience": progress.get("experience", 0),
            "last_quiz": last_quiz.get("timestamp"),
        })
    return stats


def student_submission_overview(class_data, users):
    overview = []
    for student in sorted(class_data.get("students", [])):
        user = users.get(student)
        if not user:
            continue
        last = user.get("last_quiz")
        timestamp = last.get("timestamp") if last else None
        total = len(last.get("results", [])) if last else 0
        score = last.get("score", 0) if last else 0
        percent = f"{int(score / total * 100)}%" if total else "–"
        overview.append({
            "name": student,
            "submission": timestamp or "Keine Abgabe",
            "percent": percent,
        })
    return overview

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
    selected_role = "student"
    class_code_value = ""
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")
        selected_role = request.form.get("role", "student")
        class_code_value = request.form.get("class_code", "").strip()
        class_code = class_code_value.upper() if class_code_value else None
        classes = load_classes() if selected_role == "student" and class_code else None
        if not username or not password:
            message = "Benutzername und Passwort erforderlich."
        elif password != confirm:
            message = "Passwörter stimmen nicht überein."
        elif selected_role == "student" and class_code and (classes is None or class_code not in classes):
            message = "Ungültiger Klassen-Code."
        else:
            users = load_users()
            success, info = create_user(
                users,
                username,
                password,
                role=selected_role,
                class_code=class_code if selected_role == "student" else None,
            )
            message = info
            if success:
                if selected_role == "student" and class_code and classes:
                    entry = classes[class_code]
                    if username not in entry.get("students", []):
                        entry.setdefault("students", []).append(username)
                    save_classes(classes)
                save_users(users)
                return redirect(url_for("index"))
    return render_template(
        "register.html",
        message=message,
        selected_role=selected_role,
        class_code_value=class_code_value,
    )


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
    classes = load_classes()
    if cleanup_all_classes(classes):
        save_classes(classes)
    if cleanup_all_classes(classes):
        save_classes(classes)
    student_assignments = []
    class_name = None
    user = users[username]
    if user.get("role") == "student" and user.get("class_code"):
        class_data = classes.get(user["class_code"])
        if class_data:
            class_name = class_data.get("name")
            if cleanup_class_assignments(class_data):
                save_classes(classes)
            if cleanup_class_assignments(class_data):
                save_classes(classes)
            assignments = list(reversed(class_data.get("assignments", [])))
            for assignment in assignments[:3]:
                student_assignments.append({
                    "topic": assignment["topic"],
                    "subtopic": assignment["subtopic"],
                    "mode": assignment["mode"],
                    "mode_label": MODE_LABELS.get(assignment["mode"], assignment["mode"].title()),
                    "created": assignment.get("created"),
                    "deadline": format_deadline_display(assignment.get("deadline")),
                })
    is_teacher = user.get("role") == "teacher"
    return render_template(
        "topics.html",
        topic_cards=topic_cards,
        stickers=stickers,
        is_teacher=is_teacher,
        student_assignments=student_assignments,
        class_name=class_name,
        mode_labels=MODE_LABELS,
    )


@app.route("/teacher", methods=["GET", "POST"])
def teacher_portal():
    if "username" not in session:
        return redirect(url_for("index"))
    users = load_users()
    username = session["username"]
    user = ensure_user_profile(users, username)
    if user.get("role") != "teacher":
        return redirect(url_for("choose_topic"))
    classes = load_classes()
    stickers = recent_stickers(users, username)
    message = None
    if request.method == "POST":
        action = request.form.get("action")
        if action == "create_class":
            class_name = request.form.get("class_name", "").strip()
            if not class_name:
                message = "Gib einen Klassennamen ein."
            else:
                code = generate_class_code(classes)
                classes[code] = {
                    "name": class_name,
                    "teacher": username,
                    "students": [],
                    "assignments": [],
                }
                save_classes(classes)
                user.setdefault("classes", [])
                if code not in user["classes"]:
                    user["classes"].append(code)
                save_users(users)
                message = f"Klasse '{class_name}' erstellt. Code: {code}"
        elif action == "assign_quiz":
            class_code = request.form.get("class_code")
            target = request.form.get("assignment_target")
            mode = request.form.get("mode")
            deadline_raw = request.form.get("deadline", "").strip()
            deadline_value = None
            invalid_deadline = False
            if deadline_raw:
                parsed_deadline = parse_deadline(deadline_raw)
                if parsed_deadline:
                    deadline_value = parsed_deadline.isoformat(timespec="minutes")
                else:
                    message = "Ungültiges Datum für die Deadline."
                    invalid_deadline = True
            if not invalid_deadline:
                if not class_code or class_code not in classes or classes[class_code].get("teacher") != username:
                    message = "Ungültige Klasse."
                elif not target or "|" not in target:
                    message = "Wähle ein Thema und Unterthema."
                elif mode not in MODE_ORDER:
                    message = "Wähle einen Modus."
                else:
                    topic, subtopic = target.split("|", 1)
                    assignment = {
                        "id": secrets.token_hex(4),
                        "topic": topic,
                        "subtopic": subtopic,
                        "mode": mode,
                        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "deadline": deadline_value,
                        "feedback": [],
                    }
                    classes[class_code].setdefault("assignments", []).append(assignment)
                    save_classes(classes)
                    message = (
                        f"Quiz '{topic} – {subtopic}' ({MODE_LABELS.get(mode, mode)}) "
                        f"an Klasse {class_code} verteilt."
                    )
        else:
            message = "Aktion nicht erkannt."
    teacher_classes = []
    for code, data in sorted(classes.items()):
        if data.get("teacher") != username:
            continue
        students = data.get("students", [])
        structured_assignments = []
        for assignment in reversed(data.get("assignments", [])):
            if not assignment_is_visible(assignment):
                continue
            open_status = is_deadline_open(assignment.get("deadline"))
            grace_msg = None
            if not open_status:
                grace_msg = grace_remaining_display(assignment)
            if open_status:
                status_label = "Offen"
            elif grace_msg:
                status_label = "Verlängert"
            else:
                status_label = "Abgelaufen"
            structured_assignments.append({
                "id": assignment["id"],
                "topic": assignment["topic"],
                "subtopic": assignment["subtopic"],
                "mode": assignment["mode"],
                "mode_label": MODE_LABELS.get(assignment["mode"], assignment["mode"].title()),
                "created": assignment.get("created"),
                "deadline": assignment.get("deadline"),
                "deadline_display": format_deadline_display(assignment.get("deadline")),
                "is_open": open_status,
                "status_label": status_label,
                "grace_message": grace_msg,
                "feedback": list(reversed(assignment.get("feedback", []))),
            })
        teacher_classes.append({
            "code": code,
            "name": data.get("name"),
            "students": build_student_stats(students, users),
            "assignments": structured_assignments,
        })
    teacher_class_choices = [
        {"code": entry["code"], "label": f"{entry['name']} ({entry['code']})"}
        for entry in teacher_classes
    ]
    selected_class_code = request.args.get("class", teacher_class_choices[0]["code"] if teacher_class_choices else None)
    selected_class = classes.get(selected_class_code) if selected_class_code else None
    student_overview = student_submission_overview(selected_class, users) if selected_class else []
    topic_options = []
    for topic, subtopics in quizzes.items():
        for subtopic_name in subtopics.keys():
            topic_options.append({
                "value": f"{topic}|{subtopic_name}",
                "label": f"{topic} · {subtopic_name}",
            })
    return render_template(
        "teacher.html",
        stickers=stickers,
        message=message,
        teacher_classes=teacher_classes,
        teacher_class_choices=teacher_class_choices,
        topic_options=topic_options,
        mode_labels=MODE_LABELS,
        selected_class_code=selected_class_code,
        student_overview=student_overview,
        selected_class_name=selected_class.get("name") if selected_class else None,
    )

# Quizseite
@app.route("/quiz/<topic>/<subtopic>/<mode>", methods=["GET", "POST"])
def quiz(topic, subtopic, mode):
    if "username" not in session:
        return redirect(url_for("index"))
    index = int(request.args.get("index", 0))
    quiz_state = session.get("quiz_state", {})
    topic_data = quizzes.get(topic)
    if not topic_data:
        return redirect(url_for("choose_topic"))
    subtopic_data = topic_data.get(subtopic)
    if not subtopic_data:
        return redirect(url_for("choose_topic"))
    mode_data = subtopic_data["modes"].get(mode)
    if not mode_data:
        return redirect(url_for("choose_topic"))
    question_pool = mode_data["questions"]
    if (
        quiz_state.get("topic") != topic
        or quiz_state.get("subtopic") != subtopic
        or quiz_state.get("mode") != mode
    ):
        questions = build_quiz_questions(topic, subtopic, mode, count=10)
        quiz_state = {
            "topic": topic,
            "subtopic": subtopic,
            "mode": mode,
            "questions": questions,
            "results": [],
        }
        session["quiz_state"] = quiz_state
        session["score"] = 0
        index = 0
    questions = quiz_state["questions"]
    users = load_users()
    username = session["username"]
    assignment_id = request.args.get("assignment_id")
    class_assignment = None
    classes = load_classes()
    class_code = users.get(username, {}).get("class_code")
    if assignment_id and class_code and class_code in classes:
        class_assignments = classes[class_code].get("assignments", [])
        class_assignment = next((entry for entry in class_assignments if entry.get("id") == assignment_id), None)
    if class_assignment:
        if not assignment_start_allowed(class_assignment, username):
            session["assignment_error"] = "Die Deadline wurde überschritten, das Quiz ist gesperrt."
            return redirect(url_for("dashboard"))
        starts = class_assignment.setdefault("starts", {})
        if username not in starts:
            starts[username] = datetime.now().isoformat(timespec="minutes")
            save_classes(classes)
    ensure_user_profile(users, username)
    stickers = recent_stickers(users, username)

    if "score" not in session:
        session["score"] = 0

    if request.method == "POST":
        user_answer = request.form["answer"]
        current_question = questions[index]
        expected_answer = resolve_question_answer(current_question)
        answer_for_check = expected_answer if expected_answer is not None else current_question.get("antwort")
        correct = is_correct(user_answer, answer_for_check, current_question.get("aliases"))
        if correct:
            session["score"] += 1
        entry_expected = expected_answer or current_question.get("antwort") or "Keine Angabe"
        quiz_state.setdefault("results", []).append({
            "frage": current_question["frage"],
            "answer": user_answer,
            "expected": entry_expected,
            "correct": correct
        })
        session["quiz_state"] = quiz_state
        index += 1
        if index < len(questions):
            return redirect(url_for("quiz", topic=topic, subtopic=subtopic, mode=mode, index=index, assignment_id=assignment_id))
        else:
            user = users[username]
            user["money"] += session["score"] * 10
            total_questions = len(questions)
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
            record_quiz_history(user, topic, subtopic, mode, results, session["score"])
            save_users(users)
            classes_dirty = False
            if class_assignment:
                starts = class_assignment.get("starts", {})
                if username in starts:
                    starts.pop(username, None)
                    classes_dirty = True
                class_data = classes.get(class_code) if class_code else None
                if class_data and cleanup_class_assignments(class_data):
                    classes_dirty = True
            if classes_dirty:
                save_classes(classes)
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
                mode_label=MODE_LABELS.get(mode, mode.title()),
                assignment_id=assignment_id,
            )

    frage = questions[index]["frage"]
    return render_template(
        "quiz.html",
        topic=topic,
        subtopic=subtopic,
        mode_label=MODE_LABELS.get(mode, mode.title()),
        frage=frage,
        index=index+1,
        total=len(questions),
        stickers=stickers,
        assignment_id=assignment_id,
    )

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

@app.route("/dashboard", methods=["GET", "POST"])
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
    classes = load_classes()
    if cleanup_all_classes(classes):
        save_classes(classes)
    class_assignments = []
    class_name = None
    feedback_note = None
    assignment_error = session.pop("assignment_error", None)
    class_data = None
    if user.get("role") == "student" and user.get("class_code"):
        class_data = classes.get(user["class_code"])
        if class_data:
            class_name = class_data.get("name")
    if request.method == "POST" and user.get("role") == "student" and class_data:
        action = request.form.get("action")
        if action == "feedback":
            assignment_id = request.form.get("assignment_id")
            message_text = request.form.get("feedback", "").strip()
            assignment = next((a for a in class_data.get("assignments", []) if a["id"] == assignment_id), None)
            if not assignment:
                feedback_note = "Aufgabe nicht gefunden."
            elif not message_text:
                feedback_note = "Feedback darf nicht leer sein."
            else:
                assignment.setdefault("feedback", []).append({
                    "student": username,
                    "message": message_text,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
                })
                save_classes(classes)
                feedback_note = "Feedback wurde gesendet."
        else:
            feedback_note = "Aktion nicht erlaubt."
    if class_data:
        for assignment in class_data.get("assignments", []):
            if not assignment_is_visible(assignment):
                continue
            deadline = assignment.get("deadline")
            deadline_label = format_deadline_display(deadline)
            open_status = is_deadline_open(deadline)
            started = username in assignment.get("starts", {})
            start_allowed = assignment_start_allowed(assignment, username)
            grace_msg = None
            if not started and start_allowed and not open_status:
                grace_msg = grace_remaining_display(assignment)
            if open_status:
                status_label = "Offen"
            elif grace_msg:
                status_label = "Verlängert"
            else:
                status_label = "Abgelaufen"
            class_assignments.append({
                "id": assignment["id"],
                "topic": assignment["topic"],
                "subtopic": assignment["subtopic"],
                "mode": assignment["mode"],
                "mode_label": MODE_LABELS.get(assignment["mode"], assignment["mode"].title()),
                "deadline_display": deadline_label,
                "is_open": open_status,
                "status_label": status_label,
                "start_allowed": start_allowed,
                "started": started,
                "grace_message": grace_msg,
                "feedback_count": len(assignment.get("feedback", [])),
            })
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
        assignments=class_assignments,
        class_code=user.get("class_code"),
        class_name=class_name,
        feedback_note=feedback_note,
        assignment_error=assignment_error,
        mode_labels=MODE_LABELS,
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
            if data.get("role") != "teacher"
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
        mode_labels=MODE_LABELS,
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


@app.route("/api/generate-question", methods=["POST"])
def api_generate_question():
    payload = request.get_json(silent=True) or {}
    topic = payload.get("topic", "Allgemein")
    subtopic = payload.get("subtopic", "Allgemein")
    mode = payload.get("mode", "leicht")
    hint = payload.get("hint")
    if not openai_configured():
        return jsonify(error="OpenAI nicht konfiguriert"), 503
    try:
        question = generate_openai_question(topic, subtopic, mode, hint)
    except RuntimeError as exc:
        return jsonify(error=str(exc)), 502
    return jsonify(question=question)


@app.errorhandler(TemplateNotFound)
def handle_missing_template(error):
    template_name = getattr(error, "name", "unbekannt")
    return render_template_string(
        """<!DOCTYPE html>
<html><head><title>Datei nicht gefunden</title></head><body>
<div style='font-family:Inter,system-ui,sans-serif;padding:2rem;text-align:center;'>
<h1>Template '{{ template_name }}' fehlt</h1>
<p>Bitte lege die Datei unter <code>templates/{{ template_name }}</code> ab.</p>
</div></body></html>""",
        template_name=template_name,
    ), 500

if __name__ == "__main__":
    app.run(debug=True)

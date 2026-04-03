import shutil

import pytest

import app as learning_app


@pytest.fixture(autouse=True)
def isolate_files(tmp_path):
    original_users = learning_app.USERS_PATH
    original_classes = learning_app.CLASSES_PATH
    tmp_users = tmp_path / "users.json"
    tmp_classes = tmp_path / "classes.json"
    shutil.copy(original_users, tmp_users)
    shutil.copy(original_classes, tmp_classes)
    learning_app.USERS_PATH = str(tmp_users)
    learning_app.CLASSES_PATH = str(tmp_classes)
    yield
    learning_app.USERS_PATH = original_users
    learning_app.CLASSES_PATH = original_classes


@pytest.fixture
def client(isolate_files):
    learning_app.app.config["TESTING"] = True
    with learning_app.app.test_client() as client_instance:
        yield client_instance


def login_as(client_instance, username):
    with client_instance.session_transaction() as sess:
        sess["username"] = username


def test_index_page(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Willkommen" in response.data


def test_register_page(client):
    response = client.get("/register")
    assert response.status_code == 200
    assert b"Registrieren" in response.data


def test_topics_requires_login(client):
    response = client.get("/topics")
    assert response.status_code == 302
    assert response.headers.get("Location", "").endswith("/")


def test_topics_page_for_student(client):
    login_as(client, "test-S")
    response = client.get("/topics")
    assert response.status_code == 200
    assert "Themenübersicht".encode("utf-8") in response.data


def test_student_redirected_from_teacher_portal(client):
    login_as(client, "test-S")
    response = client.get("/teacher")
    assert response.status_code == 302
    assert response.headers.get("Location", "").endswith("/topics")


def test_teacher_portal_loads_for_teacher(client):
    login_as(client, "test-L")
    response = client.get("/teacher")
    assert response.status_code == 200
    assert "Lehrer-Modus".encode("utf-8") in response.data


def test_feedback_page_student(client):
    login_as(client, "test-S")
    response = client.get("/feedback")
    assert response.status_code == 200
    assert b"Lernassistent" in response.data


def test_feedback_page_teacher(client):
    login_as(client, "test-L")
    response = client.get("/feedback")
    assert response.status_code == 200
    assert b"Feedback-Register" in response.data


def test_class_register_page(client):
    login_as(client, "test-L")
    response = client.get("/teacher/classes")
    assert response.status_code == 200
    assert b"Klassenregister" in response.data

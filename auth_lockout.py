"""Login-Lockout-Logik für LoopWise.

In-Memory-Store. Bei mehreren Workern läuft der State pro Prozess,
für Single-Region-Deployment (Fly.io fra) ausreichend.
"""
from datetime import datetime, timedelta

LOGIN_MAX_ATTEMPTS = 3
LOGIN_ATTEMPT_WINDOW = timedelta(minutes=15)
LOGIN_LOCKOUT_DURATIONS = [
    timedelta(minutes=5),
    timedelta(minutes=15),
    timedelta(minutes=60),
]

_failed_attempts = {}
_lockouts = {}


def _keys(username, ip):
    keys = []
    if username:
        keys.append(("user", username))
    if ip:
        keys.append(("ip", ip))
    return keys


def _prune(key, now):
    attempts = _failed_attempts.get(key)
    if not attempts:
        return []
    cutoff = now - LOGIN_ATTEMPT_WINDOW
    fresh = [ts for ts in attempts if ts >= cutoff]
    if fresh:
        _failed_attempts[key] = fresh
    else:
        _failed_attempts.pop(key, None)
    return fresh


def _remaining_seconds(key, now):
    entry = _lockouts.get(key)
    if not entry:
        return 0
    locked_until, _stage = entry
    if locked_until <= now:
        return 0
    return int((locked_until - now).total_seconds())


def check_lockout(username, ip):
    """Gibt verbleibende Lockout-Sekunden zurück (0 = nicht gesperrt)."""
    now = datetime.now()
    remaining = 0
    for key in _keys(username, ip):
        seconds = _remaining_seconds(key, now)
        if seconds > remaining:
            remaining = seconds
    return remaining


def register_failure(username, ip):
    """Zählt einen Fehlversuch. Gibt Lockout-Sekunden zurück, falls ausgelöst."""
    now = datetime.now()
    triggered = 0
    for key in _keys(username, ip):
        attempts = _prune(key, now)
        attempts.append(now)
        _failed_attempts[key] = attempts
        if len(attempts) >= LOGIN_MAX_ATTEMPTS:
            previous_stage = _lockouts.get(key, (None, 0))[1]
            stage_index = min(previous_stage, len(LOGIN_LOCKOUT_DURATIONS) - 1)
            duration = LOGIN_LOCKOUT_DURATIONS[stage_index]
            _lockouts[key] = (now + duration, previous_stage + 1)
            _failed_attempts.pop(key, None)
            seconds = int(duration.total_seconds())
            if seconds > triggered:
                triggered = seconds
    return triggered


def clear_failures(username, ip):
    for key in _keys(username, ip):
        _failed_attempts.pop(key, None)
        _lockouts.pop(key, None)


def reset_state():
    _failed_attempts.clear()
    _lockouts.clear()


def format_duration(seconds):
    if seconds <= 0:
        return None
    minutes = (seconds + 59) // 60
    if minutes < 60:
        return f"{minutes} Minute" if minutes == 1 else f"{minutes} Minuten"
    hours = minutes // 60
    return f"{hours} Stunde" if hours == 1 else f"{hours} Stunden"


def lockout_message(seconds):
    return (
        "Konto vorübergehend gesperrt wegen zu vieler Fehlversuche. "
        f"Bitte in {format_duration(seconds)} erneut versuchen."
    )

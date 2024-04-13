import threading
import time

timers = {}
lock = threading.Lock()


def start_timer(session_id: str):
    with lock:
        timers[session_id] = time.time()


def end_timer(session_id: str):
    with lock:
        if session_id in timers:
            start_time = timers.pop(session_id)
            return time.time() - start_time
        else:
            return None


def calculate_score(correct, total):
    return correct / total * 100




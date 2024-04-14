import threading
import time

timers = {}
lock = threading.Lock()


def start_timer(session_id: str):
    with lock:
        timers[session_id] = time.time()
        print(f"Timer started for {session_id}: {timers[session_id]}")


def end_timer(session_id: str):
    with lock:
        if session_id in timers:
            start_time = timers.pop(session_id)
            print(f"Timer ended for {session_id}")
            return time.time() - start_time
        else:
            print(f"Warning: Timer for session ID {session_id} not found.")
            return None


def calculate_score(correct, total):
    with lock:
        return correct / total * 100




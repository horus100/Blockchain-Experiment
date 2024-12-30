import time
import psutil
import os
import json
from datetime import datetime

BASE_LOG_DIR = "/home/nodo/" + "log/analysis"
ANALYSIS_FILE = os.path.join(BASE_LOG_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.json")


def _ensure_log_directory():

    if not os.path.exists(BASE_LOG_DIR):
        os.makedirs(BASE_LOG_DIR)
        print(f"Directorio creado: {BASE_LOG_DIR}")


def start_timer():

    return time.time()



def measure_resources_before():

    process = psutil.Process()
    cpu_before = process.cpu_percent(interval=None)
    mem_before = process.memory_info().rss
    return cpu_before, mem_before


def measure_resources_after(state, cpu_before, mem_before,start_time):

    process = psutil.Process()
    cpu_after = process.cpu_percent(interval=None)
    mem_after = process.memory_info().rss

    cpu_diff = cpu_after - cpu_before
    mem_diff = mem_after - mem_before

    end_time = time.time()
    elapsed = end_time - start_time

    log_data = {
        "state": state,
        "latency": elapsed,
        "cpu": cpu_diff,
        "ram": mem_diff
    }
    _write_to_file(log_data)


def _write_to_file(data):

    _ensure_log_directory()
    if os.path.exists(ANALYSIS_FILE):
        with open(ANALYSIS_FILE, "r+") as f:
            existing_data = json.load(f)
            existing_data.append(data)
            f.seek(0)
            json.dump(existing_data, f, indent=4)
    else:
        with open(ANALYSIS_FILE, "w") as f:
            json.dump([data], f, indent=4)


def salt():
    """Registra una separación para identificar diferentes pruebas."""
    log_data = {"separator": "##########################################################################################"}
    _write_to_file(log_data)

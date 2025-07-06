from celery import Celery
import os
from scanner import run_scan

app = Celery("tasks", broker=os.getenv("REDIS_URL"))

@app.task
def perform_scan_task(url, deep, scan_type):
    return run_scan(url, deep, scan_type)
  

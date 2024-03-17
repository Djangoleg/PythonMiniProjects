from celery import Celery

from config import RUN_UPDATE_CURRENCY_RATE_TASK_CRONE, TIME_ZONE

app = Celery("currency")

app.conf.timezone = TIME_ZONE

app.config_from_object("config", namespace="CELERY")

app.conf.beat_schedule = {
    "every_day_three_o_clock": {
        "task": "celery_tasks.update_currency_rate_task",
        "schedule": RUN_UPDATE_CURRENCY_RATE_TASK_CRONE,
    }
}

# Load tasks from all registered Django app configs.
# app.autodiscover_tasks(lambda: ("celery_tasks", ))
app.conf.imports = ("celery_tasks",)

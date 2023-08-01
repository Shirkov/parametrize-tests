import pytz

from datetime import datetime
from services.request_service import Request
from settings.query_data import eu_moscow_tz
from start_tests import LOG


def fetch_tasks(url, username, password, params: dict):
    task_list = []

    request = Request(url=url)
    request.auth(username=username,
                 password=password)
    rsp = request.rpc_request(
        params=params)

    for task in rsp["result"]["data"]:
        task_list.append(task)

    return task_list


def make_task_key(id, name, system, engine=None):
    if engine:
        task_key = id + "|" + name + "|" + engine + "|" + system
    else:
        task_key = id + "|" + name + "|" + system

    return task_key


def get_current_local_date(timezone):
    tz = pytz.timezone(timezone)
    now_utc = datetime.utcnow()

    return now_utc.replace(tzinfo=pytz.utc).astimezone(tz).today()


def is_not_valid_mostro_search_sync_task(task):
    if task.get("status", {}).get("value", {}).get("status", True) is False:
        LOG.error(f"Task [{task['id']['id']}] {task['engine_label']['value']} is not valid")
        return True

    return False


def is_not_valid_task(task):
    if task.get("exit_code", None) == 1 and task.get("active", None) is True:
        LOG.error(f"Task [{task['id']}] {task['name']} is not valid  -- exit_code {task['exit_code']}")
        return True

    return False


def is_not_valid_status_change_sync_task(task):
    current_datetime = get_current_local_date(timezone=eu_moscow_tz)

    datetime_task = task.get("status_change", None)
    datetime_task_obj = datetime.strptime(datetime_task, '%Y-%m-%dT%H:%M:%S.%f')

    if (current_datetime - datetime_task_obj).days >= 1:
        LOG.error(f"Task [{task['id']}] {task['name']} is not valid  -- status_change: {datetime_task}")

        return True

    return False

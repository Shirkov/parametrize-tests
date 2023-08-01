import os
import json

from settings.query_data import SystemName
from settings.env_config import settings


def get_allure_report_data(allure_report_dir):
    path_to_file = os.path.join(allure_report_dir, 'allure-report', 'widgets', 'duration.json')
    with open(path_to_file, "r", encoding='utf-8') as f:
        data = json.load(f)
        return data


def get_allure_link(env_name):
    try:
        allure_link = os.environ[env_name]
    except (KeyError, TypeError):
        allure_link = "link not found"

    return allure_link


def parse_task_key(task_name, system):
    three_parts = 3
    four_parts = 4

    task_parts = task_name.strip("test_tasks").strip(f"{system.lower()}").strip("[").strip("]").split("|")
    if len(task_parts) == three_parts:
        id, name, system_name = task_parts
        engine = None

    elif len(task_parts) == four_parts:
        id, name, system_name, engine = task_parts

    else:
        id = None
        name = None
        system_name = None
        engine = None

    return id, name, system_name, engine


def generate_link_task_name(url, id, task_name, system):
    if system in [SystemName.MOSTRO_PIM,
                  SystemName.MOSTRO_SEARCH_SYNC,
                  SystemName.SYNC,
                  SystemName.STATUS_UNCHANGED_SYNC]:
        link_task_name = f"<a href='{url}{id}/edit'>{task_name}</a>"

    elif system in [SystemName.SEARCH]:
        link_task_name = f"<a href='{url}{id}'>{task_name}</a>"

    else:
        raise TypeError(f"link_task_name is not formed")

    return link_task_name


def generate_url_for_task_link(system, engine):
    if system == SystemName.SEARCH:
        url = f"{settings.search.host}/engine/{engine}/tasks/"

    elif system in [SystemName.MOSTRO_PIM]:
        url = f"{settings.mostro_pim.host}/system/tasks/"

    elif system in [SystemName.SYNC, SystemName.STATUS_UNCHANGED_SYNC]:
        url = f"{settings.sync.host}/settings/tasks/"

    elif system == SystemName.MOSTRO_SEARCH_SYNC:
        url = f"{settings.mostro_search_sync.host}/settings/sync/"

    else:
        raise TypeError(f"url is not formed")

    return url


def generate_failed_task_list(data, system):
    fail_test_list = []

    for test_item in data:
        if test_item["status"] != "passed" and "test_tasks" in test_item["name"]:
            id, task_name, sys_name, engine = parse_task_key(test_item["name"], system=system)
            if system == sys_name:
                url = generate_url_for_task_link(sys_name, engine=engine)
                link_task_name = generate_link_task_name(url=url, id=id, system=sys_name, task_name=task_name)
                fail_test_list.append(link_task_name)
                fail_test_list.sort()

    return "\n".join(fail_test_list)

import pytest
from settings.query_data import SystemName, sync_param, mostro_search_sync_param, search_param, mostro_pim_param

from services.task_services import fetch_tasks, make_task_key, is_not_valid_task, is_not_valid_mostro_search_sync_task, \
    is_not_valid_status_change_sync_task
from settings.env_config import settings

"""MOSTRO_PIM"""
MOSTRO_PIM_TASKS = fetch_tasks(url=settings.mostro_pim.url,
                               username=settings.mostro_pim.login,
                               password=settings.mostro_pim.password,
                               params=mostro_pim_param)

MOSTRO_PIM_TASKS_NAMES = [make_task_key(id=task["task_name"]["id"],
                                        name=task["task_name"]["value"],
                                        system=SystemName.MOSTRO_PIM)
                          for task in MOSTRO_PIM_TASKS]

"""SEARCH"""
SEARCH_TASKS = fetch_tasks(url=settings.search.url,
                           username=settings.search.login,
                           password=settings.search.password,
                           params=search_param)

SEARCH_TASKS_NAMES = [make_task_key(id=task["label"]["id"],
                                    name=task["label"]["value"],
                                    system=SystemName.SEARCH,
                                    engine=settings.search.engine)
                      for task in SEARCH_TASKS]

"""MOSTRO_SEARCH_SYNC"""
MOSTRO_SEARCH_SYNC_TASKS = fetch_tasks(url=settings.mostro_search_sync.url,
                                       username=settings.mostro_search_sync.login,
                                       password=settings.mostro_search_sync.password,
                                       params=mostro_search_sync_param)

MOSTRO_SEARCH_SYNC_TASKS_NAMES = [make_task_key(id=task["id"]["id"],
                                                name=task["engine_label"]["value"],
                                                system=SystemName.MOSTRO_SEARCH_SYNC)
                                  for task in MOSTRO_SEARCH_SYNC_TASKS]

"""SYNC"""
SYNC_TASKS = fetch_tasks(url=settings.sync.url,
                         username=settings.sync.login,
                         password=settings.sync.password,
                         params=sync_param)

SYNC_TASK_NAMES = [make_task_key(id=task["id"], name=task["name"], system=SystemName.SYNC)
                   for task in SYNC_TASKS]

STATUS_UNCHANGED_SYNC_TASK_NAMES = [make_task_key(id=task["id"], name=task["name"],
                                                  system=SystemName.STATUS_UNCHANGED_SYNC)
                                    for task in SYNC_TASKS]


@pytest.mark.parametrize('task', [*MOSTRO_PIM_TASKS], ids=[*MOSTRO_PIM_TASKS_NAMES])
def test_tasks_mostro_pim(task):
    assert is_not_valid_task(task) is False


@pytest.mark.parametrize('task', [*SEARCH_TASKS], ids=[*SEARCH_TASKS_NAMES])
def test_tasks_search(task):
    assert is_not_valid_task(task) is False


@pytest.mark.parametrize('task', [*MOSTRO_SEARCH_SYNC_TASKS], ids=[*MOSTRO_SEARCH_SYNC_TASKS_NAMES])
def test_tasks_mostro_search_sync(task):
    assert is_not_valid_mostro_search_sync_task(task) is False


@pytest.mark.parametrize('task', [*SYNC_TASKS], ids=[*SYNC_TASK_NAMES])
def test_tasks_sync(task):
    assert is_not_valid_task(task) is False


@pytest.mark.parametrize('task', [*SYNC_TASKS], ids=[*STATUS_UNCHANGED_SYNC_TASK_NAMES])
def test_tasks_status_unchanged_sync(task):
    assert is_not_valid_status_change_sync_task(task) is False

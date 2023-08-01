import os
import requests

import settings
import settings.query_data
from services.allure_service import get_allure_report_data, generate_failed_task_list
from settings.query_data import SystemName
from settings.env_config import settings


def generate_message_for_telegram(dir_path):
    ENV = os.environ.get("ENV")
    sep = '\U00002063'
    allure_report = get_allure_report_data(allure_report_dir=dir_path)

    mostro_pim_task_list = generate_failed_task_list(data=allure_report, system=SystemName.MOSTRO_PIM)
    search_task_list = generate_failed_task_list(data=allure_report, system=SystemName.SEARCH)
    mostro_search_sync_task_list = generate_failed_task_list(data=allure_report, system=SystemName.MOSTRO_SEARCH_SYNC)
    sync_task_list = generate_failed_task_list(data=allure_report, system=SystemName.SYNC)
    status_unchanged_sync_list = generate_failed_task_list(data=allure_report, system=SystemName.STATUS_UNCHANGED_SYNC)

    if any([mostro_pim_task_list,
            search_task_list,
            mostro_search_sync_task_list,
            sync_task_list,
            status_unchanged_sync_list]):

        header_msg = f"{sep}          [{ENV}]----VGZ_Tasks_tests\n" \
                     f"\n" \
                     f"{sep}\U0000274C{sep} Fails:\n"

    else:
        header_msg = ""

    if mostro_pim_task_list:
        mostro_pim_msg = \
            f"\n" \
            f"{sep}   {SystemName.MOSTRO_PIM}" \
            f"\n" \
            f"{mostro_pim_task_list}\n"
    else:
        mostro_pim_msg = ""

    if search_task_list:
        search_msg = \
            f"\n" \
            f"{sep}   {SystemName.SEARCH}" \
            f"\n" \
            f"{search_task_list}\n"
    else:
        search_msg = ""

    if mostro_search_sync_task_list:
        mostro_search_sync_msg = \
            f"\n" \
            f"{sep}   {SystemName.MOSTRO_SEARCH_SYNC}" \
            f"\n" \
            f"{mostro_search_sync_task_list}\n"

    else:
        mostro_search_sync_msg = ""

    if sync_task_list:
        sync_msg = \
            f"\n" \
            f"{sep}   {SystemName.SYNC}" \
            f"\n" \
            f"{sync_task_list}\n"
    else:
        sync_msg = ""

    if status_unchanged_sync_list:
        status_sync_msg = \
            f"\n" \
            f"{sep}   {SystemName.STATUS_UNCHANGED_SYNC}" \
            f"\n" \
            f"{status_unchanged_sync_list}\n"

    else:
        status_sync_msg = ""

    return f"{header_msg}{mostro_pim_msg}{search_msg}{mostro_search_sync_msg}{sync_msg}{status_sync_msg}"


def request_in_telegram(message, token, chat_id):
    try:
        requests.post(f'{settings.telegram.bot_url}{token}/sendMessage',
                      json=dict(chat_id=chat_id, text=message, parse_mode='html'))
    except requests.exceptions.RequestException as error:
        from start_tests import LOG
        LOG.error("Request in telegram error: %s %s %s", message, token, chat_id)
        LOG.exception(error)


def send_message_to_telegram(message, argument):
    if argument == "prod":
        request_in_telegram(message=message, token=settings.telegram.token, chat_id=settings.telegram.chat_id)

    if argument == "dev":
        request_in_telegram(message=message, token=settings.telegram.token, chat_id=settings.telegram.chat_id)

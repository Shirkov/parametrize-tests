from settings.env_config import settings

mostro_pim_param = {"method": "tasks.grid",
                    "params": {
                        "page": 1,
                        "per_page": 5000,
                        "locale": "ru_RU"
                    }
                    }

search_param = {"method": "tasks.grid",
                "params": {
                    "engine": settings.search.engine,
                    "locale": "ru_RU",
                    "page": 1,
                    "per_page": 5000
                }
                }

mostro_search_sync_param = {"method": "Sync.grid",
                            "params": {
                                "page": 1,
                                "locale": "ru_RU",
                                "per_page": 10000
                            }
                            }

sync_param = {"method": "tasks.list",
              "params": {
                  "conditions": {
                      "active": True,
                      "exit_code": 1
                  },
                  "limit": 10000
              }
              }


class SystemName:
    """Важно:
            название тестовой функции должно содержать название SystemName
            Пример "test_tasks_mostro_search_sync"
            Смотри функцию "parse_task_key()"
    """
    MOSTRO_PIM = "MOSTRO_PIM"
    SEARCH = "SEARCH"
    MOSTRO_SEARCH_SYNC = "MOSTRO_SEARCH_SYNC"
    SYNC = "SYNC"
    STATUS_UNCHANGED_SYNC = "STATUS_UNCHANGED_SYNC"


# TimeZone
eu_moscow_tz = "Europe/Moscow"

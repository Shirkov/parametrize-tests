import logging
import os

DIR = os.path.dirname(__file__)

logging.basicConfig(level=logging.INFO)
LOG = logging.getLogger("log")


class MyPlugin:

    def pytest_sessionfinish(self, session, exitstatus):
        """Метод выполняется после прогона всех тестов"""
        from services.telegram_service import generate_message_for_telegram, send_message_to_telegram
        ENV = os.getenv("ENV")

        os.system("allure generate allureresult --clean")

        mark = session.config.option.markexpr
        message = generate_message_for_telegram(dir_path=DIR)

        send_message_to_telegram(message=message, argument=ENV)


if __name__ == '__main__':
    from settings.env_config import ConfigLoader, run_tests

    config_loader = ConfigLoader()
    config_loader.merge_config()

    ENV = config_loader.set_env()
    run_tests(env=ENV)

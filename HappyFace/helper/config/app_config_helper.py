import configparser

from dotenv import dotenv_values


class AppConfigHelper:
    APP_CONFIG_FILE_PATH = "config/app_config.ini"
    DB_CONFIG_FILE_PATH = "config/db_config.ini"
    LOG_CONFIG_FILE_PATH = "config/log/default.env"
    ORG_CONFIG_FILE_PATH = "config/org.ini"

    @staticmethod
    def set_basic_app_config(basic_config: dict[str, str]) -> None:
        parser = configparser.ConfigParser()
        parser["basic"] = basic_config
        with open(AppConfigHelper.APP_CONFIG_FILE_PATH, 'w') as config_file:
            parser.write(config_file)

    @staticmethod
    def get_basic_app_config() -> dict[str, str]:
        parser = configparser.ConfigParser()
        parser.read(AppConfigHelper.APP_CONFIG_FILE_PATH)
        return dict(parser["basic"])

    @staticmethod
    def get_database_config() -> dict[str, str]:
        parser = configparser.ConfigParser()
        parser.read(AppConfigHelper.DB_CONFIG_FILE_PATH)
        return dict(parser["database"])

    @staticmethod
    def get_log_config() -> dict[str, str]:
        return dotenv_values(AppConfigHelper.LOG_CONFIG_FILE_PATH)

    @staticmethod
    def get_org_config() -> dict[str, str]:
        return dotenv_values(AppConfigHelper.ORG_CONFIG_FILE_PATH)

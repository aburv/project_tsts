"""
Methods returning system config
"""
import os


class Config:
    """
    Config class to set all envs
    """

    @staticmethod
    def get_db_parameters() -> dict:
        """
        :return:
        :rtype:
        """
        return {
            "db": os.environ.get("POSTGRES_DB"),
            "user": os.environ.get("POSTGRES_USER"),
            "pass": os.environ.get("POSTGRES_PASSWORD"),
            "host": os.environ.get("POSTGRES_HOST"),
            "port": os.environ.get("POSTGRES_PORT"),
            "meta_schema": os.environ.get("POSTGRES_SCHEMA_META"),
            "schema": os.environ.get("POSTGRES_SCHEMA")
        }

    @staticmethod
    def get_api_keys() -> list:
        """
        :return:
        :rtype:
        """
        return [
            os.environ.get("WEB_CLIENT_KEY"),
            os.environ.get("ANDROID_CLIENT_KEY"),
            os.environ.get("IOS_CLIENT_KEY"),
            os.environ.get("DEV_KEY")
        ]

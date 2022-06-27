from configparser import ConfigParser


class Config:

    def __init__(self):
        config_parser = ConfigParser()
        config_parser.read("../config.ini")

        self.__configs = {"bot_name": config_parser.get("names", "bot_name"),
                          "target_path": config_parser.get("paths", "target_path"),
                          "types_to_index": config_parser.get("types", "types_to_index").split(","),
                          "folders_to_ignore": config_parser.get("types", "folders_to_ignore").split(",")}

    def get_bot_name(self):
        return self.__configs["bot_name"]

    def get_target_path(self):
        return self.__configs["target_path"]

    def get_types_to_index(self):
        return self.__configs["types_to_index"]

    def get_folders_to_ignore(self):
        return self.__configs["folders_to_ignore"]

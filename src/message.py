import PTN

from dir_scan import Directory
from src.config import Config


class Message:

    def __init__(self):
        self.__config = Config()

        self.__directory = Directory()
        if len(self.__directory.get_new_files_list()) > 0:
            print(self.return_message_text())

    def return_message_text(self):
        header_text = self.__set_header_text()
        new_file_list_string = ""
        for name in self.__directory.get_new_files_list():
            info = self.__parse_file_name(name)
            has_subtitles = self.__directory.check_for_subtitles(name)
            if has_subtitles:
                subs = "[S]"
            else:
                subs = ''

            title = info['title'].title()
            try:
                season = info['season']
                episode = info['episode']
                new_file_list_string = new_file_list_string + f" - {title}, S{season}E{episode} {subs}\n"
            except KeyError:
                new_file_list_string = new_file_list_string + f" - {title} {subs}\n"

        return f"{header_text}{new_file_list_string}"

    def __set_header_text(self):
        bot_name = self.__config.get_bot_name()

        if len(self.__directory.get_new_files_list()) == 1:
            header_text = f"1 file added to {bot_name}:\n\n"
        else:
            header_text = f"{len(self.__directory.get_new_files_list())} files have been added to {bot_name}:\n\n"
        return header_text

    @staticmethod
    def __parse_file_name(file_name):
        info = PTN.parse(file_name)

        return info


Message()

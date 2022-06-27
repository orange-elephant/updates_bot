from os import listdir, path

from src.config import Config


class Directory:
    state_file = "../state/recent_state.txt"

    def __init__(self):
        self.__config = Config()
        self.__path = self.__config.get_target_path()
        self.__video_file_extensions = self.__config.get_types_to_index()

        self.__all_files = self.__retrieve_file_list()
        self.__current_file_list = self.__filter_file_list(self.__all_files)
        self.__previous_file_list_state = self.__load_current_file_list_state()
        self.__new_files = self.__return_new_items(self.__previous_file_list_state, self.__current_file_list)
        if len(self.__current_file_list) > 0:
            self.__save_current_file_list_state()

    def get_new_files_list(self):
        return self.__new_files

    def check_for_subtitles(self, file_name):
        # split at '.' once starting from the right to remove the current file extension
        file_name_without_extension = file_name.rsplit('.', 1)[0]
        if f"{file_name_without_extension}.srt" in self.__all_files:
            return True
        return False

    def __retrieve_file_list(self):
        files_list, dir_list = self.__read_directory(self.__path, [], [])

        return files_list

    def __read_directory(self, current_path, files_list, dir_list):
        directory = listdir(current_path)

        for file in directory:
            try:
                new_path = current_path + "/" + file
                if file not in self.__config.get_folders_to_ignore() and path.isdir(new_path):
                    dir_list.append(file)
                    self.__read_directory(new_path, files_list, dir_list)
                elif not path.isdir(new_path):
                    files_list.append(file)
            except PermissionError:
                pass
        return files_list, dir_list

    def __filter_file_list(self, file_list):
        filtered_list = []

        for file in file_list:
            for video_extension in self.__video_file_extensions:
                if video_extension in file:
                    filtered_list.append(file)
                    break

        return filtered_list

    def __save_current_file_list_state(self):
        state_file = open(self.state_file, "w")
        for file_name in self.__current_file_list:
            state_file.write(f"{file_name}\n")
        state_file.close()

    def __load_current_file_list_state(self):
        current_file_list = []
        state_file = open(self.state_file, "r")
        for line in state_file:
            current_file_list.append(line.strip("\n"))
        state_file.close()

        return current_file_list

    @staticmethod
    def __return_new_items(previous, current):
        new_items = []
        for item in current:
            if item not in previous:
                new_items.append(item)

        return new_items

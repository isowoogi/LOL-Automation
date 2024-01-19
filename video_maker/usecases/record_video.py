import os
from time import sleep
import subprocess
import pyautogui
import pydirectinput
from entities.match_data import MatchData
from entities.progress import print_progress


class RecordVideo:
    def __init__(self, match_data: MatchData) -> None:
        self.__video_file_dir = os.path.abspath(r'.\media\Videos')
        self.__replay_file_dir = os.path.abspath(r'.\media\replays')
        self.__match_data = match_data
        self.total=self.__duration_in_seconds()+76

    def record(self):
        # self.__show_mouse_position()
        # print('Starting recording of the match...')
        self.remove_video_file()
        self.__run_obs()
        sleep(5)
        self.__run_game()
        
        for i in range(45):
            sleep(1)
            print_progress(i, self.total, prefix='Gameplay recording:')

        # Get the size of the screen
        screen_width, screen_height = pydirectinput.size()

        # Calculate the center of the screen
        center_x = int(screen_width / 2)
        center_y = int(screen_height / 2)

        # Click on the center of the screen
        pydirectinput.click(center_x, center_y)
        pydirectinput.keyDown('n')
        pydirectinput.keyUp('n')
        sleep(1)
        print_progress(50, self.total, prefix='Gameplay recording:')
        pydirectinput.keyDown('o')
        pydirectinput.keyUp('o')
        sleep(1)
        print_progress(51, self.total, prefix='Gameplay recording:')
        pydirectinput.keyDown('u')
        pydirectinput.keyUp('u')
        sleep(5)
        print_progress(56, self.total, prefix='Gameplay recording:')
        # select champion
        self.__select_player()
        
        sleep(2)
        print_progress(58, self.total, prefix='Gameplay recording:')
        pydirectinput.keyDown('c')
        pydirectinput.keyUp('c')
        sleep(1)
        print_progress(59, self.total, prefix='Gameplay recording:')
        # zoom out

        # Click on the center of the screen
        pydirectinput.click(center_x, center_y)
        # Press and hold Ctrl+Shift+Z
        pydirectinput.keyDown('ctrl')
        pydirectinput.keyDown('shift')
        pydirectinput.keyDown('z')
        pydirectinput.keyUp('ctrl')
        pydirectinput.keyUp('shift')
        pydirectinput.keyUp('z')
        # Move mouse pointer down 5 times
        pyautogui.scroll(-700)

        # Release all keys

        # zoom out end
        
        
        self.__start_stop_recording()
        for i in range(self.__duration_in_seconds()):
            print_progress(60+i, self.total, prefix='Gameplay recording:')
            sleep(1)
        self.__start_stop_recording()
        sleep(10)
        print_progress(60+self.__duration_in_seconds()+10, self.total, prefix='Gameplay recording:')
        # pydirectinput.click(962, 641)
        # pyautogui.click(962, 641)
        pyautogui.hotkey('alt', 'f4')
        sleep(1)
        print_progress(60+self.__duration_in_seconds()+11, self.total, prefix='Gameplay recording:')
        
        # pydirectinput.leftClick(962, 641)
        # pyautogui.click(962, 641)
        pyautogui.hotkey('alt', 'f4')
        sleep(5)
        print_progress(60+self.__duration_in_seconds()+16, self.total, prefix='Gameplay recording:')
    
        # print('Recorded match')
        return self.select_video_file()

    def __run_game(self):
        file = os.listdir(self.__replay_file_dir)[0]
        subprocess.run(["start", "cmd", "/c", f"{self.__replay_file_dir}\{file}"], shell=True)

    def __run_obs(self):
        pyautogui.hotkey('super', '1')

    def __select_player(self):
        if self.__match_data['team1']['result'] == 'Victory':
            pydirectinput.keyDown('f1')
            pydirectinput.keyUp('f1')
            pydirectinput.keyDown(self.__match_data['player_index'])
            pydirectinput.keyUp(self.__match_data['player_index'])
            pydirectinput.keyDown(self.__match_data['player_index'])
            pydirectinput.keyUp(self.__match_data['player_index'])
        else:
            keys = ['q', 'w', 'e', 'r', 't']
            pydirectinput.keyDown('f2')
            pydirectinput.keyUp('f2')
            pydirectinput.keyDown(
                keys[int(self.__match_data['player_index']) - 1])
            pydirectinput.keyUp(
                keys[int(self.__match_data['player_index']) - 1])
            pydirectinput.keyDown(
                keys[int(self.__match_data['player_index']) - 1])
            pydirectinput.keyUp(
                keys[int(self.__match_data['player_index']) - 1])

    def __start_stop_recording(self):
        pyautogui.keyDown('shiftleft')
        pyautogui.keyDown('x')
        pyautogui.keyUp('shiftleft')
        pyautogui.keyUp('x')

    def __duration_in_seconds(self) -> int:
        array = self.__match_data['duration'].split(':')
        return (int(array[0]) * 60) + int(array[1]) - 15

    def __show_mouse_position(self):
        while True:
            print(pyautogui.position())
            sleep(1)

    def select_video_file(self):
        files = os.listdir(self.__video_file_dir)
        # print(files)
        
        file_path = os.path.abspath(os.path.join(self.__video_file_dir, files[0]))
        return file_path

    def remove_video_file(self):
        file = os.listdir(self.__video_file_dir)
        for i in range(len(file)):
            os.rename(os.path.join(self.__video_file_dir, file[i]), os.path.join(
                os.path.dirname(self.__video_file_dir), 'uploaded', file[i]))

import os
import random
import time
import cv2
import PySimpleGUI as sg
import sounddevice as sd 
import numpy as np
from scipy.io.wavfile import write
from openpyxl import Workbook

class Parameters:
    def __init__(self, participant_id="", fixation_duration=1000, white_duration=1000,
                 audio_duration=6, video_dir="VIDEO_FILES", audio_dir="AUDIO_RECORDINGS",
                 data_dir="DATA_FOLDER", sample_rate=44100):
        self.participant_id = participant_id
        self.fixation_duration = fixation_duration
        self.white_duration = white_duration
        self.audio_duration = audio_duration
        self.video_dir = video_dir
        self.audio_dir = audio_dir
        self.data_dir = data_dir
        self.sample_rate = sample_rate
        self.unique_key = str(time.time())      

    def gui_layout(self):
        layout = [

            [
            sg.Column([
                [sg.Text("Participant ID:")],
                [sg.Text("Fixation Duration (ms):")],
                [sg.Text("White Duration (ms):")],
                [sg.Text("Audio Duration (s):")],
                ], element_justification="left", pad=(0, 5)),

            sg.Column([
                [sg.InputText(size = (35, 1), key = "-PARTICIPANT_ID-")],
                [sg.InputText(default_text="1000", key="-FIX-DURATION-", size=(10, 1))],
                [sg.InputText(default_text="1000", key="-WHITE-DURATION-", size=(10, 1))],
                [sg.InputText(default_text="6", key="-AUDIO-DURATION-", size=(10, 1))],
                ], element_justification="left", pad=(0, 5))
            ],

            [
            sg.Column([
                [sg.Text("Video Directory:")],
                [sg.Text("Audio Directory:")],
                [sg.Text("Data Directory:")],
                ], element_justification="left", pad=(0, 5)),

            sg.Column([
                [sg.InputText(default_text="VIDEO_FILES", key="-VIDEO-DIR-", size=(40, 1)), sg.FolderBrowse()],
                [sg.InputText(default_text="AUDIO_RECORDINGS", key="-AUDIO-DIR-", size=(40, 1)), sg.FolderBrowse()],
                [sg.InputText(default_text="DATA_FOLDER", key="-DATA-DIR-", size=(40, 1)), sg.FolderBrowse()],
                ], element_justification="left", pad=(0, 5))
            ],
            
            [
            sg.Column([ 
                [sg.Button("Start Experiment", size=(20,1))]
                ], expand_x=True, element_justification="left", pad=(0, 5)),
            
            sg.Column([ 
                [sg.Button("Reset", size=(10,1)), sg.Button("Cancel", size=(10,1))] 
                ], expand_x=True, element_justification="right", pad=(0, 5))
            ],
        ]
        return layout
    
    def validate_directory(self, dir_path):
        if not os.path.isdir(dir_path):
            raise ValueError(f"{dir_path} is not a valid directory path")
        return dir_path

    def validate_positive_int(self, value):
        if not isinstance(value, int):
            raise ValueError(f"{value} is not a valid integer")
        if value <= 0:
            raise ValueError(f"{value} is not a valid positive integer")
        return value

    def set_attributes_values(self, values):
        self.participant_id = str(values["-PARTICIPANT_ID-"])
        self.fixation_duration = self.validate_positive_int(int(values["-FIX-DURATION-"]))
        self.white_duration    = self.validate_positive_int(int(values["-WHITE-DURATION-"]))
        self.audio_duration    = self.validate_positive_int(int(values["-AUDIO-DURATION-"]))
        self.video_dir = self.validate_directory(values["-VIDEO-DIR-"])
        self.audio_dir = self.validate_directory(values["-AUDIO-DIR-"])
        self.data_dir  = self.validate_directory(values["-DATA-DIR-"])

    def reset_attributes_values(self, window):
        window["-PARTICIPANT_ID-"].update(str(self.participant_id))
        window["-FIX-DURATION-"].update(str(self.fixation_duration))
        window["-WHITE-DURATION-"].update(str(self.fixation_duration))
        window["-AUDIO-DURATION-"].update(str(self.audio_duration))
        window["-VIDEO-DIR-"].update(str(self.video_dir))
        window["-AUDIO-DIR-"].update(str(self.audio_dir))
        window["-DATA-DIR-"].update(str(self.data_dir))
    
    def get_from_gui(self):
        layout = self.gui_layout()
        window = sg.Window("Experiment Setup", layout)
        
        while True:
            event, values = window.read()
            if event == "Cancel" or event == sg.WIN_CLOSED:
                window.close()
                exit()

            elif event == "Start Experiment":
                try:
                    self.set_attributes_values(values)
                    window.close()
                    break
                except Exception as e:
                    sg.popup(f"Error: {e}")
                    continue
            
            if event == "Reset":
                self.reset_attributes_values(window)

        window.close()

def get_parameters_from_user():
    parameters = Parameters()
    parameters.get_from_gui()
    return parameters

def create_white_screen():
    return np.ones((480, 640, 3), dtype=np.uint8) * 255

def create_fixation_screen():
    fixation = create_white_screen()
    cv2.line(fixation, (320, 240-20), (320, 240+20), (0, 0, 0), thickness=3)
    cv2.line(fixation, (320-20, 240), (320+20, 240), (0, 0, 0), thickness=3)
    return fixation

def run():
    # Create the GUI to enter experiment parameters, returns a parameters object
    parameters = get_parameters_from_user()
    video_files = [f for f in os.listdir(parameters.video_dir) if f.endswith('.avi')]
    random.shuffle(video_files)

    # Set up excel file
    wb = Workbook()
    ws = wb.active
    ws.append(['ID', 'Order', 'Video', 'Audio_path'])

    # Set up full screen display
    cv2.namedWindow('main_window', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('main_window', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Display blank screen and wait for key press
    blank = create_white_screen()
    fixation = create_fixation_screen()

    cv2.imshow('main_window', blank)
    cv2.waitKey(0)

    for i, video_file in enumerate(video_files):
        video = cv2.VideoCapture(os.path.join(parameters.video_dir, video_file))
        mspf = int(1000/video.get(cv2.CAP_PROP_FPS))  # ms per frame

        # Fixation screen display
        cv2.imshow('main_window', fixation)
        cv2.waitKey(parameters.fixation_duration)

        num_samples = int(parameters.audio_duration*parameters.sample_rate)
        recording = sd.rec(num_samples, samplerate=parameters.sample_rate, channels=1)
        
        while True: # Video playing loop
            ret, frame = video.read()
            if not ret:
                break
            cv2.imshow('main_window', frame)
            cv2.waitKey(mspf)
            
        # white screen display
        cv2.imshow('main_window', blank)
        cv2.waitKey(parameters.white_duration)

        sd.wait() # wait for recording to finish
        audio_file = f"{video_file[:-4]}_{parameters.participant_id}_{parameters.unique_key}.wav"
        audio_path = os.path.join(parameters.audio_dir, audio_file)
        write(audio_path, parameters.sample_rate, recording)

        ws.append([parameters.participant_id, i+1, video_file, audio_path])

        video.release()

    cv2.destroyAllWindows()

    data_file = f"{parameters.participant_id}_{parameters.unique_key}.xlsx"
    wb.save(os.path.join(parameters.data_dir, data_file))

if __name__ == "__main__":
    run()
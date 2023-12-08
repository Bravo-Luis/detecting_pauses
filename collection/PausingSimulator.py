import time
import json
import subprocess
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import ActionChains

from netunicorn.base import Task, Success, Failure

class PausingSimulator(Task):
    def __init__(self, video_url=None, duration=None, filepath=None, chrome_location=None, webdriver_arguments=None) -> None:
        super().__init__()
        self.video_url = video_url
        self.duration = duration
        self.filepath = filepath
        self.chrome_location = chrome_location or '/usr/bin/chromium'
        self.webdriver_arguments = webdriver_arguments or []
        self.drive = None
        self.log = []
        self.sfn_open = False
    
    def run(self):
        try:
            self.init_webdriver()
            self.driver.get(self.url)
            start_time = self.wait_until_start()
            
            while time.time() - start_time < self.duration:
                delay = random.randint(5, 10)
                
                for _ in range(delay):
                    self.log_data()
                    time.sleep(1)
                self.toggle_video_state()
                pass
            
            self.save_file()
            self.driver.quit()

        except Exception as e:
            print(f"An error occurred: {e}")
            return Failure(str(e))
    
    def get_network_metrics(self):
        try:
            response = subprocess.run(["ping", "-c", "1", 'www.youtube.com'], capture_output=True)
            output = response.stdout.decode()
            latency = output.split("time=")[-1].split(" ms")[0]

            return latency
        except Exception as e:
            return f"Error measuring latency: {e}"

    
    def get_youtube_metrics(self):
        """Fetches metrics from 'Stats for nerds'."""
        
        DIVS = [1, 2, 3, 4, 5, 7, 9, 10, 11]

        DIV_TO_KEY = {
            1: 'Video ID',
            2: 'Viewport / Frame Size',
            3: 'Current Res / Optimal Res',
            4: 'Volume / Normalized',
            5: 'Codecs',
            7: 'Color',  
            9: 'Connection Speed',  
            10: 'Network Activity',  
            11: 'Buffer Health',  
        }

        try:
            if not self.enable_stats_for_nerds():
                return "Unable to open Stats for nerds"

            stat_dict = {}
            for div_id in DIVS:
                try:
                    elem = self.driver.find_element(By.CSS_SELECTOR, f".html5-video-info-panel-content > div:nth-child({div_id}) > span:nth-child(2)")
                    stat_dict[DIV_TO_KEY[div_id]] = elem.text
                except Exception as e:
                    print(f"An error occurred in get_stats for DIV {div_id}: {e}")
                    stat_dict[DIV_TO_KEY.get(div_id, f"Unknown_DIV_{div_id}")] = 'Error'
            return stat_dict
        except Exception as e:
            print(f"An error occurred in get_youtube_metrics: {e}")
            return Failure(str(e))
    
    def get_video_state(self):
        try:
            player_status = self.driver.execute_script("return document.getElementById('movie_player').getPlayerState()")
            return player_status
            pass
        except Exception as e:
            print(f"An error occurred: {e}")
            return Failure(str(e))
    
    def toggle_video_state(self):
        try:
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "ytp-play-button")))

            play_button = self.driver.find_element(By.CLASS_NAME, "ytp-play-button")

            self.driver.execute_script("arguments[0].click();", play_button)
        except Exception as e:
            print(f"An error occurred: {e}")
            return Failure(str(e))

    def init_webdriver(self):
        try:
            options = Options()
            for argument in self.webdriver_arguments:
                options.add_argument(argument)
            self.driver = webdriver.Chrome(options=options)
        except Exception as e:
            print(f"An error occurred: {e}")
            return Failure(str(e))
    
    def save_file(self):
        try:
            with open(self.filepath, "w") as json_file:
                json.dump(self.log, json_file)
        except Exception as e:
            print(f"An error occurred: {e}")
            return Failure(str(e))

        
    def wait_until_start(self):
        try:
            video_is_playing = False
            curr_time = self.find_element(By.CLASS_NAME, "ytp-time-current")
            while not video_is_playing:
                time.sleep(1)
                try:
                    curr_time = self.find_element(By.CLASS_NAME, "ytp-time-current")
                    video_is_playing = curr_time.text[:4] == curr_time.text[-4:]
                except StaleElementReferenceException:
                    pass
            return time.time()
        except Exception as e:
            print(f"An error occurred: {e}")
            return Failure(str(e))

    def find_element(self, by, value):
        try:
            return WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((by, value)))
        except Exception as e:
            print(f"An error occurred: {e}")
            return Failure(str(e))
    
    def enable_stats_for_nerds(self):
        """Enables the 'Stats for nerds' feature on the YouTube player."""
        try:
            
            if self.sfn_open:
                return True
            
            movie_player = self.driver.find_element(By.ID, 'movie_player')
            ActionChains(self.driver).move_to_element(movie_player).context_click().perform()
            options = self.driver.find_elements(By.CLASS_NAME, 'ytp-menuitem')
            for option in options:
                option_child = option.find_element(By.CLASS_NAME, 'ytp-menuitem-label')
                if option_child.text == 'Stats for nerds':
                    option_child.click()
                    self.sfn_open = True
                    return True
            return False
        except Exception as e:
            print(f"Error enabling 'Stats for nerds': {e}")
            return False
    
    def log_data(self):
        curr_state = self.get_video_state()
        yt_metrics = self.get_youtube_metrics()
        latency = self.get_network_metrics()

        self.log.append({
                    "time": time.time(),
                    "curr_state": curr_state,
                    "yt_metrics": yt_metrics,
                    "latency": latency
                })
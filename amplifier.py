
"""amplifier.py. Plugin for HifiBerryOs to control an external amplifier
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from typing import Dict
import time
import logging
import RPi.GPIO as GPIO
from ac2.plugins.control.controller import Controller
from ac2.constants import STATE_PLAYING
from threading import Event


class Amplifier(Controller):
    def __init__(self, params: Dict[str, str] = None):
        super().__init__()
        logging.info("initializing amplifier controller")
        self.paused = Event()
        self.played = Event()
        self.out = 16
        self.timeout = 60
        if "out" in params:
            try:
                self.out = int(params["out"])
            except:
                logging.info("can't parse %s use GPIO 16 instead", params["out"])
        if "t" in params:
            try:
                self.timeout = int(params["t"])
            except:
                logging.info("can't parse %s use 60 seconds instead", params["t"])

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.out, GPIO.OUT)

    def update_playback_state(self, state):
        if self.playerstate != state:
            self.playerstate = state
            logging.info("state: %s", state)
            if state == STATE_PLAYING:
                if GPIO.input(self.out) == GPIO.LOW:
                    GPIO.output(self.out, GPIO.HIGH)
                    logging.info("Set GPIO.HIGH")
                self.played.set()
            else:
                self.played.clear()
                self.paused.set()


    def run(self) -> None:
        while True:
            # wait untill Event self.paused is set
            self.paused.wait()
            # if Event self.played is set before the Timeout Time, the GPIO stays high. If not it is set to Low.
            playing_resumed = self.played.wait(self.timeout)
            if playing_resumed == False and GPIO.input(self.out) == GPIO.HIGH:
                GPIO.output(self.out, GPIO.LOW)
                logging.info("Set GPIO.LOW")
            
            self.paused.clear()

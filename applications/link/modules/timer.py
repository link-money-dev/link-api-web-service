import time

class Timer():
    def __init__(self, interval,func):
        self.interval=interval
        self.func=func

    def run(self):
        t = int(time.time())
        self.func()
        while True:
            if int(time.time())<t+self.interval:
                time.sleep(0.5)
                # pass
            else:
                t=int(time.time())
                self.func()
import time as t

class Timer:
    def __init__(self, seconds):
        self.sec = seconds
        self.start_time = None
        self.run_timer = True
        self.timer = 0
        self.start_timer = True
    def start(self):
        if self.start_timer:
            self.start_time = t.time()
            self.start_timer = False
        self.current_time = t.time()
        if self.run_timer:
            if self.start_time != None:
                self.timer = self.current_time - self.start_time
        if self.timer >= self.sec:
            self.run_timer = False
            self.timer = self.sec
    def stop(self):
        self.run_timer = False
        pass
    def restart(self,new_time='default'):
        self.start_time = None
        self.run_timer = True
        if new_time == 'default':
            self.sec = new_time
        else:
            self.sec = new_time
        self.start_timer = True
        pass
    def time(self):
        return self.timer
        pass
    def __bool__(self):
        if self.timer != self.sec:
            return False
        else:
            return True
    pass
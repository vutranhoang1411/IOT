class Lock:
    def __init__(self):
        self.Locked=False
    def Unlock(self):
        self.Locked=False
    def Lock(self):
        self.Locked=True
# --- Server State Class ---
class ServerController:
    def __init__(self):
        self.running = False

    def toggle(self):
        self.running = not self.running
        # Insert actual server start/stop logic here

    def status(self):
        return self.running

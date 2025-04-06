import digitalocean
import time
from typing import Callable, Optional

class DropletManager:
    def __init__(self, token: str, droplet_name: str):
        self.token = token
        self.droplet_name = droplet_name
        self.manager = digitalocean.Manager(token=self.token)
        self.droplet = self._get_droplet()

    def _get_droplet(self):
        droplets = self.manager.get_all_droplets()
        for droplet in droplets:
            if droplet.name == self.droplet_name:
                return droplet
        raise ValueError(f"Droplet named '{self.droplet_name}' not found")

    def power_on(self, on_complete: Optional[Callable] = None):
        if self.droplet.status != 'active':
            self.droplet.power_on()
            if on_complete:
                self._wait_for_state('active')
                on_complete(self.droplet)

    def power_off(self, on_complete: Optional[Callable] = None):
        if self.droplet.status == 'active':
            self.droplet.shutdown()
            if on_complete:
                self._wait_for_state('off')
                on_complete(self.droplet)

    def toggle_power(self, on_complete: Optional[Callable] = None):
        if self.droplet.status == 'active':
            self.droplet.shutdown()
            if on_complete:
                self._wait_for_state('off')
                on_complete(self.droplet)
        else:
            self.droplet.power_on()
            if on_complete:
                self._wait_for_state('active')
                on_complete(self.droplet)

    def get_status(self):
        self.droplet.load()
        return self.droplet.status

    def _wait_for_state(self, desired_state, timeout=300, poll_interval=5):
        start_time = time.time()
        while time.time() - start_time < timeout:
            self.droplet.load()
            if self.droplet.status == desired_state:
                return
            time.sleep(poll_interval)
        raise TimeoutError(f"Droplet did not reach state '{desired_state}' within {timeout} seconds.")

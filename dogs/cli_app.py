import cutie
from dogs.dogs import DOGS

class CLIApp:
    def __init__(self):
        self.dogs = DOGS()

    def run(self):
        while True:
            print("\nAvailable Droplets:")
            droplets = self.dogs.list_droplets()
            if not droplets:
                print("No droplets configured.")
                return

            for i, name in enumerate(droplets):
                dm = self.dogs.get_droplet_manager(name)
                print(f"[{i+1}] {name} - Status: {dm.get_status()}")

            options = droplets + ["Exit"]
            idx = cutie.select(options)

            if idx == len(droplets):
                print("Goodbye.")
                break

            self.manage_droplet(droplets[idx])

    def manage_droplet(self, name):
        dm = self.dogs.get_droplet_manager(name)

        while True:
            print(f"\nManage: {name} (Status: {dm.get_status()})")
            choice = cutie.select(["Toggle Power", "Power On", "Power Off", "Check Status", "Back"])

            if choice == 0:
                self._confirm_and_act(dm.toggle_power, "Toggled")
            elif choice == 1:
                self._confirm_and_act(dm.power_on, "Powered on")
            elif choice == 2:
                self._confirm_and_act(dm.power_off, "Powered off")
            elif choice == 3:
                print(f"Status: {dm.get_status()}")
            elif choice == 4:
                break

    def _confirm_and_act(self, action, done_message):
        wait = cutie.prompt_yes_or_no("Wait for completion?")
        if wait:
            action(on_complete=lambda d: print(f"{done_message}."))
        else:
            action()


if __name__ == "__main__":
    CLIApp().run()

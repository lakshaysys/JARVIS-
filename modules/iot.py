import os
import platform

class IOTControl:
    def __init__(self):
        self.os_type = platform.system()

    def shutdown_system(self):
        """Allows J.A.V.E.I.R.S. to turn off the computer."""
        if self.os_type == "Windows":
            os.system("shutdown /s /t 1")
        else:
            os.system("sudo shutdown now")

    def open_application(self, app_name):
        """Example: 'Jarvis, open Chrome'"""
        # This is a simple version; advanced version uses subprocess
        os.system(f"start {app_name}")
        return f"Opening {app_name} now, Master Lakshay."
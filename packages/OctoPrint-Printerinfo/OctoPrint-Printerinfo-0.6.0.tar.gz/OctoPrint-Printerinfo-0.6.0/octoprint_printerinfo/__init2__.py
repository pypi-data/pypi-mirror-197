#imports 
import logging
import requests
import octoprint.plugin
from octoprint.events import Events
from octoprint.printer.profile import PrinterProfileManager

# define the main plugin class
class PrinterinfoPlugin(octoprint.plugin.EventHandlerPlugin):
    def __init__(self):
        # initialize the plugin logger
        self._logger = logging.getLogger(__name__)
        # initialize the printer profile manager
        self._profile_manager = PrinterProfileManager()

    # define the on_event function to handle OctoPrint events
    def on_event(self, event, payload):
        if event == Events.CONNECTED:
            # handle the printer connected event
            self._handle_printer_connected(payload)
        elif event == Events.PRINT_STARTED:
            # handle the print started event
            self._handle_print_started(payload)

    def _handle_printer_connected(self, payload):
        # retrieve the printer profile for the connected printer
        profile = self._profile_manager.get(payload.get("profile", {}).get("id"))
        if profile:
            # send the printer name to the external API endpoint
            printer_name = profile.get("name")
            self._send_printer_name(printer_name)

    def _handle_print_started(self, payload):
        # retrieve the current print job data
        job_data = self._printer.get_current_job()
        if job_data:
            # send the print job data to the external API endpoint
            self._send_print_job_data(job_data)

    def _send_printer_name(self, printer_name):
        # send the printer name to the external API endpoint
        url = "https://middleman.gavinhailey.dev/api/v1/printers"
        data = {"printer": {"name": printer_name}}
        response = requests.post(url, json=data)
        if response.status_code != 200:
            self._logger.warn("Failed to send printer name to external API")

    def _send_print_job_data(self, job_data):
        # send the print job data to the external API endpoint
        url = "https://middleman.gavinhailey.dev/api/v1/jobs"
        data = {"job": job_data}
        response = requests.post(url, json=data)
        if response.status_code != 200:
            self._logger.warn("Failed to send print job data to external API")

__plugin_name__ = "Printerinfo Plugin"
__plugin_pythoncompat__ = ">=3,<4" 

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = PrinterinfoPlugin()
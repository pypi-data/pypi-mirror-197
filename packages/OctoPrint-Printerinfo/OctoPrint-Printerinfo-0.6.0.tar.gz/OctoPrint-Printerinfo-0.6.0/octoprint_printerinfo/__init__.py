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
            self._logger.info(printer_name)
            self._send_printer_name(printer_name)

    def _handle_print_started(self, payload):
        # retrieve the current print job data
        job_data = self._printer.get_current_job()
        if job_data:
            # send the print job data to the external API endpoint
            self._logger.info(job_data)
            self._send_print_job_data(job_data)

    def _send_printer_name(self, printer_name):
        # send the printer name to the external API endpoint
        url = "https://middleman.gavinhailey.dev/api/v1/printers"
        data = {"printer": {"name": printer_name}}
        response = requests.post(url, json=data)
        self._logger.info(data)
        #self._logger.warn(response.status_code)
        if response.status_code != 200:
            self._logger.warn("Failed to send printer name to external API")

    def _send_print_job_data(self, job_data):
        # send the print job data to the external API endpoint
        url = "https://middleman.gavinhailey.dev/api/v1/jobs"
        data = {"job": job_data}
        response = requests.post(url, json=data)
        self._logger.info(data)
        #self._logger.warn(response.status_code)
        if response.status_code != 200:
            self._logger.warn("Failed to send print job data to external API")

__plugin_name__ = "Printerinfo Plugin"
__plugin_pythoncompat__ = ">=3,<4" 

def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = PrinterinfoPlugin()

#import octoprint.plugin
#from octoprint.server import admin_permission
#from octoprint.events import Events
#import requests 
#class PrinterinfoPlugin(
#    octoprint.plugin.StartupPlugin,
#    octoprint.plugin.BlueprintPlugin,
#    octoprint.plugin.EventHandlerPlugin
#)#
#    
#        
#    def on_event(self, event, payload):
#        url_job = 'https://middleman.gavinhailey.dev/api/v1/jobs'
#        #set up for loop to go through printers 
#        self._logger.info(event)
#        if event == Events.PRINT_STARTED:
#            self._logger.info("New print job started!")
#            job_id = payload.get("name")
#            if job_id is not None:
#                job_data = self._printer.get_current_job()
#                #job_data = self._printer.get_job_data(job_id)
#                if job_data is not None:
#                    myObj = {
#                        "job": job_data
#                    }
#                    self._logger.info("Job data: %s", job_data)
#                    j = requests.post(url_job, json = myObj)
#                    print(j)
#                else:
#                   self._logger.warning("Failed to get job data for job id: %s", job_id)
#        
#        elif event == Events.CONNECTED:
#            url_printer = 'https://middleman.gavinhailey.dev/api/v1/printers'
#            profile = payload.get("")
#            self._logger.info("Printer profile name: {}".format(profile["name"]))
#            myObj = {
#                "printer":{
#                "name" : profile["name"]
#                }
#            }
#            print(myObj)
#            p = requests.post(url_printer, json =  myObj)
#            print(p)
#        
#  # class JobInfoPlugin(octoprint.plugin.EventHandlerPlugin):
#  #     
#  #     def on_event(self, event, payload):
#  #         if event == Events.PRINT_JOB_ADDED:
#  #             self._logger.info("New print job added!")
#  #             job_id = payload.get("job", {}).get("id")
#  #             if job_id is not None:
#  #                 job_data = self._printer.get_job_data(job_id)
#  #                 if job_data is not None:
#  #                     self._logger.info("Job data: %s", job_data)
#  #                     # Update your job object here
#  #                 else:
#  #                     self._logger.warning("Failed to get job data for job id: %s", job_id)
#  #    #
#    # Define your plugin's asset files to automatically include in the
#    # core UI here.
#    
#    def get_assets(self):
#        return {
#            #"js": ["js/printerinfo.js"],
#            #"css": ["css/printerinfo.css"],
#            #"less": ["less/printerinfo.less"]
#        #
#    # Define the API endpoint for getting the printer profile information
#    @octoprint.plugin.BlueprintPlugin.route("/api/printer/profile", methods=["GET"])
#    #@octoprint.plugin.BlueprintPlugin.requires_access(admin_permission)
#    @octoprint.plugin.BlueprintPlugin.route("/api/job", methods=["GET"])
#    #@octoprint.plugin.BlueprintPlugin.requires_access(status_permission)
#    
#    def get_printer_profile(self):
#        profile = self._printer_profile_manager.get_default()
#        #profile = octoprint.printer.profiles()
#        return profil#
#__plugin_name__ = "Printerinfo Plugin"
#__plugin_pythoncompat__ = ">=3,<4"#
#def __plugin_load__():
#    global __plugin_implementation__
#    __plugin_implementation__ = PrinterinfoPlugin(#
#    global __plugin_hooks__
#    __plugin_hooks__ = {
#       # "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
#    #
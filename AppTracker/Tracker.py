import time, psutil, json, requests, datetime
from requests.models import PreparedRequest
'''
This class tracks how long the array of executables
runs in a single session. It then sends the data to
a specified server (in the config file) as a post
request.
'''
class Tracker():
    
    # Basic Initializer
    def __init__(self):
        self.currentgame = ""

    # Runs the Tracker with the executables from the config file
    def run(self):
        self.track(self.getconfig("tracked_games"))

    # Returns the current time
    def getcurtime(self):
        ret = datetime.datetime.now().time()
        hour = ret.hour
        minutes = ret.minute
        seconds = ret.second
        return "{}:{}:{}".format(hour, minutes, seconds)
    
    # Returns the current date
    def getcurdate(self):
        today = datetime.datetime.today()
        year = today.year
        month = today.month
        day = today.day
        return "{}-{}-{}".format(year, month, day)

    # Requests the tracked executables from a server url in the config file
    def requesttrackedgames(self):
        try:
            r = requests.get(url = self.getconfig("update_tracked_games_url"))
            obj = json.loads(r.text)
            return obj["tracked_games"]
        except PermissionError as permerr:
            print(permerr)
        except Exception as ex:
            print(ex)

    
    def getconfig(self, key):
        with open("AppTracker/bin/tracker_config.json", "r") as tracker_config:
            settings = json.load(tracker_config)
            return settings[key]

    def updatetrackablegames(self):
        tracked_games = self.requesttrackedgames()
        cursettings = self.getsettings()
        cursettings["tracked_games"] = tracked_games
        self.writeconfig(cursettings)
        
    def getrunningapps(self):
        try:
            running_apps = []
            for process in psutil.process_iter():
                running_apps.append(process.name())
            return running_apps
        except Exception as ex:
            print(ex)

    def trackedgameisrunning(self, tracked_games): 
        for app in self.getrunningapps():
            for game in tracked_games:
                if app == game:
                    self.currentgame = game
                    return True
        return False

    def senddata(self, data):
        try:
            requests.post(self.prepurl(data))
            self.clearbackupdata()
            return True
        except Exception as err:
            print(err)
            print("send failed")
            self.backupdata(data)
            return False
    
    def sendbackup(self, data):
        try:
            requests.post(self.prepurl(data))
            return True
        except Exception as ex:
            print("FROM DUMPDATA()")
            print(ex)
            print("")
            return False
        
    def getsettings(self):
        with open("AppTracker/bin/tracker_config.json", "r") as tracker_config:
            return json.load(tracker_config)

    def writeconfig(self, data):
        with open("AppTracker/bin/tracker_config.json","w") as tracker_config:
            json.dump(data, tracker_config,indent=4)
   
    def backupdata(self, data):
        settings = self.getsettings()
        settings["back_up_data"].append(data)
        self.writeconfig(settings)
            
    def clearbackupdata(self):
        settings = self.getsettings()
        print(settings["back_up_data"])
        for index, data in enumerate(settings["back_up_data"]):
            try:
                if self.sendbackup(data):
                    del settings["back_up_data"][index]
            except Exception as ex:
                print("FROM CLEARBACKUPDATA()")
                print(ex)
                print("")
        self.writeconfig(settings)

    def prepurl(self, data):
        req = PreparedRequest()
        req.prepare_url(self.getconfig("post_data_url"), data)
        return req.url

    def track(self, tracked_games):
        tracking = False
        while True:
            try:
                if self.trackedgameisrunning(tracked_games):
                    tracking = True
                    start = time.time()
                    while tracking:
                        if not self.trackedgameisrunning(tracked_games):
                            tracking = False
                    finish = time.time()
                    total_time = (finish - start)/60
                    data = {
                        "date": self.getcurdate(),
                        "time": self.getcurtime(),
                        "game": self.currentgame,
                        "tot_time": total_time,
                        "userid": self.getconfig("userid"),
                        "bayid": self.getconfig("bayid")
                    }
                    self.updatetrackablegames()
                    self.senddata(data)
            except Exception as ex:
                print(ex)

if __name__ == "__main__":
    tracker = Tracker()
    tracker.run()
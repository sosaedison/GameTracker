# Voxel Application Time Tracker 
The purpose of this repo is to host the code that runs on voxel machines and reports gameplay time to the python-flask backend. 

## Application Structure
The app is run from `Driver.py`, which imports and runs a Tkinter instance which hold all the UI components for the app UI.
`Mainview.py` is there the loging view and the view that allows you to switch the tracker off and on live.

<img width="402" alt="Screen Shot 2021-05-28 at 10 58 42 PM" src="https://user-images.githubusercontent.com/17048396/120057384-4253ed80-c008-11eb-98bb-b2a9e6b5a38e.png">

Once logged in, the switch view will show and you can turn the tracker off and on via the UI

## Roadmap

I would like to finish making the backend in Node.js/Express for this UI. And then I want to make the backend in Django to further my python skills. 

## Running the application
- Run `pip install -r requierments.txt` to install all dependencies. and then run `python3 Driver.py` on Mac/Linux to see the UI. The UI is based on a tracker_config.jason file and if the `bayid` field is missing, the UI assumes you're not logged in. 

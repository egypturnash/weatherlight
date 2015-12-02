# -*- coding: utf-8 -*-
#
# peggy's little foyer-light controller
#
# selects from a set of lifx scenes based on the temperature from forecast.io
#
#
# TODO: change color based on a weighted average of the next few hours' conditions instead of the next hour
#
# TODO: maybe change my studio lighting when it's a cloudy day?
#
# keep an eye on the time, needs to be able to handle the case of lasttime was last night?
# if lasttime > now:
#   lasstime = midnight
#
# if lasttime < chosentime (~8:10am) > now:
#      SetScene(scenes['Studio Working (Cloudy)'],lifxToken)
#
# TODO: parse list of lights, add 'group off' items to the menu?
#
# TODO: package as an app and build a UI for setting all this up. RIGHT.
#       In my copious free time.
#

import requests
import sys
import math
import time

from rumps import *

lifxToken = 'c2eb1a794f21fe61907b5f601f9a54e27224763f5b4b77392f6d34c8b97d145c'
# generate your token at https://cloud.lifx.com/settings

darkSkiesToken = '1a3d891deedaefbfb289b7e83e034682'
# generate your token at https://developer.forecast.io

#
# desired temperature ranges for scenes you've set up via the lifx app
# 
choices = [
    {'scene':'Foyer Freezing',      'lower':-460,   'upper':33,     'note':'It is LITERALLY FREEZING outside.'}, # -460f ≅ 0k
    {'scene':'Foyer Cold',          'lower':34,     'upper':54,     'note':'Wear a heavy coat, miss dragon.'},
    {'scene':'Foyer Chilly',        'lower':55,     'upper':66,     'note':'Light coat. Or sweater. Or something.'},
    {'scene':'Foyer Hot',           'lower':67,     'upper':74,     'note':'As long as your sin globes are covered, anything goes.'},
    {'scene':'Foyer Really Hot',    'lower':75,     'upper':9940,   'note':'It is HOT. Take a parasol or something.'}, #9940f ≅ surface of the sun
]

nighttime = {
    'scene':'Foyer Evening',
    'nightBegins': 20.5,    # 24-hour decimal time. 8:30PM = 20.5.
    'nightEnds': 8.0,       # 24-hour decimal time. 8 AM = 8.0.
}

# temperature offsets for various conditions
# as defined by forecast.io's 'icon' property of the forecast
offsets = {
    'clear-day':0,
    'clear-night':0,
    'rain':-10,
    'snow':-10,
    'sleet':-10,
    'wind':-5,
    'fog':0,
    'cloudy':-5,
    'partly-cloudy-day':-5,
    'partly-cloudy-night':-5,
}

latitude = '47.6659248'
longitude = '-122.3181908'
# where are you?
# maybe this should talk to OSX's location manager… but that starts to look like work

repeatDelay = 9*60  # delay between repetitions, in seconds
                    # lifx' api throttles you to about once a minute
                    # forecast.io throttles to 1000 requests/day (about one every 1.4 min)

#
# turns a list-with-sublists of scenes into a RUMPS menu definition
#
def BuildMenu (scenelist, parent=None):
    # print 'Building menu from',scenelist
    # print scenes
    
    themenu = []
    
    for scene in sorted(scenelist):
        uuid = ''
        children = {}
        
        if type(scenelist[scene]) == dict:
            if len(scenelist[scene]) > 1:      # scene has multiple children;
                children = scenelist[scene]    # save them for recursing
            elif len(scenelist[scene]) == 1:           # deal with single/no children
                if scenelist[scene].keys()[0] != '':   # single just tag on the name, it's messy
                    scene = ' '.join([scene,scenelist[scene].keys()[0]])
        
        if parent:
            scene = ' '.join([parent,scene])
        if children == {}:
            print scene
            themenu.append(MenuItem(scene, callback=MenuSetScene))
        else:
            print 'scene',scene,'---->',len(children)
            submenu = BuildMenu(children,scene)
            themenu.append((scene,submenu))
        
    return themenu

#
# sorts the scenes, returns a list with sublists
#
def SortScenes (scenes):
    sortedKeys = sorted(scenes)
    repeatedKeys = {}
    
    # find repeated first words
    for key in sortedKeys:
        firstWord = key.partition(' ')[0]
        # print firstWord
        if firstWord not in repeatedKeys:
            repeatedKeys[firstWord] = {}
        # print key.partition(' ')[2],scenes[key]
        repeatedKeys[firstWord][key.partition(' ')[2]] = scenes[key]
        # repeatedKeys[firstWord].append(key.partition(' ')[2])
    
    return repeatedKeys


#
# picks a scene based on the forecast
#
def ChooseScene (choices, offsets, nighttime, forecast):
    # there should be some logic here to check the time
    # and if it's earlier or later than certain times
    # we cancel out and just display the nocturnal light
    
    now = time.localtime()
    now = now.tm_hour+((1.0/60)*now.tm_min)
    if (now < nighttime['nightEnds']) or (now > nighttime['nightBegins']):
        print "it's nighttime! the time is now ",now
        return nighttime['scene']
    
    # figures out temperature offset based on the next hour's condition
    condition = forecast['hourly']['data'][0]['icon']
    offset = offsets[condition]
    
    temperature = round(forecast['hourly']['data'][0]['temperature']+offset)
    print 'current temperature:',temperature
    
    for choice in choices:
        if temperature >= choice['lower'] and temperature <= choice['upper']:
            print choice,temperature
            # print ('{}º — {}º: {}'.format(choice['lower'], choice['upper'], choice['note']))
            return choice['scene']

#
# contacts LIFX and acquires a list of scenes
#
def GetScenes():
    headers = {
        "Authorization": "Bearer %s" % lifxToken,
    }
    
    print 'authorizing with lifx'
    authorization = requests.get('https://api.lifx.com/v1/lights/all', headers=headers)
    
    if authorization.status_code != 200:
        print "\ninvalid authorization, maybe check your token?\n"
        sys.exit()
    
    print 'asking lifx for all scenes'
    scenerequest = requests.get('https://api.lifx.com/v1/scenes', headers=headers).json()
    
    # I am sure there is a much more pythonic way to do this. Works though.
    scenes = {}
    for scene in scenerequest:
        scenes[scene['name']] = scene['uuid'].encode('ascii')
    
    print ''
    return scenes

#
# sets a lifx scene
#
def SetScene(scene):
    headers = {
        "Authorization": "Bearer %s" % lifxToken,
        "duration": 60*5,
    }
    
    uuid = scenes[scene]
    
    result = requests.put('https://api.lifx.com/v1/scenes/scene_id:'+uuid+'/activate', headers=headers)
    return result

#
# sets a scene from the menu bar
#
def MenuSetScene(sender):
    scene = sender.title
    SetScene(scene)
    
    

#
# refreshes lifx scenes, sets up menus
#
def RefreshScenes(sender=None):
    global scenes
    
    print 'refreshing lifx scenes...'
    scenes = GetScenes()
    sortedscenes = BuildMenu(SortScenes(scenes))
    app.menu.clear()
    app.menu = sortedscenes+[
        None,
        MenuItem('Refresh scenes', callback=RefreshScenes),
        MenuItem('Quit', callback=rumps.quit_application)
    ]

#
# acquires a forecast from forecast.io
#
def GetForecast(latitude, longitude):
    print 'getting forecast...'
    forecast = requests.get('https://api.forecast.io/forecast/'+darkSkiesToken+'/'+latitude+','+longitude).json()
    return forecast

#
# timed function to deal with weather tricks
#
@rumps.timer(repeatDelay)
def doWeatherLight(sender):
    global lastScene
    
    try:
        forecast = GetForecast(latitude, longitude)
        whichScene = ChooseScene(choices, offsets, nighttime, forecast)
        if lastScene == whichScene:
            print "no need to change the scene right now."
        else:
            print 'setting scene:',whichScene
            SetScene(whichScene)
            lastScene = whichScene
    except requests.exceptions.ConnectionError:
        print "couldn't connect..."


#
# all the functions are ready, let's build the app
#
app = App(name='weatherlight', icon='images/menu-normal.png', quit_button=None)

print "\n ~ peggy's little foyer-light script ~\n"
lastScene = ''

RefreshScenes()
# scenes = GetScenes()
# sortedscenes = BuildMenu(SortScenes(scenes))
#
# app.menu = sortedscenes+[
#     None,
#     MenuItem('Refresh scenes', callback=RefreshScenes),
# ]

app.run()

# the end

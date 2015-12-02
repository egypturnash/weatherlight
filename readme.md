# Peggy's little foyer-light controller

Selects from a set of lifx scenes based on the temperature and forecast.
Also provides a menu bar item to let you choose any scene.

If multiple scenes start with the same word, they will be nicely sorted into submenus.

This program does not care about individual lights; it operates entirely on the level of scenes. Use the LIFX app to set those up.

## How to use:
* edit the source to set your schedule
* also stick your lifx and forecast.io keys in there
* python weatherlight.py

You may be saying to yourself "wait, can't If This Then That change a light based on the temperature and weather conditions?".

Yes but no. The weather triggers in IFTTT are pretty simple; you can change a light or scene when the temperature lowers past a certain threshold, when it raises past a threshold, or when rain is coming. Plus, I dont want to have my foyer telling me what it's like outside 24-7; if I get up in the middle of the night, I want it to be a nice dim red instead of a bright blue to say that it's cold outside. For a while I was doing fine with LIFX's schedule overlaid on IFTTT's weather triggers, but once the temperature dropped below my 'it's freaking cold' threshold and stayed there, IFTTT never sent any more temperature change events, so when LIFX's scheduler told it to go to the nighttime red, it stayed there for a few weeks until I wrote this script.

This script also lets the weather conditions modify the displayed temperature. I live in Seattle, where rain is rarely more than a drizzle. If you live somewhere it really *rains* in, then you might want a separate light to explicitly say "hey rain is coming".

Then since I was already getting a list of the scenes, I figured, why not add in the menu bar functionality so I don't have to hunt down one of the tablets or my phone when I'm at the computer and want to change the lighting?


TODO: change color based on a weighted average of the next few hours' conditions instead of the next hour

TODO: maybe change my studio lighting when it's a cloudy day?

keep an eye on the time, needs to be able to handle the case of lasttime was last night?
if lasttime > now:
  lasstime = midnight

if lasttime < chosentime (~8:10am) > now:
     SetScene(scenes['Studio Working (Cloudy)'],lifxToken)

TODO: parse list of lights, add 'group off' items to the menu?

TODO: store keys and schedule outside of the script

TODO: package as an app and build a UI for setting all this up. RIGHT.
      In my copious free time.
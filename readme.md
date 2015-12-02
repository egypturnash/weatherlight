# Peggy's little foyer-light controller

Selects from a set of lifx scenes based on the time, temperature and forecast.
Also provides a menu bar item to let you choose any scene.

If multiple scenes start with the same word, they will be nicely sorted into submenus.

This program does not care about individual lights; it operates entirely on the level of scenes. Use the LIFX app to set those up.

## How to use:
* edit the source to set your schedule
* also stick your lifx and forecast.io keys in there
* python weatherlight.py
* enjoy!
* if you edit your scenes in the lifx app, then do 'refresh scenes' in the menu.

You may be saying to yourself "wait, can't If This Then That change a light based on the temperature and weather conditions?".

Yes but no. Setting up multiple temperature triggers in IFTTT is a pain in the ass, and hard to change. Plus it didn't interact well with also wanting my light to be a dim red in the evening once temperatures dropped past my lowest "if the temp drops past this then..." threshold. This does both.

This script also lets the weather conditions modify the displayed temperature. I live in Seattle, where rain is rarely more than a drizzle. If you live somewhere it really *rains* in, then you might want a separate light to explicitly say "hey rain is coming".

Then since I was already getting a list of the scenes, I figured, why not add in the menu bar functionality so I don't have to hunt down one of the tablets or my phone when I'm at the computer and want to change the lighting?

##License
This is licensed under the WTFPL. Do whatever the fuck you want with it.

If you turn this into a polished commercial app I'd appreciate a free copy. And some money if it makes any. But whatever.

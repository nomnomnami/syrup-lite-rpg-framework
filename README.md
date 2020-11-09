# Syrup Lite RPG Framework
inventory, shop, crafting, quests, and battle systems for ren'py!

originally designed for Syrup 2: Candy Alchemy RPG. now it's released to the world...!

feel free to modify these scripts to your heart's content. it's ok to use it for commercial projects, too! credit is appreciated, but not necessary.

## HOW TO USE

you can download the sample project and guide pdf from here: https://nomnomnami.itch.io/syrup-lite-rpg-framework
the pdf is 18 pages and has much more detailed instructions for beginner programmers.

all the scripts will work with ren'py version 7.3.5.606 and up!
they're split into modules, so you can pick and choose the features you want.
crafting+shop requires item scripts to work, but battling works on its own.

below is a summary of what you can find in each file.

### sample-script.rpy

basic navigation and setup for the various screens to work properly. copypaste its contents into script.rpy!

### battle-screens.rpy

battle menu, overlay, and damage indicator screens. change the appearance of battles here.

### battle-script.rpy

setup and event processing for the battle system. adjust battle logic and event flow to suit your needs.

### battle-units.rpy

define your enemies and sprite animations here.

### crafting-screens.rpy

recipe screens for crafting items. customize the styles to fit your game!

### item-definitions.rpy

define your items and category lists here. add your own functions to do even more with the items!

### item-screens.rpy

inventory and currency display. the grid is adjustable (shows 50 items by default)

### quest-definitions.rpy

define quests here. currently only exchanges items for money.

### quest-screens.rpy

quest management screens, plus a quest complete notifier.

### shop-screens.rpy

screen to buy and sell items, and to set the buy/sell/toss item amount.

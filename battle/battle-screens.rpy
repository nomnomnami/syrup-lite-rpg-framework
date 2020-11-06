init offset = -1

## IMPORTANT! ## IF YOU USE THE ITEM SCRIPTS you can take these lines out

# defined in item-screens.rpy
transform zoomx(x):
    zoom x
    nearest True
# defined in item-definitions.rpy
define battle_items = []
python:
    def check_inv_for(itemtype):
        for i in itemtype:
            if inv.count(i) > 0:
                return True

## THAT'S ALL! ## had to do this so it'd still work for people only using the battles...

##############################################################################
## battle menu

screen battle_menu():

    # this flag decides whether to show the main battle menu, or items menu
    default showbattlemenu = True

    tag menu
    style_prefix "battle"

    hbox:
        xalign .5
        yalign .9
        spacing 40

        if showbattlemenu:
            textbutton _("Attack"):
                action Jump("battle_attack")
                tooltip _("Fight! Beat the enemy into submission!")

            textbutton _("Guard"):
                action Jump("battle_defend")
                tooltip _("Protect yourself! Halves incoming damage.")

            if check_inv_for(battle_items):
                textbutton _("Item"):
                    action SetScreenVariable("showbattlemenu", False)
                    tooltip _("Use your candy creations in battle!")

            if not enemy.boss:
                textbutton _("Run"):
                    action Jump("battle_ran")
                    tooltip _("Escape the encounter and return home.")
        else:
            #ITEM MENU
            if "item_sucker" in inv:
                button:
                    add "item sucker" align (.5,.5) at zoomx(2)
                    action Jump("use_sucker")
                    tooltip _("Recover HP during battle")
                # add new items here
                # only room for 4 at a time with this setup

            textbutton _("Cancel"):
                action SetScreenVariable("showbattlemenu", True)
                tooltip _("Close the item menu")

    $ tooltip = GetTooltip()

    if tooltip:
        text "[tooltip!t]" xalign .2 yalign .99

default turn = 0
default atkbuff = 0
default defbuff = 0

##############################################################################
## battle overlay

screen battleoverlay():
    zorder 99

    label _("BATTLE!") style "battle_label" align (.5,.05)

    label _("Turn: [turn]") xalign .75 yalign .1 style "battleinfo_label"

    # HP bars
    bar value playerHP range playerMAXHP style "battle_bar" at battle_party1
    bar value enemyHP range enemy.MAXHP style "battle_bar" at battle_enemy1

    frame:
        style_group "battleinfo"
        xalign .025
        vbox:
            hbox:
                xfill True
                label _("Syrup")
                text _("Lv [playerLV]") style "battleHP_text" xalign 1.0

            if not playerHP < playerMAXHP/3:
                text _("HP: [playerHP] / [playerMAXHP]") style "battleHP_text"
            else:
                text _("HP: [playerHP] / [playerMAXHP]") style "battleLOWHP_text"

            frame:
                style "battleinfo_stat_frame"
                has vbox
                if atkbuff:
                    text "ATK: [playerATK] {color=#ff7c9b}+ [atkbuff]{/color}"
                else:
                    text "ATK: [playerATK]"
                if defbuff:
                    text "DEF: [playerDEF] {color=#ff7c9b}+ [defbuff]{/color}"
                else:
                    text "DEF: [playerDEF]"
                text "LUC: [playerLUC]"

    frame:
        style_group "battleinfo"
        xalign .975
        vbox:
            label "[enemy.name!t]"
            hbox:
                if enemy.boss:
                    add "bosscrown" yalign .5
                text _("HP: [enemyHP] / [enemy.MAXHP]") style "battleHP_text"
            frame:
                style "battleinfo_stat_frame"
                has vbox
                text "ATK: [enemy.ATK]"
                text "DEF: [enemy.DEF]"
                text "LUC: [enemy.LUC]"

            null height 8
            text "[enemy.info!t]"

style battle_label_text:
    size 60
    color "#FFF"
    outlines [(6,"#A51F63",1,1)]

image hp full:
    "gui/bar/left.png"
    nearest True
image hp empty:
    "gui/bar/right.png"
    nearest True
style battle_bar:
    left_bar "hp full"
    right_bar "hp empty"
    xsize 120
    ysize 10
    yoffset 90

style battleinfo_frame:
    xsize 250
    ysize 320
    yalign .42
    padding (16,16)
style battleinfo_vbox:
    spacing 6
style battleinfo_stat_frame:
    background "#ffe0ed"
    xfill True
    padding (10,6)

style battleinfo_label_text:
    color "#FFF"
    outlines [(2,"#525252",0,0),(3,"#525252",1,1)]

style battleinfo_text:
    color "#333"

style battleHP_text:
    color "#FFF"
    outlines [(2,"#5d5d5d",0,0)]
style battleLOWHP_text is battleHP_text:
    outlines [(2,"#bd2c47",0,0)]

style battle_button:
    background "[prefix_]battle"
    xysize (200,100)
    size_group "battle"
style battle_button_text:
    xalign .5
    idle_color gui.text_color
    size gui.label_text_size


##############################################################################
## show damage/crit/heal/miss

## DAMAGE NUMBERS
default damage = 0

screen showdamage(target):
    zorder 100
    style_prefix "damage"

    if target=="player":
        text "[damage]" at battle_party1, playerdamage_appear
    else:
        text "[damage]" at battle_enemy1, damage_appear

    timer .1 action Hide('showdamage')

style damage_text:
    bold True
    color "#FFF"
    outlines [(2,"#000",0,0)]

transform damage_appear:
    on show:
        alpha 1 yoffset -10 xoffset 0
        easeout .05 yoffset -20
    on hide:
        easeout .5 alpha 0 yoffset 100 xoffset 10
transform playerdamage_appear:
    on show:
        alpha 1 yoffset -10 xoffset 0
        easeout .05 yoffset -20
    on hide:
        easeout .5 alpha 0 yoffset 100 xoffset -10

screen showcrit():
    zorder 100
    style_prefix "damage"

    text "[damage]" color "#ff3939" size 36 at battle_enemy1, damage_appear

    timer .1 action Hide('showcrit')

screen showheal():
    zorder 100
    style_prefix "damage"

    # on "show" action Play("sound", audio.heal)

    text "[damage]" color "#53ff55" at battle_party1, heal_appear

    timer .1 action Hide('showheal')

transform heal_appear:
    on show:
        alpha 0 yoffset -10 xoffset 15
        easeout .1 alpha 1
    on hide:
        easeout .6 alpha 0 yoffset -60

screen showmiss():
    zorder 100
    style_prefix "damage"

    text _("MISS") at battle_enemy1, miss_appear

    timer .1 action Hide('showmiss')

transform miss_appear:
    on show:
        alpha 0 yoffset -10
        easeout .1 alpha 1
    on hide:
        easeout .6 alpha 0 yoffset 50

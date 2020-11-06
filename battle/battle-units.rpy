##############################################################################
# Enemy class

init -2 python:
    class Enemy(store.object):
        def __init__(self, name, id, info, MAXHP, ATK, DEF, LUC, RES, EXP=0, G=0, drop=None, boss=False):
            self.name=name #enemy name as seen by the player
            self.id=id #string to be used as a codename
            self.info=info #enemy description

            #STATS
            self.MAXHP=MAXHP #base HP value
            self.ATK=ATK #physical attack points
            self.DEF=DEF #physical defense points
            self.LUC=LUC #factors into crit and dodge rate
            self.RES=RES #magic effectiveness multiplier

            #REWARDS (default to 0 or None)
            self.EXP=EXP #how much exp you get for defeating them
            self.G=G #gold earned by defeating them
            self.drop=drop #item to drop

            #extra
            self.boss=boss #if True, you can't run away

        # adds enemy to list of seen enemies
        def see_enemy(self):
            if self.id not in seen_enemies:
                seen_enemies.append(self.id)

# define your own enemies here!
define m_goop = Enemy(_("Forest Goop"), "m_goop",
    info=_("High defense, weak to magic."),
    MAXHP=27, ATK=4, DEF=7, LUC=0, RES=.5,
    EXP=3, G=2, drop="item_sucker")

##############################################################################
# Battle transforms
transform battle_party1:
    xalign .4
    yalign .52
transform battle_enemy1:
    xalign .6
    yalign .52

image battle bg = Solid("#c6ffa3")
image stage bg = Frame("gui/frame.png",4,4, xysize=(700,400), yoffset=-196)

##############################################################################
# Sprite animations

##PLAYER SPRITES
image player syrup idle:
    "player syrup idle1"
    pause .2
    "player syrup idle2"
    pause .2
    "player syrup idle1"
    pause .2
    "player syrup idle3"
    pause .2
    repeat

image player syrup attack:
    "player syrup attack1"
    pause .1
    "player syrup attack2"
    pause .1
    "player syrup attack3"

image player syrup hit:
    "player syrup hit1"
    pause .1
    "player syrup hit2"
    pause .06
    "player syrup hit1"
    pause .06
    "player syrup hit2"

image player syrup guard:
    "player syrup guard1"
    pause .1
    "player syrup guard2"
image player syrup guardhit:
    "player syrup guard3"
    pause .1
    "player syrup guard2"

image player syrup down:
    "player syrup down1"
    xoffset 10

image player syrup run:
    parallel:
        "player syrup run1"
        pause .1
        "player syrup run2"
        pause .1
        "player syrup run1"
        pause .1
        "player syrup run3"
        pause .1
        repeat
    parallel:
        xoffset 0
        easein .8 xoffset -150
    parallel:
        alpha 1.0
        pause .4
        linear .4 alpha 0

image player syrup win:
    "player syrup win1"
    pause .1
    block:
        "player syrup win2"
        pause .3
        "player syrup win3"
        pause .3
        repeat

##ENEMY SPRITES
image enemy goop idle:
    "enemy goop idle1"
    pause .12
    "enemy goop idle2"
    pause .1
    "enemy goop idle3"
    pause .12
    "enemy goop idle4"
    pause .15
    repeat
image enemy goop move:
    "enemy goop idle"
image enemy goop attack:
    "enemy goop idle"
    xoffset 0
    linear .06 xoffset -20
    easein .2 xoffset 0
image enemy goop dodge:
    "enemy goop idle"
    xoffset 0
    linear .06 xoffset 20
    easein .2 xoffset 0
image enemy goop hit:
    "enemy goop hit1"
    pause .1
    "enemy goop hit2"
    pause .06
    "enemy goop hit1"
    pause .06
    "enemy goop hit2"
image enemy goop down:
    "enemy goop down1"
    pause .1
    "enemy goop down2"
    pause .1
    "enemy goop down3"
    pause .1
    "enemy goop down4"
    pause .1
    "enemy goop down5"
    pause .1
    "enemy goop down6"

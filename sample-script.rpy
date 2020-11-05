##############################################################################
## Sample script

image bg shop = Solid("#ffbedb")
image bg lab = Solid("#c3beff")

label start:

    ## copy this block into your own game
    python:
        gold = 20 #starting amount
        inv = []
        seen_items = []

        # crafting
        known_recipes = []
        seen_recipes = []
        made_recipes = []
        newitem = ""

        # shop inventory
        market = [ ]
    ##

    $ known_recipes = ["item_sugar", "item_sucker"]
    $ market = [ "item_water", "item_paper", "item_beet" ]

    $ InvItem(*item_sugar).pickup(3)
    $ InvItem(*item_water).pickup(2)
    # $ InvItem(*item_sucker).pickup(1)
    # $ InvItem(*item_beet).pickup(200)

label test_menu:
    scene bg shop
    menu:
        "Inventory":
            jump inventory
        "Crafting":
            jump start_crafting
        "Buy Items":
            jump market_buy
        "Sell Items":
            jump market_sell
        "Battle":
            jump pre_battle

label inventory:
    scene bg lab
    call screen inventory(inv) with Dissolve(.2)
    jump test_menu

label start_crafting:
    scene bg lab
    call screen recipes() with Dissolve(.2)

label craft_success:

    show screen reward(newitem.image)
    "Made {color=#d48}[newitem.name!t]{/color}!"
    hide screen reward

    jump start_crafting

label market_buy:
    scene bg shop
    call screen shop(market)
    jump test_menu

label market_sell:
    scene bg shop
    call screen inventory(inv, selling=True)
    jump test_menu

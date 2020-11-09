
##############################################################################
## Shop Screen

screen shop(seller):
    modal True

    label _("Market") style "special_label" align (.1,.05)

    use gold_count()

    on "show" action SetVariable("selected_item", None)

    frame:
        style "invgrid_frame"

        vbox:
            xalign .5
            # column names
            hbox:
                style_group "description"
                xsize 520
                xfill False
                offset (20,8)
                label _("Item")
                null width 230
                label _("In Bag")
                label _("Price") xalign 1.0

            # list of item buttons
            frame:
                margin (14,14)
                use shoplist(seller)

    use item_description()

    # you can change the style at the bottom of item-screens.rpy
    textbutton _("Return"):
        style "offset_return_button"
        yalign .98
        action [SetVariable("selected_item", None), Return()] keysym "game_menu"

screen shoplist(seller):

    vpgrid style_prefix "marketitem":
        cols 1 mousewheel True draggable True scrollbars "vertical"

        # item buttons
        for item in seller:
            $ thisitem = InvItem(*set_item(item))
            button:
                action ShowTransient("buying", whichitem=thisitem, howmuch=thisitem.value)
                hovered SetVariable("selected_item", item)
                sensitive thisitem.check_price()

                # mark items as new
                if item not in seen_items:
                    foreground "itemmarker"
                # show item image and name
                hbox:
                    if thisitem.check_price():
                        add thisitem.image
                    else:
                        add thisitem.image alpha .3
                    null width 10
                    text "[thisitem.name!t]" style "marketitem_button_text"

                # how many in bag, and price
                hbox:
                    align (.98,.5)
                    text "{}" .format(inv.count(item)) style "marketitem_button_text"
                    fixed:
                        xsize 120
                        text "[thisitem.value]" align (1.0,.5)

style marketitem_text is item_text:
    insensitive_outlines [(3, "#aaa",0,0)]
style marketitem_button is item_button
style marketitem_button_text is item_button_text:
    insensitive_color "#aaa"

screen buying(whichitem, howmuch, selling=False):
    modal True

    add Solid("#f2cdd980") #transparent overlay

    default amount = 1

    frame:
        style_group "making"

        # change label based on the action
        if howmuch > 0:
            if selling:
                label _("Selling...") style "description_label" anchor (20,44)
            else:
                label _("Buying...") style "description_label" anchor (20,44)
        else:
            label _("Tossing...") style "description_label" anchor (20,44)

        vbox:
            xalign .5
            yfill True
            # item name and a button to cancel out
            frame:
                style_group "special_small"
                has hbox
                xfill True
                label whichitem.name

                textbutton "x":
                    style "inventory_button"
                    action Hide("buying") keysym "game_menu"
                    xalign 1.0

            null height 10

            # arrow buttons to select amount, with the item image in between
            hbox:
                style_prefix "inventory"
                ysize 48
                xfill True
                textbutton "<":
                    ysize 48
                    xalign 1.0
                    action SetScreenVariable("amount", (amount-1))
                    sensitive amount > 1

                hbox:
                    xalign .5
                    xoffset 40
                    add whichitem.image
                    fixed:
                        xsize 148
                        text " x [amount]" yalign .8

                textbutton ">":
                    ysize 48
                    if howmuch > 0:
                        if selling:
                            action SetScreenVariable("amount", (amount+1))
                            sensitive amount < inv.count(whichitem.id)
                        else:
                            action SetScreenVariable("amount", (amount+1))
                            sensitive amount != int(gold/howmuch) and gold>=howmuch
                    else:
                        action SetScreenVariable("amount", (amount+1))
                        sensitive amount < inv.count(whichitem.id)

            # shortcuts to set amount to 1 or max
            hbox:
                style_prefix "inventory"
                xalign .5
                spacing 20
                textbutton _("RESET"):
                    style "sort_button"
                    action SetScreenVariable("amount",1)
                    sensitive amount>1

                textbutton _("MAX"):
                    style "sort_button"
                    if howmuch > 0:
                        if selling:
                            action SetScreenVariable("amount", inv.count(whichitem.id))
                            sensitive amount < inv.count(whichitem.id)
                        else:
                            action SetScreenVariable("amount", int(gold/howmuch))
                            sensitive amount < int(gold/howmuch)
                    else:
                        action SetScreenVariable("amount", inv.count(whichitem.id))
                        sensitive amount < inv.count(whichitem.id)

            # show how many we have and how much the final price will be
            hbox:
                xsize 300
                xfill True
                xalign .5
                $ bagcount = inv.count(whichitem.id)
                text _("In bag: [bagcount]") yalign .5
                if howmuch > 0:
                    if selling:
                        $ price = int(whichitem.value*amount/2)
                    else:
                        $ price = whichitem.value*amount
                    hbox:
                        xalign 1.0
                        xsize 100
                        text _("Price:")
                        text "[price]" yalign .5

            # buttons to make it happen
            if howmuch > 0:
                if selling:
                    textbutton _("SELL"):
                        action [ Function(whichitem.sell, amount), SetVariable("selected_item", None), Hide("buying")]
                else:
                    textbutton _("BUY"):
                        action [ SensitiveIf((whichitem.value*amount)<=gold), Function(whichitem.buy, amount), Hide("buying")]
            else:
                textbutton _("TOSS"):
                    action [ Function(whichitem.toss, amount), SetVariable("selected_item", None), Hide("buying")]

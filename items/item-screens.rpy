
##############################################################################
## Currency display

# if your game doesn't use money, set this to False
define uses_gold = True

screen gold_count():

    frame xsize 200:
        align (.98,.04) padding (10,10)
        has hbox
        xfill True

        label _("Gold")
        #add "money icon"

        text "{}" .format(gold) xalign 1.0

##############################################################################
## Inventory Screens

default selected_item = None

screen item_description(selling=False):
    frame xysize 1200, 56:
        align (.5,.86)
        padding (10,10,50,10)
        label _("Description") style "description_label" yanchor 24
        if selected_item is not None:
            $ thisitem = set_item(selected_item)
            text thisitem[3] offset (14,6) #info text
        elif selling:
            text _("Choose an item to sell.") offset (14,6) color "#8b8b8b"
        else:
            text _("Select an item to read its description.") offset (14,6) color "#8b8b8b"

screen inventory(collection, selling=False):
    modal True

    #for page navigation
    default first = 0
    default last = invgrid_x*invgrid_y
    default page = 1

    default sorted = False
    on "show" action SetVariable("selected_item", None)

    if uses_gold:
        use gold_count()

    # screen title
    if selling:
        label _("Market") style "special_label" align (.1,.05)
    else:
        label _("Inventory") style "special_label" align (.1,.05)

    style_prefix "inventory"

    # items
    use invgrid(collection, page, first, last)

    # page navigation
    hbox:
        xpos 562
        yalign .44
        spacing 532
        textbutton "<" ysize 256:
            sensitive first>0
            action [ SetScreenVariable("first", first-invgrid_x*invgrid_y), SetScreenVariable("last", last-invgrid_x*invgrid_y),
            SetScreenVariable("page",page-1) ]

        textbutton ">" ysize 256:
            sensitive len(collection)>last
            action [ SetScreenVariable("first", first+invgrid_x*invgrid_y), SetScreenVariable("last", last+invgrid_x*invgrid_y),
            SetScreenVariable("page",page+1) ]

    # sorting
    hbox:
        xpos 600
        yalign .24
        spacing 4
        style_prefix "sort"
        textbutton _("SORT BY:") text_color gui.idle_color

        textbutton _("NAME"):
            if not sorted:
                action [Function(collection.sort, key=sortbyname), SetScreenVariable("sorted", True)]
            else:
                action [Function(collection.sort, key=sortbyname, reverse=True), SetScreenVariable("sorted", False)]

        if uses_gold:
            textbutton _("PRICE"):
                if not sorted:
                    action [Function(collection.sort, key=sortbyprice), SetScreenVariable("sorted", True)]
                else:
                    action [Function(collection.sort, key=sortbyprice, reverse=True), SetScreenVariable("sorted", False)]

        ## INSERT SORTING CATEGORIES HERE ##

    # item details, appears once you click an item
    if selected_item is not None:
        $ thisitem = InvItem(*set_item(selected_item))
        frame xysize 432, 200:
            xalign .1 ypos 352
            padding (10,10)

            label _("Item Details") style "description_label" yanchor 24

            vbox pos (30, 20):
                spacing 10

                hbox ysize 96:
                    add thisitem.image at zoomx(2)

                    hbox xsize 260:
                        yalign 1.0 xfill True
                        text "x {}" .format(collection.count(thisitem.id)) xalign 0

                        if uses_gold and thisitem.value > 0:
                            hbox xsize 100:
                                xalign 1.0
                                text _("Price:")
                                text " {}" .format(int(thisitem.value/2))

                label thisitem.name style "special_small_label"

            ## !! IMPORTANT !! you need the buying screen from shop-screens.rpy for these buttons to work!
            vbox:
                align (.9,.2)
                style_group "sort"
                if selling:
                    textbutton _("SELL") action ShowTransient("buying", whichitem=thisitem, howmuch=thisitem.value, selling=True)
                else:
                    textbutton _("TOSS") action ShowTransient("buying", whichitem=thisitem, howmuch=0)
            # shop-free alternative toss button:
                #textbutton _("TOSS") action [Function(thisitem.toss, 1), SetVariable("selected_item", None)]

    use item_description(selling)

    textbutton _("Return") action Jump("test_menu") style "offset_return_button" yalign .98

style description_label_text:
    size gui.notify_text_size
    color "#fff"
    outlines [(2,"#A51F63",0,0)]
    bold True
style inventory_button:
    idle_background "#ffe8f1"
    hover_background "#ffc2da"
    xpadding 12
style inventory_button_text:
    idle_color "#f15ea9"
    hover_color "#ba4982"

style sort_button is inventory_button
style sort_button_text:
    idle_color "#f15ea9"

##############################################################################
## Inventory Grid

# change your icon size here
define itemslot_xysize = (52,52)

# default grid shows 50 items
# you can change the number of rows and columns here
define invgrid_x = 10
define invgrid_y = 5

screen invgrid(collection, page, first, last, selling=False):

    frame:
        style "invgrid_frame"
        label _("Items") style "description_label" yanchor 18

        # display the item's name when hovering
        $ tooltip = GetTooltip()
        if tooltip:
            label "[tooltip!t]" pos (40,20) yalign .96

        grid invgrid_x invgrid_y:
            align (.5,.5)
            # item buttons
            for item in collection[first:last]:
                if selected_item is not None:
                    $ thisitem = InvItem(*set_item(selected_item))

                button xysize itemslot_xysize:
                    style "itemslot_button"
                    add set_item(item)[1] #shows item image
                    tooltip set_item(item)[0] #shows item name

                    if selected_item==item:
                        if selling:
                            action ShowTransient("buying", whichitem=thisitem, howmuch=thisitem.value)
                        else:
                            action NullAction()
                    else:
                        action SetVariable("selected_item", item)

            #fill in the rest of the grid with blank squares
            for i in range(len(collection[first:last]), invgrid_x*invgrid_y):
                frame:
                    style "slot"

        text _("Page [page]") color gui.idle_color align (.96,.96)

style invgrid_frame:
    xysize (658,440)
    align (1.0,.4)
    xoffset -80
style slot:
    background "empty_item"
    xysize itemslot_xysize
    xalign .5
style itemslot_button:
    background "[prefix_]item"
    padding (2,2)
    margin (0,0)
    size_group "inv"
    focus_mask True

style item_text:
    color "#FFF"
    outlines [(3,"#c36c96",0,0)]
    hover_outlines [(3,"#D5207A",0,0)]
style item_button_text:
    idle_color "#333"
style item_button:
    xsize 540
    ysize 52
    idle_background "#FFF"
    hover_background "#FFAFCF"

screen reward(itemdrop, get=True):
    zorder 100

    vbox at reward_appear:
        align (.5,.28)
        frame:
            add itemdrop at zoomx(2)
        if get:
            text "GET!" xalign .5 size 36

transform reward_appear:
    on show:
        alpha 0 yanchor -20
        easein_circ .5 alpha 1.0 yanchor 0
    on hide:
        linear .2 alpha 0.0 yanchor 10

transform zoomx(x):
    zoom x
    nearest True

##############################################################################
## styles used for multiple screens

style special_label_text:
    size gui.special_label_text_size
    bold True
    outlines [(3,"#ffd5e7",3,3),(2,"#fff",0,0)]
style special_small_label_text:
    bold True
    outlines [(3,"#ffd5e7",2,2),(2,"#fff",0,0)]
style special_small_frame:
    background None
    xfill True

style offset_return_button:
    idle_background Frame("gui/button/choice_idle_background.png",100,5)
    hover_background Frame("gui/button/choice_hover_background.png",100,5)
    padding (100,5)
    xsize 340
    xoffset -80
style offset_return_button_text is choice_button_text:
    xalign 0

style go_button:
    idle_background "#ffe8f1"
    hover_background "#ffb4cd"
    insensitive_background "#ffe8f1"
    xysize (500, 100)
    align (.76,.9)
style go_button_text:
    size gui.special_label_text_size
    bold True
    xalign .5
    idle_color "#fff"
    hover_color "#fffba1"
    idle_outlines [(3,"#cb4388",1,1)]
    hover_outlines [(3,"#b41e6a",1,1)]

style making_frame:
    xysize (500, 400)
    align (.5,.5)
    padding (30,30)
style making_button is go_button:
    xysize (400, 100)
    align (.5,.5)
style making_button_text is go_button_text


## move this to gui.rpy if you want
init -2:
    define gui.special_label_text_size = 32
##

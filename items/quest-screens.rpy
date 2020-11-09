init offset = -1

################################################################################
## QUESTS

screen quests(page=0):

    #selects the first quest in the list
    if len(active_quests) > 0 and page==0:
        default quest = QuestItem(*set_quest(active_quests[0]))
    elif page==1:
        default quest = QuestItem(*set_quest(completed_quests[0]))
    else:
        default quest = None

    frame:
        style "quest_outer_frame"
        has vbox
        style_prefix "quest"
        label _("Quests") style "special_label"

        null height 20

        hbox:
        ##QUEST SIDEBAR
            vbox:
                hbox xysize (380,40):
                    # navigate quest lists
                    textbutton _("Active") xsize 190 action Jump("activequest") selected page==0
                    textbutton _("Complete") xsize 190 action Jump("completedquest") selected page==1 sensitive len(completed_quests) > 0

                frame xysize 400, 450:
                    # quest list
                    vpgrid style_prefix "quest":
                        cols 1 mousewheel True draggable True scrollbars "vertical"
                        pagekeys True
                        yfill True

                        # make an empty button if there are no quests in the list
                        if quest is None:
                            button

                        # active quest buttons
                        if page==0:
                            for i in active_quests:
                                $ thisquest = QuestItem(*set_quest(i))
                                button:
                                    action SetScreenVariable("quest", thisquest)
                                    selected quest.id==thisquest.id
                                    selected_foreground "quest_selected" # marker for the currently selected quest
                                    if thisquest.has_items():
                                        foreground "quest_hasitems" # marker for if you can complete it

                                    text thisquest.name xoffset 24
                        # completed quest buttons
                        else:
                            for i in completed_quests:
                                $ thisquest = QuestItem(*set_quest(i))
                                button:
                                    action SetScreenVariable("quest", thisquest)
                                    selected quest.id==thisquest.id
                                    selected_foreground "quest_selected"
                                    text thisquest.name xoffset 24
                                    # all the same except without the hasitems marker

        ##INFO PAGE
            frame:
                style "quest_content_frame"

                if quest is None:
                    if len(completed_quests) > 0:
                        text _("All quests complete!") yalign .1
                else:
                    use questinfo(quest, page)

    use gold_count()

    # you can change the style at the bottom of item-screens.rpy
    textbutton _("Return") yalign .98 action Jump("test_menu") style "offset_return_button"

##copy of craft styles
style quest_outer_frame:
    align (.5,.5)
    padding (40,20)
style quest_detail_frame:
    background None
    ysize 150
    xpadding 18
style quest_content_frame:
    xsize 700
    ysize 560
    ymargin 10
    padding (30,24)
##

## copy of recipe styles
style quest_button:
    xfill True
    ysize 48
    padding (0,0)
    idle_background "#fff"
    hover_background "#FFAFCF"
    selected_idle_background "#FFE8F1"
    selected_hover_background "#FFAFCF"
style quest_text:
    xoffset 48
    yalign .5
style quest_label_text:
    bold True
    size 36
style quest_small_label_text:
    size gui.notify_text_size
##
style quest_button_text:
    bold True
    xalign .5

style questitem_button is itemslot_button
style questitem_text:
    yalign .5

screen questinfo(quest, page):

    # show a little stamp for completed quests
    if page==1:
        add "completedquest" align (.9,.9)

    vbox:
        spacing 8
        # quest name and character icon
        frame:
            style_group "special_small"
            has hbox
            add quest.icon
            null width 10
            label quest.name yalign .5

        # flavor text
        frame:
            xfill True
            has vbox
            label _("Customer Note:") style "quest_small_label"
            frame:
                style_prefix "quest_detail"
                if page==0:
                    text quest.info style "making_text"
                else:
                    text quest.info2 style "making_text"

                text "- [quest.client!t]" align (.9,.9)

        # quest details
        hbox:
            xfill True
            vbox:
                if page==0:
                    label _("Requirement:") style "craft_small_label"
                else:
                    label _("Gave:") style "craft_small_label"
                hbox:
                    xalign .5
                    style_prefix "questitem"
                    spacing 5

                    $ tooltip = GetTooltip()
                    $ whichitem = InvItem(*set_item(quest.item))

                    button:
                        add whichitem.image
                        tooltip inv.count(whichitem.id)
                        action NullAction()
                        sensitive page==0
                        activate_sound None

                    if tooltip or tooltip==0:
                        text _("In bag: [tooltip]")
                    else:
                        text whichitem.name
                        text " x [quest.count]"

            if page==0:
                vbox:
                    xalign 1.0
                    xsize 180
                    label _("Reward:") style "craft_small_label"
                    hbox:
                        ysize 52 #match item slot
                        text "[quest.reward] "
                        text _("Gold")

    # for active quests
    if page==0:
        textbutton _("Turn In"):
            style "go_button"
            sensitive quest.has_items()
            action [ Function(quest.turn_in),
            Show("completedtask", message=_("Quest Complete!")),
            Jump("completedquest") ]

################################################################################
## Quest complete notif

screen completedtask(message):
    zorder 99
    # on "show" action Play("sound", audio.completedtask) ##add a cute sound!

    frame:
        ysize 20 yalign .5
        background Solid("#FFAFCF") #change line color here
        at lineappear
    hbox:
        align (.5,.5)
        add Text(message, slow=True, slow_cps=30, size=50, color="#fff", outlines=[(6,"#fff",0,0),(3, "#D5207A",0,0)])
        # change text properties here^

    # hide screen after a second
    timer 1.2 action Hide("completedtask", transition=Dissolve(.5))

transform lineappear:
    yzoom 0
    easein .25 yzoom 1.4
    easeout .15 yzoom 1.0
    pause 1.2
    easeout .3 yzoom 0

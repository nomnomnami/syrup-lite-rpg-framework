##############################################################################
# Quest class

init -2 python:
    class QuestItem(store.object):
        def __init__(self, name, id, client, icon, info, info2, item, count, reward=0): #list new properties up here, too!
            self.name = name #quest name
            self.id = id #string to be used as a codename
        #!! IMPORTANT !! don't change the order of anything above this line!
            self.client = client #quest-giver
            self.icon = icon #quest-giver face
            self.info = info #initial description
            self.info2 = info2 #completed description
            self.item = item #required item
            self.count = count #required amount
            ## INSERT REQUIRED PROPERTIES HERE ##
            self.reward = InvItem(*set_item(item)).value*count #earn money for completing it
            ## INSERT OPTIONAL PROPERTIES HERE ##

        ## QUEST FUNCTIONS

        # exchange quest item for gold, move quest from active list to completed
        def turn_in(self):
            global gold

            amount = self.count
            while amount>0:
                inv.remove(self.item)
                amount -= 1

            gold += self.reward

            active_quests.remove(self.id)
            completed_quests.insert(0, self.id)

        # checks if you have the required items to complete the quest
        def has_items(self):
            if inv.count(self.item) >= self.count:
                return True
            return False

##############################################################################
# more functions! (not part of QuestItem)

    # turn the quest tuple into the quest object
    def set_quest(self):

        for i in all_quests:
            if self==i[1]:
                return i

    # checks whether quest has been added/fulfilled before or not
    def new_quest(self):
        if self not in completed_quests:
            if self in active_quests:
                return False
            else:
                return True
        return False

    #add only when it's new
    def add_new_quest(self):
        if new_quest(self):
            new_quests.append(self)

##############################################################################
# QUEST DEFINITIONS

define q_sugar1 = (_("Cup of Sugar?"), "sugar1", _("Genoise"), "icon genoise",
    _("Such a lovely store... perhaps it might have been best to ask directly, but may I borrow a cup of sugar?"),
    _("Thank you for taking time out of your day to help a neighbor. The jam I made with this tasted wonderful!"),
    "item_sugar", 1 )

define q_sucker3 = (_("I'm a huge fan!"), "sucker3", _("Syrup's #1 Fan"), "icon syrupfan",
    _("I wanna be a Candy Alchemist just like you! So I thought I could start by eating the same candy as you do! Please make me some!!"),
    _("I... FEEL... LEGENDARY!! Now that I've practiced looking as cool as Syrup, I'm gonna have to start learning alchemy for real..."),
    "item_sucker", 3 )

##############################################################################
# QUEST LIST

# (works the same as itemlist)
define all_quests = [
    q_sugar1,
    q_sucker3
    ]

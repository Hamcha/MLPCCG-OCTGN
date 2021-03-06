def chkTwoSided():
   mute()
   #if not table.isTwoSided(): confirm("This game is designed to be played on a two-sided table. Please start a new game and make sure the Use-Two-Sided Table checkbox is checked")

def loadPlayerGlobalVars(args):
    try:
        me = args.player
    except IndexError:
        return

    me.setGlobalVariable("toggleAutoAT", "True")

def chkMultiplayer(args):
    mute()
    if (len(players) == 3 or len(players) == 4) and getGlobalVariable("VillainChallengeActive") == "False":
        #Prevent red errors from showing up if item is not found in the lists below
        try:
            card = args.cards[0]
            toName = args.toGroups[0].name
            fromName = args.fromGroups[0].name
        except IndexError:
            return

        if args.player._id == 2:
            if card.controller == me and card.owner == me:
                if toName != 'Table': #Any group not a Table, reset card to normal
                    card.orientation = Rot0
                elif fromName != 'Table': #If card leaves its group that is not Table, set the rot to player pos
                    card.orientation = Rot90
        elif args.player._id == 3:
            if card.controller == me and card.owner == me:
                if toName != 'Table':
                    card.orientation = Rot0
                elif fromName != 'Table':
                    card.orientation = Rot180
        elif args.player._id == 4:
            if card.controller == me and card.owner == me:
                if toName != 'Table':
                    card.orientation = Rot0
                elif fromName != 'Table':
                    card.orientation = Rot270

def autoAT(args):
    if me.getGlobalVariable("toggleAutoAT") == "True":
        #Prevent red errors from showing up if item is not found in the lists below
        try:
            toName = args.toGroups[0].name
            fromName = args.fromGroups[0].name
            card = args.cards[0]
        except IndexError:
            return

        type = card.properties["Type"]
        cardCost = card.properties["Cost"]
        cardReqPower = card.properties["PlayRequiredPower"]
        cardReqElement = card.properties["PlayRequiredElement"]
        cardSecondaryReqElement = card.properties["SecondaryPlayRequiredElement"]
        cardTriReqElement = card.properties["TertiaryPlayRequiredElement"]
        cardPower = 0
        priColorReqFailed = False
        secColorReqFailed = False
        triColorReqFailed = False
        playerCounters = me.counters['Actions'].value

        #GUID for Action and Colour Counters
        Action = ("Action", "ec99fdcb-ffea-4658-8e8f-5dc06e93f6fd")
        LoyaltyCounter = ("Loyalty", "a875a876-5ce3-4879-9590-09fc5835b5f3")
        HonestyCounter = ("Honesty", "b5ba06aa-b52f-4b17-b2e1-92302c38c5d7")
        LaughterCounter = ("Laughter", "6b46c706-08e9-44ed-8d0f-c2e478f68cd1")
        MagicCounter = ("Magic", "d970ca6c-0a3d-4def-b0e1-b1e385902a34")
        GenerosityCounter = ("Generosity", "10d7e739-bed0-4cab-93dd-24215bb13948")
        KindnessCounter = ("Kindness", "f04f63b2-52e8-439f-86a2-bff887fab0cd")

        Loyalty = 0
        Kindness = 0
        Honesty = 0
        Laughter = 0
        Magic = 0
        Generosity = 0

        if type == 'Troublemaker': #setting cost for TMs
            intCardCost = 1
        elif cardCost == '': #For Manes, do not continue with this function
            return
        else:
            intCardCost = int(card.properties["Cost"])

        if card.properties["Element"] != '': #Check if card is a friend
            cardPower = int(card.properties["Power"])


        if toName == 'Table' and fromName == 'Hand':
            if card.controller == me and card.owner == me:

                if cardReqElement != '':
                    #Capturing all face up friend cards on table for comparison
                    allCards = (card for card in table if card.isFaceUp == True and (card.properties["Type"] == 'Friend' or card.properties["Type"] == 'Mane Character' or card.properties["Type"] == 'Mane Character Boosted'))
                    for cards in allCards:
                        elementPower =  int(cards.properties["Power"]) + cards.markers[Action]

                        #Capture all colours for single, multicolored or tri-colored friend cards and add their powers
                        if cards.properties["Element"] != 'Multicolor':
                            if cards.properties["Element"] == 'Loyalty' or cards.markers[LoyaltyCounter] > 0:
                                Loyalty += elementPower
                            if cards.properties["Element"] == 'Kindness' or cards.markers[KindnessCounter] > 0:
                                Kindness += elementPower
                            if cards.properties["Element"] == 'Honesty' or cards.markers[HonestyCounter] > 0:
                                Honesty += elementPower
                            if cards.properties["Element"] == 'Laughter' or cards.markers[LaughterCounter] > 0:
                                Laughter += elementPower
                            if cards.properties["Element"] == 'Magic' or cards.markers[MagicCounter] > 0:
                                Magic += elementPower
                            if cards.properties["Element"] == 'Generosity' or cards.markers[GenerosityCounter] > 0:
                                Generosity += elementPower
                        elif cards.properties["TriElement"] == '':
                            if cards.properties["MultiPrimaryElement"] == 'Loyalty' or cards.markers[LoyaltyCounter] > 0:
                                Loyalty += elementPower
                            if cards.properties["MultiPrimaryElement"] == 'Kindness' or cards.markers[KindnessCounter] > 0:
                                Kindness += elementPower
                            if cards.properties["MultiPrimaryElement"] == 'Honesty' or cards.markers[HonestyCounter] > 0:
                                Honesty += elementPower
                            if cards.properties["MultiPrimaryElement"] == 'Laughter' or cards.markers[LaughterCounter] > 0:
                                Laughter += elementPower
                            if cards.properties["MultiPrimaryElement"] == 'Magic' or cards.markers[MagicCounter] > 0:
                                Magic += elementPower
                            if cards.properties["MultiPrimaryElement"] == 'Generosity' or cards.markers[GenerosityCounter] > 0:
                                Generosity += elementPower

                            if cards.properties["MultiSecondaryElement"] == 'Loyalty':
                                Loyalty += elementPower
                            if cards.properties["MultiSecondaryElement"] == 'Kindness':
                                Kindness += elementPower
                            if cards.properties["MultiSecondaryElement"] == 'Honesty':
                                Honesty += elementPower
                            if cards.properties["MultiSecondaryElement"] == 'Laughter':
                                Laughter += elementPower
                            if cards.properties["MultiSecondaryElement"] == 'Magic':
                                Magic += elementPower
                            if cards.properties["MultiSecondaryElement"] == 'Generosity':
                                Generosity += elementPower
                        else:
                            if cards.properties["TriPrimaryElement"] == 'Loyalty' or cards.markers[LoyaltyCounter] > 0:
                                Loyalty += elementPower
                            if cards.properties["TriPrimaryElement"] == 'Kindness' or cards.markers[KindnessCounter] > 0:
                                Kindness += elementPower
                            if cards.properties["TriPrimaryElement"] == 'Honesty' or cards.markers[HonestyCounter] > 0:
                                Honesty += elementPower
                            if cards.properties["TriPrimaryElement"] == 'Laughter' or cards.markers[LaughterCounter] > 0:
                                Laughter += elementPower
                            if cards.properties["TriPrimaryElement"] == 'Magic' or cards.markers[MagicCounter] > 0:
                                Magic += elementPower
                            if cards.properties["TriPrimaryElement"] == 'Generosity' or cards.markers[GenerosityCounter] > 0:
                                Generosity += elementPower

                            if cards.properties["TriSecondaryElement"] == 'Loyalty':
                                Loyalty += elementPower
                            if cards.properties["TriSecondaryElement"] == 'Kindness':
                                Kindness += elementPower
                            if cards.properties["TriSecondaryElement"] == 'Honesty':
                                Honesty += elementPower
                            if cards.properties["TriSecondaryElement"] == 'Laughter':
                                Laughter += elementPower
                            if cards.properties["TriSecondaryElement"] == 'Magic':
                                Magic += elementPower
                            if cards.properties["TriSecondaryElement"] == 'Generosity':
                                Generosity += elementPower

                            if cards.properties["TriElement"] == 'Loyalty':
                                Loyalty += elementPower
                            if cards.properties["TriElement"] == 'Kindness':
                                Kindness += elementPower
                            if cards.properties["TriElement"] == 'Honesty':
                                Honesty += elementPower
                            if cards.properties["TriElement"] == 'Laughter':
                                Laughter += elementPower
                            if cards.properties["TriElement"] == 'Magic':
                                Magic += elementPower
                            if cards.properties["TriElement"] == 'Generosity':
                                Generosity += elementPower

                    #Comparing card to see if it meet color req
                    intCardReqPower = int(card.properties["PlayRequiredPower"])

                    #For primary color req
                    if cardReqElement == 'Loyalty':
                        Loyalty -= cardPower #Remove the newly placed card on Table from the calculation
                        if Loyalty < intCardReqPower:
                            priColorReqFailed = True
                    elif cardReqElement == 'Kindness':
                        Kindness -= cardPower
                        if Kindness < intCardReqPower:
                            priColorReqFailed = True
                    elif cardReqElement == 'Honesty':
                        Honesty -= cardPower
                        if Honesty < intCardReqPower:
                            priColorReqFailed = True
                    elif cardReqElement == 'Laughter':
                        Laughter -= cardPower
                        if Laughter < intCardReqPower:
                            priColorReqFailed = True
                    elif cardReqElement == 'Magic':
                        Magic -= cardPower
                        if Magic < intCardReqPower:
                            priColorReqFailed = True
                    elif cardReqElement == 'Generosity':
                        Generosity -= cardPower
                        if Generosity < intCardReqPower:
                            priColorReqFailed = True

                    #For secondary color req
                    if cardSecondaryReqElement != '':
                        if cardSecondaryReqElement == 'Loyalty':
                            Loyalty -= cardPower
                            if Loyalty < intCardReqPower:
                                secColorReqFailed = True
                        elif cardSecondaryReqElement == 'Kindness':
                            Kindness -= cardPower
                            if Kindness < intCardReqPower:
                                secColorReqFailed = True
                        elif cardSecondaryReqElement == 'Honesty':
                            Honesty -= cardPower
                            if Honesty < intCardReqPower:
                                secColorReqFailed = True
                        elif cardSecondaryReqElement == 'Laughter':
                            Laughter -= cardPower
                            if Laughter < intCardReqPower:
                                secColorReqFailed = True
                        elif cardSecondaryReqElement == 'Magic':
                            Magic -= cardPower
                            if Magic < intCardReqPower:
                                secColorReqFailed = True
                        elif cardSecondaryReqElement == 'Generosity':
                            Generosity -= cardPower
                            if Generosity < intCardReqPower:
                                secColorReqFailed = True

                    #For tri color req
                    if cardTriReqElement != '':
                        if cardTriReqElement == 'Loyalty':
                            Loyalty -= cardPower
                            if Loyalty < intCardReqPower:
                                triColorReqFailed = True
                        elif cardTriReqElement == 'Kindness':
                            Kindness -= cardPower
                            if Kindness < intCardReqPower:
                                triColorReqFailed = True
                        elif cardTriReqElement == 'Honesty':
                            Honesty -= cardPower
                            if Honesty < intCardReqPower:
                                triColorReqFailed = True
                        elif cardTriReqElement == 'Laughter':
                            Laughter -= cardPower
                            if Laughter < intCardReqPower:
                                triColorReqFailed = True
                        elif cardTriReqElement == 'Magic':
                            Magic -= cardPower
                            if Magic < intCardReqPower:
                                triColorReqFailed = True
                        elif cardTriReqElement == 'Generosity':
                            Generosity -= cardPower
                            if Generosity < intCardReqPower:
                                triColorReqFailed = True

                    #notify("Honesty: {}, Loyalty: {}, Generosity: {}, Magic: {}".format(Honesty, Loyalty, Generosity, Magic))
                    #notify("PriReqFailed: {}, SecReqFailed: {} triColorReqFailed: {}".format(priColorReqFailed, secColorReqFailed, triColorReqFailed))
                    if priColorReqFailed == True or secColorReqFailed == True or triColorReqFailed == True:
                        mute()
                        card.moveTo(me.hand)
                        choice = confirm("You do not have the Color Requirement to play {}. Do you want to continue?".format(card.name))
                        if choice == True:
                            if me.isInverted:
                                card.moveToTable(-28, -120)
                            else:
                                card.moveToTable(-33, 30)
                        else:
                            return

                checkPayable = playerCounters - intCardCost

                if checkPayable < 0:
                    mute()
                    card.moveTo(me.hand)
                    choice2 = confirm("You do not have enough Action Token(s) to play {}. Do you want to continue?".format(card.name))
                    if choice2 == True:
                        if me.isInverted:
                            card.moveToTable(-28, -120)
                        else:
                            card.moveToTable(-33, 30)
                else:
                    me.counters['Actions'].value = me.counters['Actions'].value - intCardCost

def autoRotateDilemma(args):
    mute()
    try:
        toName = args.toGroups[0].name
        fromName = args.fromGroups[0].name
        card = args.cards[0]
    except IndexError:
        return

    traits = card.properties["Traits"]
    cardID = card._id
    if getGlobalVariable("PermExhausted") != "Start": #Get a list of cards that is perm exhausted
            permExhaustedList = eval(getGlobalVariable("PermExhausted"))
    else:
        permExhaustedList = []

    if (len(players) == 3 or len(players) == 4) and getGlobalVariable("VillainChallengeActive") == "False":
        if args.player._id == 1:
            if card.controller == me and card.owner == me and traits == "Dilemma":
                if toName != 'Table': #Any group not a Table, reset card to normal
                    card.orientation = Rot0
                elif fromName != 'Table': #If card leaves its group that is not Table, set the rot to player pos
                    card.orientation = Rot90
                    card.filter = "#44ff0000"
                    permExhaustedList.append(cardID) #Adds to perm exhausted list
                    setGlobalVariable("PermExhausted", str(permExhaustedList))
        elif args.player._id == 4:
            if card.controller == me and card.owner == me and traits == "Dilemma":
                if toName != 'Table':
                    card.orientation = Rot0
                elif fromName != 'Table':
                    card.orientation = Rot180
                    card.filter = "#44ff0000"
                    permExhaustedList.append(cardID) #Adds to perm exhausted list
                    setGlobalVariable("PermExhausted", str(permExhaustedList))
        elif args.player._id == 3:
            if card.controller == me and card.owner == me and traits == "Dilemma":
                if toName != 'Table':
                    card.orientation = Rot0
                elif fromName != 'Table':
                    card.orientation = Rot270
                    card.filter = "#44ff0000"
                    permExhaustedList.append(cardID) #Adds to perm exhausted list
                    setGlobalVariable("PermExhausted", str(permExhaustedList))
    else:
        if card.controller == me and card.owner == me and traits == "Dilemma":
            if toName != 'Table': #Any group not a Table, reset card to normal
                card.orientation = Rot0
            elif fromName != 'Table': #If card leaves its group that is not Table, set the rot to player pos
                card.orientation = Rot90
                card.filter = "#44ff0000"
                permExhaustedList.append(cardID) #Adds to perm exhausted list
                setGlobalVariable("PermExhausted", str(permExhaustedList))
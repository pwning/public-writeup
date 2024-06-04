def shuffleDeck(deck: list):
    i: int = len(deck)-1
    temp: list = deck[i]
    j: int = 0
    while i > 0:
        j = rand(i)
        temp = deck[i]
        deck[i] = deck[j]
        deck[j] = temp
        i -= 1

def initializeDeck() -> list:
    suits: list = [0, 1, 2, 3]
    ranks: list = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    deck: list = []
    suitIndex: int = 0
    rankIndex: int = 0
    while (suitIndex<4):
        rankIndex = 0
        while (rankIndex<13):
            append(deck, [ranks[rankIndex], suits[suitIndex]])
            rankIndex += 1

        suitIndex += 1

    shuffleDeck(deck)
    return deck

def dealCards(deck: list) -> list:
    hands: list = []
    index: int = 0
    count: int = 0
    playerHand: list = []
    while (count<2):
        playerHand = []
        cardCount: int = 0
        while (cardCount<2):
            append(playerHand, deck[index])
            index = (index+1)
            cardCount = (cardCount+1)

        append(hands, playerHand)
        count = (count+1)

    return hands

def replaceCards(playerHand: list, deck: list, cardsToReplace: list):
    replacementIndex: int = len(deck)-1
    i: int = 0
    while i < len(cardsToReplace):
        if cardsToReplace[i]:
            playerHand[i] = deck[replacementIndex]
            replacementIndex = (replacementIndex-1)
        i += 1

def scoreHand(hand: list) -> int:
    score: int = 0
    i: int = 0
    temp: list = []
    cardValue: str = ''
    while i < len(hand):
        temp = hand[i]
        cardValue = temp[0]
        if cardValue=='A':
            if score+11 > 21:
                score += 1
            else:
                score += 11
        elif (cardValue=='K' or cardValue=='Q') or cardValue=='J':
            score += 10
        else:
            score += int(cardValue)

        i += 1

    return score


def determineWinner(playerHand: list, dealerHand: list) -> int:
    playerScore: int = scoreHand(playerHand)
    dealerScore: int = scoreHand(dealerHand)
    if playerScore > dealerScore:
        return 1
    elif dealerScore > playerScore:
        return 2
    else:
        return 0


def Draw_result() -> bool:
    print('\nDraw\n')


def Player_result() -> bool:
    print('\nPlayer Win\n')


def Dealer_result() -> bool:
    print('\nDealer Win\n')


def get_user_input() -> list:
    replace_input: list = []
    i: int = 0
    while i < 2:
        choice: bytes = input('Swap Card ['+str(i)+'] [y/n]:')
        if choice == b'y':
            append(replace_input, 1)
        else:
            append(replace_input, 0)
        i += 1

    return replace_input


def ShowCard(card: list) -> bool:
    i: int = 0
    c: list = None
    level: str = None
    suits: list = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
    while i < len(card):
        c = card[i]
        print('\t'+'['+str(i)+'] '+c[0]+' of '+suits[c[1]]+'\n')
        i += 1


def main() -> int:
    while 1:
        func_list: list = [Draw_result, Player_result, Dealer_result]
        beh: list = []
        beh_func: pointer = None
        pwrite(0, func_list)
        deck: list = initializeDeck()
        hands: list = dealCards(deck)
        playerHand: list = hands[0]
        dealerHand: list = hands[1]
        print('[Dealer]\n')
        ShowCard(dealerHand)
        print('\n[Player]\n')
        ShowCard(playerHand)
        print('\n')
        cardsToReplace: list = get_user_input()
        replaceCards(playerHand, deck, cardsToReplace)
        print('\n[Dealer]\n')
        ShowCard(dealerHand)
        print('\n[Player - Card changed]\n')
        ShowCard(playerHand)
        winner: int = determineWinner(playerHand, dealerHand)
        beh = pread(0)
        beh_func = beh[winner]
        beh_func()
        sleep(3.0)
        pwrite(0, func_list)

main()

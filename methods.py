from replit import clear

# Game variables

bankroll = 0
bet = 0
deck = []
drawn_cards = []
player_cards = []
dealer_cards = []
player_count = 0
dealer_count = 0
dealers_turn = False
player_bust = False
dealer_bust = False

# Set up dealing deck

nums = range(1,14)
colors = ["hearts", "clubs", "spades", "diamonds"]

for color in colors:
  # _ = number of decks
  for _ in range(1):
    for num in nums:
      if num == 1:
        deck.append([color,"Ace", 11])
      elif num == 11:
        deck.append([color,"Jack", 10])
      elif num == 12:
        deck.append([color,"Queen", 10])
      elif num == 13:
        deck.append([color,"King", 10])
      else:
        deck.append([color,num, num])

# ----------

# Pay bankroll

def setBankroll():

  nums = "0123456789"

  bankroll_not_valid = True

  while bankroll_not_valid:

    bankroll_not_valid = False

    print("")
    print("Bankroll:")
    set_bankroll = input()

    if set_bankroll == "":
      bankroll_not_valid = True
      print("Make a deposit.")
    else:
      for i in set_bankroll:
        if i not in nums:
          bankroll_not_valid = True
          print("")
          print("The deposit must be an integer. Try again.")

  return int(set_bankroll)

# ----------

# Make bet

def makeBet(bankroll):

  nums = "0123456789"

  bet_not_valid = True

  while bet_not_valid:

    bet_not_valid = False

    print("Bet:")
    set_bet = input()

    if set_bet == "":
      bet_not_valid = True
      print("Make a bet!")
      print("")
    else:
      for i in set_bet:
        bet_is_only_nums = True
        if i not in nums:
          bet_not_valid = True
          print("")
          print("The bet must be an integer. Try again.")
          print("")
          bet_is_only_nums = False
          break
      if bet_is_only_nums and (int(set_bet) > bankroll):
        bet_not_valid = True
        print("")
        print("Not enough bankroll. Try again.")
        print("")

  return int(set_bet)

# ----------

# - DEAL FIRST CARDS -

def firstDeal():
  
  # Player card 1

  player_card_1 = deck.pop(-1)
  player_cards.append(player_card_1)
  drawn_cards.append(player_card_1)

  # Dealer card 1

  dealer_card_1 = deck.pop(-1)
  dealer_cards.append(dealer_card_1) 
  drawn_cards.append(dealer_card_1)

  # Player card 2

  player_card_2 = deck.pop(-1)
  player_cards.append(player_card_2)
  drawn_cards.append(player_card_2)

  # Dealer card 2

  dealer_card_2 = deck.pop(-1)
  dealer_cards.append(dealer_card_2)
  drawn_cards.append(dealer_card_2)

# -----------

# Count board

def countBoard(player_count, dealer_count):

  for card in player_cards:
      player_count += card[2]

  for card in dealer_cards:
      dealer_count += card[2]

  return player_count, dealer_count

# ----------

# Header

def header():

  print("")
  print("Bet: " + str(bet))
  print("")
  print("----------")
  print("")

  if dealers_turn:
    print("Dealer: " + (', '.join(f"{card[1]} of {card[0]}" for card in dealer_cards)))
  else:
    print("Dealer: {} of {}, X".format(
      dealer_cards[0][1],                                         
      dealer_cards[0][0]))
  
  print("")
  print("You: " + (', '.join(f"{card[1]} of {card[0]}" for card in player_cards)))
  print("")
  print("----------")

# ----------

# Player loop

def playerLoop(player_cards, player_count):

  player_bust = False
  player_loop = True

  while player_loop:

    clear()

    header()

    # Show bust probability

    print("")
    print("Bust risk: " + str(calculateBustProbability(player_cards, player_count)) + " %")
    
    # CHOICE 1

    print("")
    print("[enter] - Draw card")
    print("[0]     - Stay")
    print("")

    choices_1 = ["", "0"]

    choice_1_clear = False

    while not choice_1_clear:

      print("Make a choice:")
      choice_1 = input()

      if choice_1 not in choices_1:
        print("")
        print("Something went wrong. Try again.")
        print("")
      else:
        choice_1_clear = True

    if choice_1 == "":

      clear()

      header()

      player_cards, player_count = drawCard(player_cards, player_count)

      if player_count > 21:

        print("You bust...")
        print("")

        player_bust = True
        player_loop = False
        
    else:
      player_loop = False

  return player_cards, player_count, player_bust
      
# ----------

# Dealer loop

def dealerLoop(dealer_cards, dealer_count):

  dealer_bust = False

  while dealer_count < 17:

    clear()

    header()

    print("")
    print("Draw new dealer card:")
    input()

    dealer_cards, dealer_count = drawCard(dealer_cards, dealer_count)

  if dealer_count > 21:

    dealer_bust = True
    print("Dealer busts!")
    input()

  return dealer_cards, dealer_count, dealer_bust

# ----------

# Draw card

def drawCard(cards, count):
  
  # Draw new card

  draw_card = deck.pop(-1)
  cards.append(draw_card)
  drawn_cards.append(draw_card)

  # Add card value to count

  count += draw_card[2]

  # If count over 21, check if any aces

  if count > 21:
    for i, card in enumerate(cards):
      if card[1] == "Ace" and card[2] == 11:
        cards[i][2] = 1
        count -= 10

  if dealers_turn:

    print("Dealer got: {} of {}".format(draw_card[1], draw_card[0]))
    input()

  else:

    print("")
    print("You got: {} of {}".format(draw_card[1], draw_card[0]))
    input()

  return cards, count

# ----------

# Get winner

def getWinner(bankroll):

  win_pot = bet

  # If player/dealer bust

  if player_bust:
    print("Dealer wins.")
  elif dealer_bust:
    bankroll += (bet + win_pot)
    print("You win!")
    print("")
    print("+ " + str(bet) + " + " + str(win_pot))
  else:
    
    # If player have Black Jack
    
    if (len(player_cards) == 2 and player_count == 21) and \
       (len(dealer_cards)>2 or dealer_count<21):
      
      win_pot = win_pot * 1.5
      bankroll += (bet + win_pot)
      
      print("Black Jack - nice!")
      print("")
      print("+ " + str(bet) + " + " + str(win_pot))

    # If dealer have Black Jack
      
    elif len(dealer_cards) == 2 and dealer_count == 21 and \
        (len(player_cards)>2 or player_count<21):
      
      print("Dealer wins with a Black Jack hand!")

    # If player count high
    
    elif player_count > dealer_count:
      
      bankroll += (bet + win_pot)
      
      print("You win!")
      print("")
      print("+ " + str(bet) + " + " + str(win_pot))

    # If draw
    
    elif player_count == dealer_count:
      
      bankroll += bet
      
      print("It's a draw.")
      print("")
      print("+ " + str(bet))

    # If dealer wins
    
    else:
      
      print("Dealer wins.")

  # If bankrupt

  if bankroll == 0:
    
    print("")
    print("Press [enter]:")
    input()

  return bankroll 

# ----------

# Calculate bust probability

def calculateBustProbability(hand, count):

  bust_count = 0
  hand_count = count

  # If aces on hand, lower value

  for card in hand:
    if card[2] == 11:
      hand_count -= 10

  # Count cards that would bust hand

  for card in deck:
    if card[2] == 11:
      if hand_count + 1 > 21:
        bust_count += 1
    else:
      if hand_count + card[2] > 21:
        bust_count += 1

  # Calculate probability

  bust_probability = round(bust_count / len(deck) * 100, 2)
  
  return bust_probability
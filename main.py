from replit import clear
import methods
import random

# Game start - insats

print("")
print("Simons BlackJack")

methods.bankroll = methods.setBankroll()

# ----------

# - GAME LOOP -

game_on = True

while game_on:

  # Shuffle deck

  random.shuffle(methods.deck)

  # ----------

  clear()

  print("")
  print("Bankroll: {}".format(methods.bankroll))
  print("")

  # Make bet

  methods.bet = methods.makeBet(methods.bankroll)
  methods.bankroll -= methods.bet

  # ----------

  # Continue

  clear()

  print("")
  print("Bankroll: " + str(methods.bankroll)) 
  print("")
  print("Bet: " + str(methods.bet))
  print("")
  print("Press [enter] to deal cards:")
  input()

  # ----------

  # - DEAL FIRST CARDS -

  methods.firstDeal()

  # -----------

  # - START ROUND -

  clear()

  print("")
  print("Bankroll: " + str(methods.bankroll)) 
  print("")
  print("----------")

  methods.header()

  # ----------

  # - Count board -

  methods.player_count, methods.dealer_count = methods.countBoard(methods.player_count, methods.dealer_count)

  # ----------

  # Player draw loop

  methods.player_cards, methods.player_count, methods.player_bust = methods.playerLoop(methods.player_cards, methods.player_count)

  # ----------

  if not methods.player_bust:

    # Dealer draw loop

    clear()

    methods.header()

    print("")
    print("Dealer's turn!")
    print("")
    print("Press [enter] to continue:")
    input()

    methods.dealers_turn = True

    if methods.dealer_count < 17:

      methods.dealer_cards, methods.dealer_count, methods.dealer_bust = methods.dealerLoop(methods.dealer_cards, methods.dealer_count)

    else:
    
      clear()

      methods.header()

      print("")
      print("Press [enter] to continue:")
      input()

    # Final board

    if not methods.dealer_bust and not methods.player_bust:

      clear()

      methods.header()
    
      print("")
      print("Dealer's count: " + str(methods.dealer_count))
      print("")
      print("Your count: " + str(methods.player_count))
      print("")
      print("Press [enter]:")
      input()

  # ----------

  # Get winner, end round

  methods.bankroll = methods.getWinner(methods.bankroll)

  if methods.bankroll == 0:
    clear()
    print("")
    print("Bankroll empty...")
    print("")
    print("Game over.")
    game_on = False
  else:
    print("")
    print("Press [enter] to start new round:")
    input()

  # Reset board

  for i in range(len(methods.drawn_cards)):
    if methods.drawn_cards[i][2] == 1:
      methods.drawn_cards[i][2] == 11
    methods.deck.append(methods.drawn_cards[i])

  methods.drawn_cards = []
  methods.player_cards = []
  methods.dealer_cards = []
  methods.dealers_turn = False
  methods.player_bust = False
  methods.dealer_bust = False
  methods.player_count = 0
  methods.dealer_count = 0
  
  

#♠♥♦♣
import random
import time #to make function sleep for certain seconds

#draw multiple blank line, acting as BOARD eraser so card shown will go out of console screen
def draw_blank_board():
    for x in range(20):
        print("""
    -
    """)


#the Card class, has property of value (representing point of card), and suit (club, heart, diamond, spades)
class Card:

    #when initialized, ask for value, and suit of the card, eg value:10, suit hearts, so is 10 of hearts
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit
        self.name = str(self.card_name())

    #displays the card in text format (mainly during testing purposes)
    def show_card_text(self):
        print('{0} of {1}, of Value: {2}'.format(self.name, self.suit, self.value))

    #for special cards, like Ace, Jack, Queen, King which are not traditional numbers
    #eg Ace is the highest with 14 points
    def card_name(self):
        if self.value == 14:
            return 'Ace'
        elif self.value == 11:
            return 'Jack'
        elif self.value == 12:
            return 'Queen'
        elif self.value == 13:
            return 'King'
        else:
            return self.value

    #for different suit, return different suit symbol, eg hearts ♡
    def card_suit_symbol(self):
        if self.suit == 'Hearts':
            return '♡'
        elif self.suit == 'Clubs':
            return '♧'
        elif self.suit == 'Diamonds':
            return '♢'
        elif self.suit == 'Spades':
            return '♠'

    #display the card in a more EASY to recognize way, with card symbol and card name
    def display_card(self):
        print("    -- {0} of {1} --    ".format(self.name, self.card_suit_symbol()), end = " ")


#builds a list of Card, acting as the deck
#deck has function of building deck, dealing one card from deck, and display the whole deck (used in testing purpose)
class Deck:
    # attribute to assign, so can know which type of deck later on
    deck_type = 'normal'

    #when initialized, creates a list of card, self.cards
    #builds the deck that modifieds the self.cards, by appending all 52 cards
    def __init__(self):
        self.cards = []
        self.build_deck()

    def build_deck(self):
        for suit in ['Hearts', 'Clubs', 'Diamonds', 'Spades']:
            for val in range(2, 15):
                self.cards.append(Card(val, suit))

    def deal(self):
        return self.cards.pop(random.randint(0, len(self.cards) - 1))

    def display_cards_text_in_deck(self):
        for card in self.cards:
            card.show_card_text()
        print('\n')


#inherits from the Deck class, no royal deck is a modified deck, with Queen and King removed, hence the name no_royal
class NoRoyalsDeck(Deck):
    #attribute to assign, so can know which type of deck later on, in this case no_royal deck
    deck_type = "no_royals"

    #when initlized act same as Deck Class, but has additional function self.remove_king and self.remove_queen to remove the royals from the Deck
    #has 44 cards
    def __init__(self):
        self.cards = []
        self.build_deck()

        self.remove_king()
        self.remove_queen()

    #function to remove kings from the deck self.cards
    def remove_king(self):
        for card in self.cards:
            if card.name == 'K':
                self.cards.remove(card)

    # function to remove queens from the deck self.cards
    def remove_queen(self):
        for card in self.cards:
            if card.name == 'Q':
                self.cards.remove(card)

#class to deal with player, who has Name, and uses card from certain deck card_deck
class Player:

    def __init__(self, name, card_deck):
        self.name = name
        self.total_cards_at_hand = [] #creates a total_card_at_hand list of card, so can display the card at hand of certain player
        self.card_deck = card_deck
        self.win_guess = 0

    #resets current players deck
    def refresh_No_Royals_deck(self):
        self.card_deck = NoRoyalsDeck()

    #displays card at hand
    def show_cards_in_hand(self):
        print("{0} has cards: ".format(self.name))
        for card in reversed(self.total_cards_at_hand):
            card.display_card()
        print()

    def clear_hand(self):
        self.total_cards_at_hand = []


    def update_wins_guess(self):
        self.win_guess += 1

    #returns sum of all the points of card that are currently at hand
    def return_current_points(self):
        points = 0
        for card in self.total_cards_at_hand:
            points += card.value
        return points

    #displays the points at hand
    def show_current_points(self):
        print('Player {0} has {1} points!'.format(self.name, self.return_current_points()))

    #deal one card to player, adds to total_cards_at_hand
    def deal_again(self):
        self.total_cards_at_hand.append(self.card_deck.deal())

    #compares player to another player, and returns the Player with MORE point, if tie, return -1
    def return_winner(self, player2):
        if(self.return_current_points() > player2.return_current_points()):
            return self
        elif(self.return_current_points() == player2.return_current_points()):
            return -1
        else:
            return player2

    #displays point of player 1, and player 2
    #then declare winner, or else declare TIE
    def compare_points_with_player(self, player2):
        print('Player 1 : {0} has: {1} points.'.format(self.name, self.return_current_points()))
        print('Player 2 : {0} has: {1} points.'.format(player2.name, player2.return_current_points()))
        winner = self.return_winner(player2)
        if winner!= -1:
            print('WINNER is: {0}!!!'.format(winner.name))
        else:
            print('Its a TIE!')

#class for No Royal Guessing game, name No Royal come from using No Royals deck
#guessing game, because both the player will guess which player has higher points in a certain amount of seconds
#who guesses correct is the winner, if both guess correct TIE, if none guess correct both lose
class NoRoyalGuessingGame:
    #when initialized, takes 2 players, takes match type (PvP 1, PvComp 2, CompvComp 3)
    #total_card_num is number of card to be displayed
    #and time delay how long players have for guessing
    def __init__(self, player1, player2, match_type, total_card_num, time_delay):
        self.player1 = player1
        self.player2 = player2
        self.match_type = match_type
        self.total_card_num = total_card_num
        self.time_delay = time_delay

    #starts the round
    #returns winner of current round
    def play_round(self):
        for x in range(self.total_card_num):
            self.player1.deal_again()
            self.player2.deal_again()
            print()

        if self.match_type == 1 or self.match_type == 2:
            print('YOU HAVE {0} SECONDS to look at the CARDS!'.format(self.time_delay))
            print()

            print('You will be SHOWN THE CARDS IN: ')
            #5 seconds before card show up
            time.sleep(1)
            print('5...')
            time.sleep(1)
            print('4...')
            time.sleep(1)
            print('3...')
            time.sleep(1)
            print('2...')
            time.sleep(1)
            print('1...')

        print()
        self.player1.show_cards_in_hand()
        self.player2.show_cards_in_hand()
        print()

        #if match type 1/2 hence PvP, or PvComp, Human player(s) have time time_delay seconds to see the card to assess who has higher point, then make a guess
        #if CompvComp (3) then no need for this if-statement to run

        if(self.match_type == 1 or self.match_type == 2):

            #visual only, timer
            for x in range(self.time_delay):
                print('{0}..'.format(self.time_delay - x), end= ' ')
                time.sleep(1)

            #draws blank board so no longer can look into the card
            print()
            draw_blank_board()

        #if match type os 1, PvP, player 1 and player 2 be given chance to input their guesses
        #1 being player 1 has higher point, 2 being player 2 has higher point
        if self.match_type == 1:
            #checks that the input is either 1 or 2, anything else, will throw an error
            while True:
                try:
                    player1_guess = int(input("""
Player 1, {0}, guess who has the higher point! 
Enter 1 if you think YOU, or 
Enter 2 if you think player 2, {1}: \n""".format(self.player1.name, self.player2.name)))
                    if player1_guess == 1:
                        break
                    elif player1_guess == 2:
                        break
                    print('Invalid input. Enter 1 or 2: ')
                except Exception as e:
                    print(e)

            # checks that the input is either 1 or 2, anything else, will throw an error
            while True:
                try:
                    player2_guess= int(input("""
Player 2, {0}, guess who has the higher point! 
Enter 1 if you think Player 1, {1}, or 
Enter 2 if you think YOU: \n""".format(self.player2.name, self.player1.name)))
                    if player2_guess == 1:
                        break
                    elif player2_guess == 2:
                        break
                except Exception as e:
                    print(e)

            return self.guess_winner(player1_guess, player2_guess)

        #if match is PvComp, only Player 1 (human) will be given chance to input their guesses
        elif self.match_type == 2:
            # checks that the input is either 1 or 2, anything else, will throw an error
            while True:
                try:
                    player1_guess = int(input("""
Player 1, {0}, guess who has the higher point! 
Enter 1 if you think YOU, or, 
Enter 2 if you think player 2, {1}: \n""".format(self.player1.name, self.player2.name)))
                    if player1_guess == 1:
                        break
                    elif player1_guess == 2:
                        break
                    print('Invalid input. Enter 1 or 2: ')
                except Exception as e:
                    print(e)
            #for pc guess
            pc_player2_guess = random.randint(1,2)

            return self.guess_winner(player1_guess, pc_player2_guess)

        #if Comp v Comp, pc player 1 and pc player 2 will randomly guess between 1 and 2
        elif self.match_type == 3:
            pc_player1_guess = random.randint(1, 2)
            pc_player2_guess = random.randint(1, 2)
            return self.guess_winner(pc_player1_guess, pc_player2_guess)



    #function that deal with input of Player 1 and Player 2 and their guesses
    #displays whose guess is correct
    #AND returns player whose Guess is correct, 1 if both correct, 0 if neither
    def guess_winner(self, player1_guess, player2_guess):

        if player1_guess == 1:
            player1_guess_name = 'THEMSELVES'
        else:
            player1_guess_name = self.player2.name

        if player2_guess == 1:
            player2_guess_name = self.player1.name
        else:
            player2_guess_name = 'THEMSELVES'

        #winner as in higher in point
        winner = self.player1.return_winner(self.player2)

        #though extremely low chance, checks wether there is acually a TIE in point, if TIE in point Winner = -1, so checks that Winner is not -1
        #prints the screen for declaring the one Who guessed Right or Wrong
        if(winner!=-1):
            if self.player1 == winner:
                print('♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦')
                print('The one with HIGHER Point is {0} with {1} points'.format(winner.name, winner.return_current_points()))
                print('The runner up is {0} with {1} points'.format(self.player2.name, self.player2.return_current_points()))

                print('Player 1, {0}, guessed: {1}'.format(self.player1.name, player1_guess_name))
                print('Player 2, {0}, guessed: {1}'.format(self.player2.name, player2_guess_name))
                print('♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦')

                print()

                if player1_guess == 1 and player2_guess == 1:
                    print('BOTH of YOU GUESSED Correct, so both of you GET 1 point!')
                    self.player1.update_wins_guess()
                    self.player2.update_wins_guess()
                elif player1_guess == 1 and player2_guess!=1:
                        print('Player 1, {0} GUESSED IT CORRECT. WINNER is {0}!!!'.format(self.player1.name))
                        self.player1.update_wins_guess()
                elif player2_guess ==1 and player1_guess!=1:
                        print('Player 2, {0} GUESSED IT CORRECT. WINNER is {0}!!!'.format(self.player2.name))
                        self.player2.update_wins_guess()
                else:
                    print('BOTH OF YOUR GUESS IS WRONG!')

            elif self.player2 == winner:
                print('♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦')
                print('The one with HIGHER Point is {0} with {1} points'.format(winner.name, winner.return_current_points()))
                print('The runner up is {0} with {1} points'.format(self.player1.name, self.player1.return_current_points()))

                print('Player 1, {0}, guessed: {1}'.format(self.player1.name, player1_guess_name))
                print('Player 2, {0}, guessed: {1}'.format(self.player2.name, player2_guess_name))
                print('♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦')

                print()

                if player1_guess == 2 and player2_guess == 2:
                    print('BOTH of YOU GUESSED Correct, so both of you GET 1 point!')
                    self.player1.update_wins_guess()
                    self.player2.update_wins_guess()
                elif player1_guess == 2 and player2_guess != 2:
                    print('Player 1, {0} GUESSED IT CORRECT. WINNER is {0}!!!'.format(self.player1.name))
                    self.player1.update_wins_guess()
                elif player2_guess == 2 and player1_guess != 2:
                    print('Player 2, {0} GUESSED IT CORRECT. WINNER is {0}!!!'.format(self.player2.name))
                    self.player2.update_wins_guess()
                else:
                    print('BOTH OF YOUR GUESS IS WRONG!')
        else:
            print('Player 1, {0}, has: {1} points'.format(self.player1.name, self.player1.return_current_points()))
            print('Player 2, {0}, has: {1} points'.format(self.player2.name, self.player2.return_current_points()))
            print("Miraculously, both player have same amount of points! Try again!")




#the whole game function, starts with introducing game rules

class TheGame:

    min_card_num = 6
    max_card_num = 8

    min_time_delay = 6
    max_time_delay = 11

    def __init__(self, game_choice = 1, player_1_name = '', player_2_name='', card_number=7, time_delay = 8):
        self.choice = game_choice
        self.player_1_name = player_1_name
        self.player_2_name = player_2_name

        #always use new deck
        self.player1 = Player(player_1_name, NoRoyalsDeck())
        self.player2 = Player(player_2_name, NoRoyalsDeck())

        self.card_number = card_number
        self.time_delay = time_delay
        self.rounds = 1

    def play_game(self):
        no_royal_game = NoRoyalGuessingGame(self.player1, self.player2, self.choice, self.card_number, self.time_delay)
        no_royal_game.play_round()

        print()
        print('--------------------------------------------------')
        print('Score: ')
        print('Player 1, {0}, score: {1}  ||| Player 2, {2}, score: {3}\n'.format(self.player1.name, self.player1.win_guess,
                                                                                  self.player2.name, self.player2.win_guess))
        print('--------------------------------------------------')
        self.rounds += 1

        #refreshes deck so player does not run out of
        self.player1.refresh_No_Royals_deck()
        self.player1.clear_hand()
        self.player2.refresh_No_Royals_deck()
        self.player2.clear_hand()


#function to run the_game function, and allow user to play more than 1 round!
def game_cycle():

    game1 = TheGame()
    min_card_num = game1.min_card_num
    max_card_num = game1.max_card_num
    min_time_delay = game1.min_time_delay
    max_time_delay = game1.max_time_delay

    print('Welcome to No Royal GUESSING card game, where the King and Queens are taken out of an ordinary deck, and the player WHO can GUESS Which PLAYER has MORE points WINS!')
    print()
    print('The game will go as follows: ')
    print('Two sets of cards will be displayed, one of player 1 and one of player 2')
    print('Both player will guess which PLAYER has higher point, in a couple of seconds')
    print()
    print('The one WHO GUESSES CORRECTLY is the WINNER!')

    print('Do you want to play, player vs player (1), player vs computer (2), computer vs computer (3)')
    # check wether choice is 1, 2 or 3, otherwise throw error
    while True:
        try:
            choice = int(input("Enter your choice: "))
            if choice == 1:
                break
            elif choice == 2:
                break
            elif choice == 3:
                break

            print("Invalid choice entered. Enter again.")
        except Exception as e:
            print(e)

        # random name list so Computer can randomly choose their NAME
    random_name_list = ['PC John', 'PC Max', 'PC Nancy', 'PC Mark', 'PC James', 'PC Zack', 'PC Dany', 'PC Lily',
                        'PC Julie', 'PC Dan']

    # function to take user string input for Entering name
    def try_user_input_name(player_num):
        # checks wether player_name is a string and not a number
        while True:
            try:
                player_name = input('Enter player {0} name: '.format(player_num))

                #checks if name first letter is number/not string, and checks wether whole name is a number or not
                if player_name[0].isalnum() == False:
                    raise Exception("Only alphabet at the start")
                if player_name[0].isnumeric():
                    raise Exception("No number in the beginning of the name!")
                if player_name.isnumeric():
                    raise Exception("Sorry only numbers is not allowed")

                return player_name

            except Exception as e:
                print(e)


    # if choice is 1 or 2 player(s) to enter their name(s)

    if choice == 1:
        player_1_name = try_user_input_name(1)
        player_2_name = try_user_input_name(2)

    elif choice == 2:
        player_1_name = try_user_input_name(1)
        player_2_name = random_name_list[random.randint(0, len(random_name_list) - 1)]

    elif choice == 3:
        player_1_name = random_name_list.pop(random.randint(0, len(random_name_list) - 1))
        player_2_name = random_name_list.pop(random.randint(0, len(random_name_list) - 1))

    if choice == 1 or choice == 2:
        # check wether entered num is a integer and between min_card_num and max_card_num
        while True:
            try:
                card_num = input(
                    "How many cards do you want to play? Choose from {0} to {1} cards: ".format(min_card_num,
                                                                                                max_card_num))
                if card_num.isnumeric() == False:
                    raise Exception("Enter a proper integer please!")
                else:
                    card_num = int(card_num)

                if card_num >= min_card_num and card_num <= max_card_num:
                    break
                print(
                    "\nInteger out of range. Enter an integer between {0} and {1}: ".format(min_card_num, max_card_num))
            except Exception as e:
                print(e)

        while True:
            try:
                # check wether entered num is a integer and between min_time_delay and max_time_delay
                time_delay = input(
                    "How many seconds do you want to play? Choose from {0} to {1} seconds: ".format(min_time_delay, max_time_delay))

                if time_delay.isnumeric() == False:
                    raise Exception("Enter a proper integer please!")
                else:
                    time_delay = int(time_delay)
                if time_delay >= min_time_delay and time_delay <= max_time_delay:
                    break
                print("\nInvalid integer entered. Enter an integer between {0} and {1}: ".format(min_time_delay, max_time_delay))
            except Exception as e:
                print(e)

    elif choice == 3:
        card_num = random.randint(min_card_num, max_card_num)
        time_delay = 0

    game1.choice = choice
    game1.player1 = Player(player_1_name, NoRoyalsDeck())
    game1.player2 = Player(player_2_name, NoRoyalsDeck())

    game1.card_number = card_num
    game1.time_delay = time_delay

    game1.play_game()

    while True:
        try:
            play_again = input('Do you want to play the game again? Enter y (yes) or n (n):\n').upper()
            if play_again == 'Y' or play_again == 'N':
                break
            else:
                raise Exception('Enter y or n please! :')
        except Exception as e:
            print(e)

    while play_again == 'Y':
        print('Thank you for choosing to play again!')

        print('--------------------------------------------------')
        print('Round {0} begins!'.format(game1.rounds))
        print('--------------------------------------------------')

        print('Both player will guess which PLAYER has higher point, in a couple of seconds')
        print()
        print('The one WHO GUESSES CORRECTLY is the WINNER!')

        game1.play_game()

        while True:
            try:
                play_again = input('Do you want to play the game again? Enter y (yes) or n (n):\n').upper()
                if play_again == 'Y' or play_again == 'N':
                    break
                else:
                    raise Exception('Enter y or n please! :')
            except Exception as e:
                print(e)

    print('Thanks for playing!')


game_cycle()

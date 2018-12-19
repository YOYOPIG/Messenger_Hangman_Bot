import random
from transitions import Machine

class Hangman(object):

    WORDLIST_FILENAME = "words.txt"

    def __init__(self, name):
        states = ['idle', 'game running', 'finding word', 'checking status']
        self.name = name
        self.gg=True #bool for game over
        self.machine = Machine(model=self, states=states, initial='idle')
        self.machine.add_transition(trigger='start', source='idle', dest='game running')
        self.machine.add_transition(trigger='in_word', source='game running', dest='finding word')
        self.machine.add_transition(trigger='check_status', source='finding word', dest='checking status')
        self.machine.add_transition(trigger='back_to_running', source='checking status', dest='game running')
        self.machine.add_transition(trigger='end', source='checking status', dest='idle')

    # Initialize the game state
    def game_start(self):
        if(self.state=="idle"):
            self.start()
        self.missed_guesses = ""
        self.miss_ctr = 0
        self.hit_ctr = 0
        self.target_word = ""
        self.total_chances = 6
        self.guessed_letters= ""
        self.gg = False

        # Read in the words file
        self.get_target_word("words.txt")
        self.target_length=len(self.target_word)
        print(self.target_word)

        # Print starting msg
        print("Game started.")
        string = "Want to escape? Guess the word then!\n"
        string += "The word is " + str(self.target_length) + " letters long.\nGood luck!"
        return string

    def get_target_word(self, filename):
        """
        Gets a random word from file.
        filename : the string of input file's name.
        Sets the word to guess in lowercase.
        """
        inFile = open(filename, 'r')
        line = inFile.readline()
        words = line.split()
        self.target_word = random.choice(words).lower()
        return

    # Get current guessing progress
    def get_guessed_word(self, target, guessed):
        '''
        target : string, the word the user is guessing
        guessed : list, what letters have been guessed so far
        returns: string, comprised of letters and underscores that represents
        what letters in target have been guessed so far.
        '''
        string=""
        self.hit_ctr = 0
        for key in target:
            if key in guessed:
                string+=key
                string+=" "
                self.hit_ctr+=1
            else:
                string+="_ "
        return string
        
    def input_word(self, user_input):
        # Make sure its lowercase!
        if(self.state=="game running"):
            self.in_word() #for transition
        guess = user_input.lower()
        if len(guess)>1:
            if len(guess)==self.target_length:
                if guess==self.target_word:
                    self.hit_ctr = self.target_length
                    string = "That's right!"
                else:
                    string = guess + " is not my word! heheXD\n"
                    string += self.get_guessed_word(self.target_word, self.guessed_letters)
            else:
                # Invalid guess
                string = "Oops! You should only type a letter at a time"
        elif guess  in self.guessed_letters:
            # Invalid guess 2
            string = "Oops! You've already guessed that letter! \n"
            string += self.get_guessed_word(self.target_word, self.guessed_letters)
        elif guess not in self.target_word: 
            string = "That letter is not in my word! heheXD\n"
            string += self.get_guessed_word(self.target_word, self.guessed_letters)
            self.guessed_letters+=guess
            self.guessed_letters+=" "
            self.miss_ctr+=1
        else:
            self.guessed_letters+=guess
            self.guessed_letters+=" "
            string = "Good guess!\n"
            string += self.get_guessed_word(self.target_word, self.guessed_letters)
        
        return string

    def check_game_status(self):
        # Check winning conditions
        if(self.state=="finding word"):
            self.check_status() #for transition
        print("hit = ", self.hit_ctr)
        print("len = ", self.target_length)
        if self.hit_ctr==self.target_length:
            string = "Congratulations, you won!"
            self.game_over()
        elif self.total_chances - self.miss_ctr>0:
            string = "Guessed letters : "
            string += self.guessed_letters
            self.back_to_running()
        elif self.total_chances - self.miss_ctr==0:
            string = "Sorry, you ran out of guesses. The word was "
            string += self.target_word
            self.game_over()
        return string

    def get_hangman_photo_url(self):
        if self.miss_ctr==0:
            return "https://i.imgur.com/LiokmcN.png"
        elif self.miss_ctr==1:
            return "https://i.imgur.com/F1S6nD6.png"
        elif self.miss_ctr==2:
            return "https://i.imgur.com/CJiX6Vx.png"
        elif self.miss_ctr==3:
            return "https://i.imgur.com/1Bptnnf.png"
        elif self.miss_ctr==4:
            return "https://i.imgur.com/lZGclGD.png"
        elif self.miss_ctr==5:
            return "https://i.imgur.com/e5ONTNd.png"
        else:
            return "https://i.imgur.com/otFbGVh.png"

    def get_game_done(self):
        return self.gg

    def game_over(self):
        self.end() #for transition
        self.gg = True
        return
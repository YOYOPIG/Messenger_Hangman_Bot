import random

class Hangman(object):

    WORDLIST_FILENAME = "words.txt"

    def __init__(self, name):
        self.name = name

    # Initialize the game state
    def game_start(self):
        self.missed_guesses = ""
        self.miss_ctr = 0
        self.hit_ctr = 0
        self.target_word = ""
        self.total_chances = 6
        self.guessed_letters= ""

        # Read in the words file
        self.get_target_word("words.txt")
        self.target_length=len(self.target_word)
        print(self.target_word)

        # Print starting msg
        print("Game started.")
        string = "Welcome to the game Hangman!\n"
        string += "The word is " + str(self.target_length) + " letters long."
        return string


    def get_target_word(self, filename):
        """
        Gets a random word from file.
        filename : the string of input file's name.
        Sets the word to guess in lowercase.
        """
        print("Loading word list from file...")
        # inFile: file
        inFile = open(filename, 'r')
        # line: string
        line = inFile.readline()
        # wordlist: list of strings
        words = line.split()
        self.target_word = random.choice(words).lower()
        return

    #get current guessing progress
    def get_guessed_word(self, secretWord, lettersGuessed):
        '''
        secretWord : string, the word the user is guessing
        lettersGuessed : list, what letters have been guessed so far
        returns: string, comprised of letters and underscores that represents
        what letters in secretWord have been guessed so far.
        '''
        string=""
        self.hit_ctr = 0
        for key in secretWord:
            if key in lettersGuessed:
                string+=key
                string+=" "
                self.hit_ctr+=1
            else:
                string+="_ "
        return string
        
    def input_word(self, user_input):
        # Make sure its lowercase!
        guess = user_input.lower()
        if len(guess)>1:
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
        #check winning conditions
        print("hit = ", self.hit_ctr)
        print("len = ", self.target_length)
        if self.hit_ctr==self.target_length:
            string = "Congratulations, you won!"
        elif self.total_chances - self.miss_ctr>0:
            string = "You have"
            string += str(self.total_chances - self.miss_ctr)
            string += "guesses left."
        elif self.total_chances - self.miss_ctr==0:
            string = "Sorry, you ran out of guesses. The word was "
            string += self.target_word
        return string

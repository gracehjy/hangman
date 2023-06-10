import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)
    
    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for char in secret_word:
        if char not in letters_guessed:
            return False

    return True


def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    guess = ""
    for char in secret_word:
        if char in letters_guessed:
            guess += char
        else:
            guess += "_ "

    return guess


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    alphabet = string.ascii_lowercase
    available_letters = ""
    for char in alphabet:
        if char not in letters_guessed:
            available_letters += char
                
    return available_letters


def get_unique_letters(secret_word):
    '''
    secret_word : string, the word the user is guessing
    returns: int, the number of unique letters in the secret word
    '''
    s = set(secret_word)
    return len(s)
    

def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!
    
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
    
    Follows the other limitations detailed in the problem write-up.
    '''

    num_warnings = 3
    num_guesses = 6
    word_list = load_words()
    secret_word = choose_word(word_list)
    letters_guessed = []
    consonants = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z']
    vowels = ['a','e','i','o','u']
    
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", len(secret_word),"letters long.")
    print("__________")
    
    while num_guesses > 0:
        print("You have", num_warnings,"warnings left.")
        print("You have", num_guesses,"guesses left.")
        print("Available letters:", get_available_letters(letters_guessed))
        
        while True:
            print()
            guess = input("Please guess a letter: ")
            if guess.isalpha() and len(guess) == 1 and guess.lower() not in letters_guessed:
                letters_guessed.append(guess)
                isInSecretWord = False
                for char in secret_word:
                    if char == guess.lower():
                        print("Good Guess:", get_guessed_word(secret_word, letters_guessed))
                        print("__________")
                        isInSecretWord = True
                        break
                    else:
                        isInSecretWord = False
                if isInSecretWord == False:
                    if(guess.lower() in consonants):
                        num_guesses -= 1
                    elif(guess.lower() in vowels):
                        num_guesses -=2
                    print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
                    print("__________")
                    break
                break
            else:
                if guess.lower() in letters_guessed:
                    print("Oops! You've already guessed that letter.")
                else: 
                    print("Please only input an alphabet (one letter).")
                if num_warnings > 0:
                    num_warnings -= 1
                    print("You now have", num_warnings,"warnings left: ", get_guessed_word(secret_word, letters_guessed))
                    print("__________")
                else:
                    num_guesses -= 1
                    if num_guesses > 0:
                        print("You now have", num_guesses,"guesses left: ", get_guessed_word(secret_word, letters_guessed))
                        print("__________")
                    else:
                        break
        
        if is_word_guessed(secret_word, letters_guessed):
            break
    if is_word_guessed(secret_word, letters_guessed):
        print("Congratulations, you won!")
        print("Your total score for this game is:",(num_guesses*get_unique_letters(secret_word)))
    else:
        print("Sorry, you ran out of guesses. The word was", secret_word+".")
        


# The next 3 functions are for hangman_with_hints


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
    other_word: string, regular English word
    returns: boolean, True if all the actual letters of my_word match the 
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise: 
    '''
    my_word = my_word.replace(" ", "")
    if len(my_word) != len(other_word):
        return False
    
    index = 0
    letters_missing = []
    
    for char in my_word:
        if char != other_word[index:index+1] and char != "_":
            return False
        if char == other_word[index:index+1]:
            if char in letters_missing:
                return False
        else:
            if other_word[index:index+1] not in letters_missing:
                letters_missing.append(other_word[index:index+1])
        index += 1
    return True
    

def show_possible_matches(my_word, letters_not_in_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    matches = []
    for word in wordlist:
        if match_with_gaps(my_word, word):
            word_is_a_match = False
            for char in word:
                if char in letters_not_in_word:
                    word_is_a_match = False
                    break
                else:
                    word_is_a_match = True
            if word_is_a_match:
                matches.append(word)
    if len(matches) <= 1:
        print("No other matches found.")
    else:
        print("Possible matches are: ")
        print(" ".join(matches))
    
def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.
    
    Starts up an interactive game of Hangman.
    
    * At the start of the game, let the user know how many 
      letters the secret_word contains and how many guesses s/he starts with.
      
    * The user should start with 6 guesses
    
    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.
    
    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter
      
    * The user should receive feedback immediately after each guess 
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the 
      partially guessed word so far.
      
    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word. 
    
    Follows the other limitations detailed in the problem write-up.
    '''
    num_warnings = 3
    num_guesses = 6
    word_list = load_words()
    secret_word = choose_word(word_list)
    letters_guessed = []
    consonants = ['b','c','d','f','g','h','j','k','l','m','n','p','q','r','s','t','v','w','x','y','z']
    vowels = ['a','e','i','o','u']
    letters_not_in_word = []
    
    print("Welcome to the game Hangman!")
    print("I am thinking of a word that is", len(secret_word),"letters long.")
    print("__________")
    
    while num_guesses > 0:
        print("You have", num_warnings,"warnings left.")
        print("You have", num_guesses,"guesses left.")
        print("Available letters:", get_available_letters(letters_guessed))
        
        while True:
            print()
            guess = input("Please guess a letter: ")
            if guess == "*":
                show_possible_matches(get_guessed_word(secret_word, letters_guessed), letters_not_in_word)
                break
            if guess.isalpha() and len(guess) == 1 and guess.lower() not in letters_guessed:
                letters_guessed.append(guess)
                isInSecretWord = False
                for char in secret_word:
                    if char == guess.lower():
                        print("Good Guess:", get_guessed_word(secret_word, letters_guessed))
                        print("__________")
                        isInSecretWord = True
                        break
                    else:
                        isInSecretWord = False
                if isInSecretWord == False:
                    if(guess.lower() in consonants):
                        num_guesses -= 1
                    elif(guess.lower() in vowels):
                        num_guesses -=2
                    print("Oops! That letter is not in my word:", get_guessed_word(secret_word, letters_guessed))
                    print("__________")
                    letters_not_in_word.append(guess)
                    break
                break
            else:
                if guess.lower() in letters_guessed:
                    print("Oops! You've already guessed that letter.")
                else: 
                    print("Please only input an alphabet (one letter).")
                if num_warnings > 0:
                    num_warnings -= 1
                    print("You now have", num_warnings,"warnings left: ", get_guessed_word(secret_word, letters_guessed))
                    print("__________")
                else:
                    num_guesses -= 1
                    if num_guesses > 0:
                        print("You now have", num_guesses,"guesses left: ", get_guessed_word(secret_word, letters_guessed))
                        print("__________")
                    else:
                        break
        
        if is_word_guessed(secret_word, letters_guessed):
            break
    if is_word_guessed(secret_word, letters_guessed):
        print("Congratulations, you won!")
        print("Your total score for this game is:",(num_guesses*get_unique_letters(secret_word)))
    else:
        print("Sorry, you ran out of guesses. The word was", secret_word+".")


if __name__ == "__main__":
    
    # to play without hints, change hangman_with_hints(secret_word) to hangman(secret_word)
    
    secret_word = choose_word(wordlist)
    hangman_with_hints(secret_word)

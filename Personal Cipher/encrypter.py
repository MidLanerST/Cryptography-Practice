import datetime
from datetime import datetime

import random


# This class will encrypt a hidden message
class Encrypter:

    # Initiate the class with the given file location, message, and a secret encryption key. It also gets the datetime value at the time of initialization
    def __init__ (self, file_location, message, encryption_key):
        self.file_location = file_location
        self.message = message.lower().replace(' ', '') # No spaces or capitals in the message
        self.encryption_key = encryption_key
        self.datetime_value = datetime.timestamp(datetime.now())

    # End init


    # Confirms that the file storage location, the message, and the datetime value were inputted and reformatted correctly
    # This function is for testing purposes. It does not need to be used.
    def confirm(self):
        print("File will be stored at: {0} \nThe message is: {1}\nThe datetime value is: {2}".format(self.file_location, self.message, self.datetime_value))
    # End confirm
    

    # Creates a encrypted alphabet for use
    # Returns the encrypted alphabet
    def create_encrypted_alphabet(self):
        base_alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        encrypted_alphabet = base_alphabet.copy()

        # Each letter is moved three times. The seeds for each use different factors.
        # Seed 0: The year, month, and day
        # Seed 1: The encryption key
        # Seed 2: The time
        movements = [
            (datetime.fromtimestamp(self.datetime_value).year + datetime.fromtimestamp(self.datetime_value).month) - datetime.fromtimestamp(self.datetime_value).day,

            len(self.encryption_key) + ord(self.encryption_key[0]),

            float(datetime.fromtimestamp(self.datetime_value).time().isoformat().replace(':',''))
        ]


        # Collects the values from the random seeds and adds them to their respective lists
        locations = [ [], [], []]
        for i in range(0, len(movements)):
            random.seed(movements[i])

            for j in range(0, len(encrypted_alphabet)):
                locations[i].append(random.randrange(0, len(encrypted_alphabet)))

            # End for
        # End for


        # For each letter
        for i in range(0, len(encrypted_alphabet)):
            # Find the letter (a.. b.. etc)
            letter = chr(97 + i)

            # For each movement
            for j in range(0, len(movements)):
                # Swap the current letter and whichever letter is in its next location
                placeholder = encrypted_alphabet[locations[j][i]]
                encrypted_alphabet[locations[j][i]] = encrypted_alphabet[encrypted_alphabet.index(letter)]
                encrypted_alphabet[encrypted_alphabet.index(letter)] = placeholder

        #print(encrypted_alphabet) # Testing output

        return encrypted_alphabet

    # End create_encrypted_alphabet


    # Encrypt the message using a given encrypted alphabet
    # Returns the encrypted message
    def encrypt_message(self, encrypted_alphabet):
        base_alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        new_message = ''

        # Add a letter from the encrypted alphabet whos index is the same as the letter in the base alphabet
        for i in range(0, len(self.message)):
            new_message += encrypted_alphabet[base_alphabet.index(self.message[i])]

        
        #print(new_message) # Testing message output

        return new_message

    # End encrypt_message



    # Scrambles the message into a random order
    # Returns the scrambled message
    def scramble_message(self):
        message_as_list = []


    # To do
    # scrambler
    # Output
            


test = Encrypter(".", "A test Test", "no")
test.confirm()
alphabet = test.create_encrypted_alphabet()
test.encrypt_message(alphabet)
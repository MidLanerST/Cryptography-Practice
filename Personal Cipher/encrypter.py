import datetime
from datetime import datetime
from math import ceil

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
        encrypted_message = ''

        # Add a letter from the encrypted alphabet whos index is the same as the letter in the base alphabet
        for i in range(0, len(self.message)):
            encrypted_message += encrypted_alphabet[base_alphabet.index(self.message[i])]

        
        #print(encrypted_message) # Testing message output

        return encrypted_message

    # End encrypt_message



    # Scrambles the message into a random order
    # Returns the scrambled message
    def scramble_message(self, encrypted_message):

        message_as_list = [ [] for _ in range (0, ceil(len(encrypted_message)/ 5) )]

        for i in range(0, len(message_as_list)):
            for j in range(0, 5):
                try:
                    message_as_list[i].append(encrypted_message[i*5 + j])

                except:
                    message_as_list[i].append(chr(97 + j))


        #print(message_as_list) # Verify the message got put in correctly


        column_location = []
        row_location    = []

        # Column (y) Seed = datetime + the value of the first letter times the value of the last letter
        random.seed(self.datetime_value + (ord(message_as_list[0][0]) * ord(message_as_list[len(message_as_list) - 1][len(message_as_list[0]) - 1]))) 

        # Since the entire 3D List will always be filled, we can multiply number of inner lists by how many values are stored in each to get max length
        for i in range(0, len(message_as_list) * len(message_as_list[0])):
            column_location.append(random.randrange(0, len(message_as_list)))

        
        # Row (x) Seed = datetime + value of the second letter times the value of the second to last letter
        random.seed(self.datetime_value + (ord(message_as_list[0][0]) * ord(message_as_list[len(message_as_list) - 1][len(message_as_list[0]) - 1]))) 
        for i in range(0, len(message_as_list) * len(message_as_list[0])):
            row_location.append(random.randrange(0, len(message_as_list[0])))

        row_location.reverse() # Reverse the list to further randomness just in case

        #print(column_location) # Ensure value correctness
        #print(row_location) # Ensure value correctness

        for i in range(0, len(message_as_list)):
            for j in range(0, len(message_as_list[0])):
                temp_value = message_as_list[ column_location[((i + 1) * (j + 1)) - 1]][ row_location[((i + 1) * (j + 1)) - 1] ]
                message_as_list[ column_location[((i + 1) * (j + 1)) - 1]][ row_location[((i + 1) * (j + 1)) - 1] ]  = message_as_list[i][j]
                message_as_list[i][j] = temp_value

        #print(message_as_list)

        return message_as_list

        # End scramble_message
        
    # To do
    # Output
    # Reverse
            


test = Encrypter(".", "A test Testt t", "no")
test.confirm()
alphabet = test.create_encrypted_alphabet()
message = test.encrypt_message(alphabet)
test.scramble_message(message)
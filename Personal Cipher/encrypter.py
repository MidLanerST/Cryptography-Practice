import datetime
from datetime import datetime
from math import ceil
import os.path
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



    ## Miscellaneous utility functions

    # This creates an encoded key for output storage purposes
    def get_encoded_key(self):
        encoded_key = ''
        for i in range(0, len(self.encryption_key)):
                    try:
                        if(i == (len(self.encryption_key) - 1)):
                            raise Exception('No Underscore Needed')
                        
                        encoded_key += (str(ord(self.encryption_key[i])) + '_')

                    except:
                        encoded_key += (str(ord(self.encryption_key[i])) + '\n')

        return encoded_key

    # Returns the datetime value
    def get_datetime(self):
        return str(self.datetime_value)


    # Confirms that the file storage location, the message, and the datetime value were inputted and reformatted correctly
    # This function is for testing purposes. It does not need to be used.
    def confirm(self):
        return "File will be stored at: {0} \nThe message is: {1}\nThe datetime value is: {2}".format(self.file_location, self.message, self.datetime_value)
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
        random.seed(self.datetime_value + (ord(self.encryption_key[0]) * ord(self.encryption_key[len(self.encryption_key) - 1]))) 

        # Since the entire 3D List will always be filled, we can multiply number of inner lists by how many values are stored in each to get max length
        for i in range(0, len(message_as_list) * len(message_as_list[0])):
            column_location.append(random.randrange(0, len(message_as_list)))

        
        # Row (x) Seed = datetime + value of the second letter times the value of the second to last letter
        random.seed(self.datetime_value + (ord(self.encryption_key[1]) * ord(self.encryption_key[len(self.encryption_key) - 2]))) 
        for i in range(0, len(message_as_list) * len(message_as_list[0])):
            row_location.append(random.randrange(0, len(message_as_list[0])))

        row_location.reverse() # Reverse the list to handle bias

        #print(column_location) # Ensure value correctness
        #print(row_location) # Ensure value correctness

        
        for i in range(0, len(message_as_list)):
            for j in range(0, len(message_as_list[0])):
                # Column and Row are in range for 0->14 so janky looking math just to read them across their range
                temp_value = message_as_list[ column_location[((i + 1) * (j + 1)) - 1]][ row_location[((i + 1) * (j + 1)) - 1] ]
                message_as_list[ column_location[((i + 1) * (j + 1)) - 1]][ row_location[((i + 1) * (j + 1)) - 1] ]  = message_as_list[i][j]
                message_as_list[i][j] = temp_value

        #print(message_as_list)

        scrambled_encrypted_message = ''


        for i in range(0, len(message_as_list[0])):
            for j in range(0, len(message_as_list)):
                # For a 3D array, read each column then move on
                scrambled_encrypted_message += message_as_list[j][i]


        #print(scrambled_encrypted_message) # Error Testing

        return scrambled_encrypted_message

        # End scramble_message


    # Outputs the message to a file including the necessary information for de-scrambling
    # Output is formatted as follows and DOES NOT APPEND to the document
    # This means that Output will WIPE THE FILE
    # Message: <Message as one line here>
    # Key: <Encryption Key in the form ascii-letter_ascii-letter...>
    # Timestamp: <Timestamp Format>
    def output_message(self, final_message):
        try:
            with open(os.path.join(self.file_location, str(datetime.fromtimestamp(self.datetime_value).strftime("%Y-%m-%d %H-%M-%S")).replace(' ','_') + '.txt'), 'w') as out_file:
                out_file.write(final_message + '\n')
                out_file.write(self.get_encoded_key())
                out_file.write(str(self.datetime_value))

                out_file.close()

        except:
            print('Failure')
            

    # End output_message




# This class will Decrypt a message given a file
class Decrypter:

    def __init__(self, in_file_location, out_file_location):
        
        # All variables set up
        self.file_location = out_file_location # Only need to save the out location for later

        self.encrypted_message = ''
        self.encryption_key = ''
        self.datetime_value = ''

        # Read in from the given file
        with open(in_file_location) as in_file:
            file_lines = in_file.readlines()

            self.encrypted_message = str(file_lines[0]).strip()
            
            # Add each individual letter split at _
            temp_key = file_lines[1].split('_')
            for i in range(0, len(temp_key)):
                self.encryption_key += chr(int(temp_key[i]))

            self.datetime_value = float(file_lines[2])
        
    # End init


    # Confirms that the file storage location, the message, and the datetime value were inputted and reformatted correctly
    # This function is for testing purposes. It does not need to be used.
    def confirm(self):
        return  "File will be stored at: {0} \nThe message is: {1}\nThe datetime value is: {2}".format(self.file_location, self.encrypted_message, self.datetime_value)
    # End confirm



    # This function descrambles the scrambled message
    # Returns the descrambled message
    def descramble_message(self):

        message_as_list = [ [] for _ in range (0, ceil(len(self.encrypted_message)/ 5) )]

        for i in range(0, 5):
            for j in range(0, len(message_as_list)):
                message_as_list[j].append(self.encrypted_message[(i*(len(message_as_list)))+j])

        #print(message_as_list) # Checking output


        column_location = []
        row_location    = []

        # Column (y) Seed = datetime + the value of the first letter times the value of the last letter
        random.seed(self.datetime_value + (ord(self.encryption_key[0]) * ord(self.encryption_key[len(self.encryption_key) - 1]))) 

        # Since the entire 3D List will always be filled, we can multiply number of inner lists by how many values are stored in each to get max length
        for i in range(0, len(message_as_list) * len(message_as_list[0])):
            column_location.append(random.randrange(0, len(message_as_list)))

        
        # Row (x) Seed = datetime + value of the second letter times the value of the second to last letter
        random.seed(self.datetime_value + (ord(self.encryption_key[1]) * ord(self.encryption_key[len(self.encryption_key) - 2]))) 
        for i in range(0, len(message_as_list) * len(message_as_list[0])):
            row_location.append(random.randrange(0, len(message_as_list[0])))

        row_location.reverse() # Reverse the list to handle bias


        for i in range(len(message_as_list) - 1, -1, -1):
            for j in range(len(message_as_list[0]) - 1, -1 , -1):
                # Column and Row are in range for 0->14 so janky looking math just to read them across their range
                temp_value = message_as_list[ column_location[((i + 1) * (j + 1)) - 1]][ row_location[((i + 1) * (j + 1)) - 1] ]
                message_as_list[ column_location[((i + 1) * (j + 1)) - 1]][ row_location[((i + 1) * (j + 1)) - 1] ]  = message_as_list[i][j]
                message_as_list[i][j] = temp_value


        #print(message_as_list) # Verify descrambling

        descrambled_message = ''
        for i in range(0, len(message_as_list)):
            for j in range(0, len(message_as_list[0])):
                descrambled_message += message_as_list[i][j]

        return descrambled_message

    # End descramble_message



    #
    #
    def create_decryption_alphabet(self):
        base_alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        decryption_alphabet = base_alphabet.copy()

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

            for j in range(0, len(decryption_alphabet)):
                locations[i].append(random.randrange(0, len(decryption_alphabet)))

            # End for
        # End for


        # For each letter
        for i in range(0, len(decryption_alphabet)):
            # Find the letter (a.. b.. etc)
            letter = chr(97 + i)

            # For each movement
            for j in range(0, len(movements)):
                # Swap the current letter and whichever letter is in its next location
                placeholder = decryption_alphabet[locations[j][i]]
                decryption_alphabet[locations[j][i]] = decryption_alphabet[decryption_alphabet.index(letter)]
                decryption_alphabet[decryption_alphabet.index(letter)] = placeholder

        #print(decryption_alphabet) # Testing output

        return decryption_alphabet



    # Decrypts an unscrambled message given the message and the decryption alphabet
    # Returns the decryption message
    def decrypt_message(self, descrambled_message, decryption_alphabet):
        base_alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        decrypted_message = ''

        # Add a letter from the base alphabet whos index is the same as the letter in the decryption alphabet
        for i in range(0, len(descrambled_message)):
            decrypted_message += base_alphabet[decryption_alphabet.index(descrambled_message[i])]

        
        #print(decrypted_message) # Testing message output

        return decrypted_message

    # End decrypt message


    #
    #
    def output_original_message(self, original_message):
        try:
            with open(os.path.join(self.file_location, str(datetime.fromtimestamp(self.datetime_value).strftime("%Y-%m-%d %H-%M-%S")).replace(' ','_') + '_Solved.txt'), 'w') as out_file:
                out_file.write(original_message + '\n')
                #out_file.write(str(self.datetime_value))

                out_file.close()

        except:
            print('Failure?')

        #return 0

    # End output original message

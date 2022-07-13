import random as rand
import copy as cp

rand.seed(rand.randint(0,1000000000000))

class Jefferson_Cipher_Wheel:

    def __init__(self, encryptIn, encryptOut, decryptIn, decryptOut ):
        self.encryptIn      = encryptIn
        self.encryptOut     = encryptOut
        self.decryptIn      = decryptIn
        self.decryptOut     = decryptOut

        self.alphabet       = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.wheel          = []
        self.sortedWheel    = []

        self.wheels         = []
        self.sortedWheels   = []

        return


    def main(self):

        print("Hello and welcome to the Jefferson Cipher Wheel program.")

        prompt              = ''
        lines               = 0
        encryptedMessages   = []

        while( (prompt.lower() not in ['e','d','exit']) or (int(lines) <= 0) ):
            prompt = input("Would you like to (E)ncrypt or (D)ecrypt? ")

            lines = input("How many lines does your message have? (Each sentence is a line): ")

            if( (prompt.lower() not in ['e','d','exit']) or (int(lines) <= 0) ):
                print('Error, invalid prompt or line value')

        # For multiple lines
        if(int(lines) > 1):

            if(prompt.lower() == 'e'):

                messages = self.encrypt_in_many()
                encryptedMessages = (self.encrypt_message_many(messages))
                self.encrypt_out_many(encryptedMessages)

            elif(prompt.lower() == 'd'):

                inMessages = self.decrypt_in_many()
                self.decrypt_message_many(inMessages)
                self.decrypt_out_many()

        # Otherwise singular line
        elif(int(lines) == 1):

            if(prompt.lower() == 'e'):

                message = self.encrypt_in()
                encryptedMessages = (self.encrypt_message(message))
                self.encrypt_out(encryptedMessages)

            elif(prompt.lower() == 'd'):

                inMessage = self.decrypt_in()
                self.decrypt_message(inMessage)
                self.decrypt_out()

    #                           #
    #   ~~~ Actual Methods ~~~  #
    #                           #


    #   ~~~ Encryption section ~~~  #

    #   ~~~ Encrypt_In: Take in a singular line and return it, or take in multiple and return a list ~~~    #
    def encrypt_in(self):
        with open(self.encryptIn, 'r') as file:
            message = file.readline()

        file.close()

        return message

    
    def encrypt_in_many(self):
        with open(self.encryptIn, 'r') as file:
            messages = file.read().splitlines()

        file.close()

        return messages


    #   ~~~ Encrypt_Out: Send the encrypted message then the wheel vertically, or multiple messages then multiple wheels vertically ~~~ #
    def encrypt_out(self, encryptedMessage):
        
        with open(self.encryptOut, 'w') as file:
            file.write(encryptedMessage + '\n')

            for i in range(0,len(self.wheel[0])):
                for j in range(0, len(self.wheel)):
                    file.write(self.wheel[j][i] +' ')

                file.write('\n')

        file.close()
        return


    def encrypt_out_many(self, encryptedMessages):
        
        with open(self.encryptOut, 'w') as file:
            for i in range(0, len(encryptedMessages)):
                file.write(''.join(encryptedMessages[i])+ '. ')

            file.write('\n')

            for k in range(0, len(self.wheels)):
                for i in range(0,len(self.wheels[k][0])):
                    for j in range(0, len(self.wheels[k])):
                        file.write(self.wheels[k][j][i] + ' ')

                    file.write('\n')

        file.close()
        
        return

    
    def encrypt_message(self, message):
        message         = message.replace(' ', '').strip().lower()
        counter         = 0
        letterCounter   = 0

        # The wheel is made up of message length random alphabets
        
        for i in range (0, len(message)):
            list = rand.sample(self.alphabet, 26)
            self.wheel.append(list)

        self.sortedWheel = cp.deepcopy(self.wheel)

        for letter in message: # Start with a letter
            letterLocation = self.wheel[counter].index(letter) # Find its location
            letterCounter  = letterLocation # Start there

            for i in range(0,len(self.wheel[counter])): # For every letter in the alphabet
                if(letterCounter == len(self.wheel[0])): # If letter counter is at the end, back to beginning
                    letterCounter = 0
                self.sortedWheel[counter][i] = self.wheel[counter][letterCounter] # Sorted wheel from 0 to 25 = start from counter and move on
                
                letterCounter += 1

            counter += 1

        encryptedMessage = ''
        randomRow = rand.randint(1,25)

        for i in range(len(self.sortedWheel)):
            encryptedMessage += self.sortedWheel[i][randomRow]

        #self.encrypt_out(encryptedMessage)

        return encryptedMessage


    def encrypt_message_many(self, messages):
        lineTracker = 0
        self.wheels = [ [  ] for _ in range(len(messages)) ]
        self.sortedWheels = [ [ ] for _ in range(len(messages)) ]

        encryptedMessages = [ [] for _ in range(0,len(messages))]
        messageCounter = 0

        for line in messages:
            message         = line.replace(' ', '').strip().lower()
            counter         = 0
            letterCounter   = 0

            # The wheel is made up of message length random alphabets
            
            for i in range (0, len(message)):
                list = rand.sample(self.alphabet, 26)
                self.wheels[lineTracker].append(list)

            self.sortedWheels = cp.deepcopy(self.wheels)
            #print(self.sortedWheels)

            for letter in message: # Start with a letter
                letterLocation = self.wheels[lineTracker][counter].index(letter) # Find its location
                letterCounter  = letterLocation # Start there

                for i in range(0,len(self.wheels[lineTracker][counter])): # For every letter in the alphabet
                    if(letterCounter == len(self.wheels[lineTracker][0])): # If letter counter is at the end, back to beginning
                        letterCounter = 0
                    self.sortedWheels[lineTracker][counter][i] = self.wheels[lineTracker][counter][letterCounter] # Sorted wheel from 0 to 25 = start from counter and move on
                    
                    letterCounter += 1

                counter += 1

            encryptedMessage = ''
            randomRow = rand.randint(1,25)

            for i in range(len(self.sortedWheels[lineTracker])):
                encryptedMessage += self.sortedWheels[lineTracker][i][randomRow]
                
            encryptedMessages[messageCounter].append(encryptedMessage)

            lineTracker += 1
            messageCounter += 1

        return encryptedMessages


# ~~~ Decryption Section ~~~    #


    def decrypt_in(self):
        with open(self.decryptIn, 'r') as file:
            storage = file.read().splitlines()

            message = storage[0].strip()
            storage.pop(0)

            self.wheel = [ [' '] * 26 for _ in range((len(storage[0].strip().split(' ')))) ]
            counter = 0
            for line in storage:
                temp = line.strip().split(' ')
                for i in range(0,len(temp)):
                    self.wheel[i][counter] = temp[i]
                
                counter += 1

        return message

    
    def decrypt_in_many(self):
        with open(self.decryptIn, 'r') as file:
            storage = file.read().splitlines()

            messages = storage[0].split('. ')
            messages.pop()
            storage.pop(0)

            counter             = 0
            messageCounter      = 0

            self.wheels         = [ [ [] ] for _ in range(0, len(messages)) ]

            for message in messages:

                for i in range(0, len(message)-1):
                    self.wheels[messageCounter].append([])
                
                # Start at 0 or at 26, 52, etc, to (total/lines -1) * counter + 1. So 0,26-26,54-etc
                for i in range( counter * 26, (round((len(storage)/len(messages))) * (counter+1)) ):
                    

                    temp = storage[i].strip().split(' ')

                    for j in range(0,len(temp)):
                        self.wheels[messageCounter][j].append(temp[j])

                counter += 1
                messageCounter += 1

        return messages

    
    def decrypt_out(self):
        
        with open(self.decryptOut, 'w') as file:

            for i in range(0,len(self.sortedWheel[0])):
                for j in range(0, len(self.sortedWheel)):
                    file.write(self.sortedWheel[j][i] +' ')
                
                file.write('\n')

        file.close()
        return

    
    def decrypt_out_many(self):

        with open(self.decryptOut, 'w') as file:
            for k in range(0, len(self.sortedWheels)):
                for i in range(0,len(self.sortedWheels[k][0])):
                    for j in range(0, len(self.sortedWheels[k])):
                        file.write(self.sortedWheels[k][j][i] + ' ')

                    file.write('\n')

                file.write('\n')

            

        file.close()
        return


    def decrypt_message(self, message):
        
        counter = 0
        self.sortedWheel = cp.deepcopy(self.wheel)

        for letter in message: # Start with a letter
            letterLocation = self.wheel[counter].index(letter) # Find its location
            letterCounter  = letterLocation # Start there

            for i in range(0,len(self.wheel[counter])): # For every letter in the alphabet

                if(letterCounter == len(self.wheel[0])): # If letter counter is at the end, back to beginning
                    letterCounter = 0
                
                self.sortedWheel[counter][i] = self.wheel[counter][letterCounter] # Sorted wheel from 0 to 25 = start from counter and move on
                
                letterCounter += 1

            counter += 1

        return


    def decrypt_message_many(self, messages):
        
        lineTracker         = 0
        self.sortedWheels   = cp.deepcopy(self.wheels)

        #print(self.wheels[lineTracker])

        for message in messages:

            #print(message)
            counter = 0

            for letter in message: # Start with a letter
                #print(counter)
                letterLocation = self.wheels[lineTracker][counter].index(letter) # Find its location
                letterCounter  = letterLocation # Start there

                for i in range(0,len(self.wheels[lineTracker][counter])): # For every letter in the alphabet
                    if(letterCounter == len(self.wheels[lineTracker][0])): # If letter counter is at the end, back to beginning
                        letterCounter = 0
                    
                    self.sortedWheels[lineTracker][counter][i] = self.wheels[lineTracker][counter][letterCounter] # Sorted wheel from 0 to 25 = start from counter and move on
                    
                    letterCounter += 1

                counter += 1
            
            lineTracker += 1

        return


test = Jefferson_Cipher_Wheel('Jefferson Cipher Wheel/EIn.txt','Jefferson Cipher Wheel/EOut.txt','Jefferson Cipher Wheel/EOut.txt','Jefferson Cipher Wheel/DOut.txt')
test.main()

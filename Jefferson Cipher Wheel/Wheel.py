import random as rand
rand.seed(rand.randint(0,1000000000000))

class Jefferson_Cipher_Wheel:

    def __init__(self, inFile, outFile):
        self.inFile         = inFile
        self.outFile        = outFile

        self.alphabet       = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.wheel          = []
        self.sortedWheel    = []

        return


    def encrypt_out(self, encryptedMessage):
        
        with open(self.outFile, 'w') as file:
            file.write(encryptedMessage + '\n\n')

            for i in range(0,len(self.sortedWheel[0])):
                for j in range(0, len(self.sortedWheel)):
                    file.write(self.sortedWheel[j][i] +' ')

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

        self.sortedWheel = self.wheel.copy()
        print(self.wheel)

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

        self.encrypt_out(encryptedMessage)

        return encryptedMessage



        





a = Jefferson_Cipher_Wheel('Jefferson Cipher Wheel/Input.txt','Jefferson Cipher Wheel/Output.txt')
b = a.encrypt_message('Hello')
print(b)


import PySimpleGUI as UI
import encrypter as enc
import tempfile
import os, os.path

# Miscellaneous Functions for layout utility

def collapse(layout, key):
    return UI.pin(UI.Column(layout, key=key, visible = False))


##---  Themeing and Layouts Below  ---##
UI.theme('DarkAmber')

# The main layout for the core application
main_layout = [
    [UI.Push(), UI.Text("Welcome to the program"), UI.Push()], #
    [UI.Push(), UI.Text("What would you like to do?"), UI.Push(),], #
    [UI.Button('Encryption'), UI.Push(),  UI.Button('Decryption')], #
    [UI.Button('About Me'), UI.Push(), UI.Button('Cancel')], #
]


# Additional layouts used in other layouts - This is just their initial initializations
# TO EDIT THESE, EDIT VERSIONS IN THE CREATE LAYOUT FUNCTION
out_layout_collapse = [
    [UI.Text('Select the folder to place the file into: '), UI.Push(), UI.FolderBrowse(key = '-Encrypt-Out')], # Hidden unless otherwise necessary
] # Encrypt

decfile_layout_collapse = [
    [UI.Text('Select the file to decrypt:'), UI.Push(), UI.FileBrowse('Browse Files', key = '-Decrypt-In')],
] # Decrypt

man_layout_collapse = [
    [UI.Text('Message to Decrypt: '), UI.Push(), UI.InputText(key = '-Dec-Message')], #
    [UI.Text('Encryption Key used: '), UI.Push(), UI.InputText(key = '-Dec-Key')], #
    [UI.Text('Datetime value: '), UI.Push(), UI.InputText(key = '-Dec-Time')], #
] # Decrypt

decout_layout_collapse = [
    [UI.Text('Select the folder to place the file into: '), UI.Push(), UI.FolderBrowse('Browse Folders', key = '-Decrypt-Out')], # Hidden unless otherwise necessary
] # Decrypt


# The other primary layouts that may use sub layouts above or be accessed through main
# Since we cannot reuse layouts for separate windows, we will recreate it using this function for cleanliness
def create_layout(layout):

    if(layout == 'Encryption'):

        # Refresh any additional layouts the primary is dependent on
        out_layout_collapse = [
            [UI.Text('Select the folder to place the file into: '), UI.Push(), UI.FolderBrowse()], # Hidden unless otherwise necessary
        ]

        # The layout for the encryption window
        encrypt_layout = [
            [UI.Text('Message to Encrypt: (A-Z, no punctuation or special characters)')], # 
            [UI.Push(), UI.InputText(key = '-Encrypt-Message'), UI.Push(),], #
            [UI.Text('Encryption Key: (Min 4 characters, limited to Ascii, any characters)')], #
            [UI.Push(), UI.InputText(size = (35, None), key = '-Encrypt-Key'), UI.Push()], #

            [UI.Checkbox('Output the encrypted message to file?', enable_events = True, key = '-OPEN EncOutCheck')], #
            [collapse(out_layout_collapse, '-SelectOut-')], #

            [UI.Button('Encrypt Message'), UI.Push(), UI.Button('Cancel')], #

            [UI.HorizontalSeparator()], #
            [UI.Text('Output: ')],
            [UI.Multiline('Waiting...', size = (60, 10), key='-Encrypt-Display')],

            # To Add:
            # Exit Button
            # Resizing
            #
        ]

        return encrypt_layout

    # End Encryption

    elif(layout == 'Decryption'):

        # Refresh any additional layouts the primary is dependent on

        decfile_layout_collapse = [
            [UI.Text('Select the file to decrypt:'), UI.Push(), UI.FileBrowse()],
        ]

        man_layout_collapse = [
            [UI.Text('Message to Decrypt: '), UI.Push(), UI.InputText(key = '-Dec-Message')], #
            [UI.Text('Encryption Key used: '), UI.Push(), UI.InputText(key = '-Dec-Key')], #
            [UI.Text('Datetime value: '), UI.Push(), UI.InputText(key = '-Dec-Time')], #
        ] # Decrypt

        decout_layout_collapse = [
            [UI.Text('Select the folder to place the file into: '), UI.Push(), UI.FolderBrowse()], # Hidden unless otherwise necessary
        ]

        # The layout for the decryption window
        decrypt_layout = [
            [UI.Checkbox('Decrypt from file?', enable_events = True, key = '-OPEN DecFileCheck')], #
            [collapse(decfile_layout_collapse, '-DecFile-')], #
            [UI.Checkbox('Decrypt manually?', enable_events = True, key = '-OPEN DecManCheck')], #
            [collapse(man_layout_collapse, '-ManIn-')], #
            [UI.Checkbox('Output the decrypted message to file?', enable_events = True, key = '-OPEN SelectOutCheck')], #
            [collapse(decout_layout_collapse, '-SelectOut-')], #
            [UI.Button('Decrypt Message'), UI.Push(), UI.Button('Cancel')], #

            [UI.HorizontalSeparator()], #
            [UI.Text('Output: ')],
            [UI.Multiline('Waiting...', size = (60, 10), key = '-Decrypt-Display')],

            # To Add:
            # Output Window
            # Input Validation
            # Resizing

        ]

        return decrypt_layout

    # End Decryption


    elif(layout == 'About'):

        # The layout for the about window
        about_layout = [
            [UI.Text('This application was made by Cole Snyder just for fun to test out a for-fun method of simple encryption and to gain experience with GUIs and GUI Design. If you would like to reach out, you can contact him at cole.snyder.m@gmail.com.', size = (30, 10))],
            [UI.Push(), UI.Button('Cancel'), UI.Push()],
        ]

        return about_layout

    # End About
# End create_layout



# Functional Stuff Below

# Start by loading the main window
main_window = UI.Window('Test', main_layout)

# The encrypt, decrypt, and about windows are off by default
encrypt_window_active   = False
decrypt_window_active   = False
about_window_active     = False

# For collapsing sections. False by default to hide
enc_open = False
dec_in_open = False
dec_man_open = False
dec_out_open = False

# Variables for Encryption and Decryption objects
encryption_object = 'enc.Encrypter('','','')' 
decryption_object = 'enc.Decrypter('','')'


# Main Window
while True:
    main_event, main_values = main_window.Read(timeout = 100)
    if main_event in (UI.WIN_CLOSED, 'Cancel'):
        break


    # Encryption Window
    if main_event == 'Encryption' and not encrypt_window_active:
        encrypt_window_active = True
        main_window.Hide()

        layout = create_layout('Encryption')
        encrypt_window = UI.Window('Encryption', layout)
        enc_open = False

        while True:
            encrypt_event, encrypt_values = encrypt_window.Read(timeout = 100)

            # Closes cleanly
            if encrypt_event in (UI.WIN_CLOSED, 'Cancel'):
                encrypt_window.Close()
                encrypt_window_active = False
                main_window.UnHide()
                break
            
            # Event for selecting file output
            if encrypt_event.startswith('-OPEN EncOut'):
                enc_open = not enc_open
                encrypt_window['-SelectOut-'].update(visible=enc_open)


            # Button to encrypt has been pressed
            if encrypt_event in ('Encrypt Message'):

                if enc_open:
                    if encrypt_values['Browse'] == '':
                        encrypt_window['-Encrypt-Display'].update('No folder location for output selected')
                        continue

                try:

                    encrypt_values['-Encrypt-Message'].encode('ascii')

                    if not encrypt_values['-Encrypt-Message'].replace(' ','').isalpha():
                        raise Exception('Invalid Characters')

                except:
                    encrypt_window['-Encrypt-Display'].update('The message contains an invalid character. Please only use A-Z with no punctuation or special characters. Spaces are allowed.')
                    continue

                try:
                    encrypt_values['-Encrypt-Key'].encode('ascii')
                    if((len(encrypt_values['-Encrypt-Key']) >= 4) == False):
                        raise Exception('Invalid Length')
                    

                except:
                    encrypt_window['-Encrypt-Display'].update('The key has a non-ascii character or is of an invalid length. Please only use Ascii characters, including A-Z, upper and lower, digits, and symbols. Minimum 4 characters.')

                    continue

                encryption_object = enc.Encrypter(encrypt_values['Browse'], encrypt_values['-Encrypt-Message'], encrypt_values['-Encrypt-Key'])

                #encrypt_window['-Encrypt-Display'].update(encryption_object.confirm()) # Verify output

                enc_alpha = encryption_object.create_encrypted_alphabet()
                enc_mess = encryption_object.encrypt_message(enc_alpha)
                enc_scram = encryption_object.scramble_message(enc_mess)
                enc_out_success = "The encrypted message was not sent to a file."

                if enc_open == True:
                    encryption_object.output_message(enc_scram)
                    enc_out_success = "The encrypted message was successfully sent to a file!"

                
                encrypt_window['-Encrypt-Display'].update('Message: {0}\nKey: {1}Timestamp: {2}\n{3}'.format(enc_scram, encryption_object.get_encoded_key(), encryption_object.get_datetime(), enc_out_success))

                # Immediately throws away the object
                encryption_object = ''
            
        
    # End Encryption Window


    # Decryption Window
    if main_event == 'Decryption' and not decrypt_window_active:
        decrypt_window_active = True
        main_window.Hide()

        layout = create_layout('Decryption')
        decrypt_window = UI.Window('Decryption', layout)

        while True:
            decrypt_event, decrypt_values = decrypt_window.Read(timeout = 100)

            # Closes cleanly
            if decrypt_event in (UI.WIN_CLOSED, 'Cancel'):
                decrypt_window.Close()
                decrypt_window_active = False
                main_window.UnHide()
                break
            
            # Checkbox Opens for various sections

            # File input
            if decrypt_event.startswith('-OPEN DecFile'):
                dec_in_open = not dec_in_open
                decrypt_window['-DecFile-'].update(visible=dec_in_open)
                
                # Close the manual input when using file input
                if dec_man_open == True:
                    dec_man_open = not dec_man_open
                    decrypt_window['-ManIn-'].update(visible=dec_man_open)
                    decrypt_window['-OPEN DecManCheck'].update(dec_man_open)
            
            # Manual Input
            if decrypt_event.startswith('-OPEN DecMan'):
                dec_man_open = not dec_man_open
                decrypt_window['-ManIn-'].update(visible=dec_man_open)

                # Close the file input when using manual input
                if dec_in_open == True:
                    dec_in_open = not dec_in_open
                    decrypt_window['-DecFile-'].update(visible=dec_in_open)
                    decrypt_window['-OPEN DecFileCheck'].update(dec_in_open)

            # Output
            if decrypt_event.startswith('-OPEN SelectOut'):
                dec_out_open = not dec_out_open
                decrypt_window['-SelectOut-'].update(visible=dec_out_open)

            
            # Button to decrypt has been pressed
            if decrypt_event in ('Decrypt Message'):

                if dec_out_open:
                    if decrypt_values['Browse0'] == '':
                        decrypt_window['-Decrypt-Display'].update('No folder location for output selected')
                        continue

                if dec_in_open:
                    try:
                        decryption_object = enc.Decrypter(decrypt_values['Browse'], decrypt_values['Browse0'])

                    except:
                        decrypt_window['-Decrypt-Display'].update('Error: The given file is not formatted correctly. Please use the following format:\nENCRYPTED MESSAGE\nOrdOfEncryptedKey_OrdOfEncryptedKey...\nDatetime value\n\nExample:\ntewrt\n97_97_97_97\n34236523856.324235235')
                        continue


                elif dec_man_open:

                    # Input validations before we make the temp file

                    # Verify the message is ascii alphabet characters
                    try:
                        decrypt_values['-Dec-Message'].encode('ascii')

                        if not decrypt_values['-Dec-Message'].isalpha():
                            raise Exception('Invalid Characters')

                    except:
                        decrypt_window['-Decrypt-Display'].update('The message contains an invalid character. Please only use a-z.')
                        continue


                    # Make sure there's no random special characters initially, and makes sure the format is correct using chr and length is valid
                    try:
                        decrypt_values['-Dec-Key'].encode('ascii')
                        tmp_list = decrypt_values['-Dec-Key'].split('_')
                        for i in range(0, len(tmp_list)):
                            try:
                                if((chr(int(tmp_list[i])).isascii() == False) or (len(tmp_list) < 4)):
                                    raise Exception('Invalid')

                            except:
                                raise Exception('Invalid')
                    

                    except:
                        decrypt_window['-Decrypt-Display'].update('The key is invalid. Please input a valid key.')
                        continue


                    # Verify the datetime can be a float
                    try:
                        float(decrypt_values['-Dec-Time'])

                    except:
                        decrypt_window['-Decrypt-Display'].update('The datetime value is incorrect. Please make sure the datetime is in timestamp format')
                        continue


                    
                    # If it passes all our tests, now we can make the temp file

                    dec_temp, dec_temp_path = tempfile.mkstemp()

                    try:
                        with os.fdopen(dec_temp, 'w') as tmp:
                            tmp.write(str(decrypt_values['-Dec-Message']) + '\n' + str(decrypt_values['-Dec-Key']) + '\n' + str(decrypt_values['-Dec-Time']))

                        decryption_object = enc.Decrypter(dec_temp_path, decrypt_values['Browse0'])

                        
                    finally:
                        os.remove(dec_temp_path)

                # Now we can begin the actual decryption

                descrambled = decryption_object.descramble_message()
                dec_alpha = decryption_object.create_decryption_alphabet()
                dec_message = decryption_object.decrypt_message(descrambled, dec_alpha)
                dec_out_success = 'The decrypted message was not sent to file'

                if dec_out_open:
                    decryption_object.output_original_message(dec_message)
                    dec_out_success = 'The decrypted message was successfully sent to a file!'

                decrypt_window['-Decrypt-Display'].update('Original Message:\n{0}\n{1}'.format(dec_message, dec_out_success))

                decryption_object = ''

    # End Decryption Window


    # About Me Window
    if main_event == 'About Me' and not about_window_active:
        about_window_active = True
        main_window.Hide()

        layout = create_layout('About')
        about_window = UI.Window('About Me', layout)

        while True:
            about_event, about_values = about_window.Read(timeout = 100)

            # Closes cleanly
            if about_event in (UI.WIN_CLOSED, 'Cancel'):
                about_window.Close()
                about_window_active = False
                main_window.UnHide()
                break

    # End About Me Window
import PySimpleGUI as UI
import encrypter as enc

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


# Additional layouts used in other layouts
out_layout_collapse = [
    [UI.Text('Select the folder to place the file into: '), UI.Push(), UI.FolderBrowse(key = '-Encrypt-Out')], # Hidden unless otherwise necessary
] # Encrypt

decfile_layout_collapse = [
    [UI.Text('Select the file to decrypt:'), UI.Push(), UI.FileBrowse(key = '-Decrypt-In')],
] # Decrypt

man_layout_collapse = [
    [UI.Text("Placeholder")], #
] # Decrypt

decout_layout_collapse = [
    [UI.Text('Select the folder to place the file into: '), UI.Push(), UI.FolderBrowse(key = '-Decrypt-Out')], # Hidden unless otherwise necessary
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

            [UI.Checkbox('Output the encrypted message to file?', enable_events = True, key = '-OPEN SelectOutCheck')], #
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
            [UI.Text("Placeholder")], #
        ]

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

            [UI.HorizontalSeparator()], #
            [UI.Text('Output: ')],
            [UI.Multiline('Waiting...', size = (60, 10))],

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

        while True:
            encrypt_event, encrypt_values = encrypt_window.Read(timeout = 100)

            # Closes cleanly
            if encrypt_event in (UI.WIN_CLOSED, 'Cancel'):
                encrypt_window.Close()
                encrypt_window_active = False
                main_window.UnHide()
                break
            
            # Event for selecting file output
            if encrypt_event.startswith('-OPEN SelectOut'):
                enc_open = not enc_open
                encrypt_window['-SelectOut-'].update(visible=enc_open)

            if encrypt_event in ('Encrypt Message'):

                try:

                    encrypt_values['-Encrypt-Message'].encode('ascii')

                    if not encrypt_values['-Encrypt-Message'].replace(' ','').isalpha():
                        raise Exception('Invalid Characters')

                except:
                    encrypt_window['-Encrypt-Display'].update('The message contains an invalid character. Please only use A-Z with no punctuation or special characters. Spaces are allowed.')
                    continue

                try:
                    encrypt_values['-Encrypt-Key'].encode('ascii')

                except:
                    encrypt_window['-Encrypt-Display'].update('The key has a non-ascii character. Please only use Ascii characters, including A-Z, upper and lower, digits, and symbols')

                    continue

                if enc_open == True:
                    encryption_object = enc.Encrypter(encrypt_values['Browse'], encrypt_values['-Encrypt-Message'], encrypt_values['-Encrypt-Key'])

                else:
                    encryption_object = enc.Encrypter(' ', encrypt_values['-Encrypt-Message'], encrypt_values['-Encrypt-Key'])

                #encrypt_window['-Encrypt-Display'].update(encryption_object.confirm()) # Verify output

                enc_alpha = encryption_object.create_encrypted_alphabet()
                enc_mess = encryption_object.encrypt_message(enc_alpha)
                enc_scram = encryption_object.scramble_message(enc_mess)

                if enc_open == True:
                    encryption_object.output_message(enc_scram)

                
                encrypt_window['-Encrypt-Display'].update('Message: {0}\nKey: {1}Timestamp: {2}'.format(enc_scram, encryption_object.get_encoded_key(), encryption_object.get_datetime()))

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
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
    [UI.Text('Select the folder to place the file into: '), UI.Push(), UI.FolderBrowse()], # Hidden unless otherwise necessary
]

decfile_layout_collapse = [
    [UI.Text('Select the file to decrypt:'), UI.Push(), UI.FileBrowse()],
]

man_layout_collapse = [
    [UI.Text("Placeholder")], #
]

# The other primary layouts that may use sub layouts above or be accessed through main
# Since we cannot reuse layouts for separate windows, we will recreate it using this function for cleanliness
def create_layout(layout):

    if(layout == 'Encryption'):

        # The layout for the encryption window
        encrypt_layout = [
            [UI.Text('Message to Encrypt: (A-Z, no punctuation or special characters)')], # 
            [UI.Push(), UI.InputText(), UI.Push(),], #
            [UI.Text('Encryption Key: (Min 4 characters, limited to Ascii, any characters)')], #
            [UI.Push(), UI.InputText(size = (35, None)), UI.Push()], #

            [UI.Checkbox('Output the encrypted message to file?', enable_events = True, key = '-OPEN SelectOutCheck')], #
            [collapse(out_layout_collapse, '-SelectOut-')], #

            # To Add:
            # Exit/Send Input Buttons
            # Input validation
            # Resizing
            # Output Window
            #
        ]

        return encrypt_layout

    # End Encryption

    elif(layout == 'Decryption'):

        # The layout for the decryption window
        decrypt_layout = [
            [UI.Checkbox('Decrypt from file?', enable_events = True, key = '-OPEN DecFileCheck')], #
            [collapse(decfile_layout_collapse, '-DecFile-')], #
            [UI.Checkbox('Decrypt manually?', enable_events = True, key = '-OPEN DecManCheck')], #
            [collapse(man_layout_collapse, '-ManIn-')], #
            [UI.Checkbox('Output the decrypted message to file?', enable_events = True, key = '-OPEN SelectOutCheck')], #
            [collapse(out_layout_collapse, '-SelectOut-')], #

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

            # To Add
            # Literally Everything

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

            if encrypt_event.startswith('-OPEN SelectOut'):
                enc_open = not enc_open
                encrypt_window['-SelectOut-'].update(visible=enc_open)
        
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
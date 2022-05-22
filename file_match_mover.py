import shutil
import os
import PySimpleGUI as sg

def ValidateInput(values, window):
    '''Returns tuple (success, extraction_type)'''
    global indx
    
    f_path = values[0] # input file name list
    i_path = values[1] # input folder
    o_path = values[2] # output folder
    ext_type = ''
    
    if len(f_path) == 0:
        sg.PopupError('No INPUT file selected!')
        return False, ext_type
    elif not os.path.exists(f_path):
        sg.PopupError('INPUT file does not exist!')
        return False, ext_type
    else: # must be an existing file then
        if not f_path.lower().endswith('.txt'):
            sg.PopupError('Input file is not a text file! ', f_path)
            return False, ext_type
        #else:
            #ext_type = Path(f_path).suffix[1:].lower()     

    if len(i_path) == 0:
        sg.PopupError('No Source folder selected!')
        return False, ext_type
    elif not os.path.exists(i_path):
        sg.PopupError('Source folder does not exist!')
        return False, ext_type
    elif os.path.isdir(i_path):
        ext_type = 'fs'
    else: # must be an existing file then
        sg.PopupError('Source folder does not exist!', i_path)
        return False, ext_type

    # check output now
    if len(o_path) == 0 : # output folder
        sg.PopupError('No OUTPUT folder selected!')
        return False, ext_type

    return True, ext_type

sg.theme('SystemDefault')   # Add a touch of color
# All the stuff inside your window.

layout = [  [sg.Text('File Match Mover', font=("Helvetica", 22))],
            [sg.Frame(layout=[
                    [sg.Input(size=(97,1)), 
                     sg.FileBrowse(button_text='Browse File', key='INPUTFILEBROWSE')
                    ]
                ],
                title='Select File Name List (txt):')],
            [sg.Frame(layout=[
                    [sg.Input(size=(97,1)), 
                     sg.FolderBrowse(button_text='Browse Folder', key='INPUTFOLDERBROWSE')
                    ]
                ],
                title='Select Source Folder:')],            
            [sg.Frame(layout=[
                    [sg.Input(size=(97,1)),
                     sg.FolderBrowse(button_text='Browse Folder')]
                ], 
                    title='Select Output Folder:')],            
            [sg.Submit('Start'), sg.Button('Cancel')] ]

# Create the Window
window = sg.Window('File Match Mover', layout)

file_list = ''
source_dir = ''
dest_dir = ''

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):   # if user closes window or clicks cancel
        break
    
    if event == 'Start':
        
        #check is selections made properly; if not we will return to input form without exiting app altogether
        is_valid, extracttype = ValidateInput(values, window)
        if is_valid:
            
            file_list = values[0]
            source_dir = values[1]
            dest_dir = values[2]
    
            # File system extractions can contain paths > 260 char, which causes problems
            # This fixes the problem by prefixing \\?\ on each windows path.
            
            if file_list[1] == ':' and extracttype =='fs': file_list = '\\\\?\\' + file_list.replace('/', '\\')
            if source_dir[1] == ':' and extracttype =='fs': source_dir = '\\\\?\\' + source_dir.replace('/', '\\')
            if dest_dir[1] == ':': dest_dir = '\\\\?\\' + dest_dir.replace('/', '\\')

            count = 0
            
            with open(file_list, 'r') as f:
                lines = [x.strip() for x in f.readlines()]
                    
                for root, dirs, files in os.walk(source_dir):
                    for name in files:
                        if name in lines:
                            shutil.move(root + '\\' + name, dest_dir)
                            count+=1
                            
            if count == 0:
                sg.popup_ok('Job Complete - No files matches found to move')
            else:
                out_text = 'Job Complete - ' + str(count) + ' files moved!\n\n' + 'Destination: ' + dest_dir.replace('\\\\?\\','')
                sg.popup_ok(out_text)

            #window.close()
import os
import pyperclip
import pyautogui
import wmi
import PySimpleGUI as sg
import json
import time

layout = [
    [sg.Text("Username", size=(10, 1)), sg.InputText(size=(30, 1), enable_events=True)],
    [sg.Text("Password", size=(10, 1)), sg.InputText(size=(30, 1), password_char='*')],
    [sg.Text("Elo", size=(10, 1)), sg.InputText(size=(30, 1))],
    [sg.Column([[sg.Button("Save"), sg.Button("Delete")]], justification='center')],
    [
        sg.Listbox(
            values=[], enable_events=True, size=(40, 20), key='-ACCOUNT LIST-'
        )
    ],
    [
        sg.Button("Login", size=(10, 2), enable_events=True)
    ],
    [sg.Text("The account you want to login:")],
    [sg.Text(size=(20, 1), key="-TOUT-")],
    [sg.Text('Folder'), sg.In(size=(25, 1), enable_events=True, key='-FOLDER-'), sg.FolderBrowse()]
]

# create Window
window = sg.Window(title="Auto Login", layout=layout, margins=(20, 20))

savedUsernames = []
usernameAndElo = []
password_dict = {}
selectedTuple = ()

# Open json File
with open('values.json', 'r') as openfile:
    # Reading from json file
    data = json.load(openfile)

for user in data:
    summonerName = user['user']
    password = user['password']
    rank = user['rank']

    savedUsernames.append(summonerName)
    usernameAndElo.append((summonerName, rank))
    password_dict[summonerName] = password

user = ""
password = ""
rank = ""

new_String = data

# create an event loop
while True:
    event, values = window.Read()
    if event == "Save":
        if values[0] == "" or values[1] == "":
            sg.popup("You need to enter a password or a Username, else your login won't work")
        elif values[0] in savedUsernames:
            sg.popup("The Username already exists in the list")
        elif values[2] == "" and values[0] != "" and values[1] != "":
            savedUsernames.append(values[0])
            user = values[0]
            password_dict[values[0]] = values[1]
            password = values[1]
            usernameAndElo.append((values[0], "No Rank specification"))
            rank = "No Rank specification"

            dictionary = {
                "user": user,
                "password": password,
                "rank": rank,
            }
            new_String.append(dictionary)
        else:
            savedUsernames.append(values[0])
            user = values[0]
            password_dict[values[0]] = values[1]
            password = values[1]
            usernameAndElo.append((values[0], values[2]))
            rank = values[2]

            dictionary = {
                "user": user,
                "password": password,
                "rank": rank,
            }
            new_String.append(dictionary)
        window["-ACCOUNT LIST-"].update(usernameAndElo)

    # Delete Element from the List
    if event == "Delete":
        pyautogui.PAUSE = 2.5
        if len(selectedTuple) != 0:
            if selectedTuple[0] in savedUsernames:
                dict_to_remove = {"user": selectedTuple[0], "password": password_dict[selectedTuple[0]],
                                  "rank": selectedTuple[1]}
                new_String.remove(dict_to_remove)
                del password_dict[selectedTuple[0]]
                usernameAndElo.remove(selectedTuple)
                savedUsernames.remove(selectedTuple[0])

        window["-ACCOUNT LIST-"].update(usernameAndElo)

    # Display selected Username
    if event == "-ACCOUNT LIST-":
        try:
            selectedTuple = values["-ACCOUNT LIST-"][0]
            window["-TOUT-"].update(selectedTuple[0])
        except IndexError:
            window["-ACCOUNT LIST-"].update(usernameAndElo)

    if event == "Login":
        if os.stat("leaguePath.txt").st_size == 0 and values["-FOLDER-"] == "":
            sg.popup("Please enter the Path to the League of Legends Exe")

        if values["-FOLDER-"] != "" and os.stat("leaguePath.txt").st_size == 0:
            filepath = values["-FOLDER-"] + "/League of Legends.lnk"
            f = open("leaguePath.txt", "w")
            if os.stat("leaguePath.txt").st_size == 0:
                f.write(filepath)

        if len(selectedTuple) != 0 and os.stat("leaguePath.txt").st_size != 0:
            filepath = open("leaguePath.txt", "r").read()
            selectedTuple = values["-ACCOUNT LIST-"][0]
            username = selectedTuple[0]
            pyperclip.copy(username)
            password = password_dict[username]
            os.startfile(filepath)
            f = wmi.WMI()
            flag = 0
            # Iterating through all the running processes
            for process in f.Win32_Process():
                if "RiotClientServices.exe" == process.Name:
                    flag = 1
                    time.sleep(1)
                    pyautogui.hotkey('ctrl', 'v')
                    pyautogui.hotkey('tab')
                    pyperclip.copy(password)
                    pyautogui.hotkey('ctrl', 'v')
                    pyperclip.copy("")
                    i = 0
                    while i < 6:
                        pyautogui.hotkey('tab')
                        i += 1
                    pyautogui.hotkey('enter')
                    break
    # End program if user closes window
    if event == sg.WIN_CLOSED:
        with open('values.json', 'w') as f:
            json.dump(new_String, f, indent=2)
        break
window.close()

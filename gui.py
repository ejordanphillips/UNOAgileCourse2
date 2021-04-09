
import json

import PySimpleGUI as psg
import requests


def fetch():
    response = requests.get("http://ejordanphillips.pythonanywhere.com/v1/all")
    data = response.json()
    todo = []
    todo.append("\n")
    for key, value in data.items():
        todo.append(key)
        for _, value in value.items():
            todo.append(str(value))
        todo.append('\n')
    data = ''.join(todo)
    return data


def refresh_all(window, data):
    try:
        window['-DATA-'].update(data)
        window['-ID-'].update('')
        window['-NAME-'].update('')
        window['-DESCRIPTION-'].update('')
        window['-DATE-'].update('')
        window['-IMPORTANCE-'].update('')
        return
    except Exception as err:
        raise Exception from err
    

def add(name, description, date, importance):
    response = requests.get(f'http://ejordanphillips.pythonanywhere.com/add?name={name}&description={description}&date={date}&input={input}')
    return

    
def update(id, name, description, date, importance):
    response = requests.get(f'http://ejordanphillips.pythonanywhere.com/update?id={id}&name={name}&description={description}&date={date}&input={input}')
    return


def delete(id):
    response = requests.get(f'http://ejordanphillips.pythonanywhere.com/delete?id={id}')
    return
    

def start_app():

    data = fetch()

    layout = [[psg.Text("Todo Items"), psg.Text(
        size=(12, 1), key='-DISPLAY-')],
        [psg.Text(data, key='-DATA-')],
        [psg.Text('ID', size=(12, 1)), psg.Input(key='-ID-')],
        [psg.Text('NAME', size=(12, 1)), psg.Input(key='-NAME-')],
        [psg.Text('DESCRIPTION', size=(12, 1)), psg.Input(key='-DESCRIPTION-')],
        [psg.Text('DATE', size=(12, 1)), psg.Input(key='-DATE-')],
        [psg.Text('IMPORTANCE', size=(12, 1)), psg.Input(key='-IMPORTANCE-')],
        [psg.Text('')],
        [psg.Button('Add'), psg.Button('Update'), psg.Button('Delete'), psg.Button('Exit')]  
    ]

    # Create a window
    window = psg.Window("Jordan's Todo App", layout)

    # Create an event loop
    while True:
        event, values = window.read()
        if event == "Exit" or event == psg.WIN_CLOSED:
            break
        if event == "Add":
            add(values['-NAME-'], values['-DESCRIPTION-'], values['-DATE-'], values['-IMPORTANCE-'])
        if event == "Update":
            update(values['-ID-'], values['-NAME-'], values['-DESCRIPTION-'], values['-DATE-'], values['-IMPORTANCE-'])
        if event == "Delete":
            delete(values['-ID-'])
        data = fetch()
        refresh_all(window, data)
    window.close()
    

if __name__ == "__main__":
    start_app()


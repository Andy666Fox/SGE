import PySimpleGUI as sg

def set_params_window():
    layout = [[sg.Text('                     MATRIX IMAGE')],
              [sg.Text('Enter path to file:'), sg.InputText()],
              [sg.Button('ENCODE'), sg.Button('DECODE')]]
    
    window = sg.Window('SGE', layout, (20,300))      
    

    event, values = window.read()    
    window.close()

    path = values[0]  
    size = values[1]
    
    if event[0]:
        window.close()
        
    return path, int(size)

set_params_window()
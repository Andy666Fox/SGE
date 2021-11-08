# Imports
import PySimpleGUI as sg
from deencode import  SGE


# Main window function
def set_params_window():
    
    """ Main GUI window function
    """
    
    layout = [[sg.Text('                       SGE')                      ],
              [sg.Text('Enter path to file:'), sg.InputText()             ],
              [sg.Button('ENCODE'), sg.Button('DECODE'), sg.Button('EXIT')]]
    
    window = sg.Window('SGE', layout, (20,300))      
    codec = SGE()
    
    while True:    
        event, values = window.read()  
        
        if event == sg.WIN_CLOSED or event == 'EXIT':
            break

        if event == 'ENCODE':
            sg.popup('Large files can take a long time to process,\n(up to 20 minutes). Be patient.')
            codec.encode(values[0])
            sg.popup('---Done!---')

        if event == 'DECODE':
            sg.popup('Large files can take a long time to process,\n(up to 20 minutes). Be patient.')
            codec.decode(values[0])  
            sg.popup('---Done!---')  

    window.close()


if __name__ == '__main__':
    set_params_window()
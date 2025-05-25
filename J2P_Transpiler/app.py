from tkinter import *
import shutil
import translator
import importlib
import time
from tkinter import filedialog
from io import StringIO
from contextlib import redirect_stdout

file = ""
dark_mode = True

# ==== Window Setup ====
window = Tk()
window.title("Java to Python Translator")
window.geometry("1100x750")
window.configure(bg='#1e1e1e')

# ==== Frames ====
left_frame = Frame(window, bg='#1e1e1e')
left_frame.grid(row=0, column=0, padx=10, pady=10, sticky=N)

right_frame = Frame(window, bg='#1e1e1e')
right_frame.grid(row=0, column=1, padx=10, pady=10, sticky=N)

# ==== Java Code Area ====
Label(left_frame, text='Java Code', fg='white', bg='#1e1e1e', font=('Arial', 12, 'bold')).pack()
javaScroll = Scrollbar(left_frame)
javaText = Text(left_frame, height=18, width=60, yscrollcommand=javaScroll.set,
                bg='#0f0f0f', fg='lime', insertbackground='white', font=('Consolas', 10))
javaText.insert(END, 'Enter ERROR-FREE Java code')
javaScroll.pack(side=RIGHT, fill=Y)
javaText.pack()

# ==== Python Code Area ====
Label(left_frame, text='Python Code', fg='white', bg='#1e1e1e', font=('Arial', 12, 'bold')).pack()
pythonScroll = Scrollbar(left_frame)
pythonText = Text(left_frame, height=18, width=60, yscrollcommand=pythonScroll.set,
                  bg='#0f0f0f', fg='cyan', insertbackground='white', font=('Consolas', 10))
pythonText.insert(END, 'PYTHON CODE')
pythonScroll.pack(side=RIGHT, fill=Y)
pythonText.pack()

# ==== Functions ====

def openFileToParse():
    try:
        filename = filedialog.askopenfile(title="Select File", filetypes=(("Java Files", "*.java"), ("Text Files", "*.txt")))
        file = filename.name
        f = open(file)
        javaText.delete("1.0", END)
        javaText.insert(END, f.read())
        resultsText.insert(END, f"You opened: {file}\n{'-'*40}\n")
    except Exception as e:
        resultsText.insert(END, "NO FILE SELECTED or ERROR\n" + str(e) + '\n' + '-'*40 + '\n')

def writeFile():
    text = javaText.get("1.0", END)
    with open("fileToParse.java", "w") as newFile:
        newFile.write(text)
    resultsText.insert(END, "Java Code saved as fileToParse.java\n" + '-'*40 + '\n')

def translateFile():
    pythonText.delete("1.0", END)
    newFile = open("translatedFile.py", "w")
    start_time = time.perf_counter()
    translator.main()
    end_time = time.perf_counter()
    total_time = round(end_time - start_time, 4)
    transarr = translator.transarr
    shutil.os.remove("fileToParse.java")

    number_indents = 0
    ignore_syntax = False
    for index, y in enumerate(transarr):
        if y.startswith('#'):
            ignore_syntax = True
        elif y == ':' and not ignore_syntax:
            number_indents += 1
        elif y == '\t' and not ignore_syntax:
            number_indents -= 1

        if index != 0 and transarr[index - 1] == '\n':
            if y != '\n':
                ignore_syntax = False
                line = '\t' * number_indents + y
                pythonText.insert(END, line)
                newFile.write(line)
        else:
            pythonText.insert(END, y)
            newFile.write(y)

    importlib.reload(translator)
    resultsText.insert(END, f"Translated to Python.\nTime taken: {total_time} sec\n{'-'*40}\n")
    newFile.close()

def runTransFile():
    tf = StringIO()
    try:
        import translatedFile
        with redirect_stdout(tf):
            importlib.reload(translatedFile)
        resultsText.insert(END, "Output of translated file:\n")
        resultsText.insert(END, tf.getvalue())
    except Exception as e:
        resultsText.insert(END, f"Error running translated file:\n{e}\n")
    resultsText.insert(END, '-'*40 + '\n')

def clearAll():
    javaText.delete("1.0", END)
    pythonText.delete("1.0", END)
    resultsText.delete("1.0", END)

def toggleTheme():
    global dark_mode
    dark_mode = not dark_mode

    bg_color = '#ffffff' if not dark_mode else '#1e1e1e'
    code_bg = '#ffffff' if not dark_mode else '#0f0f0f'
    fg_java = '#000000' if not dark_mode else 'lime'
    fg_py = '#000000' if not dark_mode else 'cyan'
    fg_txt = '#000000' if not dark_mode else 'white'

    window.configure(bg=bg_color)
    left_frame.configure(bg=bg_color)
    right_frame.configure(bg=bg_color)

    for widget in left_frame.winfo_children() + right_frame.winfo_children():
        if isinstance(widget, Label):
            widget.configure(bg=bg_color, fg='black' if not dark_mode else 'white')

    javaText.configure(bg=code_bg, fg=fg_java, insertbackground='black' if not dark_mode else 'white')
    pythonText.configure(bg=code_bg, fg=fg_py, insertbackground='black' if not dark_mode else 'white')
    resultsText.configure(bg=code_bg, fg=fg_txt, insertbackground='black' if not dark_mode else 'white')

# ==== Buttons ====
button_font = ('Arial', 10, 'bold')
button_params = {'width': 20, 'font': button_font, 'pady': 5}

Button(right_frame, text="OPEN FILE", command=openFileToParse, fg='white', bg='darkgreen', **button_params).pack()
Button(right_frame, text="WRITE FILE", command=writeFile, fg='white', bg='darkblue', **button_params).pack()
Button(right_frame, text="TRANSLATE", command=translateFile, fg='black', bg='gold', **button_params).pack()
Button(right_frame, text="RUN", command=runTransFile, fg='white', bg='crimson', **button_params).pack()
Button(right_frame, text="CLEAR ALL", command=clearAll, fg='black', bg='orange', **button_params).pack()
Button(right_frame, text="TOGGLE THEME", command=toggleTheme, fg='white', bg='purple', **button_params).pack()

# ==== Output Section ====
Label(right_frame, text='Translation Output', fg='white', bg='#1e1e1e', font=('Arial', 12, 'bold')).pack(pady=(10, 0))
resultsScroll = Scrollbar(right_frame)
resultsText = Text(right_frame, height=10, width=55, yscrollcommand=resultsScroll.set,
                   bg='#0f0f0f', fg='white', insertbackground='white', font=('Consolas', 10))
resultsScroll.pack(side=RIGHT, fill=Y)
resultsText.pack()

# ==== Main Loop ====
window.mainloop()

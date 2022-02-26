import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
try:
    import AppKit
    canBeep = True
except ModuleNotFoundError:
    canBeep = False
    print(canBeep)
#Globals
globalIndex = 0
currentWorkingFile = ""
class window:
    def __init__(self):
        #Simple init
        self.win = tk.Tk()
        self.win.geometry("700x780")
        self.win.title("vScript")
        #Create graphical elements
        loadButton = tk.Button(self.win,
                               height=5,
                               width=10,
                               text = "Open",
                               command=lambda: bendtofend.loadFile(self),
                               )
        self.textBox = tk.Text(self.win,
                             height=43,
                             width=98,
                             state="disabled")
        goStartB = tk.Button(self.win,
                               height=5,
                               width=10,
                               text = "Go To Start",
                               command=lambda: bendtofend.toStart(self),
                               )
        backTenB = tk.Button(self.win,
                               height=5,
                               width=10,
                               text = "Back 10",
                               command=lambda: bendtofend.backTen(self),
                               )
        upTenB = tk.Button(self.win,
                               height=5,
                               width=10,
                               text = "Up 10",
                               command=lambda: bendtofend.upTen(self),
                               )
        backHunB = tk.Button(self.win,
                               height=5,
                               width=10,
                               text = "Back 50",
                               command=lambda: bendtofend.backHun(self),
                               )
        upHunB = tk.Button(self.win,
                               height=5,
                               width=10,
                               text = "Up 50",
                               command=lambda: bendtofend.upHun(self),
                               )
        honk = tk.Button(self.win,
                         height=5,
                         width=10,
                         text="GoTo",
                         command=lambda: bendtofend.goto(self, int(simpledialog.askstring("GoTo", "Put in a page number"),)-1),
                         )
        upTenB.place(x=300, y=0)
        goStartB.place(x=100,y=0)
        backTenB.place(x=200,y=0)
        backHunB.place(x=400,y=0)
        upHunB.place(x=500, y=0)
        honk.place(x=600, y=0)
        self.textBox.place(x=0,y=100)
        loadButton.place(x=0, y=0)
    def loop(self, iHateTkinter):
        self.win.mainloop()
class scriptBox:
    def __init__(self, window):
        self.text = window.textBox
    def insert(window, text):
        window.textBox.config(state='normal')
        window.textBox.delete("1.0",tk.END)
        if len(text) != 0:
                    window.textBox.insert(tk.INSERT, text)
        else:
            window.textBox.insert(tk.INSERT, "End of Resource. Click Go To Start to return to the beginning\n")
        window.textBox.insert(tk.INSERT, "CURRENT PAGE: " + str(globalIndex) + ". READING FROM BUFFER")
        window.textBox.config(state='disabled')
class bendtofend:
    def loadFile(window):
        global globalIndex
        globalIndex = 0
        currentWorkingFile = fileManager.getFileObject()
        buffer.write(currentWorkingFile.read())
        indexText = fileManager.getLineIndex(buffer.get(), globalIndex)
        scriptBox.insert(window, indexText)
    def toStart(window):
        global globalIndex
        globalIndex = -1
        bendtofend.foward(window)
    def backTen(window):
        global globalIndex
        if globalIndex-10 > 0:
            globalIndex = globalIndex - 11
            bendtofend.foward(window)
        else:
            globalIndex = -1
            bendtofend.foward(window)
    def upHun(window):
        global globalIndex
        globalIndex = globalIndex + 49
        print(globalIndex)
        bendtofend.foward(window)
    def backHun(window):
        global globalIndex
        if globalIndex-50 > 0:
            globalIndex = globalIndex - 49
            bendtofend.foward(window)
        else:
            globalIndex = -1
            bendtofend.foward(window)
    def upTen(window):
        global globalIndex
        globalIndex = globalIndex + 9
        bendtofend.foward(window)
    def foward(window):
        global globalIndex
        globalIndex += 1
        #print(str(len(currentWo.readline())) + "length")
        indexText = fileManager.getLineIndex(buffer.get(), globalIndex)
        scriptBox.insert(window, indexText)
        print("returned")
    def backward(window):
        global globalIndex
        if globalIndex > 0:
            globalIndex -= 1
        indexText = fileManager.getLineIndex(buffer.get(), globalIndex)
        scriptBox.insert(window, indexText)
    def goto(window, givenInt):
        if type(givenInt) == type(1):
            global globalIndex
            globalIndex = givenInt
            bendtofend.foward(window)
        else:
            messagebox.showerror("Error", "Not a valid page number")
    def honk():
        if canBeep == True:
            AppKit.NSBeep()
class buffer:
    def write(text):
        with open("buffer.txt", "w") as f: f.write(text)
        f.close()
    def get():
        return open("buffer.txt", "r")
class fileManager:
    def getFileObject():
        a = filedialog.askopenfile(mode="r")
        return a
    def getLineIndex(fileObject, index, until=42):
        print(index)
        i=0 #Init
        finalString = ""
        breakIndex = False
        breakIndexCount = 0
        for text in fileObject.readlines():
            if not breakIndex:
                breakIndexCount += 1
                if breakIndexCount > until*index: #times of breaking
                    breakIndex = True
                    i += 1
            if breakIndex: #break index
                #print("unpassed - " + finalString)
                finalString = finalString + text #append
                if i < until: i += 1 #break text requirement
                else:
                    break
        return finalString
if __name__ == "__main__":
    win = window()
    win.win.bind('<Return>', lambda e: bendtofend.foward(win))
    win.win.bind('<space>', lambda e: bendtofend.foward(win))
    win.win.bind('<Right>', lambda e: bendtofend.foward(win))
    win.win.bind('<Left>', lambda e: bendtofend.backward(win))
    #in.win.bind('e', lambda e: print(currentWorkingFile.readlines()))
    win.loop(win)
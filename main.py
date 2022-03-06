import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
import pickle
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
                               text = "GoTo Start",
                               command=lambda: bendtofend.toStart(self),
                               )
        backTenB = tk.Button(self.win,
                               height=5,
                               width=10,
                               text = "Back10",
                               command=lambda: bendtofend.backTen(self),
                               )
        upTenB = tk.Button(self.win,
                               height=5,
                               width=10,
                               text = "Up10",
                               command=lambda: bendtofend.upTen(self),
                               )
        backHunB = tk.Button(self.win,
                               height=5,
                               width=10,
                               text = "Bind",
                               command=lambda: bendtofend.bind(self),
                               )
        gotoB = tk.Button(self.win,
                         height=5,
                         width=10,
                         text="GoTo",
                         command=lambda: bendtofend.goto(self, int(simpledialog.askstring("GoTo", "Put in a page number"),)-1),
                         )
        clrBindB = tk.Button(self.win,
                             height=5,
                             width=10,
                             text="EditBind",
                             command= lambda: bendtofend.editBind(self))
        upTenB.place(x=300, y=0)
        goStartB.place(x=100,y=0)
        backTenB.place(x=200,y=0)
        backHunB.place(x=400,y=0)
        clrBindB.place(x=500,y=0)
        gotoB.place(x=600, y=0)
        self.textBox.place(x=0,y=100)
        loadButton.place(x=0, y=0)
    def loop(self, iHateTkinter):
        self.win.mainloop()
class scriptBox:
    def __init__(self, window):
        self.text = window.textBox
    def insert(window, text):
        window.textBox.config(state='normal') #Set state to editable
        window.textBox.delete("1.0",tk.END)
        if len(text) != 0:
                    window.textBox.insert(tk.INSERT, text) #If there is text
        else: #Send blank pages
            asciiArt = """\n ______           _        __ _____           _       _   
|  ____|         | |      / _/ ____|         (_)     | |  
| |__   _ __   __| | ___ | || (___   ___ _ __ _ _ __ | |_ 
|  __| | '_ \ / _` |/ _ \|  _\___ \ / __| '__| | '_ \| __|
| |____| | | | (_| | (_) | | ____) | (__| |  | | |_) | |_ 
|______|_| |_|\__,_|\___/|_||_____/ \___|_|  |_| .__/ \__|
                                               | |        
                                               |_|     """
            window.textBox.insert(tk.INSERT, asciiArt+ "\nClick Go To Start to return to the beginning\n")
        window.textBox.insert(tk.INSERT, "CURRENT PAGE: " + str(globalIndex) + ". READING FROM BUFFER")
        window.textBox.config(state='disabled')
class dataObj:
    def write(key, page):
        finalData = pickle.load(open("profile.p", "rb"))
        finalData.append([key, page])
        pickle.dump(finalData, open("profile.p", "wb"))
    def get():
        return pickle.load(open("profile.p", "rb"))
    def clr():
        open("profile.p", "wb")
        data = []
        pickle.dump(data, open("profile.p", "wb"))
    def delete(index):
            data = pickle.load(open("profile.p", "rb"))
            newList = []
            i = 0
            for items in data:
                if i == index[0]:
                    pass#Add if is at same point in index
                else:
                    newList.append(items)
                i += 1
            pickle.dump(newList, open("profile.p", "wb"))
class bendtofend:
    def deleteBindMini(ls):
        dataObj.delete(ls.curselection())
        ls.delete(ls.curselection())
    def addBindMini(graphical, smallWin):
        bendtofend.bind(graphical)
        smallWin.destroy() #recursive?
        bendtofend.editBind(graphical)
    def editBind(graphical):
        smallWin = tk.Tk()
        smallWin.geometry("200x200")
        smallWin.title("Edit Bindings")
        ls = tk.Listbox(smallWin, height=9, width=22)
        delB = tk.Button(smallWin, height=2, width=6, text="Del", command = lambda: bendtofend.deleteBindMini(ls))
        addB = tk.Button(smallWin, height=2, width=6, text="Add", command = lambda: bendtofend.addBindMini(graphical, smallWin))
        userProfile = dataObj.get()
        for data in userProfile:
            print(data)
            formattedString = "Key(s)" + data[0] + " | Pg. " + str(data[1])
            print(formattedString)
            ls.insert(0, formattedString)
        ls.place(x=0,y=0)
        delB.place(x=0,y=160)
        addB.place(x=60,y=160)
        smallWin.mainloop()
    def loadFile(window):
        global globalIndex
        globalIndex = 0
        currentWorkingFile = fileManager.getdataObject()
        #dName, f = currentWorkingFile.read().split("^&*")
        try:
            buffer.write(currentWorkingFile.read())
            indexText = fileManager.getLineIndex(buffer.get(), globalIndex)
            window.win.title("vScript: " + currentWorkingFile.name)
            scriptBox.insert(window, indexText)
        except AttributeError:
            pass #Fail silently, no file selected
    def bind(window):
        noError = True #Checksum
        keypress = simpledialog.askstring("Bind", "Put in a number (Ex: 1, 34, 89)")
        pageNum = int(simpledialog.askstring("Bind", "Put in a page number (Ex: 124)"))
        try:
            int(keypress)#Not a vaid keypress if eval str
        except:
            messagebox.showerror("Error", "Invalid keypress: " + keypress)
            noError = False
        if noError:
            dataObj.write(keypress, pageNum)
            #messagebox.showinfo("Sucess!", "Restart program for bindings to apply")
            win.win.bind(keypress, lambda e: bendtofend.goto(window, pageNum-1)) #Apply binding
    def toStart(window):
        global globalIndex
        global pastIndex
        pastIndex = globalIndex
        globalIndex = -1
        bendtofend.foward(window)
    def backTen(window):
        global globalIndex
        global pastIndex
        pastIndex = globalIndex
        print(pastIndex)
        if globalIndex-10 > 0:
            globalIndex = globalIndex - 11
            bendtofend.foward(window)
        else:
            globalIndex = -1
            bendtofend.foward(window)
        print(globalIndex)
    def upHun(window):
        global globalIndex
        global pastIndex
        pastIndex = globalIndex
        globalIndex = globalIndex + 49
        bendtofend.foward(window)
    def backHun(window):
        global globalIndex
        global pastIndex
        pastIndex = globalIndex
        if globalIndex-50 > 0:
            globalIndex = globalIndex - 49
            bendtofend.foward(window)
        else:
            globalIndex = -1
            bendtofend.foward(window)
    def upTen(window):
        global globalIndex
        global pastIndex
        pastIndex = globalIndex
        globalIndex = globalIndex + 9
        bendtofend.foward(window)
    def foward(window):
        global globalIndex
        global pastIndex
        pastIndex = globalIndex
        globalIndex += 1
        indexText = fileManager.getLineIndex(buffer.get(), globalIndex)
        scriptBox.insert(window, indexText)
    def backward(window):
        global globalIndex
        global pastIndex
        pastIndex = globalIndex
        if globalIndex > 0:
            globalIndex -= 1
        indexText = fileManager.getLineIndex(buffer.get(), globalIndex)
        scriptBox.insert(window, indexText)
    def goto(window, givenInt):
        print(givenInt)
        if type(givenInt) == type(1):
            global globalIndex
            #global pastIndex
            #pastIndex = globalIndex
            globalIndex = givenInt
            bendtofend.foward(window)
        else:
            messagebox.showerror("Error", "Not a valid page number")
class buffer:
    def write(text):
        with open("buffer.txt", "w") as f: f.write(text)
        f.close()
    def get():
        return open("buffer.txt", "r")
class fileManager:
    def getdataObject():
        filetypes = (
            ('vScript File', '*.vsc'),
            ('All files', '*.*')
        )
        a = filedialog.askopenfile(mode="r",  filetypes=filetypes)
        return a
    def getLineIndex(dataObject, index, until=42):
        i=0 #Init
        finalString = ""
        breakIndex = False
        breakIndexCount = 0
        for text in dataObject.readlines():
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
    win.win.bind('u', lambda e: bendtofend.goto(win, pastIndex-1))
    win.win.bind('<space>', lambda e: bendtofend.foward(win))
    win.win.bind('<Right>', lambda e: bendtofend.foward(win))
    win.win.bind('<Left>', lambda e: bendtofend.backward(win))
    win.win.bind('g', lambda e: bendtofend.goto(win, int(simpledialog.askstring("GoTo", "Put in a page number"),)-1))
    userProfile = dataObj.get()
    for data in userProfile:
        print(data[0] + "|" + str(data[1]))
        win.win.bind(data[0], lambda e: bendtofend.goto(win, data[1]-1))
    #in.win.bind('e', lambda e: print(currentWorkingFile.readlines()))
    win.loop(win)

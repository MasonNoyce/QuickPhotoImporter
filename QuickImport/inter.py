import os
import sys
import time
import threading
from tkinter import *
from tkinter.ttk import Progressbar as pb
from tkinter import _setit as st
from tkinter import filedialog as fd
from tkinter import messagebox as tmb
#from PIL import ImageTk, Image
import qi
#import cv2
finFiles = 0
tFiles = 0

lock = threading.Lock()

class Application(Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.protocol('WM_DELETE_WINDOW', self.close_app)
        self.pack()
        self.create_widgets()
        self.appOpened = True
        
    def close_app(self):
        if tmb.askokcancel("Close", "Are you sure you want to Exit"):
           self.destroy()
           qi.tkwindow = False
           self.appOpened=False
           self.master.quit()
           self.master.destroy()
           sys.exit()

    def create_widgets(self):
        global finFiles
        global tFiles




        self.importSelectorFrame = Frame(self.master)
        self.importSelectorFrame.pack(side = 'top')


        self.createNewFrame = Frame(self.master)
        self.createNewFrame.pack(side = 'top')

        self.LabelFrame = Frame(self.createNewFrame)
        self.LabelFrame.pack(side = 'left')

        self.progressBarFrame = Frame(self.master)
        self.progressBarFrame.pack(side = 'bottom')




        self.importSelect = Button(self.importSelectorFrame, text="Select Import Directory", fg="green")
        self.importSelect.pack(side="left")
        self.importSelect["command"] = self.selectImport

        self.outSelect = Button(self.importSelectorFrame, text="Select Output Directory", fg="blue")
        self.outSelect["command"] = self.selectOut
        self.outSelect.pack(side="left")
       
        self.picType = StringVar(self.master)
        self.picType.set(genChoices[0])
        self.optMenu = OptionMenu(self.importSelectorFrame,self.picType, *genChoices)
        self.optMenu.pack(side = 'left')
       
        self.importRun = Button(self.importSelectorFrame, text="RunImporter", fg="black")
        self.importRun["command"] = self.runImport
        self.importRun.pack(side="left")
        
        self.nopL = Label(self.LabelFrame, text="New Option").grid(row=0)
        self.nopL2 = Label(self.LabelFrame, text="New Folder").grid(row=1)
        self.newOptext = Entry(self.LabelFrame)
        self.newOptext.grid(row = 0,column=1)
        self.newOptext2 = Entry(self.LabelFrame)
        self.newOptext2.grid(row= 1,column =1) 


        
        self.makeNew = Button(self.createNewFrame, text="Create New Option", fg="black")
        self.makeNew["command"] = self.makeNewOps
        self.makeNew.pack(side="left")        
        
        self.newCreatedText = Text(self.createNewFrame,height=2, width = 30)
        self.newCreatedText.pack(side='left')
        self.newCreatedText.insert(END,"No Option")
       
        self.progress = pb(self.progressBarFrame,orient=HORIZONTAL,length=560,mode='determinate')
        self.progress.pack(side='bottom')
        #self.progress['value'] = finFiles

       

        

 
    def selectImport(self):
        global tFiles
        tmp = fd.askdirectory()
        qi.sroot = tmp
        
        for root, dirs, files in os.walk(tmp):
            tFiles = len(files)
            qi.totalFiles = len(files)
        print(tFiles,len(files))
        self.progress['maximum'] = tFiles

    def selectOut(self):
        qi.tmpout = fd.askdirectory()        
        
    def runImport(self):
        global finFiles
        start = time.time()
        qi.picType = self.picType.get()
#        thread1 = threading.Thread(target=self.progressBar)
        thread2 = threading.Thread(target=qi.quickImport)
#        thread1.start()
        thread2.start()
#        time.wait(1)
        self.progressBar()
#        thread1.join()
        thread2.join()
        print("threadJoined")
#        time.wait(199)
        print("FINIDDDDDD")
        print("outside ", qi.finFiles)
#        self.progressBar()
#        qi.quickImport()
        

    
    def makeNewOps(self):
        global genChoices
        if self.newOptext.get() == "" and self.newOptext2.get() == "":
            self.newCreatedText.delete('1.0',END)
            self.newCreatedText.insert(END,"Please Enter A New Option Key\n And New Folder") 
            print("Please enter a new Option key and New Folder")
            return
            
        if self.newOptext.get() == "":
            self.newCreatedText.delete('1.0',END)
            self.newCreatedText.insert(END,"Please Enter A New Option Key\n And New Folder") 
            print("Please enter a new Option key")        
            return
            
        if self.newOptext2.get() == "":
            self.newCreatedText.delete('1.0',END)
            self.newCreatedText.insert(END,"Please Enter A New Folder") 
            print("Please enter a new Option key")        
            return
                
        else:
            nopt = self.newOptext.get()
            nopt2 = self.newOptext2.get()
            

            print("trying to open options file")
            try:
                tmpf = open("options.txt",'a+')
                tmpf.write(nopt + '\n')
                tmpf.write(nopt2 + '\n')
                tmpf.close()
                genChoices.append(nopt)
                self.newCreatedText.delete('1.0',END)
                self.newCreatedText.insert(END,"New Option Created") 
                self.picType.set('')
                self.optMenu['menu'].delete('0',END)
                for i in genChoices:
                    self.optMenu['menu'].add_command(label=i, command=st(self.picType,i))
                self.picType.set(nopt)
                print(nopt)
                print(nopt2)
                qi.makeSwitch()
            except IOError:
                print("ErrorReadingFile")
                
            return
        


        
    def runExampleDS(self):
        na.runExample('DS')

    def progressBar(self):
        time.sleep(5)

        def pb():
#            lock.acquire()
            tf = qi.totalWorkers
#            lock.release()
            self.progress['maximum'] = tf
            ff = 0
            count = 0
            ncw=qi.numcWorkers
            failed = 20
            fo = 0
            if self.appOpened:
                while  ff <= tf:
                    print(tf)    
                    print(ff)
    #                lock.acquire()
                    ff = qi.finWorkers
    #                lock.release()
                    self.progress['value'] = ff
                    self.progress.update()
                    if not self.appOpened:
                        break
                    time.sleep(1)

        if self.appOpened:
            t = threading.Thread(target=pb).start()

            t.join()
#            progressbar.step(currentValue)
#            progressbar.update()
        

 #           self.btn['state']='normal'




        
    def quitt(self):
        na.quit = True
        self.master.destroy


#DSImage = cv2.imread("NoText.jpg")
#TSImage = cv2.imread("NoText.jpg")
#NImage = cv2.imread("NoText.jpg")
#ExFile = "NoText.jpg"
#oldExFile = "NoText.jpg"
genChoices = []
try:
    print("trying to open File options for Interface")
    with open('options.txt','r') as opsf:
        line = opsf.readline()
        line = line.rstrip('\n')
        line2 = opsf.readline()
        line2 = line2.rstrip('\n')

        while line2:
            genChoices.append(line)
            line = opsf.readline()
            line2 = opsf.readline()
            line = line.rstrip('\n')
            line2 = line2.rstrip('\n')
    print("IDIDIT :)")

            
except FileNotFoundError:
    print("List Of Options Not found")
    print("Create a txt file labeled: options.txt")
    print("to create an option, make the label, followed by enter")
    print("Then create the folder Name")
    print("Using Defaults for Now")
    genChoices = ['DS','Stage','PRs','Overview','Celebration']


#exitFrame = Frame(root)
#exitFrame.pack( side = 'top')



sroot = ""
tmpout = ""

if __name__ =='__main__':
    root = Tk()
    app = Application(master=root)   
    app.mainloop()


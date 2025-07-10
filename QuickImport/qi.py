import inter
import time
import os
import shutil
from shutil import copyfile
import threading
from PIL import Image,ExifTags


sroot = ""
tmpout = ""
picType ="DSTS"
numWorkers = 10
defaults = False
tkwindow = True

ops = []
switch=None
totalFiles = 0
finFiles = 0
numWorkersInit = 10
numcWorkers = 5
numcWorkersInit = 5
totalWorkers = 0
finWorkers = 0

lock = threading.Lock()

try:
    print("trying to open File options")
    with open('options.txt','r') as opsf:
        line = opsf.readline()
        line = line.rstrip('\n')
        line2 = opsf.readline()
        line2 = line2.rstrip('\n')


        while line2:
            ops.append((line,line2))        
            line = opsf.readline()
            line2 = opsf.readline()
            line = line.rstrip('\n')
            line2 = line2.rstrip('\n')

    switch = None
    switch = dict(ops)
    print("Switch: " , switch)
            
except FileNotFoundError:
    print("List Of Options Not found")
    print("Create a txt file labeled: options.txt")
    print("to create an option, make the label, followed by enter")
    print("Then create the folder Name")
    print("Using Defaults for Now")
    defaults = True






def makeSwitch():
    global switch
    try:
        print("trying to open File options")
        with open('options.txt','r') as opsf:
            line = opsf.readline()
            line = line.rstrip('\n')
            line2 = opsf.readline()
            line2 = line2.rstrip('\n')


            while line2:
                ops.append((line,line2))        
                line = opsf.readline()
                line2 = opsf.readline()
                line = line.rstrip('\n')
                line2 = line2.rstrip('\n')

        switch = None
        switch = dict(ops)
        print("Switch: " , switch)
            
    except FileNotFoundError:
        print("List Of Options Not found")
        print("Create a txt file labeled: options.txt")
        print("to create an option, make the label, followed by enter")
        print("Then create the folder Name")
        print("Using Defaults for Now")
        defaults = True

for i in ops:
    print(i)



def switchS(picType):
    global switch
    if defaults == True:
        switcher ={
        "DS":"02 - DS",
        "Stage":"01 - Stage",
        "PRs":"00 - PRs",
        "Overview":"00 - Overview",
        "Celebration":"00 - Celebration",
        }
        return switcher[picType]

    else:
        return switch[picType]


def quickImport():
    global totalFiles
    global numWorkers
    global finFiles
    global numWorkersInit
    global numcWorkers
    global numcWorkersInit
    global totalWorkers
    global finWorkers
    global twindow
    
    print("Hello World: " , picType)
    print(switchS(picType))
    st = switchS(picType)
    tmpd = tmpout + '/'+ st


    try:
        os.mkdir(tmpd)
        print("Directory Created")
        print(tmpd)
    except FileExistsError:
        print("Directory already there")
        
    try:
        os.mkdir(tmpd + "/Raw")
        print("Directory Created")
    except FileExistsError:
        print("Directory already there")


        
    try:
        print("trying to open File")
        f = open(tmpd  + '/tn'+picType+'.txt', 'r')
        print("File Found")
        var = f.read()     
        f.close
        f= open(tmpd  + '/tn'+picType+'.txt', 'w+')
        index = int(var[0]) + 1
        f.write(str(index))
        f.close()
    except FileNotFoundError:
        f = open(tmpd + '/tn'+picType+'.txt', 'w+')
        f.write('0')
        index = 0
        f.close()
    
    count = 0
    countR = 0
    

    
    workerC = 0
    totalFiles = 0
    finFiles = 0
    isRaw = False
    


    for root, dirs, files in os.walk(sroot):
        totalFiles = len(files)
        print(totalFiles)
#        while finFiles < totalFiles:
        threads = chuncker(numWorkers,totalFiles,files,root,index,tmpd)
        print(len(threads))
        finWorkers = 0
        totalWorkers = len(threads)
        if tkwindow:
            while finWorkers < totalWorkers:
                if (totalWorkers - finWorkers - numcWorkers) < 1:  
                    numcWorkers = totalWorkers - finWorkers

                for worker in threads[finWorkers:finWorkers+numcWorkers]:
                    print("startingWorker")
                    worker.start()
    #                time.sleep(1)

                
                for worker in threads[finWorkers:finWorkers+numcWorkers]:
                    print("attempting to join worker")
                    try:
                        worker.join()
                        print("worker Joined")
                        print(tkwindow)
                        finWorkers = finWorkers + 1 
                    except:
                        print("couldn't join worker")
                print(finWorkers)
                if not tkwindow:
                    finWorkers = totalWorkers
                
    time.sleep(1)
    totalFiles = 0
    finFiles = 0
    numWorkers = numWorkersInit
    numcWorkers = numcWorkersInit
    print("Finnished Exporting: " + tmpd)


def chuncker(nw,nf,f,r,i,t):

    finFiles = 0
    cs = []
    cb = []
    threads = []
    while finFiles < nf:
        if (nf - finFiles - nw) < 1:
                nw = nf - finFiles    
                print("FILE STUFF Last Workers: " ,nf,finFiles, nw)


        a = []
        b = []

        for fl in f[finFiles:finFiles+nw]:
            isRaw = False
            if fl.endswith('.dng') or fl.endswith('.DNG') or fl.endswith('.nef') or fl.endswith('.NEF'):
                isRaw = True
                a.append(fl)            
                
            else:
                a.append(fl)
            finFiles = finFiles + 1
                
    
        cb.append(a)

#        print("cb: ", cb)
        threads.append(threadName(cb,i,r,t,isRaw))

#        print(threads)
        
    return threads
            
 #   for root, dirs, files in os.walk(sroot):
 #       for file_ in files:
 
def threadName(cb,i,root,tmpd,isRaw):

    package = []



    for files in cb:
#        print("files: ",files)
        pack = []    
        for f in files:
#            print("file: " ,f)
            ti = i
            tr = root
            td = tmpd
            tis = isRaw
            pack.append([ti,tr,td,tis,f])
#            print("pack: " , pack)

        thread = threading.Thread(target=reName,args=(pack))  
        #print(pack)

        #    c,cR = reName(file_,cr,c,i,root,tmpd)

    return thread

def reName(*pack):
#    print("Rename: " ,pack)
    
#    z = zeroReturn(c, f,i)
#    lock = threading.Lock()



    if inter:#    for pack in package:
        for p in pack:

                i = p[0]
                root = p[1]
                tmpd = p[2]
                isRaw = p[3]
                f = p[4]
#                print("pack: ",i,root,tmpd,isRaw,f, " ::: ")

                filepath = root + "/" + f

                try:
                    image = Image.open(filepath)
                    for orientation in ExifTags.TAGS.keys():
                        if ExifTags.TAGS[orientation]=='Orientation':
                            break
                    exif=dict(image._getexif().items())

                    if exif[orientation] == 3:
                        image=image.rotate(180, expand=True)
                    elif exif[orientation] == 6:
                        image=image.rotate(270, expand=True)
                    elif exif[orientation] == 8:
                        image=image.rotate(90, expand=True)
                    image.save(filepath)
                    image.close()        
                except(AttributeError, KeyError,IndexError):
                    pass




#            for f in files:

                tmp = f        
                
                ##Grabs file extension
                fileExt = f[-4:]

                tmpf = ''.join([i for i in tmp if i.isdigit()])
            
                z = tmpf + str(fileExt)
                zz = list(z)
                zz[0] = str(i)
                z = "".join(zz)
            
                if z.endswith('.dng') or z.endswith('.DNG') or z.endswith('.nef') or z.endswith('.NEF'):
#                    print("copying Raw: " + z)

                    try:
#                            outf = open( tmpd+'/Raw/'+ z)
#                            inf = open(root +'/'+ str(f))
                        lock.acquire()
                        copyfile(root+'/'+str(f),tmpd+'/Raw/'+z)
                        lock.release()
 #                       finally:
 #                           if outf:
 #                               outf.close()
 #                           if inf:
 #                               inf.close()
                            
                    except(shutil.Error, OSError,IOError):
                        print("failed copying file")

                else:
#                    print("Copying reg: " + z)
                    lock.acquire()
                    copyfile(root +'/'+ str(f),tmpd+'/'+ z)
                    lock.release()
    




#def zeroReturn(c,f,i):
#    a = f[-4:]
#    print(a)
#    if c < 10:
#        return str(i) + '00' + str(c) + "_toRemove" + a
#    if c > 9 and c <100:
#        return str(i) + '0' + str(c) + "_toRemove" + a
#    if c > 99:
#        return str(i) + str(c) + "_toRemove" + a

    
    







import os
import cv2

	
sroot = input("drag over a directory with pictures you want to scale: ")

#sroot = input("enter folder location: ")
s = .25#input("enter scale: ")

print(sroot)

try:
	os.mkdir(sroot + "/scaled")
	print(sroot + "/scaled was created")
except FileExistsError:
	print("folder already there")
	
for root, dirs, files in os.walk(sroot):
    #		print(hello)
	for file_ in files:
		print( os.path.join(root, file_) )
    #Create for loop here to end of folder


		img = cv2.imread( sroot + "/" + file_)
#cv2.imshow("",img)
#cv2.waitKey(0)
		h,w,c = img.shape
		img = cv2.resize(img, (int(w*s), int(h*s))) 
		cv2.imwrite(sroot+"/scaled/" + file_, img)
		



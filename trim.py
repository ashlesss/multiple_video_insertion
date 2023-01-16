# General version

import os,glob
import sys, time

filelist = []
main_path = os.getcwd()

def getfilename():
    for filename in os.listdir(main_path):
        if (filename.endswith(".mp4")): #or .avi, .mpeg, whatever.
            filelist.append(filename)
            #print(filename)
        else:
            continue
    print("Get target file successful, starting!")
    time.sleep(3)

def trim(usercmd):
    if (usercmd == ""):
        print("No starting timestamp enter, quitting")
        quit()
    else:
        prcname = filelist[0]
        os.system("ffmpeg -sseof -" + usercmd[0] + " -i " + prcname + " -c copy " + usercmd[1] + "\\" + prcname + "".format(prcname))
        print("Videos trimmed successfully, open file directory in 5 seconds")
        print(prcname + " has been stored to " + usercmd[1])
        time.sleep(5)
        os.startfile(usercmd[1])
        #print("ffmpeg -sseof -" + usercmd[0] + " -i " + prcname + " -c copy " + usercmd[1] + "\\" + prcname)

if __name__ == "__main__":
    usercmd = sys.argv[1:]
    getfilename()
    # usercmd = "00:23:23"
    trim(usercmd)
    # path = r"C:\user"
    # path1 = "\\\\".join(path.split("\\"))
    # print(path1)
    #04:25:01

# /* cSpell:disable */

import os, time
import shutil, glob
import subprocess, re
###### Rerender container

gb_path = os.getcwd()
# work_path = os.getcwd()
# processed_dir = work_path + "\\processed\\"

def start():
    for folder in os.listdir(gb_path):
        # print(type(folder))
        wpath = gb_path + "\\" + folder + "\\"
        # print(wpath)
        if (os.path.isdir(wpath)):
            vids = check(wpath)
            if ( vids != 0 and vids > 1 ):
                prc_dir = init_job(wpath)
                rerender(wpath, prc_dir, vids)
                creat_meg(prc_dir)
                insertvid(wpath, prc_dir)
                cleaner(prc_dir)
            elif (vids == 1):
                prc_dir = init_job(wpath)
                rerender(wpath, prc_dir, vids)
                cleaner(prc_dir)
            else:
                print("\033[1;31m No video src detected, quitting.")
                quit()
        else:
            print("\033[1;31m No Folder found! END process!")
            quit()


def check(wpath):
    videos = 0
    for filename in os.listdir(wpath):
        if (filename.endswith(".ts")):
            videos += 1
        else:
            continue
    if (videos == 0):
        print("\033[1;31m No MP4 files in the working directory, quitting ")
        return 0
    else:
        print("\033[1;32m " + str(videos) + " ts files detected, Starting. Curr directory: " + wpath)
        return videos


def init_job(wpath):
    prc_dir = wpath + "prc\\"
    if os.path.exists(prc_dir):
        print("\033[1;33m History cache detected, cleaning.")
        shutil.rmtree(prc_dir)
        os.makedirs(prc_dir)
        print('\033[1;32m "prc" folder created successfully!')
        print("\033[1;32m Videos processing will start after 5 seconds.")
    else:
        os.makedirs(prc_dir)
        print('\033[1;32m "prc" folder created successfully!')
        print("\033[1;32m Videos processing will start after 5 seconds.")
    time.sleep(5)
    return prc_dir


def rerender(wpath, prc_dir, vids):
    if (vids == 1):
        for filename in os.listdir(wpath):
            if (filename.endswith(".ts")): #or .avi, .mpeg, whatever.
                os.system("ffmpeg -i " + wpath + filename + " -c copy " + wpath + filename[:-12] + ".mp4")
                # print("ffmpeg -i " + wpath + filename + " -c copy " + wpath + filename[:-3] + ".mp4")
            else:
                continue
        print("\033[1;32m All files rerender completed!")
    else:
        for filename in os.listdir(wpath):
            if (filename.endswith(".ts")): #or .avi, .mpeg, whatever.
                resolution = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "program_stream=width,height", "-of", "default=nw=1:nk=1", wpath + filename], capture_output=True, text=True)
                if (re.search("540\n960", resolution.stdout)):
                    os.system("ffmpeg -i " + wpath + filename + " -c copy " + wpath + filename[:-12] + "(竖屏).mp4")
                else:
                    os.system("ffmpeg -i " + wpath + filename + " -c copy " + prc_dir + filename)
                    # print("ffmpeg -i " + wpath + filename + " -c copy " + prc_dir + filename)
            else:
                continue
        print("\033[1;32m All files rerender completed!")

###### Post processing(insert videos)

def creat_meg(prc_dir):
    for filename in os.listdir(prc_dir):
        if (filename.endswith(".txt")):
            os.remove(prc_dir + "merge.txt")
        else:
            if (filename.endswith(".ts")):
                f = open(prc_dir + "merge.txt", "a")
                f.write("file '" + filename + "'" + "\n")
                f.close()
            else:
                continue
    print("\033[1;32m merge.txt is successfully created!")

def insertvid(wpath, prc_dir):
    time.sleep(5)
    print("Videos insertion will start after 5 second")
    file = open(prc_dir + "merge.txt", "r")
    #print(file.readline()[6:23])
    filename = file.readline()[6:]
    fname = '_'.join(filename.split('_')[:-1])
    #print(fname)
    os.system("ffmpeg -fflags +discardcorrupt -f concat -safe 0 -i "+ prc_dir + "merge.txt -c copy " + wpath + fname + ".mp4")

def cleaner(prc_dir):
    print("\033[1;32m All operations ran successfully, deleting cache in 5 seconds!")
    time.sleep(5)
    if os.path.exists(prc_dir):
        shutil.rmtree(prc_dir)
        print("\033[1;32m processed folder removed successfully!")
    else:
        print("\033[1;31m No such directly, quit!")
        quit()


if __name__ == "__main__":
    start()

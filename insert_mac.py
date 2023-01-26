import os, time
import shutil, glob
## For Mac
## Not support filename with space 
###### Rerender container


# /users/something
work_path = os.getcwd()
processed_dir = work_path + "/processed/"

def check():
    videos = 0
    for filename in os.listdir(work_path):
        if (filename.endswith(".mp4")):
            videos += 1
        else:
            continue
    if (videos == 0):
        print("No MP4 files in the working directory, quitting ")
        quit()
    else:
        print(str(videos) + " MP4 files detected, Starting.")

def init_job():
    if os.path.exists(processed_dir):
        print("History cache detected, cleaning.")
        shutil.rmtree(processed_dir)
        os.makedirs(processed_dir)
        print('"processed" folder created successfully!')
        print("Videos processing will start after 5 seconds.")
    else:
        os.makedirs(processed_dir)
        print('"processed" folder created successfully!')
        print("Videos processing will start after 5 seconds.")
    time.sleep(5)

# if not os.path.exists(processed_dir):
#     os.makedirs(processed_dir)
#     print('"processed" folder created successfully!')
#     print("Videos processing will start after 5 seconds.")
# time.sleep(5)


def rerender():
    for filename in os.listdir(work_path):
        if (filename.endswith(".mp4")): #or .avi, .mpeg, whatever.
            os.system("ffmpeg -i " + filename + " -c copy " + processed_dir + filename + "".format(filename))
            #print("ffmpeg -i " + filename + " -c copy " + processed_dir + filename + "")
        else:
            continue
    print("All files rerender completed!")

###### Post processing(insert videos)

def creat_meg():
    for filename in os.listdir(processed_dir):
        if (filename.endswith(".txt")):
            os.remove(processed_dir + "merge.txt")
        else:
            if (filename.endswith(".mp4")):
                f = open(processed_dir + "merge.txt", "a")
                f.write("file '" + filename + "'" + "\n")
                f.close()
            else:
                continue
    print("merge.txt is successfully created!")

def insertvid():
    time.sleep(5)
    print("Videos insertion will start after 5 second")
    file = open(processed_dir + "merge.txt", "r")
    #print(file.readline()[6:23])
    filename = file.readline()[6:]
    fname = '_'.join(filename.split('_')[:-1])
    #print(fname)
    os.system("ffmpeg -fflags +discardcorrupt -f concat -safe 0 -i "+ processed_dir + "merge.txt -c copy " + fname + ".mp4".format(fname))

def cleaner():
    print("All operations ran successfully, deleting cache in 5 seconds!")
    time.sleep(5)
    if os.path.exists(processed_dir):
        shutil.rmtree(processed_dir)
        print("processed folder removed successfully!")
    else:
        print("No such directly, quit!")
        quit()


if __name__ == "__main__":
    check()
    init_job()
    rerender()
    creat_meg()
    insertvid()
    cleaner()

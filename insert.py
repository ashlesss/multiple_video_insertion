# only for 轩子

import os, time
import shutil
######### Rerender container

render_path = os.getcwd()
processed_dir = r"E:\\recording\\轩子\\processed\\"

def check():
    videos = 0
    for filename in os.listdir(render_path):
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
    for filename in os.listdir(render_path):
        if (filename.endswith(".mp4")): #or .avi, .mpeg, whatever.
            os.system("ffmpeg -i {0} -c copy E:\\recording\\轩子\\processed\\{0}".format(filename))
            #print(filename)
        else:
            continue
    print("All files rerender completed!")

######### Post processing(insert videos)

processed_path = r"E:\\recording\\轩子\\processed\\"

def creat_meg():
    for filename in os.listdir(processed_path):
        if (filename.endswith(".txt")):
            os.remove(processed_path + "merge.txt")
        else:
            if (filename.endswith(".mp4")):
                f = open(processed_path + "merge.txt", "a")
                f.write("file '" + filename + "'" + "\n")
                f.close()
            else:
                continue
    print("merge.txt is successfully created!")

def insertvid():
    print("Video insertion will start after 5 seconds")
    time.sleep(5)
    file = open(processed_path + "merge.txt", "r")
    #print(f.readline()[6:22])
    filename = file.readline()[6:]
    fname = '_'.join(filename.split('_')[:-1])
    print(fname)
    os.system("ffmpeg -fflags +discardcorrupt -f concat -safe 0 -i "+ processed_path + "merge.txt -c copy " + fname + ".mp4".format(fname))

def cleaner():
    print("All operations ran successfully, deleting cache in 5 seconds!")
    time.sleep(5)
    if os.path.exists(processed_dir):
        shutil.rmtree(processed_dir)
        print("processed folder removed successfully!")
    else:
        print("No such directly, quit!")
        quit()

# def ot():
#     for filename in os.listdir(processed_path):
#         if (filename.endswith(".mp4")): #or .avi, .mpeg, whatever.
#             # os.system("ffmpeg -i {0} -c copy E:\\recording\\轩子\\processed\\{0}".format(filename))
#             print(filename[:16])
#         else:
#             continue
    


if __name__ == "__main__":
    check()
    init_job()
    rerender()
    creat_meg()
    insertvid()
    cleaner()
    # ot()
    #print(processed_path)

import os, time
import shutil, glob
import logging, sys

# This script only support file name format as 
# "streamer_2023-01-26_15-46-00.mp4"
# and only mp4 videos will be processed

###### Rerender container

###### Global
work_path = os.getcwd()
processed_dir = work_path + "\\processed\\"

###### Logger file
logging.basicConfig(filename='insert.log',
                    filemode='w',
                    level=logging.DEBUG, 
                    format='[%(asctime)s] [%(levelname)s] - %(message)s')

# Console logger
logFormatter = logging.Formatter('[%(asctime)s] [%(levelname)s] - %(message)s')
rootLogger = logging.getLogger()
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)
#logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))

def check():
    videos = 0
    for filename in os.listdir(work_path):
        if (filename.endswith(".mp4")):
            videos += 1
        else:
            continue
    if (videos == 0):
        #print("No MP4 files in the working directory, quitting ")
        logging.error("No MP4 files in the working directory, quitting ")
        quit()
    else:
        #print(str(videos) + " MP4 files detected, Starting.")
        logging.info(str(videos) + " MP4 files detected, Starting.")

def init_job():
    if os.path.exists(processed_dir):
        #print("History cache detected, cleaning.")
        logging.info("History cache detected, cleaning.")
        shutil.rmtree(processed_dir)
        os.makedirs(processed_dir)
        #print('"processed" folder created successfully!')
        logging.info('Old "processed" folder created successfully! Videos processing will start after 5 seconds.')
        #print("Videos processing will start after 5 seconds.")
    else:
        os.makedirs(processed_dir)
        logging.info('New "processed" folder created successfully! Videos processing will start after 5 seconds.')
        #print('"processed" folder created successfully!')
        #print("Videos processing will start after 5 seconds.")
    time.sleep(5)

# if not os.path.exists(processed_dir):
#     os.makedirs(processed_dir)
#     print('"processed" folder created successfully!')
#     print("Videos processing will start after 5 seconds.")
# time.sleep(5)


def rerender():
    for filename in os.listdir(work_path):
        if (filename.endswith(".mp4")): #or .avi, .mpeg, whatever.
            ctlex = "ffmpeg -i " + '"' + filename + '"' + " -c copy " + '"' + processed_dir + filename + '"' + "".format(filename)
            logging.debug("rerender ctl: " + ctlex)
            os.system(ctlex)
            #print("ffmpeg -i " + filename + " -c copy " + processed_dir + filename + "")
        else:
            continue
    #print("All files rerender completed!")
    logging.info("All files rerender completed!")

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
    #print("merge.txt is successfully created!")
    logging.info("merge.txt is successfully created!")

def insertvid():
    time.sleep(5)
    #print("Videos insertion will start after 5 second")
    logging.info("Videos insertion will start after 5 second")
    file = open(processed_dir + "merge.txt", "r")
    #print(file.readline()[6:23])
    filename = file.readline()[6:]
    fname = '_'.join(filename.split('_')[:-1])
    #print(fname)
    ctlex = "ffmpeg -fflags +discardcorrupt -f concat -safe 0 -i " + processed_dir + "merge.txt -c copy " + '"' + fname + ".mp4" + '"'.format(fname)
    logging.debug("Insert ctl: " + ctlex)
    os.system(ctlex)

def cleaner():
    #print("All operations ran successfully, deleting cache in 5 seconds!")
    logging.info("All operations ran successfully, deleting cache in 5 seconds!")
    time.sleep(5)
    if os.path.exists(processed_dir):
        shutil.rmtree(processed_dir)
        #print("processed folder removed successfully!")
        logging.info('"processed" folder removed successfully!')
    else:
        #print("No such directly, quit!")
        logging.error("No such directly, quit!")
        quit()


if __name__ == "__main__":
    check()
    init_job()
    rerender()
    creat_meg()
    insertvid()
    cleaner()

# /* cSpell:disable */

# print("\033[91mRed text\033[0m")
# print("\033[92mGreen text\033[0m")
# print("\033[93mYellow text\033[0m")

import os, time
import shutil
import subprocess
###### Rerender container

import argparse, json

mobvidArr = []
vidArr = []
mobMergeEnable = False
vidMergeEnable = False

def main():
    parser = argparse.ArgumentParser(description="A script with commands and options.")

    # Define a subparser for the "start" command
    subparsers = parser.add_subparsers(dest='command')
    start_parser = subparsers.add_parser('start', help='start command help')
    
    # Add the optional "-path" argument to the "start" command
    start_parser.add_argument('-path', type=str, help="Path to the file or directory")

    args = parser.parse_args()

    # Check if the 'start' command was provided
    if args.command == 'start':
        if args.path:
            print(f"Starting with path: {args.path}")
        else:
            print("\033[93mStarting without a specified path. Using current path instead\033[0m")
            gbPath = os.getcwd()
            start(gbPath)
    else:
        print('\033[91mNo command reveiced.\033[0m')

def start(path):
    for folder in os.listdir(path):
        currFolder = os.path.join(path, folder)
        if (os.path.isdir(currFolder)):
            resetGlobalValues()
            prcPath = initWorkEnv(currFolder)
            initWorkArray(currFolder)
            # print(mobvidArr, vidArr)
            reRender(currFolder, prcPath)
            cleaner(prcPath)
            resetGlobalValues()
        else:
            print(f"\033[93m'{currFolder}' is not a folder\033[0m")
            resetGlobalValues()

def initWorkEnv(currFolder):
    prcPath = os.path.join(currFolder, 'prc')
    if (os.path.exists(prcPath)):
        print("\033[93mHistory cache detected, cleaning\033[0m")
        shutil.rmtree(prcPath)
        os.makedirs(prcPath)
        print("\033[92m'prc' folder created successfully!\033[0m")
        print("\033[92mVideos processing will start after 5 seconds.\033[0m")
    else:
        os.makedirs(prcPath)
        print("\033[92m'prc' folder created successfully!\033[0m")
        print("\033[92mVideos processing will start after 5 seconds.\033[0m")
    time.sleep(5)
    return prcPath

def initWorkArray(currFolder):
    for filename in os.listdir(currFolder):
        if (filename.endswith('.ts')):
            vidPath = os.path.join(currFolder, filename)
            # ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of json input.mp4
            resolution = subprocess.run(["ffprobe", "-v", "error", 
                                         "-select_streams", "v:0", 
                                         "-show_entries", "stream=width,height", 
                                         "-of", "json", vidPath], 
                                         capture_output=True, text=True)
            data = json.loads(resolution.stdout)
            width = data['streams'][0]['width']
            if (width <= 540):
                mobvidArr.append(vidPath)
            else:
                vidArr.append(vidPath)
        else:
            continue

def reRender(currFolder, prcPath):
    global mobMergeEnable, vidMergeEnable
    if (len(vidArr) != 0):
        numvid = 0
        for vid in vidArr:
            # os.system("ffmpeg -i " + wpath + filename + " -c copy " + wpath + filename[:-12] + ".mp4")
            vidname = vid.split('\\')
            newvidname = vidname[-1][:vidname[-1].rfind('.')] + '.mp4'
            status = os.system(f'ffmpeg -analyzeduration 100M -probesize 50M -i {vid} -c copy {os.path.join(prcPath, newvidname)}')
            if (status == 0):
                numvid += 1
            else:
                print(f"\033[91m{vidname[-1]} converted failed\033[0m")

        # print(f"\033[91m{numvid}\033[0m")
        
        if (numvid > 1):
            vidMergeEnable = True
            genMergeFile(prcPath)
            insert(currFolder, prcPath, 'vid')
        elif (numvid == 1):
            vidMergeEnable = False
            for file in os.listdir(prcPath):
                if (file.endswith('.mp4')):
                    oldFilePath = os.path.join(prcPath, file)
                    newFileName = file[:-13] + '.mp4'
                    newFilePath = os.path.join(prcPath, newFileName)
                    # print(oldFilePath, newFilePath)
                    os.rename(oldFilePath, newFilePath)
                    # filePath = os.path.join(prcPath, newFileName)
                    shutil.move(newFilePath, currFolder)
                else:
                    continue
    
    if (len(mobvidArr) != 0):
        mobsubfolder = os.path.join(prcPath, 'sub')
        numvid = 0
        os.makedirs(mobsubfolder)
        for vid in mobvidArr:
            vidname = vid.split('\\')
            newvidname = vidname[-1][:vidname[-1].rfind('.')] + '.mp4'
            status = os.system(f'ffmpeg -analyzeduration 100M -probesize 50M -i {vid} -c copy {os.path.join(mobsubfolder, newvidname)}')
            if (status == 0):
                numvid += 1
            else:
                print(f"\033[91m{vidname[-1]} converted failed\033[0m")
        
        if (numvid > 1):
            mobMergeEnable = True
            genMergeFile(mobsubfolder)
            insert(currFolder, prcPath, 'mobvid')
        elif (numvid == 1):
            mobMergeEnable = False
            oldfilename = os.listdir(mobsubfolder)
            newfilename = oldfilename[0][:-13] + '(竖屏).mp4'
            oldfilePath = os.path.join(mobsubfolder, oldfilename[0])
            newfilepath = os.path.join(mobsubfolder, newfilename)
            os.rename(oldfilePath, newfilepath)
            # filePath = os.path.join(mobsubfolder, (filename[0][:-13] + '.mp4'))
            shutil.move(newfilepath, currFolder)

def genMergeFile(path):
    for filename in os.listdir(path):
        if (filename.endswith('.mp4')):
            f = open(os.path.join(path, 'merge.txt'), 'a')
            f.write(f'file \'{filename}\'\n')
            f.close()
        else:
            continue

def insert(currFolder, prcPath, on):
    isRan = 0
    if (vidMergeEnable and on == 'vid'):
        isRan += 1
        mergepath = os.path.join(prcPath, 'merge.txt')
        newvidname = vidArr[0].split('\\')[-1][:-12] + '.mp4'
        convertedVidPath = os.path.join(currFolder, newvidname)
        status = os.system(f'ffmpeg -fflags +discardcorrupt -f concat -safe 0 -hwaccel cuda -i {mergepath} -c copy {convertedVidPath}')
        if (status == 0):
            print("\033[92mVideo inserted successfully.\033[0m")
        else:
            print(f"\033[91mVideo inserted converted failed\033[0m")

    
    if (mobMergeEnable and on == 'mobvid'):
        isRan += 1
        subFolder = os.path.join(prcPath, 'sub')
        mergepath = os.path.join(subFolder, 'merge.txt')
        newvidname = mobvidArr[0].split('\\')[-1][:-12] + '(竖屏).mp4'
        convertedVidPath = os.path.join(currFolder, newvidname)
        status = os.system(f'ffmpeg -fflags +discardcorrupt -f concat -safe 0 -hwaccel cuda -i {mergepath} -c copy {convertedVidPath}')
        if (status == 0):
            print("\033[92mVideo inserted successfully.\033[0m")
        else:
            print(f"\033[91mVideo inserted converted failed\033[0m")
    
    if (isRan == 0):
        print("\033[92mNo need to run insert video.\033[0m")

def cleaner(prcPath):
    print("\033[93mCleaning cache...\033[0m")
    time.sleep(3)
    if (os.path.exists(prcPath)):
        shutil.rmtree(prcPath)
        print("\033[93mCache deleted sucessfully.\033[0m")
    else:
        print("\033[93mNo such directory, moving on!\033[0m")

def resetGlobalValues():
    global vidArr, mobvidArr, vidMergeEnable, mobMergeEnable
    vidArr = []
    mobvidArr = []
    vidMergeEnable = False
    mobMergeEnable = False


if __name__ == "__main__":
    main()
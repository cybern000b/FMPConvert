import os
import shlex
import subprocess
import sys
import json
import re
import time

def banner():
    banner = r""" 
  ______ __  __ _____     _____                          _   
 |  ____|  \/  |  __ \   / ____|                        | |  
 | |__  | \  / | |__) | | |     ___  _ ____   _____ _ __| |_ 
 |  __| | |\/| |  ___/  | |    / _ \| '_ \ \ / / _ \ '__| __|
 | |    | |  | | |      | |___| (_) | | | \ V /  __/ |  | |_ 
 |_|    |_|  |_|_|       \_____\___/|_| |_|\_/ \___|_|   \__|
                                    code by cybern000b Ver1.0
                                    
"""
    print(banner)
    

def nameFormat():
    currTime = time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())
    if os.path.exists(videoFile) and (not os.path.isdir(videoFile)):
        try:
            nosuffixName = os.path.basename(os.path.splitext(videoFile)[0])
            outFile = re.sub(r'[\\/:*?"<>|\r\n]+', "-", currTime +'-' +nosuffixName +'.mp4')   
            outPath = os.path.normpath(os.path.join(src_dir, outFile))      
        except:
            outPath = None
            print('[x]invalid fileName! {}\n'.format(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())),end='')
    else:
        outPath = None
        print('[x]invalid fileName! {}\n'.format(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())),end='') 
    return outPath 
    

def videoCheck():
    if not os.path.isdir(videoFile):
        print('[+]verifing......\n',end='')
        try:
            checkCMD = shlex.split('ffprobe -v quiet -print_format json -show_format -show_streams ' +videoFile, posix=False)
            chkoutput = subprocess.check_output(checkCMD, shell=True)
            checkStat = json.loads(chkoutput.decode())
            if checkStat['streams'][0]['codec_name'] != "h264":
                print('[+]target is not H264\n',end='')
                if checkStat['format']['format_name'] == "mov,mp4,m4a,3gp,3g2,mj2":
                    print('[*]ready to convert!\n',end='')
                else:
                    checkStat = None
                    print('[x]format incorrect! {}\n'.format(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())),end='')
            else:
                checkStat = 1
                print('[*]no need convert!\n',end='')     
        except:
            checkStat = None
            print('[x]videofile incorrect! {}\n'.format(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())),end='')
    else:
        checkStat = None
        print('[x]invalid fileName! {}\n'.format(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())),end='')
    return(checkStat)


def videoConvert():  
    if checkStat and outPath and checkStat != 1:
        try:
            print('[+]converting......\n',end='')
            print('[*]startTime: {}\n'.format(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())),end='')
            print('[*]EPG :\"{}\"\n'.format(outPath),end='')
            convertCMD = shlex.split('ffmpeg -i ' +videoFile +' -map 0 -c:a copy -c:s copy -c:v libx264 ' +outPath, posix=False)
            subprocess.check_output(convertCMD, stderr=subprocess.STDOUT, shell=True)
            print('[+]conversion successful!\n',end='')
            print('[*]endTime: {}\n'.format(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())),end='')
            print('[+]outPath = ' +outPath +'\n',end='')
        except:
            print('[x]conversion failed! {}\n'.format(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())),end='')
    elif not checkStat:
        print('[x]fileCheck failed! {}\n'.format(time.strftime("%Y-%m-%d-%H:%M:%S", time.localtime())),end='')


def displayFormat():
    print("\n")
    print("[*]now process \"{}\"\n".format(videoFile),end='')


if __name__ == "__main__":  
    banner()
    src_dir = (os.path.abspath(os.path.dirname(sys.argv[1])))
    if len(sys.argv) == 3 and os.path.exists(sys.argv[1]) and sys.argv[2] == r'-check':
        videoFile = sys.argv[1]
        displayFormat()
        videoCheck()
    elif len(sys.argv) == 2 and os.path.exists(sys.argv[1]) and (not os.path.isdir(sys.argv[1])):
        videoFile = sys.argv[1]
        displayFormat()
        outPath = nameFormat()
        checkStat = videoCheck()
        videoConvert()
    elif len(sys.argv) == 2 and os.path.exists(sys.argv[1]) and (os.path.isdir(sys.argv[1])):
        dirs = os.listdir(sys.argv[1])
        namePrefix = (r'~$',r'.',r'$',r'~')
        nameSuffix = (r'webm',r'avi',r'mov',r'mp4',r'mkv',r'm4a',r'wmv')
        for fileName in dirs:
            if not fileName.startswith(namePrefix) and fileName.endswith(nameSuffix):                    
                videoFile = os.path.normpath(os.path.join(os.path.abspath(sys.argv[1]),fileName))
                displayFormat()
                outPath = nameFormat()
                checkStat = videoCheck()                
                videoConvert()               
    else:
        print('[*] Usage: python3 ' +os.path.basename(__file__) +' <videofile or dir> [-check]\n',end='')
        sys.exit(0)
    
import zipfile
import platform
import subprocess
import json
import os
from pathlib import Path
import shutil
import stat

def updateNewTempalte(rootDir):
    for root,dirs,files in os.walk(rootDir):
        for file in files:
            name = file[0:file.index(".")]
            ext = file[file.index("."):]
            if ext == ".zip.py" and os.path.exists(os.path.join(root, name)) == False:
                for dir in dirs:
                    shutil.rmtree(os.path.join(root, dir))
                with zipfile.ZipFile(os.path.join(root, file), "r") as zipf:
                    zipf.extractall(os.path.join(root, name))
                return
        if root != files:
            break
        
def templateDir(rootDir):
    for root,dirs,files in os.walk(rootDir):
        for dir in dirs:
            return os.path.join(root, dir)
        if root != files:
            break
    return ""

def inputConfig(data):
    videoCount = 0
    videos = []
    imageCount = 0
    images = []
    audioCount = 0
    textCount = 0
    texts = []
    for it in data:
        if it["type"].lower() == "image":
            imageCount += 1
            images.append({
                "width": it["width"],
                "height": it["height"]
            })
        elif it["type"].lower() == "video":
            videoCount += 1
            videos.append({
                "width": it["width"],
                "height": it["height"]
            })
        elif it["type"].lower() == "audio":
            audioCount += 1
        elif it["type"].lower() == "text":
            textCount += 1
            texts.append(it["value"])
    return {
        "videoCount":videoCount,
        # "videos":videos,
        "imageCount":imageCount,
        # "images":images,
        "audioCount":audioCount,
        "textCount":textCount,
        # "texts":texts
    }

def listTemplate():
    rootDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "res")
    updateNewTempalte(rootDir)
    tpDir = templateDir(rootDir)
    if len(tpDir) <= 0:
        print("template not found")
    result = []
    for root,dirs,files in os.walk(tpDir):
        for dir in dirs:
            projFile = os.path.join(root, dir, "template.proj")
            if os.path.exists(projFile) == False:
                for root,dirs,files in os.walk(os.path.join(root, dir)):
                    for file in files:
                        name, ext = os.path.splitext(file)
                        if ext == ".proj":
                            projFile = os.path.join(root, file)
            with open(projFile, 'r') as f:
                projConfig = json.load(f)
            inputListPath = os.path.join(root, dir, "inputList.conf")
            if "inputList" in projConfig:
                inputListPath = os.path.join(root, dir, projConfig["inputList"])
            if "type" not in projConfig:
                continue
            if os.path.exists(inputListPath) == False:
                continue
            inputList = []
            with open(inputListPath, 'r') as f:
                inputList = json.load(f)
            data = inputConfig(inputList)
            data["name"] = dir
            data["path"] = os.path.join(root, dir)
            result.append(data)
        if root != files:
            break
    print(json.dumps(result))
    return
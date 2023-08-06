import os
import sys
import zipfile
import shutil


def decompiling(apkPath:str,resultDir):
    if not os.path.exists(apkPath):
        print("❌apk文件不存在:"+apkPath)
        return
    if not zipfile.is_zipfile(apkPath):
        print("❌apk文件错误:"+apkPath)
        return   
    #将APK 改为zip 解压到resultDir目录
    realApkPath = os.path.join(os.getcwd(),apkPath)
    apkFile = zipfile.ZipFile(realApkPath,"r")
    #将APK的绝对路径去除.apk
    (_,apkPathWithoutExt) = os.path.split(apkPath)
    apkPathWithoutExt = apkPathWithoutExt.replace(".apk","")
    outputDirPath = os.path.join(os.getcwd(),apkPathWithoutExt)
    if resultDir:
       outputDirPath = os.path.join(os.getcwd(),resultDir,apkPathWithoutExt) 
    #clear历史文件夹
    delFiles(outputDirPath)
    print("🚀正在解压->"+outputDirPath)
    apkFile.extractall(outputDirPath)
    #获取dex文件
    for filePath in os.listdir(outputDirPath):
        if filePath.endswith(".dex"):
            dexFilePath = os.path.join(outputDirPath,filePath)
            #将dex->jar
            jarPath = dex2Jar(dexFilePath)
            #删除dex
            delFiles(dexFilePath)
            #解压jar
            unzipJar(jarPath,outputDirPath)
            #删除jar
            delFiles(jarPath)
    openGUI()
    openDir(outputDirPath)
    print("✅将文件夹中任意.class文件拖入GUI APP查看即可-> "+outputDirPath)
    
def openDir(dir):
    print("✅正在打开文件夹->"+dir)
    command ="open "+ dir
    os.popen(command).readlines()  
    
def openGUI():
    print("✅正在打开JD-GUI->")
    current_file_dir = os.path.dirname(__file__)
    guiPath=  os.path.join(current_file_dir,'config/JD-GUI.app')
    command ="open "+ guiPath
    os.popen(command).readlines()     
    
    
def unzipJar(jarPath,outputDirPath):
    if not os.path.exists(jarPath) or not os.path.exists(outputDirPath):
        return
    jarFile = zipfile.ZipFile(jarPath,"r")
    jarFile.extractall(outputDirPath) 
          
def dex2Jar(dexPath):
    if not os.path.exists(dexPath):
        return ""
    (dexName,_) = os.path.splitext(dexPath)
    current_file_dir = os.path.dirname(__file__)
    dexDir = os.path.dirname(dexPath)
    jarPath = os.path.join(dexDir,dexName+".jar")
    dex2JarShPath=  os.path.join(current_file_dir,'config/dex-tools-2.1/d2j-dex2jar.sh')
    d2jInvokeShPath=  os.path.join(current_file_dir,'config/dex-tools-2.1/d2j_invoke.sh')
    command ="sudo chmod +x "+d2jInvokeShPath+"&& sh "+ dex2JarShPath+" "+dexPath+" -o "+jarPath+" --force"     
    commandResult = os.popen(command).readlines()      
    return jarPath
    
def delFiles(filePath):
    if os.path.exists(filePath):
       print("🧹正在删除->"+filePath)
       if os.path.isdir(filePath):
           shutil.rmtree(filePath)
       else:
          os.remove(filePath)

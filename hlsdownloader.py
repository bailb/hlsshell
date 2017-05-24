#coding=utf8
import urllib
import urllib2
import os
import sys
import socket

DIR="./"
targetName="video.ts"
URL="http://devimages.apple.com/iphone/samples/bipbop/gear1/prog_index.m3u8"
urlPrefix="http://devimages.apple.com/iphone/samples/bipbop/gear1/"

g_DownloadPercent=""

class sliceInfo(object):
        def __init__(self,url,duration):
                self._url=url
                self._size=0
                self._duration=duration
        def set_size(self,size):
                self._size=size

class sliceList(object):
        def __init__(self):
                self.__sliceList=[]

        def insert(self,aSlice):
                self.__sliceList.append(aSlice)
                return self.__sliceList;

        def count(self):
                return len(self.__sliceList)
        def getIndex(self,index):
                return self.__sliceList[index]

def progressReport(count, blockSize, totalSize):
	percent=int (count*blockSize*100/totalSize)
	if percent > 100:
		percent = 100

	sys.stdout.write("\r Total["+g_DownloadPercent+"] %3d%%" % percent)
	sys.stdout.flush()

def progress_report(count, blockSize, totalSize):
	percent=int (count*blockSize*100/totalSize)
	if percent > 100:
		percent = 100

	progressBar="["
	for i in range(percent-1):
		progressBar+="="
	if percent < 100:	
		progressBar+=">"

	for i in range(100-percent):
		progressBar+=" "

	progressBar+="]"
	sys.stdout.write("\r Total["+g_DownloadPercent+"] "+progressBar+" %d%%" % percent)
	sys.stdout.flush()

def downloadFile(url,savePath, state):
	try:
		if state == 2:
			print(url)
			print(savePath)	
			ret = urllib.urlretrieve(url, savePath, reporthook=progressReport)
		else:
			ret = urllib.urlretrieve(url, savePath)

		return 0
	except Exception,e:
		print '\n Error retrieve the URL:',url,"["+str(e)+"]"
		return -1

def downloadIndex(url):
	path=os.path.split(url)[1]
	try:
		savePath=path
		ret = downloadFile(url,savePath,1)
		if ret == 0:
			return 0
		elif ret == -1:
			return -1
	except:
		print '\n downloadIndex error:',url
		return -1

def parseM3u8(m3u8Context,m3u8List):
	listContex=m3u8Context.split("\n")
	lineNum=len(listContex)

	try:
		i=0
		while i < lineNum:
			lineContex=listContex[i]
			if "#EXTINF"==lineContex[0:len("#EXTINF")]:
				url=listContex[i+1]
				duration=lineContex.split(":")[1].split(",")[0]
				aSlice=sliceInfo(url,duration)
				m3u8List.insert(aSlice)
				i+=1
			elif "#EXT-X-MEDIA-SEQUENCE"==lineContex[0:len("#EXT-X-MEDIA-SEQUENCE")]:
				print '#EXT-X-MEDIA-SEQUENCE ',lineContex.split(":")[1].split(",")[0]
			i+=1
		return 0
	except Exception,e:
		print '\n parseM3u8 error :',m3u8Context,"["+str(e)+"]"
		return -1

def downloadSlice(m3u8List,index):
	listCount=m3u8List.count()
	if listCount <= 0:
		print 'There is no media found'
	try:
		i=index
		tryCount = 0
		while i < listCount:
			global g_DownloadPercent
			g_DownloadPercent = str(i+1)+"/"+str(listCount)
			aSlice=m3u8List.getIndex(i)
			ret = downloadFile(urlPrefix+aSlice._url,DIR+aSlice._url, 2)
			if ret == 0: #下载成功
				i+=1
				tryCount = 0
			elif ret == -1: #下载失败，重新下载
				if tryCount > 3:
					return -1
				tryCount += 1
				print "failed: ["+aSlice._url+"] will download again"

	except Exception,e:
		print'\n downloadSlice error['+str(e)+"]"

def spliceMedia(m3u8List):
	listCount=m3u8List.count()
	if listCount <= 0:
                print 'There is no media found'
	try:
		targetFile=open(targetName,"wb")		
		for i in range(listCount):
			aSlice=m3u8List.getIndex(i)
                        tmpFile = open(DIR+aSlice._url,"rb")
			targetFile.write(tmpFile.read())	
			tmpFile.close()

		targetFile.close()
	except Exception,e:
                print'\n splice  error ['+str(e)+"]"

def startDownload():
	ret = downloadIndex(URL)
	if ret == -1:
		return -1
	
	m3u8Context=open(os.path.split(URL)[1],"rb").read()

	m3u8List=sliceList()	
	ret = parseM3u8(m3u8Context,m3u8List)
	if ret == -1:
		return -1
	ret = downloadSlice(m3u8List,0)
	if ret == -1:
		print "下载失败"
	spliceMedia(m3u8List)
	return 0;
	
#if __name__ == "__main__"
socket.setdefaulttimeout(30) #配置全局属性
startDownload()


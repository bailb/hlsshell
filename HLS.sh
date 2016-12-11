#!/bin/bash
url=http://devimages.apple.com/iphone/samples/bipbop/gear1/prog_index.m3u8
url_prefix=http://devimages.apple.com/iphone/samples/bipbop/gear1/
declare -a sliceList
sourceListLength=0
downloadTool="curl"
M3U8FILE=m3uFile

downloadIndex() {
	local URL=$0
	local m3u8Context
	local i=0

	m3u8Context=`$downloadTool $URL`
	while read Line
	do
		i=$(($i+1))


		tmpLine=`echo $Line | awk -F ':' '{print $1}'` 
		echo $tmpLine 
		sliceList[$i]=$Line	
	done < $M3U8FILE
	
}

downloadSlice() {
	echo "downloadSlice"
}

startDownload() {
	echo "startDownload"	

}


        m3u8Context=`$downloadTool $url`
	echo "$m3u8Context" > $M3U8FILE
	isSliceUrl=no
	j=0	
        while read Line
        do
                i=$(($i+1))
			
		if [ "$isSliceUrl" = "yes" ]; then
			isSliceUrl=no
	                sliceList[$j]=$Line
			j=$(($j+1))
			echo $Line >> sliceUrl
			continue
		fi

                tmpLine=`echo $Line | awk -F ':' '{print $1}'`
                echo $tmpLine
		if [ "$tmpLine" = "#EXTINF" ]; then
	               isSliceUrl=yes 
		fi

        done < $M3U8FILE

	num=${#sliceList[@]}
	echo $num
	echo ${sliceList[0]}
	echo ${sliceList[100]}

	for((i=0;i<num;i++))
	{
		echo $url_prefix${sliceList[$i]}
	        $downloadTool $url_prefix${sliceList[$i]} > ${sliceList[$i]}
	} 

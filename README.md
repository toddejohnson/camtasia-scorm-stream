camtasia-scorm-stream
=====================

Convert a Camtasia SCORM to stream using Flash Media Server

SCORM's don't need to include the video file.  There are many improved technologies such as Flash Media Servers that are execlent at distributing video files in a bandwith efficent way.  Also you can rely on tradional FTP to upload these large video files.  That shrinks the SCORM ZIP file to be well below normal HTTP POST limits.  

This utility takes the unified Camtasia ZIP file output and separates the .mp4 video and updates the HTML Player to point to your RTMP URL.  

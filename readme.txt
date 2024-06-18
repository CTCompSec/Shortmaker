18/6/24

Hi,

This is an application that will allow you to generate a short video using stock footage and a gnerated voice from just a text prompt.

There are some issues with this, but I'm leaving it "as is".

Known issues:
1. All file paths need to be reworked
2. Packages need to be created
3. ./ffmpeg/pexelstemp.txt should be ./ffmpeg/ffmpegtemp.txt and all references to changed

Let's walk through it.

First we can start with calling master.sh.  This is kind of our control panel.

That's going to write to a file inside of ./zuki/

Zuki is a LLM that someone is running on a Discord server.  You're welcome to find the Discord yourself and request access or replace this with any LLM at all.

If the call is successful, it will result in writing to ./zuki/zukioutput.txt

Then we will make a call to AWS's cool, Amazon Polly,  There are a number of text to speech tools, some even inside of python.  You could rework this section with any of those tools.

Next we will make a call to pexels, searching for stock videos related to the keywords we generated in zukioutput.  Then we will download those videos into ./pexels/assets

Finally, we will concatonate and add transitions using ffmpeg.

The correct running order of our ffmpeg scripts should be:
1. /ffmpeg/ffmpegprep.py
2. /ffmpeg/script.sh
3. /ffmpeg/concat.js
4. /ffmpeg/scrip2.sh

This is a section that could be refactored and improved greatly.  Within concat.js I used a framework that someone else had already built

YOU WILL NEED TO USE NODE.JS AND INSTALL THE CORRECT DEPENDANCIES WITHIN ./ffmpeg/

Also note that race conditions are an issue here as async isn't properly implemented.  Easiest way to deal with this is to just increment sleep in ./master.sh

I left some of the final videos I made inside of ./ffmpeg they aren't necessary at all but that's what your end result should look like

-CT

CTcompsec (at) proton (dot) me

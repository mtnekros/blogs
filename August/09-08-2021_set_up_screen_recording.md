# How to set up a screen recording with ffmpeg & mpv

## We want to:
* Record the screen
* With a floating window that streams our webcam
    * Floating window can't have border and title bar. Otherwise it wouldn't be cool.
    * Should be resizable with a key binding for convenience.


## First thing's first. Let's install the required packages.

We need:
* ffmpeg => to record the screen
* mpv => to add the little floating window
* x11-utils or xorg-xdpyinfo => to get the screen size

For arch based users:
`sudo pacman -S ffmpeg mpv xorg-xdpyinfo`

For debian based users:
`sudo apt install ffmpeg mpv x11-utils`


## The main thang, commands
For the little flaoting window, we are going to use mpv which is a video
player. Instead of passing a video as the parameter, we are going to pass the
feed from the webcam for it to play. The command to do just that is given
below.

`mpv av://v4l2:/dev/video0 --profile=low-latency --no-border --no-osc`

Options:
+ av://v4l2:/dev/video0 => Specifies that we want to use /dev/video0 (webcam) as our input
+ --profile=low-latency => Use a default profile that tries to reduce the latency as much as possible
+ --no-border           => Removes the border and the title bar from the window so that it looks like a proper floating video
+ --no-osc              => Removes the onscreen control that is available in mpv by default. We don't need it because it's just going to be streaming from the webcam

Since we have no border in the floating video window, it can't be resized using
the mouse and although mpv comes with a lot of useful key bindings. It doesn't
have one for window resizing. So we'll have to manually add a key binding to
scale the window size.
1. Open the ~/.config/mpv/input.conf file. (create it if it doesn't exist)
2. You can look through the commented codes to see how it works.
3. Add the following line and save the file

```
a       add window-scale -0.005
ctrl+a  add window-scale 0.005
```

4. Now when you open mpv, you can press 'a' to make the window size smaller and
   press Ctrl+a to make it bigger.

To record the screen, we are going to use ffmpeg which is a video converter
with a lot of interesting functionalities.

`ffmpeg -f x11grab -s $(xdpyinfo | grep dimensions | awk '{print $2}') -i :0.0
-itsoffset 0.3s -f alsa -i default output.mkv`

Options:
+ -f x11grab        => Specifies we want to use x11grab as our format
+ -s $(xdpyinfo | grep dimensions | awk '{print $2}') => Specifies ffmpeg to capture the whole screen
+ -i :0.0           => Specifies we want to record the primary screen
+ -itsoffset 0.3s   => Specifies to offset the audio by 0.3s. Without this option our audio and video won't sync up since the video has a bit of latency
+ -f alsa           => Specifies alsa as our audio input format
+ -i default        => Specifies to use the default recording device

## Conclusion
So that concludes our little tutorial, we can easily setup a screen recording
with a fancy floating webcam stream using very simple command line tools. And
that is pretty cool. Also, I recommend writing these commands as a script file.
Since we need to be able to quickly run those scripts if we're going to be
using this often.


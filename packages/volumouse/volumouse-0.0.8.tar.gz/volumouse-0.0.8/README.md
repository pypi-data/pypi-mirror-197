# volumouse
[UP TO DATE] A Python 3 program that allows you to change the volume with the mouse wheel using it at the four corners of the screen. 
Run in a terminal `volumouse -c` to configure and execute it with `volumouse` command


<p align="center" width="100%">
    <img width="33%" src="https://www.evinco-software.com/eng/techImage/volumouse-mouse-volume-control.jpg"> 
</p>






# Install the main package :


1. Install dependancies :

You need x11-utils :
Debian, Ubuntu, Kali Linux, Raspbian :`apt-get install x11-utils`
Arch Linux :`pacman -S xorg-xdpyinfo`
CentOS : `yum install xorg-x11-utils`
Fedora : `dnf install xorg-x11-utils`

You also need pulseaudio-utils :
Debian, Ubuntu, Kali Linux, Raspbian : `apt-get install pulseaudio-utils`
Alpine : `apk add pulseaudio-utils`
Arch Linux : `pacman -S libpulse`
CentOS : `yum install pulseaudio-utils`
Fedora : `dnf install pulseaudio-utils`


2. Install volumouse :

#########################################

On the next version of Python and Linux you will need to install in this way (using virtual env) :

```
sudo apt install pipx
pipx install volumouse
```
To update volumouse to the latest version :
`pipx upgrade volumouse`

If volumouse has been installed in ~/.local/bin you will need to add this file to the PATH : ~/.local/bin (if it's not already done) :

`sudo echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc`

[How to create a PATH on Linux ?](https://linuxize.com/post/how-to-add-directory-to-path-in-linux/)

#########################################

Normal way to install on Linux :

```
sudo python3 -m pip install -U volumouse
```

!!! It's very important to use the `sudo` command because like this volumouse will be in the PATH


# Configure :


It's very easy to configure, there are just a simple command to execute, once for all, the first time :

All is explained in volumouse --help and volumouse --info

(`sudo` command is required if you have installed volumouse with the `sudo` command) :

Open a terminal and type :
- `sudo volumouse --configure` or `sudo volumouse -c`



# Usage : 


Just run the command `volumouse` at startup or in a terminal



# Create a PATH to volumouse :


If you have installed volumouse without the `sudo` command on Linux you will need to create a PATH for starting volumouse with the `volumouse` command.

Indead, to be able to run volumouse directly in the terminal, without going to the source package, you should add the volumouse's folder to the PATH :

On Linux, it can be permanently done by executing : `sudo gedit ~/.bashrc` and adding, at the end of the document, this line :

`export PATH=$PATH:/place/of/the/folder/volumouse`



If you want to temporarily test it before, you can just execute this command in the terminal : 

`export PATH=$PATH:/place/of/the/folder/volumouse` 

It will be restored on the next reboot.



By doing this, instead of taping `python3 '/place/of/the/folder/volumouse/volumouse.py'`,
you will be able to directly tape in the terminal : `volumouse`.






[@pzim-devdata GitHub Pages](https://github.com/pzim-devdata/volumouse/issues)












<p align="center" width="100%">
    <img width="33%" src="https://avatars.githubusercontent.com/u/52496172?v=4"> 
</p>

------------------------------------------------------------------

- [Licence](https://github.com/pzim-devdata/DATA-developer/raw/master/LICENSE)
MIT License Copyright (c) 2023 pzim-devdata

------------------------------------------------------------------

Created by @pzim-devdata - feel free to contact me!

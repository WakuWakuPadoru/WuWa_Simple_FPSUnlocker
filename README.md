# Wuthering Waves (WuWa) Simple FPS Unlocker Toolkit

## Introduction

### **RT Unlock doesn't currently work in 2.3! But FPS Unlock still works.**
### **Updated for 2.2! FPS Unlocking is now working in 2.2 even on Unsupported CPUs/GPUs** - 29th March 2025
### **Enable 120 FPS Support AND/OR Raytracing/RT on AMD/Older Nvidia GPUs**
### **<ins>For AMD GPU Users, Please read the FAQ Below!</ins>**

This project is being **actively updated** and **maintained**. 

This is a simple FPS Unlocker Toolkit that can be used to **push Wuthering Waves's max FPS cap beyond the default 60 FPS
regardless of your Graphics Card / GPU**. It also gives you the option to **enable Raytracing on older Nvidia RTX GPUs and RT-Capable AMD GPUs**.
This Unlocker is designed to be **simple to use** without much frills. Automated checks and scripts mean that you can
just
run the program, and it will do the rest for you along with comprehensive error checking. It comes in a Windows exe
executable format, so you just need to
download,
extract, and run!

If you find this useful, do consider giving this project a star and share it with your friends!

**This Unlocker doesn't modify or interact with any of the Game Files and Assets! It only modifies settings and configurations on the user's behalf. This is 100% safe and won't result in a ban.**

**Wuthering Waves is a game developed by Kuro Games, and this project is not affiliated with them in any way. All rights
belong to their respective copyright holders and owners.**

## Features

- Simple to use with clear instructions at every step of the way!
- Multiple checks and verifications to make this as bug-free and smooth as possible.
- Simple to use UI, no need for command prompts or CLI. Just run the program / exe and navigate the UI with buttons and
  mouse
  clicks!
- Unlock 120 FPS Support!
- Manually enable Raytracing on GPUs older than the RTX 4000 series or AMD RX 6000 series and up, allows you to set the Raytracing quality, Raytraced Reflections, and Raytraced Global Illumination.
- Program will notify you whenever there are updates available!
- No additional installations or dependencies required (apart from Wuthering Waves). Just download and run the program!
- Light-weight and simple. No modifications to the game files, just the settings file.
- ~~Enable True Full Screen Mode / Exclusive Full Screen for potentially better performance, better smoothness, less
  stuttering, and
  less hitching.~~
- ~~Set your desired Full Screen Resolution. For example, something lower than your Monitor's native resolution while
  still in Full Screen for some extra Performance! The game doesn't allow this by default but the unlocker allows you to
  do this!~~

## Ray Tracing on the AMD Radeon RX 9070 XT GPU
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/aV7NE15RSnY/0.jpg)](https://www.youtube.com/watch?v=aV7NE15RSnY)


## Releases / Downloads

You can find the latest release [here](https://github.com/WakuWakuPadoru/WuWa_Simple_FPSUnlocker/releases/latest).

## Installation

- Download the latest release.
- Extract **all of the contents** of the downloaded ZIP file.
- Run "main.exe" or "main" from the extracted folder.
- Run the downloaded file :)
- Win your 50s/50s!

#### Before/After Raytracing on 2080Ti
![img](https://i.imgur.com/kELEp7N.jpeg)

#### Before:

![Before](https://i.imgur.com/hVF6LN4.jpeg)

#### After:

![After](https://i.imgur.com/CyeQKx2.png)

##### (Note: The FPS counter is from MSI Afterburner, not the game itself) After the Unlocker is applied, it will show the Frame Rate as 30 FPS which is false.
![Menu](https://i.imgur.com/PXQurCx.png)
## Screenshots:
![Screenshot 0](https://i.imgur.com/6Kc06vY.png)
![Screenshot 0.5](https://i.imgur.com/nJrkgIi.png)
![Screenshot 1](https://i.imgur.com/evBWUrr.png)
![Screenshot 3](https://i.imgur.com/tGMRk8h.png)

## FAQ
### I use an older AMD GPU (Older than 9000 Series), but Raytracing either stutters or crashes at Shader Compilation.
Please download [24.12.1](https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-WIN-24-12-1.html) from AMD.
### I use an AMD RDNA 4 GPU (9000 Series), but Raytracing either stutters or crashes at Shader Compilation.
There is currently no older version of AMD's drivers that can be installed that doesn't have this issue, this is an AMD issue, not a Kuro issue. [Please report this to AMD](https://www.amd.com/en/resources/support-articles/faqs/AMDBRT.html) as this issue didn't happen in 24.X.
However, you **may** still brute force it if you want to, but you may encounter **Performance Issues**. <ins>**PLEASE DON'T DO THIS IF YOU HAVE AN AMD 6000-7000 SERIES! Read the first FAQ above**.</ins>
1) Use the Unlocker as per normal, apply RT, and restart the game up to 2 times to trigger the Shader Compilation.
2) The game **will** crash at around 70%, but don't click "ok" and let the game continue.
3) The game **will** automatically exit after around a minute; restart it and repeat the process until the shaders eventually compile.
Eventually, you will be able to play the game with RT Enabled once you get pass the Shader Compilation process but performance will likely be unstable.
### Didn't Kuro Games already officially allow 120 FPS?
Yes, but they only officially allow certain specific hardware to use this officially. Even if your PC is perfectly powerful enough to run it, if it's not on the White List, you can't run the game, particularly on AMD Ryzen PCs.
### Even though I don't have an RTX 4000 series and newer, can I enable Raytracing?
Yes. Though..you would still require an RT-capable GPU, something like an RX 6600 or an RTX 2060. You won't be able to run this on a GTX 1080 for instance.
### Why did Kuro Games only allow specific hardware to run 120 FPS officially?
I don't know.
### Is this safe?
Yes. This only modifies the game's configuration and settings on the user's behalf, and not the game files. Whenever you make changes to the game's settings via in-game, these very same files are the ones that are saved and updated.
### Version X.X just came out, why isn't the Unlocker working?
It isn't uncommon for Kuro Games to update the format and structure of the configuration files between versions. As these changes are never documented and might be "spaghetti" in nature, it might take a few days to investigate and implement an updated solution.
### I have issues with the Unlocker and/or would like to provide feedback and suggestions.
You can post it either in [Discussions](https://github.com/WakuWakuPadoru/WuWa_Simple_FPSUnlocker/discussions) or [Issues](https://github.com/WakuWakuPadoru/WuWa_Simple_FPSUnlocker/issues).

## Technology

This project is built using Python and Tkinter for the UI. It checks and modifies the game's configuration files to
unlock the FPS cap using SQLite. It does not interfere with the game files and uses minimal packages as much as
possible. Compiled to EXE using PyInstaller.
Even though it's meant to be a simple Unlocker, I ended up implementing multiple checks and fail-safes that probably
wasn't needed. (sweats)

## Repository Links

[WuWa_Simple_FPSUnlocker](https://github.com/WakuWakuPadoru/WuWa_Simple_FPSUnlocker/)

## Waku Waku

![Waku Waku](https://i.imgur.com/xkQ9ko5.gif)

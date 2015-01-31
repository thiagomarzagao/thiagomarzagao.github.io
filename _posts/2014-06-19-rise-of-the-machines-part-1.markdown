---
author: thiagomarzagao
comments: true
date: 2014-06-19 01:08:14+00:00
layout: post
slug: rise-of-the-machines-part-1
title: rise of the machines - part 1
wordpress_id: 792
categories:
- Python
- stats
tags:
- C
- Mindstorms
- Python
---

Social scientists spend a lot of time writing code that has no physical manifestation. Other than changing pixels in a laptop screen our scripts do not change the material world in any observable way. Meanwhile our colleagues in the engineering department get to build Terminator-like robots and all sorts of fun machines. So I decided I wouldn't live in perpetual envy anymore. 

Enter LEGO Mindstorms.

[![](http://i.imgur.com/UOxfMHq.png)](http://imgur.com/UOxfMHq)

I've been <del>playing</del> experimenting with it for about a week and it's hard to overstate how much fun it is. Besides lots of regular LEGO pieces you get a mini-CPU, a couple of servomotors, a light sensor, and a proximity sensor. You plug the motors and sensors into the mini-CPU (usually referred to as the "EV3 brick"), use the regular LEGO pieces to assemble whatever robot your imagination produces, and then connect your computer to the EV3 brick to control the motors and read data from the sensors.

[![](http://i.imgur.com/5lBRG0j.jpg)](http://imgur.com/5lBRG0j)
EV3 brick, motors, and sensors

The EV3 is the third generation of the LEGO Mindstorms set. The previous ones were called NXT and RCX. The EV3 improves on the NXT on several aspects, including processing power, memory size, number of ports, the inclusion of a microSD card slot, ability to communicate with iOS, and a larger screen. The NXT is still around though, but somehow it costs more than the EV3 ($449.99 vs $349.95 on Amazon); maybe that's because there are more applications developed for the NXT, as it's been around since 2006.

The EV3 brick runs on six AA batteries. They go flat really fast (two or three days with moderate use), so I strongly recommend that you buy rechargeable ones. Also, if you don't want to have to disassemble the robot every time you need to recharge the batteries you should look into [this](https://shop.education.lego.com/legoed/education/LEGO+MINDSTORMS+Education+EV3/EV3+Rechargeable+DC+Battery/45501&isSimpleSearch=true).

Another thing you can do is use a Raspberry Pi instead of the EV3 brick. You can do it yourself if you're familiar with these things or you can buy a Raspberry Pi that's already customized for use with the EV3 sensors and motors (see [here](http://www.dexterindustries.com/BrickPi.html)).

The first step is deciding how exactly you are going to interact with your robot. If you don't want to write code, LEGO provides an [app](http://www.lego.com/en-us/mindstorms/downloads/software/ddsoftwaredownload/) that lets you program visually, using flowcharts (a bit like in [Scratch](http://scratch.mit.edu/)). You do the programming in your computer and then send the commands to the EV3 brick via USB, Bluetooth, or WiFi. It looks like this:

[![](http://i.imgur.com/wP1GEq9.png)](http://imgur.com/wP1GEq9)

But more likely you will want to write code (if for no other reason than because the LEGO app is painfully slow - even in my quad-core laptop with 16GB of memory). You have a number of options. 

<strong>Java</strong>

If Java is your cup of tea then [leJOS](http://www.lejos.org/) is the way to go about it. leJOS is a Java Virtual Machine that can replace the native firmware of the EV3 brick and let you run Java code on it. It works like this: you get ahold of a microSD card, make it bootable (follow [these instructions](http://sourceforge.net/p/lejos/wiki/Installing%20leJOS/)), insert it into the EV3 brick, and turn it on. If everything went well the EV3 will boot to leJOS (and not to its native firmware). You can then start writing your Java programs, using the leJOS [API](http://www.lejos.org/ev3/docs/). (Conveniently, leJOS doesn't mess with the native firmware: if you remove the microSD card and restart the EV3 it will boot to the native firmware again.)

[![](http://i.imgur.com/haYU2on.jpg)](http://imgur.com/haYU2on)
leJOS initial screen

<strong>Python</strong>

The Python alternative works similarly to the Java one: you get ahold of a microSD card, make it bootable (following [these instructions](https://github.com/topikachu/python-ev3)), insert it into the EV3 brick and turn it on. If everything went well the EV3 will boot the custom debian wheezy OS in the bootable card (and not to its native firmware). You then SSH into the EV3 and use this [API](https://github.com/hmml/ev3) to write your programs. (Same as with leJOS, the native firmware is still there for when you want it - just remove the microSD card and restart the EV3.)

The Python alternative sounds great, but somehow I couldn't make it work. I insert the card, turn the EV3 on, but then nothing (visible) happens, it seems that at some point in the process the EV3 gets stuck. I tried re-flashing the card and also buying a different card, but nothing worked. After two days of failed attempts I gave up (I may come back to it at some point though). (Also note that even if it works [the Bluetooth is not stable yet](https://github.com/topikachu/python-ev3#notes)).

<strong>Matlab</strong>

There are two ways to program the EV3 using Matlab. One is the official [EV3 package](http://www.mathworks.com/hardware-support/lego-mindstorms-ev3-simulink.html) from MathWorks. Downside: it only works on Windows (32-bit and 64-bit) and on Linux (64-bit). Which takes us to the second alternative: the folks from CyPhy Lab have created a [Matlab-EV3 toolkit](https://wiki.qut.edu.au/display/cyphy/QUT+EV3+MATLAB+toolkit) that should work on Macs as well. Their website is full of documentation and examples to help you get started.

Unlike the Java and Python solutions the Matlab ones do not require any microSD cards. You will boot the EV3 normally and your program will communicate with the native EV3 firmware (via USB, Bluetooth, or WiFi). I think this is a huge plus.

<strong>Microsoft API</strong>

Microsoft has produced an [API](http://legoev3.codeplex.com/) that lets you interact with the EV3 from Windows desktop, Windows Phone 8, and WinRT, using .NET, WinJS, and C++. (I don't want to work with Windows, so I didn't really look into it.)

<strong>C</strong>

The EV3's native firmware is [open source](https://github.com/mindboards/ev3sources) and written (largely) in C. If you clone it you can use C to communicate with the EV3. Like the Matlab and Microsoft solutions it doesn't require any microSD cards; you just turn the EV3 on and communicate with its native firmware via USB, Bluetooth, or WiFi. And unlike the Matlab and Microsoft solutions it's 100% open source - no need to spend money on Matlab or Windows. The downside is that the firmware source code is only partially documented, so figuring out the right command to do this or that involves a fair amount of trial and error (or asking for help on StackOverflow). But I think it's still worth it (this is what I've been using).

This is it for now. In part 2 I'll talk a bit about using C to communicate with the EV3. My end goal is to build a self-driving robot, for the fun of it. I'm not sure I'll use C for everything; I may use it just to communicate with the EV3 and then pass all the data to Python for the machine learning algorithms. We'll see.

This is something that I'm learning on-the-fly - I've never done any serious work in C before and I just learned what bytecode is -, so these posts will not be a tutorial, but merely a way to share these experiences (and perhaps receive some useful feedback from people who actually know this stuff).

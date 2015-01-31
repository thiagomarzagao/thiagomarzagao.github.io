---
author: thiagomarzagao
comments: true
date: 2014-06-27 17:00:03+00:00
layout: post
slug: rise-of-the-machines-part-3
title: rise of the machines - part 3
wordpress_id: 907
tags:
- EV3
- Mindstorms
- Python
---

[![](http://i.imgur.com/LTJZhVI.png)](http://imgur.com/LTJZhVI)

In [part 2](http://thiagomarzagao.com/2014/06/24/rise-of-the-machines-part-2-2/) we saw how to use C++ and bytecodes to program LEGO Mindstorms EV3 bricks. Now, bytecodes don't make for human-readable scripts. And C++ scripts take [~4 times](http://www.connellybarnes.com/documents/language_productivity.pdf) longer to write than equivalent Python or Perl scripts. So, I've started writing a Python module that should make life easier - I've called it ev3py.

Here's the GitHub [repo](https://github.com/thiagomarzagao/ev3py). For now the module is still inchoate; it only covers three basic functions (starting motors, stopping motors, and reading data from sensors) and it only works on Macs, and only via Bluetooth. But it's a start.

Let's see a concrete example. Say you want to start the motor on port A with power 20. If you're using bytecodes and C++ you need to write something like this:

{% highlight cpp %}
#include <unistd.h>
#include <fcntl.h>
#include "ev3sources/lms2012/c_com/source/c_com.h"

int main()
{    
    unsigned const char start_motor[] {13, 0, 0, 0,
        DIRECT_COMMAND_NO_REPLY,
        0, 0,
        opOUTPUT_POWER, LC0(0), LC0(1), LC1(20),
        opOUTPUT_START, LC0(0), LC0(1)};

    int bt = open("/dev/tty.EV3-SerialPort", O_RDWR);
    write(bt, start_motor, 15);
 }
{% endhighlight %}

With ev3py here's how you do it:

{% highlight python %}
from ev3py import ev3

mybrick = ev3()
mybrick.connect('bt')
mybrick.start_motor(port = 'a', power = 20)
{% endhighlight %}

So, with ev3py the code becomes human-readable and intuitive. It also becomes much faster to write. You no longer need to set message size, message counter, command type, etc.

Unlike other EV3 modules ev3py interacts with the EV3's native firmware, so there's no need to make the EV3 boot to a different operating system; just turn the brick on and you're ready.

The goal is to eventually cover all EV3 capability and make ev3py work with USB and WiFi and also with Linux and Windows. I.e., something along the lines of the [QUT-EV3 toolkit](https://wiki.qut.edu.au/display/cyphy/QUT+EV3+MATLAB+toolkit) and the [Microsoft EV3 API](https://legoev3.codeplex.com/). If you'd like to contribute your help is much appreciated - just fork the GitHub repo and add capabilities, fix bugs, or suggest changes to the overall structure of the module.

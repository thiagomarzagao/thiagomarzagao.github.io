---
comments: true
layout: post
title: rise of the machines - part 2
---

Here I show how to use C++ to communicate via Bluetooth with the LEGO Mindstorms EV3 brick (see [previous post](http://thiagomarzagao.com/2014/06/19/rise-of-the-machines-part-1/)).

If you are on a Mac everything should work right away. If you are using Ubuntu or other Linux distro I think you'll only need to change the Bluetooth part a bit (my Ubuntu laptop doesn't have Bluetooth, so I can't be sure). If somehow you are forced to use Windows I think you'll need to change the Bluetooth part a lot. All the rest should be the same though.

So, you start by cloning the [source code](https://github.com/mindboards/ev3sources) of the EV3 firmware: open up your terminal and do `git clone https://github.com/mindboards/ev3sources.git` Name the folder `ev3sources`, to make the examples below easier to run. Also, open the `ev3sources/lms2012/c_com/source/c_com.h` file and change the line `#include "lms2012.h"` in order to provide the full path to the `lms2012.h` file. Say: 

{% highlight cpp %}
#include "/Users/YourUsername/MyLegoProject/ev3sources/lms2012/lms2012/source/lms2012.h"
{% endhighlight %}

That's all the setup you need - you are now ready to write and send commands to the EV3. Turn on your EV3, enable Bluetooth, make it discoverable (see the [EV3 user guide](http://www.lego.com/en-us/mindstorms/downloads/user-guides/enus/) if necessary), plug some motor to port A, fire up Xcode or whatever IDE you use, and try running the following code snippet:

{% highlight cpp %}
#include <unistd.h>
#include <fcntl.h>
#include "ev3sources/lms2012/c_com/source/c_com.h"

int main()
{
    
    // write command to start motor on port A with power 20
    unsigned const char start_motor[] {13, 0, 0, 0,
        DIRECT_COMMAND_NO_REPLY,
        0, 0,
        opOUTPUT_POWER, LC0(0), LC0(1), LC1(20),
        opOUTPUT_START, LC0(0), LC0(1)};

    // send command to EV3 via Bluetooth
    int bt = open("/dev/tty.EV3-SerialPort", O_RDWR);
    write(bt, start_motor, 15);

    // end connection with EV3
    close(bt);
}
{% endhighlight %}

If everything went well you should see the motor starting.

If instead you get an authentication-related error message, download and install the [official LEGO app](http://www.lego.com/en-us/mindstorms/downloads/software/ddsoftwaredownload/) (if you haven't already), launch it, use it to connect to the EV3 via Bluetooth, check that it really connected, then close it. Somehow that fixes the issue for good. (I know, it's an ugly hack, but life is short).

Now let's deconstruct our little script. There are two steps: writing the command and sending the command. Writing the command is the hard part. As you see, it's not as simple as, say, `EV3.start_motor(port = "A", power = 20)`. Instead of human-readable code what we have here is something called _bytecodes_. In this particular example every comma-separated piece of the expression inside the inner curly braces is a bytecode - except for the `LC1(20)` part, which is two bytecodes (more on this in a moment). The first and second bytecodes - 13 and 0 - tell the EV3 the message size (not counting the 13 and the 0 themselves). The third and fourth bytecodes - 0 and 0 - are the message counter.

The fifth bytecode - `DIRECT_COMMAND_NO_REPLY` - tells the EV3 two things. First, that the instruction is a direct command, as opposed to a system command. Direct commands let you interact with the EV3 and the motors and sensors. System commands let you do things like write to files, create directories, and update the firmware. Second, `DIRECT_COMMAND_NO_REPLY` tells the EV3 that this is a one-way communication: just start the motor, no need to send any data back. So, the three alternatives to `DIRECT_COMMAND_NO_REPLY` are `SYSTEM_COMMAND_NO_REPLY`, `DIRECT_COMMAND_REPLY`, and `SYSTEM_COMMAND_REPLY`.

The sixth and seventh bytecodes - 0 and 0 - are, respectively, the number of global and local variables you will need when receiving data from the EV3. Here we're using a `DIRECT_COMMAND_NO_REPLY` type of command, so there is no response from the EV3 and hence both bytecodes are zero.

Now we get to the command _lui-même_. We actually have two commands here, one after the other. The first one, `opOUTPUT_POWER`, sets how much power to send to the motor. The second one, `opOUTPUT_START`, starts the motor. Each command is followed by a bunch of local constants (that's what LC stands for), which contain the necessary arguments. For both commands the first `LC0()` is zero unless you have multiple EV3 bricks (you can join up to four EV3 bricks together; that's called a "daisy chain"). Also for both commands, the second `LC0()` determines the EV3 port. Here we're using port A - hence `LC0(1)`. Use `LC0(2)` for port B, `LC0(4)` for port C, and `LC0(8)` for port D. Finally, `opOUTPUT_POWER` takes one additional argument: the desired power. The unit here is percentages: 20 means that we want the motor to run at 20% of its maximum capacity. Unlike the other local constants, this one is of type `LC1`, not `LC0`, so it takes up two bytes (see the [bytecodes.h](https://github.com/mindboards/ev3sources/blob/master/lms2012/lms2012/source/bytecodes.h) file for more on local constants); that is why the message size is 13 even though we only have 12 comma-separated elements.

(Don't be a sloppy coder like me: instead of having these magic numbers, declare proper variables or constants and use these instead - `LC0(port)`, `LC1(power)`, etc.)

Now let's send the command we just wrote. On a Mac the way we communicate with other devices via Bluetooth is by writing to (and reading from) `tty` files that live in the `\dev` folder (these are not actual files, but file-like objects). If you inspect that folder you will see one `tty` file for every Bluetooth device you have paired with your computer: your cell phone, your printer, etc. The EV3 file is called `tty.EV3-SerialPort`. (If you're curious, here's [all the specs and intricacies](https://developer.apple.com/library/mac/documentation/devicedrivers/conceptual/bluetooth/BT_Bluetooth_On_MOSX/BT_Bluetooth_On_MOSX.html) of how Bluetooth is implemented on a Mac.)

So, to send the command we wrote before to the EV3 via Bluetooth we open the `tty.EV3-SerialPort` file (line 16), write the command to it (line 17), and close it (line 20).

That's it, you can now use C++ to control the EV3 motors.

Just so you know, your command is automatically converted to hexadecimal format before being sent to the EV3 (those `LC()`s are macros that make the conversion). In other words, your EV3 will not receive `{13, 0, 0, 0, DIRECT_COMMAND_NO_REPLY, 0, 0, opOUTPUT_POWER, LC0(0), LC0(1), LC1(20), opOUTPUT_START, LC0(0), LC0(1)}`. It will receive `\x0D\x00\x00\x00\x80\x00\x00\xA4\x00\x01\x81\x14\xA6\x00\x01` instead. The mapping is provided in the [bytecodes.h](https://github.com/mindboards/ev3sources/blob/master/lms2012/lms2012/source/bytecodes.h) file. For instance, `DIRECT_COMMAND_NO_REPLY` is `0x80`, `opOUTPUT_POWER` is `0xA4`, and so on.

If you prefer you can hardcode the hexadecimals. This produces the exact same outcome:

{% highlight cpp %}
#include <unistd.h>
#include <fcntl.h>
#include "ev3sources/lms2012/c_com/source/c_com.h"

int main()
{
    
    // write command to start motor on port A with power 20
    char start_motor[] = "\x0D\x00\x00\x00\x80\x00\x00\xA4\x00\x01\x81\x14\xA6\x00\x01";

    // send command to EV3 via Bluetooth
    int bt = open("/dev/tty.EV3-SerialPort", O_RDWR);
    write(bt, start_motor, 15);

    // end connection with EV3
    close(bt);
}
{% endhighlight %}

If you master the hexadecimals you can use any language to communicate with the EV3. For instance, in Python you can do this:

{% highlight python %}
# write command to start motor on port A with power 20
start_motor = '\x0D\x00\x00\x00\x80\x00\x00\xA4\x00\x01\x81\x14\xA6\x00\x01' + '\n'

# send command to EV3 via Bluetooth
with open('/dev/tty.EV3-SerialPort, mode = 'w+', buffering = 0) as bt:
    bt.write(start_motor)
{% endhighlight %}

All right then. Now, how do we get data back from the EV3? Well, it's the reverse process: instead of writing to `tty.EV3-SerialPort` we read from it. The trick here is to find the sensor data amidst all the other stuff that the EV3 sends back to your computer, but we'll get there (btw, I'm grateful to the good samaritan who [showed me how to do this](http://stackoverflow.com/questions/24253509/using-c-to-get-data-from-a-lego-ev3-sensor)). To make matters more clear, plug some sensor on port 1 and try running this code:

{% highlight cpp %}
#include <unistd.h>
#include <fcntl.h>
#include <iostream>
#include "ev3sources/lms2012/c_com/source/c_com.h"

int main()
{
    
    // read sensor on port 1
    unsigned const char read_sensor[] {11, 0, 0, 0,
        DIRECT_COMMAND_REPLY,
        1, 0,
        opINPUT_READ, LC0(0), LC0(0), LC0(0), LC0(0), GV0(0)};

    // send command to EV3 via Bluetooth
    int bt = open("/dev/tty.EV3-SerialPort", O_RDWR);
    write(bt, read_sensor, 13);

    // receive data back from EV3 via Bluetooth
    unsigned char sensor_data[255];
    read(bt, sensor_data, 255);
    for(int i=0; i<255; i++) {
        printf("%x", sensor_data[i]);
    }
    
    // end connection with EV3
    close(bt);
}
{% endhighlight %}

The structure of the code is pretty similar to what we had before. The first change is that now our command type is no longer `DIRECT_COMMAND_NO_REPLY` but `DIRECT_COMMAND_REPLY`, as we now want to receive data from the EV3. The second change is the sixth bytecode, which is now 1. That means we are now requesting one global variable - we'll need it to store the sensor data. 

The third change is of course the command itself, which is now `opINPUT_READ`. Its arguments are, in order: the EV3 brick (usually 0, unless you have multiple bricks), the port number (minus 1), the sensor type (0 = don't change the type), and the sensor mode (0 = don't change the mode). `GV0` is not an argument, but the global variable where the sensor data will be stored. Like the motor power, the data we will get back will be in percentage (alternatively, there is an `opINPUT_READSI` command that returns the data in SI units).

The fourth change is that we now have a new code block. Its first line - `unsigned char sensor_data[255]` - creates an array of size 255, with all values initialized to zero. The size is 255 because at this point we don't know exactly what the actual size of the received data will be, so we want to be safe: the data will be in hexadecimal format, so 255 is about as large as it gets (just as with the data we send, the first two bytes of the data we receive tell us how large the message is - but we can only count up to 255 with two bytes in hexadecimal format, so 255 is the limit here). The second line receives the data and the for loop prints each byte to the screen.

If everything went well you should see as output something like 400021F00000... Try it a couple more times, moving the sensor around in-between. You will notice that the first five digits or so don't change, and neither do all the others after the sixth or seventh digit. For instance, your results will look like 400023D00000... or 400025B00000... Only two digits or so will change. _That is your sensor data!_ In these three examples, for instance, your data points are 1F, 3D, and 5B. That's hexadecimal format; in decimal format that means 31, 61, and 91 (here's a [conversion table](http://ascii.cl/conversion.htm)). Now, once you've figured out what the relevant digits are you can get rid of that loop and print only them (say, `printf("%x", sensor_data[5]);`).

That's it! Now you can control the motors and read the sensors - that should help you get started. If you inspect the [c_com.h](https://github.com/mindboards/ev3sources/blob/e5be3a6d591c60b26a3fb853989a9c86f5a7cc56/lms2012/c_com/source/c_com.h) files you will see lots of other commands, some of them with usage examples. The way forward is by exploring the firmware code and by trial and error.

Happy building!

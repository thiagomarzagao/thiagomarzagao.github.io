---
comments: true
layout: post
title: doing data science when you live in a failed state
---

Brazil is the undisputed world leader in homicides: over 50 thousand a year, which is more than Europe, Oceania, United States, Russia, and China combined. Yes, combined. Yes, the whole freaking Europe. Yes, the supposedly gun-loving United States. Yes, China with its 1.3 billion people. Brazil beats these continents and countries by 4,473 homicides, which is roughly equivalent to Uganda or to ten Canadas. No, [I'm not making these numbers up](https://en.wikipedia.org/wiki/List_of_countries_by_intentional_homicide_rate). Take a moment to let that sink in.

As you might guess, a country with lots of homicides also tends to have lots of robbery. I'd love to take my MacBook Pro to a coffee shop and work there all day like I used to when I was in grad school - back when I lived in lovely, safe, Columbus, Ohio. But if I do that in Brasília I'll probably come back home empty handed (if I come back home at all). You can't parade Apple gear around when you live in a failed state. 

I finally got tired of working from home all weekend, so I decided to enable SSH and HTTP connections into my home network, so I can use my Mac remotely as if it were an AWS server. That way I can go to the coffee shop with my old, cheap Lenovo - or even a tablet or smartphone - and use it to connect to my MacBook, which will remain safe and sound back home. It took some doing and I imagine others may be going through the same problem (i.e., wanting to work at a coffee shop but [living in an episode of The Walking Dead](https://www.wsj.com/articles/chaos-swells-amid-police-strike-in-brazil-state-1486572445)), so here's a how-to.

My setup is: Humax HG100R-L2 modem (that's what most clients of NET - Brazil's largest cable company - have), AirPort Extreme Base Station router, MacBook Pro. Your setup will likely differ, but you can probably tweak the instructions here to fit whatever you have.

**step 1: your modem**

If you have both a modem and a router then the easiest way to go about this is to put your modem in 'bridge mode'. That means disabling your modem's advanced settings and delegating them to your router. That way you only need to worry about router settings. You won't need to worry about complex interactions between your modem settings and router settings.

Head to http://192.168.0.1/ on your browser. You should see the page below.

<img src="http://i.imgur.com/5qdWoaO.png" title="source: imgur.com" />

If you've never changed them, your id and password are 'admin' and 'password' respectively. Sign in. You should see the following, except with your WiFi network name and password shown under "SSID(2.4GHz)" and "Senha" respectively. (Your password will be shown in plain characters, not as a bunch of dots, so don't let your neighbors peek.) (Yes, Humax' settings are in a mix of Portuguese and English. It beats me too.)

<img src="http://i.imgur.com/6OckjLr.png" title="source: imgur.com" />

Click "Advanced Network Settings" (lower right corner). You should see something like this:

<img src="http://i.imgur.com/S2CYOO8.png" title="source: imgur.com" />

Click on "Definir" (between "Status" and "Back Up", second column from the left). You should see a page with a bit more options than the following one (that's because your modem is not in bridge mode yet).

<img src="http://i.imgur.com/jDP8MvD.png" title="source: imgur.com" />

On the "Modo Switch" menu, choose "Bridge", then click "Aplicar". Click "ok" on whatever confirmation pop up appears. This will make you go offline for a couple of minutes, as your modem resets itself. Wait until it's back up online again and voilà, your modem is now in bridge mode.

(If you ever need to tweak your modem settings again, it's no longer http://192.168.0.1/ but http://192.168.100.1)

**step 2: your router**

On to your router now. We need to tell it to accept incoming SSH and HTTP connections. In order to do that we need to tell your router to map those types of connections to specific ports.

On your Mac, open the AirPort Utility app.

<img src="http://i.imgur.com/qYhU4lc.png" title="source: imgur.com" />

Click on the AirPort Extreme picture to go into your routers' settings and go to the 'Network' tab. You should see something like this:

<img src="http://i.imgur.com/1GkIwv3.png" title="source: imgur.com" />

We'll make a lot of changes here. First, on the "Router Mode" dropdown menu, choose "DHCP and NAT" if that's not the chosen value already. Then click the "+" button near "DHCP Reservations". That will open a small page. You'll make it look like the one below by selecting the exact same choices. (To do that you'll need to know your MAC address, which you can find out in your Mac by going into "System Preferences", "Network", "Advanced"; it's the combination of digits you see right next to "Wi-Fi Address".) When everything matches, click "Save".

<img src="http://i.imgur.com/X8XBJaT.png" title="source: imgur.com" />

Now you're back to this:

<img src="http://i.imgur.com/1GkIwv3.png" title="source: imgur.com" />

Click the "+" button near "Port Settings". A small page will pop up. Tweak all the fields so that it looks exactly like this:

<img src="http://i.imgur.com/iOwiAPY.png" title="source: imgur.com" />

Click "Save". Then click the "+" button near "Port Settings" again. The same small page will pop up. Make it look exactly like this:

<img src="http://i.imgur.com/5eNGZ94.png" title="source: imgur.com" />

Click "Save". Then click "Update". Your router will go crazy for a moment as it does its magic. Wait until it comes back up online and voilà, you have allowed SSH and HTTP connections into your home network. SSH connections will be forwarded to port 22 and HTTP connections will be forwarded to port 8080.

**step 3: your Mac**

This part is simple. Go to "System Preferences", "Sharing", and enable Remote Login:

<img src="http://i.imgur.com/2Q79h2Y.png" title="source: imgur.com" />

If your firewall is active then you need to tell it to allow incoming traffic through ports 22 and 8080. This can be a bit tricky and it depends on your OS version. [This](http://superuser.com/questions/265856/configure-osx-firewall-to-allow-ssh-server) may help. Alternatively, you can take the lazy and insecure path of simply disabling your firewall altogether ("System Preferences", "Security and Privacy", "Firewall").

**step 4: your IP address**

You need to know your MacBook's public IP address so you can access it from the outside. [This](http://www.whatsmyip.org/) should tell you. Write it down.

My experience with NET in Brazil (and with TimeWarnerCable in the US) is that IP addresses don't change that often. But they do sometimes. If that bothers you you may ask that your cable provider give you a static IP address (they may charge a small fee for that). (EDIT: alternatively, you can use a Dynamic DNS service - like [this](http://dyn.com/remote-access/); h/t [Thompson Marzagão](https://twitter.com/marzagao?lang=en).)

**step 5: your coffee shop**

Take whatever cheap, inconspicous piece of hardware you have at hand to your favorite coffee shop. Launch a terminal and do `ssh myusername@myipaddress`, where myusername is the username you normally use to log into your Mac and myipaddress is the IP address you wrote down in step 4. Enter your password and that's it, you are now inside your Mac. You can `cd` into different directories, run code, do whatever you want.

If your coffee shop hardware is a tablet or smartphone, [Termius](https://www.termius.com/) is a terrific SSH client for mobile devices.

<img src="http://i.imgur.com/fgFpOka.jpg" title="source: imgur.com" />

**step 6 (optional): your data science**

Wondering why I made you enable HTTP connections? Well, here comes the really fun part: [Jupyter notebooks](https://jupyter.readthedocs.io/en/latest/running.html). You can start a Jupyter server in your Mac and then, with your coffee shop cheapoware, use your browser to write code interactively and have it run on your Mac. Jupyter's default language is Python but you can install kernels for an increasingly large number of languages, like R and Julia.

On your Mac, do `pip install jupyter` to install Jupyter and then do `jupyter notebook --ip='0.0.0.0' --port='8080' --no-browser` to start the Jupyter server. You'll be given a url. Something like `http://0.0.0.0:8080/?token=sfdsfs90809809s8dfs0df8sdf`. Replace `0.0.0.0` by myipaddress (see step 4). That's the address you'll use at the coffee shop to launch Jupyter notebooks.

(If your cheapoware is a laptop things should work right out-of-the-box. If it's an iOS device then you have some additional steps to take - see [here](https://github.com/jupyter/notebook/issues/1421).)

**step 7: your venti caramel macchiato**

That's it! You have now reduced your likelihood of getting mugged and minimized your losses in case you do get mugged. Time to grab your katana and go mingle with the locals.
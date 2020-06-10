---
layout: post
title: "Christmas Lights 2: Serial Protocol Adventures"
category: Projects
tags: []
---
{% include JB/setup %}

A couple of years ago, my dad and I built [a fancy wooden enclosure for the GE ColorEffects programmable LED lights](/2012/04/23/my-dads-new-lights), and I think the finished product looked excellent:

<img src="/img/2012-04-23/DSC_0283.jpg" width="75%">

 However, I was never entirely happy with the electronics that I designed to control them. The system I was using involved a laptop running a Python web server to provide the user interface and an Arduino microcontroller to speak the precisely timed protocol needed to control the lights themselves. The laptop and microcontroller communicated over a simple serial protocol that I wrote, and the microcontroller's firmware was very simple: it would listen for a command containing the ID of a particular light and its desired brightness and color and then then translate that information and send it along to the string of lights. The microcontroller was necessary because the GE lights themselves can only be controlled through a self-clocked single wire protocol, helpfully reverse-engineered by [deepdarc](http://www.deepdarc.com/2010/11/27/hacking-christmas-lights/). The protocol is as follows (quoting from deepdarc):

<blockquote>
<ul>
<li>Idle bus state: Low</li>
<li>Start Bit: High for 10µSeconds</li>
<li>0 Bit: Low for 10µSeconds, High for 20µSeconds</li>
<li>1 Bit: Low for 20µSeconds, High for 10µSeconds</li>
<li>Minimum quiet-time between frames: 30µSeconds</li>
</ul>

Each frame is 26 bits long and has the following format:

<ul>
<li>Start bit</li>
<li>6-Bit Bulb Address, MSB first</li>
<li>8-Bit Brightness, MSB first</li>
<li>4-Bit Blue, MSB first</li>
<li>4-Bit Green, MSB first</li>
<li>4-Bit Red, MSB first</li>
</ul>
</blockquote>

The key is the timing for the 0 and 1 bits: we have to be able to create accurate pulses of 10 and 20µs, which is actually quite difficult to do with a normal computer. That's because a normal operating system is easily distracted: any task your program asks it to do will get done...eventually. So, to send a 0 to the lights, you might set some output value to Low and then ask the operating system to wait for 10µs, but meanwhile the operating system will have wandered off to think about where you've moved the mouse or what your music player is doing or what the next packet from the internet is and by the time it gets back to you, it will be several milliseconds too late. There are so-called *real-time* operating systems which will let you say things like "wait 10µs and no more", but I wasn't quite ready to wipe out my entire computer just for this project.

Instead, when people need accurate timing they often just use a microcontroller. Microcontrollers are extremely simple, and generally run exactly one program at a time. That means that you can easily write commands like "set this pin low for 10µs and then high for 20µs" and expect them to work every time. This is exactly what I originally did for the lights, and it worked. The problem is simply that adding another computer (the microcontroller) adds a lot of complication, since we now have to write the software for the microcontroller and the protocol for it to communicate with the laptop, and this adds a lot of new opportunities for error. For example, I would routinely see garbage output on the lights (flickering, displaying the wrong colors, etc.) until I realized that the laptop was sending data faster than the microcontroller could translate it, which would eventually overflow its memory and cause all kinds of problems. I fixed that problem, but it meant reducing the throughput of the whole system, which lowered the framerate of the lights.

As a result, I was highly motivated to try to get the microcontroller out of the system. This is where everybody's favorite $35 Linux computer, the Raspberry Pi, comes in handy. The Raspberry Pi fills a really interesting niche in the computer market: it's fast enough to act like a real desktop computer when you need it to, but it's as small and as cheap as an Arduino, and, most importantly, it has a whole bunch of general purpose input/output ports that you can use do interact with all kinds of electronic devices. One of the ports that the Pi has uses a protocol called [SPI or Serial Peripheral Interface](http://en.wikipedia.org/wiki/Serial_Peripheral_Interface_Bus) which is a simple way for the Pi to communicate with one or more external devices. I wired the ouptut of the SPI port to the data line of the lights, using a simple logic inverter chip to raise the output voltage to 5V and protect the Pi in case of a short somewhere in the lights:

<figure class="onecol-figure">
	<img class="svg-figure" src="/img/2014-07-25-lights/wiring.svg">
	<figcaption>Wiring diagram for the connection between the Raspberry Pi and the ColorEffects lights. The 74HC14N is a 5 Volt logic inverter, which I'm using here just to raise the output voltage of the Raspberry Pi's signal from 3.3V to 5V and to isolate the Pi in case there is a short circuit in the lights. MOSI (for "master out slave in") is the output of the SPI port.</figcaption>
</figure>

If you want to build this yourself, you'll need a way to wire up to the Pi's IO pins. The easiest way to do that is with a ["Pi Cobbler" from Adafruit](http://www.adafruit.com/products/914), but you can also do it yourself with a piece of ribbon cable. You'll also need a 74HC14 or similar, like [this one](http://www.digikey.com/product-detail/en/SN74HC14N/296-1577-5-ND/277223) on digikey ([datasheet](http://www.ti.com/lit/ds/symlink/sn74hc14.pdf)) and a small breadboard to hold everything.


The SPI interface on the Pi is very cool, but it doesn't solve our problem right away. It can't be directly configured to send data in the format that the lights want (with a 0 as 10µs low, 20µs high, etc.); instead, it can only send a byte consisting of 8 high or low values, at a bit rate of 125kHz or 250kHz or 500kHz or 1MHz or 2MHz and so on. In addition, in between every byte, the output of the SPI line goes low for exactly one clock cycle.

Fortunately, we can work with this. I first tried to use the SPI port by setting it to a bit rate of 250kHz, which meant that every byte took `\((1 + 8) \times \frac{1}{250000} = 36\)`µs, which is quite close to 10µs low + 20µs high = 30µs total we want. I couldn't control the exact amount of time that the output stayed high or low, but I could keep it low or high for several clock cycles by sending a byte with several 0s or 1s in a row. To send a 0 to the lights, I would write 00111111 to the SPI port, and to send a 1 to the lights I would write 00001111. This worked...almost. You can see the timing I used in the figure below:

<figure class="onecol-figure">
	<img class="svg-figure" src="/img/2014-07-25-lights/bad_labeled_timing.svg">
	<figcaption>Timing information for my first try with the SPI protocol. The labels on bottom of the figure show the 8-bit bytes written to SPI, along with the 12µs pause between each byte. The labels on the top of the figure show the individual bits as interpreted by the GE lights. This timing worked, but not reliably, resulting in the lights frequently misinterpreting the desired color or address.</figcaption>
</figure>

Unfortunately, I must have been just on the edge of what the lights could understand: the commands I sent to them were correctly followed over 90% of the time, but the missed commands resulted in flickering and lights being set to the wrong color. The timing just wasn't quite good enough, and changing the number of 0s and 1s in each byte couldn't solve it.

I decided to try a different bit rate. Decreasing the rate from 250kHz to 125kHz brought the time to write a byte over SPI up to `\((1+8) \times \frac{1}{125000} = 72\)`µs. I decided to try to pack 3 bits worth of data into this space, which gave me exactly 3 clock cycles per bit. This made life really easy: to send a 0 to the lights I could just write 011 over SPI, and to send a 1 I would write 001. Three of those values packed together took 9 clock cycles, which fit perfectly into the size of an SPI byte (8 clock cycles plus the 1 cycle pause). You can see what this looked like on the oscilloscope below:

<figure class="onecol-figure">
	<img class="svg-figure" src="/img/2014-07-25-lights/labeled_timing.svg">
	<figcaption>Better SPI timing, which worked perfectly. This setup uses a 125kHz SPI data rate with 3 GE bits per SPI byte. As before, the labels on bottom of the figure show the 8-bit bytes written to SPI, along with the 8.1µs pause between each byte. A 0 is now 8.2µs low, 16.4µs high.</figcaption>
</figure>

 This worked perfectly. I can now control my lights directly from the Raspberry Pi with no flickering or errors, and I've successfully cut the complexity of the whole system in half. Hooray!

## Source Code
All the code for this project lives on GitHub in the [Bemis100](https://github.com/rdeits/Bemis-100) repository. You can see the SPI driver for the GE lights in [ge_spi.py](https://github.com/rdeits/Bemis-100/blob/master/led/ge_spi.py).

# Useful Links for HP-16C Jovial Assembler

## Documentation

- [HP-16C User Manual](https://literature.hpcalc.org/community/hp16c-oh-en.pdf)
- [HP-16C at the Museum of HP Calculators](https://www.hpmuseum.org/hp16.htm)
- [HP-16C Features](https://www.hpmuseum.org/features/16cf.htm)
- [HP-16C CPU](https://www.hpmuseum.org/techcpu.htm)
- [HP-16C Tech Specs](https://www.hpmuseum.org/tech10.htm)

## Getting your hands on an HP-16C
- [eBay](https://www.ebay.com/sch/i.html?_nkw=hp-16c) - This is how I got mine. They are not cheap, but they are worth it and will last forever. 
- [SwissMicro DM16L](https://www.swissmicros.com/product/dm16l) - A modern clone of the HP-16C
- [PX16C Kit](https://www.tindie.com/products/hobbystone/px16c-an-hp16c-programmers-calculator-emulator/) - This is a Raspberry Pi-based emulator of the HP-16C. It is a kit that you have to assemble yourself. It is currently out of stock. 
    - I plan on getting on of these at some point. I would like to maybe try to port the Jovial Assembler to output to it, but it isn't open source, so I don't know if that will be possible. It could be a fun project to try reverse engineering it though.
    - I would love to see someone replace the Raspberry Pi with an FPGA to make it more authentic. I believe people have replicated the HP nut processor in Verilog and/or VHDL, so it should be possible.

## Software

- [JRPN HP-16C Simulator](https://jrpn.jovial.com/)
    - This is the simulator that I have on my phone for everyday use if I don't have my physical HP-16C with me.
- [HP16C Emulator by Jamie O'Connell](http://www.hp16c.org/)
    - This is my preferred simulator for debugging. It allows you to see the Program memory, Registers, and Stack all at once. 
- [HP16C Emulator by The Joseph M. Newcomer Co.](http://flounder.com/hp16c.htm)
    - I haven't tried this one out, but it supports the Palm Pilot! That alone was cool enough to include it in this list of links. 
    - Note that this is not supported by the Jovial Assembler (it does not even support programming at all), but who doesn't love the Palm Pilot?

## Other Computer Scientist's Calculators
- [Casio CM-100](http://edspi31415.blogspot.com/2017/02/retro-review-casio-cm-100-computer-math.html)
    - This has one feature that the HP-16C does not, a conversion between decimal degrees and sexagesimal degrees (degrees, minutes, seconds) and vice versa. Of course, I wrote a program to do this on my HP-16C (we can't have the Casio outdoing the HP now can we?), but it executes the conversion much faster than the HP-16C.
    - It is also solar powered (without a backup battery), which has its pros and cons.
- [Texas Instruments TI Programmer](http://www.datamath.org/Sci/MAJESTIC/Programmer.htm)
    - There is also an LCD model and the TI Programmer II which is identical to the LCD model in a different case. They all have the same functionality, just different form factors and display types.
    - I don't have one of these, but I am aware that you can replace the ancient battery pack with a standard 9V battery!
- These calculators are much cheaper than the HP-16C, but they are not nearly as powerful. If you are a broke college student, these might be a good alternative if you need something dedicated and physical.  
- These are the only other two dedicated Computer Scientist's calculators that I know of. If you know of any others, please let me know. I would love to learn more about them.
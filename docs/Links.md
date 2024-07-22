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

## Other Tools

- [JRPN HP-16C Simulator](https://jrpn.jovial.com/)
    - This is the primary tool I am using to test Jovial assembly programs. It is seems to be a little buggy, but it is open source and the exported programs are in a human-readable format. This is also the simulator that I have on my phone for everyday use if I don't have my physical HP-16C with me.
- [HP-16C Emulator by Jamie O'Connell](http://www.hp16c.org/)
    - I find this one to be more robust than the JRPN simulator. It also has stack, register, and program views, which aid strongly in debugging your program. However, it is closed source and the format of the exported programs is not easily decipherable. Therefore, programs must be typed in manually unless I/someone reverse engineers the it. The project is Donationware, but the forum is still up and running, so it may be possible to get the original creator to share the source code. 
- [HP16C Emulator by The Joseph M. Newcomer Co.](http://flounder.com/hp16c.htm)
    - I haven't tried this one out, but it supports the Palm Pilot! That alone was cool enough to include it. However it is not a full implementation. 

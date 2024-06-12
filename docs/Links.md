# Useful Links for HP-16C Compiler and VoyagerC Project

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
    - I plan on getting on of these at some point. I would like to maybe try to port the VoyagerC compiler to it, but this is very far down the line.

## Other Tools

- [JRPN HP-16C Simulator](https://jrpn.jovial.com/)
    - This is the primary tool I am using to test VoyagerC programs. It is seems to be a little buggy (I have had some program editing features not work as expected), but it is open source and the exported programs are in a human-readable format.
- [HP-16C Emulator by Jamie O'Connell](http://www.hp16c.org/)
    - I find this one to be more robust than the JRPN simulator. It also has stack, register, and program views. However, it is closed source and the format of the exported programs is not easily decipherable. Therefore, programs must be typed in manually.
- [HP16C Emulator by The Joseph M. Newcomer Co.](http://flounder.com/hp16c.htm)
    - I haven't tried this one out yet, but it supports the Palm Pilot!

## Helpful Resources I Came Across While Working on This Project
- [I wrote a programming language. Here’s how you can, too.](https://www.freecodecamp.org/news/the-programming-language-pipeline-91d3f449c919/)
- [Building Your Own Programming Language From Scratch](https://hackernoon.com/building-your-own-programming-language-from-scratch)
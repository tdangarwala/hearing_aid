# hearing_aid
Inspired by my grandfather's hearing aid performance complaints I wanted to learn more about what goes into making them work and apply the concepts I learned in my digital signal processing class. 

I'm using a Daisy Seed microcontroller.

Why: This microcontroller is optimized for audio processing and similar applications. It allows for easy integration with a microphone input and headphones as output. It features an ARM Cortex M7 processor and signal processing compatiblity which is well suited for the real time requirements of this project. Most importantly, it has a lot of built in build tools, cpu usage optimization tools, and a very active discord channel if I get stuck. 

Scope: The main areas I want to target are improving hearing with one on one conversations in noisy environments and conversations in group settings (i.e. a large dinner or multi family gathering for the holidays) while using cheaper off the shelf components. 

I am planning on designing an FIR filter. Even though FIR filters are more computationally expensive and slower than IIR, they are inherently stable (no poles - no chance for instability with denominator going to 0), they can achieve linear phase response (preserves order), and simpler to implement (mostly for my novice skills).

Process:
1. Start with characterizing how much noise the microphone picks up without any generated sound. 

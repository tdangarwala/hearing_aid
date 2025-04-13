# hearing_aid
Inspired by my grandfather's hearing aid performance complaints I wanted to learn more about what goes into making them work and apply the concepts I learned in my digital signal processing class. 

I'm using a Daisy Seed microcontroller.

Why: This microcontroller is optimized for audio processing and similar applications. It allows for easy integration with a microphone input and headphones as output. It features an ARM Cortex M7 processor and signal processing compatiblity which is well suited for the real time requirements of this project. Most importantly, it has a lot of built in build tools, cpu usage optimization tools, and a very active discord channel if I get stuck. 

Scope: The main areas I want to target are improving hearing with one on one conversations in noisy environments and conversations in group settings (i.e. a large dinner or multi family gathering for the holidays) while using cheaper off the shelf components. 

Requirements:
- 1 ms latency maximum
- capable of running on Daisy Seed Microcontroller
- only one microphone - the benefit of 2 microphones is having them in different locations (similar to stereo vision concepts), but the way I have it set up the cameras be right next to each other and would effectively capture the same signal. 
- filter able to handle non stationary signals

Given the varied nature of the signals that will be experienced, I am planning on designing an adaptive FIR filter. 

FIR choice: I am planning on designing an FIR filter. Even though FIR filters are more computationally expensive and slower than IIR, they are inherently stable (no poles - no chance for instability with denominator going to 0), and they can achieve linear phase response (preserves order).

In the filter: 
e(n) = d(n) - y(n), where e(n) is the error or clean speech signal, d(n) is the desired signal, and y(n) is the output signal after the FIR filter. There is a negative feedback loop that runs until the MSE is minimized using gradient descent. 

The general flow im going for:
Input signal -> windowing function -> subband analysis (filter bank) -> parallel processing per subband for subband NLMS (VAD feature extraction, noise statistics estimation, iterative signal reconstruction)-> subband synthesis -> output signal

Adaptive Filter Choice: I chose subband NLMS for the adaptive filter because at a high level it meets the computational, convergence speed (N part), and the subband aspect of breaking apart the input signal into smaller bands helps with computational cost and performance. 

Noise Handling: The reason I need the VAD feature extraction and noise estimation is because I am using only one microphone. With the way the adaptive filter works I am subtracting the noise from the original signal and preserving just the speech.

Windowing: Going with a Hamming window as it is better suited for reducing spectral leakage and maintaining more of the speech features because it has a wider main lobe and lower side lobes. 


Playground.py: This is a python script I created to visualize the audio signals and what happens to them when I apply the different steps of the process detailed above to them. Once I get this working I will transition it to C++ to go on the daisy seed. 








#include "daisy_seed.h"
#include "daisysp.h"

using namespace daisy;
using namespace daisysp;

DaisySeed hw;
daisysp::Oscillator osc;

//bool blink_light = false;

//Nyquist criterion (Hz) -> > 2 * max freq
//max freq = 20khz 
//constexpr int SAMPLE_RATE = 24000;

constexpr int SAMPLE_BUFFER_SIZE = 4;
//why 1024? power of 2 requirement for fft, frequency resolution
//buffer size is a good mix between memory and freq resolution

//bool led_state = true;

void AudioCallback(AudioHandle::InputBuffer in, AudioHandle::OutputBuffer out, size_t size)
{
	// static float phase = 0.0f;
	// float freq = 1000.0f; // 1 kHz test tone
	// float sample_rate = 1000.0f;

	for(size_t i = 0; i < size; i++){
		out[0][i] = in[0][i];
		out[1][i] = in[1][i];
	}
	
	
}

// void create_hann_window(float* window, int size) {
//     for(int i = 0; i < size; i++){
//         window[i] = 0.5f * (1.0f - cosf((2.0f * M_PI * i)/(size-1)));
//     }
// }


int main(void)
{


	hw.Init();

	//hw.StartLog(true);

	//hw.PrintLine("Hello World!");

	hw.SetAudioBlockSize(SAMPLE_BUFFER_SIZE); // number of samples handled per callback
	hw.SetAudioSampleRate(SaiHandle::Config::SampleRate::SAI_48KHZ);
	osc.Init(hw.AudioSampleRate());
	osc.SetFreq(440.0f);
	hw.StartAudio(AudioCallback);

	//hw.SetLed(led_state);
	

	while(1) {

	}
}

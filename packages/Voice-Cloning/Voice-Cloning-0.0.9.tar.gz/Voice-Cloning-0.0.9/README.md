Voice_Cloning is a Python package that allows users to synthesize speech and clone voices using Artificial Intelligence techniques. With Voice_Cloning, users can create their own text-to-speech systems, generate audio from text, and even clone their own voice to create a personalized speech model. Voice_Cloning is a powerful tool for anyone looking to add speech synthesis or voice cloning capabilities to their projects, whether it be for personal use or commercial applications.

## Disclaimer
The Voice_Cloning Python package is intended to be used as a tool to assist individuals who have lost their voice due to medical conditions or surgeries. While it can generate synthetic speech that sounds similar to a person's natural voice, it is not intended to replace the natural human voice, nor is it a guarantee that the synthetic voice created will sound exactly like the person's natural voice.

Furthermore, we strongly advise against using this package for any illegal or unethical purposes that may harm individuals or society as a whole. We do not condone or support any misuse of this technology and will not be held responsible for any consequences resulting from such misuse.

It is the responsibility of the user to ensure that they are using this technology in an ethical and responsible manner, in compliance with all applicable laws and regulations.

By using the Voice_Cloning Python package, you agree to these terms and acknowledge that you understand the limitations and potential risks associated with this technology.

| Feature  | Output  |
|---|---|
| Real-time voice cloning | The package can clone a user's voice in real time by analyzing a reference voice clip and a user's speech input |
| Speech synthesis | Allow users to generate synthetic speech using a text input with pre-loaded speakers, similar to a text-to-speech (TTS) system |
| Multi-Accent support | Supports Indian and Western-style accents for voice cloning and speech synthesis |
| Noise reduction | The package includes functions to reduce noise in the recorded audio, improving the quality of the cloned or synthesized voice |

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Voice-Cloning

```bash
pip install voice-cloning
```

## Usage

### 1. Clone using an external reference voice
```python
# load all the functions
from voice_cloning.generation import *

# provide a reference sound file, speech text and clone the voice
sound_path = r"xx/xxx/xxx.wav" # support most of the sound formats
speech_text = "Please use this package carefully"

generated_wav = speech_generator(
    voice_type = "western", # supports "indian" & "western"
    sound_path = sound_path, 
    speech_text=  speech_text
    )

## Play and save the sound with noise-reduction capabilities

# play the generated sound
play_sound(generated_wav)

# save the file
save_sound(generated_wav, filename="voice output", noise_reduction=True) # enable noise reduction

```

### 2. Speech Synthesis: Use an existing voice from the sound library
the sound library offers support to both "western & "indian" sounds, with 31 speaker voices
library: https://github.com/dreji18/Voice_Cloning/blob/main/speakers/speaker_library.xlsx

```python

# load all the functions
from voice_cloning.generation import *

speech_text = "Please use this package carefully"

# play the speaker sound and generate the voice
play_library_sound(voice_type = "western", gender = "female", speaker_id = "speaker-3") 

play_library_sound(voice_type = "indian", gender = "male", speaker_id = "speaker-1") # complete list available in the repo, 

generated_wav = speech_generator(
    voice_type = "western", 
    gender = "male", 
    speaker_id = "speaker-4", 
    speech_text= speech_text
    )

# play the generated sound & save the file
play_sound(generated_wav)

save_sound(generated_wav, filename="voice output", noise_reduction=True) # enable noise reduction

```

## About
This Package is part of the Research Topic "Voice_Cloning: A Python library for Speech Synthesis and Voice Cloning to assist Individuals with Speech Disorders" conducted by R. Vinotha, L.D Vijay Anand, Hepsiba D, Deepak John Reji. If you use this work (code, model or dataset),

Please cite us and star at: https://github.com/dreji18/Voice_Cloning

## License
[MIT](https://choosealicense.com/licenses/mit/) License

############################################################################################
#Licensed under the Apache License, Version 2.0 (the "License");
#you may not use this file except in compliance with the License.
#You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
#Unless required by applicable law or agreed to in writing, software
#distributed under the License is distributed on an "AS IS" BASIS,
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#See the License for the specific language governing permissions and
#limitations under the License.
############################################################################################
from setuptools import setup, find_packages

def readme():
    with open("README.md") as f:
        README = f.read()
    return README


required = """inflect==5.3.0
librosa==0.8.1
matplotlib
numpy
Pillow
scikit-learn
scipy
sounddevice
SoundFile
tqdm
umap-learn
Unidecode
urllib3
visdom
webrtcvad
noisereduce
torch"""

required = required.split("\n")


#with open("requirements-optional.txt") as f:
#    optional_required = f.read().splitlines()

setup(
    name="Voice-Cloning",
    version="0.0.9",
    description="Introducing Voice_Cloning: A Python Package for Speech Synthesis and Voice Cloning!",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/dreji18/Voice_Cloning",
    author="Deepak John Reji",
    author_email="deepakjohn1994@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    package_data={'voice_cloning': ['saved_models', 'encoder/data_objects/*', 'synthesizer/models/*', 'synthesizer/utils/*', 'vocoder/*', 'vocoder/models/*', 'speakers/indian/female/*', 'speakers/indian/male/*', 'speakers/western/male/*', 'speakers/western/female/*', 'speakers/speaker_library.xlsx']},
    license_files=("LICENSE",),
    install_requires=required,
)
# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['video_vocal_rt']

package_data = \
{'': ['*']}

install_requires = \
['moviepy>=1.0.3,<2.0.0',
 'numpy>=1.24.2,<2.0.0',
 'opencv-python>=4.7.0.72,<5.0.0.0',
 'openpyxl>=3.1.2,<4.0.0',
 'pysimplegui>=4.60.4,<5.0.0',
 'scipy>=1.10.1,<2.0.0',
 'sounddevice>=0.4.6,<0.5.0']

setup_kwargs = {
    'name': 'video-vocal-rt',
    'version': '0.3.2',
    'description': 'Video-Vocal-RT: a minimal package for vocal response to video',
    'long_description': '# video-vocal-RT\nA minimal package to record vocal response to video stimuli. Useful for vocal reaction time research with video stimuli instead of pictures. Uses open CV for video playing, among other things.\n\n# Usage\nI will provide more information soon 😉\n\n## Installation with pip\n```\npip install video-vocal-rt\n```\n\n## Installation with poetry\nFirst, clone the repository\n```\ngit clone https://github.com/LoonanChauvette/video-vocal-RT.git\n```\nThen, inside the package folder, install the dependencies with poetry\n```\ncd video-vocal-RT\npoetry install\n```\nPoetry creates a virtual environment, you should be able to activate it using : \n```\npoetry shell\n```\nThen you can run the script using : \n```\npoetry run python video_vocal_rt/main.py\n```\n\n## How-to \nPlace your video files in the VIDEO_FILES directory (only supports .avi files for now). For the moment, you need to go inside video_vocal_rt/main.py before running the experiement. There you should make sure to set the audio recording duration in seconds (default is 6 seconds, but should be the typical length of your videos). You also need to set the PARTICIPANT_ID to the desired value. \n\nYou can also set fixation parameters with FIXATION_DUR for the duration (default is 1000 ms). You can provide change the file "fixation.png" to customize the fixation. By default, there is a whiteout period after the video, its duration can be changed with WHITEN_DUR (default is 1000 ms).\n\n# Citation\n \n```\nChauvette, L. (2023). Video-Vocal-RT: a minimal package for vocal response to video.\nhttps://github.com/LoonanChauvette/video-vocal-RT\n````\n\nBibtex:\n```\n@manual{Video-Vocal-RT,\n  title={{Video-Vocal-RT: a minimal package for vocal response to video}},\n  author={{Chauvette, Loonan}},\n  year={2023},\n  url={https://github.com/LoonanChauvette/video-vocal-RT},\n}\n```',
    'author': 'Loonan Chauvette',
    'author_email': 'loonan.chauvette@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/LoonanChauvette/video-vocal-RT',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<3.12',
}


setup(**setup_kwargs)

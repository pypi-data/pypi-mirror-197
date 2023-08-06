# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['meetingscribe']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp[all]>=3.8.4,<4.0.0',
 'cchardet[all]>=2.1.7,<3.0.0',
 'openai[all]>=0.27.2,<0.28.0',
 'pydub[all]>=0.25.1,<0.26.0',
 'pysrt[all]>=1.1.2,<2.0.0',
 'rich==10.11.0',
 'srt[all]>=3.5.2,<4.0.0',
 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['meeting = meetingscribe.main:app',
                     'meetingscribe = meetingscribe.main:app']}

setup_kwargs = {
    'name': 'meetingscribe',
    'version': '0.1.0',
    'description': 'MeetingScribe is an AI-driven command-line tool designed to streamline your meeting experience by handling transcription, translation, and note-taking. Effortlessly generate accurate translation/transcription in English from audio file. Additionally, the tool intelligently creates meeting notes, summaries, and identifies action items.',
    'long_description': "# MeetingScribe\n\nAI-driven command-line tool designed to streamline your meeting experience by handling transcription, translation, and note-taking. Effortlessly generate accurate translation/transcription in English from audio file. Additionally, the tool intelligently creates meeting notes, summaries, and identifies action items.\n\nPowered by OpenAI's GPT-3 and Whisper API\n\n**Prerequisites**:\n\n1. Specify [OpenAI API Key](https://platform.openai.com/account/api-keys):\n\n```console\nexport OPENAI_API_KEY=<your-openai-api-key>\n```\n\n2. Install [FFmpeg](https://ffmpeg.org/download.html)\n\n**Installation**:\n\n<details>\n\n<summary>\nusing <code>pip</code>\n</summary>\n\n```console\nexport OPENAI_API_KEY=<your-openai-api-key>\n\ndocker run -it -e OPENAI_API_KEY=$OPENAI_API_KEY ghcr.io/0x77dev/meetingscribe --help\n```\n\n</details>\n\n<details>\n\n<summary>\nusing <code>docker</code>\n</summary>\n\n```console\nexport OPENAI_API_KEY=<your-openai-api-key>\n\ndocker run -it -e OPENAI_API_KEY=$OPENAI_API_KEY ghcr.io/0x77dev/meetingscribe --help\n```\n\n</details>\n\n**Usage**:\n\n```console\nmeeting [OPTIONS] COMMAND [ARGS]...\n```\n\n**Options**:\n\n- `--install-completion`: Install completion for the current shell.\n- `--show-completion`: Show completion for the current shell, to copy it or customize the installation.\n- `--help`: Show this message and exit.\n\n**Commands**:\n\n- `process`: Transcribe (and optionally translate to English) audio file into SRT file\n- `srt2txt`: Transform SRT file to TXT file\n- `summarize`: Generate meeting summary, notes, and action items from SRT file\n\n## `meeting process`\n\nTranscribe (and optionally translate) audio file into SRT file\nTranslation will translate from source language to English\n\n**Usage**:\n\n```console\nmeeting process [OPTIONS] INPUT_AUDIO_FILE\n```\n\n**Arguments**:\n\n- `INPUT_AUDIO_FILE`: [required]\n\n**Options**:\n\n- `--output-srt-file TEXT`: [default: output.srt]\n- `--source-language TEXT`\n- `--segment-length INTEGER`: [default: 600000]\n- `--help`: Show this message and exit.\n\n## `meeting srt2txt`\n\nTransform SRT file to TXT file\n\n**Usage**:\n\n```console\nmeeting srt2txt [OPTIONS]\n```\n\n**Options**:\n\n- `--srt-file TEXT`: [default: output.srt]\n- `--output-file TEXT`: [default: output.txt]\n- `--help`: Show this message and exit.\n\n## `meeting summarize`\n\nGenerate meeting summary, notes, and action items from SRT file\n\n**Usage**:\n\n```console\nmeeting summarize [OPTIONS]\n```\n\n**Options**:\n\n- `--input-srt-file TEXT`: [default: output.srt]\n- `--output-summary-file TEXT`: [default: output.md]\n- `--help`: Show this message and exit.\n",
    'author': 'Mykhailo Marynenko',
    'author_email': 'mykhailo@0x77.dev',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/0x77dev/meetingscribe',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)

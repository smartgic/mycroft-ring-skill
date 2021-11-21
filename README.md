[![Build Status](https://travis-ci.com/smartgic/mycroft-ring-skill.svg?branch=20.8.1)](https://travis-ci.com/github/smartgic/mycroft-ring-skill) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![contributions welcome](https://img.shields.io/badge/contributions-welcome-pink.svg?style=flat)](https://github.com/smartgic/mycroft-ring-skill/pulls) [![Skill: MIT](https://img.shields.io/badge/mycroft.ai-skill-blue)](https://mycroft.ai) [![Discord](https://img.shields.io/discord/809074036733902888)](https://discord.gg/Vu7Wmd9j)


<p align="center">
  <img alt="Mycrof Ring Skill" src="docs/mycroft-ring-logo.png" width="500px">
</p>

# Ring

Retrieve alerts from Ring devices such as the Doorbell, Chime, Camera.

## About

[Ring](https://www.ring.com) is the company behind the smart doorbell that contains a high-definition camera, a motion sensor, and a microphone and speaker for two-way audio communication.

This skill allows Mycroft to notify you if someone at your front door.

## Examples

* "discover my ring devices"


## Installation

Make sure to be within the Mycroft `virtualenv` before running the `msm` command.

```
$ . mycroft-core/venv-activate.sh
$ msm install https://github.com/smartgic/mycroft-ring-skill.git
```

## Configuration

This skill utilizes the `settings.json` file which allows you to configure this skill via `home.mycroft.ai` after a few seconds of having the skill installed you should see something like below in the https://home.mycroft.ai/#/skill location:

<img src='docs/ring-config.png' width='450'/>

Fill this out with your appropriate information and hit the `save` button.


## Credits

- [Smart'Gic](https://smartgic.io/)
- [python_ring_doorbell](https://github.com/tchellomello/python-ring-doorbell)
- [SoundBible](https://soundbible.com/)

## Category

**IoT & Home**

## Tags

#camera
#iot
#doorbell
#ring
#device
#smart
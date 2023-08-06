# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['neon_homeassistant_skill']

package_data = \
{'': ['*'], 'neon_homeassistant_skill': ['dialog/en-us/*', 'vocab/en-us/*']}

install_requires = \
['pfzy>=0.3.4,<0.4.0']

entry_points = \
{'console_scripts': ['neon-homeassistant-skill = '
                     'neon_homeassistant_skill:NeonHomeAssistantSkill'],
 'ovos.plugin.skill': ['neon_homeassistant_skill.mikejgray = '
                       'neon_homeassistant_skill:NeonHomeAssistantSkill']}

setup_kwargs = {
    'name': 'neon-homeassistant-skill',
    'version': '0.0.9',
    'description': 'A Neon AI Skill for Home Assistant, which integrates with ovos-PHAL-plugin-homeassistant.',
    'long_description': "# Home Assistant Neon Skill\n\nUses [PHAL Home Assistant plugin](https://github.com/OpenVoiceOS/ovos-PHAL-plugin-homeassistant)\n\nStill a work in progress - PRs and issues welcome\n\nAvailable on PyPi: `pip install neon-homeassistant-skill`\n\n## Installation on Neon\n\nInstall ovos-PHAL-plugin-homeassistant [per their documentation](https://github.com/OpenVoiceOS/ovos-PHAL-plugin-homeassistant)\nNote that Neon uses a YAML configuration, not a JSON file, so edit ~/.config/neon/neon.yaml and make the following update for a minimal installation:\n\n```yaml\nPHAL:\n  ovos-PHAL-plugin-homeassistant:\n    host: http://<HA_IP_OR_HOSTNAME>:8123\n    api_key: <HA_LONG_LIVED_TOKEN>\n```\n\nYou can also say `open home assistant dashboard` on a device with a screen, like the Mark 2, and use the OAuth login flow from the PHAL plugin.\n\nSSH to the Neon device\n\n```shell\nosm install https://github.com/mikejgray/neon-homeassistant-skill\n```\n\n## Upcoming Features\n\n- Start OAuth workflow with voice\n- Start an instance of the ovos-PHAL-plugin-homeassistant if PHAL isn't already running\n- Vacuum functions\n- HVAC functions\n",
    'author': 'Mike Gray',
    'author_email': 'mike@graywind.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)

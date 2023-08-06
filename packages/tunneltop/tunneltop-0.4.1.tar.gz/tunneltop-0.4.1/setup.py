# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tunneltop']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['tunneltop = tunneltop.tunneltop:main']}

setup_kwargs = {
    'name': 'tunneltop',
    'version': '0.4.1',
    'description': 'A top-like tunnel manager',
    'long_description': '# tunneltop\nA tunnel manager in the familiar top style written with ncurses and asyncio.\n\n![Image](tunneltop.png)\n\n## Install\n```sh\npip install tunneltop\n```\n\n## what it is\n* a simple tunnel manager written in python that uses the standard library only(standard library only in python 3.11)\n* it starts and manages the tunnels for you\n* lets the user interactively manage the tunnels as well\n* will reload the config file if it receives a `SIGHUP`\n* it is intentionally written as simple and tunnel-agnostic\n* may or may not work on windows(let me know if you test it on windows)\n\n## toml file\n\ntunneltop expects its config file to be at at `$HOME/.tunneltoprc`.\n\nYou can see an example config file below:</br>\n```toml\n[color]\nheader_fg = 4\nheader_bg = 0\nactive_fg = 23\nactive_bg = 0\ndisabled_fg = 8\ndisabled_bg = 0\ntimeout_fg = 63\ntimeout_bg = 0\nunknown_fg = 38\nunknown_bg = 0\ndown_fg = 208\ndown_bg = 0\nbox_fg = 22\nbox_bg = 0\n\n[tunnel.socks5ir]\naddress = "127.0.0.1"\nport = 9997\ncommand = "autossh -M 0 -N -D 9997 -o ServerAliveInterval=180 -o ServerAliveCountMax=3 -o ExitOnForwardFailure=yes -l debian -p 22 100.100.100.101"\ntest_command = \'curl -s -o /dev/null -s -w "%{http_code}" -k -I -4 --socks5 socks5h://127.0.0.1:9997 https://icanhazip.com\'\ntest_command_result = "200"\ntest_interval = 300\ntest_timeout = 10\nauto_start = false\n\n[tunnel.socks5_3]\naddress = "127.0.0.1"\nport = 9995\ncommand = "autossh -M 0 -N -D 0.0.0.0:9995 -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o VerifyHostKeyDNS=no -o ServerAliveInterval=180 -o ServerAliveCountMax=3 -o ExitOnForwardFailure=yes -l debian -p 2022 100.100.100.100"\ntest_command = \'curl -s -o /dev/null -s -w "%{http_code}" -k -I -4 --socks5 socks5h://127.0.0.1:9995 https://icanhazip.com\'\ntest_command_result = "200"\ntest_interval = 300\ntest_timeout = 10\nauto_start = true\n```\n\nThe tunnel names must be unique.</br>\n\n### address\nDisplays the address at which the tunnel is available at. It is a display-only option.</br>\n\n### port\nDisplays the port at which the tunnel is available at. It is a display-only option.</br>\n\n### command\nThe command used to start the tunnel.</br>\n\n### test_command\nThe command used to test the state of the tunnel.</br>\n\n### test_command_result\nThe expected result of the test command.</br>\n\n### test_interval\nHow often should the `test_command` be run.</br>\n\n### test_timeout\nHow long before the test is considered to have timed out.</br>\n\n### auto_start\nWhether to automatically start this tunnel  on startup.</br>\n\n## keybindings\n`j` and `k` move you up and down.</br>\n\n`g` and `G`move you to the first or last tunnel.</br>\n\n`s` toggles a tunnel from enabled to disabled or vice versa.</br>\n\n`r`  restarts a tunnel.</br>\n\n`t` runs the test right now.</br>\n\nTo quit send a `SIGINT` or a `SIGTERM`. I\'m working on improving this of course.</br>\n\ntunneltop will reload its config file upon receiving a `SIGHUP` and apply the changes immediately if there are any.</br>\n',
    'author': 'terminaldweller',
    'author_email': 'devi@terminaldweller.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/terminaldweller/tunneltop',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)

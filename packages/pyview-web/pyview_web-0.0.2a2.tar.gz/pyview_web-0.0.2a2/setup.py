# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyview',
 'pyview.changesets',
 'pyview.examples.succulents',
 'pyview.template',
 'pyview.vendor',
 'pyview.vendor.flet.pubsub',
 'pyview.vendor.ibis']

package_data = \
{'': ['*'],
 'pyview': ['assets/*',
            'assets/js/*',
            'static/assets/*',
            'static/examples/succulents/*']}

install_requires = \
['APScheduler==3.9.1.post1',
 'fastapi==0.89.1',
 'psutil>=5.9.4,<6.0.0',
 'uvicorn==0.20.0',
 'wsproto==1.2.0']

setup_kwargs = {
    'name': 'pyview-web',
    'version': '0.0.2a2',
    'description': 'LiveView in Python',
    'long_description': '<img src="https://pyview.rocks/images/pyview_logo_512.png" width="128px" align="right" />\n\n# PyView\n\n> A Python implementation of Phoenix LiveView\n\nPyView enables dynamic, real-time web apps, using server-rendered HTML.\n\n**Source Code**: <a href="https://github.com/ogrodnek/pyview" target="_blank">https://github.com/ogrodnek/pyview</a>\n\n# Installation\n\n`pip install pyview-web`\n\n# Live Examples\n\n[https://examples.pyview.rocks/](https://examples.pyview.rocks/)\n\n## Simple Counter\n\n[See it live!](https://examples.pyview.rocks/counter)\n\ncount.py:\n\n```python\nfrom pyview import LiveView, LiveViewSocket\nfrom typing import TypedDict\n\n\nclass CountContext(TypedDict):\n    count: int\n\n\nclass CountLiveView(LiveView[CountContext]):\n    async def mount(self, socket: LiveViewSocket[CountContext]):\n        socket.context = {"count": 0}\n\n    async def handle_event(self, event, payload, socket: LiveViewSocket[CountContext]):\n        if event == "decrement":\n            socket.context["count"] -= 1\n\n        if event == "increment":\n            socket.context["count"] += 1\n\n    async def handle_params(self, url, params, socket: LiveViewSocket[CountContext]):\n        # check if "c" is in params\n        # and if so set self.count to the value\n        if "c" in params:\n            socket.context["count"] = int(params["c"][0])\n```\n\ncount.html:\n\n```html\n<div>\n  <h1>Count is {{count}}</h1>\n  <button phx-click="decrement">-</button>\n  <button phx-click="increment">+</button>\n</div>\n```\n\n# Acknowledgements\n\n- Obviously this project wouldn\'t exist without [Phoenix LiveView](https://github.com/phoenixframework/phoenix_live_view), which is a wonderful paradigm and implementation. Besides using their ideas, we also directly use the LiveView JavaScript code.\n- Thanks to [Donnie Flood](https://github.com/floodfx) for the encouragement, inspiration, help, and even pull requests to get this project started! Check out [LiveViewJS](https://github.com/floodfx/liveviewjs) for a TypeScript implementation of LiveView (that\'s much more mature than this one!)\n\n- Thanks to [Darren Mulholland](https://github.com/dmulholl) for both his [Let\'s Build a Template Language](https://www.dmulholl.com/lets-build/a-template-language.html) tutorial, as well as his [ibis template engine](https://github.com/dmulholl/ibis), which he very generously released into the public domain, and forms the basis of templating in PyView.\n\n# Running the included Examples\n\n## Setup\n\n```\npoetry install\n```\n\n## Running\n\n```\npoetry run uvicorn examples.app:app --reload\n```\n\nThen go to http://localhost:8000/\n\n### Poetry Install\n\n```\nbrew install pipx\npipx install poetry\npipx ensurepath\n```\n\n# License\n\nPyView is licensed under the [MIT License](LICENSE).\n',
    'author': 'Larry Ogrodnek',
    'author_email': 'ogrodnek@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://pyview.rocks',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9.16,<4.0.0',
}


setup(**setup_kwargs)

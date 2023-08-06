<img src="https://pyview.rocks/images/pyview_logo_512.png" width="128px" align="right" />

# PyView

> A Python implementation of Phoenix LiveView

PyView enables dynamic, real-time web apps, using server-rendered HTML.

**Source Code**: <a href="https://github.com/ogrodnek/pyview" target="_blank">https://github.com/ogrodnek/pyview</a>

# Installation

`pip install pyview-web`

# Live Examples

[https://examples.pyview.rocks/](https://examples.pyview.rocks/)

## Simple Counter

[See it live!](https://examples.pyview.rocks/counter)

count.py:

```python
from pyview import LiveView, LiveViewSocket
from typing import TypedDict


class CountContext(TypedDict):
    count: int


class CountLiveView(LiveView[CountContext]):
    async def mount(self, socket: LiveViewSocket[CountContext]):
        socket.context = {"count": 0}

    async def handle_event(self, event, payload, socket: LiveViewSocket[CountContext]):
        if event == "decrement":
            socket.context["count"] -= 1

        if event == "increment":
            socket.context["count"] += 1

    async def handle_params(self, url, params, socket: LiveViewSocket[CountContext]):
        # check if "c" is in params
        # and if so set self.count to the value
        if "c" in params:
            socket.context["count"] = int(params["c"][0])
```

count.html:

```html
<div>
  <h1>Count is {{count}}</h1>
  <button phx-click="decrement">-</button>
  <button phx-click="increment">+</button>
</div>
```

# Acknowledgements

- Obviously this project wouldn't exist without [Phoenix LiveView](https://github.com/phoenixframework/phoenix_live_view), which is a wonderful paradigm and implementation. Besides using their ideas, we also directly use the LiveView JavaScript code.
- Thanks to [Donnie Flood](https://github.com/floodfx) for the encouragement, inspiration, help, and even pull requests to get this project started! Check out [LiveViewJS](https://github.com/floodfx/liveviewjs) for a TypeScript implementation of LiveView (that's much more mature than this one!)

- Thanks to [Darren Mulholland](https://github.com/dmulholl) for both his [Let's Build a Template Language](https://www.dmulholl.com/lets-build/a-template-language.html) tutorial, as well as his [ibis template engine](https://github.com/dmulholl/ibis), which he very generously released into the public domain, and forms the basis of templating in PyView.

# Running the included Examples

## Setup

```
poetry install
```

## Running

```
poetry run uvicorn examples.app:app --reload
```

Then go to http://localhost:8000/

### Poetry Install

```
brew install pipx
pipx install poetry
pipx ensurepath
```

# License

PyView is licensed under the [MIT License](LICENSE).

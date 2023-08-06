from dataclasses import dataclass
from .data import Plant, suggest, search
from pyview import LiveView, LiveViewSocket
from typing import Optional


@dataclass
class PlantsContext:
    plant: str
    result: Optional[Plant]
    matches: list[Plant]


class PlantsLiveView(LiveView[PlantsContext]):
    async def mount(self, socket: LiveViewSocket[PlantsContext]):
        socket.context = PlantsContext("", None, [])

    async def handle_event(self, event, payload, socket: LiveViewSocket[PlantsContext]):
        if event == "plant-suggest":
            if "plant" in payload:
                socket.context.plant = payload["plant"][0]
                socket.context.matches = suggest(payload["plant"][0])
            return

        if event == "plant-search":
            if "plant" in payload:
                p = payload["plant"][0]
                socket.context.plant = p
                found = search(p)
                if found:
                    socket.context.result = found

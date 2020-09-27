from types import MethodType

from .utils import quickembed


def start_included(self, start, end):
    for event in self:
        if (start <= event.begin <= end):
            yield event


def rrule(self):
    for c_line in self.extra:
        if c_line.name == 'RRULE':
            return c_line.value
    return None


def timeline_patch(t):
    t.start_included = MethodType(start_included, t)
    return t


def event2embed(e):
    return quickembed(e.name, e.description, e.begin, e.end)

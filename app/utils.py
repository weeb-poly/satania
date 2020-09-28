from typing import List, TypeVar

from arrow import Arrow
from discord import Embed
from discord.utils import sleep_until
from html2markdown import convert as html2md

T = TypeVar('T')

async def sleep_till(a: Arrow) -> None:
    await sleep_until(a.datetime)

def divide_chunks(arr: List[T], n: int) -> List[List[T]]:
    return [arr[i * n : (i + 1) * n] for i in range((len(arr) + n - 1) // n)]

def quickembed(name: str, desc: str, begin: Arrow, end: Arrow) -> Embed:
    return Embed(
        title = name,
        description = html2md(desc)
    ).add_field(
        name = "Start",
        value = begin.to('local').ctime()
    ).add_field(
        name = "End",
        value = end.to('local').ctime()
    )

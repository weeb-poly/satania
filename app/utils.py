from discord import Embed
import html2markdown


def divide_chunks(arr, n):
    return [arr[i * n : (i + 1) * n] for i in range((len(arr) + n - 1) // n)]


def quickembed(name, desc, begin, end):
    return Embed(
        title = name,
        description = html2markdown.convert(desc)
    ).add_field(
        name = "Start",
        value = begin.to('local').ctime()
    ).add_field(
        name = "End",
        value = end.to('local').ctime()
    )

import asyncio

from .transformer import transform

# --------------------------------------------------------------------
# helper functions


async def segment_comment(comment_data: dict[str, str]):
    """The segment_comment function segments the `content` value from `comment_data`.

    Args:
        comment_data (dict): a dict containing the comment data
    Returns:
        a dict: {
            'type': 'pos',
            'author': 'lixing',
            'content': [[
                ('我', 'Nh'),
                ('喜歡', 'VK'),
                ('程式', 'Na')
            ]],
            'order': '1',
        }
    """
    content = await transform(comment_data["content"])
    return {**comment_data, "content": content}


async def segment_comments(list_of_comments: list[dict[str, str]]):
    """The segment_comments function segments a list of comments."""
    return await asyncio.gather(*list(map(segment_comment, list_of_comments)))


# --------------------------------------------------------------------
# public interface


async def segment(data: str | list[str] | list[dict[str, str]]):
    """The segment function segments the `data` based on its type.

    Args:
        data (str | list): the post-related data (i.e title, body or comments)
    Returns:
        a list of dicts if the data refers to comments, a list of list of tuples
        otherwise.
    """
    is_comment_data = isinstance(data, list) and all(
        isinstance(value, dict) for value in data
    )

    if is_comment_data:
        return await segment_comments(data)

    return await transform(data)

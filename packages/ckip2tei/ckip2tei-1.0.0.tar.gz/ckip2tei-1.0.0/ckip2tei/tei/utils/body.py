def check_en_or_zh_chars(sentence: str) -> bool:
    """The check_en_or_zh_chars method checks whether the sentece is a English or Mandarin sentence.

    Args:
        sentence (str)
    Returns:
        True if the sentence is English or Mandarin, False otherwise.
    """
    return all(
        map(
            lambda value: not (19968 <= ord(value) <= 40869)
            and not (97 <= ord(value) <= 122)
            and not (65 <= ord(value) <= 90),
            sentence,
        )
    )


def validate_sentence(sentence: str) -> str | None:
    """The validate_sentence method validates whether the sentence is English or Mandarin.

    Args:
        sentence (str)
    Returns:
        a str if the sentence is English or Mandarin, None otherwise.
    """
    stripped_sentence = sentence.strip()

    if not check_en_or_zh_chars(stripped_sentence) and not stripped_sentence.startswith(
        "◆ From:"
    ):
        return stripped_sentence

    return None


def filter_body(sentence: str) -> list[str]:
    """The filter_body function filters the post body that are not English or Mandarin sentences.

    Args:
        sentence (str)
    Retunrs:
        a list of strings
    """
    output = map(validate_sentence, sentence.split("\n"))
    return list(filter(lambda value: value is not None, output))

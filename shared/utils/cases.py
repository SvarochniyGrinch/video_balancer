def to_camel_case(snake: str) -> str:
    if not snake:
        return snake
    result = ''.join(word.title() for word in snake.split('_'))
    if snake[0].islower():
        return result[0].lower() + result[1:]
    return result


def to_pascal_case(snake: str) -> str:
    if not snake:
        return snake
    return ''.join(word.title() for word in snake.split('_'))


__all__ = [
    "to_camel_case",
    "to_pascal_case",
]

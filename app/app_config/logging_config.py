import logging


def setup_logging():
    logging.basicConfig(
        level=logging.DEBUG,  # Change to INFO in prod
        format="%(asctime)s | %(levelname)s | %(name)s | %(funcName)s |%(message)s",
    )


def get_logger(name: str | None = None) -> logging.Logger:
    """
    Return a logger with the given name.
    By default the name will be caller module name
    """
    if name is None:
        name = __name__
    return logging.getLogger(name)

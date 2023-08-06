import functools
import logging
from datetime import datetime
from os import mkdir
from os.path import exists
from time import perf_counter
from typing import Any, Callable

if not exists('logs'):
    mkdir('logs')

log_path = 'logs'
filename = f"{datetime.now().strftime('%Y_%m_%d')}"
default_logger = logging.getLogger('default')
logging.basicConfig(
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S',
    format='%(asctime)s - [%(name)s] [%(levelname)s]: %(message)s',
    handlers=[
        logging.FileHandler(f'{log_path}/{filename}.log'),
        logging.StreamHandler(),
    ],
)


def benchmark_with(logger: logging.Logger):
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            start = perf_counter()
            result = func(*args, **kwargs)
            end = perf_counter()
            runtime = end - start
            logger.info(f'Execution of {func.__name__} took {runtime:.3f}.')
            return result

        return wrapper

    return decorator


def logging_with(logger: logging.Logger):
    def decorator(
        func: Callable[..., Any],
    ) -> Callable[..., Any]:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            logger.info(f'Calling {func.__name__}')
            result = func(*args, **kwargs)
            logger.info(f'Finished Calling {func.__name__}')
            return result

        return wrapper

    return decorator


default_logging = functools.partial(logging_with, logger=default_logger)
default_benchmark = functools.partial(benchmark_with, logger=default_logger)

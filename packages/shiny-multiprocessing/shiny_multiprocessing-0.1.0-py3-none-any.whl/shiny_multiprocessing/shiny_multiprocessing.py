from pebble import ProcessPool, ProcessFuture
from concurrent.futures import TimeoutError

from typing import List, Any, Iterable, Dict, Callable


class TooManyRetriesException(Exception):
    """ Dedicated exception to mark too many failed processing attempts. """
    pass


# helper exception for the example
class __TaskTimeoutError(TimeoutError):
    pass


def process_and_retry(
        function: Callable,
        items: Iterable[Dict[Any, Any]],
        max_retries_per_task: int = 3,
        retry_on_exceptions: List[Any] = (),
        timeout: float = None,
        log_function: Callable = None,
        pass_previous_attempts_key: str = None,
        *args,
        **kwargs,
) -> List[Any]:
    """ Invokes a provided function in parallel in multiple processes and provides retry and timeout logic.

    This function makes use of pebble's ProcessPool. It monitors all function calls' execution times
    and tracks per item, if the processing timed out or any other exception was raised, and orchestrates
    retrials on specified failures.

    :param function: Callable to executed in multiple processes.
    :param items: List of uniform dictionaries, where each dictionary establishes a set of parameters
        provided to a single function call in a process, i.e. the dictionary must match the function's
        signature.
    :param max_retries_per_task: Sets the number of times a single task is re-attempted upon failure.
        See also the parameter 'retry_on_exceptions'.
    :param retry_on_exceptions: List of exceptions upon which another attempt on the task is made. In
        case of any other exception or error, the whole process is crashed. See also the parameter
        'max_retries_per_task'.
    :param timeout: Maximum number of seconds a single task is allowed to take in a process. Passed
        on the pebble.ProcessPool.
    :param log_function: If set, caught failures (see 'retry_on_exceptions') are logged using this function. E.g.
        provide "logger.error".
    :param pass_previous_attempts_key: If not None, the list of previous failed attempts is passed as
        an additional keyword argument to the function. The function must accept the provided key as
        parameter of type List[Exception]!
    :param args: Positional arguments passed on to the pebble ProcessPool.
    :param kwargs: Keyword arguments passed on to the pebble ProcessPool.

    :return: The collected results from the successfully processed function calls.

    :raises:
        * TooManyRetriesException: If processing a task failed to many times.
        * Any exceptions raised by the called function.
    """
    results = list()

    with ProcessPool(
            *args,
            **kwargs
    ) as pool:

        retries = dict()
        for i in items:
            data = {'item': i, 'fails': []}
            if pass_previous_attempts_key is not None:
                i[pass_previous_attempts_key] = []
            future = pool.schedule(
                function,
                kwargs=i,
                timeout=timeout
            )
            retries[future] = data

        while len(retries) > 0:
            new_retries = {}
            for future in retries:
                exc = future.exception()
                if exc is not None:
                    if exc.__class__ not in retry_on_exceptions:
                        raise exc
                    data = retries[future]
                    data['fails'].append(exc)

                    if log_function is not None:
                        msg = f'Task {future} had failed attempts:\n'
                        for fail in retries[future]['fails']:
                            msg += f'\t* {fail.__class__}: {fail}'
                        log_function(msg)

                    if len(data['fails']) >= max_retries_per_task:
                        __stop_all_retries([retries, new_retries])
                        raise TooManyRetriesException(f'{future} failed too many times! All processes stopped!')

                    item = data['item']
                    if pass_previous_attempts_key is not None:
                        item[pass_previous_attempts_key] = data['fails']

                    new_future = pool.schedule(
                        function,
                        kwargs=item,
                        timeout=timeout
                    )
                    new_retries[new_future] = data
                else:
                    results.append(future.result())

            retries = new_retries
    return results


def __stop_all_retries(
        retries_list: List[Dict[ProcessFuture, Dict[str, Any]]]
) -> None:
    for retries in retries_list:
        for future in retries:
            future.cancel()

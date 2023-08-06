from functools import lru_cache


@lru_cache
def running_in_ipython() -> bool:
    try:
        return bool(__IPYTHON__)  # type: ignore
    except NameError:
        return False

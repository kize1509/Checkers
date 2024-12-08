import threading

class FunctionTimeoutError(Exception):
    pass

def function_with_timeout(func, core, timeout=15):
    result_container = [None]

    def wrapper():
        result_container[0] = func(core)

    thread = threading.Thread(target=wrapper)
    thread.start()
    thread.join(timeout)

    if thread.is_alive():
        raise FunctionTimeoutError(f"Function did not complete within {timeout} seconds")

    return result_container[0]
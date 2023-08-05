import os
import platform
import signal
import threading
from pathlib import Path

import psutil  # type: ignore

IS_WINDOWS = os.name == "nt"


def robocorp_home():
    """Get the absolute path to the user's Robocorp home folder.
    Prefers environment variable ROBOCORP_HOME, if defined.
    """
    env = os.getenv("ROBOCORP_HOME", "")

    if env.strip():
        path = Path(env)
    elif platform.system() == "Windows":
        path = Path.home() / "AppData" / "Local" / "robocorp"
    else:
        path = Path.home() / ".robocorp"

    return path.resolve()


def set_interval(interval):
    """Decorator for calling function every `interval` seconds.
    Starts after first function invocation.
    """
    interval = float(interval)

    def decorator(function):
        def wrapper(*args, **kwargs):
            stop = threading.Event()

            def loop():
                while not stop.wait(interval):
                    function(*args, **kwargs)

            thread = threading.Thread(target=loop)
            thread.daemon = True
            thread.start()
            return stop

        return wrapper

    return decorator


def force_kill_process(logger, pid=None, suspend=False):
    try:
        # if pid is None will kill all children of current process
        current_proc = psutil.Process(pid)
        _suspend_process(logger=logger, proc=current_proc, suspend=suspend)

        if current_proc.is_running():
            logger.debug("Stopping children of process: %s", current_proc.pid)
            # get the children of process
            children = _get_process_children(logger=logger, proc=current_proc)

            # go through the children and try to kill each one
            for child in children:
                try:
                    # if the child process has children, we go through those first
                    grandchildren = _get_process_children(logger=logger, proc=child)
                    if len(grandchildren) > 0:
                        force_kill_process(logger=logger, pid=child.pid)

                    # attempt to kill the child process
                    logger.debug("Stopping child process: %s", child.pid)
                    _send_kill_to_process(logger=logger, proc=child)
                except Exception as error:  # pylint: disable=W0703
                    logger.debug(
                        f"Continuing, but there was an error killing process: {error}"
                    )
            # check if there are any processes left (zombies) that we should kill
            _, alive = psutil.wait_procs(children, timeout=2)
            for child in alive:
                logger.debug(f"Killing process still alive: {child}")
                _send_kill_to_process(logger=logger, proc=child)

            # kill the process
            _send_kill_to_process(logger=logger, proc=current_proc)
        else:
            logger.debug("Process not running: %s", pid)
    except Exception as error:  # pylint: disable=W0703
        logger.debug(f"There was an error while killing process: {error}")


def _send_kill_to_process(logger, proc):
    try:
        if "SIGKILL" in signal.__dict__:
            os.kill(proc.pid, signal.SIGKILL)
        else:
            os.kill(proc.pid, signal.SIGTERM)
        proc.kill()
    except Exception as error:  # pylint: disable=W0703
        logger.debug(f"There was an error while killing process: {error}")


def _suspend_process(logger, proc, suspend=False):
    if suspend:
        try:
            logger.debug("Suspending process: %s", proc.pid)
            proc.suspend()
        except Exception as error:  # pylint: disable=W0703
            logger.debug(f"There was an error suspending process: {proc}: {error}")


def _get_process_children(logger, proc):
    try:
        return proc.children()
    except Exception as error:  # pylint: disable=W0703
        logger.debug(f"Error getting children for the process: {proc}: {error}")
    return []

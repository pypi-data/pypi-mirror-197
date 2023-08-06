import asyncio
import logging
import uuid
from asyncio import AbstractEventLoop, Queue, Task
from datetime import datetime
from typing import Callable

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import numpy as np
from data_access.visual_knowledge_db import SystemDB, UserDB
from entities.visual_knowledge_entities import System
from use_cases.visual_knowledge_cases import UserUseCases

from mvfy.use_cases.visual_knowledge_cases import SystemUseCases

from ..utils import index as utils


def async_scheduler(job: 'Callable', trigger: CronTrigger, *kargs) -> AsyncIOScheduler:
    """create a scheduler to be executed in future 

    :param job: _description_
    :type job: Callable
    :param trigger: _description_
    :type trigger: CronTrigger
    :param type: _description_, defaults to "cron"
    :type type: str, optional
    :return: _description_
    :rtype: _type_
    """
    _scheduler = AsyncIOScheduler()
    _scheduler.add_job(job, trigger = trigger, id = str(uuid.uuid4()), *kargs)
    _scheduler.start()

    return _scheduler
    
def loop_manager(func: 'Callable') -> 'Callable':
    """Decorator for Manage Event Loop.

    Args:
        func ([type]): callback async function
    
    Returns:
        (function): result of func
    """
    async def wrapper_function(*args, **kargs):
        loop = asyncio.get_event_loop()
        if loop is None:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return await func(*args, **kargs, loop = loop)
        
    return wrapper_function

async def async_queue_object_put(list: list[dict], keys: list[str], queue: 'Queue' = Queue()) -> None:
    """Generate Queue with object properties extracted

    Args:
        list (list[dict]): list of objects 
        keys (list[str]): list of pairs key:value, required
        queue (Queue, optional): [description]. Defaults to Queue().
    
    Example
        >>> ... await async_queue_object([..., {..., "system": 1}], ["system"])

    """
    for obj in list:
        await queue.put({
            f"{k}":v for k, v in obj.items() if k in keys
        })
    
    queue.task_done()

async def async_queue_object_get(queue: 'Queue', callback: 'function', args: tuple = ()) -> None:

    while not queue.empty():
        res = await queue.get()
        await callback(*args, queue_result=res)

    queue.task_done()

@loop_manager
async def load_user_descriptors(system_id: str, db: UserDB, loop: 'asyncio.AbstractEventLoop') -> 'utils.ThreadedGenerator|None':
    """Load user descriptors from database.

    Args:
        system_id (str): id of parent system
        db (str): data-base of users
        loop (asyncio.AbstractEventLoop): actual event loop

    Returns:
        list[dict]: [description]
    """

    use_cases = UserUseCases(db)
    results = await loop.run_in_executor(None, lambda: use_cases.get_users({
        "system_id": system_id
    }))


    if results is None or results == []:
        results = []

    return utils.extract_objects(results, ["detection", "author"])

@loop_manager
async def get_system(system: 'dict', db: SystemDB, loop: 'asyncio.AbstractEventLoop') -> 'dict|None':
    """Get information about a system.

    Returns:
        dict: system found
    """
    use_cases = SystemUseCases(db)
    result = await loop.run_in_executor(None, lambda: use_cases.get_system(system))

    if result == [] or result is None:
        return None

    return result

@loop_manager
async def insert_system(system: 'dict', db: SystemDB, loop: 'asyncio.AbstractEventLoop') -> 'dict|None':
    """add information about a system.

    Returns:
        str: id of system insert
    """
    use_cases = SystemUseCases(db)
    result = await loop.run_in_executor(None, lambda: use_cases.add_system(system))

    if result == [] or result is None:
        return None

    return result

@loop_manager
async def insert_user(user: 'dict', db: UserDB, loop: 'asyncio.AbstractEventLoop') -> 'dict|None':
    """add information about a user.

    Returns:
        str: id of user insert
    """
    use_cases = UserUseCases(db)
    result = await loop.run_in_executor(None, lambda: use_cases.add_user(user))

    if result == [] or result is None:
        return None

    return result

@loop_manager
async def find_user(filter: 'dict', db: UserDB, loop: 'asyncio.AbstractEventLoop') -> 'dict|None':
    """search information about a user.

    Returns:
        str: id of user insert
    """
    use_cases = UserUseCases(db)
    result = await loop.run_in_executor(None, lambda: use_cases.get_user(filter))

    if result == [] or result is None:
        return None

    return result

@loop_manager
async def get_users(_filter: 'dict', db: UserDB, loop: 'asyncio.AbstractEventLoop') -> 'list':
    """search information about users.

    Returns:
        list: list of users
    """
    use_cases = UserUseCases(db)
    result = await loop.run_in_executor(None, lambda: use_cases.get_users(_filter))

    if result == [] or result is None:
        return None

    return result

@loop_manager
async def remove_users_duplicate_detection(_filter: 'dict', db: UserDB, loop: 'asyncio.AbstractEventLoop') -> None:
    """search information about users.

    Returns:
        list: list of users
    """
    use_cases = UserUseCases(db)
    users = await loop.run_in_executor(None, lambda: use_cases.get_users(_filter))

    if users != [] or not (users is None):
        detections = None
        for user in users:
            if detections is None:
                detections = np.array([user.detection])
            else:
                distance = np.apply_along_axis(lambda row: utils.euclidean_distance(row, np.array(user.detection)), 1, detections)
from ._internal import Launch
import inspect
import functools
import asyncio
from typing import Union, Literal
import pytest

def _run_func(func, *args, **kwargs):
    __tracebackhide__ = True
    if inspect.iscoroutinefunction(func):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError as e:
            if "no running event loop" in str(e):
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            else:
                raise e

            return loop.run_until_complete(func(*args, **kwargs))

    return func(*args, **kwargs)


def _get_parent_name(*args):
    try:
        return str(args[0].__class__.__qualname__)
    except AttributeError:
        return ''

def _get_class_parent(child_class):
    for base_class in child_class.__bases__:
        base_class_name = base_class.__name__
        print(base_class_name)
        if base_class_name in Launch.items.keys():
            print('found')
            return base_class_name
        elif len(base_class.__bases__) > 0:
            result = _get_class_parent(base_class)
            if result:
                return result

@pytest.mark.skip(reason='')
def step(title: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            __tracebackhide__ = True
            parent = Launch.get_caller_name()
            name = title.format(*args, **kwargs)
            item_id = Launch.create_report_item(
                name=name,
                parent_item=parent,
                type='step',
                has_stats=False,
                description=func.__doc__)

            Launch.items[func.__name__] = item_id
            result = None
            try:
                result = _run_func(func, *args, **kwargs)

            except Exception as exception:
                Launch.finish_failed_item(func.__name__, str(exception))
                raise exception

            Launch.finish_passed_item(func.__name__)
            return result

        return wrapper
    return decorator

@pytest.mark.skip(reason='')
def title(title: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            __tracebackhide__ = True
            parent_class_name = _get_parent_name(*args)
            name = title.format(*args, **kwargs)
            item_id = Launch.create_report_item(
                name=name,
                parent_item=parent_class_name,
                type='test',
                description=func.__doc__)

            Launch.items[func.__name__] = item_id
            result = _run_func(func, *args, **kwargs)
            Launch.finish_item(func.__name__)
            return result

        return wrapper
    return decorator

@pytest.mark.skip(reason='')
def feature(name: str):
    def decorator(cls):
        __tracebackhide__ = True
        item_id = Launch.create_report_item(
            name=name,
            type='suite',
            description=cls.__doc__)

        Launch.items[cls.__name__] = item_id
        return cls

    return decorator

@pytest.mark.skip(reason='')
def story(name: str):
    def decorator(cls):
        parent = _get_class_parent(cls)
        print(parent)
        item_id = Launch.create_report_item(
            name=name,
            parent_item=parent,
            type='story',
            description=cls.__doc__)

        Launch.items[cls.__name__] = item_id
        return cls

    return decorator

def log(*, message: str, level: str = "INFO"):
    item = Launch.get_caller_name()
    Launch.create_log(item=item, message=message, level=level)

def attachment(*, name: str, attachment: Union[str, bytes], attachment_type: str, attach_to: Union[str, None] = None, level: Literal["ERROR", "INFO", "DEBUG"] = "ERROR"):
    """Add attachment to the item (test class/case/step)
    :param item: The item name (function name)
    :param name: The attachment name
    :param attachment: attachment as bytes or the path to the attachment
    :param attachment_type: The type of the attachment (i.e use report.attachment_type.PNG)
    :param level: The log level of the the attachment (i.e if an error occured and you want to attach a screenshot use "ERROR")
    """
    item = list(Launch.items.keys())[-1] if attach_to is None else attach_to
    Launch.add_attachment(item=item, message=name, level=level, attachment=attachment, attachment_type=attachment_type)

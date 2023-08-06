from functools import wraps

from .use_cases import Formatter
from .core import Codes


def output(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        return_value = function(*args, **kwargs)

        print(return_value)
        if kwargs.get('flush'):
            print(Codes.line_up, end=Codes.line_clear)

    return wrapper


class Logger:
    '''
    The Logger class can be used in two ways: it can be instanced with a name or used as a static class for quick outputs.
    
    The Logger class has four logging levels: info, debug, warning and error.
    '''
    info_prefix: str = Formatter.green(Formatter.bold('[INFO]'))
    debug_prefix: str = Formatter.blue(Formatter.bold('[DEBUG]'))
    warning_prefix: str = Formatter.yellow(Formatter.bold('[WARNING]'))
    error_prefix: str = Formatter.red(Formatter.bold('[ERROR]'))

    
    def __init__(self, name: str) -> None:
        '''
        Parameters
        ----------
        name: str
            the name of the instance
        '''
        self.name: str = name

    @output
    @staticmethod
    def info(*message, sep: str = '', flush: bool = False) -> str:
        '''        
        Log the given message at the info level.
        
        Parameters
        ----------
        *message: Any | *tuple[Any]
            the message to log
        
        sep: str, optional
            the separation of the given inputs. Default to ''
        
        flush: bool, optional
            when set to True, the inputs will stay in the same line. Default to False
        '''        
        if isinstance(message[0], Logger):
            return __class__.info_prefix + Formatter.green(f'    [{message[0].name}] {sep.join(map(str, message[1:]))}')
        else:
            return __class__.info_prefix + Formatter.green(f'    {sep.join(map(str, message))}')

    @output
    @staticmethod
    def debug(*message, sep: str = '', flush: bool = False) -> str:
        '''
        Log the given message at the debug level.
        
        Parameters
        ----------
        *message: Any | *tuple[Any]
            the message to log
        
        sep: str, optional
            the separation of the given inputs. Default to ''
        
        flush: bool, optional
            when set to True, the inputs will stay in the same line. Default to False
        '''        
        if isinstance(message[0], Logger):
            return __class__.debug_prefix + Formatter.blue(f'   [{message[0].name}] {sep.join(map(str, message[1:]))}')
        else:
            return __class__.debug_prefix + Formatter.blue(f'   {sep.join(map(str, message))}')


    @output
    @staticmethod
    def warning(*message, sep: str = '', flush: bool = False) -> str:
        '''
        Log the given message at the warning level.
        
        Parameters
        ----------
        *message: Any | *tuple[Any]
            the message to log
        
        sep: str, optional
            the separation of the given inputs. Default to ''
        
        flush: bool, optional
            when set to True, the inputs will stay in the same line. Default to False
        '''        
        if isinstance(message[0], Logger):
            return __class__.warning_prefix + Formatter.yellow(f' [{message[0].name}] {sep.join(map(str, message[1:]))}')
        else:
            return __class__.warning_prefix + Formatter.yellow(f' {sep.join(map(str, message))}')


    @output
    @staticmethod
    def error(*message, sep: str = '', flush: bool = False) -> str:
        '''
        Log the given message at the error level.
        
        Parameters
        ----------
        *message: Any | *tuple[Any]
            the message to log
        
        sep: str, optional
            the separation of the given inputs. Default to ''
        
        flush: bool, optional
            when set to True, the inputs will stay in the same line. Default to False
        '''
        if isinstance(message[0], Logger):
            return __class__.error_prefix + Formatter.red(f'   [{message[0].name}] {sep.join(map(str, message[1:]))}')
        else:
            return __class__.error_prefix + Formatter.red(f'   {sep.join(map(str, message))}')


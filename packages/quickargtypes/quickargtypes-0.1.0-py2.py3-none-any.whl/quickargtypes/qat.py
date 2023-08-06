from typing import Any, Callable, List, Optional, Union
from numbers import Number
from abc import ABC, abstractmethod

import os


def absolute_path(func):
    """Change a relative path into its absolute equivalent."""
    def wrapper(self, arg: str) -> str:
        return func(self, os.path.abspath(arg))

    return wrapper


def _extension_matches(file: str, extension: str) -> bool:
    """Check whether a file path has a given extension.

    Note that extension ".gz" would match even if the full extension was ".nii.gz".

    Parameters
    ----------
    file: str
        File path.
    extension: str
        Extension.

    Returns
    -------
    bool
        Whether the file has the extension.

    """
    # Return whether the file has the extension
    if file[-len(extension):].lower() == extension.lower():
        return True

    return False

def _delimit(arg: str, delimiter: str, strip: bool = True):
    lst = arg.split(delimiter)
    if strip:
        lst = [elem.strip() for elem in lst]
    
    return lst


class APTError(Exception):
    pass


class ArgparseType(ABC):
    """Abstract type."""
    def __init__(self, name: Optional[str] = None):
        self.abstract = True
        self.fn = self.__call__ # A short alias for __call__.

        self.name = None
        if name is not None:
            self.name = name


    def __call__(self, arg: Any) -> Any:
        return arg

    
    def n(self):
        if self.name is None:
            return "Argument"
        else:
            return f"{self.name} argument"
    

    def __getattribute__(self, name):
        """Handle the accessing of the fn attribute in abstract types."""
        if name == "fn" and self.abstract:
            raise APTError(
                f"argparsetypes type {self.__class__.__name__} is abstract. Only its children may be instantiated."
            )
        else:
            return object.__getattribute__(self, name)


class Number(ArgparseType):
    """Abstract type for a number."""
    def __init__(
        self,
        minimum: Optional[int] = None,
        maximum: Optional[int] = None,
        min_inclusive: bool = True,
        max_inclusive: bool = True,
        **type_kwargs,
    ):
        super().__init__(**type_kwargs)
        self.abstract = True # Note: Must call after super

        self.minimum = minimum
        self.maximum = maximum
        self.min_inclusive = min_inclusive
        self.max_inclusive = max_inclusive


    def __call__(self, num: Number) -> Number:
        if self.minimum is not None:
            if self.min_inclusive:
                if num < self.minimum:
                    raise APTError(
                        f"{self.n()} value {num} is less than the allowed {self.minimum}."
                    )
            else:
                if num <= self.minimum:
                    raise APTError(
                        f"{self.n()} value {num} is less than or equal to the allowed {self.minimum}."
                    )

        if self.maximum is not None:
            if self.max_inclusive:
                if num > self.maximum:
                    raise APTError(
                        f"{self.n()} value {num} is greater than the allowed {self.maximum}."
                    )
            else:
                if num >= self.maximum:
                    raise APTError(
                        f"{self.n()} value {num} is greater than or equal to the allowed {self.maximum}."
                    )

        return super().__call__(num)


class Int(Number):
    """Type for an integer."""
    def __init__(self, **num_kwargs):
        super().__init__(**num_kwargs)
        self.abstract = False # Note: Must call after super


    def __call__(self, arg: str) -> int:
        try:
            num = int(arg)
        except ValueError:
            raise APTError(
                f"{self.n()} value {arg} cannot be converted to an integer."
            )

        return super().__call__(num)


class Float(Number):
    """Type for a float."""
    def __init__(self, **num_kwargs):
        super().__init__(**num_kwargs)
        self.abstract = False # Note: Must call after super


    def __call__(self, arg: str) -> int:
        try:
            num = float(arg)
        except ValueError:
            raise APTError(
                f"{self.n()} value {arg} cannot be converted to a float."
            )

        return super().__call__(num)


class Path(ArgparseType):
    """Abstract type for a path."""
    def __init__(self, **type_kwargs):
        super().__init__(**type_kwargs)
        self.abstract = True # Note: Must call after super

    @absolute_path
    def __call__(self, arg: str) -> str:
        return super().__call__(arg)


class _File(Path):
    """Abstract type for a file path."""
    def __init__(self, ext: Optional[Union[str, List[str]]] = None, **path_kwargs):
        """
        
        Parameters
        ----------
        ext: str or list of str, optional
            An extension, or a list of extensions. One of which the file must have.
        """
        super().__init__(**path_kwargs)
        self.abstract = True # Note: Must call after super

        ext = [ext] if isinstance(ext, str) else ext
        self.ext = [e if e.startswith(".") else "." + e for e in ext]


    @absolute_path
    def __call__(self, arg: str) -> str:
        if self.ext is None:
            return super().__call__(arg)

        for ext in self.ext:
            if _extension_matches(arg, ext):
                return super().__call__(arg)

        raise APTError(
            f"{self.n()} value {arg} does not match extensions: {','.join(self.ext)}."
        )


class File(_File):
    """Type for an existing file path."""
    def __init__(self, **file_kwargs):
        super().__init__(**file_kwargs)
        self.abstract = False # Note: Must call after super


    @absolute_path
    def __call__(self, arg: str) -> str:
        if not os.path.isfile(arg):
            raise APTError(
                f"{self.n()} value {arg} is not an existing file path."
            )

        return super().__call__(arg)


class SaveFile(_File):
    """Type for a save file path."""
    def __init__(self, exist_ok: bool = False, make_parent: bool = False, parent_exists: bool = True, **path_kwargs):
        super().__init__(**path_kwargs)
        self.abstract = False # Note: Must call after super

        self.exist_ok = exist_ok
        self.make_parent = make_parent
        self.parent_exists = parent_exists


    @absolute_path
    def __call__(self, arg: str) -> str:
        if not self.exist_ok:
            if os.path.isfile(arg):
                raise APTError(
                    f"{self.n()} value {arg} already exists as a file."
                )

        parent = os.path.dirname(arg)

        if self.make_parent:
            os.makedirs(parent, exist_ok=True)

        elif self.parent_exists:
            if not os.path.isdir(parent):
                raise APTError(
                    f"{self.n()} value {arg} file save path parent must exist."
                )

        return super().__call__(arg)


class _Dir(Path):
    """Abstract type for a directory path."""
    def __init__(self, **path_kwargs):
        super().__init__(**path_kwargs)
        self.abstract = True # Note: Must call after super


    @absolute_path
    def __call__(self, arg: str) -> str:
        return super().__call__(arg)


class Dir(_Dir):
    """Type for an existing directory path."""
    def __init__(self, **path_kwargs):
        super().__init__(**path_kwargs)
        self.abstract = False # Note: Must call after super


    @absolute_path
    def __call__(self, arg: str) -> str:
        if not os.path.isdir(arg):
            raise APTError(
                f"{self.n()} value {arg} is not a valid directory path."
            )

        return super().__call__(arg)


class SaveDir(_Dir):
    """Type for a directory path to which to save items."""
    def __init__(self, exist_ok: bool = False, make: bool = False, parent_exists: bool = True, **path_kwargs):
        super().__init__(**path_kwargs)
        self.abstract = False # Note: Must call after super

        self.exist_ok = exist_ok
        self.make = make
        self.parent_exists = parent_exists


    @absolute_path
    def __call__(self, arg: str) -> str:
        if not self.exist_ok:
            if os.path.isdir(arg):
                raise APTError(
                    f"{self.n()} value {arg} already exists as a directory."
                )

        parent = os.path.dirname(arg)

        if self.make:
            os.makedirs(arg, exist_ok=True)

        elif self.parent_exists:
            if not os.path.isdir(parent):
                raise APTError(
                    f"{self.n()} value {arg} directory save path parent must exist."
                )

        return super().__call__(arg)


class Delimited(ArgparseType):
    """Type for delimited strings."""
    def __init__(self, delimiter: str = ",", strip: bool = True):
        super().__init__(**path_kwargs)
        self.abstract = False # Note: Must call after super

        self.delimiter = delimiter
        self.strip = strip


    def __call__(self, arg: str) -> List[str]:
        return super().__call__(_delimit(arg, self.delimiter, strip=self.strip))


class DelimitedInt(ArgparseType):
    """Type for delimited integers."""
    def __init__(self, delimiter: str = ",", as_tuple: bool = False, **type_kwargs):
        super().__init__(**type_kwargs)
        self.abstract = False # Note: Must call after super

        self.delimiter = delimiter
        self.as_tuple = as_tuple


    def __call__(self, arg: str) -> List[str]:
        lst = _delimit(arg, self.delimiter, strip=True)
        lst = [Int().fn(elem) for elem in lst]

        if self.as_tuple:
            return tuple(lst)

        return super().__call__(lst)


class DelimitedFloat(ArgparseType):
    """Type for delimited floats."""
    def __init__(self, delimiter: str = ",", as_tuple: bool = False, **type_kwargs):
        super().__init__(**type_kwargs)
        self.abstract = False # Note: Must call after super

        self.delimiter = delimiter
        self.as_tuple = as_tuple


    def __call__(self, arg: str) -> List[str]:
        lst = _delimit(arg, self.delimiter, strip=True)
        lst = [Float().fn(elem) for elem in lst]

        if self.as_tuple:
            return tuple(lst)

        return super().__call__(lst)

    
class Percent(ArgparseType):
    """Type for a decimal percentage."""
    def __init__(self, **type_kwargs):
        super().__init__(**type_kwargs)
        self.abstract = False # Note: Must call after super

    def __call__(self, arg: str) -> float:
        num = Float().fn(arg)
        
        if num < 0:
            raise APTError(
                f"{self.n()} value {arg} is invalid (negative percentage)."
            )

        if num > 1:
            raise APTError(
                f"{self.n()} value {arg} is invalid (percentage > 1)."
            )

        return super().__call__(num)


class Boolean(ArgparseType):
    """Type for a non-flagged boolean.

    Especially useful when wanting a default "True" value without using store_true.
    """
    def __init__(
        self,
        true_vals: Optional[List[str]] = None,
        false_vals: Optional[List[str]] = None,
        case_sensitive: bool = False,
        **type_kwargs,
    ):
        super().__init__(**type_kwargs)
        self.abstract = False # Note: Must call after super
        
        self.true_vals = true_vals
        if true_vals is None:
            self.true_vals = ["yes", "true", "t", "y", "1"]
            
        self.false_vals = false_vals
        if false_vals is None:
            self.false_vals = ["no", "false", "f", "n", "0"]

        self.case_sensitive = case_sensitive


    def __call__(self, arg: str) -> bool:
        if arg.lower() in self.true_vals:
            return super().__call__(True)

        if arg.lower() in self.false_vals:
            return super().__call__(False)

        raise APTError(
            f"{self.n()} value {arg} is not a recognized boolean value."
        )

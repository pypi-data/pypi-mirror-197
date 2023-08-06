# quickargtypes

`quickargtypes` is a wrapper built atop [argparse](https://docs.python.org/3/library/argparse.html) to make it simple to use and create flexible argument parsing types which interface with native `argparse` parsers.


To install:
```
pip install quickargtypes
```

Here is an example illustrating its functionality:
```
import argparse
from quickargtypes import qat

parser = argparse.ArgumentParser()

parser.add_argument(
    "-i",
    "--integer",
    type=qat.Int(name="integer", minimum=4).fn,
    required=True,
)
parser.add_argument(
    "-f",
    "--file",
    type=qat.File(name="file", ext=".py").fn,
    required=True,
)
parser.add_argument(
    "-s",
    "--save",
    type=qat.SaveFile(name="save", ext=".py", exist_ok=True).fn,
    required=True,
)
parser.add_argument(
    "-d",
    "--dir",
    type=qat.SaveDir(name="dir", exist_ok=True).fn,
    required=True,
)
parser.add_argument(
    "--delimited",
    type=qat.DelimitedInt(name="delimited", as_tuple=True).fn,
    required=True,
)
parser.add_argument(
    "-b",
    type=qat.Boolean(name="b").fn,
    required=False,
)
```
"""
MIT License

Copyright (c) 2020-2024 EntySec

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from typing import Optional

from pawn.lib.option import *
from pawn.lib.options import Options

from pex.platform.types import *
from pex.arch.types import *


class Module(object):
    """ Subclass of pawn.lib module.

    This subclass of pawn.lib module is intended for providing
    wrapper for a module.
    """

    def __init__(self) -> None:
        super().__init__()

        self.details = {
            'Name': "",
            'Authors': [
                ''
            ],
            'Arch': None,
            'Platform': None,
        }

    def set(self, option: str, value: Optional[str] = None) -> bool:
        """ Set module option.

        :param str option: option name
        :param Optional[str] value: option value
        :return bool: True if success else False
        """

        return Options().set_option(self, option, value)

    def run(self) -> None:
        """ Run this module.

        :return None: None
        """

        pass

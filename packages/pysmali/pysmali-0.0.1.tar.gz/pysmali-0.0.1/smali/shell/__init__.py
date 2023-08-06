# This file is part of rgoogle's Smali API
# Copyright (C) 2023 MatrixEditor

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.
__doc__ = """
"""

import cmd

from smali.bridge.vm import SmaliVM, _SourceFieldVisitor

class SmaliShell(cmd.Cmd):
    
    def precmd(self, line: str) -> str:
        print("Call:", line)
        return "continue"

    def do_continue(self, arg):
        pass
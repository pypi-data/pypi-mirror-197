# along with this program.  If not, see <https://www.gnu.org/licenses/>.
import struct

from smali import SmaliValue
from smali.opcode import *
from smali.bridge.frame import Frame
from smali.bridge.errors import ExecutionError
from smali.bridge.lang import SmaliObject
from smali.bridge.objects import Object, Class

__all__ = [
    'Executor', 'OpcodeExecutor', 'executor', 'nop', 'return_void', 
    'return_object', 'goto', 'invoke', 'int_to_long', 'int_to_int', 
    'int_to_char', 'int_to_byte', 'int_to_float', 'sput_object', 
    'sget_object', 'rem_int__lit8', 'rem_int', 'const', 'const_class', 
    'move_result', 'move', 'move_exception', 'new_instance'
]

__executors__ = {}
"""Sepcial dict tat stores all opcodes with their executors"""

class Executor:

    opcode: str
    """The linked opcode"""

    action = None
    """Optional action if this class is not subclassed."""

    frame: Frame = None
    """The current execution frame"""

    args: tuple = None
    """THe current execution arguments"""

    kwargs: dict = None
    """The current execution"""

    def __init__(self, action, name=None,
                 map_to: list = None) -> None:
        self.opcode = name
        self.action = action
        self.frame = None
        if self.action:
            self.opcode = (str(action.__name__)
                .replace('__', '/')
                .replace('_', '-'))

        if not self.opcode:
            raise ValueError('Opcode name must be non-null!')
        __executors__[self.opcode] = self
        if map_to:
            for op_name in map_to:
                __executors__[op_name] = self

    def __call__(self, frame: Frame):
        self.frame = frame
        self.args = self.args or ()
        if self.action:
            self.action(self, *self.args)

    def __repr__(self) -> str:
        return f"<{self.opcode} at {id(self):#x}>"

    def __str__(self) -> str:
        return self.__repr__()


def OpcodeExecutor(map_to=[]):
    def wrapper(func):
        return Executor(func, map_to=map_to)
    return wrapper

def executor(name: str) -> Executor:
    if name not in __executors__:
        raise KeyError(f'Could not find executor for opcode: {name}')

    return __executors__[name]

@OpcodeExecutor()
def nop(self):
    pass

################################################################################
# RETURN
################################################################################
@OpcodeExecutor(map_to=[RETURN_VOID_BARRIER, RETURN_VOID_NO_BARRIER])
def return_void(self: Executor):
    self.frame.return_value = None
    self.frame.finished = True

@OpcodeExecutor(map_to=[RETURN, RETURN_WIDE])
def return_object(self: Executor, register: str):
    self.frame.return_value = self.frame[register]
    self.frame.finished = True

################################################################################
# GOTO
################################################################################
@OpcodeExecutor(map_to=[GOTO_16, GOTO_32])
def goto(self: Executor, label: str):
    if label not in self.frame.labels:
        raise ExecutionError("NoSuchLabelError", label)

    self.frame.label = label
    self.frame.pos = self.frame.labels[label]

################################################################################
# INVOKE
################################################################################
@OpcodeExecutor()
def invoke(self: Executor, inv_type, args, owner, method):
    # TODO: add direct calls to int or str objects
    if inv_type in ('direct', 'virtual', 'static'):
        vm_class = None
        if owner == 'Ljava/lang/Class;':
            # If class methods should be invoked, just use the
            # previously moved class object
            vm_class = self.frame[args[0]]
            self.frame.method_return = Class[method](vm_class)
            return

        if owner == 'Ljava/lang/Object;':
            target = Object[method]
            self.frame.method_return = target(self.frame[args[0]])
            return

        if inv_type != 'static':
            instance = values[0]
            super_cls = instance.smali_class.super_cls
            if super_cls == owner:
                vm_class = self.frame.vm.get_class(super_cls)

        values = [self.frame[register] for register in args]

        if not vm_class:
            vm_class = self.frame.vm.get_class(owner)

        instance = None if inv_type == 'static' else values[0]
        if instance:
            values = values[1:]

        target = vm_class.method(method)
        self.frame.method_return = self.frame.vm.call(target, instance, *values)


################################################################################
# INT-2-OBJECT, LONG-2-OBJECT
################################################################################
@OpcodeExecutor()
def int_to_long(self: Executor, dest: str, src: str):
    self.frame[dest] = self.frame[src] & 0xFFFFFFFFFFFFFFFF

@OpcodeExecutor(map_to=[LONG_TO_INT])
def int_to_int(self: Executor, dest: str, src: str):
    self.frame[dest] = self.frame[src] & 0xFFFFFFFF

@OpcodeExecutor(map_to=[INT_TO_SHORT])
def int_to_char(self: Executor, dest: str, src: str):
    self.frame[dest] = self.frame[src] & 0xFFFF

@OpcodeExecutor()
def int_to_byte(self: Executor, dest: str, src: str):
    self.frame[dest],  = struct.unpack('>i', self.frame[src])

@OpcodeExecutor(map_to=[INT_TO_DOUBLE])
def int_to_float(self: Executor, dest: str, src: str):
    self.frame[dest] = float(self[src])

################################################################################
# SGET, SPUT
################################################################################
@OpcodeExecutor(map_to=[
    SPUT, SPUT_BOOLEAN, SPUT_SHORT, SPUT_CHAR, SPUT_BYTE,
    SPUT_OBJECT_VOLATILE, SPUT_WIDE,SPUT_WIDE_VOLATILE
])
def sput_object(self: Executor, register: str, dest: str):
    # The destination string contains the owner class name, field name and
    # field type.
    value = self.frame[register]

    owner, name_type = dest.split('->')
    name, _ = name_type.split(':')

    cls = self.frame.vm.get_class(owner)
    field = cls.field(name)
    field.value = value


@OpcodeExecutor(map_to=[
    SGET, SGET_BOOLEAN, SGET_BYTE, SGET_OBJECT_VOLATILE, SGET_VOLATILE,
    SGET_WIDE, SGET_WIDE_VOLATILE, SGET_CHAR
])
def sget_object(self: Executor, register: str, dest: str):
    # The destination string contains the owner class name, field name and
    # field type.
    owner, name_type = dest.split('->')
    name, _ = name_type.split(':')

    cls = self.frame.vm.get_class(owner)
    field = cls.field(name)
    self.frame[register] = field.value

################################################################################
# REMINT/LIT
################################################################################
@OpcodeExecutor(map_to=[REM_INT_LIT16])
def rem_int__lit8(self: Executor, dest: str, src: str, lit: str):
    value = SmaliValue(lit)
    self.frame[dest] = self.frame[src] % value

@OpcodeExecutor(map_to=[REM_DOUBLE, REM_FLOAT, REM_LONG])
def rem_int(self: Executor, dest: str, src: str, val: str):
    self.frame[dest] = self.frame[src] % self.frame[val]


################################################################################
# CONST
################################################################################
@OpcodeExecutor(map_to=[
    CONST_STRING, CONST_STRING_JUMBO, CONST_16, CONST_4,
    CONST_WIDE, CONST_WIDE_HIGH16, CONST_WIDE_32
])
def const(self: Executor, register: str, value: str):
    self.frame[register] = SmaliValue(value)

@OpcodeExecutor(map_to=[CONST_CLASS])
def const_class(self: Executor, register: str, name: str):
    self.frame[register] = self.frame.vm.get_class(name)

################################################################################
# MOVE
################################################################################
@OpcodeExecutor(map_to=[MOVE_RESULT_OBJECT])
def move_result(self: Executor, register: str):
    self.frame[register] = self.frame.method_return

@OpcodeExecutor()
def move(self: Executor, dest: str, src: str):
    self.frame[dest] = self.frame[src]

@OpcodeExecutor()
def move_exception(self: Executor, dest: str):
    self.frame[dest] = self.frame.error

################################################################################
# NEW-INSTANCE
################################################################################
@OpcodeExecutor()
def new_instance(self: Executor, register: str, descriptor: str):
    smali_class = self.frame.vm.get_class(descriptor)
    instance = SmaliObject(smali_class)
    instance.init()

    self.frame[register] = instance
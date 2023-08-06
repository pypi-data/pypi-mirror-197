# PySmali

![LastEdit](https://img.shields.io:/static/v1?label=LastEdit&message=03/15/2023&color=9cf)
![Status](https://img.shields.io:/static/v1?label=Status&message=DRAFT&color=yellow)
![Platform](https://img.shields.io:/static/v1?label=Platforms&message=Linux|Windows&color=yellowgreen)
[![Documentation Status](https://readthedocs.org/projects/pysmali/badge/?version=latest)](https://pysmali.readthedocs.io/en/latest/?badge=latest)
![PyPi](https://img.shields.io:/static/v1?label=PyPi&message=0.0.1&color=green)


The main functionalities of this repository cover creating and parsing Smali files with Python3 as well as interpret Smali source code files.


## Installation

By now, the only way to install the python module in this repository is by cloning it and running the following command:

```bash
$ cd ./pysmali && pip install .
```

## Usage

For a more detailed explanation of the Smali Visitor-API use the [docs](https://pysmali.readthedocs.io/).

### Parsing Smali-Files

The simplest way to parse code is to use a `SmaliReader` together with a visitor:

```python
from smali import SmaliReader, ClassVisitor

code = """
.class public final Lcom/example/Hello;
.super Ljava/lang/Object;
# One line comment
.source "SourceFile" # EOL comment
"""

reader = SmaliReader()
reader.visit(code, ClassVisitor())
```

There are a few options to have in mind when parsing with a `SmaliReader`:

* `comments`: To explicitly parse comments, set this variable to True (in constructor or directly)
* `snippet`: To parse simple code snippets without a .class definition, use the 'snippet' variable (or within the constructor). Use this property only if you don't have a '.class' definition at the start of the source code
* `validate`: Validates the parsed code
* `errors`: With values `"strict"` or `"ignore"` this attribute will cause the reader to raise or ignore exceptions

Actually, the code above does nothing as the `ClassVisitor` class does not handle any notification by the reader. For instance, to print out the class name of a parsed code, the following implementation could be used:

```python
from smali import SmaliReader, ClassVisitor, Type

class NamePrinterVisitor(ClassVisitor):
    def visit_class(self, name: str, access_flags: int) -> None:
        # The provided name is the type descriptor, so we have to 
        # convert it:
        cls_type = Type(name)
        print('ClassName:', cls_type.class_name)

reader = SmaliReader()
reader.visit(".class public final Lcom/example/Hello;", NamePrinterVisitor())
```

### Writing Smali-Files

Writing is as simple as parsing files. To write the exact same document the has been parsed, the `SmaliWriter` class can be used as the visitor:

```python
from smali import SmaliReader, SmaliWriter

reader = SmaliReader()
writer = SmaliWriter()

reader.visit(".class public final Lcom/example/Hello;", writer)
# The source code can be retrieved via a property
text = writer.code
```

To create own Smali files, the pre-defined `SmaliWriter` can be used again:

```python
from smali import SmaliWriter, AccessType

writer = SmaliWriter()
# create the class definition
writer.visit_class("Lcom/example/Hello;", AccessType.PUBLIC + AccessType.FINAL)
writer.visit_super("Ljava/lang/Object;")

# create a field
field_writer = writer.visit_field("foo", AccessType.PRIVATE, "Ljava/lang/String")

# create the finished source code, BUT don't forget visit_end()
writer.visit_end()
text = writer.code
```

### Importing classes and execute methods

As of version `0.0.1` you can import Smali files and execute defined methods:

```python
from smali.bridge import SmaliVM, SmaliObject

with open('example.smali', 'r', encoding='utf-8') as fp:
    source = fp.read()
    
vm = SmaliVM()
# Import class definition
smali_class = vm.classloader.load_class(source, init=False)
# Call <clinit> method
smali_class.clinit()

# Create a new instance of the imported class
instance = SmaliObject(smali_class)
# Call the object's constructor
instance.init()

# Execute the method 'toString'
toString = instance.smali_class.method("toString")
# The instance must be always the first element (on 
# static methods this argument must be None)
value = toString(instance)
print(value)
```

## License

Distributed under the GNU GPLv3. See `LICENSE` for more information.

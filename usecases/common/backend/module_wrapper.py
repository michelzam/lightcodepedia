# (c) 2020 mz

import ast
import keyword
import sys
import types
import typing
from dataclasses import field, dataclass
from typing import Type, Any, get_origin, List, Dict, Optional
import inspect
from typing import List, Optional


NL = '\n'

# forward declaration
class Class:
    ...

class Wrapper:
    pass


@dataclass
class Wrapper:
    name: str = "(anonymous)"
    value: Any = field(default=None)  # the py object!
    doc: str = field(default="")
    icon: str = field(default="")
    hidden: bool = field(default=False)
    following: float = field(default=0.0)
    tag: str = field(default="", metadata={"doc": "Decorate with errors, checks, ..."})
    _tags: List[str] = field(default_factory=list, metadata={"doc": "Decorate with transient errors, checks, ..."})
    _class: Class = field(default=None)
    # _yaml_str: str = ""


    def __post_init__(self):
        # Example usage
        #self._class = self._generate_class_from_wrapper(type(self))
        pass

    def __str__(self):
        return f"{self.icon} {self.name}"

    def get_tags(self) -> List[str]:
        """Get the tags of the wrapper, including class and methods"""
        tags = self._tags.copy()
        return tags

    def _generate_class_from_wrapper(self, wrapper_cls: Type[Wrapper]) -> Class:
        """Generate a Class instance from a given Wrapper class."""

        attributes = []
        methods = []
        bases = []

        # Handle inheritance
        if hasattr(wrapper_cls, '__bases__'):
            bases = [base.__name__ for base in wrapper_cls.__bases__ if base is not Wrapper]

        # Inspect the wrapper class to find attributes and methods
        for name, member in inspect.getmembers(wrapper_cls):
            if isinstance(member, property):
                # Properties in Python are usually getters/setters -> can be treated as attributes
                attr_type = "Unknown"
                if member.fget is not None:
                    attr_type = type(inspect.signature(member.fget).return_annotation).__name__
                attributes.append(Attribute(name=name, type=attr_type))

            elif isinstance(member, (int, str, list, dict, float, bool)):
                # Static attributes
                attr_type = type(member).__name__
                attributes.append(Attribute(name=name, type=attr_type, default=member))

            elif inspect.isfunction(member):
                # Methods
                code = inspect.getsource(member).strip()
                methods.append(Method(name=name, code=code))

        # Create a Class instance with identified attributes and methods
        class_instance = Class(
            name=wrapper_cls.__name__,
            bases=bases,
            attributes=attributes,
            methods=methods,
            doc=wrapper_cls.__doc__ or "",
            icon=getattr(wrapper_cls, 'icon', "📦")  # Default icon if not set
        )

        return class_instance


    def __repr__(self) -> str:
        return f"{self.icon} {self.name}"

    def _run(self, *args, **kwargs) -> bool:
        return True  # dummy to cope with designers ...

    @property
    def label(self) -> str:
        return f"{self.icon} {self.name}"

    @property
    def title(self) -> str:
        return f"{self.icon} {self.name.capitalize().replace('_', ' ')}"

    def _check(self) -> int:
        """
        Check the wrapper for errors.
        Note: this could be extracted and managed by visitors ...
        :return: the number of errors
        """
        self._tags = []
        ret = 1 if keyword.iskeyword(self.name) else 0
        if ret > 0:
            self._tags.append(f"Error: {self.name} is a keyword")
        if " " in self.name:
            self._tags.append(f"Error: {self.name} contains spaces")
            ret += 1
        return ret

@dataclass
class Attribute(Wrapper):
    type: str = field(default="")
    default: Any = field(default=None)
    read_only: bool = field(default=False)
    is_long: bool = field(default=False)
    language: str = field(default="")
    owned: bool = field(default=False, metadata={"doc": "Class exclusive owns of the value"})
    advanced: bool = field(default=False, metadata={"doc": "Advanced attribute"})
    options: List[str] = field(default_factory=list)
    option_field: str = field(default="")
    captions: List[str] = field(default_factory=list)

    def __post_init__(self):
        icon_map = {
            "str": "🔤" if not self.is_long else "🔠",
            "int": "🔢",
            "float": "🔢",
            "bool": "🔘",
            "date": "📅",  # more: 📆 or 🗓
            "datetime": "🕗",
            list: "⦙",
        }
        if self.icon == "":
            icon = icon_map.get(self.type, "📦")
            self.icon = icon
        if self.default is None:
            if self.type in ["int", "float"]:
                self.default = 0

    def __repr__(self):
        return f"{super().__repr__()}: ({self.type})"

    def get_label(self):
        #_get_label(attr.name, attr.type, capitalize=True)
        name = self.name.capitalize()
        return f"{self.icon} {name}"


@dataclass
class Method(Wrapper):
    code: str = field(default="...")
    icon: str = field(default="⚙️")
    preconditions: List[str] = field(default_factory=list)
    postcondition: str = field(default="")
    # guard: str = field(default="True")
    # value will remain empty for now

    def _check(self) -> int:
        result = super()._check()
        try:
            ast.parse(self.code, type_comments=True)
        except SyntaxError as e:
            error_message = e.msg
            lineno = e.lineno
            offset = e.offset
            line = e.text
            error_message = f"SyntaxError: {error_message} at line {lineno}, offset {offset}\n{line}\n{' ' * (offset - 1)}^"
            self._tags.append(error_message)
            return result + 1

        return result

# Forward declaration
class Module:
    ...


@dataclass
class Class(Wrapper):
    bases: List[str] = field(default_factory=list)
    attributes: List[Attribute] = field(default_factory=list)
    methods: List[Method] = field(default_factory=list)
    state: str = field(default="")
    states: List[str] = field(default_factory=list)
    # value will remain empty for now
    icon: str = field(default="🗄️")
    _module: Module = field(default=None)

    def _check(self) -> int:
        result = super()._check()
        for a in self.attributes:
            result += a._check()

        for m in self.methods:
            result += m._check()

        if result > 0:
            self._tags.append(f"⚠️{result if result > 1 else ''}")
        return result

    def get_tags(self) -> List[str]:
        """Get the tags of the class, including attributes and methods"""
        tags = [f"Class: {self.name}"]
        tags += super().get_tags()
        for a in self.attributes:
            tags += a.get_tags()
        for m in self.methods:
            tags += m.get_tags()
        return tags

    def find_attribute(self, name: str) -> Optional[Attribute]:
        for a in self.attributes:
            if a.name == name:
                return a
        for b in self.bases:
            return b.find_attribute(name)
        return None

    def find_method(self, name: str) -> Optional[Method]:
        for m in self.methods:
            if m.name == name:
                return m
        for b in self.bases:
            return b.find_method(name)
        return None

    def get_attributes(self) -> List[Attribute]:
        attributes = []
        for base in self.bases:
            attributes += base.get_attributes()
        for attr in self.attributes:
            if attr.name not in [a.name for a in attributes]:
                attributes.append(attr)
            else:
                index = [a.name for a in attributes].index(attr.name)
                attributes[index] = attr
        return attributes


    def check_state(self, sender, method_name: str) -> bool:
        if not hasattr(sender, "state"):
            return True  # no need to check anymore

        method = self.find_method(method_name)
        assert method is not None, f"Method {method_name} not found in {self.name}"

        if method.preconditions:
            return sender.state in method.preconditions

        return True

    def change_state(self, sender, method_name: str) -> bool:
        if not hasattr(sender, "state"):
            return True  # no need to check anymore

        method = self.find_method(method_name)
        assert method is not None

        if len(method.postcondition) > 0:
            sender.state = method.postcondition

        return True


@dataclass
class Module(Wrapper):
    """A wrapper for a [dynamic or not] py module.
    OBSOLETE: If value is not None, it is a py module and will not have class wrappers.
    Therefore, those classes would only be available from method code
    """
    as_name: str = field(default="")
    imports: Dict[str, Module] = field(default_factory=dict)
    classes: Dict[str, Class] = field(default_factory=dict)
    # instances: Dict[str, Any] = field(default_factory=dict) # native py instances!
    instances: List[Any] = field(default_factory=list) # native py instances!
    icon: str = field(default="🧩")
    _imported: List[Module] = field(default_factory=list) # temp cache for diagram
    is_admin: bool = field(default=False)
    designing: bool = field(default=False)
    revision: int = field(default=0)  # -1: new, 0: saved, >0: modified
    _loader: typing.Any = field(default=None, metadata={"doc": "The loader that created this module"})

    # traces: List[Trace] = field(default_factory=list) # temp cache for diagram

    def __post_init__(self):
        if self.as_name == "":
            self.as_name = self.name
        ## NOT A GOOD IDEA: self._class = Module

    def get_tags(self) -> List[str]:
        """Get the tags of the module, including classes and methods"""
        tags = [f"Module: {self.name}"]
        tags += super().get_tags()
        for c in self.classes.values():
            tags += c.get_tags()
        return tags

    def _check(self) -> int:
        result = super()._check()
        error_count = 0 if result == 0 else 1
        # super()._check()
        for class_name, c in self.classes.items():
            ret = c._check()
            if ret > 0:
                error_count += ret
            result += ret

        if error_count > 0:
            self._tags.append(f"⚠️{error_count if error_count > 1 else ''}")
        else:
            self._tags.append("✅")
        return result

    def find_class(self, name: str) -> Class:
        """Find a class in the module"""
        if "." in name:  # using module_alias.class_name ?
            module_name, class_name = name.split(".")
            for m in self.imports.values():
                if m.as_name == module_name:
                    return m.find_class(class_name)

        for c in self.classes.values():
            if c.name == name:
                return c
        for m in self.imports.values():
            ret = m.find_class(name)
            if ret is not None:
                return ret
        return None

    def _OLD_get_classes(self) -> List[Class]:
        """Get all classes in the module and imports"""
        classes = []
        for c in self.classes.values():
            classes.append(c)
        for m in self.imports.values():
            clz = m.get_classes()
            classes += [c for c in clz if c not in classes]
        return classes

    def get_classes(self, visited=None) -> List[Class]:
        """Get all classes in the module and imports, recursively avoiding cycles."""
        if visited is None:
            visited = set()

        if id(self) in visited:
            return []
        visited.add(id(self))

        classes = list(self.classes.values())

        for m in self.imports.values():
            clz = m.get_classes(visited)
            classes.extend(c for c in clz if c not in classes)

        return classes

    def _make(self, _loader=None):
        """Make the py module from wrapper"""
        self.value = types.ModuleType(self.name)
        self.value.__doc__ = self.doc
        self.value._module = self  # hack
        sys.modules[self.name] = self.value
        globals()[self.as_name] = self.value
        self._loader = _loader
        pass  # Breakpoint here?

    def _unmake(self):
        """Remove the py module from sys.modules"""
        if self.name in sys.modules:
            del sys.modules[self.name]
        if self.as_name in globals():
            del globals()[self.as_name]
        self.value = None
        self.imports.clear() #: Dict[str, Module] = field(default_factory=dict)
        self._imported.clear()
        self.classes.clear()  # : Dict[str, Class] = field(default_factory=dict)
        self.instances.clear() # : Dict[str, Any] = field(default_factory=dict) # native py instances!
        self.icon =  ""  # : str = field(default="🧩")

    def _find_module(self, name: str) -> Module:
        if name == self.name:
            return self
        for mod in self.imports.values():
            if mod.name == name:
                return mod
            else:
                return mod._find_module(name)
        return None

    def _run(self, *args, **kwargs) -> bool:
        """Run the module"""
        for i in self.instances:
            if hasattr(i, "_run"):
                if not i._run(module=self, args=args, kwargs=kwargs):
                    break
        return True

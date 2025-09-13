# (c) 2020 mz / module_manager.py

import ast
import importlib
import linecache
import sys
import traceback
import types
from dataclasses import Field, field, dataclass
from dataclasses import fields, MISSING, make_dataclass
from typing import Any, get_origin, List, Dict, Set
from beartype import beartype
from beartype.door import is_bearable

import pandas as pd
import yaml
import re
# from pydantic import BaseModel


# class MyBaseModel(BaseModel):
#     class Config:
#         arbitrary_types_allowed = True
#

from functools import wraps
import logging

def trace_methods(cls):
    """ Decorator to trace execution of all methods in a dataclass """
    for attr in dir(cls):
        if callable(getattr(cls, attr)) and not attr.startswith("__"):
            method = getattr(cls, attr)
            @wraps(method)
            def wrapper(*args, **kwargs):
                logging.info(f"🔍 Calling `{method.__name__}` with args={args[1:]}, kwargs={kwargs}")
                result = method(*args, **kwargs)
                logging.info(f"✅ `{method.__name__}` returned: {result}")
                return result
            setattr(cls, attr, wrapper)
    return cls

from usecases.common.backend.file_access import RepoManager
# from tracing import trace_execution_time


from usecases.common.backend.module_wrapper import Module, Class, Method, Attribute, NL


def _extract_bare_type(type_str: str) -> str:

    # Your input string. Example: "List[ people.Person ]"
    input_string = type_str

    # Regular expression to match the pattern and extract the desired portion
    pattern = r"(\w+)\s*\[\s*\w+\.(\w+)\s*\]"

    # Substitute to remove the module part (e.g., 'people.')
    output_string = re.sub(pattern, r'\1[ \2 ]', input_string)

    # delete all spaces
    output_string = output_string.replace(" ", "")

    # print(output_string)  # Output: "List[ Person ]"
    return output_string


def get_dataclass_field_str(type_str: str, default_value: Any = None, repr: bool = False) -> Field:
    """Generate a dataclass field based on the type and optional default value.

    Args:
        type_str (str): The str repr of the dataclass field.
        default_value (Any, optional): The default value for the field. Defaults to None.

    Returns:
        Field: A dataclass field configured based on the given type and default value.
    """

    try:
        origin = get_origin(eval(type_str, globals()))
    except:
        if "." in type_str:
            base_name = type_str
            if type_str.startswith("List["):
                base_name = _extract_bare_type(type_str)
            else:
                alias, base_name = type_str.split(".")
            origin = get_origin(eval(base_name, globals()))

    if origin is list or origin is List:
        if default_value is None:
            return field(default_factory=list, repr=repr)
        else:
            return field(default_factory=lambda: default_value.copy(), repr=repr)

    if origin is dict or origin is Dict:
        return field(default_factory=dict, repr=repr)

    if origin is set or origin is Set:
        return field(default_factory=set, repr=repr)

    # Tuples are generally immutable, so a default_factory is less common
    if origin is tuple:
        return field(default_factory=tuple, repr=repr)

    if origin is None:
        if type_str =="str" and default_value is None:
            default_value = ""
        return field(default=default_value, repr=repr)

    # Fallback if no conditions are met
    return None


# Forward declaration
class ModuleLoader:
    ...


@dataclass
class ModuleLoader:
    module_name: str = ""
    yaml_str: str = ""
    module: Module = None
    _debug: bool = False
    _target: Any = None
    _nesting_level: int = 0
    _master: ModuleLoader = None
    _repo: RepoManager = None
    _clone: ModuleLoader = None

    def __post_init__(self):
        yaml.add_constructor('!Attribute', self.yaml_constructor(Attribute), Loader=yaml.SafeLoader)
        yaml.add_constructor('!Class', self.yaml_constructor(Class), Loader=yaml.SafeLoader)
        yaml.add_constructor('!Method', self.yaml_constructor(Method), Loader=yaml.SafeLoader)
        yaml.add_constructor('!Module', self.yaml_constructor(Module), Loader=yaml.SafeLoader)
        yaml.add_representer(Attribute, self.dataclass_representer)
        yaml.add_representer(Class, self.dataclass_representer)
        yaml.add_representer(Method, self.dataclass_representer)
        yaml.add_representer(Module, self.dataclass_representer)
        yaml.add_representer(str, self.represent_str)
        yaml.add_representer(pd.DataFrame, self.dataframe_representer)

        if self.module is None:
            self.module = Module(name=self.module_name)
        if self._master is None:
            self._master = self

        assert self.module is not None
        assert self._repo is not None

    def extract_section(self, section_name: str) -> Any:
        lines = self.yaml_str.split(NL)
        in_section = False
        section_lines = []

        for line in lines:
            rline = line.rstrip()
            if line.startswith(f"{section_name}:"):
                in_section = True
                section_lines.append(rline)  # Add the section name line
                continue
            elif in_section:
                if line.startswith(' ') or line == '':  # Inside the section if line starts with space
                    section_lines.append(rline)
                else:  # End of the section if line starts without space
                    in_section = False
                    break


        return yaml.safe_load(NL.join(section_lines))

    def yaml_constructor(self, cls):
        def constructor(loader, node):
            fields = loader.construct_mapping(node, deep=True)
            new_instance = cls(**fields)
            # new_instance._yaml_str = node.start_mark.buffer[node.start_mark.index:node.end_mark.index]  # yaml.dump(node)
            return new_instance

        return constructor

    def represent_str(self, dumper, data):
        if '\n' in data:
            return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
        # else:
        # Single-line string, use quotes
        #    return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='"')
        return dumper.represent_scalar('tag:yaml.org,2002:str', data)

    def dataclass_representer(self, dumper, obj):
        # data = {field.name: getattr(obj, field.name) for field in fields(obj)}
        # for field in fields(obj):
        #   print(f"{field.name}= {getattr(obj, field.name)} vs. {field.default = }]")

        serialized_data = {
            field.name: getattr(obj, field.name)
            for field in fields(obj)
            if (not field.name.startswith("_"))  # Exclude '_fields' field
               and getattr(obj, field.name) != field.default
               and (not isinstance(getattr(obj, field.name), list)
                    or not getattr(obj, field.name) == [])
        }
        tag = f'!{obj.__class__.__name__}'
        # print(f"represent dataclass: {tag} {serialized_data}")
        return dumper.represent_mapping(tag, serialized_data)
        # return dumper.represent_mapping('tag:yaml.org,2002:map', asdict(obj))

    def dataframe_representer(self, dumper, data):
        # Ensure that data is a DataFrame
        if isinstance(data, pd.DataFrame):
            serialized_data = data.to_dict(orient='records')
            if self._debug:
                print("serialized_data:")
                print(serialized_data)
            return dumper.represent_data(serialized_data)
        else:
            raise NotImplementedError
            # Handle other data types or raise an error

    @property
    def _prefix(self) -> str:
        return self._nesting_level * "#"

    def _is_multiple(self, value: Any) -> bool:
        return get_origin(value) is not None and get_origin(value) is list

    def load_header(self):
        try:
            import_data = self.extract_section('module')['module']
        except:
            import_data = []
        if len(import_data) > 0:
            keys = import_data[0].keys()
            if self._debug:
                print(f"{keys = }")
                print(f"{import_data = }")
            for key in keys:
                if hasattr(self.module, key):
                    setattr(self.module, key, import_data[0][key])

        try:
            self.module._make(_loader=self)
        except Exception as e:
            print(self.module)
            print(e)
            raise e

    def import_modules(self, main_module: Module = None):

        if main_module is None:
            main_module = self.module
            main_module._imported = []
            if self._debug:
                print(f"Starting with {main_module.name}")

        import_data = []
        try:
            import_data = self.extract_section('imports')['imports']
            if import_data is None:
                import_data = []
        except:
            import_data = []

        for mod in import_data:
            if self._debug:
                print(f"IM/for {mod.name}: {[m.name for m in main_module._imported]}")
                print(f"{mod.name = } {type(mod).__name__ = }")

            xmod = None
            for m in main_module._imported:
                if m.name == mod.name:
                    xmod = m
                    break

            if xmod:
                # just add reference without importing again
                main_module.imports[mod.as_name] = xmod
                self.module.imports[mod.as_name] = xmod
            else:
                path_to_file, paths_exists = self._check_py_file(mod)
                if paths_exists:
                    self._build_py_module(mod, path_to_file)

                    if self._debug:
                        print(f"Importing py {path_to_file}")
                    try:
                        print(f"Trying to import {mod.name} from {path_to_file}")
                        pymodule = importlib.import_module(f"modules.{mod.name}")
                    except Exception as e:
                        print(e)
                        print(f"Exception during import {mod.name} from {path_to_file}")
                        print(traceback.format_exc())
                        raise e
                    if self._debug:
                        print(f"{pymodule.__name__ = }")
                    module = Module(name=mod.name, value=pymodule, as_name=mod.as_name, hidden=mod.hidden)
                    module.value = pymodule
                    self.module.imports[mod.as_name] = module
                else:
                    try:
                        yaml_exists, yaml_file = self._check_yaml_file(mod.name)
                    except Exception as e:
                        yaml_exists = False
                        print(f"Exxxxxception during check_yaml_file {path_to_file}")

                    if yaml_exists:
                        if self._debug:
                            print(f"Importing {path_to_file}")
                        yaml_str = self._read_yaml_file(yaml_file)
                        if self._debug:
                            print(f"IM/mod2 {mod.name}: {[m.name for m in main_module._imported]}")

                        module_loader = self._get_new_loader(mod, yaml_str)


                        module_loader.module._make()  # redondant with the next statement
                        module_loader.module.hidden = mod.hidden
                        module_loader.load_header()

                        module_loader.import_modules(main_module=main_module)
                        module_loader.create_classes()
                        ...  # and maybe more ???

                        self.module.imports[mod.as_name] = module_loader.module

                        # new stuff to declare imported names in the current module
                        setattr(self.module.value, mod.as_name, module_loader.module.value)

                        main_module._imported.append(module_loader.module)
                    else:
                        try:
                            import_str = f"import {mod.name} as {mod.as_name}"
                            exec(import_str, globals())
                            mo = globals()[mod.as_name]

                            old_module = Module(name=mod.name, value=mo, as_name=mod.as_name)
                            old_module.value = mo
                            self.module.imports[mod.as_name] = old_module

                        except Exception as e:
                            print(e)
                            print(f"Exception during import {mod.name} as {mod.as_name}")
                            print(traceback.format_exc())
                            raise e

    def _get_new_loader(self, mod, yaml_str):
        if self._debug:
            print(f"{self.module.name = } gets new loader for {mod.name = } ")
            # print(self)
        module_loader = ModuleLoader(module_name=mod.name,
                                     yaml_str=yaml_str,
                                     _debug=self._debug,
                                     _master=self._master,
                                     _nesting_level=self._nesting_level + 1,
                                     _repo=self._repo)
        return module_loader

    def _read_yaml_file(self, yaml_file: str) -> str:
        if self._debug:
            print(f"  L: reading os file: {yaml_file}")

        yaml_str = self._repo.read_content(yaml_file)
        return yaml_str

    def _read_py_file(self, py_file: str) -> str:
        if self._debug:
            print(f"  L: reading os file: {py_file}")

        yaml_str = self._repo.read_content(py_file)
        return yaml_str


    def _check_yaml_file(self, path_to_file: str) -> tuple[bool, str]:
        if self._debug:
            print(f"  L: check path_to_file: {path_to_file}")
        yaml_file = f"{path_to_file}.yaml"
        yaml_exists = self._repo.check_file_exists(yaml_file)
        if self._debug:
            print(f"  L:  {yaml_exists = } {yaml_file = }")
        return yaml_exists, yaml_file

    def _check_py_file(self, mod: Module) -> tuple[str, bool]:
        if self._debug:
            print(f"  L: check_py_file: {mod.name}")
        path_to_file = f"{mod.name}.py"
        paths_exists = self._repo.check_file_exists(path_to_file)
        if self._debug:
            print(f"  L: {path_to_file = } {paths_exists = }")
        return path_to_file, paths_exists


    def _get_class(self, base):

        def find_module_by_alias(alias):
            # Iterate through all items in globals()
            for name, obj in globals().items():
                # Check if the object is a module and the name matches the alias
                if isinstance(obj, types.ModuleType) and name == alias:
                    return obj
            # try to find it in all loaded modules
            if alias in sys.modules:
                return sys.modules[alias]

            return None

        if "." in base:
            alias, base_name = base.split(".")
            # base_module = importlib.import_module(module_name)
            base_module = find_module_by_alias(alias)
        else:
            module_name = self.module.name
            base_name = base
            base_module = self.module.value
        return base_module, base_name

    def create_classes(self):

        try:
            # class_data = self.extract_section('classes')['classes']
            section = self.extract_section('classes')
            class_data = section.get('classes', []) if section else []

            if self._debug:
                print(f"CREATE_CLASSES: {self.module.name}: {class_data = }")
            if class_data is None:
                class_data = []
        except Exception as e:
            class_data = []
            print(f"{e = }")
            print(traceback.format_exc())
            ## DO NOT RAISE HERE 'cose empty classes section is fine
            # raise e


        for cls in class_data:
            try:
                self._create_class(cls)
            except Exception as e:
                print(f"### Error in {cls.name}")
                print(e)
                print(traceback.format_exc())
                raise e

    def _create_class(self, cls):
        cls._module = self.module
        class_name = cls.name
        # Prepare attributes and default values
        if self._debug:
            print(cls)
        attributes_with_defaults = []
        is_key = True
        for attr in cls.attributes:
            self._create_attribute(attr, attributes_with_defaults, class_name, is_key)

        try:
            if self._debug:
                print(f"{cls.bases = }")
            bases = []   # MyBaseModel]
            for base in cls.bases:
                base_module, base_name = self._get_class(base)
                base_class = getattr(base_module, base_name)
                bases.append(base_class)

            bases_tuple = tuple(bases)
        except Exception as e:
            print(f"{e = }")
            print(traceback.format_exc())
            # SHOULD I RAISE if base class is not found??
            raise e
        try:
            if self._debug:
                print(f"##Evaluating: {class_name}")
                for attr in cls.attributes:
                    print(f"Evaluating: {attr.name}: {attr.type}" in {cls.name})
            ns = self._make_namespece(cls)
        except Exception as e:
            print(f"Can't eval: {attr.name}: {attr.type}" in {cls.name})
            print(traceback.format_exc())
            raise e

        if len(cls.states) > 0:
            py_state = ("state", str, field(default=cls.states[0]))
            attributes_with_defaults.append(py_state)
        if self._debug:
            print(f"## Make dataclass: {class_name}")
            print(attributes_with_defaults)
        py_new_class = make_dataclass(
            class_name,
            attributes_with_defaults,
            bases=bases_tuple,
            repr=True,
            namespace={"__annotations__": ns}
        )
        if self._debug:
            print(f"AA{py_new_class = }")
            print(py_new_class)
        cls.value = py_new_class
        cls.bases = [w._class for w in bases_tuple]   #  if w != MyBaseModel]
        try:
            setattr(self.module.value, class_name, py_new_class)
            py_new_class.__module__ = self.module.name
        except Exception as e:
            print(f"{e = }")
            print(traceback.format_exc())
            print(f"## {class_name}")
            print(f"{type(self.module)}")
            print(self.module)
            raise e
        py_new_class.__doc__ = cls.doc
        py_new_class.icon = cls.icon
        if len(cls.states) > 0:
            py_new_class.states = cls.states
            py_new_class.state = cls.states[0]
        py_new_class._class = cls
        self.module.classes[class_name] = cls
        current_module = self.module.value  # sys.modules[__name__]
        setattr(current_module, class_name, py_new_class)
        yaml.add_representer(py_new_class, self.dataclass_representer)
        yaml.add_constructor(f'!{class_name}', self.yaml_constructor(py_new_class), Loader=yaml.SafeLoader)
        globals()[class_name] = py_new_class
        if self._debug:
            print(f"{__name__ = }")
            print(f"{py_new_class = }")
            print(f"{globals()[class_name] = }")
        # Handle methods
        for method in cls.methods:
            self._create_method(class_name, method, py_new_class)


    def _make_namespece(self, cls):
        #ns = {attr.name: eval(attr.type, globals()) for attr in cls.attributes}
        ns = {}

        # Iterate over each attribute in cls.attributes
        for attr in cls.attributes:
            try:
                # Evaluate the attribute type in the context of globals()
                evaluated_type = eval(attr.type, globals())
            except Exception as e:
                if "." in attr.type:
                    if attr.type.startswith("List["):
                        base_name = _extract_bare_type(attr.type)
                    else:
                        alias, base_name = attr.type.split(".")
                    evaluated_type = get_origin(eval(base_name, globals()))
                else:
                    # Debugging: Print the error if something goes wrong
                    print(f"Error processing attribute {attr.name}: {e}")
                    print(traceback.format_exc())
                    raise e

            # Assign the evaluated type to the attribute's name in the namespace
            ns[attr.name] = evaluated_type

            if self._debug:
                # Debugging: Print the attribute name and its evaluated type
                print(f"Assigned {attr.name} = {evaluated_type}")

        return ns

    def _create_method(self, class_name, method, py_new_class):
        method_name = method.name
        code = method.code
        # Create the function from code
        new_code = f"def {method_name}(self, *args, **kwargs):"  # {NL}    {code}{NL}"
        if self._debug:
            new_code += f"\n\tprint('🔍 >> Entering {class_name}.{method_name}')"
        new_code += f"\n\ttype(self)._class.check_state(self, '{method_name}')\n\t"
        new_code += f"\n\t__exception = False\n\t"
        new_code += f"\n\ttry:\n\t"
        new_code += "\n\t\t" + code.replace("\n", "\n\t\t")
        new_code += f"\n\texcept Exception as e:\n\t\t"
        if self._debug:
            new_code += f"\n\t\tprint('❌ xx Exception in {class_name}.{method_name}: %s', e, exc_info=True)\n\t\t"
        new_code += f"\n\t\tprint(f'Exception occured: {{e}}')\n\t\t"
        new_code += f"\n\t\t__exception = True\n\t"
        new_code += f"\n\t\traise\n\t\t"
        new_code += f"\n\tfinally:\n\t\t"
        new_code += f"\n\t\tif not __exception:\n\t\t"
        new_code += f"\n\t\t\ttype(self)._class.change_state(self, '{method_name}')\n\t"
        if self._debug:
            new_code += f"\n\t\tprint('✅ << Exiting {class_name}.{method_name}')"

        if self._debug:
            print(new_code)
        try:
            tree = ast.parse(new_code)
            func_def = tree.body[0]
        except Exception as e:
            print(e)
            print(f"Error in {class_name}.{method_name}")
            print(new_code)
            full_traceback = traceback.format_exc()
            last_lines = full_traceback.strip().splitlines()[-3:]
            last_lines = "\n".join(last_lines)
            print(last_lines)
            alter_code = f"def {method_name}(self, *args, **kwargs):{NL}\tpass{NL}"
            alter_code += f"\t\"\"\"{NL}"
            alter_code += f"\t{last_lines}{NL}"
            alter_code += f"\t{NL}{code}"
            alter_code += f"\t\"\"\"{NL}"
            print(alter_code)
            try:
                new_tree = ast.parse(alter_code)
                tree = new_tree
            except:
                print(f"Error in {class_name}.{method_name}")
                print(alter_code)
                print(last_lines)
                raise e


            #raise e

        # Compile the AST to code object
        code_obj = compile(tree, filename=f"{class_name}_{method_name}", mode="exec")
        # Create function and attach to class
        # namespace = {}
        exec(code_obj, globals())  # namespace)
        new_method = globals()[method_name]

        try:
            beartype(new_method)
        except Exception as e:
            raise TypeError(f"{new_method.__name__} has uncheckable or invalid annotations")

        setattr(py_new_class, method_name, new_method)  # namespace[method_name])
        if method.doc:
            globals()[method_name].__doc__ = method.doc
        method.value = code_obj

    def _create_attribute(self, attr, attributes_with_defaults, class_name, is_key):
        name = attr.name
        type_str = attr.type
        default_value = attr.default if attr.default else MISSING
        py_new_attr = None
        try:

            if attr.default is not None:
                def_value = attr.default
                if def_value == "None":
                    def_value = None
                else:
                    # def_value = "lambda: " + f"{attr.default}"
                    try:
                        # EXPERIMENTAL DEACTIVATION
                        ...

                        # def_value = eval(str(def_value), globals())
                    except Exception as e:
                        print(f"### Warning in {class_name}.{name} default value: {def_value}")
                        print(e)
                        print("More:")
                        print(traceback.format_exc())
                attr_type = self._get_class(type_str)

                if type_str.lstrip().startswith("List["):
                    # new style for defaults!!!
                    py_new_attr = (name, attr_type, get_dataclass_field_str(type_str, def_value, is_key))
                else:
                    py_new_attr = (name, attr_type, field(default=def_value, repr=is_key))

            else:
                def_value = None
                # py_new_attr = (name, eval(type_str, globals()), get_dataclass_field_str(type_str, def_value))

                attr_type = self._get_class(type_str)
                py_new_attr = (name, attr_type, get_dataclass_field_str(type_str, def_value, is_key))
            is_key = False  # only the first one is the key ...
            attributes_with_defaults.append(py_new_attr)
            attr.value = py_new_attr
        except Exception as e:
            print(f"### Exception in {class_name}.{name} default value: {def_value}")
            print(e)
            print(traceback.format_exc())

    def load_instances(self):

        try:
            instance_data = self.extract_section('instances')['instances']
        except Exception as e:
            instance_data = []
            print(f"Error: {e}")
            print("Error details")
            global_dict = globals()
            user_classes = [name for name, obj in global_dict.items() if
                            isinstance(obj, type)]
            # isinstance(obj, type) and obj.__module__ == '__main__']
            print(f"{user_classes = }")
            print(traceback.format_exc())
            raise e

        assert isinstance(instance_data, list)

        self.module.instances = instance_data

        for instance in instance_data:
            if hasattr(instance, "_declare"):
                instance._declare(module=self.module)
            else:
                print(f"⚠️ {type(instance).__name__} has no _declare method")


    @property
    def K_MOD(self):
        return f"K_MOD_{self.module_name}"

    def load(self, force=False, yaml_str=None) -> Module:
        if yaml_str is not None:
            self.yaml_str = yaml_str
        elif self.yaml_str is None:
            self.yaml_str = self._read_yaml_file(f"{self.module_name}.yaml")
        if True:
            self.load_header()
            self.import_modules()
            self.create_classes()
            self.load_instances()
        return self.module

    def unload(self, force=False, yaml_str=None) -> Module:
        """Unloads the module, clearing its instances and classes."""
        self.module._unmake()
        return self.module


    def run(self, design=False):

        if True:
            print(f"{self.module.title}")
            for i in self.module.instances:
                try:
                    if hasattr(i, "_run"):
                        # i._run()
                        if not i._run(module=self.module):
                            if self._debug:
                                print(id(i))
                                print(f"{i}._run() stopped")
                            break
                except Exception as e:
                    print(f"⚠️⚠️ {e}")
                    # print("Error details")
                    print(i)
                    # print(type(i))
                    # print(traceback.format_exc())
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    tb = traceback.extract_tb(exc_traceback)
                    filename, lineno, funcname, line = tb[-1]
                    print(f"Error in {type(i)} {filename} line {lineno}:")
                    prefix = len(type(i)._class.name) + 1
                    method_name = filename[prefix:]
                    # method = type(i)._class.methods[0]
                    method = type(i)._class.find_method(method_name)
                    print(f"  1 def {method_name}():")
                    line_no = 2
                    if method is not None:
                        for line in method.code.split("\n"):
                            if line_no == lineno:
                                print(f"{line_no:>3}   {line} 👈 ⚠️ {e}")
                                print(f"     ☝️🤢")
                                break
                            else:
                                print(f"{line_no:>3}   {line}")
                            line_no += 1

                    if self._debug:
                        print("---")
                        print(line)
                        # Display surrounding context
                        context = 3  # Number of lines to show around the error line
                        start = max(1, lineno - context)
                        end = lineno + context
                        for i in range(start, end + 1):
                            line = linecache.getline(filename, i).rstrip()
                            marker = '>>' if i == lineno else '  '
                            print(f"{i}: {marker} {line}")

                        print(i)
        #print("---")

        if self._debug:
            print(self.module.instances[0])

    def test(self) -> int:

        debug = self._debug
        nb_errors = 0
        try:

            check_err = self.module._check()
            nb_errors += check_err
            for tag in self.module.get_tags():
                print(f"  {tag}")

            try:
                assert check_err == 0
            except AssertionError as e:
                print(e)
                print(f"⚠️ Module has errors, can't run tests:")
                raise e

            self._debug = True
            if self._debug:
                print(f"Loading {self.module_name}")
            if debug:
                print("Debug")
                try:
                    self.load_header()
                    self.import_modules()
                    self.create_classes()
                    self.load_instances()
                except Exception as e:
                    print(e)
                    print(traceback.format_exc())
                    raise e

            print(f"System Under Test: {self.module.title}")

            if True:  # test instances one by one
                print(f"{self.module.title}")
                for i, instance in enumerate(self.module.instances):
                    try:
                        if hasattr(instance, "_test"):
                            if not instance._test(module=self.module):
                                if self._debug:
                                    print(id(instance))
                                print(f"{i}._test() stopped")
                                nb_errors += 1
                                break
                    except Exception as e:
                        print(e)
                        print(traceback.format_exc())
                        raise e

            for cn, c in self.module.classes.items():
                print()
                print(f"## {c.icon} {cn}")
                print(f"ℹ️ {c.doc}")
                for m in c.methods:
                    if m.name.startswith("_test_"):
                        if self._debug:
                            print(f"### {cn}.{m.name}")

                        if True:  # st.form(key=f"{cn}_{str(id(i))}_{m['name']}"):
                            try:
                                label = f"✅ {m.title}"
                                instance = c.value(_module = self.module)  # dummy instance
                                # i = c.value()  # dummy instance
                                m2c = getattr(instance, m.name)
                                result = m2c()
                            except Exception as e:
                                nb_errors += 1
                                label = f"❌ {m.title}"
                                result = None
                                print(f"{m.name}: ❌")
                                if True:   # with st.expander("Error details", expanded=True):
                                    print(e)
                                    if debug:
                                        print(dir(instance))
                                    print(instance)
                            if True:
                                print(f"ℹ️ {m.doc}")
                                code = "def " + m.name + "():\n    " + m.code.replace("\n", "\n    ")
                                print(code)
                                print(f"`{result = }`")

        except Exception as e:
            print(e)
            if debug:
                print(traceback.format_exc())
        finally:
            self._debug = debug
            print(f"#")
            if nb_errors == 0:
                print(f"# ✅ Done with no errors.")
            else:
                print(f"# ❌ Done with {nb_errors} errors.")

        return nb_errors

    def _build_py_module(self, module_data, path_to_file):

        module_name = module_data.name
        module_alias = module_data.as_name
        py_str = self._read_py_file(path_to_file)
        # The dynamic module name and the code as a string
        mod_name = f"modules.{module_name}"
        module_code = f"{py_str}"

        # Step 1: Create a new module object
        pymodule = types.ModuleType(mod_name)
        # Step 2: Execute the string code in the module's namespace
        exec(module_code, pymodule.__dict__)
        # Step 3: Register the module in sys.modules
        sys.modules[mod_name] = pymodule

        # this is added to access the module from the global namespace
        globals()[module_alias] = pymodule

        # Example of usage:
        # Now you can import it using importlib.import_module
        # imported_module = importlib.import_module(mod_name)
        # Test if the module works as expected
        # imported_module.hello()

# END OF FILE HERE


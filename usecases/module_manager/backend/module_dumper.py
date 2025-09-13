# (c) 2020 mz
from dataclasses import dataclass
import yaml
import copy
from dataclasses import is_dataclass, fields
from typing import Any

from usecases.common.backend.module_wrapper import Module, NL


def dump_module(module: Module) -> str:
    dumper = ModuleDumper(module=module)
    yaml_str = dumper.dump()
    return yaml_str


@dataclass
class ModuleDumper:
    module: Module

    def dump(self) -> str:
        self_module = self.module
        ## DONE: name not needed anymore. The filename is enough ...
        ## f"  - name: {self_module.name}" + NL + \

        module_header = "module:" + NL + \
                        f"    doc: {self._reformat_text(self_module.doc, 6)}" + NL + \
                        f"    icon: \"{self_module.icon}\"" + NL + \
                        f"    tag: \"{self_module.tag}\"" + NL
        if self_module.is_admin:
            module_header += f"    is_admin: \"{self_module.is_admin}\"" + NL
        imports = "imports:" + NL

        for i in self_module.imports.values():
            imports += f"  - !Module {{name: {i.name}"
            if i.as_name != i.name:
                imports += f", as_name: {i.as_name}"
            if i.hidden:
                imports += f", hidden: {i.hidden}"
            imports += f"}}" + NL
        imports += NL

        clz = "classes:" + NL
        if len(self_module.classes) > 0:
            clz += "  # forward declarations:" + NL
        for c in self_module.classes.values():
            clz += f"  - !Class {{name: {c.name}}}" + NL
        clz += NL

        for c in self_module.classes.values():
            clz += f"  - !Class" + NL
            clz += f"    name: {c.name}" + NL
            # clz += f"    doc: |{NL}      {c.doc}" + NL  # LATERTODO: multiline doc to split and save
            if len(c.doc) > 0:
                clz += f"    doc: {self._reformat_text(c.doc, 6)}" + NL
            clz += f"    icon: '{c.icon}'" + NL
            if len(c.bases) > 0:
                clz = self._get_base_classes(c, clz, self_module)
            if len(c.attributes) > 0:
                clz += f"    attributes:" + NL
            for a in c.attributes:
                clz += f"    - !Attribute" + NL
                clz += f"      name: {a.name}" + NL
                clz += f"      type: {a.type}" + NL
                if len(a.doc) > 0:
                    # clz += f"      doc: \"{a.doc}\"" + NL
                    clz += f"      doc: {self._reformat_text(a.doc, 8)}" + NL
                if a.icon not in ["📦"]:
                    clz += f"      icon: \"{a.icon}\"" + NL
                if a.default not in [None, ""]:
                    clz += f"      default: {a.default}" + NL
                if a.read_only:
                    clz += f"      read_only: {a.read_only}" + NL
                if a.is_long:
                    clz += f"      is_long: {a.is_long}" + NL
                if a.language:
                    clz += f"      language: {a.language}" + NL
                if a.following != 0:
                    clz += f"      following: {a.following}" + NL
                if a.advanced:
                    clz += f"      advanced: {a.advanced}" + NL
                if a.hidden:
                    clz += f"      hidden: {a.hidden}" + NL
                if len(a.option_field) > 0:
                    clz += f"      option_field: {a.option_field}" + NL
                if a.options:
                    clz += f"      options: {a.options}" + NL
                if a.captions:
                    clz += f"      captions: {a.captions}" + NL
            if len(c.states) > 0:
                clz += f"    states: {c.states}" + NL
            if len(c.methods) > 0:
                clz += f"    methods:" + NL

            for m in c.methods:
                clz += f"    - !Method" + NL
                clz += f"      name: {m.name}" + NL
                if len(m.doc) > 0:
                    # clz += f"      doc: \"{m.doc}\"" + NL
                    clz += f"      doc: {self._reformat_text(m.doc, 8)}" + NL
                if m.icon not in ["⚙️"]:
                    clz += f"      icon: {m.icon}" + NL
                if len(m.preconditions) > 0:
                    clz += f"      preconditions: {m.preconditions}" + NL
                if len(m.postcondition) > 0:
                    clz += f"      postcondition: {m.postcondition}" + NL
                clz += f"      code: |" + NL
                for line in m.code.split(NL):
                    clz += f"        {line}" + NL

        # representers = yaml.representer.Representer.yaml_representers
        # for data_type, representer in representers.items():
        #    print(f"{data_type}: {representer}")

        # clz = "classes:" + NL # + \
        # yaml.dump(list(self.classes.values()), default_flow_style=False, allow_unicode=True, sort_keys=False)

        inst = self._custom_dump(self_module)

        instances = "instances:" + NL
        for line in inst.split(NL):
            if line.startswith("- !") or line.startswith("- &"):
                line = NL + "  " + line
            instances += f"  {line}" + NL

        return module_header + imports + clz + NL + instances

    import copy
    from dataclasses import is_dataclass, fields
    from typing import Any

    @staticmethod
    def strip_recursive_refs(obj: Any) -> Any:
        visited = set()

        def _strip(o: Any, ancestry: set[int]) -> Any:
            obj_id = id(o)
            if obj_id in ancestry:
                return None  # Avoid recursion
            ancestry = ancestry | {obj_id}

            # Recursively handle dataclasses
            if is_dataclass(o):
                o_copy = copy.copy(o)
                for f in fields(o):
                    val = getattr(o, f.name)
                    val_stripped = _strip(val, ancestry)
                    setattr(o_copy, f.name, val_stripped)
                return o_copy

            # Recursively handle dicts
            elif isinstance(o, dict):
                return {k: _strip(v, ancestry) for k, v in o.items()}

            # Recursively handle lists or tuples
            elif isinstance(o, (list, tuple)):
                new_items = [_strip(item, ancestry) for item in o]
                return type(o)(new_items)

            # Other objects (non-dataclass, non-collection)
            return o

        return _strip(obj, visited)

    def _custom_dump(self, self_module: Module) -> str:
        # safe_instances = self.strip_recursive_refs(self_module.instances)
        safe_instances = self_module.instances
        inst = yaml.dump(safe_instances, default_flow_style=False, allow_unicode=True, sort_keys=False)
        return inst

    def _OLD_custom_dump(self, self_module):
        inst = yaml.dump(self_module.instances, default_flow_style=False, allow_unicode=True, sort_keys=False)
        return inst

    def _get_base_classes(self, c, clz, self_module):
        clz += f"    bases: [" + ", ".join \
            ([f"{b._module.name + '.' if b._module != self_module else ''}{b.name}" for b in c.bases]) + "]" + NL
        return clz

    def standard_dump(self) -> str:
        self_module = self.module
        """Dump the instances to yaml"""
        return yaml.dump(self_module.instances, default_flow_style=False, allow_unicode=True, sort_keys=False)


    def _reformat_text(self, doc: str, ident: int=0):
        if len(doc) < 50:
            return doc
        lines = doc.split(NL)
        new_doc = "|"
        for line in lines:
            new_doc += f"{NL}{' ' * ident}{line}"
        return new_doc
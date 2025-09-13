# (c) 2020 mz
import types
from dataclasses import dataclass
from typing import List, get_origin, Tuple
import traceback
import sys
import builtins

from usecases.common.backend.module_wrapper import Module, Class, Attribute, NL

NL = "\n"

NNL = "\\n"

@dataclass
class ModuleDecorator:
    """
    Decorates a module in a deep way (imported modules included)
    """
    def get_import_tree(self, module: Module, level: int = 1) -> str:
        result = f"{'  ' * level} {module.name} {id(module)}: {len(module.imports)}"
        for mod in module.imports.values():
            result += NL + self.get_import_tree(mod, level + 1)
        return result

    def get_module_tree(self, module: Module, deep: bool = True, level: int = 0) -> str:
        result = f"{'  ' * level} {module.name} {id(module)}: {len(module.classes)}"
        for class_ in module.classes.values():
            base_icons = [b.icon for b in class_.bases]
            label = class_.label()
            result += NL + label + f": {','.join(base_icons)}"
            if deep:
                for attribute in class_.attributes:
                    result += NL + f"{'  ' * (level + 1)}" + self._get_attribute_label(class_, attribute)
                    # Deactivated for now:
                    # result += NL + f"{'  ' * (level + 1)}" + self._get_label_for_diag(module, attribute.name, attribute.type)
                for method in class_.methods:
                    result += NL + f"{'  ' * (level + 1)} ⏵  {method.name}()"
        return result


    def _get_attribute_label(self, class_: Class, attribute: Attribute, capitalize: bool = False, is_long: bool = False) -> str:
        module = class_._module
        """
        Computes the label for an attribute
        :param attribute_name: attr name
        :param attribute_type: int, str, Person, ...
        :param capitalize:
        :param aclassname: the class name owning the attribute, optional. Helps to identify reflexivity
        :return: the label
        """
        attribute_name = attribute.name
        attribute_type = attribute.type
        cname = attribute_name.capitalize() if capitalize else attribute_name
        if (attribute_name.startswith("on ") or attribute_name.startswith("before ")
            or attribute_name.startswith("after ") or attribute_name == "code"):
            return f"⚡️{cname}"
        match attribute_type:
            case "str":
                match attribute_name:
                    case "password":
                        return f"🔒 {cname}"
                    case _ if is_long:
                        return f"🔡 {cname}"
                    case _:
                        return f"🔤 {cname}"

            case "int" | "float":
                return f"🔢 {cname}"
            case "bool":
                return f"🔘 {cname}"
            case "date":
                return f"📅 {cname}"  # 📆🗓
            case "datetime":
                return f"🕗 {cname}"
            case 'list':
                return f"⦙ {cname}"
            case _:
                pass

        try:
            # TODO: improve to "safe eval"!
            the_type = eval(attribute_type, globals())
        except Exception as e:
            the_type = attribute_type  # + f" Error: {e}"
            if attribute_type.startswith("List["):
                if attribute_type.endswith("]"):
                    inner_type = attribute_type[5:-1].strip()
                    if module.classes.get(inner_type) is not None:
                        the_type = List[inner_type]
                        icon = module.classes[inner_type].icon
                        return f"{icon}⦙ {attribute_name}"  # ⁺⫶⋮⋆ⁿₙᵢ
                    else:
                        the_type = List[types.NoneType]
            else:
                the_type = List[None]  # List[types.NoneType]

        origin = get_origin(the_type)
        if origin is None:
            try:
                icon = the_type._class.icon
            except:
                icon = "📦"
            return f"{icon} {cname}"

        if (origin is list) or (origin is List):
            try:
                inner_type = the_type.__args__[0]
            except:
                inner_type = "…"
            try:
                # print(f"{inner_type = }")
                if inner_type is not types.NoneType:
                    return f"{module._get_attribute_label('', inner_type.__name__, capitalize=capitalize)}⦙ {cname}"
            except:
                try:
                    icon = module.classes.get(inner_type)._class.icon
                except:
                    icon = "📦"
                return f"{icon}⦙ {cname}"
        else:
            try:
                icon = module.classes.get(inner_type)._class.icon
            except:
                icon = "📦"
            return f"{icon}⦙ {cname}"
        return f"📦 {cname}"

    def _get_label_for_diag(self, module: Module, attribute_name: str = "", attribute_type: str = "str") -> str:

        if attribute_type.startswith("List["):
            attribute_type = attribute_type[5:-1].strip()
            is_list = True
        else:
            is_list = False
        slist = "⦙ " if is_list else ""

        if (attribute_name.startswith("on ") or attribute_name.startswith("before ")
            or attribute_name.startswith("after ") or attribute_name == "code"):
            return f"⚡ {attribute_name}"
        if attribute_type == "str":
            return f"🔤 {slist}{attribute_name}"
        if attribute_type in ["int", "float"]:
            return f"🔢 {slist}{attribute_name}"
        if attribute_type == "bool":
            return f"🔘 {slist}{attribute_name}"
        if attribute_type == "date":
            return f"📅 {slist}{attribute_name}"  # 📆🗓
        if attribute_type == "datetime":
            return f"🕗 {slist}{attribute_name}"
        if attribute_type == list:
            return f"⦙ {attribute_name}"

        try:
            the_type = eval(f"sys.modules['{module.name}'].{attribute_type}", globals())
        except Exception as e:
            the_type = attribute_type  # + f" Error: {e}"
            if attribute_type.startswith("List["):
                if attribute_type.endswith("]"):
                    inner_type = attribute_type[5:-1].strip()
                    if module.classes.get(inner_type) is not None:
                        the_type = List[inner_type]
                        icon = module.classes[inner_type].icon
                        return f"{icon} ⦙ {attribute_name}"  # ⁺⫶⋮⋆ⁿₙᵢ
                    else:
                        the_type = List[types.NoneType]
            else:
                the_type = List[None]  # List[types.NoneType]

        origin = get_origin(the_type)
        if origin is list or origin is List:
            try:
                inner_type = the_type.__args__[0]
            except:
                inner_type = "…"
            try:
                if inner_type is not types.NoneType:
                    return f"{self._get_label_for_diag(module, '', inner_type.__name__)} ⦙ {attribute_name}"  # ⁺⫶⋮⋆ⁿₙᵢ
            except:
                return f"⦙ {attribute_name}"
        else:
            ...
            # get class by name (pets) and get icon
            ref_class = module.find_class(attribute_type)
            return f"{ref_class.icon} ⦙ {attribute_name}"

        return f"📦 {attribute_name}"



    def get_diagram(self, module: Module, main_graph: bool = True, main_module: Module = None,
                    debug: bool = False, statemachines: bool = True) -> str:

        if main_graph:
            main_module = module
            main_module._imported = []
            # main_module._display_import_tree(1)

        if module in main_module._imported:
            return ""

        # st.write(f" diag: from {self.name} for {main_module.name}: imported: {[m.name for m in self._imported]}")

        # st.caption(f"{self.name = }")
        prefix = self._get_prefix()

        legend = self._get_legend()


        cls = ""
        module_states = "" # this compiles all statemachines of a whole module

        # st.write(f"{self.module.classes = }")
        imports = ""
        imports = self._treat_imports(debug, imports, main_module, module, statemachines=statemachines)

        for class_ in module.classes.values():
            one_cls, module_states_all = self._treat_class(class_, debug, module, statemachines)
            cls += one_cls
            module_states += module_states_all

        if False:
            # do not draw an empty module
            if len(cls) == 0:
                return ""


        # else:
        #    cls += f" pk_{self.name} " + NL
        #    cls += f" {next(iter(self.classes.values())).name} -> pk_{self.name}  ; " + NL  # [style=invis];
        if True: ## st.container
            try:
                module_name = module.name
                # nodesep=0.25;

                ndoc = module.doc.replace("\n", "\\n")
                tooltip: str = "" if len(ndoc) == 0 else f'tooltip=\"{module.icon} {ndoc}\";'

                my_border = NL + f'subgraph cluster_{module_name}' + \
                            f' {{label="{module.icon} {module_name}"; nodesep=0.25; color=grey85; ' + \
                            f'{tooltip}' + \
                            f'style="filled"; fillcolor=grey98; margin=30; penwidth=0.1;' + \
                            (f'color=blue; fontcolor=blue;' if main_graph else '')
                # f' invisible_{self.name} [style=invis];' + NL
                more_imports = ""
                for imp in module.imports.values():
                    # if len(imp.classes) == 0:
                    icon_imp = imp.icon if imp.icon not in ["", "🧩"] else "🛄"
                    more_imports += (f'{icon_imp} {imp.name} {imp.as_name if imp.as_name != imp.name else ""}\l')
                if len(more_imports) > 0:
                    more_imports = f'Imports_{module.name} [label = "{more_imports}", shape=box, style="filled, rounded", fillcolor=white, color=lightgrey, penwidth=0.5]'
                    my_border += more_imports + NL

                    # my_border += f' invisible_{imp.name} [style=invis];' + NL
                    # my_border += f' invisible_{imp.name} -> invisible_{self.name} [style=invis];' + NL

                    #  "dotted"
                    # f'style="filled, bold"; fillcolor=grey98; style="rounded"; margin=30'  # "dotted"
                if statemachines:
                    my_border += module_states
                if main_graph:
                    s = prefix + imports + my_border + NL + cls + NL + "}" + NL + legend + "}" + NL
                    if debug:
                        # with st.expander("Debug"):
                        print(s)
                    #st.graphviz_chart(s, use_container_width=True)
                    return s
                else:
                    return imports + my_border + cls + NL + "}" + NL
            except Exception as e:
                print(e)
                print(traceback.print_exc())
                raise e

    def _treat_imports(self, debug: bool, imports: str, main_module: Module, module: Module, statemachines: bool = True):
        for mo in module.imports.values():
            if mo.hidden:
                continue
            if mo not in main_module._imported:
                imports += self.get_diagram(module=mo, main_graph=False, main_module=main_module, debug=debug, statemachines=statemachines)
                main_module._imported.append(mo)
                # st.write(f"{main_module.name}: {self.name}->{mo.name}/{mo.as_name} {mo.hidden = }")
                # st.write(f"{[m.name for m in main_module._imported]}")
        return imports

    def _treat_class(self, class_: Class, debug: bool, module: Module, statemachines: bool) ->  Tuple[str, str]:
        module_states = ""
        cls = f'{module.name}_{class_.name};' + NL
        cls_bases, ignored_bases = self._get_bases(class_, module, debug)
        cls += cls_bases
        attrs = ""
        assocs = ""
        for a in class_.attributes:
            assoc, attr = self._treat_attribute(a, class_, module)
            assocs += assoc
            attrs += attr
        meths = ""
        states = ""
        state_contents = {}

        def make_state(state: str, states: list[str], activity: str = "") -> str:
            if state not in state_contents:
                state_contents[state] = ''
            if len(activity) > 0:
                if state_contents[state] == '':
                    state_contents[state] = f"| ▹ {activity}\l"
                else:
                    state_contents[state] += f" ▹ {activity}\l"
            label = f'➡️ {state}' if state == states[0] else state
            return f'state_{class_.name}_{state} [label="{{{label} {state_contents[state]}}}"]'

        if statemachines and len(class_.states) > 0:
            for s in reversed(class_.states):
                states += make_state(s, class_.states) + NL
        for m in [m for m in class_.methods]:
            mm, states = self._treat_method(class_, m, make_state, statemachines, states)

            if not debug:
                if m.name.startswith("_"):
                    continue
                if m.name.startswith("test_"):
                    continue
                if m.name.startswith("build"):
                    continue

            mm = f'{mm}\l'
            meths += mm
        if len(ignored_bases) > 0:
            sbases = f" ➭ {' '.join([b.icon for b in ignored_bases])}"
        else:
            sbases = ""
        ndoc = class_.doc.replace("\n", "\\n")
        tooltip: str = "" if len(class_.doc) == 0 else f', tooltip=\"{class_.icon} {ndoc}\"'
        cls += f'{module.name}_{class_.name} [label = "{{{class_.icon} {class_.name} {sbases}\l|{attrs}|{meths}}}" {tooltip}];' + NL
        cls += assocs
        if statemachines and len(class_.states) > 0:
            tooltip: str = f'tooltip=\"States of {class_.icon} {class_.name}\";'

            statemachine_border = NL + f'subgraph cluster_statemachine_{class_.name}' + NL + \
                                  "{rankdir = BT; #nodesep=0.1;" + NL + \
                                  f' {tooltip}' + \
                                  f' label="{class_.icon} states 🎛️"; color=grey85; ' + \
                                  f'style="filled, rounded"; fillcolor=white; margin=30; ' + \
                                  f'penwidth=0.1; ' + """
                            node[
                                fontname = "Monaco,sans-serif"
                                penwidth = 0.3
                                shape = record
                                style = "filled, rounded"
                                fillcolor = "gray95"
                                color = "gray"
                                fontsize = 12
                            ]
                            edge[
                                style = "solid"
                                arrowhead = "open"
                                penwidth = 0.2
                                arrowsize = 0.5
                                fontsize = 10
                            ]""" + NL

            states = statemachine_border + NL + states + "}" + NL
            module_states += states + NL + \
                             f'state_{class_.name}_{class_.states[0]} -> {module.name}_{class_.name} [style=dashed, arrowhead="none"];' + NL
            # "" # f'state_{c.name}_{c.states[0]} -> {c.name} [style=dashed, arrowhead="none", arrowsize=0.5];' + NL + \
        return cls, module_states

    def _treat_method(self, c, m, make_state, statemachines: bool, states):
        if not m.name.startswith("__"):  # private attrs
            mname = m.name.replace("_", " ")
        else:
            mname = m.name
        mm = mname
        if len(m.preconditions) > 0:
            mm = f' ▹ {mm}'
        else:
            mm = f' ▸ {mm}'
        if len(m.postcondition) > 0:
            mm = f'{mm} ▹'
        if statemachines:
            for p in m.preconditions:
                if len(m.postcondition) == 0:
                    _c = c
                    while len(_c.states) == 0:
                        if len(_c.bases) == 0:
                            break  # NOT consistent
                        _c = _c.bases[0]

                    states += make_state(p, _c.states, mname) + NL
                else:
                    # here headlabel is a space to force label visible (DOT bug)
                    states += f'state_{c.name}_{p} -> state_{c.name}_{m.postcondition} ' \
                              f'[label="{mname}", headlabel=" ", constraint=false]' + NL
        return mm, states

    def _treat_attribute(self, a: Attribute, c: Class, module: Module) -> Tuple[str, str]:
        assocs = ""
        attrs = ""
        aa = a.name
        sdest_type = a.type
        pydest_type = None
        is_list = False
        is_my_type = False
        if sdest_type.startswith("List["):
            sdest_type = sdest_type[5:-1].strip()
            is_list = True
        try:
            if sdest_type.find(".") < 0:
                if not is_builtin_type_name(sdest_type):
                    clz = module.find_class(sdest_type)
                    modz = clz._module
                    squaldest_type = f"sys.modules['{modz.name}'].{sdest_type}"
                    # squaldest_type = f"sys.modules['{module.name}'].{sdest_type}"
                    if hasattr(module, sdest_type):
                        pydest_type = getattr(module.value, sdest_type)  # eval(sdest_type, globals())
                    else:
                        pydest_type = eval(squaldest_type, globals())
                else:
                    pydest_type = eval(sdest_type, globals())
            else:
                module_name = sdest_type.split(".")[0]
                type_name = sdest_type.split(".")[1]
                if hasattr(sys.modules[module_name], type_name):
                    pydest_type = getattr(sys.modules[module_name], type_name)
                # pydest_type = eval(sdest_type, globals())
            is_my_type = hasattr(pydest_type, "_class")
        except Exception as e:
            is_my_type = False
            print(e)
            print("Error in eval: " + sdest_type)
            print(traceback.format_exc())
            # raise e
        arrowhead = "normal"
        if aa.startswith("_"):  # prefer UML convention for derived assocs
            aa = aa.replace("_", "/ ", 1)
            arrowhead = "crow"
        aa = aa.replace("_", " ")
        if sdest_type in [c.name]:  # reflexive attribute
            if is_list:
                aa = f'{self._get_label_for_diag(module, aa, a.type)} ↩️'
            else:
                aa = f'{self._get_label_for_diag(module, aa, a.type)} ⤴️'
            if a.owned:
                aa += " ♢"
            attrs += f'{aa}\l'
        elif sdest_type in ["kore.Object", "Object"]:  # Object
            if is_list:
                # aa = f'{module._get_label(aa, a.type)}'
                aa = f'{self._get_label_for_diag(module, aa, a.type)}'
            else:
                # aa = f'{module._get_label(aa, a.type)}'
                aa = f'{self._get_label_for_diag(module, aa, a.type)}'
            if a.owned:
                aa += " ♢"
            attrs += f'{aa}\l'
        elif not is_my_type:  #

            #aa = f'{self._get_attribute_label(class_=c, attribute=a, is_long=a.is_long)}'  ## a.type
            aa = f'{self._get_label_for_diag(module, aa, a.type)}'  ## a.type
            if isinstance(a.default, str):
                aa_val_default = str(a.default).replace('{', '\{').replace('}', '\}')
            else:
                aa_val_default = str(a.default)
            aa_val_default = f' = {aa_val_default}' if a.default is not None else ""
            if len(aa_val_default) > 15:
                aa_val_default = f"{aa_val_default[:15]}…"
            attrs += f'{aa}{aa_val_default}\l'
        else:
            atype = sdest_type  # a.type
            s: str = atype
            if s.find(".") >= 0:
                atype = s.replace(".", "_")
            else:
                nmodule_name = module.find_class(atype)._module.name
                atype = f"{nmodule_name}_{atype}"
            # convention: if role name is the same as the class name, don't show it
            sdest_bare_name = sdest_type.split(".")[-1]
            if aa.startswith("/ "):
                aaa = aa[2:]
                aaname = "/ " if sdest_bare_name.lower() == aaa.lower() else aa
            else:
                aaa = aa
                aaname = "" if sdest_bare_name.lower() == aaa.lower() else aa
            if aaname.startswith("_"):  # prefer UML convention for derived assocs
                aaname = aaname.replace("_", "/", 1)
            if is_list:
                aaname = "⦙ " if f"{s.lower()}s" == a.name.lower() else f'⦙ {aaname}'

            if a.owned:
                arrowtail = "diamond"
            else:
                arrowtail = "none"

            aa_default = " = " if a.default is not None else ""

            asso = f""" 
                      {module.name}_{c.name} -> {atype} [
                    dir = back, arrowtail = {arrowtail}, color=blue, labeldistance=2, fontcolor=blue,
                          taillabel = "", label = " ", headlabel = "{aaname}{aa_default}", fontsize = "6"]
                    """

            #  aaname instand of a["name"]
            assocs += asso
        return assocs, attrs

    def _get_bases(self, c, module, debug) -> Tuple[str, List[Class]]:

        cls = ""
        ignored_bases = []
        for base in c.bases:
            if hasattr(base, "name"):
                sbase: str = base.name
                if sbase == "Object":
                    if base not in ignored_bases:
                        ignored_bases.append(base)
                    continue
                cls += NL + f"# {sbase = }" + NL
                if sbase.find(".") >= 0:
                    sbase = sbase.replace(".", "_")
                else:
                    sbase = f"{base._module.name}_{sbase}"
                constraint_str = "constraint=true" if not debug else "constraint=false"
                cls += f'{module.name}_{c.name} -> {sbase} [color=black, penwidth=0.3, {constraint_str}];' + NL
        return cls, ignored_bases

    def _get_legend(self):

        legend = """
                    subgraph cluster_legend {
                        # label="Legend"; // Name of the package
                        #color=grey85;
                        style=invis; //"filled, rounded";
                        fillcolor=white;
                        fontsize = "10" 
                        fontcolor=gray
                """
        legend_label = """
                        legend [style="filled, rounded", fillcolor=gray98, fontcolor="#505050", label = "{
                            Legend 
                          | 🔤 str or 🔡 long str\l
                            🔢 int or float\l
                            🔘 bool\l
                            🕗 datetime\l
                            🔒 password\l
                            🔤 ⦙ list of 🔤\l
                            ◻️ Object from kore\l
                            📦 any\l 
                            🐟 custom type Fish\l 
                             /  derived\l
                             _  private\l
                             =  default value\l
                            ⤴️ reflexive reference\l
                            ↩️ ⦙ reflexive collection\l 
                             ♢ composite or owned\l| 
                            ⚡️ event or code\l 
                             ▸ method\l
                             ▹ conditionnal method\l
                             ▹ with transition ▹\l|
                            🎛️ state machine\l 
                            ➡️ initial state\l| 
                             ➭  inherits from\l| 
                            🛄 imported py\l}"];
                    }
                    """

        legend_label2 = """
                        legend [style="filled, rounded", fillcolor=gray98, fontcolor="#505050", label = "{
                            Legend 
                          | 🔤 str or 🔡 long str\l
                            🔢 int or float\l
                            🔘 bool\l
                            🕗 datetime\l
                            🔒 password\l
                            🔤 ⦙ list of 🔤\l
                            ◻️ Object from kore\l
                            📦 any\l 
                            🐟 custom type Fish\l 
                             /  derived\l
                             _  private\l
                             =  default value\l
                            ⤴️ reflexive reference\l
                            ↩️ ⦙ reflexive collection\l 
                             ♢ composite or owned\l| 
                            ⚡️ event or code\l 
                             ▸ method\l
                             ▹ conditionnal method\l
                             ▹ with transition ▹\l|
                            🎛️ state machine\l 
                            ➡️ initial state\l| 
                             ➭  inherits from\l| 
                            🛄 imported py\l}"];
                        }
                        """
        return legend + NL + legend_label2.replace("\n", " ") + NL + NL

    def _get_prefix(self) -> str:
        prefix = """
                    digraph {
                      rankdir = BT
                      nodesep=0.25
                      graph [
                          penwidth=0.1    
                          splines=ortho
                          #splines=polylines
                          #splines=spline
                          #nodesep=1
                          lineheight=4
                          fontsize=12
                          fontname="Monaco,sans-serif"
                      ]
                      node [
                          fontname="Monaco,sans-serif"
                          penwidth=0.5    
                          shape=record
                          style=filled
                          color=lightgray
                          fillcolor=white # gray98
                          fontsize = "12" 
                      ]
                      edge [
                          fontname="Monaco,sans-serif"
                          penwidth=0.2    
                          fillcolor=gray99
                      ]
                  """ + NL
        return prefix


def is_builtin_type_name(type_name: str):
    return hasattr(builtins, type_name) and isinstance(getattr(builtins, type_name), type)

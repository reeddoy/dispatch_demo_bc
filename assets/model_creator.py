import os, string

underscore = "_"
dash = "-"
empty = ""
space = " "
spike = "`"

ors = dict(str='""', int=0, bool=False)


class Property:
    def __init__(self, line: str) -> None:
        line = line.replace(dash, empty).strip()
        words = line.split()
        self.name = words[0]
        self.type = words[1].strip(spike)
        self.nr = "`nr`" in line

        if "list" in self.type:
            self.default = " = []"
        elif "dict" in self.type:
            self.default = " = {}"
        elif "`nr`" in line:
            self.default = " = None"
        else:
            self.default = ""


class Data:
    def __init__(
        self,
        datas: "Datas",
        name: str,
        inherited_properties: list[str],
    ):
        self.datas = datas
        self.inherited_properties = inherited_properties
        self.name = name.replace(dash, empty).strip()
        self.plural_name = self.name

        if self.name.endswith("s"):
            self.plural_name = self.name + "es"
        elif self.name.endswith("y"):
            self.plural_name = "".join(self.name[:-1]) + "ies"
        else:
            self.plural_name = self.name + "s"

        self.properties: list[Property] = []

    @property
    def py(self):
        annotations = ""
        consts = ""
        _def = ""

        for property in self.properties:
            default = property.default
            prop_name = ""

            if default:
                _def = " = None"

            if _def:
                default = _def
                if "list" in property.type:
                    default = " = []"
                    # prop_name = " or []"
                elif "dict" in property.type:
                    default = " = {}"
                    # prop_name = " or {}"
                elif property.type in ors:
                    default = f" = {ors[property.type]}"

            type = self.datas.complex_types.get(property.type, property.type)
            annotations += f"{property.name}: {type}{default}, "

            consts += f"        self.{property.name} = {property.name}{prop_name}\n"

        p = f"from .model import *\n\nclass {self.name}(Model):\n    def __init__(self, models: '{self.plural_name}', *, {annotations}**kwargs,) -> None:\n\n        super().__init__(models, **kwargs)\n\n{consts}\n\nclass {self.plural_name}(Models):\n    model_class = {self.name}\n"

        p += f"\n\n{self.plural_name} = {self.plural_name}()"

        return p

    @property
    def filename(self):
        ns = ""
        for n in self.name:
            if n in string.ascii_uppercase:
                n = f"{underscore}{n.lower()}"
            ns += n
        ns = f"{ns.strip(underscore)}.py"
        return ns

    def add_property(self, line: str):
        self.properties.append(Property(line))

    def save(self, folder: str = ""):
        path = os.path.join(folder, self.filename)
        file = open(path, "w")
        file.write(self.py)
        file.close()


class Datas:
    def __init__(
        self,
        data_file: str,
        models_path: str = "",
        inherited_properties: dict[str, str] = {},
        complex_types: dict[str, str] = {},
        property_to_remove_on_db_dumb: list[str] = [],
    ):
        self.data_file = data_file
        self.models_path = models_path
        self.inherited_properties = inherited_properties
        self.complex_types = complex_types
        self.property_to_remove_on_db_dumb = property_to_remove_on_db_dumb

        self.datas: list[Data] = []

        lines = open(data_file).readlines()

        data: Data = None

        ih = list(inherited_properties.keys())

        for line in lines:
            if line.startswith(dash):
                if data:
                    self.datas.append(data)
                data = Data(self, line, ih)
            elif line.strip() and line.startswith(space):
                data.add_property(line)
            elif line.startswith("##"):
                break
        if data:
            self.datas.append(data)

    def save(self):
        property_to_remove_on_db_dumb = "["
        for ptrndd in self.property_to_remove_on_db_dumb:
            property_to_remove_on_db_dumb += f'"{ptrndd}", '
        property_to_remove_on_db_dumb = property_to_remove_on_db_dumb.strip(", ") + "]"

        annotations = ""
        consts = ""
        for (
            property,
            type,
        ) in self.inherited_properties.items():
            type = self.complex_types.get(type, type)
            annotations += f"{property}: {type}, "
            consts += f"        self.{property} = {property}\n"
        annotations = annotations.strip(", ")

        init_py = "\n".join(
            f"from .{os.path.splitext(data.filename)[0]} import {data.name}, {data.plural_name}"
            for data in self.datas
        )
        init_py += (
            "\n\n__all__ = ["
            + ", ".join(f'"{data.name}", "{data.plural_name}"' for data in self.datas)
            + "]"
        )
        open(f"{self.models_path}/__init__.py", "w").write(init_py)

        for data in self.datas:
            data.save(self.models_path)


data_file = "models.md"
models_path = "../src/models"

datas = Datas(
    data_file,
    models_path,
    inherited_properties=dict(
        id="str",
        created_timestamp="int",
    ),
    property_to_remove_on_db_dumb=["id", "created_timestamp"],
)

datas.save()

# p = open(r"C:\Users\USER\Desktop\Workspace\Fuitos\src\models\model.py").read()
# print(repr(p))

os.system("cd .. && black .")

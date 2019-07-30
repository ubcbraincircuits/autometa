from abc import ABC, abstractmethod


class Field(ABC):
    def __init__(self, name, description, required=False):
        self._name = None
        self._description = None
        self._required = False
        self.init()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name):
        self._name = new_name

    @name.deleter
    def name(self):
        self._name = None

    @property
    def description(self):
        return self._description

    @name.setter
    def description(self, new_description):
        self._description = new_description

    @name.deleter
    def description(self):
        self._description = None

    @property
    def required(self):
        return self._required

    @required.setter
    def required(self, new_setting):
        type_new_setting = type(new_setting)
        if type_new_setting is bool:
            self._required = new_setting
        else:
            raise TypeError(
                "Expected argument ``new_setting`` to be of type ``bool``,"
                "received ``{}`` instead.".format(type_new_setting)
            )

    @abstractmethod
    def init(self):
        pass

    @abstractmethod
    def to_json(self):
        pass

    @abstractmethod
    def from_json(self, json_dump):
        pass


class Dropdown(Field):
    def init(self):
        self._choices = set()
        self._current_selection = None
        return self

    @property
    def choices(self):
        return self._choices

    def add_choice(self, choice):
        self._choices.add(choice)

    def remove_choice(self, choice):
        self._choices.remove(choice)

    def clear_all_choices(self):
        self._choices.clear()

    @property
    def current_selection(self):
        return self._current_selection

    @current_selection.setter
    def current_selection(self, selection):
        self._current_selection = selection

    def to_json(self):
        name = self._name
        if (name == None) or (name == ""):
            raise ValueError("Attribute ``name`` not specified")
        description = self._description
        if (description == None) or (description == ""):
            raise ValueError("No description given")
        choices = list(self.choices)
        if len(choices) == 0:
            raise ValueError("There are no dropdown options for ``{}``".format(name))
        attributes = {
            "type": "Dropdown",
            "name": name,
            "description": description,
            "choices": choices,
            "required": self.required,
        }
        return json.dumps(attributes)

    def from_json(self, json_dump):
        loaded_dump = json.loads(json_dump)
        self._name = loaded_dump["name"]
        self._descripton = loaded_dump["description"]
        self._choices = set(loaded_dump["choices"])
        self._required = loaded_dump["required"]

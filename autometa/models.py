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


class ShortText(Field):
    # Template
    @property
    def data(self):
        return self._data

    def init(self):
        self._lower_limit = 0
        self._upper_limit = 256
        self._data = None
        self._exclude_sequence = set()
        return self

    @property
    def lower_limit(self):
        return self._lower_limit

    @lower_limit.setter
    def lower_limit(self, limit):
        if type(limit) is not int:
            raise TypeError(
                "Argument ``lower_limit`` must be of type ``int``, received ``{}`` instead.".format(
                    type(limit)
                )
            )
        if limit < 0:
            raise ValueError("Argument ``lower_limit`` must be greater than 0")
        if limit > 256:
            raise ValueError("Argument ``lower_limit`` must be smaller than 256")
        if limit > self.upper_limit:
            raise ValueError(
                "Argument ``lower_limit`` of value {} cannot be larger than ``upper_limit`` of value {}".format(
                    limit, self.upper_limit
                )
            )
        else:
            self._lower_limit = limit

    @lower_limit.deleter
    def lower_limit(self):
        self._lower_limit = 0

    @property
    def upper_limit(self):
        return self._upper_limit

    @upper_limit.setter
    def upper_limit(self, limit):
        if type(limit) is not int:
            raise TypeError(
                "Argument ``upper_limit`` must be of type ``int``, received ``{}`` instead.".format(
                    type(limit)
                )
            )
        if limit < 0:
            raise ValueError("Argument ``upper_limit`` must be greater than 0")
        if limit > 256:
            raise ValueError("Argument ``upper_limit`` must be smaller than 256")
        if limit < self.lower_limit:
            raise ValueError(
                "Argument ``upper_limit`` of value {} cannot be larger than ``lower_limit`` of value {}".format(
                    limit, self.lower_limit
                )
            )
        else:
            self._upper_limit = limit

    @upper_limit.deleter
    def upper_limit(self):
        self._upper_limit = 256

    def exclude_sequence(self, sequence):
        if type(sequence) is not str:
            raise TypeError(
                "Argument ``sequence`` must be of type ``str``, received ``{}`` instead.".format(
                    type(sequence)
                )
            )
        else:
            self._exclude_characters.add(sequence)

    def include_sequence(self, sequence):
        if type(sequence) is not str:
            raise TypeError(
                "Argument ``sequence`` must be of type ``str``, received ``{}`` instead.".format(
                    type(sequence)
                )
            )
        else:
            self._exclude_sequence.discard(sequence)

    @property
    def exclusion_list(self):
        return self._exclude_sequence

    # UI
    @data.setter
    def data(self, string):
        if type(string) is not str:
            raise TypeError("Argument ``string`` must be of type ``str``")
        length = len(string)
        if not (self.lower_limit <= length <= self.upper_limit):
            raise ValueError(
                "Argument ``string`` must be between {} and {} "
                "characters in length, received length of {} instead".format(
                    self.lower_limit, self.upper_limit, length
                )
            )
        for char in self.exclusion_list:
            if char in string:
                raise ValueError(
                    "Sequence `{}` not permitted in Argument ``string``".format(char)
                )
        else:
            self._data = string

    @data.deleter
    def data(self):
        self._data = None

    def to_json(self):
        name = self._name
        if (name == None) or (name == ""):
            raise ValueError("Attribute ``name`` not specified")
        description = self._description
        if (description == None) or (description == ""):
            raise ValueError("No description given")
        attributes = {
            "type": "ShortText",
            "name": name,
            "description": description,
            "lower_limit": self._lower_limit,
            "upper_limit": self._upper_limit,
            "required": self._required,
        }
        return json.dumps(attributes)

    def from_json(self):
        loaded_dump = json.loads(json_dump)
        self._name = loaded_dump["name"]
        self._descripton = loaded_dump["description"]
        self._lower_limit = loaded_dump["lower_limit"]
        self._upper_limit = loaded_dump["upper_limit"]
        self._required = loaded_dump["required"]


class CheckBoxes(Field):
    def init(self):
        self._min_choices = 0
        self._max_choices = 256
        self._choices = set()
        self._selections = set()

    @property
    def choices(self):
        return self._choices

    @property
    def min_choices(self):
        return self._min_choices

    @min_choices.setter
    def min_choices(self, limit):
        if type(limit) is not int:
            raise TypeError(
                "Argument ``min_choices`` must be of type ``int``, received ``{}`` instead.".format(
                    type(limit)
                )
            )
        if limit < 0:
            raise ValueError("Argument ``min_choices`` must be greater than 0")
        if limit > self.max_choices:
            raise ValueError(
                "Argument ``min_choices`` of value {} cannot be larger than ``max_choices`` of value {}".format(
                    limit, self.max_choices
                )
            )
        else:
            self._min_choices = limit

    @min_choices.deleter
    def min_choices(self):
        self._min_choices = 0

    @property
    def max_choices(self):
        return self._max_choices

    @max_choices.setter
    def max_choices(self, limit):
        if type(limit) is not int:
            raise TypeError(
                "Argument ``max_choices`` must be of type ``int``, received ``{}`` instead.".format(
                    type(limit)
                )
            )
        if limit < 0:
            raise ValueError("Argument ``max_choices`` must be greater than 0")
        if limit < self.min_choices:
            raise ValueError(
                "Argument ``max_choices`` of value {} cannot be larger than ``min_choices`` of value {}".format(
                    limit, self.min_choices
                )
            )
        else:
            self._max_choices = limit

    @max_choices.deleter
    def max_choices(self):
        self._max_choices = 256

    def add_choice(self, choice):
        self._choices.add(choice)

    def remove_choice(self, choice):
        self._choices.remove(choice)

    def clear_all_choices(self):
        self._choices.clear()

    # UI
    def add_selection(self, selection):
        self._selections.add(selection)

    def remove_selection(self, selection):
        self._selections.remove(selection)

    def clear_all_selections(self):
        self._selections.clear()


def DateTime(Field):
    def init(self):
        self._date = None
        self._start_date = None
        self._end_date = None

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, date):
        pass  # TODO

    @start_date.deleter
    def start_date(self):
        self._start_date = None

    @property
    def end_date(self):
        return self._start_date

    @end_date.setter
    def end_date(self, date):
        pass  # TODO

    @end_date.deleter
    def end_date(self):
        self._end_date = None

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

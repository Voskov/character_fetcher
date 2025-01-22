from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class BaseCharacter(ABC):
    def __init__(self, name, origin, species, additional_attribute):
        self.name = name
        self.origin = origin
        self.species = species
        self.additional_attribute = additional_attribute

    def __str__(self):
        return f"{self.name} is a {self.species} from {self.origin} with {self.additional_attribute} as an additional attribute"

    def to_dict(self):
        return {
            'name': self.name,
            'origin': self.origin,
            'species': self.species,
            'additional_attribute': self.additional_attribute
        }

    @classmethod
    @abstractmethod
    def from_raw_character(cls, raw_character: dict) -> 'BaseCharacter':
        pass

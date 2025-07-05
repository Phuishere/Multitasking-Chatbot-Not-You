import os
import json
from enum import Enum
from typing import Union
from .text_resources import MainText, SideBarText, Locale

# Get enums for texts
ENUMS = [MainText, SideBarText]
LANGUAGE_MAP = {
    "English": Locale.ENGLISH,
    "Tiếng Việt": Locale.VIETNAMESE,
}

class Translator:
    def __init__(self, locale: Locale, default_locale: Locale = Locale.ENGLISH, path: str = 'i18n'):
        # Set default path and locale
        self.path: str = path
        self.language: str = locale.value
        self.locale: Locale = locale

        self.set_locale(locale)

        # Set default locale (fallback)
        file_path = os.path.join(self.path, f'{default_locale.value}.json')
        with open(file_path, encoding='utf-8') as file:
            self.default_locale = default_locale
            self.default_translation = json.load(file)

    def set_locale(self, locale: Locale):
        self.language = locale.value
        self.locale = locale
        
        file_path = os.path.join(self.path, f'{locale.value}.json')
        with open(file_path, encoding='utf-8') as file:
            self.translation = json.load(file)
    
    def text(self, text: Enum):
        mes = self.translation.get(text.value)

        # Option to fallback to English when no translation found
        is_default_locale = self.locale != self.default_locale
        if mes is None and is_default_locale:
            raise AttributeError(f"No key '{text.value}' found in {self.default_locale.value} (default)")
        elif mes is None:
            mes = self.default_translation.get(text.value)
            if mes is None:
                raise AttributeError(f"No key '{text.value}' found in both {self.locale.value} and {self.default_locale.value} (default)")
        
        # Add format if there is one
        return mes

class TextResources:
    def __init__(self, translator: Translator, registered_enums: list[type[Enum]] = ENUMS):
        # Init translator
        self.translator = translator

        # Get enums (text values) - beware not to include identical keys in different classes
        self._registered_enums: list[type[Enum]] = []
        self._all_keys: set[str] = set()
        self.register_keys(registered_enums)

    def __getattr__(self, name: str):
        for re in self._registered_enums:
            if name in re.__members__:
                text_resource = re[name]
                return self.translator.text(text_resource)
        raise Exception(f"Translation key {name} is not available. Please register them first.")
    
    def __dir__(self):
        # Merge normal attrs with dynamic keys
        return list(super().__dir__()) + list(self._all_keys)
            
    def register_keys(self, enum_classes: Union[Enum, list[type[Enum]]]):
        # If enum_cls is an Enum, put into list
        try:
            if issubclass(enum_classes, Enum):
                enum_classes = [enum_classes]
        except TypeError:
            # When enum_classes is a list
            pass

        # Loop over the classes
        for enum_cls in enum_classes:
            # Check overlap
            overlap = self._all_keys.intersection(enum_cls.__members__.keys())
            if overlap:
                raise KeyError(f"Duplicate keys found: {overlap}")
            
            # If no overlap, register
            self._registered_enums.append(enum_cls)
            self._all_keys.update(enum_cls.__members__.keys())
    
if __name__ == "__main__":
    from .text_resources import MainText, SideBarText

    # Translator
    translator = Translator(locale = Locale.VIETNAMESE)
    print(translator.translation)
    print(translator.text(MainText.TITLE))
    
    # Text resource
    enums = [MainText]
    text_resources = TextResources(translator = translator, registered_enums = enums)
    text_resources.register_keys(SideBarText)
    print(text_resources.RAG)
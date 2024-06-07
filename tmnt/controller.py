from .dsl import TM
from .engines import Engine, Assignment

class TMNTController(object):

    """
    TMNTController is what starts a TMNT threat modeling session. Your
    initialized threat model will be empty by default, or you can specify a
    file path for your YAML configuration file
    (see `examples.parser_examples`).
    You can initialize with a set of Engines or you can add them
    later, by default it uses just the basic Assignment engine. Additionally,
    if you have any reference threat models that you want to compare against,
    you can add them with `references`.
    """

    def __init__(self, config_file: str = "", engines: Engine | list[Engine] = Assignment(), references: TM | list[TM] = None):
        pass

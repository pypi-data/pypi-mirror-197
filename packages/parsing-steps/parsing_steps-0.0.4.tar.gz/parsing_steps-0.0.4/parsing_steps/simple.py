from typing import Iterable


class SimpleParsingStep:
    """
    Simpliify class for parsing data step by step.
    The class represents one parsing step.

    input_data is required on initializing.
    To start parsing, call the "perform" method.

    "parse" method must be overrated on inherited classes.

    For multithreaded use, override the "perform_next_step" method.
    """

    next_step_class = None

    def __init__(self, input_data, inherited_data=None, **kwargs):
        """
        Sets the input parameters as the class fields.
        "input_data" parameter is required
        """
        for name, value in kwargs.items():
            setattr(self, name, value)
        self.input_data = input_data
        self.inherited_data = inherited_data

    def get_next_step_class(self, next_step_data):
        """
        Returns "next_step" class
        """
        return self.next_step_class

    def parse(self, input_data) -> Iterable:
        """
        Processes input_data to produce output_data. output_data is iterable
        object (list, set, or generator) of parsing steps instances.
        output_data must be returned.
        """
        raise NotImplementedError

    def perform_next_step(self, next_step):
        """
        The method that starts the next parsing step.
        The code is run by the calling "perform" method.

        If you want to run parsing in multi-threaded mode or through tasks
        (celery, for example) - override this method.
        The "next_step.perform(*args, **kwargs)" method must be run
        on a new thread, process or task in this case.
        """
        if next_step is None:
            return None

        if next_step.inherited_data is None:
            next_step.inherited_data = self.inherited_data

        return next_step.perform()

    def perform(self):
        """
        Performs data parsing.
        """
        self.output_data = self.parse(self.input_data)

        assert hasattr(self.output_data, "__iter__") or \
            self.output_data is None, \
            "Wrong data type of output data. " \
            "Must be either an iterable object or None."

        if self.output_data is None:
            return

        for num, next_step in enumerate(self.output_data, start=1):
            if next_step and self.perform_next_step:
                self.perform_next_step(next_step=next_step)

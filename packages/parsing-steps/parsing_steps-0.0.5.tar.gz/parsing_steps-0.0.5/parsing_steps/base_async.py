import asyncio


class BaseAsyncParsingStep:
    """
    Base class for parsing data step by step asynchronously.
    The class represents one parsing step.

    input_data is required on initializing.
    To start parsing, call the "perform" method.

    "parse" method must be overrated on inherited classes.

    For multithreaded use, override the "perform_next_step" method.
    """

    next_step_class = None
    inherited_data = None

    def __init__(
            self, input_data, task_coros=None, inherited_data=None, **kwargs):
        """
        Sets the input parameters as the class fields.
        "input_data" parameter is required
        """
        for name, value in kwargs.items():
            setattr(self, name, value)
        self.input_data = input_data
        self.inherited_data = inherited_data

        if task_coros is None:
            task_coros = set()
        self.task_coros = task_coros

    async def get_next_step_class(self, next_step_data, *args, **kwargs):
        """
        Returns "next_step" class
        """
        return self.next_step_class

    async def parse(self, input_data, *args, **kwargs):
        """
        Processes input_data to produce output_data.
        output_data must be returned.
        """
        raise NotImplementedError

    async def perform_next_step(self, next_step_class, next_step_data,
                                *next_step_args, **next_step_kwargs):
        """
        The method that starts the next parsing step.
        The code is run by the calling "perform" method.

        If you want to run parsing in multi-threaded mode or through tasks
        (celery, for example) - override this method.
        The "next_step.perform(*args, **kwargs)" method must be run
        on a new thread, process or task in this case.
        """
        if next_step_class is None:
            return None
        next_step = next_step_class(
            input_data=next_step_data,
            task_coros=self.task_coros,
            inherited_data=self.inherited_data,
            *next_step_args, **next_step_kwargs)
        return await next_step.perform()

    async def perform(self):
        """
        Performs data parsing.
        """
        self.output_data = await self.parse(self.input_data)

        assert hasattr(self.output_data, "__iter__") or \
            self.output_data is None, \
            "Wrong data type of output data. " \
            "Must be either an iterable object or None."

        if self.output_data is None:
            return

        for num, next_step_data in enumerate(self.output_data, start=1):
            next_step_class = await self.get_next_step_class(next_step_data)
            if next_step_class and self.perform_next_step:
                coro = self.perform_next_step(next_step_class=next_step_class,
                                              next_step_data=next_step_data,
                                              num_in_list=num)
                self.task_coros.add(asyncio.create_task(coro=coro))

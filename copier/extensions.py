"""Jinja2 extension to add to the Jinja2 environment."""

from jinja2 import nodes
from jinja2.environment import Environment
from jinja2.exceptions import UndefinedError
from jinja2.ext import Extension


class YieldExtension(Extension):
    """`Jinja2 extension for the `yield` tag.

    If `yield` tag is used in a template, it sets the `yield_context` attribute to the
    jinja environment. `yield_context` is a dictionary with the single variable name as
    the key and the looped variable as the value.

    Note that this extension just sets the `yield_context` attribute but renders template
    as usual. It is caller's responsibility to use the `yield_context` attribute in the
    template to generate the desired output.

    Example:
        template: "{% yield single_var from looped_var %}"
        context: {"looped_var": [1, 2, 3], "single_var": "item"}

        then,
        >>> from jinja2.environment import Environment
        >>> from copier.extensions import YieldExtension
        >>> env = Environment(extensions=[YieldExtension])
        >>> template = env.from_string("{% yield single_var from looped_var %}{{ single_var }}{% endyield %}")
        >>> template.render({"looped_var": [1, 2, 3])
        ''
        >>> env.yield_context
        {'single_var': [1, 2, 3]}
    """

    tags = {"yield"}

    def __init__(self, environment: Environment):
        super().__init__(environment)

        environment.extend(yield_context=dict())

    def parse(self, parser):
        """Parse the `yield` tag."""
        lineno = next(parser.stream).lineno

        single_var = parser.parse_expression()
        parser.stream.expect("name:from")
        looped_var = parser.parse_expression()
        body = parser.parse_statements(["name:endyield"], drop_needle=True)

        return nodes.CallBlock(
            self.call_method(
                "_yield_support",
                [looped_var, nodes.Const(single_var.name)],
            ),
            [],
            [],
            body,
            lineno=lineno,
        )

    def _yield_support(self, looped_var, single_var_name, caller):
        """Support function for the yield tag.

        Sets the yield context in the environment with the given
        looped variable and single variable name, then calls the provided caller
        function. If an UndefinedError is raised, it returns an empty string.

        """
        self.environment.yield_context = {single_var_name: looped_var}

        try:
            res = caller()

        # Can be raised if `dict.attr` is used before context is set
        except UndefinedError:
            res = ""

        return res

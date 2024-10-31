"""拡張機能を定義するモジュール."""

from jinja2 import nodes
from jinja2.environment import Environment
from jinja2.ext import Extension


class YieldExtension(Extension):
    """Yield タグを定義するクラス."""

    tags = {"yield"}

    def __init__(self, environment: Environment):
        """コンストラクタ."""
        super().__init__(environment)

        environment.extend(yield_context=dict())

    def parse(self, parser):
        """パーサー."""
        lineno = next(parser.stream).lineno
        # 変数名を取得
        single_var = parser.parse_expression()

        # 'from' キーワードを取得
        parser.stream.expect("name:from")

        # リストを取得
        looped_var = parser.parse_expression()

        # タグのボディを取得
        body = parser.parse_statements(["name:endyield"], drop_needle=True)

        return nodes.CallBlock(
            self.call_method(
                "_yield_support",
                [looped_var, nodes.Const(single_var.name)],
            ),
            [],
            [],
            body,
        )

    def _yield_support(self, looped_var, single_var_name, caller):
        self.environment.yield_context = {single_var_name: looped_var}

        return caller()

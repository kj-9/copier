"""拡張機能を定義するモジュール."""

from jinja2 import nodes
from jinja2.ext import Extension


class YieldExtension(Extension):
    """Yield タグを定義するクラス."""

    tags = {"yield"}

    def __init__(self, environment):
        """コンストラクタ."""
        super().__init__(environment)

        environment.extend(yield_state=None)

    def parse(self, parser):
        """パーサー."""
        lineno = next(parser.stream).lineno

        # 変数名を取得
        single_var = parser.parse_expression()

        # 'from' キーワードを取得
        parser.stream.expect("name:from")

        # リストを取得
        # looped_var = parser.parse_expression()

        # タグのボディを取得
        body = parser.parse_statements(["name:endyield"], drop_needle=True)

        node = nodes.OverlayScope(lineno=lineno)
        node.body = list(body)
        node.context = self.call_method(
            "_yield_support", [nodes.Const(single_var.name)]
        )
        return node

    def _yield_support(self, single_var):
        return {single_var: 1}
        # result = []
        # for item in looped_var:
        #    result.append(caller(**{single_var.name: item}))
        # return "".join(result)

        # if self.environment.yield_state:
        #     context[single_var.name] = self.environment.yield_state.pop(0)

        # if not looped_var:
        #     raise ValueError("looped_var is empty")

        # if not self.environment.yield_state:
        #     self.environment.yield_state = looped_var
        #     return ""
        # else:
        #     res = caller(single_var=self.environment.yield_state.pop(0))

        # return res

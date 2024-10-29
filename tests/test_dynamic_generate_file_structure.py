import warnings

import copier
from tests.helpers import build_file_tree


def test_render_items(tmp_path_factory):
    src, dst = map(tmp_path_factory.mktemp, ("src", "dst"))
    build_file_tree(
        {
            src / "copier.yml": """
                _items: "test"
            """,
            src
            / "{% yield single_var from looped_var %}{{ single_var }}{{hello}}.txt{% endyield %}.jinja": "Hello {{hello}}",
        }
    )
    # No warnings, because template is explicit
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        copier.run_copy(
            str(src),
            dst,
            data={
                "looped_var": ["one", "two", "three"],
                "hello": "world",
            },
            defaults=True,
            overwrite=True,
        )

        one_rendered = (dst / "world.txt").read_text()
        one_expected = "Hello world"
        assert one_rendered == one_expected

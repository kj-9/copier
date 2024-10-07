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
            / "{% yield single_var from looped_var %}{{ single_var }}{{hello}}.txt{% endyield %}{{looped_var}}hey": "This is {{ _item }}. Hello {{hello}}",
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

        one_rendered = (dst / "one.txt").read_text()
        one_expected = "This is one. Hello world"
        assert one_rendered == one_expected

        one_rendered = (dst / "two.txt").read_text()
        one_expected = "This is two. Hello world"
        assert one_rendered == one_expected

        one_rendered = (dst / "three.txt").read_text()
        one_expected = "This is three. Hello world"
        assert one_rendered == one_expected

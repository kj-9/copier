import warnings

import copier
from tests.helpers import build_file_tree


def test_yield_files(tmp_path_factory):
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

        for i in ["one", "two", "three"]:
            one_rendered = (dst / f"{i}world.txt").read_text()
            one_expected = "Hello world"
            assert one_rendered == one_expected


def test_yield_dirs(tmp_path_factory):
    src, dst = map(tmp_path_factory.mktemp, ("src", "dst"))
    build_file_tree(
        {
            src / "copier.yml": """
                _items: "test"
            """,
            src
            / "{% yield single_var from looped_var %}dir-{{ single_var }}{% endyield %}"
            / "file.txt.jinja": "Hello {{hello}}",
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

        for i in ["one", "two", "three"]:
            one_rendered = (dst / f"dir-{i}/file.txt").read_text()
            one_expected = "Hello world"
            assert one_rendered == one_expected


# def test_folder_loop(tmp_path_factory):
#     src, dst = map(tmp_path_factory.mktemp, ("src", "dst"))
#     build_file_tree(
#         {
#             src / "copier.yml": """
#                 _items: "test"
#             """,
#             src
#             / "folder_loop"
#             / "{% yield item from strings %}{{ item }}{% endyield %}"
#             / "{{ item }}.txt.jinja": "Hello {{ item }}",
#         }
#     )
#     with warnings.catch_warnings():
#         warnings.simplefilter("error")
#         copier.run_copy(
#             str(src),
#             dst,
#             data={
#                 "strings": ["a", "b", "c"],
#             },
#             defaults=True,
#             overwrite=True,
#         )

#         for i in ["a", "b", "c"]:
#             rendered = (dst / f"folder_loop/{i}/{i}.txt").read_text()
#             expected = f"Hello {i}"
#             assert rendered == expected


# def test_nested_folder_loop(tmp_path_factory):
#     src, dst = map(tmp_path_factory.mktemp, ("src", "dst"))
#     build_file_tree(
#         {
#             src / "copier.yml": """
#                 _items: "test"
#             """,
#             src
#             / "nested_folder_loop"
#             / "{% yield string_item from strings %}{{ string_item }}{% endyield %}"
#             / "{% yield integer_item from integers %}{{ integer_item }}{% endyield %}"
#             / "{{ string_item }}_{{ integer_item }}.txt.jinja": "Hello {{ string_item }} {{ integer_item }}",
#         }
#     )
#     with warnings.catch_warnings():
#         warnings.simplefilter("error")
#         copier.run_copy(
#             str(src),
#             dst,
#             data={
#                 "strings": ["a", "b"],
#                 "integers": [1, 2, 3],
#             },
#             defaults=True,
#             overwrite=True,
#         )

#         for s in ["a", "b"]:
#             for i in [1, 2, 3]:
#                 rendered = (dst / f"nested_folder_loop/{s}/{i}/{s}_{i}.txt").read_text()
#                 expected = f"Hello {s} {i}"
#                 assert rendered == expected


# def test_file_loop(tmp_path_factory):
#     src, dst = map(tmp_path_factory.mktemp, ("src", "dst"))
#     build_file_tree(
#         {
#             src / "copier.yml": """
#                 _items: "test"
#             """,
#             src
#             / "file_loop"
#             / "{% yield string_item from strings %}{{ string_item }}{% endyield %}.txt.jinja": "Hello {{ string_item }}",
#         }
#     )
#     with warnings.catch_warnings():
#         warnings.simplefilter("error")
#         copier.run_copy(
#             str(src),
#             dst,
#             data={
#                 "strings": ["a", "b", "c"],
#             },
#             defaults=True,
#             overwrite=True,
#         )

#         for i in ["a", "b", "c"]:
#             rendered = (dst / f"file_loop/{i}.txt").read_text()
#             expected = f"Hello {i}"
#             assert rendered == expected


# def test_folder_loop_dict_items(tmp_path_factory):
#     src, dst = map(tmp_path_factory.mktemp, ("src", "dst"))
#     build_file_tree(
#         {
#             src / "copier.yml": """
#                 _items: "test"
#             """,
#             src
#             / "folder_loop_dict_items"
#             / "{% yield dict_item from dicts %}{{ dict_item.folder_name }}{% endyield %}"
#             / "{{ dict_item.file_name }}.txt.jinja": "Hello {{ dict_item.file_name }}",
#         }
#     )
#     with warnings.catch_warnings():
#         warnings.simplefilter("error")
#         copier.run_copy(
#             str(src),
#             dst,
#             data={
#                 "dicts": [
#                     {"folder_name": "folder_a", "file_name": "file_a"},
#                     {"folder_name": "folder_b", "file_name": "file_b"},
#                     {"folder_name": "folder_c", "file_name": "file_c"},
#                 ],
#             },
#             defaults=True,
#             overwrite=True,
#         )

#         for d in [
#             {"folder_name": "folder_a", "file_name": "file_a"},
#             {"folder_name": "folder_b", "file_name": "file_b"},
#             {"folder_name": "folder_c", "file_name": "file_c"},
#         ]:
#             rendered = (
#                 dst / f"folder_loop_dict_items/{d['folder_name']}/{d['file_name']}.txt"
#             ).read_text()
#             expected = f"Hello {d['file_name']}"
#             assert rendered == expected


def test_file_contents_loop(tmp_path_factory):
    src, dst = map(tmp_path_factory.mktemp, ("src", "dst"))
    build_file_tree(
        {
            src / "copier.yml": """
                _items: "test"
            """,
            src / "file_contents_loop" / "my_file.txt.jinja": """
                {% for string_item in strings %}
                Hello {{ string_item }}
                {% endfor %}
            """,
        }
    )
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        copier.run_copy(
            str(src),
            dst,
            data={
                "strings": ["a", "b", "c"],
            },
            defaults=True,
            overwrite=True,
        )

        rendered = (dst / "file_contents_loop/my_file.txt").read_text().strip()
        expected = "Hello a\n\nHello b\n\nHello c"
        assert rendered == expected

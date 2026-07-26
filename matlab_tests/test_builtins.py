from translate.builtins import translate_builtin


def test_builtin_sort_mappings():
    assert translate_builtin("sort") == "np.sort"
    assert translate_builtin("sortrows") == "np.lexsort"

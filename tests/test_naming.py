from biji_archive.naming import collection_name, safe_name

def test_collection_name_decodes_follow_name():
    assert collection_name('https://www.biji.com/subject/x/DEFAULT?followName=Ai%E6%B1%9F%E6%B9%96') == 'Ai江湖'

def test_safe_name_removes_reserved_characters():
    assert safe_name('a/b:c') == 'a_b_c'

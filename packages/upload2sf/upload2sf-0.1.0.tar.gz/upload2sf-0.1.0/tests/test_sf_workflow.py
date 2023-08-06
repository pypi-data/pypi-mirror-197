from upload2sf.sf_utils import  clean_token, clean_object_triple

def test_clean_token():
    assert "DROP TABLE USERS" not in clean_token("INSERT INTO USERS FOO; DROP TABLE USERS;").upper()

def test_remove_bad_chars_from_namespace():
    namespace = ("DROP TABLE USERS", "foo", "bar")
    namespace = clean_object_triple(namespace)
    assert "DROP TABLE USERS" not in namespace[0].upper()


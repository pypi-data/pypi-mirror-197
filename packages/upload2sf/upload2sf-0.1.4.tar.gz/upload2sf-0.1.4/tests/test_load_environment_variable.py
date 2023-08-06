from upload2sf.load_environment_variables import set_env_variables_if_missing, verify_env_variables_exist


def test_set_env_variables_if_missing():
    set_env_variables_if_missing('upload2sf', 'dev')
    assert verify_env_variables_exist()
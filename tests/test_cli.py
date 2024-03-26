def test_version():
    from excel2xx import main

    argv = ["--version"]
    code = main.main_docopt(argv)
    assert 0 == code
    pass

=====
Usage
=====

To use list_files in a project::

    from list_files import list_files
    # defaults to current dir
    list_files()
    # specific dir
    list_files("path/to/dir")
    # find files with numbers
    list_files(pattern='[0-9]+')

__version__ = '0.0.2_post_2'

print('Entered test_project_python.__init__ :)')

def function_name():
    print('Ran test_project_python.__init__.function_name')
    return True


if __name__ == '__main__':
    print('__name__ == "__main__" is True for test_project_python.__init__')
    function_name()

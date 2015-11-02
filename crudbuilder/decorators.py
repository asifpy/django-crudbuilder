
class DecorateCrudBuilder(object):
    def __init__(self):
        self.func_map = {}

    def register(self, name):
        def func_wrapper(func):
            print self.self.__class__.__name__
            self.func_map[name] = func
            return func
        return func_wrapper

    def call_registered(self, name=None):
        func = self.func_map.get(name, None)
        if func is None:
            raise Exception("No function registered against - " + str(name))
        return func()

app = DecorateCrudBuilder()

#
# import json
#
# class A: pass
#
# a = A()
# a.jos = 'test'
#
# print(json.dumps([1,2,{'a':a}]))

class Test:
    def __call__(self, key=None):
        print(key)

t = Test()
t(5)
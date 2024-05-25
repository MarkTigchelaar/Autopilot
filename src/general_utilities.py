import sys, functools


# Private wrapper to make methods in classes private (cheks at runtime)
def private(member):
    @functools.wraps(member)
    def wrapper(*function_args):
      myself = member.__name__
      caller = sys._getframe(1).f_code.co_name
      print(f"function args: {function_args}")
      caller_name = None
      if len(function_args) > 0:
        caller_name = function_args[0]
      if (not caller in dir(caller_name) and not caller is myself):
         raise Exception("%s called by %s is private"%(myself,caller))
      return member(*function_args)
    return wrapper



# Exxample
# class Test:
#   def __init__(self):
#     self.field = "Hi"
    
  
#   def pub_method(self):
#     self.private_method()
    
    
#   @private
#   def private_method(self):
#     print(self.field)


# t = Test()
# t.pub_method()
#t.private_method()
# MalPython
#
# Intercept the HTTP requests by requests module
# Example of monkeypatching

import sys 
import importlib
import importlib.abc
import importlib.machinery

class MalPyHook(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    TARGET = "requests"

    def find_spec(self, fullname, path, target=None):
        if fullname == self.TARGET:
            spec = importlib.machinery.PathFinder.find_spec(fullname, path)            
            if spec and spec.loader:
                spec.loader = MalPyLoader(spec.loader)
                return spec
        return None     # fallback to default loaders


class MalPyLoader(importlib.abc.Loader):
    def __init__(self, original_loader):
        self.original_loader = original_loader

    def create_module(self, spec):
        return self.original_loader.create_module(spec)

    def exec_module(self, module):
        # load real module using original loader
        self.original_loader.exec_module(module)

        # injecting backdoor into requests module
        def malpy_get(*args, **kwargs):
            # requests.get(url)
            print(f"[!] exfiltrating GET request to {args[0]}")
            return module._original_get(*args, **kwargs)

        if hasattr(module, "get"):
            module._original_get = module.get 
            module.get = malpy_get

sys.meta_path.insert(0, MalPyHook())

# Test
#
# import intercept
# import requests
# response = requests.get("http://example.com")
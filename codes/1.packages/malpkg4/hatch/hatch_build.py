from hatchling.builders.hooks.plugin.interface import BuildHookInterface

# three entry points available
class CustomBuildHook(BuildHookInterface):
    # before cleaning if the "-c" / "-clean" flag passed to the build
    def clean(self, versions):
        print("[!] hook at clean")

    # before each build
    def initialize(self, version, build_data):
        print("[!] hook before each build")

    # after each build
    def finalize(self, version, build_data, artifact_path):
        print("[!] hook after each build")
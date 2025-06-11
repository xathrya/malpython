# add target for either wheel or sdist
def pdm_build_hook_enabled(context):
    return context.target == "wheel"

# hook run at cleaning
def pdm_build_clean(context):
    print("[!] hook at clean")

# hook run before each build
def pdm_build_initialize(context):
    print("[!] hook before each build")

# hook run after each build
def pdm_build_finalize(context, artifact):
    print("[!] hook after each build")
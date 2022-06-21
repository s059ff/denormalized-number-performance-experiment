import platform

assert platform.system() == "Linux"

if platform.machine() == "x86_64":
    from fenv_x86_64 import set_ftz, unset_ftz

elif platform.machine() == "aarch64":
    from fenv_aarch64 import set_ftz, unset_ftz

else:
    raise RuntimeError()

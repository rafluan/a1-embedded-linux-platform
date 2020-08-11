A1_VALID_MACHINES = []

def __set_defaults_a1_yocto():

    import os
    import sys

    # Append to valid machines
    global A1_VALID_MACHINES
    A1_VALID_MACHINES += [
        'imx6ull-a1-r1',
    ]

    local_conf_exists = os.path.isfile(os.path.join(build_dir,
                                                    'conf',
                                                    'local.conf'))

    def required_var_error(varname, valid_vals):
        sys.stderr.write("ERROR: You must set '%s' before setting up the environment.\n" %
                         (varname,))
        sys.stderr.write("       Set MACHINE variable with one of the possible values.\n"
                         "       Possible values are: %s\n\n"
                         "       Ex: MACHINE=imx6ull-a1-basic source setup-environment build\n"
                         % valid_vals)
        sys.exit(1)

    def maybe_set_default(varname, valid_vals):
        try:
            val = os.environ[varname]
        except KeyError:
            val = None

        if val:
            if val in valid_vals:
                set_default(varname, val)
            else:
                required_var_error(varname, valid_vals)
        elif not local_conf_exists:
            required_var_error(varname, valid_vals)

    maybe_set_default('MACHINE', A1_VALID_MACHINES)
    set_default('DISTRO', 'a1el')

def __after_init_a1_yocto():
    PLATFORM_ROOT_DIR = os.environ['PLATFORM_ROOT_DIR']

    append_layers([ os.path.join(PLATFORM_ROOT_DIR, 'sources', p) for p in
                    [
                        'meta-a1',
                        'meta-freescale',
                    ]])

    # FSL EULA
    eulas.accept['meta-freescale/EULA'] = 'ACCEPT_FSL_EULA = "1"'

run_set_defaults(__set_defaults_a1_yocto)
run_after_init(__after_init_a1_yocto)

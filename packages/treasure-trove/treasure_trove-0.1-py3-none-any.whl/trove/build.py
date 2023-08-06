'''Tools for building the pipeline.'''

import ast
import copy
import os
import trove.config_parser as config_parser

########################################################################

def link_params_to_config(
        config_fp,
        script_id = None,
        variation = None,
        global_variation = None,
        create_data_dirs = True,
        **pm
    ):
    '''Link the values of a set of existing params to those in a config,
    overwriting the existing values if the config has that value.

    Args:
        config_fp (str):
            Location of the config file to use for updating the parameters.

        script_id (str):
            Specific script to select.
            If None, defaults to the next in the trove.

        variation (str):
            Specific variation to select from the config.
            If None, defaults to the next in the trove.

        global_variation (str):
            Specific global variation to select from the config.
            If None, defaults to the next in the trove.

        create_data_dirs (bool):
            If True, create any data dirs that don't exist.

    Kwargs:
        All parameters to update.

    Returns:
        pm (dict), [pm_new (dict)]
            Dictionaries containing new/updated parameters.
    '''

    # Read the config
    tcp = config_parser.ConfigParser( config_fp )

    # Get the next variation
    script_id, variation, global_variation = tcp.get_next_variation_args(
        script_id,
        variation,
        global_variation,
        when_done = 'return_last',
    )

    # Defaults
    pm_new = {}
    for option in tcp.defaults():
        pm_new[option] = tcp.get( 'DEFAULT', option )

    # Global variation options
    if global_variation != '':
        for option in tcp.options( global_variation, exclude_defaults=True ):
            pm_new[option] = tcp.get( global_variation, option )

    # Variation options
    if variation != 'DEFAULT':
        for option in tcp.options( variation, exclude_defaults=True ):
            pm_new[option] = tcp.get( variation, option )

    # Interpret strings
    for key, item in pm_new.items():
        if item is not None:
            # We'll try to evaluate the argument, but fallback to the str rep
            try:
                pm_new[key] = ast.literal_eval( item )
            except ( SyntaxError, ValueError ) as e:
                pass

    # Store variation and important info
    pm_new['config_fp'] = config_fp
    pm_new['config_parser'] = tcp
    pm_new['script_id'] = script_id
    pm_new['variation'] = variation
    pm_new['global_variation'] = global_variation

    # Store data_dirs
    # Note that the data dir can change for different scripts
    pm_new['data_dirs'] = {}
    for script_id_i in tcp.scripts:
        pm_new['data_dirs'][script_id_i] = tcp.get_data_dir(
            script_id_i,
            variation,
            global_variation,
            create = create_data_dirs,
        )
    pm_new['data_dir'] = pm_new['data_dirs'][script_id]
    pm_new['base_data_dir'] = tcp.get_data_dir(
        script_id,
        variation,
        '',
        create = create_data_dirs,
    )

    # Update and return
    pm.update( pm_new )
    return pm

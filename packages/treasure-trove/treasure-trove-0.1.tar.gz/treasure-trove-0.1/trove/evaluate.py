'''Tools for evaluating pipeline progress.'''
import argparse
import glob
import os
import pathlib
import sys

import trove.config_parser as config_parser

########################################################################

def evaluate( config_fp, verbose=True ):
    '''Look for data files that mark a part of the trove process as complete
    and mark them as done.

    Args:
        config_fp (str):
            Config to use for the conversion process. Must contain a section
            titled "DATA PRODUCTS".
    '''

    # As a precaution, convert to absolute path
    config_fp = os.path.abspath( config_fp )

    # Load the config
    tcp = config_parser.ConfigParser( config_fp )

    if verbose:
        print( 'Determining progress. Found data products for the following:' )

    # Loop and look for existing files
    n_found = 0
    for filepath in tcp.manager.data_files:
        # Split into parameters
        data_dir, troveflag = os.path.split( filepath )
        script_id = '.'.join( troveflag.split( '.' )[:-1] )

        # Skip files we're not given an option for
        if not tcp.has_option( 'DATA PRODUCTS', script_id ):
            continue

        # Find what to search for
        filename = tcp.get( 'DATA PRODUCTS', script_id )
        filepath = os.path.join( data_dir, filename )

        # Check if it exists
        if len( glob.glob( filepath ) ) > 0:
            if verbose: print( '    {} | {}'.format( script_id, data_dir ) )
            troveflag_fp = os.path.join( data_dir, script_id + '.troveflag' )
            pathlib.Path( troveflag_fp ).touch()
            n_found += 1

    print( '{:.3g}% of data products found'.format(
        100. * n_found / len( tcp.manager.data_files )
    ) )

########################################################################

if __name__ == '__main__':

    # Parse args
    parser = argparse.ArgumentParser(
        description='Evaluate pipeline progress.'
    )
    parser.add_argument(
        'config_fp',
        type = str,
        help = 'Location of your config file used to guide evaluation.',
    )
    parser.add_argument(
        '--quiet',
        help = 'Quiet down the output.',
        action = 'store_true',
    )
    args = parser.parse_args()

    # Run
    evaluate(
        args.config_fp,
        not args.quiet,
    )


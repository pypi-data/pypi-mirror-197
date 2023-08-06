'''Tools for cleaning the pipeline.'''
import argparse
import glob
import os
import shutil
import sys

import trove.config_parser as config_parser

########################################################################

def collate( config_fp, dir_key, output_dir, verbose=True, skip_suspect_folders=True ):
    '''Function for collecting global variation outputs into a single folder
    for easy side-by-side comparison

    Args:
        config_fp (str):
            Config to base the cleaning on.

        dir_key (str):
            The parameter stored in the config that describes where the output
            is stored.

        output_dir (str):
            Where to store the collated directory.

        verbose (bool):
            If True, print more information.

        skip_suspect_folders (bool):
            If True, skip folders that are likely to cause errors, e.g.
            global variation folders in the default folder.
    '''

    # As a precaution, convert to absolute path
    config_fp = os.path.abspath( config_fp )

    # Load the config
    tcp = config_parser.ConfigParser( config_fp )

    if verbose: print( 'Collating...' )

    if not os.path.exists( output_dir ):
        print( 'Output directory does not exist, creating {}'.format( output_dir ) )
        os.makedirs( output_dir, exist_ok=True )

    for i, gv in enumerate( tcp.execute['global_variations'] ):

        if gv == '':
            gv = 'DEFAULT'

        # Get the dir and output dir
        dir_i = tcp.get( gv, dir_key )
        dir_i = os.path.abspath( dir_i )
        output_dir = os.path.abspath( output_dir )

        print( '    Copying {}...'.format( gv ) )

        # Walk through the dir and copy
        for (dirpath, dirnames, filenames) in os.walk( dir_i ):

            # Create the appropriate output dir
            if dirpath != dir_i:
                output_dir_i = dirpath.replace( dir_i, output_dir )
            else:
                output_dir_i = output_dir

            # Skip any folders that might cause recursion errors
            if skip_suspect_folders and ( gv == 'DEFAULT' ):
                    if tcp.global_variations_dirname in dirpath:
                        continue

            for j, src_file in enumerate( filenames ):

                # Setup destination and source filepaths
                if gv != 'DEFAULT':
                    base, tail = os.path.splitext( src_file )
                    dst_file = base + '.' + gv + tail
                else:
                    dst_file = src_file
                dst_fp = os.path.join( output_dir_i, dst_file )
                src_fp = os.path.join( dirpath, src_file )

                # Ensure destination folder exists
                os.makedirs( os.path.dirname( dst_fp ), exist_ok=True )

                # Copy
                shutil.copyfile( src_fp, dst_fp )

########################################################################

if __name__ == '__main__':

    # Parse args
    parser = argparse.ArgumentParser(
        description='Collate output from global variations into a single folder.'
    )
    parser.add_argument(
        'config_fp',
        type = str,
        help = 'Location of your config file used to guide collating.',
    )
    parser.add_argument(
        '--dir_key',
        type = str,
        help = 'Config key that gives the output directory to collate.',
    )
    parser.add_argument(
        '--output_dir',
        type = str,
        help = 'Location to store the output.',
    )
    args = parser.parse_args()

    # Run
    collate(
        args.config_fp,
        args.dir_key,
        args.output_dir,
    )


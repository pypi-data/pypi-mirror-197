'''Tools for evaluating pipeline progress.'''
import argparse
import os
import subprocess
import warnings

import trove.config_parser as config_parser

########################################################################

def archive( config_fp, verbose=True, use_shell=True ):
    '''Archive everything in the data directories.

    Args:
        config_fp (str):
            Config to use for the conversion process. Must contain a section
            titled "DATA PRODUCTS".
    '''

    # As a precaution, convert to absolute path
    config_fp = os.path.abspath( config_fp )

    # Load the config
    tcp = config_parser.ConfigParser( config_fp )

    # Set up archive dir.
    if tcp.has_option( 'DEFAULT', 'archive_dir' ):
        archive_dir = tcp.get( 'DEFAULT', 'archive_dir' )
        if not use_shell:
            archive_dir = os.path.abspath( archive_dir )
    else:
        raise KeyError( 'No "archive_dir" specified in config file. Cannot archive.' )
    if not os.path.exists( archive_dir ):
        warnings.warn( 'Archive directory {} may not exist.' )
        if not use_shell:
            os.makedirs( archive_dir, exist_ok=True )

    if verbose:
        print( 'Archiving data products:' )

    # Loop through and archive
    root_data_dir = tcp.get( 'DEFAULT', 'root_data_dir' )
    starting_dir = os.getcwd()
    for variation in tcp.variations:
        archive_filename = '{}.tar'.format( variation )

        # Move to the appropriate location
        data_dir = os.path.join( root_data_dir, variation )
        print( '\nArchiving files in {}'.format( data_dir ) )
        os.chdir( data_dir )

        if use_shell:
            # Tar
            os.system(
                'tar -cvf {} *'.format( archive_filename )
            )
            # Copy
            os.system(
                'rsync --progress {} {}/'.format(
                    archive_filename,
                    archive_dir,
                )
            )
        else:
            # Tar
            subprocess.run([
                'tar',
                '-cvf',
                archive_filename,
                '*',
            ])
            # Copy. Use rsync to allow cross-filesystem
            subprocess.run([
                'rsync',
                '--progress',
                archive_filename,
                archive_dir,
            ])

        # Change back
        os.chdir( starting_dir )

########################################################################

if __name__ == '__main__':

    # Parse args
    parser = argparse.ArgumentParser(
        description='Archive/backup results.'
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
    parser.add_argument(
        '--use_subprocess',
        help = 'Use subprocess.run instead of os.system.',
        action = 'store_true',
    )
    args = parser.parse_args()

    # Run
    archive(
        args.config_fp,
        not args.quiet,
        not args.use_subprocess,
    )


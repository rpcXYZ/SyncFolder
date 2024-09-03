#!/usr/bin/env python
import os
import shutil
import argparse
import logging
import time
import hashlib


def setup_output(log_file):
    logger = logging.getLogger('syncFolders')

    logging.addLevelName(logging.WARNING, 'COPIED')
    logging.addLevelName(logging.INFO, 'UP_TO_DATE')
    logging.addLevelName(logging.CRITICAL, 'UPDATED')
    logging.addLevelName(21, 'DELETED')

    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s [%(levelname)s]: %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


def sync_folders(source, replica, delay):

    if delay <= 0:
        logger.error(f'Time interval is not valid. Please insert a value greater than 0.')
        raise SystemExit(1)
    if os.path.isabs(replica) and os.path.isabs(replica):
        logger.debug(f'Starting synchronization...\nSrc: {source}\nDst: {replica}\nSync time: {delay}')
    else:
        logger.debug(f'Starting synchronization...\nSrc: {os.path.abspath(source)}\nDst: {os.path.abspath(replica)}\nSync time: {delay}')

    try:
        while True:
            if not os.path.isdir(source):
                logger.debug(f'The {source} folder does not exist. Please try again.')
                break
            if not os.path.isdir(replica):
                os.makedirs(replica)
                logger.warning(f'Replica folder created: {replica}')
            compare_folders(source, replica)
            logger.debug('Synchronization completed.')
            time.sleep(delay)
    except KeyboardInterrupt:
        logger.error('Synchronization stopped manually.')
    finally:
        logger.debug('Exiting the synchronization script.')


def compare_files(file1, file2):
    try:
        with open(file1, 'rb') as f1, open(file2, 'rb') as f2:
            return hashlib.md5(f1.read()).hexdigest() == hashlib.md5(f2.read()).hexdigest()
    except PermissionError as e:
        logger.error(f'Permission denied while comparing files:{e}')
        return False


def compare_folders(source, replica):
    files_src = os.listdir(source)
    files_dst = os.listdir(replica)

    for file in files_src:
        src_filepath = os.path.join(source, file)
        dst_filepath = os.path.join(replica, file)

        if os.path.isdir(src_filepath):
            if not os.path.exists(dst_filepath):
                shutil.copytree(src_filepath, dst_filepath, symlinks=True)
                logger.warning(f'{src_filepath}')
            else:
                compare_folders(src_filepath, dst_filepath)
        else:
            if file in files_dst:
                if compare_files(src_filepath, dst_filepath):
                    logger.info(f'{src_filepath}')  # up do date
                else:
                    shutil.copy2(src_filepath, dst_filepath)
                    logger.critical(f'{src_filepath}')  # modified

            else:
                shutil.copy2(src_filepath, replica)
                logger.warning(f'{src_filepath}')  # created/copied

    # Remove extra files (on replica and not in the source)
    for file in files_dst:
        if file not in files_src:
            file_path = os.path.join(replica, file)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            else:
                os.remove(file_path)
            logger.log(21, f'{file_path}') # deleted


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SyncFolder scrypt',
                                     epilog='Author: rpcXYZ @ 2024',
                                     add_help=True)

    parser.add_argument('--src',
                        type=str,
                        required=True,
                        help='Source folder path')

    parser.add_argument('--dst',
                        type=str,
                        default='replica',
                        help='Replica folder path')

    parser.add_argument('--log-file',
                        type=str,
                        default='log.txt',
                        help='Log file path')

    parser.add_argument('--delay',
                        type=int,
                        default=10,
                        help='Delay for synchronization in seconds (Default: 10)')

    args = parser.parse_args()

    logger = setup_output(args.log_file)

    sync_folders(args.src, args.dst, args.delay)

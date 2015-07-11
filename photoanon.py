#!/usr/bin/env python3
# -*- Mode: Python; py-indent-offset: 4 -*-

# (c) Copyright Cameron Conn 2015
# This file is licensed GPLv3 or Later
# See LICENSE for details


from gi.repository import GExiv2

import argparse
from os.path import abspath, splitext, dirname, join
from fractions import Fraction
from random import uniform, randrange
from time import time
from datetime import datetime
import pprint


IMAGE_EXTENSIONS = ('.jpg', '.jpeg', '.gif', '.tif', '.png')
LONGITUDE_TAG = 'Exif.GPSInfo.GPSLongitude'
LATITUDE_TAG = 'Exif.GPSInfo.GPSLatitude'
ALTITUDE_TAG = 'Exif.GPSInfo.GPSAltitude'

_SAFE_TAGS_CACHE = None
_UNSAFE_TAGS_CACHE = None


def _load_cache():
    '''
    Load module cache of good and bad tags
    '''
    global _SAFE_TAGS_CACHE
    global _UNSAFE_TAGS_CACHE

    if _SAFE_TAGS_CACHE is None:
        script_dir = dirname(abspath(__file__))
        with open(join(script_dir, 'safe_tags.txt')) as tags:
            _SAFE_TAGS_CACHE = tuple(line.rstrip() for line in tags.readlines())
    if _UNSAFE_TAGS_CACHE is None:
        script_dir = dirname(abspath(__file__))
        with open(join(script_dir, 'unsafe_tags.txt')) as tags:
            _UNSAFE_TAGS_CACHE = tuple(line.rstrip() for line in tags.readlines())


def _to_deg(loc: str) -> float:
    '''
    Convert a coordinate in `dd mm ss` format to degrees in floating point

    loc - the string to convert to a location

    return the location coordination in degrees
    '''
    parts = loc.split(' ')

    if len(parts) != 4:
        raise ValueError('Bad coordinate format')

    direction = parts[3].upper().strip()

    if direction not in ('N', 'S', 'E', 'W'):
        raise ValueError('Invalid direction')

    dir_mult = 1 if (direction in ('N', 'E')) else -1

    # Use abs() to fix data
    degrees = abs(Fraction(parts[0]))
    mins = abs(Fraction(parts[1]))
    secs = abs(Fraction(parts[2]))

    result = float(degrees + mins / 60 + secs / 3600) * dir_mult

    if not (result <= 180 and result >= -180):
        raise ValueError('Coordinate out of range')

    return result


def _to_dms(loc: float) -> str:
    '''
    Convert a decimal coordinate to DMS format

    loc - the location coordinate to convert
    '''

    assert loc <= 180 and loc >= -180, 'Coordinate out of range [-180, 180]'

    is_positive = loc >= 0
    loc = abs(loc)
    minutes, seconds = divmod(loc * 3600, 60)
    degrees, minutes = divmod(minutes, 60)
    degrees = degrees if is_positive else -degrees

    seconds = Fraction(seconds)
    return '{}/1 {}/1 {}'.format(int(degrees), int(minutes), seconds)


def _parse_altitude(alt: str, ref_bit: int) -> float:
    '''
    Parse an altitude to a number

    alt - the altitude fraction, in meters
    ref_bit - reference bit from EXIF data
    '''

    alt_mult = 1 if ref_bit else -1

    return float(Fraction(alt) * alt_mult)


def remove_bad_tags(path: str):
    '''
    Remove the bad tags defined in unsafe_tags.txt from an image

    path - the file to remove the unsafe tags from
    '''
    if _UNSAFE_TAGS_CACHE is None:
        _load_cache()

    metadata = GExiv2.Metadata(path)

    for tag in _UNSAFE_TAGS_CACHE:
        # Asking for forgiveness is faster than asking for permission
        try:
            del metadata[tag]
            print('Deleted tag {}'.format(tag))
        except KeyError:
            pass

    metadata.save_file()


def write_metadata(path: str, data: dict=None):
    '''
    Write metadata to file

    path - the file path to write the metadata to
    data - the data to write to the file
        'Time': the UNIX time to set the image to
        'Latitude': the latitude in decimal format
        'Longitude': the longitude in decimal format
        'Altitude': the altitude in meters
    '''
    metadata = GExiv2.Metadata(path)

    if 'Time' in data:
        date_obj = datetime.fromtimestamp(data['Time'])
        metadata.set_date_time(date_obj)

        # Don't set metadata values that aren't already there
        if 'Exif.GPSInfo.GPSDateStamp' in metadata:
            metadata['Exif.GPSInfo.GPSDateStamp'] = date_obj.strftime('%Y:%m:%d')

        for tag in ('Exif.Image.DateTime', 'Exif.Photo.DateTimeDigitized',
                    'Exif.Photo.DateTimeOriginal'):
            if tag in metadata:
                metadata[tag] = date_obj.strftime('%Y:%m:%d %H:%M:%S')

    if 'Latitude' in data and 'Longitude' in data and 'Altitude' in data:
        metadata.set_gps_info(data['Latitude'],
                              data['Longitude'],
                              data['Altitude'])

    metadata.save_file()


def read_metadata(path: str) -> dict:
    '''
    Process an image and read it's information

    path - the path of the image to anonymize
    noise - whether or not to add random noise to the image

    Returns whether or not the image was successfully parsed
    '''

    # TODO: Determine file type by using Magic numbers instead of file extension
    f_path, ext = splitext(path)

    if ext not in IMAGE_EXTENSIONS:
        print('This image format is not supported! Extension type: {}'.format(ext))
        return False

    # Actually process image
    metadata = GExiv2.Metadata(path)
    info = dict()

    if LONGITUDE_TAG in metadata and \
       LATITUDE_TAG in metadata:
        lat_dms = metadata[LATITUDE_TAG] + ' ' + metadata[LATITUDE_TAG + 'Ref']
        long_dms = metadata[LONGITUDE_TAG] + ' ' + metadata[LONGITUDE_TAG + 'Ref']

        #print('Lat:  {}'.format(lat_dms))
        #print('Long: {}'.format(long_dms))

        info['Latitude'] = _to_deg(lat_dms)
        info['Longitude'] = _to_deg(long_dms)
    if ALTITUDE_TAG in metadata:
        altitude_bit = metadata[ALTITUDE_TAG + 'Ref']
        altitude_dms = metadata[ALTITUDE_TAG]

        info['Altitude'] = _parse_altitude(altitude_dms, altitude_bit)

    return info


def get_bad_tags(path: str):
    '''
    Get "bad" tags that an image has

    path - the path of the file to check for bad EXIF tags

    returns a tuple of the bad tags an image has
    '''
    _load_cache()

    metadata = GExiv2.Metadata(path)

    return tuple([key for key in metadata if key in _UNSAFE_TAGS_CACHE])


def create_fake_data() -> dict:
    '''
    Create a dictionary of Fake EXIF data
    '''

    data = {'Latitude': uniform(-180, 180),
            'Longitude': uniform(-180, 180),
            'Altitude': uniform(-200, 3200),
            'Time': randrange(int(time()))}

    return data


def main():
    '''
    Interprets command-line arguments and act accordingly
    '''
    parser = argparse.ArgumentParser(description='Tool to anonymize images via EXIF and image manipulation.')
    parser.add_argument('images', help='Image(s) to anonymize', nargs='+')
    parser.add_argument('-p', '--preserve', help='Keep original images; adds a prefix to anonymized images.',
                        action='store_true')
    parser.add_argument('-n', '--noise', help='Add noise to image to combat lense fingerprinting.',
                        action='store_true')
    parser.add_argument('-v', '--verbose', help='Be very generous with printing to output.', action='store_true')
    parser.add_argument('-i', '--info', help='Get information about file\'s dangerous EXIF data.',
                        action='store_true')
    parser.add_argument('-m', '--method', type=str, choices=('remove', 'randomize'), default='randomize', nargs=1,
                        help='''The method to anonymize the file with. Default=randomize. The `randomize` option creates '''
                             '''random data for the unsafe EXIF tags. The `remove` option removes those tags completely.''')

    args = parser.parse_args()
    printer = pprint.PrettyPrinter(indent=4)

    for image in args.images:
        image_path = abspath(image)
        geotag_info = read_metadata(image_path)

        if args.info:  # nondestructive read to file's metadata
            print('Geotagging data in {}'.format(image_path))
            if len(geotag_info):
                printer.pprint(geotag_info)
            else:
                print('None found')

            print('=' * 60)
            print('Bad tags in {}:'.format(image_path))
            bad_tags = get_bad_tags(image_path)
            if len(bad_tags):
                for t in bad_tags:
                    print(t)
            else:
                print('None found')

            if args.verbose:
                print('=' * 60)
                print('Full list of EXIF tags in {}:'.format(image_path))
                metadata = GExiv2.Metadata(image_path)
                for k in metadata:
                    print('{}: {}'.format(k, metadata[k]))
        else:
            remove_bad_tags(image_path)
            print('Removed bad image tags from {}'.format(image_path))

            if args.method == 'randomize':
                fake_geo_data = create_fake_data()
                printer.pprint(fake_geo_data)
                write_metadata(image_path, fake_geo_data)
                print('Wrote fake geodata to {}'.format(image_path))
            elif args.method == 'remove':
                pass
            else:
                print('An error occurred...')


if __name__ == '__main__':
    main()

#PhotoAnon

A simple tool to anonymize EXIF data from photos.

You can read [this blog post](http://camconn.cc/introducing-photoanon/) to learn a little about photoanon.

## Dependencies

To use photoanon.py, you must install the following dependencies on Ubuntu

    sudo apt-get install python3-scipy python3-numpy gir1.2-gexiv2-0.10 libexiv2-dev

Adapt these instructions to your distribution as needed.

Once you have installed these dependencies, you may install photoanon with:

    git clone https://github.com/camconn/photoanon.git
    cd photoanon
    sudo ./setup.py install

Now, you may run the program with the `photoanon` command

    $ photoanon --help

## Usage

For help using this program, run `./photoanon.py --help`

## Testing

Unit tests are in `tests/`. You can run them with `./setup.py test`.

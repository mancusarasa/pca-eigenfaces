#!/usr/bin/env python
from __future__ import print_function
from os import listdir
from os.path import abspath
from os.path import isdir
from os.path import join
from os.path import split
from os import mkdir
from os import rmdir
from shutil import rmtree
from os.path import exists
import click
from PIL import Image


@click.command()
@click.argument(
    'input-training-set',
    type=click.Path(exists=True, file_okay=False)
)
@click.argument(
    'output-training-set',
    type=click.Path(exists=False, file_okay=False)
)
def main(input_training_set, output_training_set):

    # get all the folders under input_training_set
    abs_path = abspath(input_training_set)
    abs_files = [join(abs_path, entry) for entry in listdir(abs_path)]
    input_folders = [entry for entry in abs_files if isdir(entry)]

    min_width = float('inf')
    min_height = float('inf')
    # iterate over all the images, getting its width and height
    # to get the global minimum size
    for folder in input_folders:
        images_paths = [join(folder, image) for image in listdir(folder)]
        for image_path in images_paths:
            with Image.open(image_path).convert('L') as img:
                width, height = img.size
                min_width = min(min_width, width)
                min_height = min(min_height, height)

    # having the minimum width and height, create a new training set with
    # all the images resized to (min_width, min_height).

    # first: delete the output folder if exists, then
    # create the output_training_set folder.
    output_abs_path = abspath(output_training_set)
    if exists(output_abs_path):
        rmtree(output_abs_path)
    mkdir(output_abs_path)

    # second: iterate the original images, resizing them
    # and saving them in output_abs_path, respecting the
    # original folders hierarchy.
    for folder in input_folders:
        input_path, input_folder = split(folder)
        output_folder = join(output_abs_path, input_folder)
        mkdir(output_folder)
        input_images_paths = [image for image in listdir(folder)]
        for input_image in input_images_paths:
            input_image_abs = join(folder, input_image)
            output_image_abs = join(output_folder, input_image)
            try:
                with Image.open(input_image_abs).convert('L') as img:
                    img.thumbnail((min_width, min_height))
                    img.save(output_image_abs)
            except:
                print('Error resizing file {}. Skipping.'.format(
                    input_image_abs)
                )


if __name__ == '__main__':
    main()

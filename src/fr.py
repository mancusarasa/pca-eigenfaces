#!/usr/bin/env python
from __future__ import print_function
import click
from os import listdir
from os.path import abspath
from os.path import isdir
from os.path import join

from subject import SubjectBuilder
from matrix import create_normalized_data
from matrix import create_characteristic_transformation
from matrix import find_closest_subject


def __create_subjects(training_set, new_data):
    '''
    Creates the subjects, based on the root path where all their images
    are saved.
    @param training_set path with all the subjects images.
    '''
    abs_path = abspath(training_set)
    new_data_abs_path = abspath(new_data)

    abs_files = [join(abs_path, entry) for entry in listdir(abs_path)]
    builder = SubjectBuilder()
    folders = [entry for entry in abs_files if isdir(entry)]
    train_subjects = [
        builder.create_training_subject(folder) for folder in folders
    ]
    unknown_subject = builder.create_classification_subject(new_data_abs_path)
    return train_subjects, unknown_subject


@click.command()
@click.argument(
    'training-set',
    type=click.Path(exists=True, file_okay=False)
)
@click.argument(
    'new-data',
    type=click.Path(exists=True, file_okay=True, dir_okay=False)
)
@click.option(
    '--pc',
    help='number of principal components to consider. Defaults to 5.',
    type=int,
    default=5
)
def main(training_set, new_data, pc):
    '''
    Entry point for the face recognition program.\n
    Training set: Directory with the training set. Must contain a list of
    directories, where each one of them must contain a set of images.\n
    New data: Element to be recognized as one of the training set.
    '''
    train_subjects, unknown_subject = __create_subjects(training_set, new_data)
    matrix_data, new_subject_data = create_normalized_data(
        train_subjects, unknown_subject
    )
    V = create_characteristic_transformation(matrix_data, pc)
    closest = find_closest_subject(train_subjects, unknown_subject, V)
    print('Subject \'{}\' is apparently \'{}\' from the training set.'.format(
        unknown_subject.name, closest.name)
    )

if __name__ == '__main__':
    main()

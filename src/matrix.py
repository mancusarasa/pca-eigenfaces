from __future__ import division
import numpy as np
from math import sqrt


def create_normalized_data(train_subjects, unknown_subject):
    '''
    Creates the A matrix, based on the recieved train_subjects.
    Also, creates the normalized data corresponding to the
    unknonw subject.
    '''
    matrix_data = []
    unknown_subject_data = unknown_subject.get_image_data(0)
    for subject in train_subjects:
        images_count = subject.get_images_count()
        for i in xrange(images_count):
            matrix_data.append(subject.get_image_data(i))

    # once the matrix with the images as row is created,
    # the following step is to normalize each column
    rows = len(matrix_data)
    cols = len(matrix_data[0])
    for col in xrange(cols):
        mean = 0
        for row in xrange(rows):
            mean += matrix_data[row][col]
        mean = mean / rows
        stddev = sqrt(rows)-1
        # normalize the training data
        for row in xrange(rows):
            matrix_data[row][col] = (matrix_data[row][col] - mean) / stddev
        # normalize the new subject data
        unknown_subject_data[col] = (unknown_subject_data[col] - mean) / stddev
    return matrix_data, unknown_subject_data


def create_characteristic_transformation(matrix_data, pc=5):
    '''
    Based on the recieved training set data, creates the characteristic
    transformation.
    '''
    A = np.matrix(matrix_data)
    A_t = A.getT()
    diagonal_mat = np.dot(A, A_t)
    # calculate the eigenvectors and eigenvalues of diagonal_mat
    V = []
    for i in xrange(pc):
        u_i, lambda_i = power_method(diagonal_mat)
        # having the eigenvector+eigenvalue of A*A_t,
        # calculate the same pair eigenvector of A_t*A
        # eigenrow = eigenvec.getT().tolist()[0]
        v_i = (np.dot(A_t, u_i) / sqrt(lambda_i)).getT().tolist()[0]
        # apply wielandt deflation to the diagonal matrix
        diagonal_mat = diagonal_mat - lambda_i*u_i*u_i.getT()
        V.append(v_i)
    return V


def power_method(matrix, iter_count=100):
    '''
    Performs iter_count iterations of the power method, to calculate
    the dominant pair (eigenvector, eigenvalue).
    '''
    b_i = np.random.rand(matrix.shape[0], 1)
    for i in xrange(iter_count):
        next_bi = matrix * b_i
        next_bi_norm = np.linalg.norm(next_bi)
        b_i = next_bi / next_bi_norm

    lambda_i = np.dot(b_i.getT(), np.dot(matrix, b_i))
    lambda_i = lambda_i / (np.linalg.norm(b_i)**2)
    return b_i, lambda_i[0, 0]


def find_closest_subject(train_subjects, unknown_subject, V):
    '''
    Finds the closest subject in the training set to the unknown subject,
    based on the characteristic transformation V.
    '''
    # get the projection of the unknown subject
    transformation = np.matrix(V)
    unknown_proj = np.dot(
        transformation, np.array(unknown_subject.get_image_data(0))
    )

    # project all the images of all the subjects, returning the
    # subject with the closest projection to unknown_proj.
    max_distance = float('inf')
    closest_subject = None
    for subject in train_subjects:
        imgs_count = subject.get_images_count()
        for i in xrange(imgs_count):
            curr_img_data = np.array(subject.get_image_data(i))
            curr_proj = np.dot(transformation, curr_img_data)
            curr_diff = unknown_proj - curr_proj
            diff = np.linalg.norm(curr_diff)
            if diff < max_distance:
                closest_subject = subject
                max_distance = diff

    return closest_subject

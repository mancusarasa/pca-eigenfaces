# Face recognition using PCA
The script fr.py implements the popular (?) eigenfaces method for face recognition. For more information, simply go to the [wikipedia entry](https://en.wikipedia.org/wiki/Eigenface).

# Usage
The script takes two parameters, trainingSet and newData.
* trainingSet: a path to a folder containing the training set images, with one folder for each subject containing his/her photos.
* newData: a path to a new subject photo.

For reference about the file system structure necessary for the trainingSet, check the folder sample\_data/training\_set in
this repo. Also, you can run

    $ ./fr.py --help

to print the help.

# Examples

    $./fr.py ../sample_data/training_set/ ../sample_data/test_set/subject6.pgm

This test run uses the ../sample\_data/training\_set/ directory as the training set, and attempts to classify the image
../sample\_data/test\_set/subject6.pgm (which obviously belongs to subject s6 from the training set).

# Dependencies
The dependencies are listed in requirements.txt. To install them, simply run

    $ pip install -r requirements.txt

Just use a virtualenv for these, man.

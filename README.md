# Face recognition using PCA
The script fr.py implements the popular (?) eigenfaces method for face recognition. For more information about the algorithm, you can visit its [wikipedia entry](https://en.wikipedia.org/wiki/Eigenface).

# Usage
The script takes two mandatory parameters, trainingSet and newData, and also an optional parameter pc .
* trainingSet: a path to a folder containing the training set images, with one folder for each subject containing his/her photos.
* newData: a path to a new subject photo.
* pc: the amount of principal components to consider on the classification of the unknown subject.

For reference about the file system structure necessary for the trainingSet, check the folder sample\_data/training\_set in
this repo. Also, you can run

    $ ./fr.py --help

to print the help.

# Examples

    $./fr.py ../sample_data/training_set/ ../sample_data/test_set/subject6.pgm --pc=10

This test run uses the ../sample\_data/training\_set/ directory as the training set, and attempts to classify the image
../sample\_data/test\_set/subject6.pgm (which obviously belongs to subject s6 from the training set), considering the first
10 principal components.

# Dependencies
The dependencies are listed in requirements.txt. Just use a virtualenv for these, man:

    $ sudo apt-get install python-virtualenv
    $ mkdir venv && virtualenv --always-copy --no-site-packages venv/
    $ . ./venv/bin/activate && pip install -r requirements.txt

Also, if you don't mind installing those globally, you can just run:

    $ sudo pip install -r requirements.txt

from PIL import Image
from os import listdir
from os.path import dirname
from os.path import split
from os.path import join


class SubjectInfo(object):
    '''A set of images that belong to the same subject.'''
    def __init__(self, images_paths):
        super(SubjectInfo, self).__init__()
        self.__images_paths = images_paths

    def get_count(self):
        '''
        Returns the amount of images held by the info instance.
        '''
        return len(self.__images_paths)

    def get_data(self, index):
        '''
        Returns data from the image at the specified index.
        '''
        # opens the image converted to grayscale ('L')
        pixels = []
        with Image.open(self.__images_paths[index]).convert('L') as img:
            pixels = [pixel for pixel in img.getdata()]
        return pixels


class Subject(object):
    '''A training subject, implemented as a composition of his set of images'''
    def __init__(self, name, info):
        super(Subject, self).__init__()
        self.name = name
        self.info = info

    def get_images_count(self):
        '''
        Returns the amount of images for this subject.
        '''
        return self.info.get_count()

    def get_image_data(self, index):
        '''
        Returns the data of the image at the given index.
        '''
        return self.info.get_data(index)


class SubjectBuilder(object):
    '''A Subjects Builder. Returnes new, configured Subject instances.'''
    def __init__(self):
        super(SubjectBuilder, self).__init__()

    def create_training_subject(self, imgs_path):
        '''
        Creates a new Subject.
        @param imgs_path path to a directory with the subjects images.
        '''
        images_paths = [join(imgs_path, image) for image in listdir(imgs_path)]
        info = SubjectInfo(images_paths)
        path, folder_name = split(imgs_path)
        return Subject(folder_name, info)

    def create_classification_subject(self, img_path):
        '''
        Creates the single individual to be recognized as one of the
        subjects in the training set.
        '''
        info = SubjectInfo([img_path])
        path, folder_name = split(img_path)
        return Subject(folder_name, info)

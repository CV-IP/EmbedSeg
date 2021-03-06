import os
import urllib
import zipfile
import shutil
from glob import glob
import numpy as np


def extract_data(zip_url, project_name, data_dir='../../../data/'):
    """
        Extracts data from `zip_url` to the location identified by `data_dir` and `project_name` parameters.
        Parameters
        ----------
        zip_url: string
            Indicates the url
        project_name: string
            Indicates the path to the sub-directory at the location identified by the parameter `data_dir`
        data_dir: string
            Indicates the path to the directory where the data should be saved.

    """

    zip_path = os.path.join(data_dir, project_name + '.zip')

    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print("Created new directory {}".format(data_dir))

    if (os.path.exists(zip_path)):
        print("Zip file was downloaded and extracted before!")
    else:
        if (os.path.exists(os.path.join(data_dir, project_name, 'download/'))):
            pass
        else:
            os.makedirs(os.path.join(data_dir, project_name, 'download/'))
            urllib.request.urlretrieve(zip_url, zip_path)
            print("Downloaded data as {}".format(zip_path))
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(data_dir)
            if os.path.exists(os.path.join(data_dir, os.path.basename(zip_url)[:-4], 'train')):
                shutil.move(os.path.join(data_dir, os.path.basename(zip_url)[:-4], 'train'),
                        os.path.join(data_dir, project_name, 'download/'))
            if os.path.exists(os.path.join(data_dir, os.path.basename(zip_url)[:-4], 'test')):
                shutil.move(os.path.join(data_dir, os.path.basename(zip_url)[:-4], 'test'),
                        os.path.join(data_dir, project_name, 'download/'))
            print("Unzipped data to {}".format(os.path.join(data_dir, project_name, 'download/')))


def make_dirs(data_dir, project_name):
    """
        Makes directories - `train`, `val, `test` and subdirectories under each `images` and `masks`
        Parameters
        ----------
        data_dir: string
            Indicates the path where the `project` lives.
        project_name: string
            Indicates the name of the sub-folder under the location identified by `data_dir`.
    """
    image_path_train = os.path.join(data_dir, project_name, 'train', 'images/')
    instance_path_train = os.path.join(data_dir, project_name, 'train', 'masks/')
    image_path_val = os.path.join(data_dir, project_name, 'val', 'images/')
    instance_path_val = os.path.join(data_dir, project_name, 'val', 'masks/')
    image_path_test = os.path.join(data_dir, project_name, 'test', 'images/')
    instance_path_test = os.path.join(data_dir, project_name, 'test', 'masks/')

    if not os.path.exists(image_path_train):
        os.makedirs(os.path.dirname(image_path_train))
        print("Created new directory : {}".format(image_path_train))

    if not os.path.exists(instance_path_train):
        os.makedirs(os.path.dirname(instance_path_train))
        print("Created new directory : {}".format(instance_path_train))

    if not os.path.exists(image_path_val):
        os.makedirs(os.path.dirname(image_path_val))
        print("Created new directory : {}".format(image_path_val))

    if not os.path.exists(instance_path_val):
        os.makedirs(os.path.dirname(instance_path_val))
        print("Created new directory : {}".format(instance_path_val))

    if not os.path.exists(image_path_test):
        os.makedirs(os.path.dirname(image_path_test))
        print("Created new directory : {}".format(image_path_test))

    if not os.path.exists(instance_path_test):
        os.makedirs(os.path.dirname(instance_path_test))
        print("Created new directory : {}".format(instance_path_test))

        
        
def split_train_crops(project_name, center, crops_dir = 'crops', subset=0.15, train_name = 'train', seed=1234):
    imageDir = os.path.join(crops_dir, project_name, train_name, 'images')
    instanceDir = os.path.join(crops_dir, project_name, train_name, 'masks')
    centerDir = os.path.join(crops_dir, project_name, train_name, 'center-'+center)
    
    image_names = sorted(glob(os.path.join(imageDir, '*.tif')))
    instance_names = sorted(glob(os.path.join(instanceDir, '*.tif')))
    center_names = sorted(glob(os.path.join(centerDir, '*.tif')))
    
    indices = np.arange(len(image_names))
    np.random.seed(seed)
    np.random.shuffle(indices)
    subsetLen = int(subset * len(image_names))
    valIndices = indices[:subsetLen]
    
    image_path_val = os.path.join(crops_dir, project_name, 'val', 'images/')
    instance_path_val = os.path.join(crops_dir, project_name, 'val', 'masks/')
    center_path_val = os.path.join(crops_dir, project_name, 'val', 'center-'+center+'/')
    
    val_images_exist = False
    val_masks_exist = False
    val_center_images_exist = False
    
    if not os.path.exists(image_path_val):
        os.makedirs(os.path.dirname(image_path_val))
        print("Created new directory : {}".format(image_path_val))
    else:
        val_images_exist=True

    if not os.path.exists(instance_path_val):
        os.makedirs(os.path.dirname(instance_path_val))
        print("Created new directory : {}".format(instance_path_val))
    else:
        val_masks_exist=True
    
    if not os.path.exists(center_path_val):
        os.makedirs(os.path.dirname(center_path_val))
        print("Created new directory : {}".format(center_path_val))
    else:
        val_center_images_exist=True
        
    if not val_images_exist and not val_masks_exist and not val_center_images_exist:
        for val_index in valIndices:
            shutil.move(image_names[val_index], os.path.join(crops_dir, project_name, 'val', 'images'))
            shutil.move(instance_names[val_index], os.path.join(crops_dir, project_name, 'val', 'masks'))
            shutil.move(center_names[val_index], os.path.join(crops_dir, project_name, 'val', 'center-'+center))
        
        print("Val Images/Masks/Center-{}-image crops saved at {}".format(center, os.path.join(crops_dir, project_name, 'val')))
    else:
        print("Val Images/Masks/Center-{}-image crops already available at {}".format(center, os.path.join(crops_dir, project_name, 'val')))
def split_train_val(data_dir, project_name, train_val_name, subset=0.15, seed=1234):
    """
        Splits the `train` directory into `val` directory using the partition percentage of `subset`.
        Parameters
        ----------
        data_dir: string
            Indicates the path where the `project` lives.
        project_name: string
            Indicates the name of the sub-folder under the location identified by `data_dir`.
        train_val_name: string
            Indicates the name of the sub-directory under `project-name` which must be split
        subset: float
            Indicates the fraction of data to be reserved for validation
        seed: integer
            Allows for the same partition to be used in each experiment.
            Change this if you would like to obtain results with different train-val partitions.
    """

    imageDir = os.path.join(data_dir, project_name, 'download', train_val_name, 'images')
    instanceDir = os.path.join(data_dir, project_name, 'download', train_val_name, 'masks')
    image_names = sorted(glob(os.path.join(imageDir, '*.tif')))
    instance_names = sorted(glob(os.path.join(instanceDir, '*.tif')))
    indices = np.arange(len(image_names))
    np.random.seed(seed)
    np.random.shuffle(indices)
    subsetLen = int(subset * len(image_names))
    valIndices = indices[:subsetLen]
    trainIndices = indices[subsetLen:]
    make_dirs(data_dir=data_dir, project_name=project_name)

    for val_index in valIndices:
        shutil.copy(image_names[val_index], os.path.join(data_dir, project_name, 'val', 'images'))
        shutil.copy(instance_names[val_index], os.path.join(data_dir, project_name, 'val', 'masks'))

    for trainIndex in trainIndices:
        shutil.copy(image_names[trainIndex], os.path.join(data_dir, project_name, 'train', 'images'))
        shutil.copy(instance_names[trainIndex], os.path.join(data_dir, project_name, 'train', 'masks'))

    imageDir = os.path.join(data_dir, project_name, 'download', 'test', 'images')
    instanceDir = os.path.join(data_dir, project_name, 'download', 'test', 'masks')
    image_names = sorted(glob(os.path.join(imageDir, '*.tif')))
    instance_names = sorted(glob(os.path.join(instanceDir, '*.tif')))
    testIndices = np.arange(len(image_names))
    for testIndex in testIndices:
        shutil.copy(image_names[testIndex], os.path.join(data_dir, project_name, 'test', 'images'))
        shutil.copy(instance_names[testIndex], os.path.join(data_dir, project_name, 'test', 'masks'))
    print("Train-Val-Test Images/Masks copied to {}".format(os.path.join(data_dir, project_name)))


def split_train_test(data_dir, project_name, train_test_name, subset=0.5, seed=1234):
    """
        Splits the `train` directory into `test` directory using the partition percentage of `subset`.
        Parameters
        ----------
        data_dir: string
            Indicates the path where the `project` lives.
        project_name: string
            Indicates the name of the sub-folder under the location identified by `data_dir`.
        train_test_name: string
            Indicates the name of the sub-directory under `project-name` which must be split
        subset: float
            Indicates the fraction of data to be reserved for evaluation
        seed: integer
            Allows for the same partition to be used in each experiment.
            Change this if you would like to obtain results with different train-test partitions.
    """

    image_dir = os.path.join(data_dir, project_name, 'download', train_test_name, 'images')
    instance_dir = os.path.join(data_dir, project_name, 'download', train_test_name, 'masks')
    image_names = sorted(glob(os.path.join(image_dir, '*.tif')))
    instance_names = sorted(glob(os.path.join(instance_dir, '*.tif')))
    indices = np.arange(len(image_names))
    np.random.seed(seed)
    np.random.shuffle(indices)
    subsetLen = int(subset * len(image_names))
    test_indices = indices[:subsetLen]
    make_dirs(data_dir=data_dir, project_name=project_name)
    test_images_exist = False
    test_masks_exist = False
    if not os.path.exists(os.path.join(data_dir, project_name, 'download', 'test', 'images')):
        os.makedirs(os.path.join(data_dir, project_name, 'download', 'test', 'images'))
        print("Created new directory : {}".format(os.path.join(data_dir, project_name, 'download', 'test', 'images')))
    else:
        test_images_exist= True
    if not os.path.exists(os.path.join(data_dir, project_name, 'download', 'test', 'masks')):
        os.makedirs(os.path.join(data_dir, project_name, 'download', 'test', 'masks'))
        print("Created new directory : {}".format(os.path.join(data_dir, project_name, 'download', 'test', 'masks')))
    else:
        test_masks_exist= True
    if not test_images_exist and not test_masks_exist:
        for test_index in test_indices:
            shutil.move(image_names[test_index], os.path.join(data_dir, project_name, 'download', 'test', 'images'))
            shutil.move(instance_names[test_index], os.path.join(data_dir, project_name, 'download', 'test', 'masks'))
        print("Train-Test Images/Masks saved at {}".format(os.path.join(data_dir, project_name, 'download')))
    else:
        print("Train-Test Images/Masks already available at {}".format(os.path.join(data_dir, project_name, 'download')))
    


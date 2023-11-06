from typing import Dict, List, Optional, Union

from dataset_tools.templates import (
    AnnotationType,
    Category,
    CVTask,
    Domain,
    Industry,
    License,
    Research,
)

##################################
# * Before uploading to instance #
##################################
PROJECT_NAME: str = "GTSDB"
PROJECT_NAME_FULL: str = "GTSDB: The German Traffic Sign Detection Benchmark"
HIDE_DATASET = False  # set False when 100% sure about repo quality

##################################
# * After uploading to instance ##
##################################
LICENSE: License = License.Custom(url="https://benchmark.ini.rub.de/gtsdb_about.html#Availability_of_datasets")
APPLICATIONS: List[Union[Industry, Domain, Research]] = [Industry.Automotive()]
CATEGORY: Category = Category.SelfDriving()

CV_TASKS: List[CVTask] = [AnnotationType.ObjectDetection()]
ANNOTATION_TYPES: List[AnnotationType] = [AnnotationType.ObjectDetection()]

RELEASE_DATE: Optional[str] = "2013-06-09"  # e.g. "YYYY-MM-DD"
if RELEASE_DATE is None:
    RELEASE_YEAR: int = None

HOMEPAGE_URL: str = "https://benchmark.ini.rub.de/gtsdb_dataset.html"
# e.g. "https://some.com/dataset/homepage"

PREVIEW_IMAGE_ID: int = 7232560
# This should be filled AFTER uploading images to instance, just ID of any image.

GITHUB_URL: str = "https://github.com/dataset-ninja/gtsdb"
# URL to GitHub repo on dataset ninja (e.g. "https://github.com/dataset-ninja/some-dataset")

##################################
### * Optional after uploading ###
##################################
DOWNLOAD_ORIGINAL_URL: Optional[Union[str, dict]] = {
    "FullIJCNN2013.zip": "https://sid.erda.dk/public/archives/ff17dc924eba88d5d01a807357d6614c/FullIJCNN2013.zip",
    "TestIJCNN2013.zip": "https://sid.erda.dk/public/archives/ff17dc924eba88d5d01a807357d6614c/TestIJCNN2013.zip",
    "TrainIJCNN2013.zip": "https://sid.erda.dk/public/archives/ff17dc924eba88d5d01a807357d6614c/TrainIJCNN2013.zip",
    "gt.txt": "https://sid.erda.dk/public/archives/ff17dc924eba88d5d01a807357d6614c/gt.txt",
}
# Optional link for downloading original dataset (e.g. "https://some.com/dataset/download")

CLASS2COLOR: Optional[Dict[str, List[str]]] = {
    "speed limit 20": [230, 25, 75],
    "speed limit 30": [60, 180, 75],
    "speed limit 50": [255, 225, 25],
    "speed limit 60": [0, 130, 200],
    "speed limit 70": [245, 130, 48],
    "speed limit 80": [145, 30, 180],
    "restriction ends 80": [70, 240, 240],
    "speed limit 100": [240, 50, 230],
    "speed limit 120": [210, 245, 60],
    "no overtaking": [250, 190, 212],
    "no overtaking (trucks)": [0, 128, 128],
    "priority at next intersection": [220, 190, 255],
    "priority road": [170, 110, 40],
    "give way": [255, 250, 200],
    "stop": [128, 0, 0],
    "no traffic both ways": [170, 255, 195],
    "no trucks": [128, 128, 0],
    "no entry": [255, 215, 180],
    "danger": [0, 0, 128],
    "bend left": [245, 130, 48],
    "bend right": [145, 30, 180],
    "bend": [70, 240, 240],
    "uneven road": [240, 50, 230],
    "slippery road": [210, 245, 60],
    "road narrows": [250, 190, 212],
    "construction": [0, 128, 128],
    "traffic signal": [220, 190, 255],
    "pedestrian crossing": [170, 110, 40],
    "school crossing": [255, 250, 200],
    "cycles crossing": [128, 0, 0],
    "snow": [170, 255, 195],
    "animals": [128, 128, 0],
    "restriction ends": [255, 215, 180],
    "go right": [0, 0, 128],
    "go left": [245, 130, 48],
    "go straight": [145, 30, 180],
    "go right or straight": [70, 240, 240],
    "go left or straight": [240, 50, 230],
    "keep right": [210, 245, 60],
    "keep left": [250, 190, 212],
    "roundabout": [0, 128, 128],
    "restriction ends (overtaking)": [220, 190, 255],
    "restriction ends (overtaking (trucks))": [170, 110, 40],
}
# If specific colors for classes are needed, fill this dict (e.g. {"class1": [255, 0, 0], "class2": [0, 255, 0]})

# If you have more than the one paper, put the most relatable link as the first element of the list
# Use dict key to specify name for a button
PAPER: Optional[Union[str, List[str], Dict[str, str]]] = "https://ieeexplore.ieee.org/document/6706807"
BLOGPOST: Optional[Union[str, List[str], Dict[str, str]]] = None
REPOSITORY: Optional[Union[str, List[str], Dict[str, str]]] = None

CITATION_URL: Optional[str] = "https://benchmark.ini.rub.de/gtsdb_news.html"
AUTHORS: Optional[List[str]] = ["Sebastian Houben", "Johannes Stallkamp", "Jan Salmen", "Marc Schlipsing",  "Christian Igel"]
AUTHORS_CONTACTS: Optional[List[str]] = ["tsd-benchmark@ini.rub.de"]

ORGANIZATION_NAME: Optional[Union[str, List[str]]] = ["University of Bochum, Germany", "University of Copenhagen, Denmark"]
ORGANIZATION_URL: Optional[Union[str, List[str]]] = ["http://www.ruhr-uni-bochum.de/en", "https://www.ku.dk/english/"]

# Set '__PRETEXT__' or '__POSTTEXT__' as a key with string value to add custom text. e.g. SLYTAGSPLIT = {'__POSTTEXT__':'some text}
SLYTAGSPLIT: Optional[Dict[str, Union[List[str], str]]] = {"traffic sign categories":["prohibitory", "mandatory", "danger", "other"], "__POSTTEXT__": "Explore them in the supervisely labeling tool"}
TAGS: Optional[List[str]] = None


SECTION_EXPLORE_CUSTOM_DATASETS: Optional[List[str]] = None

##################################
###### ? Checks. Do not edit #####
##################################


def check_names():
    fields_before_upload = [PROJECT_NAME]  # PROJECT_NAME_FULL
    if any([field is None for field in fields_before_upload]):
        raise ValueError("Please fill all fields in settings.py before uploading to instance.")


def get_settings():
    if RELEASE_DATE is not None:
        global RELEASE_YEAR
        RELEASE_YEAR = int(RELEASE_DATE.split("-")[0])

    settings = {
        "project_name": PROJECT_NAME,
        "project_name_full": PROJECT_NAME_FULL or PROJECT_NAME,
        "hide_dataset": HIDE_DATASET,
        "license": LICENSE,
        "applications": APPLICATIONS,
        "category": CATEGORY,
        "cv_tasks": CV_TASKS,
        "annotation_types": ANNOTATION_TYPES,
        "release_year": RELEASE_YEAR,
        "homepage_url": HOMEPAGE_URL,
        "preview_image_id": PREVIEW_IMAGE_ID,
        "github_url": GITHUB_URL,
    }

    if any([field is None for field in settings.values()]):
        raise ValueError("Please fill all fields in settings.py after uploading to instance.")

    settings["release_date"] = RELEASE_DATE
    settings["download_original_url"] = DOWNLOAD_ORIGINAL_URL
    settings["class2color"] = CLASS2COLOR
    settings["paper"] = PAPER
    settings["blog"] = BLOGPOST
    settings["repository"] = REPOSITORY
    settings["citation_url"] = CITATION_URL
    settings["authors"] = AUTHORS
    settings["authors_contacts"] = AUTHORS_CONTACTS
    settings["organization_name"] = ORGANIZATION_NAME
    settings["organization_url"] = ORGANIZATION_URL
    settings["slytagsplit"] = SLYTAGSPLIT
    settings["tags"] = TAGS

    settings["explore_datasets"] = SECTION_EXPLORE_CUSTOM_DATASETS

    return settings

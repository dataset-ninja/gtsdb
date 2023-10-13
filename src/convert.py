# https://www.kaggle.com/datasets/safabouguezzi/german-traffic-sign-detection-benchmark-gtsdb

import os
import shutil
import xml.etree.ElementTree as ET
from collections import defaultdict
from urllib.parse import unquote, urlparse

import cv2
import numpy as np
import supervisely as sly
from dataset_tools.convert import unpack_if_archive
from dotenv import load_dotenv
from supervisely.io.fs import (
    dir_exists,
    file_exists,
    get_file_ext,
    get_file_name,
    get_file_name_with_ext,
    get_file_size,
    mkdir,
    remove_dir,
)
from tqdm import tqdm

import src.settings as s


def download_dataset(teamfiles_dir: str) -> str:
    """Use it for large datasets to convert them on the instance"""
    api = sly.Api.from_env()
    team_id = sly.env.team_id()
    storage_dir = sly.app.get_data_dir()

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, str):
        parsed_url = urlparse(s.DOWNLOAD_ORIGINAL_URL)
        file_name_with_ext = os.path.basename(parsed_url.path)
        file_name_with_ext = unquote(file_name_with_ext)

        sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
        local_path = os.path.join(storage_dir, file_name_with_ext)
        teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

        fsize = api.file.get_directory_size(team_id, teamfiles_dir)
        with tqdm(
            desc=f"Downloading '{file_name_with_ext}' to buffer...",
            total=fsize,
            unit="B",
            unit_scale=True,
        ) as pbar:        
            api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)
        dataset_path = unpack_if_archive(local_path)

    if isinstance(s.DOWNLOAD_ORIGINAL_URL, dict):
        for file_name_with_ext, url in s.DOWNLOAD_ORIGINAL_URL.items():
            local_path = os.path.join(storage_dir, file_name_with_ext)
            teamfiles_path = os.path.join(teamfiles_dir, file_name_with_ext)

            if not os.path.exists(get_file_name(local_path)):
                fsize = api.file.get_directory_size(team_id, teamfiles_dir)
                with tqdm(
                    desc=f"Downloading '{file_name_with_ext}' to buffer...",
                    total=fsize,
                    unit="B",
                    unit_scale=True,
                ) as pbar:
                    api.file.download(team_id, teamfiles_path, local_path, progress_cb=pbar)

                sly.logger.info(f"Start unpacking archive '{file_name_with_ext}'...")
                unpack_if_archive(local_path)
            else:
                sly.logger.info(
                    f"Archive '{file_name_with_ext}' was already unpacked to '{os.path.join(storage_dir, get_file_name(file_name_with_ext))}'. Skipping..."
                )

        dataset_path = storage_dir
    return dataset_path
    
def count_files(path, extension):
    count = 0
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith(extension):
                count += 1
    return count
    
def convert_and_upload_supervisely_project(
    api: sly.Api, workspace_id: int, project_name: str
) -> sly.ProjectInfo:

    # project_name = "German Traffic Sign Detection"
    ds_path = "/home/grokhi/rawdata/gtsdb"
    train_path = (
        "/home/grokhi/rawdata/gtsdb/TrainIJCNN2013/TrainIJCNN2013"
    )
    test_path = "/home/grokhi/rawdata/gtsdb/TestIJCNN2013/TestIJCNN2013Download"
    bbox_file_path = "/home/grokhi/rawdata/gtsdb/TrainIJCNN2013/TrainIJCNN2013/gt.txt"
    batch_size = 30
    images_ext = ".ppm"
    new_images_ext = ".png"

    ds_name_to_path = {"train": train_path, "test": test_path}


    def create_ann(image_path):
        labels = []

        img = cv2.imread(image_path)
        img_height = img.shape[0]
        img_wight = img.shape[1]

        file_name = get_file_name_with_ext(image_path)

        bbox_data = name_to_data[file_name]

        for curr_data in bbox_data:
            obj_class = idx_to_class[int(curr_data[4])]

            if int(curr_data[4]) in [0, 1, 2, 3, 4, 5, 7, 8, 9, 10, 15, 16]:
                tag = sly.Tag(prohibitory)
            elif int(curr_data[4]) in [33, 34, 35, 36, 37, 38, 39, 40]:
                tag = sly.Tag(mandatory)
            elif int(curr_data[4]) in [11, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]:
                tag = sly.Tag(danger)
            else:
                tag = sly.Tag(other)

            left = int(curr_data[0])
            right = int(curr_data[2])
            top = int(curr_data[1])
            bottom = int(curr_data[3])
            rectangle = sly.Rectangle(top=top, left=left, bottom=bottom, right=right)
            label = sly.Label(rectangle, obj_class, tags=[tag])
            labels.append(label)

        return sly.Annotation(img_size=(img_height, img_wight), labels=labels)


    prohibitory = sly.TagMeta("prohibitory", sly.TagValueType.NONE)
    mandatory = sly.TagMeta("mandatory", sly.TagValueType.NONE)
    danger = sly.TagMeta("danger", sly.TagValueType.NONE)
    other = sly.TagMeta("other", sly.TagValueType.NONE)

    idx_to_class = {
        0: sly.ObjClass("speed limit 20", sly.Rectangle),
        1: sly.ObjClass("speed limit 30", sly.Rectangle),
        2: sly.ObjClass("speed limit 50", sly.Rectangle),
        3: sly.ObjClass("speed limit 60", sly.Rectangle),
        4: sly.ObjClass("speed limit 70", sly.Rectangle),
        5: sly.ObjClass("speed limit 80", sly.Rectangle),
        6: sly.ObjClass("restriction ends 80", sly.Rectangle),
        7: sly.ObjClass("speed limit 100", sly.Rectangle),
        8: sly.ObjClass("speed limit 120", sly.Rectangle),
        9: sly.ObjClass("no overtaking", sly.Rectangle),
        10: sly.ObjClass("no overtaking (trucks)", sly.Rectangle),
        11: sly.ObjClass("priority at next intersection", sly.Rectangle),
        12: sly.ObjClass("priority road", sly.Rectangle),
        13: sly.ObjClass("give way", sly.Rectangle),
        14: sly.ObjClass("stop", sly.Rectangle),
        15: sly.ObjClass("no traffic both ways", sly.Rectangle),
        16: sly.ObjClass("no trucks", sly.Rectangle),
        17: sly.ObjClass("no entry", sly.Rectangle),
        18: sly.ObjClass("danger", sly.Rectangle),
        19: sly.ObjClass("bend left", sly.Rectangle),
        20: sly.ObjClass("bend right", sly.Rectangle),
        21: sly.ObjClass("bend", sly.Rectangle),
        22: sly.ObjClass("uneven road", sly.Rectangle),
        23: sly.ObjClass("slippery road", sly.Rectangle),
        24: sly.ObjClass("road narrows", sly.Rectangle),
        25: sly.ObjClass("construction", sly.Rectangle),
        26: sly.ObjClass("traffic signal", sly.Rectangle),
        27: sly.ObjClass("pedestrian crossing", sly.Rectangle),
        28: sly.ObjClass("school crossing", sly.Rectangle),
        29: sly.ObjClass("cycles crossing", sly.Rectangle),
        30: sly.ObjClass("snow", sly.Rectangle),
        31: sly.ObjClass("animals", sly.Rectangle),
        32: sly.ObjClass("restriction ends", sly.Rectangle),
        33: sly.ObjClass("go right", sly.Rectangle),
        34: sly.ObjClass("go left", sly.Rectangle),
        35: sly.ObjClass("go straight", sly.Rectangle),
        36: sly.ObjClass("go right or straight", sly.Rectangle),
        37: sly.ObjClass("go left or straight", sly.Rectangle),
        38: sly.ObjClass("keep right", sly.Rectangle),
        39: sly.ObjClass("keep left", sly.Rectangle),
        40: sly.ObjClass("roundabout", sly.Rectangle),
        41: sly.ObjClass("restriction ends (overtaking)", sly.Rectangle),
        42: sly.ObjClass("restriction ends (overtaking (trucks))", sly.Rectangle),
    }


    project = api.project.create(workspace_id, project_name, change_name_if_conflict=True)
    meta = sly.ProjectMeta(
        obj_classes=list(idx_to_class.values()), tag_metas=[prohibitory, mandatory, danger, other]
    )
    api.project.update_meta(project.id, meta.to_json())

    name_to_data = defaultdict(list)

    with open(bbox_file_path) as f:
        content = f.read().split("\n")
        for row in content:
            if len(row) > 0:
                row = row.split(";")
                name_to_data[row[0]].append(row[1:])


    for ds_name, data_path in ds_name_to_path.items():
        dataset = api.dataset.create(project.id, ds_name, change_name_if_conflict=True)

        images_names = [
            im_name for im_name in os.listdir(data_path) if get_file_ext(im_name) == images_ext
        ]

        progress = sly.Progress("Create dataset {}".format(ds_name), len(images_names))

        for images_names_batch in sly.batched(images_names, batch_size=batch_size):
            img_pathes_batch = [
                os.path.join(data_path, image_name) for image_name in images_names_batch
            ]

            temp_img_pathes_batch = []
            temp_folder = os.path.join(ds_path, "temp")
            mkdir(temp_folder)
            for im_path in img_pathes_batch:
                temp_img = cv2.imread(im_path)
                new_img_path = os.path.join(temp_folder, get_file_name(im_path) + new_images_ext)
                temp_img_pathes_batch.append(new_img_path)
                cv2.imwrite(new_img_path, temp_img)

            images_names_batch = [get_file_name_with_ext(im_path) for im_path in temp_img_pathes_batch]

            img_infos = api.image.upload_paths(dataset.id, images_names_batch, temp_img_pathes_batch)
            img_ids = [im_info.id for im_info in img_infos]

            remove_dir(temp_folder)
            if ds_name != "test":
                anns = [create_ann(image_path) for image_path in img_pathes_batch]
                api.annotation.upload_anns(img_ids, anns)

            progress.iters_done_report(len(images_names_batch))
    return project



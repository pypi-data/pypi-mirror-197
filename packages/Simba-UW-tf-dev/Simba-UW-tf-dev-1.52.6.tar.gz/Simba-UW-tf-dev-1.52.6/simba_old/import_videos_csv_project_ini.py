__author__ = "Simon Nilsson", "JJ Choong"

import shutil
import os, glob
import pandas as pd
from simba.extract_frames_fast import video_to_frames
from simba.drop_bp_cords import get_fn_ext
from simba.read_config_unit_tests import (read_config_file,
                                          read_config_entry,
                                          read_project_path_and_file_type,
                                          check_file_exist_and_readable,
                                          check_if_filepath_list_is_empty)
from simba.misc_tools import SimbaTimer, get_number_of_header_columns_in_df
from simba.enums import Paths, ReadConfig, Dtypes

def extract_frames_from_all_videos_in_directory(config_path: str,
                                                directory: str) -> None:
    """
    Helper to extract all frames from all videos in a directory. The results are saved in the project_folder/frames/input
    directory of the SimBa project

    Parameters
    ----------
    config_path: str
        path to SimBA project config file in Configparser format
    directory: str
        path to file or folder containing videos in mp4 and/or avi format

    :return
    ----------
    list

    Examples
    ----------
    >>> extract_frames_from_all_videos_in_directory(config_path='project_folder/project_config.ini', source='/MyVideoDirectory/')
    """
    timer = SimbaTimer()
    timer.start_timer()
    video_paths, video_types = [], ['.avi', '.mp4']
    files_in_folder = glob.glob(directory + '/*')
    for file_path in files_in_folder:
        _, _, ext = get_fn_ext(filepath=file_path)
        if ext.lower() in video_types:
            video_paths.append(file_path)
    if len(video_paths) == 0:
        print('SIMBA ERROR: 0 video files in mp4 or avi format found in {}'.format(directory))
        raise ValueError(f'SIMBA ERROR: 0 video files in mp4/avi format found in {directory}')
    config = read_config_file(config_path)
    project_path = read_config_entry(config, 'General settings', 'project_path', data_type='folder_path')

    print('Extracting frames for {} videos into project_folder/frames/input directory...'.format(len(video_paths)))
    for video_path in video_paths:
        dir_name, video_name, ext = get_fn_ext(video_path)
        save_path = os.path.join(project_path, 'frames', 'input', video_name)
        if not os.path.exists(save_path): os.makedirs(save_path)
        else: print(f'Frames for video {video_name} already extracted. SimBA is overwriting prior frames...')
        video_to_frames(video_path, save_path, overwrite=True, every=1, chunk_size=1000)
    timer.stop_timer()
    print(f'SIMBA COMPLETE: Frames created for {str(len(video_paths))} videos (elapsed time: {timer.elapsed_time_str}s).')


def copy_img_folder(config_path: str, source: str) -> None:
    timer = SimbaTimer()
    timer.start_timer()
    if not os.path.isdir(source):
        print(f'SIMBA ERROR: source {source} is not a directory.')
        raise NotADirectoryError(f'SIMBA ERROR: source {source} is not a directory.')
    if len(glob.glob(source + '/*.png')) == 0:
        print(f'SIMBA ERROR: source {source} foes not contain any .png files.')
        raise ValueError(f'SIMBA ERROR: source {source} foes not contain any .png files.')
    input_basename = os.path.basename(source)
    config = read_config_file(config_path)
    project_path = read_config_entry(config, ReadConfig.GENERAL_SETTINGS.value, ReadConfig.PROJECT_PATH.value, data_type='folder_path')
    input_frames_dir = os.path.join(project_path, Paths.INPUT_FRAMES_DIR.value)
    destination = os.path.join(input_frames_dir, input_basename)
    if os.path.isdir(destination):
        print(f'SIMBA ERROR: {destination} already exist in SimBA project.')
        raise ValueError(f'SIMBA ERROR: {destination} already exist in SimBA project.')
    print(f'Importing image files for {input_basename}...')
    shutil.copytree(source, destination)
    timer.stop_timer()
    print(f'SIMBA COMPLETE: {destination} imported to SimBA project (elapsed time {timer.elapsed_time_str}s)')

def copy_singlevideo_DPKini(inifile,source):
    try:
        print('Copying video...')
        dest = str(os.path.dirname(inifile))
        dest1 = str(os.path.join(dest, 'videos', 'input'))

        if os.path.exists(os.path.join(dest1, os.path.basename(source))):
            print(os.path.basename(source), 'already exist in', dest1)
        else:
            shutil.copy(source, dest1)
            nametoprint = os.path.join('', *(splitall(dest1)[-4:]))
            print(os.path.basename(source),'copied to',nametoprint)

        print('Finished copying video.')
    except:
        pass

def copy_singlevideo_ini(simba_ini_path: str,
                         source_path: str) -> None:

    """ Helper to import single video file to SimBA project
    Parameters
    ----------
    simba_ini_path: str
        path to SimBA project config file in Configparser format
    source_path: str
        Path to video file.
    """

    print('Copying video file...')
    dir_name, filename, file_extension = get_fn_ext(source_path)
    new_filename = os.path.join(filename + file_extension)
    destination = os.path.join(os.path.dirname(simba_ini_path), 'videos', new_filename)
    if os.path.isfile(destination):
        print('SIMBA ERROR: {} already exist in SimBA project. To import, delete this video file before importing the new video file with the same name.'.format(filename))
        raise FileExistsError()
    else:
        shutil.copy(source_path, destination)
        print('SIMBA COMPLETE: Video {} imported to SimBA project (project_folder/videos directory).'.format(filename))

def copy_multivideo_DPKini(inifile,source,filetype):
    try:
        print('Copying videos...')
        dest = str(os.path.dirname(inifile))
        dest1 = os.path.join(dest, 'videos', 'input')
        files = []

        ########### FIND FILES ###########
        for i in os.listdir(source):
            if i.__contains__(str('.'+ filetype)):
                files.append(i)

        for f in files:
            filetocopy = os.path.join(source, f)
            if os.path.exists(os.path.join(dest1,f)):
                print(f, 'already exist in', dest1)

            elif not os.path.exists(os.path.join(dest1, f)):
                shutil.copy(filetocopy, dest1)
                nametoprint = os.path.join('', *(splitall(dest1)[-4:]))
                print(f, 'copied to', nametoprint)

        print('Finished copying videos.')
    except:
        print('Please select a folder and enter in the file type')


def import_dlc_csv(config_path: str, source: str) -> list:
    """
    Imports file or folder DLC pose-estimation CSV files to SimBA project. Returns list of file paths to the imported files.

    Parameters
    ----------
    config_path: str
        path to SimBA project config file in Configparser format
    source: str
        path to file or folder containing DLC pose-estimation CSV files

    :return
    ----------
    list

    Examples
    ----------
    >>> import_dlc_csv(config_path='project_folder/project_config.ini', source='CSV_import/Together_1.csv')
    >>> ['project_folder/csv/input_csv/Together_1.csv']
    """

    timer = SimbaTimer()
    timer.start_timer()
    config = read_config_file(ini_path=config_path)
    project_path, file_type = read_project_path_and_file_type(config=config)
    original_file_name_dir = os.path.join(project_path, 'csv', 'input_csv', 'original_filename')
    input_csv_dir = os.path.join(project_path, 'csv', 'input_csv')
    imported_files = glob.glob(input_csv_dir + '/*.' + file_type)
    imported_file_names = []
    imported_file_paths = []
    for file_path in imported_files:
        _, video_name, _ = get_fn_ext(filepath=file_path)
        imported_file_names.append(video_name)
    if not os.path.exists(original_file_name_dir): os.makedirs(original_file_name_dir)
    if os.path.isdir(source):
        csv_files = glob.glob(source + '/*.csv')
        check_if_filepath_list_is_empty(csv_files, error_msg=f'SIMBA ERROR: NO .csv files found in {source} directory.')
    else:
        csv_files = [source]

    for file_path in csv_files:
        check_file_exist_and_readable(file_path=file_path)
        _, video_name, file_ext = get_fn_ext(filepath=file_path)
        if 'DLC_' in video_name:
            new_file_name = video_name.split('DLC_')[0] + '.csv'
        elif 'DeepCut' in video_name:
            new_file_name = video_name.split('DeepCut')[0] + '.csv'
        else:
            new_file_name = video_name.split('.')[0] + '.csv'
        new_file_name_wo_ext = new_file_name.split('.')[0]
        video_basename = os.path.basename(file_path)
        print(f'Importing {video_name} to SimBA project...')
        if new_file_name_wo_ext in imported_file_names:
            print(f'SIMBA IMPORT ERROR: {new_file_name} already exist in project. Remove file from project or rename imported video file name before importing.')
            raise FileExistsError(f'SIMBA IMPORT ERROR: {new_file_name} already exist in project. Remove file from project or rename imported video file name before importing.')
        shutil.copy(file_path, input_csv_dir)
        shutil.copy(file_path, original_file_name_dir)
        os.rename(os.path.join(input_csv_dir, video_basename), os.path.join(input_csv_dir, new_file_name))
        df = pd.read_csv(os.path.join(input_csv_dir, new_file_name))
        header_cols = get_number_of_header_columns_in_df(df=df)
        if header_cols == 3:
            df = df.iloc[1:]
        if file_type == 'parquet':
            df = pd.read_csv(os.path.join(input_csv_dir, video_basename))
            df = df.apply(pd.to_numeric, errors='coerce')
            df.to_parquet(os.path.join(input_csv_dir, new_file_name))
            os.remove(os.path.join(input_csv_dir, video_basename))
        if file_type == 'csv':
            df.to_csv(os.path.join(input_csv_dir, new_file_name), index=False)
        imported_file_paths.append(os.path.join(input_csv_dir, new_file_name))
        print(f'Pose-estimation data for video {video_name} imported to SimBA project...')
    return imported_file_paths
from __future__ import division
import os, glob
import pandas as pd
import math
import numpy as np
from scipy.spatial import ConvexHull
import scipy
from configparser import ConfigParser, NoOptionError, NoSectionError
from simba.features_scripts.unit_tests import check_minimum_roll_windows, read_video_info_csv, read_video_info
from simba.misc_tools import get_file_path_parts
from simba.rw_dfs import read_df, save_df



def extract_features_wotarget_4(inifile):
    configFile = str(inifile)
    config = ConfigParser()
    config.read(configFile)
    csv_dir = config.get('General settings', 'csv_path')
    csv_dir_in = os.path.join(csv_dir, 'outlier_corrected_movement_location')
    csv_dir_out = os.path.join(csv_dir, 'features_extracted')
    vidInfPath = config.get('General settings', 'project_path')
    vidinfDf = read_video_info_csv(os.path.join(vidInfPath, 'logs', 'video_info.csv'))

    if not os.path.exists(csv_dir_out):
        os.makedirs(csv_dir_out)
    def count_values_in_range(series, values_in_range_min, values_in_range_max):
        return series.between(left=values_in_range_min, right=values_in_range_max).sum()

    def angle3pt(ax, ay, bx, by, cx, cy):
        ang = math.degrees(
            math.atan2(cy - by, cx - bx) - math.atan2(ay - by, ax - bx))
        return ang + 360 if ang < 0 else ang

    roll_windows = []
    roll_windows_values = [2, 5, 6, 7.5, 15]

    #REMOVE WINDOWS THAT ARE TOO SMALL
    minimum_fps = vidinfDf['fps'].min()
    roll_windows_values = check_minimum_roll_windows(roll_windows_values, minimum_fps)

    try:
        wfileType = config.get('General settings', 'workflow_file_type')
    except NoOptionError:
        wfileType = 'csv'

    filesFound = glob.glob(csv_dir_in + '/*.' + wfileType)

    ########### CREATE PD FOR RAW DATA AND PD FOR MOVEMENT BETWEEN FRAMES ###########
    for currentFile in filesFound:
        M1_hull_large_euclidean_list = []
        M1_hull_small_euclidean_list = []
        M1_hull_mean_euclidean_list = []
        M1_hull_sum_euclidean_list = []
        _, currVidName, _ = get_file_path_parts(currentFile)

        # get current pixels/mm
        currVideoSettings, currPixPerMM, fps = read_video_info(vidinfDf=vidinfDf, currVidName=currVidName)
        fps = float(currVideoSettings['fps'])
        print('Processing ' + '"' + str(currVidName) + '".' + ' Fps: ' + str(fps) + ". mm/ppx: " + str(currPixPerMM))

        for i in range(len(roll_windows_values)):
            roll_windows.append(int(fps / roll_windows_values[i]))

        columnHeaders = ["Ear_left_x", "Ear_left_y", "Ear_left_p", "Ear_right_x", "Ear_right_y",
                         "Ear_right_p", "Nose_x", "Nose_y", "Nose_p", "Tail_base_x",
                         "Tail_base_y", "Tail_base_p"]

        csv_df = read_df(currentFilePath=currentFile, wfileType=wfileType).fillna(0)
        csv_df.columns = columnHeaders

        #csv_df = csv_df.drop(csv_df.index[[0]])
        csv_df = csv_df.apply(pd.to_numeric).reset_index(drop=True)

        print('Evaluating convex hulls...')
        ########### MOUSE AREAS ###########################################
        ########### CREATE SHIFTED DATAFRAME FOR DISTANCE CALCULATIONS ###########################################
        csv_df_shifted = csv_df.shift(periods=1)
        csv_df_shifted = csv_df_shifted.rename(
            columns={'Ear_left_x': 'Ear_left_x_shifted', 'Ear_left_y': 'Ear_left_y_shifted',
                     'Ear_left_p': 'Ear_left_p_shifted', 'Ear_right_x': 'Ear_right_x_shifted', \
                     'Ear_right_y': 'Ear_right_y_shifted', 'Ear_right_p': 'Ear_right_p_shifted',
                     'Nose_x': 'Nose_x_shifted', 'Nose_y': 'Nose_y_shifted', \
                     'Nose_p': 'Nose_p_shifted', 'Tail_base_x': 'Tail_base_x_shifted',
                     'Tail_base_y': 'Tail_base_y_shifted', \
                     'Tail_base_p': 'Tail_base_p_shifted'})
        csv_df_combined = pd.concat([csv_df, csv_df_shifted], axis=1, join='inner').fillna(0).reset_index(drop=True)

        print('Calculating euclidean distances...')
        ########### EUCLIDEAN DISTANCES ###########################################
        csv_df['Mouse_nose_to_tail'] = (np.sqrt((csv_df.Nose_x - csv_df.Tail_base_x) ** 2 + (
                csv_df.Nose_y - csv_df.Tail_base_y) ** 2)) / currPixPerMM
        csv_df['Mouse_Ear_distance'] = (np.sqrt((csv_df.Ear_left_x - csv_df.Ear_right_x) ** 2 + (
                csv_df.Ear_left_y - csv_df.Ear_right_y) ** 2)) / currPixPerMM
        csv_df['Movement_mouse_nose'] = (np.sqrt(
            (csv_df_combined.Nose_x_shifted - csv_df_combined.Nose_x) ** 2 + (
                    csv_df_combined.Nose_y_shifted - csv_df_combined.Nose_y) ** 2)) / currPixPerMM
        csv_df['Movement_mouse_tail_base'] = (np.sqrt(
            (csv_df_combined.Tail_base_x_shifted - csv_df_combined.Tail_base_x) ** 2 + (
                    csv_df_combined.Tail_base_y_shifted - csv_df_combined.Tail_base_y) ** 2)) / currPixPerMM
        csv_df['Movement_mouse_left_ear'] = (np.sqrt(
            (csv_df_combined.Ear_left_x_shifted - csv_df_combined.Ear_left_x) ** 2 + (
                    csv_df_combined.Ear_left_y_shifted - csv_df_combined.Ear_left_y) ** 2)) / currPixPerMM
        csv_df['Movement_mouse_right_ear'] = (np.sqrt(
            (csv_df_combined.Ear_right_x_shifted - csv_df_combined.Ear_right_x) ** 2 + (
                    csv_df_combined.Ear_right_y_shifted - csv_df_combined.Ear_right_y) ** 2)) / currPixPerMM

        print('Calculating hull variables...')
        ########### HULL - EUCLIDEAN DISTANCES ###########################################
        for index, row in csv_df.iterrows():
            M1_np_array = np.array(
                [[row['Ear_left_x'], row["Ear_left_y"]], [row['Ear_right_x'], row["Ear_right_y"]],
                 [row['Nose_x'], row["Nose_y"]], [row['Tail_base_x'], row["Tail_base_y"]]]).astype(int)
            M1_dist_euclidean = scipy.spatial.distance.cdist(M1_np_array, M1_np_array, metric='euclidean')
            M1_dist_euclidean = M1_dist_euclidean[M1_dist_euclidean != 0]
            M1_hull_large_euclidean = np.amax(M1_dist_euclidean)
            M1_hull_small_euclidean = np.min(M1_dist_euclidean)
            M1_hull_mean_euclidean = np.mean(M1_dist_euclidean)
            M1_hull_sum_euclidean = np.sum(M1_dist_euclidean)
            M1_hull_large_euclidean_list.append(M1_hull_large_euclidean)
            M1_hull_small_euclidean_list.append(M1_hull_small_euclidean)
            M1_hull_mean_euclidean_list.append(M1_hull_mean_euclidean)
            M1_hull_sum_euclidean_list.append(M1_hull_sum_euclidean)
        csv_df['M1_largest_euclidean_distance_hull'] = list(
            map(lambda x: x / currPixPerMM, M1_hull_large_euclidean_list))
        csv_df['M1_smallest_euclidean_distance_hull'] = list(
            map(lambda x: x / currPixPerMM, M1_hull_small_euclidean_list))
        csv_df['M1_mean_euclidean_distance_hull'] = list(map(lambda x: x / currPixPerMM, M1_hull_mean_euclidean_list))
        csv_df['M1_sum_euclidean_distance_hull'] = list(map(lambda x: x / currPixPerMM, M1_hull_sum_euclidean_list))


        ########### COLLAPSED MEASURES ###########################################
        csv_df['Total_movement_all_bodyparts_M1'] = csv_df[
            'Movement_mouse_nose'] + csv_df['Movement_mouse_tail_base'] + \
                                                    csv_df['Movement_mouse_left_ear'] + csv_df[
                                                        'Movement_mouse_right_ear']

        ########### CALC ROLLING WINDOWS MEDIANS AND MEANS ###########################################
        print('Calculating rolling windows: medians, medians, and sums...')

        for i in range(len(roll_windows_values)):
            currentColName = 'Mouse1_mean_euclid_distances_median_' + str(roll_windows_values[i])
            csv_df[currentColName] = csv_df['M1_mean_euclidean_distance_hull'].rolling(roll_windows[i], min_periods=1).median()
            currentColName = 'Mouse1_mean_euclid_distances_mean_' + str(roll_windows_values[i])
            csv_df[currentColName] = csv_df['M1_mean_euclidean_distance_hull'].rolling(roll_windows[i],min_periods=1).mean()
            currentColName = 'Mouse1_mean_euclid_distances_sum_' + str(roll_windows_values[i])
            csv_df[currentColName] = csv_df['M1_mean_euclidean_distance_hull'].rolling(roll_windows[i], min_periods=1).sum()


        for i in range(len(roll_windows_values)):
            currentColName = 'Mouse1_smallest_euclid_distances_median_' + str(roll_windows_values[i])
            csv_df[currentColName] = csv_df['M1_smallest_euclidean_distance_hull'].rolling(roll_windows[i], min_periods=1).median()
            currentColName = 'Mouse1_smallest_euclid_distances_mean_' + str(roll_windows_values[i])
            csv_df[currentColName] = csv_df['M1_smallest_euclidean_distance_hull'].rolling(roll_windows[i],min_periods=1).mean()
            currentColName = 'Mouse1_smallest_euclid_distances_sum_' + str(roll_windows_values[i])
            csv_df[currentColName] = csv_df['M1_smallest_euclidean_distance_hull'].rolling(roll_windows[i], min_periods=1).sum()


        for i in range(len(roll_windows_values)):
            currentColName = 'Mouse1_largest_euclid_distances_median_' + str(roll_windows_values[i])
            csv_df[currentColName] = csv_df['M1_largest_euclidean_distance_hull'].rolling(roll_windows[i], min_periods=1).median()
            currentColName = 'Mouse1_largest_euclid_distances_mean_' + str(roll_windows_values[i])
            csv_df[currentColName] = csv_df['M1_largest_euclidean_distance_hull'].rolling(roll_windows[i],min_periods=1).mean()
            currentColName = 'Mouse1_largest_euclid_distances_sum_' + str(roll_windows_values[i])
            csv_df[currentColName] = csv_df['M1_largest_euclidean_distance_hull'].rolling(roll_windows[i], min_periods=1).sum()


        for i in range(len(roll_windows_values)):
            currentColName = 'Tail_base_movement_M1_median_' + str(roll_windows_values[i])
            csv_df[currentColName] = csv_df['Movement_mouse_tail_base'].rolling(roll_windows[i], min_periods=1).median()
            currentColName = 'Tail_base_movement_M1_mean_' + str(roll_windows_values[i])
            csv_df[currentColName] = csv_df['Movement_mouse_tail_base'].rolling(roll_windows[i], min_periods=1).mean()
            currentColName = 'Tail_base_movement_M1_sum_' + str(roll_windows_values[i])
            csv_df[currentColName] = csv_df['Movement_mouse_tail_base'].rolling(roll_windows[i], min_periods=1).sum()

        for i in range(len(roll_windows_values)):
            currentColName = 'Nose_movement_M1_median_' + str(roll_windows_values[i])
            csv_df[currentColName] = csv_df['Movement_mouse_nose'].rolling(roll_windows[i], min_periods=1).median()
            currentColName = 'Nose_movement_M1_mean_' + str(roll_windows_values[i])
            csv_df[currentColName] = csv_df['Movement_mouse_nose'].rolling(roll_windows[i], min_periods=1).mean()
            currentColName = 'Nose_movement_M1_sum_' + str(roll_windows_values[i])
            csv_df[currentColName] = csv_df['Movement_mouse_nose'].rolling(roll_windows[i], min_periods=1).sum()

        for i in range(len(roll_windows_values)):
            currentColName = 'Total_movement_M1_median_' + str(roll_windows_values[i])
            csv_df[currentColName] = csv_df['Total_movement_all_bodyparts_M1'].rolling(roll_windows[i], min_periods=1).median()
            currentColName = 'Total_movement_M1_mean_' + str(roll_windows_values[i])
            csv_df[currentColName] = csv_df['Total_movement_all_bodyparts_M1'].rolling(roll_windows[i], min_periods=1).mean()
            currentColName = 'Total_movement_M1_sum_' + str(roll_windows_values[i])
            csv_df[currentColName] = csv_df['Total_movement_all_bodyparts_M1'].rolling(roll_windows[i], min_periods=1).sum()

        ########### DEVIATIONS ###########################################
        print('Calculating deviations...')

        csv_df['Total_movement_all_bodyparts_deviation'] = (csv_df['Total_movement_all_bodyparts_M1'].mean() - csv_df['Total_movement_all_bodyparts_M1'])
        csv_df['M1_smallest_euclid_distances_hull_deviation'] = (csv_df['M1_smallest_euclidean_distance_hull'].mean() - csv_df['M1_smallest_euclidean_distance_hull'])
        csv_df['M1_largest_euclid_distances_hull_deviation'] = (csv_df['M1_largest_euclidean_distance_hull'].mean() - csv_df['M1_largest_euclidean_distance_hull'])
        csv_df['M1_mean_euclid_distances_hull_deviation'] = (csv_df['M1_mean_euclidean_distance_hull'].mean() - csv_df['M1_mean_euclidean_distance_hull'])


        for i in range(len(roll_windows_values)):
            currentColName = 'Mouse1_smallest_euclid_distances_mean_' + str(roll_windows_values[i])
            currentDev_colName = currentColName + '_deviation'
            csv_df[currentDev_colName] = (csv_df[currentColName].mean() - csv_df[currentColName])

        for i in range(len(roll_windows_values)):
            currentColName = 'Mouse1_largest_euclid_distances_mean_' + str(roll_windows_values[i])
            currentDev_colName = currentColName + '_deviation'
            csv_df[currentDev_colName] = (csv_df[currentColName].mean() - csv_df[currentColName])

        for i in range(len(roll_windows_values)):
            currentColName = 'Mouse1_mean_euclid_distances_mean_' + str(roll_windows_values[i])
            currentDev_colName = currentColName + '_deviation'
            csv_df[currentDev_colName] = (csv_df[currentColName].mean() - csv_df[currentColName])

        ########### PERCENTILE RANK ###########################################
        print('Calculating percentile ranks...')
        csv_df['Movement_mouse_nose_percentile_rank'] = csv_df['Movement_mouse_nose'].rank(pct=True)

        for i in range(len(roll_windows_values)):
            currentColName = 'Total_movement_M1_mean_' + str(roll_windows_values[i])
            currentDev_colName = currentColName + '_percentile_rank'
            csv_df[currentDev_colName] = (csv_df[currentColName].mean() - csv_df[currentColName])

        for i in range(len(roll_windows_values)):
            currentColName = 'Mouse1_mean_euclid_distances_mean_' + str(roll_windows_values[i])
            currentDev_colName = currentColName + '_percentile_rank'
            csv_df[currentDev_colName] = (csv_df[currentColName].mean() - csv_df[currentColName])

        for i in range(len(roll_windows_values)):
            currentColName = 'Mouse1_smallest_euclid_distances_mean_' + str(roll_windows_values[i])
            currentDev_colName = currentColName + '_percentile_rank'
            csv_df[currentDev_colName] = (csv_df[currentColName].mean() - csv_df[currentColName])

        for i in range(len(roll_windows_values)):
            currentColName = 'Mouse1_largest_euclid_distances_mean_' + str(roll_windows_values[i])
            currentDev_colName = currentColName + '_percentile_rank'
            csv_df[currentDev_colName] = (csv_df[currentColName].mean() - csv_df[currentColName])

        ########### CALCULATE STRAIGHTNESS OF POLYLINE PATH: tortuosity  ###########################################
        print('Calculating path tortuosities...')
        as_strided = np.lib.stride_tricks.as_strided
        win_size = 3
        centroidList_Mouse1_x = as_strided(csv_df.Nose_x, (len(csv_df) - (win_size - 1), win_size),
                                           (csv_df.Nose_x.values.strides * 2))
        centroidList_Mouse1_y = as_strided(csv_df.Nose_y, (len(csv_df) - (win_size - 1), win_size),
                                           (csv_df.Nose_y.values.strides * 2))

        for k in range(len(roll_windows_values)):
            start = 0
            end = start + int(roll_windows_values[k])
            tortuosity_M1 = []
            for y in range(len(csv_df)):
                tortuosity_List_M1 = []
                CurrCentroidList_Mouse1_x = centroidList_Mouse1_x[start:end]
                CurrCentroidList_Mouse1_y = centroidList_Mouse1_y[start:end]
                for i in range(len(CurrCentroidList_Mouse1_x)):
                    currMovementAngle_mouse1 = (
                        angle3pt(CurrCentroidList_Mouse1_x[i][0], CurrCentroidList_Mouse1_y[i][0],
                                 CurrCentroidList_Mouse1_x[i][1], CurrCentroidList_Mouse1_y[i][1],
                                 CurrCentroidList_Mouse1_x[i][2], CurrCentroidList_Mouse1_y[i][2]))
                    tortuosity_List_M1.append(currMovementAngle_mouse1)
                tortuosity_M1.append(sum(tortuosity_List_M1) / (2 * math.pi))
                start += 1
                end += 1
            currentColName1 = str('Tortuosity_Mouse1_') + str(roll_windows_values[k])
            csv_df[currentColName1] = tortuosity_M1

        ########### CALC THE NUMBER OF LOW PROBABILITY DETECTIONS & TOTAL PROBABILITY VALUE FOR ROW###########################################
        print('Calculating pose probability scores...')
        csv_df['Sum_probabilities'] = (csv_df['Ear_left_p'] + csv_df['Ear_right_p'] + csv_df['Nose_p'] + csv_df['Tail_base_p'])
        csv_df['Sum_probabilities_deviation'] = (csv_df['Sum_probabilities'].mean() - csv_df['Sum_probabilities'])
        csv_df['Sum_probabilities_deviation_percentile_rank'] = csv_df['Sum_probabilities_deviation'].rank(pct=True)
        csv_df['Sum_probabilities_percentile_rank'] = csv_df['Sum_probabilities_deviation_percentile_rank'].rank(
            pct=True)
        csv_df_probability = csv_df.filter(
            ['Ear_left_p', 'Ear_right_p', 'Nose_p', 'Tail_base_p'])
        values_in_range_min, values_in_range_max = 0.000000000, 0.1
        csv_df["Low_prob_detections_0.1"] = csv_df_probability.apply(
            func=lambda row: count_values_in_range(row, values_in_range_min, values_in_range_max), axis=1)
        values_in_range_min, values_in_range_max = 0.000000000, 0.5
        csv_df["Low_prob_detections_0.5"] = csv_df_probability.apply(
            func=lambda row: count_values_in_range(row, values_in_range_min, values_in_range_max), axis=1)
        values_in_range_min, values_in_range_max = 0.000000000, 0.75
        csv_df["Low_prob_detections_0.75"] = csv_df_probability.apply(
            func=lambda row: count_values_in_range(row, values_in_range_min, values_in_range_max), axis=1)

        csv_df = csv_df.reset_index(drop=True).fillna(0)
        if 'index' in csv_df.columns:
            csv_df = csv_df.drop(columns=['index'])
        saveFN = os.path.join(csv_dir_out, currVidName + '.' + wfileType)
        save_df(csv_df, wfileType, saveFN)
        print('Feature extraction complete for ' + '"' + str(currVidName) + '".')
    print('All feature extraction complete.')
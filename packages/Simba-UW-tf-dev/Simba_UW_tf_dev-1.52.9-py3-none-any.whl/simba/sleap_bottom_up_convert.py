import h5py
import pandas as pd
import json
import cv2
import os, glob
from pylab import *
import numpy as np
import operator
from functools import reduce
from configparser import ConfigParser, MissingSectionHeaderError, NoOptionError
import errno
import pyarrow.parquet as pq
import pyarrow as pa
import simba.rw_dfs
from simba.interpolate_pose import *
from simba.misc_tools import smooth_data_gaussian
from simba.drop_bp_cords import get_workflow_file_format

def importSLEAPbottomUP(inifile, dataFolder, currIDList, interpolation_method, smooth_settings_dict):

    def func(name, obj):
        attr = list(obj.attrs.items())
        if name == 'metadata':
            jsonList = (attr[1][1])
            jsonList = jsonList.decode('utf-8')
            final_dictionary = json.loads(jsonList)
            final_dictionary = dict(final_dictionary)
            return final_dictionary

    configFile = str(inifile)
    config = ConfigParser()
    try:
        config.read(configFile)
    except MissingSectionHeaderError:
        print('ERROR:  Not a valid project_config file. Please check the project_config.ini path.')
    projectPath = config.get('General settings', 'project_path')

    filesFound = glob.glob(dataFolder + '/*.slp')
    if len(filesFound) == 0: print('No SLP files found in ' + str(dataFolder))
    videoFolder = os.path.join(projectPath, 'videos')
    outputDfFolder = os.path.join(projectPath, 'csv', 'input_csv')
    wfileType = get_workflow_file_format(config)
    animalsNo = len(currIDList)
    bpNamesCSVPath = os.path.join(projectPath, 'logs', 'measures', 'pose_configs', 'bp_names', 'project_bp_names.csv')
    poseEstimationSetting = config.get('create ensemble settings', 'pose_estimation_body_parts')
    print('Converting .slp into dataframes...')
    csvPaths = []

    for filename in filesFound:
        print('Processing ' + str(os.path.basename(filename)) + '...')
        f = h5py.File(filename, 'r')
        bpNames, orderVarList, OrderedBpList, MultiIndexCol, dfHeader, csvFilesFound, colorList, xy_heads, bp_cord_names, bpNameList, projBpNameList = [], [], [], [], [], [], [], [], [], [], []
        final_dictionary = f.visititems(func)
        try:
            videoName = os.path.basename(final_dictionary['provenance']['video.path']).replace('.mp4', '')
        except KeyError:
            videoName = filename.replace('.slp', '')
            print('Warning: The video name could not be found in the .SLP meta-data table')
            print('SimBA therefore gives the imported CSV the same name as the SLP file.')
            print(
                'To be sure that SimBAs slp import function works, make sure the .SLP file and the associated video file has the same file name - e.g., "Video1.mp4" and "Video1.slp" before importing the videos and SLP files to SimBA.')
        savePath = os.path.join(outputDfFolder, videoName + '.csv')
        for bpName in final_dictionary['nodes']: bpNames.append((bpName['name']))
        skeletonOrder = final_dictionary['skeletons'][0]['nodes']
        for orderVar in skeletonOrder: orderVarList.append((orderVar['id']))
        for indexNo in orderVarList: OrderedBpList.append(bpNames[indexNo])

        with h5py.File(filename, 'r') as f:
            frames = f['frames'][:]
            instances = f['instances'][:]
            predicted_points = f['pred_points'][:]
            predicted_points = np.reshape(predicted_points, (predicted_points.size, 1))

        ### CREATE COLUMN IN DATAFRAME

        for animal in range(len(currIDList)):
            for bp in OrderedBpList:
                colName1, colName2, colName3 = str('Animal_' + str(animal + 1) + '_' + bp + '_x'), ('Animal_' + str(animal + 1) + '_' + bp + '_y'), ('Animal_' + str(animal + 1) + '_' + bp + '_p')
                xy_heads.extend((colName1, colName2))
                bp_cord_names.append('_' + bp + '_x')
                bp_cord_names.append('_' + bp + '_y')
                bpNameList.extend((colName1, colName2, colName3))
                dfHeader.extend((colName1, colName2, colName3))
        if poseEstimationSetting == 'user_defined':
            config.set("General settings", "animal_no", str(animalsNo))
            with open(inifile, "w+") as f:
                config.write(f)
            f.close()

        bpNameListGrouped = [xy_heads[x:x + len(OrderedBpList) * 2] for x in range(0, len(xy_heads) - 2, len(OrderedBpList) * 2)]
        dataDf = pd.DataFrame(columns=dfHeader)


        ### COUNT ANIMALS IN EACH FRAME
        animalsinEachFrame = []
        framesList = [l.tolist() for l in frames]
        for row in framesList:
            noAnimals = row[4] - row[3]
            animalsinEachFrame.append(noAnimals)

        noFrames = int(len(frames))
        frameCounter, instanceCounter, startCurrFrame = 0, 0, 0

        for frame in range(noFrames):
            animalsinCurrFrame = animalsinEachFrame[frame]
            endCurrFrame = startCurrFrame + (len(OrderedBpList) * animalsinCurrFrame)
            currStartAnimal, currEndAnimal = 0, len(OrderedBpList)
            currFrameNp = predicted_points[startCurrFrame:endCurrFrame]
            currRow = []
            for animal in range(animalsinCurrFrame):
                currAnimalNp = currFrameNp[currStartAnimal:currEndAnimal]
                currTrackID = int(instances[instanceCounter][4])
                for bp in currAnimalNp:
                    currX, currY, currP = bp[0][0], bp[0][1], bp[0][4]
                    currRow.extend((currX, currY, currP))
                currRow.append(currTrackID)
                currNpRow = np.array_split(currRow, animalsinCurrFrame)
                currNpRow = [l.tolist() for l in currNpRow]
                currNpRow = sorted(currNpRow, key=operator.itemgetter(-1))
                outRow = reduce(operator.concat, currNpRow)
                instanceCounter += 1
                currStartAnimal += len(OrderedBpList)
                currEndAnimal += len(OrderedBpList)

            if animalsinCurrFrame == 0:
                outRow = [0] * len(dfHeader)

            else:
                ### check if all animals exist
                splitOutRow = np.array_split(outRow, animalsinCurrFrame)
                splitOutRow = [l.tolist() for l in splitOutRow]
                for newValue in range(len(splitOutRow)):
                    splitOutRow[newValue][-1] = newValue
                animalsExist = []
                for animalList in splitOutRow:
                    animalsExist.append(animalList[-1])
                missingVals = [ele for ele in range(animalsNo) if ele not in animalsExist]
                for val in missingVals:
                    list2Append = [0] * ((len(OrderedBpList))) * 3
                    list2Append.append((int(val)))
                    splitOutRow.append(list2Append)
                for row in splitOutRow:
                    del row[-1]
                outRow = reduce(operator.concat, splitOutRow)

            dataDf.loc[len(dataDf)] = outRow
            startCurrFrame = endCurrFrame
            frameCounter += 1

        dataDf.fillna(0, inplace=True)
        simba.rw_dfs.save_df(dataDf, wfileType, savePath)
        csvPaths.append(savePath)

    ###### ASSIGN IDENTITIES

    global currIDcounter

    def define_ID(event, x, y, flags, param):
        global currIDcounter
        if (event == cv2.EVENT_LBUTTONDBLCLK):
            centerX, centerY, currID = (int(x), int(y), currIDList[currIDcounter])
            ID_user_cords.append([centerX, centerY, currIDList[currIDcounter]])
            cv2.putText(overlay, str(currID), (centerX, centerY), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 255, 0), 5)
            currIDcounter += 1

    cmap = cm.get_cmap(str('tab10'), animalsNo + 1)
    for i in range(cmap.N):
        rgb = list((cmap(i)[:3]))
        rgb = [i * 255 for i in rgb]
        rgb.reverse()
        colorList.append(rgb)

    for csvFile in csvPaths:
        indBpCordList, frameNumber, addSpacer, EuclidDistanceList, changeList = [], 0, 2, [], []
        ID_user_cords, currIDcounter = [], 0
        all_animals_missing, assigningIDs, completePromt, chooseFrame, assignBpCords = False, False, False, True, True
        currDf = simba.rw_dfs.read_df(csvFile, wfileType)
        vidFname = os.path.join(videoFolder, os.path.basename(csvFile).replace('.csv', '.mp4'))
        vidBasename = os.path.basename(vidFname)
        if not os.path.exists(vidFname):
            # print('Please import ' + str(vidBasename) + ' to your SimBA project.')
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), vidFname)
        cap = cv2.VideoCapture(vidFname)
        if not cap.isOpened():
            raise Exception('Can\'t open video file ' + vidFname)
        width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        mySpaceScale, myRadius, myResolution, myFontScale = 40, 10, 1500, 1.2
        maxResDimension = max(width, height)
        circleScale, fontScale, spacingScale = int(myRadius / (myResolution / maxResDimension)), float(
            myFontScale / (myResolution / maxResDimension)), int(mySpaceScale / (myResolution / maxResDimension))
        cv2.namedWindow('Define animal IDs', cv2.WINDOW_NORMAL)

        while (1):
            if ((chooseFrame == True) and (assignBpCords == True)) or (all_animals_missing == True):
                cv2.namedWindow('Define animal IDs', cv2.WINDOW_NORMAL)
                cap.set(1, frameNumber)
                ret, frame = cap.read()
                if not ret:
                    raise Exception('Can\'t read video file ' + vidFname)
                overlay = frame.copy()
                all_x_y_cords = []
                for animal_bps in range(len(bpNameListGrouped)):
                    currCols = bpNameListGrouped[animal_bps]
                    currcolor = tuple(colorList[animal_bps])
                    for ind_bp_cords in range(0, len(currCols), 2):
                        y_cord = currDf.loc[currDf.index[frameNumber], currCols[ind_bp_cords + 1]]
                        x_cord = currDf.loc[currDf.index[frameNumber], currCols[ind_bp_cords]]
                        all_x_y_cords.extend((int(x_cord), int(y_cord)))
                        indBpCordList.append([x_cord, y_cord, currCols[ind_bp_cords]])
                        cv2.circle(overlay, (int(x_cord), int(y_cord)), circleScale, currcolor, -1,
                                   lineType=cv2.LINE_AA)
                    loop = 0
                    for name in indBpCordList:
                        currstring = name[2]
                        for substring in bp_cord_names:
                            if substring in currstring:
                                newstring = currstring.replace(substring, '')
                                indBpCordList[loop][2] = newstring
                        loop += 1
                imWithCordsOnly = overlay.copy()
                if len(set(all_x_y_cords)) == 1:
                    all_animals_missing, frameNumber = True, frameNumber + 50
                if len(set(all_x_y_cords)) > 1:
                    all_animals_missing = False
                    chooseFrame = False
            if (chooseFrame == False) and (assignBpCords == True) and (all_animals_missing == False):
                sideImage = np.ones((int(height / 2), width, 3))
                cv2.putText(sideImage, 'Current video: ' + str(vidBasename), (10, int(spacingScale)),
                            cv2.FONT_HERSHEY_SIMPLEX, fontScale, (255, 255, 255), 3)
                cv2.putText(sideImage, 'Can you assign identities based on the displayed frame ?',
                            (10, int(spacingScale * (addSpacer * 2))), cv2.FONT_HERSHEY_SIMPLEX, fontScale,
                            (255, 255, 255), 3)
                cv2.putText(sideImage, 'Press "x" to display new, random, frame',
                            (10, int(spacingScale * (addSpacer * 3))), cv2.FONT_HERSHEY_SIMPLEX, fontScale,
                            (255, 255, 0), 3)
                cv2.putText(sideImage, 'Press "c" to continue to start assigning identities using this frame',
                            (10, int(spacingScale * (addSpacer * 4))), cv2.FONT_HERSHEY_SIMPLEX, fontScale, (0, 255), 3)
                imageConcat = np.concatenate((overlay, sideImage), axis=0)
                imageConcat = np.uint8(imageConcat)
                cv2.imshow('Define animal IDs', imageConcat)
                k = cv2.waitKey(10)
                if k == ord('x'):
                    cv2.destroyWindow('Define animal IDs')
                    chooseFrame, assignBpCords = True, True
                    frameNumber += 50
                elif k == ord('c'):
                    chooseFrame, assignBpCords = False, False
                    assigningIDs, completePromt, assigningIDs = True, False, True

            if assigningIDs == True:
                sideImage = np.ones((int(height / 2), width, 3))
                cv2.putText(sideImage, 'Double left mouse click on:', (10, int(spacingScale)), cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale, (255, 255, 255), 3)
                cv2.putText(sideImage, str(currIDList[currIDcounter]), (10, int(spacingScale * (addSpacer * 2))),
                            cv2.FONT_HERSHEY_SIMPLEX, fontScale, (255, 255, 0), 3)
                imageConcat = np.concatenate((overlay, sideImage), axis=0)
                imageConcat = np.uint8(imageConcat)
                cv2.setMouseCallback('Define animal IDs', define_ID)
                cv2.imshow('Define animal IDs', imageConcat)
                cv2.waitKey(10)
                if currIDcounter >= len(currIDList):
                    cv2.destroyWindow('Define animal IDs')
                    assigningIDs, completePromt = False, True

            if completePromt == True:
                cv2.namedWindow('Define animal IDs', cv2.WINDOW_NORMAL)
                sideImage = np.ones((int(height / 2), width, 3))
                cv2.putText(sideImage, 'Current video: ' + str(vidBasename), (10, int(spacingScale)),
                            cv2.FONT_HERSHEY_SIMPLEX, fontScale, (255, 255, 255), 3)
                cv2.putText(sideImage, 'Are you happy with your assigned identities ?',
                            (10, int(spacingScale * (addSpacer * 2))), cv2.FONT_HERSHEY_SIMPLEX, fontScale,
                            (255, 255, 255), 3)
                cv2.putText(sideImage, 'Press "c" to continue (to finish, or proceed to the next video)',
                            (10, int(spacingScale * (addSpacer * 3))), cv2.FONT_HERSHEY_SIMPLEX, fontScale,
                            (255, 255, 0), 3)
                cv2.putText(sideImage, 'Press "x" to re-start assigning identities',
                            (10, int(spacingScale * (addSpacer * 4))), cv2.FONT_HERSHEY_SIMPLEX, fontScale,
                            (0, 255, 255), 3)
                imageConcat = np.concatenate((overlay, sideImage), axis=0)
                imageConcat = np.uint8(imageConcat)
                cv2.imshow('Define animal IDs', imageConcat)
                k = cv2.waitKey(10)
                if k == ord('c'):
                    cv2.destroyWindow('Define animal IDs')
                    break
                if k == ord('x'):
                    overlay = imWithCordsOnly.copy()
                    ID_user_cords, currIDcounter = [], 0
                    assigningIDs, completePromt = True, False

        print('Re-organizing pose data-frame based on user-assigned identities: ' + str(os.path.basename(vidFname)) + '....')

        for values in ID_user_cords:
            currClickedX, currClickedY, currClickedID = values[0], values[1], values[2]
            for bpCords in indBpCordList:
                currX, currY, ID = bpCords[0], bpCords[1], bpCords[2]
                currEuclidian = np.sqrt((currClickedX - currX) ** 2 + (currClickedY - currY) ** 2)
                EuclidDistanceList.append([currEuclidian, currClickedID, ID])
        euclidDf = pd.DataFrame(EuclidDistanceList)
        euclidDf.columns = ['Distance', 'clickID', 'pose_ID']
        for i in currIDList:
            minDistance = euclidDf.loc[euclidDf['clickID'] == i, 'Distance'].min()
            animalPoseID = euclidDf.loc[euclidDf['Distance'] == minDistance, 'pose_ID'].iloc[0]
            changeList.append([animalPoseID, i])
        for animal in changeList:
            currPoseName, newName = animal[0], animal[1]
            for loop, header in enumerate(bpNameList):
                if header.startswith(currPoseName):
                    newHeader = header.replace(currPoseName, newName)
                    bpNameList[loop] = newHeader

        currDf.columns = bpNameList
        outDf = pd.DataFrame()
        column_names_lst = currDf.columns


        for animal_name in currIDList:
            currCols = []
            for col_name in column_names_lst:
                col_name_split = col_name.split('_')[0]
                if animal_name.lower() == col_name_split.lower():
                    currCols.append(col_name)
            sliceDf = currDf[currCols]
            outDf = pd.concat([outDf, sliceDf], axis=1)
        outDfcols = list(outDf.columns)
        toBpCSVlist = []

        if poseEstimationSetting == 'user_defined':
            for i in outDfcols:
                currBpName = i[:-2]
                bp_name_parts = currBpName.split('_')
                for identityNo in range(len(currIDList)):
                    if str(currIDList[identityNo]) == bp_name_parts[0]:
                        currBpName = currBpName + '_' + str(identityNo + 1)
                toBpCSVlist.append(currBpName) if currBpName not in toBpCSVlist else toBpCSVlist
            newCSVlist_df = pd.DataFrame(toBpCSVlist)
            newCSVlist_df.to_csv(bpNamesCSVPath, index=False, header=False)

        MultiIndexCol = []
        for column in range(len(outDf.columns)):
            MultiIndexCol.append(tuple(('SLEAP_multi', 'SLEAP_multi', outDf.columns[column])))
        outDf.columns = pd.MultiIndex.from_tuples(MultiIndexCol, names=['scorer', 'bodypart', 'coords'])
        outputCSVname = os.path.basename(vidFname).replace('.mp4', '.' + wfileType)
        if wfileType == 'csv':
            outDf.to_csv(os.path.join(outputDfFolder, outputCSVname))
        if wfileType == 'parquet':
            table = pa.Table.from_pandas(outDf)
            pq.write_table(table, os.path.join(outputDfFolder, outputCSVname))

        if interpolation_method != 'None':
            print('Interpolating missing values (Method: ' + str(interpolation_method) + ') ...')
            if wfileType == 'parquet':
                csv_df = pd.read_parquet(os.path.join(outputDfFolder, outputCSVname))
            if wfileType == 'csv':
                csv_df = pd.read_csv(os.path.join(outputDfFolder, outputCSVname), index_col=0)
            interpolate_body_parts = Interpolate(inifile, csv_df)
            interpolate_body_parts.detect_headers()
            interpolate_body_parts.fix_missing_values(interpolation_method)
            interpolate_body_parts.reorganize_headers()
            if wfileType == 'parquet':
                table = pa.Table.from_pandas(interpolate_body_parts.new_df)
                pq.write_table(table, os.path.join(outputDfFolder, outputCSVname))
            if wfileType == 'csv':
                interpolate_body_parts.new_df.to_csv(os.path.join(outputDfFolder, outputCSVname))

        if smooth_settings_dict['Method'] == 'Gaussian':
            time_window = smooth_settings_dict['Parameters']['Time_window']
            smooth_data_gaussian(config=config, file_path=os.path.join(outputDfFolder, outputCSVname), time_window_parameter=time_window)


        print('Imported ', outputCSVname, 'to project.')
    print('All multi-animal SLEAP .slp tracking files ordered and imported into SimBA project in chosen workflow file format')




# importSLEAPbottomUP(r"Z:\DeepLabCut\DLC_extract\Troubleshooting\Parquet_test2\project_folder\project_config.ini",
#                     r"Z:\DeepLabCut\DLC_extract\Troubleshooting\Parquet_test2\import_2",
#                     ["female", "male"],
#                     "Animals(s): Nearest",
#                     {'Method': 'None', 'Parameters': {'Time_window': '200'}})


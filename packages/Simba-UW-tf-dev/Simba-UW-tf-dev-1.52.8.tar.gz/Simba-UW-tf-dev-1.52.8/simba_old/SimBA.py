__author__ = "Simon Nilsson", "JJ Choong"

import warnings
warnings.filterwarnings('ignore',category=FutureWarning)
warnings.filterwarnings('ignore',category=DeprecationWarning)
import csv
from tkinter.filedialog import askopenfilename,askdirectory
from tkinter import tix, messagebox
from PIL import ImageTk
import PIL.Image
import tkinter.ttk as ttk
import webbrowser
from simba.plotly_create_h5 import *
from simba.tkinter_functions import (DropDownMenu,
                                     Entry_Box,
                                     FileSelect,
                                     FolderSelect)
from simba.project_config_creator import ProjectConfigCreator
from simba.import_mars import MarsImporter
from simba.probability_graph_interactive import InteractiveProbabilityGrapher
from simba.Validate_model_one_video_run_clf import ValidateModelRunClf
from simba.cue_light_tools.cue_light_menues import CueLightAnalyzerMenu
from simba.import_videos_csv_project_ini import *
from simba.machine_model_settings_pop_up import MachineModelSettingsPopUp
from simba.process_severity import analyze_process_severity
from simba.validate_model_on_single_video import ValidateModelOneVideo
from simba.outlier_scripts.outlier_corrector_movement import OutlierCorrecterMovement
from simba.outlier_scripts.outlier_corrector_location import OutlierCorrecterLocation
from simba.outlier_scripts.skip_outlier_correction import OutlierCorrectionSkipper
from simba.features_scripts.feature_extractor_16bp import ExtractFeaturesFrom16bps
from simba.features_scripts.feature_extractor_14bp import ExtractFeaturesFrom14bps
from simba.features_scripts.extract_features_14bp_from_16bp import extract_features_wotarget_14_from_16
from simba.features_scripts.extract_features_9bp import extract_features_wotarget_9
from simba.features_scripts.feature_extractor_8bp import ExtractFeaturesFrom8bps
from simba.features_scripts.feature_extractor_8bps_2_animals import ExtractFeaturesFrom8bps2Animals
from simba.features_scripts.feature_extractor_7bp import ExtractFeaturesFrom7bps
from simba.features_scripts.feature_extractor_4bp import ExtractFeaturesFrom4bps
from simba.features_scripts.feature_extractor_user_defined import UserDefinedFeatureExtractor
from simba.BENTO_appender import BentoAppender
from simba.dlc_multi_animal_importer import MADLC_Importer
from simba.BORIS_appender import BorisAppender
from simba.Directing_animals_analyzer import DirectingOtherAnimalsAnalyzer
from simba.solomon_importer import SolomonImporter
from simba.import_trk import *
from simba.classifications_per_ROI import *
from simba.read_DANNCE_mat import import_DANNCE_file, import_DANNCE_folder
from simba.ethovision_import import ImportEthovision
from simba.sleap_import_new import ImportSLEAP
from simba.sleap_csv_importer import SleapCsvImporter
from simba.train_single_model import TrainSingleModel
from simba.train_mutiple_models_from_meta_new import TrainMultipleModelsFromMeta
from simba.run_model_new import RunModel
import urllib.request
from cefpython3 import cefpython as cef
import threading
import atexit
from simba.batch_process_videos.batch_process_menus import BatchProcessFrame
from simba.video_info_table import VideoInfoTable
from simba.read_config_unit_tests import check_int
from simba.roi_tools.ROI_define import *
from simba.roi_tools.ROI_menus import *
from simba.roi_tools.ROI_reset import *
from simba.misc_tools import (smooth_data_gaussian,
                              smooth_data_savitzky_golay,
                              copy_single_video_to_project,
                              copy_multiple_videos_to_project,
                              run_user_defined_feature_extraction_class)
from simba.video_processing import (video_to_greyscale,
                                    superimpose_frame_count)
from simba.sleap_importer import SLEAPImporterH5
from simba.setting_menu import SettingsMenu
from simba.pop_up_classes import (HeatmapLocationPopup,
                                  QuickLineplotPopup,
                                  ClfByROIPopUp,
                                  FSTTCPopUp,
                                  KleinbergPopUp,
                                  TimeBinsClfPopUp,
                                  ClfDescriptiveStatsPopUp,
                                  DownsampleVideoPopUp,
                                  CLAHEPopUp,
                                  CropVideoPopUp,
                                  ClipVideoPopUp,
                                  MultiShortenPopUp,
                                  ChangeImageFormatPopUp,
                                  ConvertVideoPopUp,
                                  ExtractSpecificFramesPopUp,
                                  ExtractAllFramesPopUp,
                                  Csv2ParquetPopUp,
                                  Parquet2CsvPopUp,
                                  MultiCropPopUp,
                                  ChangeFpsSingleVideoPopUp,
                                  ChangeFpsMultipleVideosPopUp,
                                  ExtractSEQFramesPopUp,
                                  MergeFrames2VideoPopUp,
                                  PrintModelInfoPopUp,
                                  CreateGIFPopUP,
                                  CalculatePixelsPerMMInVideoPopUp,
                                  PoseReorganizerPopUp,
                                  MakePathPlotPopUp,
                                  AboutSimBAPopUp,
                                  ConcatenatingVideosPopUp,
                                  VisualizePoseInFolderPopUp,
                                  DropTrackingDataPopUp,
                                  ConcatenatorPopUp,
                                  SetMachineModelParameters,
                                  OutlierSettingsPopUp,
                                  RemoveAClassifierPopUp,
                                  VisualizeROIFeaturesPopUp,
                                  VisualizeROITrackingPopUp,
                                  CreateUserDefinedPoseConfigurationPopUp,
                                  PoseResetterPopUp,
                                  SklearnVisualizationPopUp,
                                  GanttPlotPopUp,
                                  VisualizeClassificationProbabilityPopUp,
                                  PathPlotPopUp,
                                  DistancePlotterPopUp,
                                  HeatmapClfPopUp,
                                  DataPlotterPopUp,
                                  DirectingOtherAnimalsVisualizerPopUp,
                                  PupRetrievalPopUp,
                                  ClassifierValidationPopUp,
                                  AnalyzeSeverityPopUp,
                                  ImportFrameDirectoryPopUp,
                                  AddClfPopUp,
                                  ArchiveProcessedFilesPopUp,
                                  InterpolatePopUp,
                                  SmoothingPopUp)
from simba.bounding_box_tools.boundary_menus import BoundaryMenus
from simba.labelling_interface import select_labelling_video
from simba.labelling_advanced_interface import select_labelling_video_advanced
from simba.deepethogram_importer import DeepEthogramImporter
from simba.enums import Formats, Options
from simba.mixins.pop_up_mixin import PopUpMixin
import sys

sys.setrecursionlimit(10 ** 6)
simBA_version = 1.2
currentPlatform = platform.system()

class BatchPreProcessWindow(object):
    def __init__(self):
        batchprocess = Toplevel()
        batchprocess.minsize(400, 200)
        batchprocess.wm_title("Batch process video")
        label_videoselection = LabelFrame(batchprocess,text='Folder selection',font='bold',padx=5,pady=5)
        self.input_folder = FolderSelect(label_videoselection,'Video directory:',title='Select Folder with Input Videos')

        #output video
        self.output_folder = FolderSelect(label_videoselection,'Output directory:',title='Select Folder for Output videos')

        confirm_btn = Button(label_videoselection,text='Confirm',command=lambda: self.confirm_table())

        #organize
        label_videoselection.grid(row=0,sticky=W)
        self.input_folder.grid(row=0,sticky=W)
        self.output_folder.grid(row=1,sticky=W)
        confirm_btn.grid(row=2,sticky=W)

    def confirm_table(self):
        if (self.output_folder.folder_path=='No folder selected'):
            print('SIMBA ERROR: Please select an "Output directory"')
        elif (self.input_folder.folder_path == 'No folder selected'):
            print('SIMBA ERROR: Please select an "Input video directory"')
        elif (self.output_folder.folder_path == self.input_folder.folder_path):
            print('SIMBA ERROR: The input directory and output directory CANNOT be the same folder')
        else:
            batch_preprocessor = BatchProcessFrame(input_dir=self.input_folder.folder_path, output_dir=self.output_folder.folder_path)
            batch_preprocessor.create_main_window()
            batch_preprocessor.create_video_table_headings()
            batch_preprocessor.create_video_rows()
            batch_preprocessor.create_execute_btn()
            batch_preprocessor.batch_process_main_frame.mainloop()

class LoadProjectPopUp(object):
    def __init__(self):
        main_frm = Toplevel()
        main_frm.minsize(300, 200)
        main_frm.wm_title("Load SimBA project (project_config.ini file)")
        load_project_frm = LabelFrame(main_frm, text='LOAD SIMBA PROJECT_CONFIG.INI', font=("Helvetica", 12, 'bold'), pady=5, padx=5, fg='black')
        self.selected_file = FileSelect(load_project_frm,'Select file: ', title='Select project_config.ini file')
        load_project_btn = Button(load_project_frm, text='LOAD PROJECT', font=("Helvetica", 12, 'bold'), command=lambda: self.launch_project())

        load_project_frm.grid(row=0)
        self.selected_file.grid(row=0,sticky=NW)
        load_project_btn.grid(row=1,pady=10, sticky=NW)

    def launch_project(self):
        print('Loading {}...'.format(self.selected_file.file_path))
        check_file_exist_and_readable(file_path=self.selected_file.file_path)
        _ = ProjectPopUp(config_path=self.selected_file.file_path)

def Exit():
    app.root.destroy()

class create_project_DLC:

    def __init__(self):

        # Popup window
        createproject = Toplevel()
        createproject.minsize(400, 250)
        createproject.wm_title("Create Project")


        self.label_dlc_createproject = LabelFrame(createproject,text='Create Project',font=Formats.LABELFRAME_HEADER_FORMAT.value)
        #project name
        self.label_projectname = Entry_Box(self.label_dlc_createproject,'Project name','16')

        #Experimenter name
        self.label_experimentername = Entry_Box(self.label_dlc_createproject,'Experimenter name','16')

        #button 1
        button_videofol = Button(self.label_dlc_createproject,text='Import Single Video',command=self.changetovideo2,fg='blue')
        #button 2
        button_videofo2 = Button(self.label_dlc_createproject,text='Import Multiple Videos',command=self.changetovideo,fg='green4')

        # Video Path
        self.videopath1selected = FolderSelect(self.label_dlc_createproject, 'Video Folder          ',title='Select folder with videos',color='green4')
        self.videopath1selected.grid(row=4, sticky=W)

        #video folder
        self.folderpath1selected = FolderSelect(self.label_dlc_createproject,'Project directory   ',title='Select main directory')

        #bodypart configuration file
        self.bodypartconfigfile = FileSelect(self.label_dlc_createproject, 'Bp config file ', title='Select a csv file')

        #checkbox_apply golden aggresion config yaml settings
        self.var_changeyaml = IntVar()
        checkbox2 = Checkbutton(self.label_dlc_createproject,text='Apply Golden Lab 16-body part config',variable=self.var_changeyaml)

        #checkbox for copy videos true or false
        self.var_copyvid = IntVar()
        checkbox1 = Checkbutton(self.label_dlc_createproject,text='Copy videos (If unchecked, shortcuts are created)',variable=self.var_copyvid)

        #run create project
        button_createproject = Button(self.label_dlc_createproject,text='Create Project',fg='red',command=self.createprojectcommand)

        #organize
        self.label_dlc_createproject.grid(row=0)
        self.label_projectname.grid(row=0,column=0,sticky=W)
        self.label_experimentername.grid(row=1,column=0,sticky=W)
        button_videofol.grid(row=2,sticky=W,pady=5)
        button_videofo2.grid(row=3,sticky=W,pady=5)
        self.folderpath1selected.grid(row=5,sticky=W)
        self.bodypartconfigfile.grid(row=6, sticky=W)
        checkbox2.grid(row=7,column=0,sticky=W)
        checkbox1.grid(row=8,sticky=W)
        button_createproject.grid(row=9,column=3,pady=10,padx=5)

    def changetovideo(self):
        self.videopath1selected.grid_remove()
        self.videopath1selected = FolderSelect(self.label_dlc_createproject, 'Video Folder          ',title='Select folder with videos',color='green4')
        self.videopath1selected.grid(row=4, sticky=W)


    def changetovideo2(self):
        self.videopath1selected.grid_remove()
        self.videopath1selected = FileSelect(self.label_dlc_createproject, 'Video path             ',color='blue',title='Select a video file')
        self.videopath1selected.grid(row=4, sticky=W)

    def createprojectcommand(self):
        projectname = self.label_projectname.entry_get
        experimentalname = self.label_experimentername.entry_get
        if self.var_copyvid.get()==1:
            copyvid = True
        elif self.var_copyvid.get()==0:
            copyvid = False

        if 'FileSelect' in str(type(self.videopath1selected)):
            videolist = [self.videopath1selected.file_path]
        else:
            try:
                videolist = []

                for i in os.listdir(self.videopath1selected.folder_path):
                    if ('.avi' or '.mp4') in i:
                        i = os.path.join(self.videopath1selected.folder_path, i)
                        videolist.append(i)
            except:
                print('Please select a video folder to import videos')

        if 'FileSelect' in str(type(self.bodypartconfigfile)):
            bodyPartConfigFile = (self.bodypartconfigfile.file_path)


        if self.var_changeyaml.get()==1:
            if (projectname !='') and (experimentalname !='') and ('No'and'selected' not in videolist) and (self.folderpath1selected.folder_path!='No folder selected'):
                config_path = deeplabcut.create_new_project(str(projectname), str(experimentalname), videolist,working_directory=str(self.folderpath1selected.folder_path), copy_videos=copyvid)
                changedlc_config(config_path, 0)
            else:
                print('Please make sure all the information are filled in')
        else:
            if (projectname != '') and (experimentalname != '') and ('No' and 'selected' not in videolist) and (self.folderpath1selected.folder_path != 'No folder selected'):
                config_path = deeplabcut.create_new_project(str(projectname), str(experimentalname), videolist,working_directory=str(self.folderpath1selected.folder_path), copy_videos=copyvid)
            else:
                print('Please make sure all the information are filled in')
        if bodyPartConfigFile != 'No file selected':
            changedlc_config(config_path, bodyPartConfigFile)

class project_config:

    def __init__(self):
        self.all_entries = []
        self.allmodels = []
        # Popup window
        self.toplevel = Toplevel()
        self.toplevel.minsize(750, 750)
        self.toplevel.wm_title("Project Configuration")

        #tab
        tab_parent = ttk.Notebook(hxtScrollbar(self.toplevel))
        tab1 = ttk.Frame(tab_parent)
        tab2 = ttk.Frame(tab_parent)
        tab3 = ttk.Frame(tab_parent)
        tab4 = ttk.Frame(tab_parent)
        #tab title
        tab_parent.add(tab1,text=f'{"[ Generate project config ]": ^20s}')
        tab_parent.add(tab2, text=f'{"[ Import videos into project folder ]": ^20s}')
        tab_parent.add(tab3, text=f'{"[ Import tracking data ]": ^20s}')
        tab_parent.add(tab4, text=f'{"[ Extract frames into project folder ]": ^20s}')
        #initiate tab
        tab_parent.grid(row=0)

        # General Settings
        self.label_generalsettings = LabelFrame(tab1, text='General Settings',fg='black',font =Formats.LABELFRAME_HEADER_FORMAT.value,padx=5,pady=5)
        self.directory1Select = FolderSelect(self.label_generalsettings, "Project Path:", title='Select Main Directory',lblwidth='12')
        self.label_project_name = Entry_Box(self.label_generalsettings, 'Project Name:',labelwidth='12')
        label_project_namedescrip = Label(self.label_generalsettings, text='(project name cannot contain spaces)')
        self.csvORparquet = DropDownMenu(self.label_generalsettings,'Workflow file type',['csv','parquet'],'15')
        self.csvORparquet.setChoices('csv')

        #SML Settings
        self.label_smlsettings = LabelFrame(self.label_generalsettings, text='SML Settings',padx=5,pady=5)
        self.label_notarget = Entry_Box(self.label_smlsettings,'Number of predictive classifiers (behaviors):','33', validation='numeric')
        addboxButton = Button(self.label_smlsettings, text='<Add predictive classifier>', fg="navy",  command=lambda:self.addBox(self.label_notarget.entry_get))

        ##dropdown for # of mice
        #self.dropdownbox = TrackingSelectorMenu(main_frm=)
        self.dropdownbox = LabelFrame(self.label_generalsettings, text='Animal Settings')


        ## choose multi animal or not
        self.singleORmulti = DropDownMenu(self.dropdownbox,'Type of Tracking',['Classic tracking','Multi tracking', '3D tracking'],'15', com=self.trackingselect)
        self.singleORmulti.setChoices('Classic tracking')

        #choice
        self.frame2 = Frame(self.dropdownbox)

        label_dropdownmice = Label(self.frame2, text='# config')
        self.option_mice, optionsBasePhotosList = bodypartConfSchematic()

        # del multi animal
        del self.option_mice[9:13]
        del optionsBasePhotosList[9:13]

        self.var = StringVar()
        self.var.set(self.option_mice[6])
        micedropdown = OptionMenu(self.frame2, self.var, *self.option_mice)

        self.var.trace("w", self.change_image)

        self.photos = []
        for i in range(len(optionsBasePhotosList)):
            self.photos.append(PhotoImage(file=os.path.join(os.path.dirname(__file__),(optionsBasePhotosList[i]))))

        self.label = Label(self.frame2, image=self.photos[6])
        self.label.grid(row=10,sticky=W,columnspan=2)
        #reset button
        resetbutton = Button(self.frame2,text='Reset user-defined pose configs', command=lambda: PoseResetterPopUp())
        #organize
        self.singleORmulti.grid(row=0,sticky=W)
        self.frame2.grid(row=1,sticky=W)
        label_dropdownmice.grid(row=0,column=0,sticky=W)
        micedropdown.grid(row=0,column=1,sticky=W)
        self.label.grid(row=1,sticky=W,columnspan=2)
        resetbutton.grid(row=0,sticky=W,column=2)

        #generate project ini
        button_generateprojectini = Button(self.label_generalsettings, text='CREATE PROJECT CONFIG', command=self.make_projectini, font=("Helvetica",12,'bold'),fg='navy')

        #####import videos
        label_importvideo = LabelFrame(tab2, text='Import Videos into project folder',fg='black', font=Formats.LABELFRAME_HEADER_FORMAT.value, padx=15, pady=5)
        # multi video
        label_multivideoimport = LabelFrame(label_importvideo, text='Import multiple videos', pady=5, padx=5)
        self.multivideofolderpath = FolderSelect(label_multivideoimport, 'Folder path',title='Select Folder with videos')
        self.video_type = Entry_Box(label_multivideoimport, 'Format (i.e., mp4, avi):', '18')
        button_multivideoimport = Button(label_multivideoimport, text='Import multiple videos',command= self.import_multivid,fg='navy')

        # singlevideo
        label_singlevideoimport = LabelFrame(label_importvideo, text='Import single video', pady=5, padx=5)
        self.singlevideopath = FileSelect(label_singlevideoimport, "Video path",title='Select a video file')
        button_importsinglevideo = Button(label_singlevideoimport, text='Import a video',command= self.import_singlevid,fg='navy')


        #import all csv file into project folder
        self.label_import_csv = LabelFrame(tab3,text='Import Tracking Data',fg='black',font=Formats.LABELFRAME_HEADER_FORMAT.value,pady=5,padx=5)
        self.filetype = DropDownMenu(self.label_import_csv,'File type',['CSV (DLC/DeepPoseKit)','JSON (BENTO)','H5 (multi-animal DLC)','SLP (SLEAP)', 'CSV (SLEAP)', 'H5 (SLEAP)', 'TRK (multi-animal APT)', 'MAT (DANNCE 3D)'],'12',com=self.fileselected)
        self.filetype.setChoices('CSV (DLC/DeepPoseKit)')
        self.frame = Frame(self.label_import_csv)

        #method
        self.labelmethod = LabelFrame(self.frame,text='Interpolate missing pose-estimation data',pady=5, padx=5)
        self.interpolation = DropDownMenu(self.labelmethod,'Interpolation',['None','Animal(s): Nearest', 'Animal(s): Linear', 'Animal(s): Quadratic','Body-parts: Nearest', 'Body-parts: Linear', 'Body-parts: Quadratic'],'12')
        self.interpolation.setChoices('None')

        # smoothing
        self.smooth_pose_win_lbl = LabelFrame(self.frame, text='Smooth pose-estimation data', pady=5, padx=5)
        self.smooth_dropdown = DropDownMenu(self.smooth_pose_win_lbl, 'Smoothing', ['None', 'Gaussian', 'Savitzky Golay'], '12', com=self.smoothing_selected)
        self.smooth_dropdown.setChoices('None')
        self.smoothing_time_label = Entry_Box(self.smooth_pose_win_lbl, 'Period (ms):', labelwidth='12', width=10)

        #multicsv
        label_multicsvimport = LabelFrame(self.frame, text='Import multiple csv files', pady=5, padx=5)
        self.folder_csv = FolderSelect(label_multicsvimport,'Folder Select:',title='Select Folder with .csv(s)')
        button_import_csv = Button(label_multicsvimport,text='Import csv to project folder',command = lambda: self.import_multiple_dlc_tracking_csv_file,fg='navy')
        #singlecsv
        label_singlecsvimport = LabelFrame(self.frame, text='Import single csv file', pady=5, padx=5)
        self.file_csv = FileSelect(label_singlecsvimport,'File Select',title='Select a .csv file')
        button_importsinglecsv = Button(label_singlecsvimport,text='Import single csv to project folder',command= lambda: self.import_single_dlc_tracking_csv_file,fg='navy')


        #extract videos in projects
        label_extractframes = LabelFrame(tab4,text='Extract Frames into project folder',fg='black',font=Formats.LABELFRAME_HEADER_FORMAT.value,pady=5,padx=5)
        label_note = Label(label_extractframes,text='Note: This is no longer needed for labelling videos. Instead, extract video frames are used for visualizations')
        label_caution = Label(label_extractframes,text='Caution: This extract all frames from all videos in project,')
        label_caution2 = Label(label_extractframes,text='and is computationally expensive if there is a lot of videos at high frame rates/resolution.')
        button_extractframes = Button(label_extractframes,text='Extract frames',command=self.extract_frames,fg='navy')

        #organize
        self.label_generalsettings.grid(row=0,sticky=W)
        self.directory1Select.grid(row=1,column=0,sticky=W)
        self.label_project_name.grid(row=2,column=0,sticky=W)
        label_project_namedescrip.grid(row=3,sticky=W)
        self.csvORparquet.grid(row=4,sticky=W)

        self.label_smlsettings.grid(row=5,column=0,sticky=W,pady=5,columnspan=2)
        self.label_notarget.grid(row=0,column=0,sticky=W,pady=5,columnspan=2)
        addboxButton.grid(row=1,column=0,sticky=W,pady=6)

        self.dropdownbox.grid(row=6,column=0,sticky=W)

        button_generateprojectini.grid(row=20, pady=5, ipadx=5, ipady=5)

        label_importvideo.grid(row=4,sticky=W,pady=5)
        label_multivideoimport.grid(row=0, sticky=W)
        self.multivideofolderpath.grid(row=0, sticky=W)
        self.video_type.grid(row=1, sticky=W)
        button_multivideoimport.grid(row=2, sticky=W)
        label_singlevideoimport.grid(row=1,sticky=W)
        self.singlevideopath.grid(row=0,sticky=W)
        button_importsinglevideo.grid(row=1,sticky=W)

        self.label_import_csv.grid(row=5,sticky=W,pady=5)
        self.filetype.grid(row=0,sticky=W)
        self.frame.grid(row=1,sticky=W)
        self.labelmethod.grid(row=0,sticky=W)
        self.interpolation.grid(row=0,sticky=W)
        self.smooth_pose_win_lbl.grid(row=1, sticky=W)
        self.smooth_dropdown.grid(row=1,sticky=W)

        label_multicsvimport.grid(row=2, sticky=W)
        self.folder_csv.grid(row=0,sticky=W)
        button_import_csv.grid(row=1,sticky=W)
        label_singlecsvimport.grid(row=3,sticky=W)
        self.file_csv.grid(row=0,sticky=W)
        button_importsinglecsv.grid(row=1,sticky=W)

        label_extractframes.grid(row=7,sticky=W)
        label_note.grid(row=0,sticky=W)
        label_caution.grid(row=1,sticky=W)
        label_caution2.grid(row=2,sticky=W)
        button_extractframes.grid(row=3,sticky=W)

    def smoothing_selected(self, choice):
        if choice == 'None':
            self.smoothing_time_label.grid_forget()
        if (choice == 'Gaussian') or (choice == 'Savitzky Golay'):
            self.smoothing_time_label.grid(row=1, column=1, sticky=E)

    def trackingselect(self,val):
        try:
            self.frame2.destroy()
        except:
            pass
        # choice
        self.frame2 = Frame(self.dropdownbox)
        if val == 'Classic tracking':
            label_dropdownmice = Label(self.frame2, text='# config')
            self.option_mice, optionsBasePhotosList = bodypartConfSchematic()
            # del multi animal
            del self.option_mice[9:13]
            del optionsBasePhotosList[9:13]

            self.var = StringVar()
            self.var.set(self.option_mice[6])
            micedropdown = OptionMenu(self.frame2, self.var, *self.option_mice)

            self.var.trace("w", self.change_image)

            self.photos = []
            for i in range(len(optionsBasePhotosList)):
                self.photos.append(PhotoImage(file=os.path.join(os.path.dirname(__file__), (optionsBasePhotosList[i]))))

            self.label = Label(self.frame2, image=self.photos[6])
            self.label.grid(row=10, sticky=W, columnspan=2)
            # reset button
            resetbutton = Button(self.frame2, text='Reset user-defined pose configs', command= lambda: PoseResetterPopUp())
            # organize
            self.frame2.grid(row=1, sticky=W)
            label_dropdownmice.grid(row=0, column=0, sticky=W)
            micedropdown.grid(row=0, column=1, sticky=W)
            self.label.grid(row=1, sticky=W, columnspan=2)
            resetbutton.grid(row=0, sticky=W, column=2)

        else:
            if val == 'Multi tracking':
                label_dropdownmice = Label(self.frame2, text='# config')
                self.option_mice, optionsBasePhotosList = bodypartConfSchematic()
                # del single animal
                del self.option_mice[0:9]
                self.option_mice.remove('3D')
                del optionsBasePhotosList[0:9]
                optionsBasePhotosList = [x for x in optionsBasePhotosList if "Picture13.png" not in x]

                self.var = StringVar()
                self.var.set(self.option_mice[2])
                micedropdown = OptionMenu(self.frame2, self.var, *self.option_mice)

                self.var.trace("w", self.change_image)

                self.photos = []
                for i in range(len(optionsBasePhotosList)):
                    self.photos.append(
                        PhotoImage(file=os.path.join(os.path.dirname(__file__), (optionsBasePhotosList[i]))))

                self.label = Label(self.frame2, image=self.photos[2])
                self.label.grid(row=10, sticky=W, columnspan=2)
                # reset button
                resetbutton = Button(self.frame2, text='Reset user-defined pose configs', command= lambda: PoseResetterPopUp())
                # organize
                self.frame2.grid(row=1, sticky=W)
                label_dropdownmice.grid(row=0, column=0, sticky=W)
                micedropdown.grid(row=0, column=1, sticky=W)
                self.label.grid(row=1, sticky=W, columnspan=2)
                resetbutton.grid(row=0, sticky=W, column=2)

            if val == '3D tracking':
                label_dropdownmice = Label(self.frame2, text='# config')
                self.option_mice, optionsBasePhotosList = bodypartConfSchematic()

                # del single animal and multi-animal
                del self.option_mice[0:12]
                del optionsBasePhotosList[0:12]
                self.var = StringVar()
                self.var.set(self.option_mice[0])
                micedropdown = OptionMenu(self.frame2, self.var, *self.option_mice)

                self.var.trace("w", self.change_image)

                self.photos = []
                for i in range(len(optionsBasePhotosList)):
                    self.photos.append(
                        PhotoImage(file=os.path.join(os.path.dirname(__file__), (optionsBasePhotosList[i]))))

                self.label = Label(self.frame2, image=self.photos[0])
                self.label.grid(row=10, sticky=W, columnspan=2)
                # reset button
                resetbutton = Button(self.frame2, text='Reset user-defined pose configs', command= lambda: PoseResetterPopUp())
                # organize
                self.frame2.grid(row=1, sticky=W)
                label_dropdownmice.grid(row=0, column=0, sticky=W)
                micedropdown.grid(row=0, column=1, sticky=W)
                self.label.grid(row=1, sticky=W, columnspan=2)
                resetbutton.grid(row=0, sticky=W, column=2)

    def fileselected(self,val):
        try:
            self.frame.destroy()
        except:
            pass

        self.frame = Frame(self.label_import_csv)
        self.labelmethod = LabelFrame(self.frame, text='Interpolate missing pose-estimation data', pady=5, padx=5)
        self.interpolation = DropDownMenu(self.labelmethod, 'Interpolation', ['None','Animal(s): Nearest', 'Animal(s): Linear', 'Animal(s): Quadratic','Body-parts: Nearest', 'Body-parts: Linear', 'Body-parts: Quadratic'], '12')
        self.interpolation.setChoices('None')
        self.interpolation.grid(row=0, sticky=W)

        self.smooth_pose_win_lbl = LabelFrame(self.frame, text='Smooth pose-estimation data', pady=5, padx=5)
        self.smooth_dropdown = DropDownMenu(self.smooth_pose_win_lbl, 'Smoothing', ['None', 'Gaussian', 'Savitzky Golay'], '12', com=self.smoothing_selected)
        self.smooth_dropdown.setChoices('None')
        self.smooth_dropdown.grid(row=1, sticky=E)
        self.smoothing_time_label = Entry_Box(self.smooth_pose_win_lbl, 'Period (ms):', labelwidth='12', width=10)

        if self.filetype.getChoices()== 'CSV (DLC/DeepPoseKit)':
            # multicsv
            label_multicsvimport = LabelFrame(self.frame, text='Import multiple csv files', pady=5, padx=5)
            self.folder_csv = FolderSelect(label_multicsvimport, 'Folder Select:', title='Select Folder with .csv(s)')
            button_import_csv = Button(label_multicsvimport, text='Import csv to project folder', command=self.import_multicsv, fg='navy')

            # singlecsv
            label_singlecsvimport = LabelFrame(self.frame, text='Import single csv file', pady=5, padx=5)
            self.file_csv = FileSelect(label_singlecsvimport, 'File Select', title='Select a .csv file')
            button_importsinglecsv = Button(label_singlecsvimport, text='Import single csv to project folder',
                                            command=self.import_single_dlc_tracking_csv_file, fg='navy')
            self.frame.grid(row=1,sticky=W)
            self.labelmethod.grid(row=0,sticky=W)
            self.smooth_pose_win_lbl.grid(row=1,sticky=W)
            label_multicsvimport.grid(row=2, sticky=W)
            self.folder_csv.grid(row=0, sticky=W)
            button_import_csv.grid(row=1, sticky=W)
            label_singlecsvimport.grid(row=3, sticky=W)
            self.file_csv.grid(row=0, sticky=W)
            button_importsinglecsv.grid(row=1, sticky=W)

        elif val == 'MAT (DANNCE 3D)':
            label_multicsvimport = LabelFrame(self.frame, text='Import multiple DANNCE files', pady=5, padx=5)
            self.folder_csv = FolderSelect(label_multicsvimport, 'Folder selected:', title='Select Folder with MAT files')
            button_import_csv = Button(label_multicsvimport, text='Import DANNCE files to project folder', command = lambda: import_DANNCE_folder(self.configinifile, self.folder_csv.folder_path, self.interpolation.getChoices()), fg='navy')
            label_singlecsvimport = LabelFrame(self.frame, text='Import single DANNCE files', pady=5, padx=5)
            self.file_csv = FileSelect(label_singlecsvimport, 'File selected', title='Select a .csv file')
            button_importsinglecsv = Button(label_singlecsvimport, text='Import single DANNCE to project folder', command = lambda: import_DANNCE_file(self.configinifile, self.file_csv.file_path, self.interpolation.getChoices()), fg='navy')
            self.frame.grid(row=1, sticky=W)

            self.labelmethod.grid(row=0, sticky=W)
            self.smooth_pose_win_lbl.grid(row=1, sticky=W)
            label_multicsvimport.grid(row=2, sticky=W)
            self.folder_csv.grid(row=0, sticky=W)
            button_import_csv.grid(row=1, sticky=W)
            label_singlecsvimport.grid(row=3, sticky=W)
            self.file_csv.grid(row=0, sticky=W)
            button_importsinglecsv.grid(row=1, sticky=W)

        elif self.filetype.getChoices()=='JSON (BENTO)':

            label_multijsonimport = LabelFrame(self.frame, text='Import multiple json files', pady=5, padx=5)
            self.folder_json = FolderSelect(label_multijsonimport, 'Folder Select:',
                                            title='Select Folder with .json(s)')
            button_import_json = Button(label_multijsonimport, text='Import json to project folder', fg='navy', command=lambda: MarsImporter(config_path=self.configinifile,
                                                                                                                                              data_path=self.folder_json.folder_path,
                                                                                                                                              interpolation_method=self.interpolation.getChoices(),
                                                                                                                                              smoothing_method=self.smooth_dropdown.getChoices()))

            label_singlejsonimport = LabelFrame(self.frame, text='Import single json file', pady=5, padx=5)
            self.file_json = FileSelect(label_singlejsonimport, 'File Select', title='Select a .csv file')
            button_importsinglejson = Button(label_singlejsonimport, text='Import single .json to project folder', fg='navy', command=lambda: MarsImporter(config_path=self.configinifile,
                                                                                                                                                            data_path=self.folder_json.folder_path,
                                                                                                                                                            interpolation_method=self.interpolation.getChoices(),
                                                                                                                                                            smoothing_method=self.smooth_dropdown.getChoices()))
            # import json into projectfolder
            self.frame.grid(row=1, sticky=W)
            self.labelmethod.grid(row=0, sticky=W)
            self.smooth_pose_win_lbl.grid(row=1, sticky=W)
            label_multijsonimport.grid(row=2, sticky=W)
            self.folder_json.grid(row=0, sticky=W)
            button_import_json.grid(row=1, sticky=W)
            label_singlejsonimport.grid(row=3, sticky=W)
            self.file_json.grid(row=0, sticky=W)
            button_importsinglejson.grid(row=1, sticky=W)

        elif self.filetype.getChoices() in ('H5 (multi-animal DLC)', 'SLP (SLEAP)', 'CSV (SLEAP)', 'H5 (SLEAP)', 'TRK (multi-animal APT)'):
            animalsettings = LabelFrame(self.frame,text='Animal settings',pady=5,padx=5)
            noofanimals = Entry_Box(animalsettings,'No of animals','15')
            animalnamebutton = Button(animalsettings,text='Confirm',command=lambda:self.animalnames(noofanimals.entry_get,animalsettings))

            if self.filetype.getChoices() == 'H5 (multi-animal DLC)':
                options =['skeleton','box','ellipse']
                self.dropdowndlc = DropDownMenu(self.frame,'Tracking type',options,'15')
                self.dropdowndlc.setChoices(options[1])
                self.h5path = FolderSelect(self.frame,'Path to h5 files',lblwidth=15)
                labelinstruction = Label(self.frame,text='Please import videos before importing the multi animal DLC tracking data')
                runsettings = Button(self.frame,text='Import h5',command=self.importh5)
                self.dropdowndlc.grid(row=3, sticky=W)

            elif self.filetype.getChoices() == 'SLP (SLEAP)':
                self.h5path = FolderSelect(self.frame, 'Path to .slp files', lblwidth=15)
                labelinstruction = Label(self.frame, text='Please import videos before importing the multi animal SLEAP tracking data')
                runsettings = Button(self.frame, text='Import .slp', command=self.importh5)

            elif self.filetype.getChoices() == 'TRK (multi-animal APT)':
                self.h5path = FolderSelect(self.frame, 'Path to .trk files', lblwidth=15)
                labelinstruction = Label(self.frame, text='Please import videos before importing the multi animal trk tracking data')
                runsettings = Button(self.frame, text='Import .trk', command=self.importh5)

            elif self.filetype.getChoices() == 'H5 (SLEAP)':
                self.h5path = FolderSelect(self.frame, 'Path to H5 files', lblwidth=15)
                labelinstruction = Label(self.frame, text='Please import videos before importing the multi animal SLEAP H5 tracking data')
                runsettings = Button(self.frame, text='Import .H5', command=self.importh5)

            elif self.filetype.getChoices() == 'CSV (SLEAP)':
                self.h5path = FolderSelect(self.frame, 'Path to CSV files', lblwidth=15)
                labelinstruction = Label(self.frame, text='Please import videos before importing the multi animal SLEAP CSV tracking data')
                runsettings = Button(self.frame, text='Import .CSV', command=self.importh5)

            #organize
            self.frame.grid(row=1,sticky=W)
            self.labelmethod.grid(row=0, sticky=W)
            self.smooth_pose_win_lbl.grid(row=1, sticky=W)
            animalsettings.grid(row=2,sticky=W)
            noofanimals.grid(row=0,sticky=W)
            animalnamebutton.grid(row=0,column=1,sticky=W)

            self.h5path.grid(row=4,sticky=W)
            labelinstruction.grid(row=5,pady=10,sticky=W)
            runsettings.grid(row=6,pady=10)

    def importh5(self):
        idlist = []
        try:
            for i in self.animalnamelist:
                idlist.append(i.entry_get)
        except AttributeError:
            print('Please fill in the animal identity names appropriately.')

        config = read_config_file(ini_path=self.configinifile)
        config.set('Multi animal IDs', 'ID_list', ",".join(idlist))
        with open(self.configinifile, 'w') as configfile:
            config.write(configfile)


        smooth_settings_dict = {}
        if self.smooth_dropdown.getChoices() == 'Gaussian':
            smooth_settings_dict['Method'] = 'Gaussian'
            smooth_settings_dict['Parameters'] = {}
            smooth_settings_dict['Parameters']['Time_window'] = self.smoothing_time_label.entry_get

        if self.smooth_dropdown.getChoices() == 'Savitzky Golay':
            smooth_settings_dict['Method'] = 'Savitzky Golay'
            smooth_settings_dict['Parameters'] = {}
            smooth_settings_dict['Parameters']['Time_window'] = self.smoothing_time_label.entry_get


        if self.smooth_dropdown.getChoices() == 'None':
            smooth_settings_dict['Method'] = 'None'

        if self.filetype.getChoices() == 'H5 (multi-animal DLC)':
            dlc_multi_animal_importer = MADLC_Importer(config_path=self.configinifile,
                                                       data_folder=self.h5path.folder_path,
                                                       file_type=self.dropdowndlc.getChoices(),
                                                       id_lst=idlist,
                                                       interpolation_settings=self.interpolation.getChoices(), smoothing_settings=smooth_settings_dict)
            dlc_multi_animal_importer.import_data()


        if self.filetype.getChoices() == 'SLP (SLEAP)':
            sleap_importer = ImportSLEAP(self.configinifile,self.h5path.folder_path,idlist, self.interpolation.getChoices(), smooth_settings_dict)
            sleap_importer.initate_import_slp()
            if sleap_importer.animals_no > 1:
                sleap_importer.visualize_sleap()
            sleap_importer.save_df()
            sleap_importer.perform_interpolation()
            sleap_importer.perform_smothing()
            print('All SLEAP imports complete.')

        if self.filetype.getChoices() == 'TRK (multi-animal APT)':
            try:
                import_trk(self.configinifile,self.h5path.folder_path,idlist, self.interpolation.getChoices(), smooth_settings_dict)
            except Exception as e:
                messagebox.showerror("Error", str(e))

        if self.filetype.getChoices() == 'CSV (SLEAP)':
            sleap_csv_importer = SleapCsvImporter(config_path=self.configinifile,
                                                  data_folder=self.h5path.folder_path,
                                                  actor_IDs=idlist,
                                                  interpolation_settings=self.interpolation.getChoices(),
                                                  smoothing_settings=smooth_settings_dict)
            sleap_csv_importer.initate_import_slp()
            print('SIMBA COMPLETE: Sleap H5 files imported to project_folder/csv/input_csv directory.')

        if self.filetype.getChoices() == 'H5 (SLEAP)':
            sleap_h5_importer = SLEAPImporterH5(config_path=self.configinifile,
                                                  data_folder=self.h5path.folder_path,
                                                  actor_IDs=idlist,
                                                  interpolation_settings=self.interpolation.getChoices(),
                                                  smoothing_settings=smooth_settings_dict)
            sleap_h5_importer.import_sleap()

    def animalnames(self,noofanimal,master):
        try:
            self.frame2.destroy()
        except:
            pass

        no_animal = int(noofanimal)
        self.animalnamelist =[0]*no_animal

        self.frame2 = Frame(master)
        self.frame2.grid(row=1,sticky=W)

        for i in range(no_animal):
            self.animalnamelist[i] = Entry_Box(self.frame2,'Animal ' + str(i+1) + ' name','15')
            self.animalnamelist[i].grid(row=i,sticky=W)

    def change_image(self,*args):
        if (self.var.get() != 'Create pose config...'):
            self.label.config(image=self.photos[self.option_mice.index(str(self.var.get()))])
        else:
            _ = CreateUserDefinedPoseConfigurationPopUp(master=self.toplevel, project_config_class=project_config)

    def import_single_dlc_tracking_csv_file(self):
        if (self.configinifile == 'No file selected') and (self.file_csv.file_path == 'No file selected'):
            print('SIMBA ERROR: Please select a pose-estimation data path.')
            raise FileNotFoundError('SIMBA ERROR: Please select a pose-estimation data path.')
        imported_file_paths = import_dlc_csv(config_path=str(self.configinifile), source=self.file_csv.file_path)
        config = read_config_file(ini_path=str(self.configinifile))
        csv_df = pd.read_csv(imported_file_paths[0], index_col=0)
        if self.interpolation.getChoices() != 'None':
            print('Interpolating missing values (Method: ' + str(self.interpolation.getChoices()) + ') ...')
            interpolate_body_parts = Interpolate(str(self.configinifile), csv_df)
            interpolate_body_parts.detect_headers()
            interpolate_body_parts.fix_missing_values(self.interpolation.getChoices())
            interpolate_body_parts.reorganize_headers()
            interpolate_body_parts.new_df.to_csv(imported_file_paths[0])
        if self.smooth_dropdown.getChoices() == 'Gaussian':
            time_window = self.smoothing_time_label.entry_get
            print('Smoothing data using Gaussian method and {} ms time window ...'.format(str(time_window)))
            smooth_data_gaussian(config=config, file_path=imported_file_paths[0], time_window_parameter=time_window)
        if self.smooth_dropdown.getChoices() == 'Savitzky Golay':
            time_window = self.smoothing_time_label.entry_get
            print('Smoothing data using Savitzky Golay method and {} ms time window ...'.format(str(time_window)))
            smooth_data_savitzky_golay(config=config, file_path=imported_file_paths[0], time_window_parameter=time_window)

    def import_multiple_dlc_tracking_csv_file(self):
        if (self.configinifile == 'No file selected') and (self.folder_csv.folder_path == 'No file selected'):
            print('SIMBA ERROR: Please select a pose-estimation data path.')
            raise FileNotFoundError('SIMBA ERROR: Please select a pose-estimation data path.')
        imported_file_paths = import_dlc_csv(config_path=str(self.configinifile), source=self.folder_csv.folder_path)
        config = read_config_file(ini_path=str(self.configinifile))
        if self.interpolation.getChoices() != 'None':
            print('Interpolating missing values (Method: ' + str(self.interpolation.getChoices()) + ') ...')
            for file_path in imported_file_paths:
                csv_df = read_df(file_path, 'csv')
                interpolate_body_parts = Interpolate(str(self.configinifile), csv_df)
                interpolate_body_parts.detect_headers()
                interpolate_body_parts.fix_missing_values(self.interpolation.getChoices())
                interpolate_body_parts.reorganize_headers()
                interpolate_body_parts.new_df.to_csv(file_path)

            if self.smooth_dropdown.getChoices() == 'Gaussian':
                time_window = self.smoothing_time_label.entry_get
                print('Smoothing data using Gaussian method and {} ms time window ...'.format(str(time_window)))
                for file_path in imported_file_paths:
                    smooth_data_gaussian(config=config, file_path=file_path, time_window_parameter=time_window)

            if self.smooth_dropdown.getChoices() == 'Savitzky Golay':
                time_window = self.smoothing_time_label.entry_get
                print('Smoothing data using Savitzky Golay method and {} ms time window ...'.format(str(time_window)))
                for file_path in imported_file_paths:
                    smooth_data_savitzky_golay(config=config, file_path=file_path, time_window_parameter=time_window)
            print('SIMBA COMPLETE: Finished importing tracking data.')

    def import_multivid(self):
        if not hasattr(self, 'configinifile'):
            print('SIMBA ERROR: Please create a project before importing videos.')
            raise ValueError('SIMBA ERROR: Please create a project before importing videos.')
        try:
            copy_multiple_videos_to_project(self.configinifile, self.multivideofolderpath.folder_path, self.video_type.entry_get)
        except:
            print('Please select a folder containing the videos and enter the correct video format to proceed')

    def import_singlevid(self):
        if not hasattr(self, 'configinifile'):
            print('SIMBA ERROR: Please create a project before importing videos.')
            raise ValueError('SIMBA ERROR: Please create a project before importing videos.')

        copy_single_video_to_project(self.configinifile, self.singlevideopath.file_path)

    def addBox(self, noTargetStr):
        try:
            for i in self.lab:
                i.destroy()
            for i in self.ent1:
                i.destroy()
        except:
            pass
        try:
            noTarget = int(noTargetStr)
        except ValueError:
            assert False, 'Invalid number of predictive classifiers'

        self.all_entries = []
        self.lab=[0]*noTarget
        self.ent1=[0]*noTarget
        for i in range(noTarget):
            self.lab[i]= Label(self.label_smlsettings, text=str('Classifier ') + str(i + 1))
            self.lab[i].grid(row=i+2, column=0, sticky=W)
            self.ent1[i] = Entry(self.label_smlsettings)
            self.ent1[i].grid(row=i+2, column=1, sticky=W)

        self.all_entries = self.ent1

    def setFilepath(self):
        file_selected = askopenfilename()
        self.modelPath.set(file_selected)

    def make_projectini(self):

        project_path = self.directory1Select.folder_path
        project_name = self.label_project_name.entry_get

        #sml settings
        no_targets = self.label_notarget.entry_get
        target_list = []
        for number, ent1 in enumerate(self.all_entries):
            target_list.append(ent1.get())

        ### animal settings
        listindex = self.option_mice.index(str(self.var.get()))
        if self.singleORmulti.getChoices()=='Classic tracking':
            if listindex == 0:
                bp = '4'
            elif listindex == 1:
                bp = '7'
            elif listindex == 2:
                bp = '8'
            elif listindex == 3:
                bp = '9'
            elif (listindex == 4):
                bp = '8'
            elif (listindex == 5):
                bp='14'
            elif (listindex == 6):
                bp = '16'
            elif listindex == 7:
                bp = '987'
            elif listindex == 8:
                bp = 'user_defined'
            else:
                bp = 'user_defined'

        elif self.singleORmulti.getChoices() =='Multi tracking':
            if listindex == 0:
                bp = '8'
            elif listindex == 1:
                bp = '14'
            elif listindex == 2:
                bp = '16'
            else:
                bp = 'user_defined'

        elif self.singleORmulti.getChoices() == '3D tracking':
            bp = '3D_user_defined'


        if (self.singleORmulti.getChoices() =='Classic tracking') and (bp=='user_defined') and (listindex >8):
            listindex = listindex + 4
        elif (self.singleORmulti.getChoices()=='Multi tracking') and (bp=='user_defined') and (listindex > 2):
            listindex = listindex + 1

        noAnimalsPath = os.path.join(os.path.dirname(__file__), 'pose_configurations', 'no_animals', 'no_animals.csv')
        with open(noAnimalsPath, "r", encoding='utf8') as f:
            cr = csv.reader(f, delimiter=",")  # , is default
            rows = list(cr)  # create a list of rows for instance

        if (self.singleORmulti.getChoices()=='Multi tracking'):
            listindex += 9

        if (self.singleORmulti.getChoices()=='3D tracking'):
            listindex += 12

        animalNo = int(rows[listindex][0])
        config_creator = ProjectConfigCreator(project_path=project_path,
                                              project_name=project_name,
                                              target_list=target_list,
                                              pose_estimation_bp_cnt=bp,
                                              body_part_config_idx=listindex,
                                              animal_cnt=animalNo,
                                              file_type=self.csvORparquet.getChoices())

        self.configinifile = config_creator.config_path

    def extract_frames(self):
        try:
            videopath = os.path.join(os.path.dirname(self.configinifile), 'videos')
            print(videopath)
            extract_frames_from_all_videos_in_directory(videopath, self.configinifile)
        except Exception as e:
            print(e.args)
            print('Please make sure videos are imported and located in /project_folder/videos')

def open_web_link(url):
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize()
    cef.CreateBrowserSync(url=url,
                          window_title=url)
    cef.MessageLoop()


def wait_for_internet_connection(url):
    while True:
        try:
            response = urllib.request.urlopen(url, timeout=1)
            return
        except:
            pass

class ProjectPopUp(ConfigReader, PopUpMixin):
    def __init__(self,
                 config_path=str):

        ConfigReader.__init__(self, config_path=config_path)
        PopUpMixin.__init__(self, config_path=config_path, title='LOAD PROJECT')
        self.main_frm = Toplevel()
        self.main_frm.minsize(1300, 800)
        self.main_frm.wm_title("LOAD PROJECT")
        self.main_frm.columnconfigure(0, weight=1)
        self.main_frm.rowconfigure(0, weight=1)
        tab_parent = ttk.Notebook(hxtScrollbar(self.main_frm))
        tab2 = ttk.Frame(tab_parent)
        tab3 = ttk.Frame(tab_parent)
        tab4 = ttk.Frame(tab_parent)
        tab5 = ttk.Frame(tab_parent)
        tab6 = ttk.Frame(tab_parent)
        tab7 = ttk.Frame(tab_parent)
        tab8 = ttk.Frame(tab_parent)
        tab9 = ttk.Frame(tab_parent)
        tab10 = ttk.Frame(tab_parent)
        tab11 = ttk.Frame(tab_parent)


        tab_parent.add(tab2, text= f"{'[ Further imports (data/video/frames) ]':20s}")
        tab_parent.add(tab3, text=f"{'[ Video parameters ]':20s}")
        tab_parent.add(tab4, text=f"{'[ Outlier correction ]':20s}")
        tab_parent.add(tab6, text=f"{'[ ROI ]':10s}")
        tab_parent.add(tab5, text=f"{'[ Extract features ]':20s}")
        tab_parent.add(tab7, text=f"{'[ Label behavior] ':20s}")
        tab_parent.add(tab8, text=f"{'[ Train machine model ]':20s}")
        tab_parent.add(tab9, text=f"{'[ Run machine model ]':20s}")
        tab_parent.add(tab10, text=f"{'[ Visualizations ]':20s}")
        tab_parent.add(tab11,text=f"{'[ Add-ons ]':20s}")

        tab_parent.grid(row=0)
        tab_parent.enable_traversal()

        #label import
        further_imports_tab_frm = LabelFrame(tab2)

        label_importvideo = LabelFrame(further_imports_tab_frm, text='IMPORT FURTHER VIDEOS', font=Formats.LABELFRAME_HEADER_FORMAT.value, padx=15,pady=5,fg='black')
        label_multivideoimport = LabelFrame(label_importvideo, text='IMPORT MULTIPLE VIDEOS', pady=5, padx=5)
        self.multivideofolderpath = FolderSelect(label_multivideoimport, 'VIDEO DIRECTORY:', title='Select directory with videos', lblwidth=20)
        self.single_import_video_type = DropDownMenu(label_multivideoimport, 'FILE FORMAT:', Options.VIDEO_FORMAT_OPTIONS.value, '20')
        self.single_import_video_type.setChoices(Options.VIDEO_FORMAT_OPTIONS.value[0])
        button_multivideoimport = Button(label_multivideoimport, text='IMPORT MULTIPLE VIDEOS', fg='blue', command= lambda: copy_multiple_videos_to_project(config_path=self.config_path, file_type=self.single_import_video_type.getChoices()))
        label_singlevideoimport = LabelFrame(label_importvideo, text='IMPORT SINGLE VIDEO', pady=5, padx=5)
        self.singlevideopath = FileSelect(label_singlevideoimport, "VIDEO PATH", title='Select a video file', lblwidth=20)
        button_importsinglevideo = Button(label_singlevideoimport, text='IMPORT SINGLE VIDEO', fg='blue', command= lambda: copy_single_video_to_project(simba_ini_path=self.config_path, source_path=self.singlevideopath.file_path))

        self.import_frm = LabelFrame(further_imports_tab_frm, text='IMPORT FURTHER TRACKING DATA', font=Formats.LABELFRAME_HEADER_FORMAT.value, pady=5, padx=5,fg='black')
        self.pose_estimation_dropdown = DropDownMenu(self.import_frm, 'FILE TYPE: ', Options.POSE_ESTIMATION_DATA_TYPES.value, '20', com=self.toggle_pose_estimation_data_type(parent=self, parent_frame=self.import_frm))
        self.pose_estimation_dropdown.setChoices(Options.POSE_ESTIMATION_DATA_TYPES.value[0])

        further_methods_frm = LabelFrame(further_imports_tab_frm, text='FURTHER METHODS', font=Formats.LABELFRAME_HEADER_FORMAT.value, pady=5, padx=5, fg='black')
        extract_frm_btn = Button(further_methods_frm, text='EXTRACT FRAMES FOR ALL VIDEOS IN SIMBA PROJECT', fg='blue', command=self.extract_frames_loadini)
        import_frm_dir_btn = Button(further_methods_frm,text='IMPORT FRAMES DIRECTORY TO SIMBA PROJECT', fg='blue', command=lambda: ImportFrameDirectoryPopUp(config_path=self.config_path))
        add_clf_btn = Button(further_methods_frm, text='ADD CLASSIFIER TO SIMBA PROJECT', fg='blue', command=lambda: AddClfPopUp(config_path=self.config_path))
        remove_clf_btn = Button(further_methods_frm, text='REMOVE CLASSIFIER FROM SIMBA PROJECT', fg='blue', command=lambda: RemoveAClassifierPopUp(config_path=self.config_path))
        archive_files_btn = Button(further_methods_frm, text='ARCHIVE PROCESSED FILES IN SIMBA PROJECT', fg='blue', command=lambda: ArchiveProcessedFilesPopUp(config_path=self.config_path))
        reverse_btn = Button(further_methods_frm, text='REVERSE TRACKING IDENTITIES IN SIMBA PROJECT',fg='blue', command=lambda: self.reverseid())
        interpolate_btn = Button(further_methods_frm, text='INTERPOLATE POSE IN SIMBA PROJECT', fg='blue', command=lambda: InterpolatePopUp(config_path=self.config_path))
        smooth_btn = Button(further_methods_frm, text='SMOOTH POSE IN SIMBA PROJECT', fg='blue', command=lambda: SmoothingPopUp(config_path=self.config_path))


        #get coordinates
        label_setscale = LabelFrame(tab3,text='VIDEO PARAMETERS (FPS, RESOLUTION, PPX/MM ....)', font=Formats.LABELFRAME_HEADER_FORMAT.value, pady=5,padx=5,fg='black')
        self.distanceinmm = Entry_Box(label_setscale, 'KNOWN DISTANCE (MILLIMETERS)', '25', validation='numeric')
        button_setdistanceinmm = Button(label_setscale, text='AUTO-POPULATE', fg='green', command=lambda: self.set_distancemm(self.distanceinmm.entry_get))

        button_setscale = Button(label_setscale, text='CONFIGURE VIDEO PARAMETERS', fg='blue', command=lambda: self.create_video_info_table())

        self.new_ROI_frm = LabelFrame(tab6, text='SIMBA ROI INTERFACE', font=Formats.LABELFRAME_HEADER_FORMAT.value)
        self.start_new_ROI = Button(self.new_ROI_frm, text='DEFINE ROIs', fg='green', command= lambda: ROI_menu(self.config_path))
        self.delete_all_ROIs = Button(self.new_ROI_frm, text='DELETE ALL ROI DEFINITIONS', fg='red', command=lambda: delete_all_ROIs(self.config_path))
        self.tutorial_link = Label(self.new_ROI_frm, text='[Link to ROI user-guide]', cursor='hand2',  font='Verdana 8 underline')
        self.tutorial_link.bind("<Button-1>", lambda e: self.callback('https://github.com/sgoldenlab/simba/blob/master/docs/ROI_tutorial_new.md'))

        self.new_ROI_frm.grid(row=0, sticky=NW)
        self.start_new_ROI.grid(row=0, sticky=NW)
        self.delete_all_ROIs.grid(row=1, column=0, sticky=NW)
        self.tutorial_link.grid(row=2, sticky=W)

        self.roi_draw = LabelFrame(tab6, text='ANALYZE ROI DATA', font=Formats.LABELFRAME_HEADER_FORMAT.value)
        analyze_roi_btn = Button(self.roi_draw, text='ANALYZE ROI DATA: AGGREGATES', fg='green', command=lambda: SettingsMenu(config_path=self.config_path, title='ROI ANALYSIS'))
        analyze_roi_time_bins_btn = Button(self.roi_draw, text='ANALYZE ROI DATA: TIME-BINS',  fg='blue', command=lambda: SettingsMenu(config_path=self.config_path, title='TIME BINS: ANALYZE ROI'))

        self.roi_draw.grid(row=0, column=1, sticky=N)
        analyze_roi_btn.grid(row=0, sticky='NW')
        analyze_roi_time_bins_btn.grid(row=1, sticky='NW')

        ###plot roi
        self.roi_draw1 = LabelFrame(tab6, text='VISUALIZE ROI DATA', font=Formats.LABELFRAME_HEADER_FORMAT.value)

        # button
        visualizeROI = Button(self.roi_draw1, text='VISUALIZE ROI TRACKING', fg='green', command= lambda: VisualizeROITrackingPopUp(config_path=self.config_path))
        visualizeROIfeature = Button(self.roi_draw1, text='VISUALIZE ROI FEATURES', fg='blue', command= lambda: VisualizeROIFeaturesPopUp(config_path=self.config_path))

        ##organize
        self.roi_draw1.grid(row=0, column=2, sticky=N)
        visualizeROI.grid(row=0, sticky='NW')
        visualizeROIfeature.grid(row=1, sticky='NW')

        processmovementdupLabel = LabelFrame(tab6,text='OTHER ANALYSES / VISUALIZATIONS', font=Formats.LABELFRAME_HEADER_FORMAT.value)
        analyze_distances_velocity_btn = Button(processmovementdupLabel, text='ANALYZE DISTANCES / VELOCITY: AGGREGATES', fg='green', command=lambda: SettingsMenu(config_path=self.config_path, title='ANALYZE MOVEMENT'))
        analyze_distances_velocity_timebins_btn = Button(processmovementdupLabel, text='ANALYZE DISTANCES / VELOCITY: TIME-BINS', fg='blue', command=lambda: SettingsMenu(config_path=self.config_path, title='TIME BINS: DISTANCE/VELOCITY'))
        self.hmlvar = IntVar()
        self.hmlvar.set(1)

        heatmaps_location_button = Button(processmovementdupLabel,text='CREATE LOCATION HEATMAPS', fg='red', command=lambda: HeatmapLocationPopup(config_path=self.config_path))

        button_lineplot = Button(processmovementdupLabel, text='CREATE PATH PLOTS', fg='orange', command=lambda: QuickLineplotPopup(config_path=self.config_path))
        button_analyzeDirection = Button(processmovementdupLabel,text='ANALYZE DIRECTIONALITY BETWEEN ANIMALS', fg='pink', command =lambda: self.directing_other_animals_analysis())
        button_visualizeDirection = Button(processmovementdupLabel,text='VISUALIZE DIRECTIONALITY BETWEEN ANIMALS', fg='brown', command=lambda:self.directing_other_animals_visualizer())

        #organize
        processmovementdupLabel.grid(row=0,column=3,sticky=NW)
        analyze_distances_velocity_btn.grid(row=0, sticky=NW)
        heatmaps_location_button.grid(row=1, sticky=NW)
        analyze_distances_velocity_timebins_btn.grid(row=2, sticky=NW)
        button_lineplot.grid(row=3, sticky=NW)
        button_analyzeDirection.grid(row=4, sticky=NW)
        button_visualizeDirection.grid(row=5, sticky=NW)

        #outlier correction
        label_outliercorrection = LabelFrame(tab4,text='OUTLIER CORRECTION',font=Formats.LABELFRAME_HEADER_FORMAT.value,pady=5,padx=5,fg='black')
        label_link = Label(label_outliercorrection,text='[Link to user guide]',cursor='hand2',font='Verdana 10 underline')
        button_settings_outlier = Button(label_outliercorrection,text='SETTINGS', fg='blue', command = lambda: OutlierSettingsPopUp(config_path=self.config_path))
        button_outliercorrection = Button(label_outliercorrection,text='RUN OUTLIER CORRECTION', fg='green', command=lambda:self.correct_outlier())
        button_skipOC = Button(label_outliercorrection,text='SKIP OUTLIER CORRECTION (CAUTION)',fg='red', command=lambda: self.initiate_skip_outlier_correction())

        label_link.bind("<Button-1>",lambda e: self.callback('https://github.com/sgoldenlab/simba/blob/master/misc/Outlier_settings.pdf'))

        #extract features
        label_extractfeatures = LabelFrame(tab5,text='EXTRACT FEATURES',font=Formats.LABELFRAME_HEADER_FORMAT.value,pady=5,padx=5,fg='black')
        button_extractfeatures = Button(label_extractfeatures,text='Extract Features',command = lambda: threading.Thread(target=self.extractfeatures).start())

        def activate(box, *args):
            for entry in args:
                if box.get() == 0:
                    entry.configure(state='disabled')
                elif box.get() == 1:
                    entry.configure(state='normal')

        labelframe_usrdef = LabelFrame(label_extractfeatures)
        self.scriptfile = FileSelect(labelframe_usrdef, 'Script path')
        self.scriptfile.btnFind.configure(state='disabled')
        self.user_defined_var = BooleanVar(value=False)

        userscript = Checkbutton(labelframe_usrdef,text='Apply user-defined feature extraction script',variable=self.user_defined_var, command=lambda: activate(self.user_defined_var, self.scriptfile.btnFind))
        append_roi_features = Button(label_extractfeatures, text='Append ROI data to features (CAUTION)', fg='red',command=lambda: SettingsMenu(config_path=self.config_path, title='APPEND ROI FEATURES'))
        append_roi_features.grid(row=10,pady=10)

        #label Behavior
        label_behavior_frm = LabelFrame(tab7,text='LABEL BEHAVIOR',font=Formats.LABELFRAME_HEADER_FORMAT.value,pady=5,padx=5,fg='black')

        select_video_btn_new = Button(label_behavior_frm, text='Select video (create new video annotation)',command= lambda:select_labelling_video(config_path=self.config_path,
                                                                                                                                                   threshold_dict=None,
                                                                                                                                                   setting='from_scratch',
                                                                                                                                                   continuing=False))
        select_video_btn_continue = Button(label_behavior_frm, text='Select video (continue existing video annotation)', command= lambda:select_labelling_video(config_path=self.config_path,
                                                                                                                                                   threshold_dict=None,
                                                                                                                                                   setting=None,
                                                                                                                                                   continuing=True))
        label_thirdpartyann = LabelFrame(tab7,text='IMPORT THIRD-PARTY BEHAVIOR ANNOTATIONS',font=Formats.LABELFRAME_HEADER_FORMAT.value,pady=5,padx=5,fg='black')
        button_importmars = Button(label_thirdpartyann,text='Import MARS Annotation (select folder with .annot files)',command=self.importMARS)
        button_importboris = Button(label_thirdpartyann,text='Import Boris Annotation (select folder with .csv files)',command = self.importBoris)
        button_importsolomon = Button(label_thirdpartyann,text='Import Solomon Annotation (select folder with .csv files',command = self.importSolomon)
        button_importethovision = Button(label_thirdpartyann, text='Import Ethovision Annotation (select folder with .xls/xlsx files)', command=self.import_ethovision)
        button_importdeepethogram = Button(label_thirdpartyann,text='Import DeepEthogram Annotation (select folder with .csv files)', command=self.import_deepethogram)


        #pseudolabel
        label_pseudo = LabelFrame(tab7,text='PSEUDO-LABELLING',font=Formats.LABELFRAME_HEADER_FORMAT.value,pady=5,padx=5,fg='black')
        pseudo_intructions_lbl_1 = Label(label_pseudo,text='Note that SimBA pseudo-labelling require initial machine predictions.')
        pseudo_intructions_lbl_2 = Label(label_pseudo, text='Click here more information on how to use the SimBA pseudo-labelling interface.', cursor="hand2", fg="blue")
        pseudo_intructions_lbl_2.bind("<Button-1>", lambda e: self.callback('https://github.com/sgoldenlab/simba/blob/master/docs/label_behavior.md'))
        pLabel_framedir = FileSelect(label_pseudo,'Video Path',lblwidth='10')
        plabelframe_threshold = LabelFrame(label_pseudo,text='Threshold',pady=5,padx=5)
        plabel_threshold =[0]*len(self.clf_names)
        for count, i in enumerate(list(self.clf_names)):
            plabel_threshold[count] = Entry_Box(plabelframe_threshold,str(i),'20')
            plabel_threshold[count].grid(row=count+2,sticky=W)

        pseudo_lbl_btn = Button(label_pseudo,text='Correct labels',command = lambda:select_labelling_video(config_path=self.config_path,
                                                                                                           threshold_dict=dict(zip(self.clf_names, plabel_threshold)),
                                                                                                           setting='pseudo',
                                                                                                           continuing=False,
                                                                                                           video_file_path=pLabel_framedir.file_path))

        label_adv_label = LabelFrame(tab7,text='ADVANCED LABEL BEHAVIOR',font=Formats.LABELFRAME_HEADER_FORMAT.value,pady=5,padx=5,fg='black')
        label_adv_note_1 = Label(label_adv_label,text='Note that you will have to specify the presence of *both* behavior and non-behavior on your own.')
        label_adv_note_2 = Label(label_adv_label, text='Click here more information on how to use the SimBA labelling interface.', cursor="hand2", fg="blue")
        label_adv_note_2.bind("<Button-1>", lambda e: self.callback('https://github.com/sgoldenlab/simba/blob/master/docs/advanced_labelling.md'))
        adv_label_btn_new = Button(label_adv_label, text='Select video (create new video annotation)',command= lambda: select_labelling_video_advanced(config_path=self.config_path,
                                                                                                                                          continuing=False))
        adv_label_btn_continue = Button(label_adv_label, text='Select video (continue existing video annotation)',command=lambda: select_labelling_video_advanced(config_path=self.config_path, continuing=True))

        #train machine model
        label_trainmachinemodel = LabelFrame(tab8,text='TRAIN MACHINE MODELS',font=Formats.LABELFRAME_HEADER_FORMAT.value,padx=5,pady=5,fg='black')
        button_trainmachinesettings = Button(label_trainmachinemodel,text='SETTINGS',command=self.trainmachinemodelsetting)
        button_trainmachinemodel = Button(label_trainmachinemodel,text='TRAIN SINGLE MODEL (GLOBAL ENVIRONMENT)',fg='blue',command = lambda: threading.Thread(target=self.train_single_model(config_path=self.config_path)).start())
        button_train_multimodel = Button(label_trainmachinemodel, text='TRAIN MULTIPLE MODELS (ONE FOR EACH SAVED SETTING)',fg='green',command = lambda: threading.Thread(target=self.train_multiple_models_from_meta(config_path=self.config_path)).start())

        ##Single classifier valid
        label_model_validation = LabelFrame(tab9, text='VALIDATE MODEL ON SINGLE VIDEO', pady=5, padx=5, font=("Helvetica", 12, 'bold'), fg='blue')
        self.csvfile = FileSelect(label_model_validation, 'SELECT DATA FEATURE FILE', color='blue', lblwidth=30)
        self.modelfile = FileSelect(label_model_validation, 'SELECT MODEL FILE', color='blue', lblwidth=30)
        button_runvalidmodel = Button(label_model_validation, text='RUN MODEL', fg='blue', command=lambda: self.validate_model_first_step())

        button_generateplot = Button(label_model_validation, text="GENERATE PLOT", fg='blue', command=self.updateThreshold)
        self.dis_threshold = Entry_Box(label_model_validation, 'DISCRIMINATION THRESHOLD (0.0-1.0):', '30')
        self.min_behaviorbout = Entry_Box(label_model_validation, 'MINIMUM BOUT LENGTH (MS):', '30', validation='numeric')
        self.generategantt_dropdown = DropDownMenu(label_model_validation, 'CREATE GANTT PLOT', ['None', 'Gantt chart: video', 'Gantt chart: final frame only (slightly faster)'], '15')
        self.generategantt_dropdown.setChoices('None')
        button_validate_model = Button(label_model_validation, text='VALIDATE', fg='blue', command=self.validatemodelsinglevid)

        label_runmachinemodel = LabelFrame(tab9,text='RUN MACHINE MODEL',font=Formats.LABELFRAME_HEADER_FORMAT.value, padx=5, pady=5, fg='black')
        button_run_rfmodelsettings = Button(label_runmachinemodel,text='MODEL SETTINGS', fg='green', command= lambda: SetMachineModelParameters(config_path=self.config_path))
        button_runmachinemodel = Button(label_runmachinemodel,text='RUN MODELS', fg='green', command = self.runrfmodel)

        kleinberg_button = Button(label_runmachinemodel,text='KLEINBERG SMOOTHING', fg='green', command=lambda: KleinbergPopUp(config_path=self.config_path))
        fsttc_button = Button(label_runmachinemodel,text='FSTTC', fg='green', command=lambda:FSTTCPopUp(config_path=self.config_path))
        label_machineresults = LabelFrame(tab9,text='ANALYZE MACHINE RESULTS',font=Formats.LABELFRAME_HEADER_FORMAT.value,padx=5,pady=5,fg='black')

        button_process_datalog = Button(label_machineresults, text='ANALYZE MACHINE PREDICTIONS: AGGREGATES', fg='blue', command=lambda: ClfDescriptiveStatsPopUp(config_path=self.config_path))
        button_process_movement = Button(label_machineresults, text='ANALYZE DISTANCES/VELOCITY: AGGREGATES', fg='blue', command=lambda: SettingsMenu(config_path=self.config_path, title='ANALYZE MOVEMENT'))
        button_movebins = Button(label_machineresults, text='ANALYZE DISTANCES/VELOCITY: TIME BINS', fg='blue', command=lambda: SettingsMenu(config_path=self.config_path, title='TIME BINS: DISTANCE/VELOCITY'))
        button_classifierbins = Button(label_machineresults,text='ANALYZE MACHINE PREDICTIONS: TIME-BINS', fg='blue', command=lambda: TimeBinsClfPopUp(config_path=self.config_path))
        button_classifier_ROI = Button(label_machineresults, text='ANALYZE MACHINE PREDICTION: BY ROI', fg='blue', command=lambda: ClfByROIPopUp(config_path=self.config_path))
        button_severity = Button(label_machineresults, text='ANALYZE MACHINE PREDICTION: BY SEVERITY', fg='blue', command=lambda: AnalyzeSeverityPopUp(config_path=self.config_path))

        visualization_frm = LabelFrame(tab10,text='DATA VISUALIZATIONS',font=Formats.LABELFRAME_HEADER_FORMAT.value,pady=5,padx=5,fg='black')
        sklearn_visualization_btn = Button(visualization_frm,text='VISUALIZE CLASSIFICATIONS', fg='black',command= lambda:SklearnVisualizationPopUp(config_path=self.config_path))
        sklearn_visualization_btn.grid(row=0, column=0, sticky=NW)

        gantt_visualization_btn = Button(visualization_frm,text='VISUALIZE GANTT', fg='blue', command=lambda:GanttPlotPopUp(config_path=self.config_path))
        gantt_visualization_btn.grid(row=1, column=0, sticky=NW)

        probability_visualization_btn = Button(visualization_frm,text='VISUALIZE PROBABILITIES', fg='green', command=lambda:VisualizeClassificationProbabilityPopUp(config_path=self.config_path))
        probability_visualization_btn.grid(row=2, column=0, sticky=NW)

        path_visualization_btn = Button(visualization_frm, text='VISUALIZE PATHS', fg='orange', command=lambda: PathPlotPopUp(config_path=self.config_path))
        path_visualization_btn.grid(row=3, column=0, sticky=NW)

        distance_visualization_btn = Button(visualization_frm, text='VISUALIZE DISTANCES', fg='red', command=lambda: DistancePlotterPopUp(config_path=self.config_path))
        distance_visualization_btn.grid(row=4, column=0, sticky=NW)

        heatmap_clf_visualization_btn = Button(visualization_frm, text='VISUALIZE CLASSIFICATION HEATMAPS', fg='pink', command=lambda: HeatmapClfPopUp(config_path=self.config_path))
        heatmap_clf_visualization_btn.grid(row=5, column=0, sticky=NW)

        data_plot_visualization_btn = Button(visualization_frm, text='VISUALIZE DATA PLOTS', fg='purple',command=lambda: DataPlotterPopUp(config_path=self.config_path))
        data_plot_visualization_btn.grid(row=6, column=0, sticky=NW)

        clf_validation_btn = Button(visualization_frm, text='CLASSIFIER VALIDATION CLIPS', fg='blue', command=lambda: ClassifierValidationPopUp(config_path=self.config_path))
        clf_validation_btn.grid(row=7, column=0, sticky=NW)

        #Merge frames
        merge_frm = LabelFrame(tab10, text='MERGE FRAMES', pady=5, padx=5, font=("Helvetica", 12, 'bold'), fg='black')
        merge_frm_btn = Button(merge_frm, text='MERGE FRAMES', fg='black', command=lambda:ConcatenatorPopUp(config_path=self.config_path))


        #Plotly
        plotlyInterface = LabelFrame(tab10, text= 'PLOTLY / DASH', font=("Helvetica", 12, 'bold'), pady=5, padx=5, fg='black')
        plotlyInterfaceTitles = ['Sklearn results', 'Time bin analyses', 'Probabilities', 'Severity analysis']
        toIncludeVar = []
        for i in range(len(plotlyInterfaceTitles)+1):
            toIncludeVar.append(IntVar())
        plotlyCheckbox = [0] * (len(plotlyInterfaceTitles)+1)
        for i in range(len(plotlyInterfaceTitles)):
            plotlyCheckbox[i] = Checkbutton(plotlyInterface, text=plotlyInterfaceTitles[i], variable=toIncludeVar[i])
            plotlyCheckbox[i].grid(row=i, sticky=W)

        button_save_plotly_file = Button(plotlyInterface, text='Save SimBA / Plotly dataset', command=lambda: self.generateSimBPlotlyFile(toIncludeVar))
        self.plotly_file = FileSelect(plotlyInterface, 'SimBA Dashboard file (H5)', title='Select SimBA/Plotly dataset (h5)')
        self.groups_file = FileSelect(plotlyInterface, 'SimBA Groups file (CSV)', title='Select groups file (csv')
        button_open_plotly_interface = Button(plotlyInterface, text='Open SimBA / Plotly dataset', fg='black', command=lambda: [self.open_plotly_interface('http://127.0.0.1:8050')])

        #addons
        lbl_addon = LabelFrame(tab11,text='SimBA Expansions',pady=5, padx=5,font=Formats.LABELFRAME_HEADER_FORMAT.value,fg='black')
        button_bel = Button(lbl_addon,text='Pup retrieval - Analysis Protocol 1',command=lambda: PupRetrievalPopUp(config_path=self.config_path))
        button_unsupervised = Button(lbl_addon,text='Unsupervised',command = lambda:unsupervisedInterface(self.config_path))
        cue_light_analyser_btn = Button(lbl_addon, text='Cue light analysis', command=lambda: CueLightAnalyzerMenu(config_path=self.config_path))
        anchored_roi_analysis_btn = Button(lbl_addon, text='Animal-anchored ROI analysis', command=lambda: BoundaryMenus(config_path=self.config_path))

        #organize
        label_import.grid(row=0,column=0,sticky=W,pady=5)
        self.label_import_csv.grid(row=2, sticky=N + W, pady=5)
        filetype.grid(row=0,sticky=W)
        self.frame.grid(row=3,sticky=W)

        #method
        self.labelmethod.grid(row=0,sticky=W)
        self.interpolation.grid(row=0,sticky=W)
        self.smooth_pose_win_lbl.grid(row=1, sticky=W)
        self.smooth_dropdown.grid(row=0, sticky=W)
        label_multicsvimport.grid(row=2, sticky=W)
        self.folder_csv.grid(row=0, sticky=W)
        button_import_csv.grid(row=1, sticky=W)
        label_singlecsvimport.grid(row=3, sticky=W)
        self.file_csv.grid(row=0, sticky=W)
        button_importsinglecsv.grid(row=1, sticky=W)

        label_importvideo.grid(row=0,column=0, sticky=N+W, pady=5,padx=5,rowspan=2)
        label_multivideoimport.grid(row=0, sticky=W)
        self.multivideofolderpath.grid(row=0, sticky=W)
        self.single_import_video_type.grid(row=1, sticky=W)
        button_multivideoimport.grid(row=2, sticky=W)
        label_singlevideoimport.grid(row=1, sticky=W)
        self.singlevideopath.grid(row=0, sticky=W)
        button_importsinglevideo.grid(row=1, sticky=W)

        further_methods_frm.grid(row=0, column=1, sticky=NW,pady=5,padx=5)
        extract_frm_btn.grid(row=1, column=0, sticky=NW)
        import_frm_dir_btn.grid(row=2, column=0, sticky=NW)
        add_clf_btn.grid(row=3, column=0, sticky=NW)
        remove_clf_btn.grid(row=4,column=0, sticky=NW)
        archive_files_btn.grid(row=5,column=0, sticky=NW)
        reverse_btn.grid(row=6, column=0, sticky=NW)
        interpolate_btn.grid(row=7, column=0, sticky=NW)
        smooth_btn.grid(row=8, column=0, sticky=NW)

        label_setscale.grid(row=0, sticky=NW,pady=5,padx=5)
        self.distanceinmm.grid(row=0,column=0,sticky=NW)
        button_setdistanceinmm.grid(row=0, column=1, sticky=NW)
        button_setscale.grid(row=1,column=0,sticky=NW)

        label_outliercorrection.grid(row=0,sticky=W)
        button_settings_outlier.grid(row=0,sticky=W)
        button_outliercorrection.grid(row=1,sticky=W)
        button_skipOC.grid(row=2,sticky=W,pady=5)
        label_link.grid(row=3, sticky=W)

        label_extractfeatures.grid(row=4,sticky=W)
        button_extractfeatures.grid(row=0,sticky=W)
        labelframe_usrdef.grid(row=1,sticky=W,pady=5)
        userscript.grid(row=1,sticky=W)
        self.scriptfile.grid(row=2,sticky=W)

        label_behavior_frm.grid(row=5,sticky=W)
        select_video_btn_new.grid(row=0,sticky=W)
        select_video_btn_continue.grid(row=1,sticky=W)

        label_pseudo.grid(row=6,sticky=W,pady=10)

        pLabel_framedir.grid(row=0,sticky=W)
        pseudo_intructions_lbl_1.grid(row=1,sticky=W)
        pseudo_intructions_lbl_2.grid(row=2, sticky=W)
        plabelframe_threshold.grid(row=4,sticky=W)
        pseudo_lbl_btn.grid(row=5,sticky=W)

        label_adv_label.grid(row=7, sticky=W)
        label_adv_note_1.grid(row=0, pady=10, sticky=W)
        label_adv_note_2.grid(row=1, pady=10, sticky=W)
        adv_label_btn_new.grid(row=3, sticky=W)
        adv_label_btn_continue.grid(row=4, sticky=W)

        label_thirdpartyann.grid(row=8, sticky=W)
        button_importmars.grid(row=0, sticky=W, pady=5)
        button_importboris.grid(row=1,sticky=W,pady=5)
        button_importsolomon.grid(row=2,sticky=W,pady=5)
        button_importethovision.grid(row=3,sticky=W,pady=5)
        button_importdeepethogram.grid(row=4,sticky=W,pady=5)

        label_trainmachinemodel.grid(row=6,sticky=W)
        button_trainmachinesettings.grid(row=0,column=0,sticky=W,padx=5)
        button_trainmachinemodel.grid(row=0,column=1,sticky=W,padx=5)
        button_train_multimodel.grid(row=0,column=2,sticky=W,padx=5)

        label_model_validation.grid(row=7, sticky=W, pady=5)
        self.csvfile.grid(row=0, sticky=W)
        self.modelfile.grid(row=1, sticky=W)
        button_runvalidmodel.grid(row=2, sticky=W)
        button_generateplot.grid(row=3, sticky=W)
        self.dis_threshold.grid(row=4, sticky=W)
        self.min_behaviorbout.grid(row=5, sticky=W)
        self.generategantt_dropdown.grid(row=6,sticky=W)
        button_validate_model.grid(row=7, sticky=W)

        label_runmachinemodel.grid(row=8,sticky=NW)
        button_run_rfmodelsettings.grid(row=0,sticky=NW)
        button_runmachinemodel.grid(row=1,sticky=NW)
        kleinberg_button.grid(row=2,sticky=NW)
        fsttc_button.grid(row=3,sticky=NW)

        label_machineresults.grid(row=9,sticky=W,pady=5)
        button_process_datalog.grid(row=2,column=0,sticky=W,padx=3)
        button_process_movement.grid(row=2,column=1,sticky=W,padx=3)
        button_movebins.grid(row=3,column=1,sticky=W,padx=3)
        button_classifierbins.grid(row=3,column=0,sticky=W,padx=3)
        button_classifier_ROI.grid(row=4, column=0, sticky=W, padx=3)
        button_severity.grid(row=4, column=1, sticky=W, padx=3)

        visualization_frm.grid(row=11,column=0,sticky=W+N,padx=5)
        merge_frm.grid(row=11,column=2,sticky=W+N,padx=5)
        merge_frm_btn.grid(row=0, sticky=NW, padx=5)

        plotlyInterface.grid(row=11, column=3, sticky=W + N, padx=5)
        button_save_plotly_file.grid(row=10, sticky=W)
        self.plotly_file.grid(row=11, sticky=W)
        self.groups_file.grid(row=12, sticky=W)
        button_open_plotly_interface.grid(row=13, sticky=W)

        lbl_addon.grid(row=15,sticky=W)
        button_bel.grid(row=0,sticky=W)
        button_unsupervised.grid(row=1,sticky=W)
        cue_light_analyser_btn.grid(row=2, sticky=W)
        anchored_roi_analysis_btn.grid(row=3, sticky=W)

    def create_video_info_table(self):
        video_info_tabler = VideoInfoTable(config_path=self.config_path)
        video_info_tabler.create_window()

    def initiate_skip_outlier_correction(self):
        outlier_correction_skipper = OutlierCorrectionSkipper(config_path=self.config_path)
        outlier_correction_skipper.skip_outlier_correction()


    def validate_model_first_step(self):
        _ = ValidateModelRunClf(config_path=self.config_path, input_file_path=self.csvfile.file_path, clf_path=self.modelfile.file_path)


    def directing_other_animals_analysis(self):
        directing_animals_analyzer = DirectingOtherAnimalsAnalyzer(config_path=self.config_path)
        directing_animals_analyzer.process_directionality()
        directing_animals_analyzer.create_directionality_dfs()
        directing_animals_analyzer.save_directionality_dfs()
        directing_animals_analyzer.summary_statistics()

    def directing_other_animals_visualizer(self):
        _ = DirectingOtherAnimalsVisualizerPopUp(config_path=self.config_path)

    def smoothing_selected(self, choice):
        if choice == 'None':
            self.smoothing_time_label.grid_forget()
        if (choice == 'Gaussian') or (choice == 'Savitzky Golay'):
            self.smoothing_time_label.grid(row=0, column=1, sticky=E)

    def reverseid(self):
        config = ConfigParser()
        configFile = str(self.config_path)
        config.read(configFile)
        noanimal = int(config.get('General settings','animal_no'))

        if noanimal ==2:
            reverse_dlc_input_files(self.config_path)
        else:
            print('This only works if you have exactly 2 animals in your tracking data and video.')

    def train_single_model(self, config_path=None):
        model_trainer = TrainSingleModel(config_path=config_path)
        model_trainer.perform_sampling()
        model_trainer.train_model()
        model_trainer.save_model()

    def train_multiple_models_from_meta(self, config_path=None):
        model_trainer = TrainMultipleModelsFromMeta(config_path=config_path)
        model_trainer.train_models_from_meta()

    def savethres(self):
        config = ConfigParser()
        configFile = str(self.config_path)
        config.read(configFile)

        config.set('threshold_settings', 'bp_threshold_sklearn',str(self.bpthres.entry_get))
        with open(self.config_path, 'w') as configfile:
            config.write(configfile)

        print('Threshold saved >>', str(self.bpthres.entry_get))

    def DLSsettings(self):

        config = ConfigParser()
        configFile = os.path.join(str(self.label_settingsini.folder_path),'settings.ini')
        config.read(configFile)

        # get current settings
        #streaming
        resolution = config.get('Streaming', 'RESOLUTION')
        framerate = config.get('Streaming', 'FRAMERATE')
        streams = config.get('Streaming','STREAMS')
        outputdir = config.get('Streaming','OUTPUT_DIRECTORY')
        multi_devices = config.get('Streaming','MULTIPLE_DEVICES')
        video_source = config.get('Streaming','VIDEO_SOURCE')
        video_path = config.get('Streaming','VIDEO_PATH')
        video = config.get('Streaming','VIDEO')
        animal_no = config.get('Streaming','ANIMALS_NUMBER')
        port = config.get('Streaming','PORT')
        ipwebcam = config.get('Streaming','IPWEBCAM')
        #deeplabcut
        dlcpath = config.get('DeepLabCut','DLC_PATH')
        model = config.get('DeepLabCut','MODEL')
        #classification
        classifier_path = config.get('Classification','PATH_TO_CLASSIFIER')
        allbp = config.get('Classification','ALL_BODYPARTS')
        ppm = config.get('Classification','PIXPERMM')
        threshold = config.get('Classification','THRESHOLD')
        poolsize = config.get('Classification','POOL_SIZE')
        #experiment
        exp_no = config.get('Experiment','EXP_NUMBER')
        record_exp = config.get('Experiment','RECORD_EXP')
        #deeplabstream
        dls_path = config.get('DeepLabStream','DLS_PATH')

        #top level design
        dlstoplevel = Toplevel()
        dlstoplevel.minsize(300, 400)
        dlstoplevel.wm_title('DeepLabStream Settings')
        #streaming
        labelStreamimg = LabelFrame(dlstoplevel,text='Streaming', pady=5, padx=5,font=Formats.LABELFRAME_HEADER_FORMAT.value,fg='black')
        self.e_reso = Entry_Box(labelStreamimg,'Resolution','15')
        self.e_fps = Entry_Box(labelStreamimg,'Frame rate','15')
        self.e_streams = Entry_Box(labelStreamimg, 'Streams', '15')
        self.e_outputdir = FolderSelect(labelStreamimg,'Output directory',title='Select output directory',lblwidth='15')
        self.e_multiDevice = Entry_Box(labelStreamimg, 'Multiple devices', '15')
        self.e_videosource = Entry_Box(labelStreamimg, 'Video source', '15')
        self.e_videopath = FileSelect(labelStreamimg,'Video path',title='Select video',lblwidth='15')
        self.e_video = Entry_Box(labelStreamimg, 'Video', '15')
        self.e_animalNo = Entry_Box(labelStreamimg, 'Animals #', '15')
        self.e_port = Entry_Box(labelStreamimg, 'Port', '15')
        self.e_ipwebcam = Entry_Box(labelStreamimg, 'IP webcam', '15')
        #deeplabcut
        label_dlc = LabelFrame(dlstoplevel,text='DeepLabCut', pady=5, padx=5,font=Formats.LABELFRAME_HEADER_FORMAT.value,fg='black')
        self.e_dlcpath = FolderSelect(label_dlc,'DLC path',title='Select deeplabcut package in python site packages',lblwidth='15')
        self.e_model = FolderSelect(label_dlc,'Model folder path',title='Select DeepLabCut tracking model folder path',lblwidth='15')
        #classification
        label_classification = LabelFrame(dlstoplevel,text='Classification', pady=5, padx=5,font=Formats.LABELFRAME_HEADER_FORMAT.value,fg='black')
        self.e_classifierpath = FileSelect(label_classification,'Classifier path',title='Select Simba Classifier (.sav) file',lblwidth='15')
        self.e_allBP = Entry_Box(label_classification,'All bodyparts',labelwidth='15')
        self.e_ppm = Entry_Box(label_classification,'Pixel / mm','15')
        self.e_threshold = Entry_Box(label_classification,'Threshold','15')
        self.e_poolsize = Entry_Box(label_classification,'Pool size','15')
        #experiment
        label_exp = LabelFrame(dlstoplevel,text='Experiment', pady=5, padx=5,font=Formats.LABELFRAME_HEADER_FORMAT.value,fg='black')
        self.e_expNo = Entry_Box(label_exp,'Experiment #','15')
        self.e_recordExp = Entry_Box(label_exp,'Record Experiment','15')
        # deeplabstream
        label_dls = LabelFrame(dlstoplevel,text='DeepLabStream', pady=5, padx=5,font=Formats.LABELFRAME_HEADER_FORMAT.value,fg='black')
        self.e_dls_path = FolderSelect(label_dls,'DLS path',title='Please select DeepLabStream folder in python packages')

        #feed in config parser
        #streaming
        self.e_reso.entPath.insert(0,resolution)
        self.e_fps.entPath.insert(0,framerate)
        self.e_streams.entPath.insert(0,streams)
        self.e_outputdir.folderPath.set(outputdir)
        self.e_multiDevice.entPath.insert(0,multi_devices)
        self.e_videosource.entPath.insert(0,video_source)
        self.e_videopath.filePath.set(video_path)
        self.e_video.entPath.insert(0,video)
        self.e_animalNo.entPath.insert(0,animal_no)
        self.e_port.entPath.insert(0,port)
        self.e_ipwebcam.entPath.insert(0,ipwebcam)
        #deeplabcut
        self.e_dlcpath.folderPath.set(dlcpath)
        self.e_model.folderPath.set(model)
        #classification
        self.e_classifierpath.filePath.set(classifier_path)
        self.e_allBP.entPath.insert(0,allbp)
        self.e_ppm.entPath.insert(0,ppm)
        self.e_threshold.entPath.insert(0,threshold)
        self.e_poolsize.entPath.insert(0,poolsize)
        #experiment
        self.e_expNo.entPath.insert(0,exp_no)
        self.e_recordExp.entPath.insert(0,record_exp)
        #dls
        self.e_dls_path.folderPath.set(dls_path)

        #organize
        #streaming
        labelStreamimg.grid(row=0,sticky=W)
        self.e_reso.grid(row=0,sticky=W)
        self.e_fps.grid(row=1,sticky=W)
        self.e_streams.grid(row=2,sticky=W)
        self.e_outputdir.grid(row=3,sticky=W)
        self.e_multiDevice.grid(row=4,sticky=W)
        self.e_videosource.grid(row=5,sticky=W)
        self.e_videopath.grid(row=6,sticky=W)
        self.e_video.grid(row=7,sticky=W)
        self.e_animalNo.grid(row=8,sticky=W)
        self.e_port.grid(row=9,sticky=W)
        self.e_ipwebcam.grid(row=10,sticky=W)
        #deeplabcut
        label_dlc.grid(row=1,sticky=W)
        self.e_dlcpath.grid(row=0,sticky=W)
        self.e_model.grid(row=1,sticky=W)
        #classification
        label_classification.grid(row=2,sticky=W)
        self.e_classifierpath.grid(row=0,sticky=W)
        self.e_allBP.grid(row=1,sticky=W)
        self.e_ppm.grid(row=2,sticky=W)
        self.e_threshold.grid(row=3,sticky=W)
        self.e_poolsize.grid(row=4,sticky=W)
        #experiment
        label_exp.grid(row=3,sticky=W)
        self.e_expNo.grid(row=0,sticky=W)
        self.e_recordExp.grid(row=1,sticky=W)
        #dls
        label_dls.grid(row=4,sticky=W)
        self.e_dls_path.grid(row=0,sticky=W)

        #confirm button
        button = Button(dlstoplevel,text='Save settings',command=self.saveDLSsettings)
        button.grid(row=5,pady=10,padx=10)

        #run dls
        button2 = Button(dlstoplevel,text='Run DeepLabStream',command=lambda: threading.Thread(target=self.rundls).start())
        button2.grid(row=6,pady=10,padx=10)

    def rundls(self):
        path = str(os.path.join(self.e_dls_path.folder_path,'app.py'))
        print(path)
        call(['python',path])

    def saveDLSsettings(self):

        config = ConfigParser()
        configFile = os.path.join(str(self.label_settingsini.folder_path),'settings.ini')
        config.read(configFile)

        # write the new values into ini file
        config.set('Streaming', 'RESOLUTION', str(self.e_reso.entry_get))
        config.set('Streaming', 'FRAMERATE', str(self.e_fps.entry_get))
        config.set('Streaming', 'STREAMS', str(self.e_streams.entry_get))
        config.set('Streaming', 'OUTPUT_DIRECTORY', str(self.e_outputdir.folder_path))
        config.set('Streaming', 'MULTIPLE_DEVICES', str(self.e_multiDevice.entry_get))
        config.set('Streaming', 'VIDEO_SOURCE', str(self.e_videosource.entry_get))
        config.set('Streaming', 'VIDEO_PATH', str(self.e_videopath.file_path))
        config.set('Streaming', 'VIDEO', str(self.e_video.entry_get))
        config.set('Streaming', 'ANIMALS_NUMBER', str(self.e_animalNo.entry_get))
        config.set('Streaming', 'PORT', str(self.e_port.entry_get))
        config.set('Streaming', 'IPWEBCAM', str(self.e_ipwebcam.entry_get))

        config.set('DeepLabCut', 'DLC_PATH', str(self.e_dlcpath.folder_path))
        config.set('DeepLabCut', 'MODEL', str(self.e_model.folder_path))

        config.set('Classification', 'PATH_TO_CLASSIFIER', str(self.e_classifierpath.file_path))
        config.set('Classification', 'ALL_BODYPARTS', str(self.e_allBP.entry_get))
        config.set('Classification', 'PIXPERMM', str(self.e_ppm.entry_get))
        config.set('Classification', 'THRESHOLD', str(self.e_threshold.entry_get))
        config.set('Classification', 'POOL_SIZE', str(self.e_poolsize.entry_get))

        config.set('Experiment', 'EXP_NUMBER', str(self.e_expNo.entry_get))
        config.set('Experiment', 'RECORD_EXP', str(self.e_recordExp.entry_get))

        config.set('DeepLabStream','dls_path', str(self.e_dls_path.folder_path))

        with open(os.path.join(str(self.label_settingsini.folder_path),'settings.ini'), 'w') as configfile:
            config.write(configfile)

        print('Settings saved in',os.path.basename(configFile))

    def importBoris(self):
        ann_folder = askdirectory()
        boris_appender = BorisAppender(config_path=self.config_path, boris_folder=ann_folder)
        boris_appender.create_boris_master_file()
        boris_appender.append_boris()

    def importSolomon(self):
        ann_folder = askdirectory()
        solomon_importer = SolomonImporter(config_path=self.config_path,
                                           solomon_dir=ann_folder)
        solomon_importer.import_solomon()

    def import_ethovision(self):
        ann_folder = askdirectory()
        ImportEthovision(config_path=self.config_path, folder_path=ann_folder)

    def import_deepethogram(self):
        ann_folder = askdirectory()
        deepethogram_importer = DeepEthogramImporter(config_path=self.config_path, deep_ethogram_dir=ann_folder)
        deepethogram_importer.import_deepethogram()

    def importMARS(self):
        bento_dir = askdirectory()
        bento_appender = BentoAppender(config_path=self.config_path,
                                       bento_dir=bento_dir)
        bento_appender.read_files()

    def importh5(self):
        idlist = []

        smooth_settings_dict = {}
        if self.smooth_dropdown.getChoices() == 'Gaussian':
            smooth_settings_dict['Method'] = 'Gaussian'
            smooth_settings_dict['Parameters'] = {}
            smooth_settings_dict['Parameters']['Time_window'] = self.smoothing_time_label.entry_get

        if self.smooth_dropdown.getChoices() == 'Savitzky Golay':
            smooth_settings_dict['Method'] = 'Savitzky Golay'
            smooth_settings_dict['Parameters'] = {}
            smooth_settings_dict['Parameters']['Time_window'] = self.smoothing_time_label.entry_get

        if self.smooth_dropdown.getChoices() == 'None':
            smooth_settings_dict['Method'] = 'None'

        # try:
        for i in self.animalnamelist:
            idlist.append(i.entry_get)

        self.config.set('Multi animal IDs', 'ID_list', ",".join(idlist))
        with open(self.projectconfigini, 'w') as configfile:
            self.config.write(configfile)

        if self.val =='H5 (multi-animal DLC)':
            #importMultiDLCpose(self.projectconfigini, self.h5path.folder_path, self.dropdowndlc.getChoices(), idlist, self.interpolation.getChoices(), smooth_settings_dict)
            dlc_multi_animal_importer = MADLC_Importer(config_path=self.projectconfigini,
                                                           data_folder=self.h5path.folder_path,
                                                           file_type=self.dropdowndlc.getChoices(),
                                                           id_lst=idlist,
                                                           interpolation_settings=self.interpolation.getChoices(),
                                                           smoothing_settings=smooth_settings_dict)
            dlc_multi_animal_importer.import_data()

        if self.val == 'SLP (SLEAP)':
            sleap_importer = ImportSLEAP(self.projectconfigini, self.h5path.folder_path, idlist,
                                             self.interpolation.getChoices(), smooth_settings_dict)
            sleap_importer.initate_import_slp()

            if sleap_importer.animals_no > 1:
                sleap_importer.visualize_sleap()
            sleap_importer.save_df()
            sleap_importer.perform_interpolation()
            sleap_importer.perform_smothing()
            print('All SLEAP imports complete.')

        if self.val == 'TRK (multi-animal APT)':
            import_trk(self.projectconfigini,self.h5path.folder_path, idlist, self.interpolation.getChoices(), smooth_settings_dict)

        if self.val == 'CSV (SLEAP)':
            sleap_csv_importer = SleapCsvImporter(config_path=self.projectconfigini,
                                                  data_folder=self.h5path.folder_path,
                                                  actor_IDs=idlist,
                                                  interpolation_settings=self.interpolation.getChoices(),
                                                  smoothing_settings=smooth_settings_dict)
            sleap_csv_importer.initate_import_slp()
            print('SIMBA COMPLETE: Sleap CSV files imported to project_folder/csv/input_csv directory.')

        if self.val == 'H5 (SLEAP)':
            sleap_h5_importer = SLEAPImporterH5(config_path=self.projectconfigini,
                                                  data_folder=self.h5path.folder_path,
                                                  actor_IDs=idlist,
                                                  interpolation_settings=self.interpolation.getChoices(),
                                                  smoothing_settings=smooth_settings_dict)
            sleap_h5_importer.import_sleap()


    def animalnames(self, noofanimal, master):
        try:
            self.frame2.destroy()
        except:
            pass

        no_animal = int(noofanimal)
        self.animalnamelist = [0] * no_animal

        self.frame2 = Frame(master)
        self.frame2.grid(row=1, sticky=W)

        for i in range(no_animal):
            self.animalnamelist[i] = Entry_Box(self.frame2, 'Animal ' + str(i + 1) + ' name', '15')
            self.animalnamelist[i].grid(row=i, sticky=W)
            try:
                self.animalnamelist[i].entry_set(self.animal_ID_list[i])
            except IndexError:
                pass


    def choose_animal_bps(self):
        if hasattr(self, 'path_plot_animal_bp_frm'):
            self.path_plot_animal_bp_frm.destroy()
        self.path_plot_animal_bp_frm = LabelFrame(self.path_plot_frm, text='CHOOSE ANIMAL BODY-PARTS',font=('Helvetica',10,'bold'), pady=5, padx=5)
        self.path_plot_bp_dict = {}
        for animal_cnt in range(int(self.path_animal_cnt_dropdown.getChoices())):
            self.path_plot_bp_dict[animal_cnt] = DropDownMenu(self.path_plot_animal_bp_frm, 'Animal {} bodypart'.format(str(animal_cnt + 1)), self.bp_set, '15')
            self.path_plot_bp_dict[animal_cnt].setChoices(self.bp_set[animal_cnt])
            self.path_plot_bp_dict[animal_cnt].grid(row=animal_cnt, sticky=NW)
        self.path_plot_animal_bp_frm.grid(row=2, column=0, sticky=NW)

    def updateThreshold(self):
        interactive_grapher = InteractiveProbabilityGrapher(config_path=self.projectconfigini,
                                                            file_path=self.csvfile.file_path,
                                                            model_path=self.modelfile.file_path)
        interactive_grapher.create_plots()

    def generateSimBPlotlyFile(self,var):
        inputList = []
        for i in var:
            inputList.append(i.get())

        create_plotly_container(self.projectconfigini, inputList)

    def open_web_link(self, url):
        sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
        cef.Initialize()
        cef.CreateBrowserSync(url=url,
                              window_title=url)
        cef.MessageLoop()

    def open_plotly_interface(self, url):

        # kill any existing plotly cache
        try:
            self.p.kill()
            self.p2.kill()
        except:
            print('Starting plotly')
        #get h5 file path and csv file path
        filePath, groupPath = self.plotly_file.file_path, self.groups_file.file_path

        #print file read
        if filePath.endswith('.h5'):
            print('Reading in',os.path.basename(filePath))
        elif groupPath.endswith('.csv'):
            print('Reading in',os.path.basename(groupPath))

        self.p = subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__),'SimBA_dash_app.py'), filePath, groupPath])
        # csvPath = os.path.join(os.path.dirname(self.projectconfigini),'csv')
        # p = subprocess.Popen([sys.executable, r'simba\SimBA_dash_app.py', filePath, groupPath, csvPath])
        wait_for_internet_connection(url)
        self.p2 = subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__),'run_dash_tkinter.py'), url])
        subprocess_children = [self.p, self.p2]
        atexit.register(terminate_children, subprocess_children)



    def analyzseverity(self):
        analyze_process_severity(self.projectconfigini,self.severityscale.entry_get,self.severityTarget.getChoices())

    def runrfmodel(self):
        rf_model_runner = RunModel(config_path=self.projectconfigini)
        rf_model_runner.run_models()

    def validatemodelsinglevid(self):
        model_validator = ValidateModelOneVideo(ini_path=self.projectconfigini, feature_file_path=self.csvfile.file_path, model_path=self.modelfile.file_path, d_threshold=self.dis_threshold.entry_get, shortest_bout=self.min_behaviorbout.entry_get, create_gantt=self.generategantt_dropdown.getChoices())
        model_validator.perform_clf()
        model_validator.plug_small_bouts()
        model_validator.create_video()

    def trainmachinemodelsetting(self):
        _ = MachineModelSettingsPopUp(config_path=self.projectconfigini)

    def extractfeatures(self):
        config = read_config_file(ini_path=self.projectconfigini)
        pose_estimation_body_parts = read_config_entry(config=config, section='create ensemble settings', option='pose_estimation_body_parts', data_type=Dtypes.STR.value)
        animal_cnt = read_config_entry(config=config, section=ReadConfig.GENERAL_SETTINGS.value, option=ReadConfig.ANIMAL_CNT.value, data_type=Dtypes.INT.value)
        print(f'Pose-estimation body part setting for feature extraction: {str(animal_cnt)} animals {str(pose_estimation_body_parts)} body-parts')
        if self.user_defined_var.get():
            _ = run_user_defined_feature_extraction_class(file_path=self.scriptfile.file_path, config_path=self.projectconfigini)
        else:
            if pose_estimation_body_parts == '16':
                feature_extractor = ExtractFeaturesFrom16bps(config_path=self.projectconfigini)
                feature_extractor.extract_features()
            if (pose_estimation_body_parts == '14'):
                feature_extractor = ExtractFeaturesFrom14bps(config_path=self.projectconfigini)
                feature_extractor.extract_features()
            if (pose_estimation_body_parts == '987'):
                extract_features_wotarget_14_from_16(self.projectconfigini)
            if pose_estimation_body_parts == '9':
                extract_features_wotarget_9(self.projectconfigini)
            if pose_estimation_body_parts == '8':
                if animal_cnt == 1:
                    feature_extractor = ExtractFeaturesFrom8bps(config_path=self.projectconfigini)
                elif animal_cnt == 2:
                    feature_extractor = ExtractFeaturesFrom8bps2Animals(config_path=self.projectconfigini)
                feature_extractor.extract_features()
            if pose_estimation_body_parts == '7':
                feature_extractor = ExtractFeaturesFrom7bps(config_path=self.projectconfigini)
                feature_extractor.extract_features()
            if pose_estimation_body_parts == '4':
                feature_extractor = ExtractFeaturesFrom4bps(config_path=self.projectconfigini)
                feature_extractor.extract_features()
            if pose_estimation_body_parts == 'user_defined':
                feature_extractor = UserDefinedFeatureExtractor(config_path=self.projectconfigini)
                feature_extractor.extract_features()

    def import_single_dlc_tracking_csv_file(self):
        if (self.projectconfigini == 'No file selected') and (self.file_csv.file_path == 'No file selected'):
            print('SIMBA ERROR: Please select a pose-estimation data path.')
            raise FileNotFoundError('SIMBA ERROR: Please select a pose-estimation data path.')
        imported_file_paths = import_dlc_csv(config_path=str(self.projectconfigini), source=self.file_csv.file_path)
        config = read_config_file(ini_path=str(self.projectconfigini))
        csv_df = pd.read_csv(imported_file_paths[0], index_col=0)
        if self.interpolation.getChoices() != 'None':
            print('Interpolating missing values (Method: ' + str(self.interpolation.getChoices()) + ') ...')
            interpolate_body_parts = Interpolate(str(self.projectconfigini), csv_df)
            interpolate_body_parts.detect_headers()
            interpolate_body_parts.fix_missing_values(self.interpolation.getChoices())
            interpolate_body_parts.reorganize_headers()
            interpolate_body_parts.new_df.to_csv(imported_file_paths[0])
        if self.smooth_dropdown.getChoices() == 'Gaussian':
            time_window = self.smoothing_time_label.entry_get
            print('Smoothing data using Gaussian method and {} ms time window ...'.format(str(time_window)))
            smooth_data_gaussian(config=config, file_path=imported_file_paths[0], time_window_parameter=time_window)
        if self.smooth_dropdown.getChoices() == 'Savitzky Golay':
            time_window = self.smoothing_time_label.entry_get
            print('Smoothing data using Savitzky Golay method and {} ms time window ...'.format(str(time_window)))
            smooth_data_savitzky_golay(config=config, file_path=imported_file_paths[0], time_window_parameter=time_window)

    def import_multiple_dlc_tracking_csv_file(self):
        if (self.projectconfigini == 'No file selected') and (self.folder_csv.folder_path == 'No file selected'):
            print('SIMBA ERROR: Please select a pose-estimation data path.')
            raise FileNotFoundError('SIMBA ERROR: Please select a pose-estimation data path.')
        imported_file_paths = import_dlc_csv(config_path=str(self.projectconfigini), source=self.folder_csv.folder_path)
        config = read_config_file(ini_path=str(self.projectconfigini))

        if self.interpolation.getChoices() != 'None':
            print('Interpolating missing values (Method: ' + str(self.interpolation.getChoices()) + ') ...')
            for file_path in imported_file_paths:
                csv_df = read_df(file_path, 'csv')
                interpolate_body_parts = Interpolate(str(self.projectconfigini), csv_df)
                interpolate_body_parts.detect_headers()
                interpolate_body_parts.fix_missing_values(self.interpolation.getChoices())
                interpolate_body_parts.reorganize_headers()
                interpolate_body_parts.new_df.to_csv(file_path)

            if self.smooth_dropdown.getChoices() == 'Gaussian':
                time_window = self.smoothing_time_label.entry_get
                print('Smoothing data using Gaussian method and {} ms time window ...'.format(str(time_window)))
                for file_path in imported_file_paths:
                    smooth_data_gaussian(config=config, file_path=file_path, time_window_parameter=time_window)

            if self.smooth_dropdown.getChoices() == 'Savitzky Golay':
                time_window = self.smoothing_time_label.entry_get
                print('Smoothing data using Savitzky Golay method and {} ms time window ...'.format(str(time_window)))
                for file_path in imported_file_paths:
                    smooth_data_savitzky_golay(config=config, file_path=file_path, time_window_parameter=time_window)
            print('SIMBA COMPLETE: Finished importing tracking data.')

    def set_distancemm(self, distancemm):
        check_int(name='DISTANCE IN MILLIMETER', value=distancemm)
        config = read_config_file(ini_path=self.projectconfigini)
        config.set('Frame settings', 'distance_mm', distancemm)
        with open(self.projectconfigini, 'w') as configfile:
            config.write(configfile)

    def extract_frames_loadini(self):
        extract_frames_from_all_videos_in_directory(config_path=self.projectconfigini, directory=os.path.join(os.path.dirname(self.projectconfigini), 'videos'))

    def correct_outlier(self):
        outlier_correcter_movement = OutlierCorrecterMovement(config_path=self.projectconfigini)
        outlier_correcter_movement.correct_movement_outliers()
        outlier_correcter_location = OutlierCorrecterLocation(config_path=self.projectconfigini)
        outlier_correcter_location.correct_location_outliers()
        print('SIMBA COMPLETE: Outlier correction complete. Outlier corrected files located in "project_folder/csv/outlier_corrected_movement_location" directory')


    def callback(self,url):
        webbrowser.open_new(url)

def get_frame(self):
    '''
      Return the "frame" useful to place inner controls.
    '''
    return self.canvas

class App(object):
    def __init__(self):
        scriptdir = os.path.dirname(os.path.realpath(__file__))
        self.root = Tk()
        self.root.title('SimBA')
        self.root.minsize(750,750)
        self.root.geometry("750x750")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        if currentPlatform == 'Windows':
            self.root.iconbitmap(os.path.join(scriptdir,'SimBA_logo.ico'))

        #img = PhotoImage(file=os.path.join(scriptdir,'golden.png'))
        img = PhotoImage(file=os.path.join(scriptdir, 'bg.png'))
        background = Label(self.root, image=img, bd=0)
        background.pack(fill='both', expand=True)
        background.image = img

        ### drop down menu###f
        menu = Menu(self.root)
        self.root.config(menu=menu)

        #first menu
        fileMenu = Menu(menu)
        menu.add_cascade(label='File', menu=fileMenu)
        fileMenu.add_command(label='Create a new project',command=project_config)
        fileMenu.add_command(label='Load project', command=lambda: LoadProjectPopUp())
        fileMenu.add_separator()
        fileMenu.add_command(label='Exit', command=self.root.destroy)

        # Process video
        pvMenu = Menu(menu)
        menu.add_cascade(label='Process Videos', menu=pvMenu)
        pvMenu.add_command(label='Batch pre-process videos', command=BatchPreProcessWindow)

        #third menu
        thirdMenu = Menu(menu)
        menu.add_cascade(label='Tracking',menu=thirdMenu)

        #labelling tool
        labellingtoolmenu = Menu(thirdMenu)
        labellingtoolmenu.add_command(label='labelImg', command=lambda: subprocess.call(["labelImg"]))
        labellingtoolmenu.add_command(label='labelme', command=lambda: subprocess.call(["labelme"]))
        #third menu organize
        thirdMenu.add_cascade(label='Labelling tools', menu=labellingtoolmenu)

        #fifth menu
        fifthMenu = Menu(menu)
        fpsMenu = Menu(fifthMenu)
        fpsMenu.add_command(label='Change fps for single video', command=ChangeFpsSingleVideoPopUp)
        fpsMenu.add_command(label='Change fps for multiple videos',command=ChangeFpsMultipleVideosPopUp)
        menu.add_cascade(label='Tools',menu=fifthMenu)
        fifthMenu.add_command(label='Clip videos',command=ClipVideoPopUp)
        fifthMenu.add_command(label='Clip video into multiple videos', command=MultiShortenPopUp)
        fifthMenu.add_command(label='Crop videos',command=CropVideoPopUp)
        fifthMenu.add_command(label='Multi-crop',command=MultiCropPopUp)
        fifthMenu.add_command(label='Downsample videos',command=DownsampleVideoPopUp)
        fifthMenu.add_command(label='Get mm/ppx',command = CalculatePixelsPerMMInVideoPopUp)
        fifthMenu.add_command(label='Create path plot', command=MakePathPlotPopUp)
        fifthMenu.add_cascade(label='Change fps...',menu =fpsMenu)
        fifthMenu.add_cascade(label='Concatenate two videos', command=ConcatenatingVideosPopUp)
        fifthMenu.add_cascade(label='Concatenate multiple videos', command=lambda:ConcatenatorPopUp(config_path=None))
        fifthMenu.add_cascade(label='Visualize pose-estimation in folder...', command=VisualizePoseInFolderPopUp)
        fifthMenu.add_cascade(label='Reorganize Tracking Data', command= PoseReorganizerPopUp)
        fifthMenu.add_cascade(label='Drop body-parts from tracking data', command=DropTrackingDataPopUp)

        #changefpsmenu organize

        changeformatMenu = Menu(fifthMenu)
        changeformatMenu.add_command(label='Change image file formats',command=ChangeImageFormatPopUp)
        changeformatMenu.add_command(label='Change video file formats',command=ConvertVideoPopUp)
        changeformatMenu.add_command(label='Change .seq to .mp4', command=lambda:convertseqVideo(askdirectory(title='Please select video folder to convert')))
        fifthMenu.add_cascade(label='Change formats...',menu=changeformatMenu)

        fifthMenu.add_command(label='CLAHE enhance video',command=CLAHEPopUp)
        fifthMenu.add_command(label='Superimpose frame numbers on video',command=lambda:superimpose_frame_count(file_path=askopenfilename()))
        fifthMenu.add_command(label='Convert to grayscale',command=lambda:video_to_greyscale(file_path=askopenfilename()))
        fifthMenu.add_command(label='Merge frames to video',command=MergeFrames2VideoPopUp)
        fifthMenu.add_command(label='Generate gifs', command=CreateGIFPopUP)
        fifthMenu.add_command(label='Print classifier info...', command=PrintModelInfoPopUp)

        extractframesMenu = Menu(fifthMenu)
        extractframesMenu.add_command(label='Extract defined frames',command=ExtractSpecificFramesPopUp)
        extractframesMenu.add_command(label='Extract frames',command=ExtractAllFramesPopUp)
        extractframesMenu.add_command(label='Extract frames from seq files', command=ExtractSEQFramesPopUp)
        fifthMenu.add_cascade(label='Extract frames...',menu=extractframesMenu)

        convertWftypeMenu = Menu(fifthMenu)
        convertWftypeMenu.add_command(label='Convert CSV to parquet', command=Csv2ParquetPopUp)
        convertWftypeMenu.add_command(label='Convert parquet o CSV', command=Parquet2CsvPopUp)
        fifthMenu.add_cascade(label='Convert working file type...', menu=convertWftypeMenu)


        #sixth menu
        sixthMenu = Menu(menu)
        menu.add_cascade(label='Help',menu=sixthMenu)
        #labelling tool
        links = Menu(sixthMenu)
        links.add_command(label='Download weights',command = lambda:webbrowser.open_new(str(r'https://osf.io/sr3ck/')))
        links.add_command(label='Download classifiers', command=lambda: webbrowser.open_new(str(r'https://osf.io/kwge8/')))
        links.add_command(label='Ex. feature list',command=lambda: webbrowser.open_new(str(r'https://github.com/sgoldenlab/simba/blob/master/misc/Feature_description.csv')))
        links.add_command(label='SimBA github', command=lambda: webbrowser.open_new(str(r'https://github.com/sgoldenlab/simba')))
        links.add_command(label='Gitter Chatroom', command=lambda: webbrowser.open_new(str(r'https://gitter.im/SimBA-Resource/community')))
        links.add_command(label='Install FFmpeg',command =lambda: webbrowser.open_new(str(r'https://m.wikihow.com/Install-FFmpeg-on-Windows')))
        links.add_command(label='Install graphviz', command=lambda: webbrowser.open_new(str(r'https://bobswift.atlassian.net/wiki/spaces/GVIZ/pages/20971549/How+to+install+Graphviz+software')))
        sixthMenu.add_cascade(label="Links",menu=links)
        sixthMenu.add_command(label='About', command= AboutSimBAPopUp)

        #Status bar at the bottom
        self.frame = Frame(background, bd=2, relief=SUNKEN, width=300, height=300)
        self.frame.pack(expand=True)
        self.txt = Text(self.frame, bg='white')
        self.txt.config(state=DISABLED, font=("Rockwell", 11))
        self.txt.pack(expand=True, fill='both')
        #self.txt.configure(font=("Comic Sans MS", 20, "bold"))
        sys.stdout = StdRedirector(self.txt)

# writes text out in GUI
class StdRedirector(object):
    def __init__(self, text_widget):
        self.text_space = text_widget

    def write(self, string):
        self.text_space.config(state=NORMAL)
        self.text_space.insert("end", string)
        self.text_space.update()
        self.text_space.see("end")
        self.text_space.config(state=DISABLED)

class SplashScreen:
    def __init__(self, parent):
        self.parent = parent
        self.Splash()
        self.Window()

    def Splash(self):
        scriptdir = os.path.dirname(__file__)
        if currentPlatform == 'Windows':
            self.image = PIL.Image.open(os.path.join(scriptdir,"splash_050122.png"))
        if (currentPlatform == 'Linux') or (currentPlatform == 'Darwin'):
            try:
                self.image = PIL.Image.open(os.path.join(scriptdir, "splash_050122.PNG"))
            except FileNotFoundError:
                self.image = PIL.Image.open(os.path.join(scriptdir, "splash_050122.png"))
        self.imgSplash = ImageTk.PhotoImage(self.image)


    def Window(self):
        width, height = self.image.size
        halfwidth = (self.parent.winfo_screenwidth()-width)//2
        halfheight = (self.parent.winfo_screenheight()-height)//2
        self.parent.geometry("%ix%i+%i+%i" %(width, height, halfwidth,halfheight))
        Label(self.parent, image=self.imgSplash).pack()

def terminate_children(children):
    for process in children:
        process.terminate()

def main():
    #windows icon
    if currentPlatform == 'Windows':
        import ctypes
        myappid = 'SimBA development wheel'  # arbitrary string
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    # if platform.system() == "Darwin":
    #     multiprocessing.set_start_method('spawn', force=True)


    root = Tk()
    root.overrideredirect(True)
    # import tkinter.font as TkFont
    # default_font = TkFont.nametofont("TkDefaultFont")
    # default_font.configure(size=6)
    # root.option_add("*Font", default_font)

    app = SplashScreen(root)
    root.after(2500, root.destroy)
    root.mainloop()
    app = App()
    print('Welcome fellow scientists :)' + '\n')
    print('\n')
    app.root.mainloop()

from simba.read_config_unit_tests import (check_int, check_str, check_float, read_config_entry, read_config_file, )
import os, glob
from simba.misc_tools import check_multi_animal_status, get_video_meta_data
from simba.drop_bp_cords import getBpNames, get_fn_ext, createColorListofList, create_body_part_dictionary
import itertools
import pandas as pd
import numpy as np
import cv2
from copy import deepcopy

class ImportMADLC(object):
    def __init__(self,
                 config_path=None,
                 data_folder=None,
                 file_type=None,
                 id_lst=None,
                 interpolation_settings=None,
                 smoothing_settings=None):

        self.config = read_config_file(config_path)
        self.interpolation_settings = interpolation_settings
        self.smoothing_settings = smoothing_settings
        self.input_folder = data_folder
        self.id_lst = id_lst
        self.project_path = read_config_entry(self.config, 'General settings', 'project_path', data_type='str')
        self.animal_cnt = read_config_entry(self.config, 'General settings', 'animal_no', 'int')
        self.video_folder = os.path.join(self.project_path, 'videos')
        self.videos_in_project = self.find_all_videos_in_project(self.video_folder)
        self.videos_in_project_lower_case = [os.path.basename(x).lower() for x in self.videos_in_project]
        self.save_folder = os.path.join(self.project_path, 'csv', 'input_csv')
        self.file_type = read_config_entry(self.config, 'General settings', 'workflow_file_type', 'str', 'csv')
        self.pose_setting = read_config_entry(self.config, 'create ensemble settings', 'pose_estimation_body_parts', data_type='str')
        if file_type == 'skeleton': dlc_file_ending, dlc_filtered_file_ending = 'sk.h5', 'sk_filtered.h5'
        elif file_type == 'box': dlc_file_ending, dlc_filtered_file_ending = 'bx.h5', 'bx_filtered.h5'
        elif file_type == 'ellipse': dlc_file_ending, dlc_filtered_file_ending = 'el.h5', 'el_filtered.h5'
        else: raise ValueError('SIMBA ERROR: DLC FILETYPE {} NOT SUPPORTED'.format(file_type))
        self.files_found = glob.glob(self.input_folder + '/*' + dlc_file_ending) + glob.glob(self.input_folder + '/*' + dlc_filtered_file_ending)
        self.files_in_folder = glob.glob(self.input_folder + '/*')
        self.multi_animal_status, self.multi_animal_ids = check_multi_animal_status(self.config, self.animal_cnt)
        self.x_cols, self.y_cols, self.pcols = getBpNames(config_path)
        self.clr_lst_of_lst = createColorListofList(self.animal_cnt, int(len(self.x_cols) / self.animal_cnt) + 1)
        self.animal_bp_dict = create_body_part_dictionary(self.multi_animal_status, self.multi_animal_ids, self.animal_cnt, self.x_cols, self.y_cols, self.pcols, self.clr_lst_of_lst)
        self.split_file_exts = list(itertools.product(*[['dlc_resnet50', 'dlc_resnet_50', 'dlc_dlcrnetms5', 'dlc_effnet_b0'], ['.mp4', '.avi']]))
        self.space_scaler, self.radius_scaler, self.res_scaler, self.font_scaler = 40, 10, 1500, 1.2
        self.bp_lst = []
        for animal in self.animal_bp_dict.keys():
            for currXcol, currYcol, currPcol in zip(self.animal_bp_dict[animal]['X_bps'], self.animal_bp_dict[animal]['Y_bps'], self.animal_bp_dict[animal]['P_bps']):
                self.bp_lst.extend((animal + '_' + currXcol, animal + '_' + currYcol, animal + '_' + currPcol))

        if len(self.files_found) == 0:
            raise FileNotFoundError('SIMBA ERROR: Found 0 files in {} path that satisfy the criterion for maDLC {} filetype. SimBA detected {} other files within in directory'.format(self.input_folder, file_type, str(len(self.files_in_folder))))
        print('Importing {} file(s)...'.format(str(len(self.files_found))))

    def find_all_videos_in_project(self, folder_path=None):
        video_paths = []
        file_paths_in_folder = glob.glob(folder_path + '/*')
        for file_cnt, file_path in enumerate(file_paths_in_folder):
            _, file_name, file_ext = get_fn_ext(file_path)
            if (file_ext.lower() == '.mp4') or (file_ext.lower() == '.avi'):
                video_paths.append(file_path)
        if len(video_paths) == 0:
            raise FileNotFoundError('SIMBA ERROR: No videos in mp4 or avi format imported to SimBA project')
        else:
            return video_paths

    def find_video_file(self):
        assessed_file_paths, self.video_path = [], None
        for combination in self.split_file_exts:
            possible_vid_name = self.file_name.lower().split(combination[0])[0] + combination[1]
            for video_cnt, video_name in enumerate(self.videos_in_project_lower_case):
                if possible_vid_name == video_name:
                    self.video_path = self.videos_in_project[video_cnt]
                else:
                    assessed_file_paths.append(possible_vid_name)
        if self.video_path is None:
            print(assessed_file_paths)
            print('SimBA ERROR: SimBA searched your project_folder/videos directory for a video file representing {}, and could not find a match. Above is a list of possible video filenames that SimBA searched for within your projects video directory without success.'.format(self.file_name))
            raise AttributeError
        else:
             _, self.video_basename, _ = get_fn_ext(self.video_path)

    def insert_all_bps(self, frame=None):
        for animal, bp_data in self.img_bp_cords_dict.items():
            for bp_cnt, bp_tuple in enumerate(bp_data):
                try:
                    cv2.circle(frame, bp_tuple, self.vid_circle_scale, self.animal_bp_dict[animal]['colors'][bp_cnt], -1, lineType=cv2.LINE_AA)
                except Exception as err:
                    if type(err) == OverflowError:
                        print('SIMBA ERROR: SimBA encountered a pose-estimated body-part located at pixel position {}. '
                              'This value is too large to be converted to an integer. '
                              'Please check your pose-estimation data to make sure that it is accurate.'.format(str(bp_tuple)))
                    print(err.args)

    def create_first_side_img(self):
        side_img = np.ones((int(self.video_info['height'] / 2), self.video_info['width'], 3))
        cv2.putText(side_img, 'Current video: ' + self.video_basename, (10, self.vid_space_scale), cv2.FONT_HERSHEY_SIMPLEX, self.vid_font_scale, (255, 255, 255), 3)
        cv2.putText(side_img, 'Can you assign identities based on the displayed frame ?', (10, int(self.vid_space_scale * (self.add_spacer * 2))), cv2.FONT_HERSHEY_SIMPLEX, self.vid_font_scale, (255, 255, 255), 2)
        cv2.putText(side_img, 'Press "x" to display new, random, frame', (10, int(self.vid_space_scale * (self.add_spacer * 3))), cv2.FONT_HERSHEY_SIMPLEX, self.vid_font_scale, (255, 255, 0), 3)
        cv2.putText(side_img, 'Press "c" to continue to start assigning identities using this frame', (10, int(self.vid_space_scale * (self.add_spacer * 4))), cv2.FONT_HERSHEY_SIMPLEX, self.vid_font_scale, (0, 255, 0), 2)
        self.img_concat = np.uint8(np.concatenate((self.img_overlay, side_img), axis=0))

    def create_choose_animals_side_img(self, animal_id):
        self.side_img = np.ones((int(self.video_info['height'] / 2), self.video_info['width'], 3))
        cv2.putText(self.side_img, 'Double left mouse click on:', (10, self.vid_space_scale), cv2.FONT_HERSHEY_SIMPLEX, self.vid_font_scale, (255, 255, 255), 2)
        cv2.putText(self.side_img, animal_id, (10, int(self.vid_space_scale * (self.add_spacer * 2))), cv2.FONT_HERSHEY_SIMPLEX, self.vid_font_scale, (255, 255, 0), 2)
        self.img_concat = np.uint8(np.concatenate((self.img_overlay, self.side_img), axis=0))

    def initiate_choose_frame(self):
        cv2.destroyAllWindows()
        self.cap.set(1, self.frame_no)
        self.all_frame_data = self.data_df.loc[self.frame_no, :]
        cv2.namedWindow('Define animal IDs', cv2.WINDOW_NORMAL)
        self.img_bp_cords_dict = {}
        ret, self.img = self.cap.read()
        self.img_overlay = deepcopy(self.img)
        for animal_cnt, (animal_name, animal_bps) in enumerate(self.animal_bp_dict.items()):
            self.img_bp_cords_dict[animal_name] = []
            for bp_cnt in range(len(animal_bps['X_bps'])):
                x_cord = int(self.data_df.loc[self.frame_no, animal_name + '_' + animal_bps['X_bps'][bp_cnt]])
                y_cord = int(self.data_df.loc[self.frame_no, animal_name + '_' + animal_bps['Y_bps'][bp_cnt]])
                self.img_bp_cords_dict[animal_name].append((x_cord, y_cord))
        self.insert_all_bps(frame=self.img_overlay)
        self.create_first_side_img()
        cv2.imshow('Define animal IDs', self.img_concat)
        cv2.resizeWindow('Define animal IDs', self.video_info['height'], self.video_info['width'])

        keyboard_choice = False
        while not keyboard_choice:
            k = cv2.waitKey(10)
            if k == ord('x'):
                cv2.destroyWindow('Define animal IDs')
                self.frame_no += 50
                self.initiate_choose_frame()
                break
            elif k == ord('c'):
                cv2.destroyWindow('Define animal IDs')
                self.initiate_choose_animals()
                break

    def get_x_y_loc(self, event, x, y, flags, param):
        if event == 7:
            self.click_loc = (x,y)
            self.ID_cords[self.animal_cnt] = {}
            self.ID_cords[self.animal_cnt]['cord'] = self.click_loc
            self.ID_cords[self.animal_cnt]['name'] = self.animal_name

    def insert_all_animal_names(self):
        for animal_cnt, animal_data in self.ID_cords.items():
            #cv2.circle(self.new_frame, animal_data['cord'], self.vid_circle_scale, self.animal_bp_dict[animal_data['name']]['colors'][animal_cnt], -1, lineType=cv2.LINE_AA)
            cv2.putText(self.new_frame, animal_data['name'], animal_data['cord'], cv2.FONT_HERSHEY_SIMPLEX, self.vid_font_scale, (255, 255, 255), 3)

    def initiate_choose_animals(self):
        self.ID_cords = {}
        for animal_cnt, animal in enumerate(self.animal_bp_dict.keys()):
            self.new_overlay = deepcopy(self.img_overlay)
            cv2.namedWindow('Define animal IDs', cv2.WINDOW_NORMAL)
            self.animal_name = animal
            self.animal_cnt = animal_cnt
            self.side_img = np.ones((int(self.video_info['height'] / 2), self.video_info['width'], 3))
            cv2.putText(self.side_img, 'Double left mouse click on:', (10, self.vid_space_scale), cv2.FONT_HERSHEY_SIMPLEX, self.vid_font_scale, (255, 255, 255), 3)
            cv2.putText(self.side_img, animal, (10, int(self.vid_space_scale * (self.add_spacer * 2))), cv2.FONT_HERSHEY_SIMPLEX, self.vid_font_scale, (255, 255, 0), 3)
            for id in self.ID_cords.keys():
                cv2.putText(self.new_overlay, self.ID_cords[id]['name'], self.ID_cords[id]['cord'], cv2.FONT_HERSHEY_SIMPLEX, self.vid_font_scale, (255, 255, 255), 3)
            self.new_overlay = np.uint8(np.concatenate((self.new_overlay, self.side_img), axis=0))
            cv2.imshow('Define animal IDs', self.new_overlay)
            cv2.resizeWindow('Define animal IDs', self.video_info['height'], self.video_info['width'])
            while animal_cnt not in self.ID_cords.keys():
                cv2.setMouseCallback('Define animal IDs', self.get_x_y_loc)
                cv2.waitKey(400)
        self.initiate_confirm()

    def initiate_confirm(self):
        cv2.destroyAllWindows()
        cv2.namedWindow('Define animal IDs', cv2.WINDOW_NORMAL)
        self.new_frame = deepcopy(self.img)
        self.side_img = np.ones((int(self.video_info['height'] / 2), self.video_info['width'], 3))
        cv2.putText(self.side_img, 'Current video: {}'.format(self.video_basename), (10, int(self.vid_space_scale)), cv2.FONT_HERSHEY_SIMPLEX, self.vid_font_scale, (255, 255, 255), 3)
        cv2.putText(self.side_img, 'Are you happy with your assigned identities ?', (10, int(self.vid_space_scale * (self.add_spacer * 2))), cv2.FONT_HERSHEY_SIMPLEX, self.vid_font_scale, (255, 255, 255), 2)
        cv2.putText(self.side_img, 'Press "c" to continue (to finish, or proceed to the next video)', (10, int(self.vid_space_scale * (self.add_spacer * 3))), cv2.FONT_HERSHEY_SIMPLEX, self.vid_font_scale, (255, 255, 0), 2)
        cv2.putText(self.side_img, 'Press "x" to re-start assigning identities', (10, int(self.vid_space_scale * (self.add_spacer * 4))), cv2.FONT_HERSHEY_SIMPLEX, self.vid_font_scale, (0, 255, 255), 2)
        self.insert_all_bps(frame=self.new_frame)
        self.insert_all_animal_names()
        self.img_concat = np.uint8(np.concatenate((self.new_frame, self.side_img), axis=0))
        cv2.imshow('Define animal IDs', self.img_concat)
        cv2.waitKey(1)
        cv2.resizeWindow('Define animal IDs', self.video_info['height'], self.video_info['width'])
        keyboard_choice = False
        while not keyboard_choice:
            k = cv2.waitKey(0)
            if k == ord('x'):
                cv2.destroyWindow('Define animal IDs')
                self.frame_no += 50
                self.initiate_choose_frame()
                break
            elif k == ord('c'):
                # cv2.destroyAllWindows()
                # for i in range(1, 100):
                #     cv2.waitKey(1)
                # #cv2.destroyWindow('Define animal IDs')
                #
                # keyboard_choice = True
                # cv2.waitKey(20)
                break

    def initiate_import(self):
        for file_cnt, file_path in enumerate(self.files_found):
            self.add_spacer = 2
            _, self.file_name, _ = get_fn_ext(file_path)
            self.find_video_file()
            self.data_df = pd.read_hdf(file_path).replace([np.inf, -np.inf], np.nan).fillna(0)

            try:
                self.data_df.columns = self.bp_lst
            except ValueError as err:
                print(err)
                print('The number of body-parts in the input file {} do not match the number of body-parts in your SimBA project. '
                      'The number of of body-parts expected by your SimBA project is {}. '
                      'The number of of body-parts contained in file {} is {}. '
                      'Make sure you have specified the correct number of animals and body-parts in your project.'.format(file_path, str(len(self.x_cols)), file_path, str(len(self.data_df.columns))))

            self.video_info = get_video_meta_data(self.video_path)
            self.max_video_dimension = max(self.video_info['width'], self.video_info['height'])
            self.vid_circle_scale = int(self.radius_scaler / (self.res_scaler / self.max_video_dimension))
            self.vid_font_scale = float(self.font_scaler / (self.res_scaler / self.max_video_dimension))
            self.vid_space_scale = int(self.space_scaler / (self.res_scaler / self.max_video_dimension))
            self.frame_no = 1
            self.cap = cv2.VideoCapture(self.video_path)
            self.initiate_choose_frame()
            cv2.destroyWindow('Define animal IDs')
            cv2.waitKey(5000)
            self.cap.release()
            self.find_closest_animals()
            self.organize_df()

    def check_intergity_of_order(self):
        for click_key_combination in itertools.combinations(list(self.animal_order.keys()), 2):
            click_n, click_n1 = click_key_combination[0], click_key_combination[1]
            animal_1, animal_2 = self.animal_order[click_n]['animal_name'], self.animal_order[click_n1]['animal_name']
            if animal_1 == animal_2:
                print('SIMBA ERROR: The animal most proximal to click number {} is animal named {}. The animal most proximal to click number {} is also animal {}.'
                      'Please indicate which animal is which using a video frame where the animals are clearly separated')
            else:
                pass

    def find_closest_animals(self):
        self.animal_order = {}
        for animal_number, animal_click_data in self.ID_cords.items():
            animal_name, animal_cord = animal_click_data['name'], animal_click_data['cord']
            closest_animal = {}
            closest_animal['animal_name'] = None
            closest_animal['body_part_name'] = None
            closest_animal['distance'] = np.inf
            for animal_name, animal_bps in self.animal_bp_dict.items():
                animal_bp_names_x = self.animal_bp_dict[animal_name]['X_bps']
                animal_bp_names_y = self.animal_bp_dict[animal_name]['Y_bps']
                for x_col, y_col in zip(animal_bp_names_x, animal_bp_names_y):
                    bp_location = (int(self.all_frame_data['{}_{}'.format(animal_name, x_col)]), int(self.all_frame_data['{}_{}'.format(animal_name, y_col)]))
                    distance = abs(np.sqrt((animal_cord[0] - bp_location[0]) ** 2 + (animal_cord[1] - bp_location[1]) ** 2))
                    if distance < closest_animal['distance']:
                        closest_animal['animal_name'] = animal_name
                        closest_animal['body_part_name'] = (x_col, y_col)
                        closest_animal['distance'] = distance
            self.animal_order[animal_number] = closest_animal
        self.check_intergity_of_order()

    def organize_df(self):
        out_df = pd.DataFrame()
        for animal_cnt, animal_data in self.animal_order.items():
            closest_animal_dict = self.animal_bp_dict[animal_data['animal_name']]
            x_cols, y_cols, p_cols = closest_animal_dict['X_bps'], closest_animal_dict['Y_bps'], closest_animal_dict['P_bps']
            x_cols = [animal_data['animal_name'] + '_' + x for x in x_cols]
            y_cols = [animal_data['animal_name'] + '_' + x for x in y_cols]
            p_cols = [animal_data['animal_name'] + '_' + x for x in p_cols]
            for x_col, y_col, p_cols in zip(x_cols, y_cols, p_cols):
                df = self.data_df[[x_col, y_col, p_cols]]
                out_df = pd.concat([out_df, df], axis=1)


# test = ImportMADLC(config_path=r'/Users/simon/Desktop/troubleshooting/B1-MS_US/project_folder/project_config.ini',
#                    data_folder=r'/Users/simon/Desktop/troubleshooting/B1-MS_US/el_import',
#                    file_type='ellipse',
#                    id_lst=['MS', 'US'],
#                    interpolation_settings=None,
#                    smoothing_settings=None)





# test = ImportMADLC(config_path=r'/Users/simon/Desktop/troubleshooting/train_model_project/project_folder/project_config.ini',
#                    data_folder=r'/Users/simon/Desktop/troubleshooting/train_model_project/import',
#                    file_type='ellipse',
#                    id_lst=['Simon', 'JJ'],
#                    interpolation_settings=None,
#                    smoothing_settings=None)
test.initiate_import()

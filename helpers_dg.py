import pandas as pd

def user_input():

	images = input("How many images? ")
	dummy_text = input("What is the dummy text? ")	
	directory = input("What is the image directory? ")
	d = {'images': int(images), 'dummy_text': dummy_text, 'directory': directory}
	return d


def object_classes(df):
	
	# Identify all object classes present in the video
	classes = []
	for index, row in df.iterrows():
	    entry = df['Class'][index]
	    if not pd.isna(entry):
	        if entry not in classes:
	            classes.append(df['Class'][index])       
	classes.sort()
	return classes


def ground_truth(df):

	# Create a dictionary mapping frames to sets of objects in them
	length = len(df)
	image = 0
	index = 0
	ground = {}

	while index < length:
	    num = int(df['NumDetected'][index])
	    d = {'num': num}
	    if num == 0:
	        num = 1
	    elif num == 1:
	        dd = {'Class': df['Class'][index], 'Score': df['Score'][index], 'xmin': df['xmin'][index],
	              'xmax': df['xmax'][index], 'ymin': df['ymin'][index], 'ymax':df['ymax'][index]}
	        d.update({'1':dd})
	    else:
	        for k in range(num):
	            temp = index + k
	            dd = {'Class': df['Class'][temp], 'Score': df['Score'][temp], 'xmin': df['xmin'][temp],
	                  'xmax': df['xmax'][temp],'ymin': df['ymin'][temp], 'ymax':df['ymax'][temp]}
	            d.update({str(k+1): dd})
	    ground.update({str(image): d})
	    image = image + 1
	    index = index + num

	return ground


def class_frames(classes, ground):

	# Create a dictionary mapping object classes to frames that contain them
	frames = {}
	for obj_class in classes:
	    contained = []
	    for key in ground:
	        image = ground[key]
	        num = image['num']
	        if num > 0:
	            for k in range(1, num+1):
	                curr_class = image[str(k)]['Class']
	                if curr_class == obj_class:
	                    contained.append(int(key))
	                    break
	    frames[obj_class] = contained
	return frames


def data_wrapper(frames, ground):

	# Create a dictionary mapping classes to dictionaries mapping frames 
	# to sets of objects
	class_ground = {}
	for key in frames:
	    images = frames[key]    
	    data = []
	    
	    for image in images:
	        info = ground[str(image)]
	        num = info['num']
	        wrapper_d = {}
	        temp_d = {}
	        count = 1
	        for i in range(1, num + 1):
	            if info[str(i)]['Class'] == key:
	                obj_d = {}
	                obj_d['Score'] = info[str(i)]['Score']
	                obj_d['xmin'] = info[str(i)]['xmin']
	                obj_d['xmax'] = info[str(i)]['xmax']
	                obj_d['ymin'] = info[str(i)]['ymin']
	                obj_d['ymax'] = info[str(i)]['ymax']
	                temp_d[count] = obj_d
	                count = count + 1
	        wrapper_d['num'] = count - 1
	        wrapper_d['frame'] = image
	        wrapper_d['data'] = temp_d
	        data.append(wrapper_d)
	    
	    class_ground[key] = data
	return class_ground


def labelling(class_ground):


	# Create a dictionary mapping classes to dictionaries mapping names 
	# to dictionaries mapping frames to object data
	data = {}
	for obj_type in class_ground:
	    test = class_ground[obj_type]
	    obj_num = 1
	    count = 0
	    objects = {}
	    curr = {}

	    for frame in test:
	        if count == 0:
	            for i in range(1, frame['num'] + 1):
	                name = 'obj-' + str(obj_type) + '-' + str(obj_num)   
	                d = frame['data'][i]
	                f = frame['frame']
	                info = {f: d}
	                objects[name] = [info]
	                curr[name] = d
	                curr[name]['frame'] = f
	                obj_num = obj_num + 1

	        else:
	            for i in range(1, frame['num'] + 1):
	                unnamed = True
	                for key in curr:                
	                    curr_data = curr[key]    
	                    if curr_data['frame'] == frame['frame']:
	                        continue

	                    xmin_diff = abs(curr_data['xmin'] - frame['data'][i]['xmin']) / curr_data['xmin'] * 100
	                    xmax_diff = abs(curr_data['xmax'] - frame['data'][i]['xmax']) / curr_data['xmax'] * 100
	                    ymin_diff = abs(curr_data['ymin'] - frame['data'][i]['ymin']) / curr_data['ymin'] * 100
	                    ymax_diff = abs(curr_data['ymax'] - frame['data'][i]['ymax']) / curr_data['ymax'] * 100
	                    frame_diff = frame['frame'] - curr_data['frame']

	                    if frame_diff <= 10:
	                        if (xmin_diff < (10 + frame_diff) and xmax_diff < (10 + frame_diff) or 
	                             (ymin_diff < (10 + frame_diff) and ymax_diff < (10 + frame_diff))):
	                            d = frame['data'][i]
	                            f = frame['frame']
	                            info = {f: d}
	                            objects[key].append(info)
	                            curr[key] = d
	                            curr[key]['frame'] = f
	                            unnamed = False
	                            break

	                if unnamed:
	                    name = 'obj-' + str(obj_type) + '-' + str(obj_num)   
	                    d = frame['data'][i]
	                    f = frame['frame']
	                    info = {f: d}
	                    objects[name] = [info]
	                    curr[name] = d
	                    curr[name]['frame'] = f
	                    obj_num = obj_num + 1

	        count = count + 1 
	    data[obj_type] = objects

	return data

def name_objects(df):

	classes = object_classes(df)
	ground = ground_truth(df)
	frames = class_frames(classes, ground)
	class_ground = data_wrapper(frames, ground)
	data = labelling(class_ground)

	




def impute(df):

	classes = []



	return df
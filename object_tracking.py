from basic_detection import structured_output
from helpers_ot import user_input, frame_input, massage_data
from helpers_ot import tempDS_update, currentDS_update, pastDS_update


# Parameters
# (1) Dataset or New Folder
# (2) Tree Depth/Sliding Window Size 
# (3) Maximum Inactivity

if __name__ =='__main__':

	# Faster R-CNN Model chosen for Flanagan Lab Research
	MODEL_NAME = 'faster_rcnn_resnet50_coco_2018_01_28'
	FROZEN_GRAPH = 'frozen_inference_graph.pb'
	LABELS = 'mscoco_label_map.pbtxt'
	
	# Instance for testing 
	folder = 'datasets/Forward_10204_1844'
	first = 'Forward_10204_1844-f-0000001.jpg'
	last = 'Forward_10204_1844-f-0012331.jpg'
	start = 1
	end = 12331
	count = 1490
	method = 'video'


	# parameters = user_input()

	# if parameters == None:
	# 	return



	# Data Structure that acts as a sliding window on past object detections
	temp_objects = {
		'window': 3,
		'classes': [],
		1: {},
		2: {},
		3: {}
	}

	# Data Structure that keeps track of objects deemed active in a specific context
	current_objects = {
		'class_counts': {},
		'active': [],
		'active_classes': [],
		'active_objects': {},
	}

	# Data Structure that objects that are deemed inactive
	past_objects = {
		'inactive': [],
		'inactive_classes': [],
		'inactive_objects': {}
	}

	while (count <= end):
		
		data = None
		if method == 'video':
			image_path = frame_input(count)  # Dummy function specific to testing instance 
			data = structured_output(MODEL_NAME, FROZEN_GRAPH, LABELS, image_path)
		elif method == 'dataset':
			data = dataset_extraction() ###### TBD

		if not data:
			continue

		new_objects = massage_data(data, method)
		temp_objects = tempDS_update(temp_objects, new_objects)
		# current_objects = tree_search(temp_objects, current_objects, count)
		current_objects = currentDS_update(current_objects, temp_objects, count)
		update = pastDS_update(current_objects, past_objects, count)
		current_objects = update[0]
		past_objects = update[1]
		
		
		print(count)
		print('_____________')
		print('')		
		print(new_objects)
		print('')
		print(temp_objects)
		print('')
		print(current_objects)
		print('')
		print(past_objects)
		print('')

		count = count + 1









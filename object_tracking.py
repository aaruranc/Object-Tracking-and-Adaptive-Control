from basic_detection import structured_output
from helpers_ot import user_input, frame_input, still_video, trajectory_check
from helpers_ot import likelihood, establish_correspondence, tempDS_update, currentDS_update, pastDS_update

# DATA SKELETON

	# temp_objects = {'n-step': k,
	# 					'classes': [1.0, 3.0, 42.0, ... , 10.0],
	# 					'1.0':{
	# 						'1': {
	# 							'objs': ['a', 'b', 'c'],
	# 							'a': {'P-Score': q,
	# 								'box': {'xmin': w, 'ymin': x, 'xmax': y, 'ymax': z}
	# 								 }
	# 						},
	# 						'2': {},
	# 						...
	# 						'k': {}
	# 					}
	# 					...
	#					'k.0': {}
	# 	}


	# current_objects = {'active': ['obj-1.0-135', 'obj-1.0-136', ..., 'obj-120.0-5'],
	# 					'class_counts': {
	# 						1.0: 3,
	# 						2.0: 1,
	# 						...
	# 						120.0: 7
	# 					},
	# 					'active_classes': [1.0, 3.0, ..., 120.0],
	# 					'active_objects': {
	# 						'obj-1.0-135': {...},
	# 						...
	# 						'obj-120.0-5': {...}
	# 					},
	# 					'inactive_classes': [1.0, 2.0, ..., 130.0],
	# 					'inactive': ['obj-1.0-1', 'obj-1.0-2', ..., 'obj-130.0-3'],
	# 					'inactive_objects': {
	# 						'obj-1.0-1': {...},
	# 						...
	# 						'obj-130.0-3': {...}
	# 					}						
	# }


	# obj-4.0-135 = {'P-Score': 1, 'first_detected': 75, 'last_detected': 123, 
	# 		'curr_box': 
	# 			{'xmin': 0, 'ymin': 0.3, 'xmax': 0.5, 'ymax': 0.8},
	# 		'trajectory': 
	# 			{'distribution': {},
	# 			 'history': {}
	# 			 }
	# 	}







if __name__ =='__main__':


	# Faster R-CNN Model chosen for Flanagan Lab Research
	MODEL_NAME = 'faster_rcnn_resnet50_coco_2018_01_28'
	FROZEN_GRAPH = 'frozen_inference_graph.pb'
	LABELS = 'mscoco_label_map.pbtxt'
	# info = user_input()   // FIX LATER, will include temp_objects window size
	
	# Instance for testing 
	folder = 'datasets/Forward_10204_1844'
	first = 'Forward_10204_1844-f-0000001.jpg'
	last = 'Forward_10204_1844-f-0012331.jpg'
	start = 1
	end = 12331
	count = 1373

	temp_objects = {
		'window': 3,
		'classes': [],
		1: {},
		2: {},
		3: {}
	}

	current_objects = {
		'class_counts': {},
		'active': [],
		'active_classes': [],
		'active_objects': {},
	}

	past_objects = {
		'inactive': [],
		'inactive_classes': [],
		'inactive_objects': {}
	}
	

	while still_video(count, end):  # The generalization depends on method of video processing
		print(count)
		image_path = frame_input(count)  # Dummy function specific to testing instance 
		data = structured_output(MODEL_NAME, FROZEN_GRAPH, LABELS, image_path)

		
		if data == 'none':
			continue

		correspondence = {}
		new_objects = {}

		counter = 1
		for object_class in data:
			temp_keys = list(data[object_class])
			
			for object_key in temp_keys:
				# print(object_key)
				poss_parents = trajectory_check(current_objects, object_key, data[object_class][object_key])
				# print(poss_parents)


			if not poss_parents:
				name = 'newobj-' + str(counter)
				counter = counter + 1
				data[object_class][object_key]['class'] = object_class
				new_objects[name] = data[object_class][object_key]

			# else:
			# 	correspondence[object_key] = poss_parents

		print(new_objects)
		temp_objects = tempDS_update(temp_objects, new_objects)
		print('')
		print(temp_objects)
		print('')
		current_objects = currentDS_update(current_objects, temp_objects, count)
		data = pastDS_update(current_objects, past_objects, count)
		current_objects = data[0]
		past_objects = data[1]
		print(current_objects)
		print('')
		# print(past_objects)
		print('')

		count = count + 1


		# current_objects = currentDS_update(current_objects, correspondence)

		# print('')

		# There likely exist situations where the correspondence dict can be pruned based upon 
		# logical consistency. This extension of the algorithm will be saved for the next version


		# parent_probabilities = {}
		# for obj in correspondence_dict:
		# 	likely_parents = correspondence_dict[obj]
		# 	d = {}
		# 	for parent in likely_parents:
		# 		val = likelihood(curr_objs[parent], temp_objs, image_data[obj])
		# 		dd = {parent: val}
		# 		d.update(dd)
		# 	parent_probabilities[obj] = dd


		# semantic_update(current_objects, temp_objects, new_objects)








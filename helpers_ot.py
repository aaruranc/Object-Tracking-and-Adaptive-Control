import copy

def user_input():

	directory = input("What is the video directory? ")
	first = input("What is the first image name? ")
	last = input("What is the last image name? ")
	d = {'directory': directory, 'first': first, 'last': last}
	return d

def still_video(count, end):
	if count <= end:
		return True
	else:
		return False


def frame_input(count):

	text = 'Forward_10204_1844-f-0012331.jpg'
	dummy = 'Forward_10204_1844-f-'
	frame = ''
	if count < 10:
		frame = dummy + '000000' + str(count) + '.jpg'
	elif 10 <= count < 100:
		frame = dummy + '00000' + str(count) + '.jpg'
	elif 100 <= count < 1000:
		frame = dummy + '0000' + str(count) + '.jpg'
	elif 1000 <= count < 10000:
		frame = dummy + '000' + str(count) + '.jpg'
	else:
		frame = dummy + '00' + str(count) + '.jpg'
	
	file = 'datasets/Forward_10204_1844/' + frame
	return file



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

	# obj: {'P-Score': obj_score, 'box': {'xmin': xmin, 'xmax': xmax, 'ymin': ymin, 'ymax': ymax}}



def extract_class(object_key):
	object_key = 3.0-1
	object_class = 3.0
	return object_class



def extract_matching(active_objects, object_class):
	n = len(object_class)
	candidates = []
	for obj in active_objects:
		if obj[4:4+n] == object_class:
			candidates.append(obj)
	return candidates



def on_target(parent_data, fresh_object):
	return True



def parent_trajectory(current_objects, candidate, fresh_object):
	parent_data = current_objects['active_objects'][candidate]

	#### Need to finalize representation for object trajectory 
	if on_target(parent_data, fresh_object): # Dummy function specific to testing instance
		return True

	return False



def trajectory_check(current_objects, object_key, fresh_object):
	if not current_objects:
		return {}


	object_class = extract_class(object_key)  # Dummy function specific to testing instance  
	if object_class in current_objects['active_classes']:
		
		candidates = extract_matching(current_objects['active'], object_class)
		possible_parents = []
		for candidate in candidates:
			if parent_trajectory(current_objects, candidate, fresh_object): # Needs robust generalization
				possible_parents.append(candidate)

		return possible_parents


	# Could add an option to check trajectories against passive objects (Final Build w/ UI)
	# Could create a good dataset to track the complexity tradeoffs in this algorithm
	
	return {}



def likelihood():
	return




def establish_correspondence():
	return



def tempDS_update(temp_objects, new_objects):


	if temp_objects[3]:
		for obj_class in temp_objects[3]:
			if obj_class not in temp_objects[2] and obj_class not in temp_objects[1]:
				index = 'a'
				for n in range(len(temp_objects['classes'])):
					if temp_objects['classes'][n] == obj_class:
						index = n
				temp_objects['classes'].pop(index)

	if temp_objects[2]:
		temp_objects[3] = temp_objects[2]
	if temp_objects[1]:
		temp_objects[2] = temp_objects[1]
		temp_objects[1] = {}

	for obj in new_objects:
		obj_class = new_objects[obj].pop('class')
		if obj_class not in temp_objects[1]:
			d = {'count': 1, 1: new_objects[obj]}
			temp_objects[1][obj_class] = d
			if obj_class not in temp_objects['classes']:
				temp_objects['classes'].append(obj_class)
		else:
			index = temp_objects[1]['count'] + 1
			temp_objects[1]['count'] = index
			temp_objects[1][obj_class][index] = new_objects[obj]

	return temp_objects




def currentDS_update(current_objects, object_correspondence):
	return



# def semantic_update(current_objects, temp_objects, new_objects):


# 	if temp_objects[3]:
# 		for obj_class in temp_objects[3]:
# 			if obj_class not in temp_objects[2] and obj_class not in temp_objects[1]:
# 				temp_objects['classes'].pop(obj_class)

# 	# Update temp_objects
# 	temp_objects[3] = temp_objects[2]
# 	temp_objects[2] = temp_objects[1]


# 	for obj in new_objects:
		
# 		object_class = new_objects[obj].pop('class')

# 		if object_class not in temp_objects[1]:
			
# 			d = {'count': 1, 1: new_objects[obj]}


# 			temp_objects[1][object_class] = deep_d
	
		
# 		else:
# 			temp_objects[1][object_class]['count'] = temp_objects[1][object_class]['count'] + 1
# 			index = temp_objects[1][object_class]['count']
# 			temp_objects[1][object_class][index] = new_objects[obj]

# 		if object_class not in temp_objects['classes']:
# 				temp_objects['classes'].append(object_class)


# 	print('')
# 	print('')

	
# 	print(temp_objects[3])
# 	print(temp_objects[2])
# 	print(temp_objects[1])
# 	print('')


# 	return


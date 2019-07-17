import copy
import numpy as np

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


def fresh_object(current_objects, obj_class, obj, count):

	num = -1
	if obj_class not in current_objects['class_counts']:
		num = 1
		current_objects['class_counts'].update({obj_class: num})
		current_objects['active_objects'].update({obj_class: {}})
		current_objects['active_classes'].append(obj_class)
	
	else:
		num = current_objects['class_counts'][obj_class] + 1
		current_objects['class_counts'][obj_class] = num
		
	name = 'obj-' + str(obj_class) + '-' + str(num)
	current_objects['active'].append(name)

	d = {'P-Score': obj['P-Score'], 
		'box': obj['box'],
		'first_detected': count, 
		'last_detected': count,
		'filter':{
			'mean': 'x', 
			'covariance': 'P'
		}
	}
	# print(d)
	# print('')
	current_objects['active_objects'][obj_class].update({name: d})


	return current_objects



def relative_difference(contenders, obj):
	
	d = {}
	for name in contenders:
		diffs = {}
		
		if contenders[name]['filter']['mean'] == 'x':

			box = contenders[name]['box']
			if obj['box']['xmin'] == 0:
				diffs['xmin'] = 'na'
			if obj['box']['xmin'] != 0:
				diffs['xmin'] = ((box['xmin'] - obj['box']['xmin']) / obj['box']['xmin']) * 100
			
			diffs['xmax'] = ((box['xmax'] - obj['box']['xmax']) / obj['box']['xmax']) * 100

			if obj['box']['ymin'] == 0:
				diffs['ymin'] = -'na'
			if obj['box']['ymin'] != 0:
				diffs['ymin'] = ((box['ymin'] - obj['box']['ymin']) / obj['box']['ymin']) * 100

			diffs['ymax'] = ((box['ymax'] - obj['box']['ymax']) / obj['box']['ymax']) * 100
			
			d[name] = diffs

		else:
			continue



	return d



def similarity_check(contender_diffs):

	d = {}
	for name in contender_diffs:

		if contender_diffs[name]['xmin'] == 'na':
			# if 0 < contender_diffs[name]['xmax'] < 10 or -10 < contender_diffs[name]['xmax'] < 0:
			# 	d[name] = contender_diffs[name]
				continue
		if contender_diffs[name]['ymin'] == 'na':
			# if 0 < contender_diffs[name]['xmax'] < 10 or -10 < contender_diffs[name]['xmax'] < 0:
			# 	d[name] = contender_diffs[name] 
				continue

		if 0 < contender_diffs[name]['xmin'] < 10 and 0 < contender_diffs[name]['xmax'] < 10:
			d[name] = contender_diffs[name]
		elif -10 < contender_diffs[name]['xmin'] < 0 and -10 < contender_diffs[name]['xmax'] < 0:
			d[name] = contender_diffs[name]
		elif 0 < contender_diffs[name]['ymin'] < 10 and 0 < contender_diffs[name]['ymax'] < 10:
			d[name] = contender_diffs[name]
		elif -10 < contender_diffs[name]['ymin'] < 0 and -10 < contender_diffs[name]['ymax'] < 0:
			d[name] = contender_diffs[name]


	return d



def linear_filter(info):
	return





def update_parent(current_objects, candidates, obj_class, obj, count):

	print('GOT HERE BITCH')
	print('')

	names = list(candidates)
	if len(names) == 1:
		

		info = current_objects['active_objects'][obj_class][names[0]]
		diffs = {}
		for key in obj['box']:

			diffs[key] = info['box'][key] - obj['box'][key]
		

		tf_output = np.array([obj['box']['xmin'], obj['box']['xmax'], obj['box']['ymin'], obj['box']['ymax']])
		print('tf_output')
		print(tf_output)
		print('')
		state = np.array([info['box']['xmin'], info['box']['xmax'], info['box']['ymin'], info['box']['ymax'],
						diffs['xmin'], diffs['xmax'], diffs['ymin'], diffs['ymax']])
		print('state')
		print(state)
		print('')
		covariance = np.array([[.1, .05, .025, .0125, 0, 0, 0, 0],
								[.05, .1, .0125, .025, 0, 0, 0, 0],
								[.025, .0125, .1, .05, 0, 0, 0, 0],
								[.0125, .025, .05, .1, 0, 0, 0, 0],
								[0, 0, 0, 0, .2, .1, 0, 0],
								[0, 0, 0, 0, .1, .2, 0, 0],
								[0, 0, 0, 0, 0, 0, .2, .1],
								[0, 0, 0, 0, 0, 0, .1, .2]])
		print('covariance')
		print(covariance)
		print('')
		transition = np.array([[1, 0, 0, 0, 1, 0, 0, 0], 
								[0, 1, 0, 0, 0, 1, 0, 0],
								[0, 0, 1, 0, 0, 0, 1, 0],
								[0, 0, 0, 1, 0, 0, 0, 1],
								[0, 0, 0, 0, 1, 0, 0, 0],
								[0, 0, 0, 0, 0, 1, 0, 0],
								[0, 0, 0, 0, 0, 0, 1, 0],
								[0, 0, 0, 0, 0, 0, 0, 1]])
		print('transition')
		print(transition)
		print('')
		transition_noise = np.array([[.1, .05, 0, 0, 0, 0, 0, 0],
									[.05, .1, 0, 0, 0, 0, 0, 0],
									[0, 0, .1, .05, 0, 0, 0, 0],
									[0, 0, .05, .1, 0, 0, 0, 0],
									[0, 0, 0, 0, .1, .05, 0, 0],
									[0, 0, 0, 0, .05, .1, 0, 0],
									[0, 0, 0, 0, 0, 0, .1, .05],
									[0, 0, 0, 0, 0, 0, .05, .1]])
		print('transition_noise')
		print(transition_noise)
		print('')
		measurement = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
								[0, 1, 0, 0, 0, 0, 0, 0],
								[0, 0, 1, 0, 0, 0, 0, 0],
								[0, 0, 0, 1, 0, 0, 0, 0]])
		print('measurement')
		print(measurement)
		print('')
		measurement_noise = np.array([[.1, .05, .025, .0125],
									[.05, .1, .0125, .025],
									[.025, .0125, .1, .05],
									[.0125, .025, .05, .1]])
		print('measurement_noise')
		print(measurement_noise)
		print('')


		prior_mean = transition.dot(np.transpose(state))
		print('prior_mean')
		print(prior_mean)
		print('')

		prior_covariance = np.add((transition.dot(covariance)).dot(np.transpose(transition)), transition_noise)
		residual = np.subtract(np.transpose(tf_output), measurement.dot(prior_mean))
		uncertainty = np.add((measurement.dot(prior_covariance)).dot(np.transpose(measurement)), measurement_noise)
		kalman_gain = (prior_covariance.dot(np.transpose(measurement))).dot(np.linalg.inv(uncertainty))
		posterior_mean = np.add(prior_mean, kalman_gain.dot(residual))
		posterior_covariance = (np.subtract(np.identity(8), kalman_gain.dot(measurement))).dot(prior_covariance)

		print('posterior_mean')
		print(posterior_mean)
		print('')

		info['P-Score'] = obj['P-Score']
		info['box'] = obj['box']
		info['last_detected'] = count
		info['filter']['mean'] = posterior_mean
		info['filter']['covariance'] = posterior_covariance
		current_objects['active_objects'][obj_class][names[0]] = info

		return current_objects

	else:


		return current_objects




def currentDS_update(current_objects, temp_objects, count):

	new_objects = temp_objects[1]
	classes = list(new_objects)

	for obj_class in classes:
		num = new_objects[obj_class]['count'] + 1
		for k in range(1, num):
			obj = new_objects[obj_class][k]
			if obj_class not in current_objects['active_classes']:
				current_objects = fresh_object(current_objects, obj_class, obj, count)
			else: 
				
				contenders = current_objects['active_objects'][obj_class]
				contender_diffs = relative_difference(contenders, obj)
				candidates = similarity_check(contender_diffs)
				# print('ZZZZZZZZZ')
				# print(candidates)
				# print(obj)
				# print('')

				if not candidates:
					current_objects = fresh_object(current_objects, obj_class, obj, count)

				else:
					current_objects = update_parent(current_objects, candidates, obj_class, obj, count)
					# continue




				

	return current_objects




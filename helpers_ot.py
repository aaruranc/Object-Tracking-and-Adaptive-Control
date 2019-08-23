import numpy as np
import os
import math

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


def user_input():

	d = {}
	datasets = ['Forward_10204_1498', 'Forward_10204_1780', 'Forward_10204_1796', 
				'Forward_10204_1834', 'Forward_10204_1844', 'Forward_10205_0127',
				'Forward_10205_0827']

	method = raw_input("Run on Video or Dataset? Press 'v' or 'd'")
	if method == 'v':
		print("Make sure the image folder is in 'videos/' ")
		folder = raw_input("What is the folder name?")
		file = raw_input("What is the name of the first file (include extension)?")
		
		# Check if folder exists
		# Check if file exists in folder

		text = file.split('-')
		text2 = text[1].split('.')
		dummy = text[0]
		length = len(text2[0])
		extension = text2[1]

		d['folder'] = folder
		d['dummy'] = dummy
		d['length'] = length
		d['extension'] = extension


	elif method == 'd':
		dataset = raw_input("Which Dataset?")
		if dataset not in datasets:
			print('Not a dataset')
			return None

		d['dataset'] = dataset


	else:
		print("Bad input")
		return None



	first = int(raw_input("Start at which image?"))
	last = int(raw_input("End at which image?"))

	d['method'] = method
	d['first'] = first
	d['last'] = last


	return d







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




















def massage_data(data, method):

	# This function simply repackages the output

	new_objects = {}
	counter = 1
	if method == 'video':
		for object_class in data:
			temp_keys = list(data[object_class])
			for object_key in temp_keys:
				name = 'newobj-' + str(counter)
				counter = counter + 1
				data[object_class][object_key]['class'] = object_class
				new_objects[name] = data[object_class][object_key]
	
	elif method == 'dataset':
		######### TBD
		x = None 

	return new_objects




def tempDS_update(temp_objects, new_objects):

	####### This function is written only for trees of depth 3, needs generalized


	# Identifies and pops object classes only present in the final window
	if temp_objects[3]:
		for obj_class in temp_objects[3]:
			if obj_class not in temp_objects[2] and obj_class not in temp_objects[1]:
				index = 'a'
				for n in range(len(temp_objects['classes'])):
					if temp_objects['classes'][n] == obj_class:
						index = n
				temp_objects['classes'].pop(index)
	
	# Shifts sliding window  
	if temp_objects[2]:
		temp_objects[3] = temp_objects[2]
	if temp_objects[1]:
		temp_objects[2] = temp_objects[1]
		temp_objects[1] = {}


	# Updates temp_objects with data from new_objects
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






def relative_difference(contenders, obj):
	
	d = {}
	for name in contenders:
		
		diffs = {}
		box = contenders[name]['box']
		if contenders[name]['filter']['mean'] == 'x':

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

		else:
			
			filter_state = contenders[name]['filter']['mean'][0:5]

			if filter_state[0] == 0:
				diffs['xmin'] = 'na'
			if filter_state[0] != 0:
				diffs['xmin'] = ((box['xmin'] - filter_state[0]) / filter_state[0]) * 100

			diffs['xmax'] = ((box['xmax'] - filter_state[1]) / filter_state[1]) * 100

			if filter_state[2] == 0:
				diffs['ymin'] = 'na'
			if filter_state[2] != 0:
				diffs['ymin'] = ((box['ymin'] - filter_state[2]) / filter_state[2]) * 100

			diffs['ymax'] = ((box['ymax'] - filter_state[3]) / filter_state[3]) * 100


		d[name] = diffs



	return d



def similarity_check(contender_diffs):

	# print(contender_diffs)
	# print('')

	d = {}
	for name in contender_diffs:

		if contender_diffs[name]['xmin'] == 'na':
			if 0 < contender_diffs[name]['xmax'] < 10 or -10 < contender_diffs[name]['xmax'] < 0:
				d[name] = contender_diffs[name]
				continue
		if contender_diffs[name]['ymin'] == 'na':
			if 0 < contender_diffs[name]['xmax'] < 10 or -10 < contender_diffs[name]['xmax'] < 0:
				d[name] = contender_diffs[name] 
				continue

		# Kick the Can
		if contender_diffs[name]['xmin'] == 'na' or contender_diffs[name]['ymin'] == 'na':
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




def most_similar(current_objects, candidates, obj_class, obj):

	score = {}
	for name in candidates:
		box = current_objects['active_objects'][obj_class][name]['box']
		difference = ((box['xmin'] - obj['box']['xmin']) ** 2) + ((box['xmax'] - obj['box']['xmax']) ** 2) 
		+ ((box['ymin'] - obj['box']['ymin']) ** 2) + ((box['ymax'] - obj['box']['ymax']) ** 2)
		score[name] = difference

	min_name = ''
	minimum = 10000
	for name in score:
		if score[name] < minimum:
			min_name = name
			minimum = score[name]

	return min_name



def bayesian_updating(state, covariance, tf_output=''):
	

	transition = np.array([[1, 0, 0, 0, 1, 0, 0, 0], 
							[0, 1, 0, 0, 0, 1, 0, 0],
							[0, 0, 1, 0, 0, 0, 1, 0],
							[0, 0, 0, 1, 0, 0, 0, 1],
							[0, 0, 0, 0, 1, 0, 0, 0],
							[0, 0, 0, 0, 0, 1, 0, 0],
							[0, 0, 0, 0, 0, 0, 1, 0],
							[0, 0, 0, 0, 0, 0, 0, 1]])
	
	transition_noise = np.array([[1, .5, 0, 0, 0, 0, 0, 0],
									[.5, 1, 0, 0, 0, 0, 0, 0],
									[0, 0, 1, .5, 0, 0, 0, 0],
									[0, 0, .5, 1, 0, 0, 0, 0],
									[0, 0, 0, 0, 1, .5, 0, 0],
									[0, 0, 0, 0, .5, 1, 0, 0],
									[0, 0, 0, 0, 0, 0, 1, .5],
									[0, 0, 0, 0, 0, 0, .5, 1]])

	prior_mean = transition.dot(np.transpose(state))
	prior_covariance = np.add((transition.dot(covariance)).dot(np.transpose(transition)), transition_noise)

	if tf_output == '':
		x = (prior_mean, prior_covariance)
	else:
	
		measurement = np.array([[1, 0, 0, 0, 0, 0, 0, 0],
								[0, 1, 0, 0, 0, 0, 0, 0],
								[0, 0, 1, 0, 0, 0, 0, 0],
								[0, 0, 0, 1, 0, 0, 0, 0]])

		measurement_noise = np.array([[1, .5, .25, .125],
									[.5, 1, .125, .25],
									[.25, .125, 1, .5],
									[.125, .25, .5, 1]])

		residual = np.subtract(np.transpose(tf_output), measurement.dot(prior_mean))
		uncertainty = np.add((measurement.dot(prior_covariance)).dot(np.transpose(measurement)), measurement_noise)
		kalman_gain = (prior_covariance.dot(np.transpose(measurement))).dot(np.linalg.inv(uncertainty))
		
		posterior_mean = np.add(prior_mean, kalman_gain.dot(residual))
		posterior_covariance = (np.subtract(np.identity(8), kalman_gain.dot(measurement))).dot(prior_covariance)
		x = (posterior_mean, posterior_covariance)
	

	return x



def linear_filter(current_objects, parent, obj_class, obj, count):
	
	info = current_objects['active_objects'][obj_class][parent]
	tf_output = np.array([obj['box']['xmin'], obj['box']['xmax'], obj['box']['ymin'], obj['box']['ymax']])
	state = ''
	covariance = ''

	if info['filter']['mean'] == 'x':

		speed = {}
		for key in obj['box']:
			speed[key] =  obj['box'][key] - info['box'][key]
		
		state = np.array([info['box']['xmin'], info['box']['xmax'], info['box']['ymin'], info['box']['ymax'],
						speed['xmin'], speed['xmax'], speed['ymin'], speed['ymax']])
		covariance = np.array([[1, .5, .25, .125, 0, 0, 0, 0],
								[.5, 1, .125, .25, 0, 0, 0, 0],
								[.25, .125, 1, .5, 0, 0, 0, 0],
								[.125, .25, .5, 1, 0, 0, 0, 0],
								[0, 0, 0, 0, 2, 1, 0, 0],
								[0, 0, 0, 0, 1, 2, 0, 0],
								[0, 0, 0, 0, 0, 0, 2, 1],
								[0, 0, 0, 0, 0, 0, 1, 2]])


	else:

		state = info['filter']['mean']
		covariance = info['filter']['covariance']

	updated_info = bayesian_updating(state, covariance, tf_output)	
	info['P-Score'] = obj['P-Score']
	info['box'] = obj['box']
	info['last_detected'] = count
	info['filter']['mean'] = updated_info[0]
	info['filter']['covariance'] = updated_info[1]
	current_objects['active_objects'][obj_class][parent] = info

	return current_objects



def update_parent(current_objects, candidates, obj_class, obj, count):

	names = list(candidates)
	parent = ''
	if len(names) == 1:
		parent = names[0]
	else:
		parent = most_similar(current_objects, candidates, obj_class, obj)

	current_objects = linear_filter(current_objects, parent, obj_class, obj, count)
	return current_objects



def update_filter(current_objects, count):

	for obj_class in current_objects['active_objects']:
		for name in current_objects['active_objects'][obj_class]:
			info = current_objects['active_objects'][obj_class][name]

			if info['last_detected'] < count and info['filter']['mean'] != 'x':
				updated_info = bayesian_updating(info['filter']['mean'], info['filter']['covariance'])
				current_objects['active_objects'][obj_class][name]['filter']['mean'] = updated_info[0]
				current_objects['active_objects'][obj_class][name]['filter']['covariance'] = updated_info[1]

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

				if not candidates:
					current_objects = fresh_object(current_objects, obj_class, obj, count)

				else:
					current_objects = update_parent(current_objects, candidates, obj_class, obj, count)


	current_objects = update_filter(current_objects, count)


	return current_objects















def update_objects(current_objects, mapped, temp_objects, obj_class, count):

	for parent in mapped:
		
		### Need to handle cases of dropout and exiting
		if mapped[parent] == 'E':
			x = 0
		elif mapped[parent] == 'D':
			x = 0
		
		else:
			index = mapped[obj]
			child = temp_objects[3][obj_class][index]
			current_objects = linear_filter(current_objects, parent, obj_class, child, count)
	
	return current_objects



def identify_child(vector_count, counts, position):

	length = vector_count[obj]
	index = position + 1
	if index = length:
		return 'E'
	
	subtree_size = (counts[2] + 1) * (counts[1] + 1) + 1
	subtree = index // subtree_size
	modulo = index % subtree_size
	if modulo != 0:
		subtree = subtree + 1

	if subtree > counts[3]:
		return 'D'
	else:
		return subtree




def identify_unmapped(parent_data, vector_count, counts, mapped, key):

	if not mapped:
		return list(range(vector_count[key]))

	children = []
	for obj in mapped:
		if mapped[obj] != 'D' and mapped[obj] != 'E':
			children.append(mapped[obj])
	if not children:
		return list(range(vector_count[key]))

	viable = []
	subtree_size = (counts[2] + 1) * (counts[1] + 1) + 1
	for obj in range(counts[3]):
		if (obj + 1) not in children:
			for k in range(subtree_size):
				viable.append((obj * subtree_size) + k)		
	if parent_data[key]:
		for k in range(subtree_size):
			viable.append((counts[3] * subtree_size) + k)

	return viable


def multinormal_pdf(mean, covariance, observation):

	top = np.multiply(np.multiply(np.transpose(np.subtract(observation, mean)), np.linalg.inv(covariance)), 
						np.subtract(observation, mean))
	numerator = math.exp((-.5) * top)

	bottom = ((2 * math.pi) ** 4) * np.linalg.det(covariance)
	denominator = math.sqrt(bottom)

	likelihood = numerator / denominator
	return likelihood




def likelihood(current_objects, temp_objects, key, i='E', j='E', k='E'):
	

	## Need to compute likelihoods of dropout and exit 
	if i == 'E':
		return -5
	elif j == 'E':
		return -5
	elif k == 'E':
		return -5


	if i == 'D':
		return -5
	elif j == 'D':
		return -5
	elif k == 'D':
		return -5


	identifiers = key.split('-')
	obj_class = identifiers[1]

	parent = current_objects['active_objects'][obj_class][key]
	temp_3 = temp_objects[3][obj_class][i]['box']
	temp_2 = temp_objects[2][obj_class][j]['box']
	temp_1 = temp_objects[1][obj_class][k]['box']

	temp_3_np = np.array([temp_3['xmin'], temp_3['xmax'], temp_3['ymin'], temp_3['ymax']])
	temp_2_np = np.array([temp_2['xmin'], temp_2['xmax'], temp_2['ymin'], temp_2['ymax']])
	temp_1_np = np.array([temp_1['xmin'], temp_1['xmax'], temp_1['ymin'], temp_1['ymax']])

	
	if parent['filter']['mean'] == 'x':
		###### Need to choose a universal prior distribution  

		return -5

	else:
		parent_mean = parent['filter']['mean']
		parent_covariance = parent['filter']['covariance']

		one_step = bayesian_updating(parent_mean, parent_covariance, temp_3_np)
		two_step = bayesian_updating(one_step[0], one_step[1], temp_2_np)

		first_obs = multinormal_pdf(parent_mean[0:4], parent_covariance[0:4][0:4], temp_3_np)
		second_obs = multinormal_pdf(one_step[0][0:4], one_step[1][0:4][0:4], temp_2_np)
		third_obs = multinormal_pdf(two_step[0][0:4], two_step[1][0:4][0:4], temp_1_np)

		likelihood = first_obs * second_obs * third_obs
		return likelihood





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

	current_objects['active_objects'][obj_class].update({name: d})
	return current_objects



def tree_search(temp_objects, current_objects, count):

	if temp_objects[3] == {}:
		##### TBD
		return 'empty'

	objs = temp_objects[3]
	for obj_class in objs:
		if obj_class not in current_objects['active_classes']:
			for k in range(objs[obj_class]['count']):
				current_objects = fresh_object(current_objects, obj_class, objs[obj_class][k], count-3)
			del objs[obj_class]

	for obj_class in objs:

		parent_data = {}
		for parent in current_objects['active_objects'][obj_class]:
			if parent['filter']['mean'] == 'x':
				parent_data[parent] = False
			else:
				parent_data[parent] = True


		counts = {1: temp_objects[1][obj_class]['count'],
					2: temp_objects[2][obj_class]['count'],
					3: temp_objects[3][obj_class]['count']}

		vector_count = {}
		for key in parent_data:
			if parent_data[key] == True:
				vector_count[key] = (counts[3]+1) * (counts[2]+1) * (counts[1]+1) + counts[3] + 2
			else:
				vector_count[key] = (counts[3]) * (counts[2]+1) * (counts[1]+1) + counts[3] + 1

		probabilities = {}
		for key in vector_count:
			
			probabilities[key] = np.zeros((1, vector_count[key]))
			index = 0
			span = 0
			
			if parent_data[key]:
				span = counts[3] + 2
			else:
				span = counts[3] + 1

	
			for i in range(1, span):
				for j in range(1, counts[2] + 2):
					for k in range(1, counts[1] + 2):

						if i == (counts[3] + 1):
							i = 'D'
						if j == (counts[2] + 1):
							j = 'D'
						if k == (counts[1] + 1):
							k = 'E'

						x = likelihood(current_objects, temp_objects, key, i, j, k)
						probabilities[index] = x
						index = index + 1
				y = likelihood(current_objects, temp_objects, key, i, 'E')
				probabilities[index] = y
				index = index + 1
			z = likelihood(current_objects, temp_objects, key, 'E')
			probabilities[index] = z


		num = 0
		mapped = {}
		while (num < counts[3]):
			maximum = 0
			obj = 'x'
			position = 'a'

			if not probabilities:
				break

			for key in probabilities:
				
				viable = identify_unmapped(parent_data, vector_count, counts, mapped, key)
				for index in viable:
					if probabilities[obj][index] > maximum:
						maximum = probabilities[obj][index]
						obj = key
						position = index


			child = identify_child(vector_count, counts, position)
			mapped[obj] = child

			if child != 'D' and child != 'E':
				del probabilities[obj]
				num = num + 1

		current_objects = update_objects(current_objects, mapped, temp_objects, obj_class, count)

	return current_objects





def pastDS_update(current_objects, past_objects, count):

	decommission = []

	for obj_class in current_objects['active_objects']:
		for name in current_objects['active_objects'][obj_class]:
			
			last = current_objects['active_objects'][obj_class][name]['last_detected']
			if last < (count - 5):
				info = (obj_class, name)
				decommission.append(info)


	for entry in decommission:
		
		obj_class = entry[0]
		name = entry[1]
		d = (current_objects['active_objects'][obj_class]).pop(name)
		dd = {name: d}

		current_objects['active'].remove(name)
		if obj_class not in current_objects['active_objects']:
			current_objects['active_classes'].remove(obj_class)
		past_objects['inactive'].append(name)
		if obj_class not in past_objects['inactive_classes']:
			past_objects['inactive_classes'].append(obj_class)

		if not past_objects['inactive_objects']:
			past_objects['inactive_objects'] = {obj_class: dd}
		elif obj_class not in past_objects['inactive_objects']:
			past_objects['inactive_objects'][obj_class] = dd
		else:
			past_objects['inactive_objects'][obj_class][name] = d

	data = (current_objects, past_objects)
	return data


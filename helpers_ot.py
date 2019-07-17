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

	current_objects['active_objects'][obj_class].update({name: d})


	return current_objects



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



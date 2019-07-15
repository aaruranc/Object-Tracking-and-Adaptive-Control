import numpy as np
import pandas as pd
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile

from distutils.version import StrictVersion
from collections import defaultdict
from io import StringIO
# from matplotlib import pyplot as plt
from PIL import Image
from object_detection.utils import ops as utils_ops

if StrictVersion(tf.__version__) < StrictVersion('1.9.0'):
  raise ImportError('Please upgrade your TensorFlow installation to v1.9.* or later!')

from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util

#HELPERS
def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)


def run_inference_for_single_image(image, graph):
  with graph.as_default():
    with tf.Session() as sess:
      # Get handles to input and output tensors
      ops = tf.get_default_graph().get_operations()
      all_tensor_names = {output.name for op in ops for output in op.outputs}
      tensor_dict = {}
      for key in [
          'num_detections', 'detection_boxes', 'detection_scores',
          'detection_classes', 'detection_masks'
      ]:
        tensor_name = key + ':0'
        if tensor_name in all_tensor_names:
          tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
              tensor_name)
      if 'detection_masks' in tensor_dict:
        # The following processing is only for single image
        detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
        detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
        # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
        real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
        detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
        detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
            detection_masks, detection_boxes, image.shape[0], image.shape[1])
        detection_masks_reframed = tf.cast(
            tf.greater(detection_masks_reframed, 0.5), tf.uint8)
        # Follow the convention by adding back the batch dimension
        tensor_dict['detection_masks'] = tf.expand_dims(
            detection_masks_reframed, 0)
      image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

      # Run inference
      output_dict = sess.run(tensor_dict,
                             feed_dict={image_tensor: np.expand_dims(image, 0)})

      # all outputs are float32 numpy arrays, so convert types as appropriate
      output_dict['num_detections'] = int(output_dict['num_detections'][0])
      output_dict['detection_classes'] = output_dict[
          'detection_classes'][0].astype(np.uint8)
      output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
      output_dict['detection_scores'] = output_dict['detection_scores'][0]
      if 'detection_masks' in output_dict:
        output_dict['detection_masks'] = output_dict['detection_masks'][0]
  return output_dict

def image_list(images, dummy_text, PATH_TO_TEST_IMAGES_DIR):
	TEST_IMAGE_PATHS = []
	count = 1
	while count < images:
		length = len(str(count))
		dummy_num = ''
		if length < 5:
			num = 5 - length
			while num != 0:
				dummy_num = dummy_num + '0'
				num = num - 1
		filename = dummy_text + dummy_num + str(count) + '.jpg'
		# print(filename)
		TEST_IMAGE_PATHS.append(os.path.join('datasets/' + PATH_TO_TEST_IMAGES_DIR, filename))
		count = count + 1
	return TEST_IMAGE_PATHS


def update_data(output_dict, data, image_path):
	temp = data
	box_ctr = 0;
	box_count = output_dict['num_detections']
	if box_count == 0:
	  	info = (image_path[-11:-4], 0, '', '', '', '', '', '')
	  	temp.append(info)  
	
	while box_ctr < box_count :
	  	xmin = output_dict['detection_boxes'][box_ctr][1]
	  	xmax = output_dict['detection_boxes'][box_ctr][3]
	  	ymin = output_dict['detection_boxes'][box_ctr][0]
	  	ymax = output_dict['detection_boxes'][box_ctr][2]
	  	obj_class = output_dict['detection_classes'][box_ctr]
	  	obj_score = output_dict['detection_scores'][box_ctr]

	  	if box_ctr == 0:
	  		info = (image_path[-11:-4], box_count, obj_class, obj_score, xmin, xmax, ymin, ymax)
	  	else:
	  		info = ('', '', obj_class, obj_score, xmin, xmax, ymin, ymax)

	  	temp.append(info)
	  	box_ctr = box_ctr + 1

	return temp

def tensorflow_detection(MODEL_NAME, FROZEN_GRAPH, LABELS, info):

	# Faster R-CNN Model
	# MODEL_NAME = 'faster_rcnn_resnet50_coco_2018_01_28'
	
	# Path to frozen detection graph. This is the actual model that is used for the object detection.
	PATH_TO_FROZEN_GRAPH = os.path.join('parameters', MODEL_NAME, FROZEN_GRAPH)

	# List of the strings that is used to add correct label for each box.
	PATH_TO_LABELS = os.path.join('parameters', 'data', LABELS)

	# LOAD MODEL INTO MEMORY
	detection_graph = tf.Graph()
	with detection_graph.as_default():
	  od_graph_def = tf.GraphDef()
	  with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
	    serialized_graph = fid.read()
	    od_graph_def.ParseFromString(serialized_graph)
	    tf.import_graph_def(od_graph_def, name='')

	#Label Map
	category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)
	images = info['images']
	dummy_text = info['dummy_text']
	directory = info['directory']

	TEST_IMAGE_PATHS = image_list(images, dummy_text, directory)
	if not TEST_IMAGE_PATHS:
		return pd.DataFrame()

	# Size, in inches, of the output images.
	IMAGE_SIZE = (12, 8)

	data = []
	count = 1
	for image_path in TEST_IMAGE_PATHS:
	  print("image" + str(count) + " processing")
	  print(str(float(100 * count) / images) + "%")
	  image = Image.open(image_path)
	  # the array based representation of the image will be used later in order to prepare the
	  # result image with boxes and labels on it.
	  image_np = load_image_into_numpy_array(image)
	  # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
	  image_np_expanded = np.expand_dims(image_np, axis=0)
	  # Actual detection.
	  output_dict = run_inference_for_single_image(image_np, detection_graph)
	  
	  # Visualization of the results of a detection.
	  # vis_util.visualize_boxes_and_labels_on_image_array(
	  #     image_np,
	  #     output_dict['detection_boxes'],
	  #     output_dict['detection_classes'],
	  #     output_dict['detection_scores'],
	  #     category_index,
	  #     instance_masks=output_dict.get('detection_masks'),
	  #     use_normalized_coordinates=True,
	  #     line_thickness=8)
	  # plt.figure(figsize=IMAGE_SIZE)
	  # plt.imshow(image_np)
	  # print(output_dict)
	  
	  data = update_data(output_dict, data, image_path)
	  count = count + 1
	
	print('')
	cols = ['Image', 'NumDetected', 'Class', 'Score', 'xmin', 'xmax', 'ymin', 'ymax']
	df = pd.DataFrame(data, columns=cols)
	return df



def structured_output(MODEL_NAME, FROZEN_GRAPH, LABELS, image_path):

	PATH_TO_FROZEN_GRAPH = os.path.join('parameters', MODEL_NAME, FROZEN_GRAPH)
	PATH_TO_LABELS = os.path.join('parameters', 'data', LABELS)
	
	detection_graph = tf.Graph()
	with detection_graph.as_default():
	  od_graph_def = tf.GraphDef()
	  with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
	    serialized_graph = fid.read()
	    od_graph_def.ParseFromString(serialized_graph)
	    tf.import_graph_def(od_graph_def, name='')

	category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

	IMAGE_SIZE = (12, 8)

	image = Image.open(image_path)
	image_np = load_image_into_numpy_array(image)
	image_np_expanded = np.expand_dims(image_np, axis=0)
	output_dict = run_inference_for_single_image(image_np, detection_graph)

	d = {}
	box_ctr = 0;
	box_count = output_dict['num_detections']
	if box_count == 0:
	  	return 'none'
	
	curr_class = int(output_dict['detection_classes'][box_ctr])
	class_num = 0
	while box_ctr < box_count :
		obj_score = output_dict['detection_scores'][box_ctr]
		xmin = output_dict['detection_boxes'][box_ctr][1]
		xmax = output_dict['detection_boxes'][box_ctr][3]
		ymin = output_dict['detection_boxes'][box_ctr][0]
		ymax = output_dict['detection_boxes'][box_ctr][2]
		obj_class = output_dict['detection_classes'][box_ctr]

		if int(curr_class) != int(obj_class):
			curr_class = int(obj_class)
			class_num = 1
		else:
			class_num = class_num + 1

		obj = {'P-Score': obj_score, 'box': {'xmin': xmin, 'xmax': xmax, 'ymin': ymin, 'ymax': ymax}}
		name = 'obj-' + str(curr_class) + '.0' '-' + str(class_num)
		dd = {name: obj}

		class_name = str(curr_class) + '.0'
		if curr_class not in d:
			d[class_name] = dd
		else:
			d[class_name].update(dd)
		box_ctr = box_ctr + 1

	return d




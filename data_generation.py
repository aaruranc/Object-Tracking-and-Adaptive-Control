import os
from helpers_dg import user_input, name_objects, impute
from basic_detection import tensorflow_detection

if __name__ == '__main__':

	# Faster R-CNN Model chosen for Flanagan Lab Research
	MODEL_NAME = 'faster_rcnn_resnet50_coco_2018_01_28'
	FROZEN_GRAPH = 'frozen_inference_graph.pb'
	LABELS = 'mscoco_label_map.pbtxt'


	datasets = {'Forward_10204_1498': {'images': 2898, 'dummy_text': 'Forward_10204_1498-f-00'}, 
				'Forward_10204_1780': {'images': 13901, 'dummy_text': 'Forward_10204_1780-f-00'}, 
				'Forward_10204_1796': {'images': 6148, 'dummy_text': 'Forward_10204_1796-f-00'},
				'Forward_10204_1834': {'images':15349, 'dummy_text': 'Forward_10204_1834-f-00'}, 
				'Forward_10204_1844': {'images': 12331, 'dummy_text':'Forward_10204_1844-f-00'},
				'Forward_10205_0127': {'images': 3544, 'dummy_text':'Forward_10205_0127-f-00'}, 
				'Forward_10205_0827': {'images': 51299, 'dummy_text':'Forward_10205_0827-f-00'}
				}

	for key in datasets:
		print(key)
		print('')
		datasets[key].update({'directory': key})
		df = tensorflow_detection(MODEL_NAME, FROZEN_GRAPH, LABELS, datasets[key])
		if df.empty:
			print('Input Error')

		else:

			dir_name = 'output/' + datasets[key]['directory']

			if not os.path.exists(dir_name):
				os.mkdir(dir_name)

			# df2 = name_objects(df)
			# df3 = impute(df2)

			file = dir_name + '/' + "classified_images.csv"
			# file2 = dir_name + '/' + "labeled_images.csv"
			# file3 = dir_name + '/' + "imputed_images.csv"
			
			df.to_csv(file, index=False)
			# df2.to_csv(file2, index=False)
			# df3.to_csv(file3, index=False)





#2000 draws for MCMC
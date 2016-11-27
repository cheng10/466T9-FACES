import tensorflow as tf, sys
import os, csv, collections

DIR = sys.argv[1]
res = {}
writer_res = {}

# Loads label file, strips off carriage return
label_lines = [line.rstrip() for line
                   in tf.gfile.GFile("/tf_files/retrained_labels.txt")]

# Unpersists graph from file
with tf.gfile.FastGFile("/tf_files/retrained_graph.pb", 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _ = tf.import_graph_def(graph_def, name='')

with tf.Session() as sess:
    # Feed the image_data as input to the graph and get first prediction
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')

    for image_name in os.listdir(DIR): 
        image_path = DIR+image_name
        # Read in the image_data
        image_data = tf.gfile.FastGFile(image_path, 'rb').read()

        predictions = sess.run(softmax_tensor, \
                 {'DecodeJpeg/contents:0': image_data})

        # Sort to show labels of first prediction in order of confidence
        top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]

        print image_name
        for node_id in top_k:
            human_string = label_lines[node_id]
            if human_string == 'female':
                continue
            score = predictions[0][node_id]
            print('%s (score = %.5f)' % (human_string, score))
            res[image_name[0:6]] = score

print res

for i in range(283, 476):
    writer_res[i] = 0

for key, value in res.iteritems():
    writer_res[int(key[1:4])] += value
print writer_res 

ordered_res = collections.OrderedDict(sorted(writer_res.items()))
print ordered_res

for key, value in ordered_res.items():
    ordered_res[key] = value / 4

with open('res.csv', 'wb') as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=' ',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for key,value in ordered_res.iteritems():
        spamwriter.writerow([key, value])

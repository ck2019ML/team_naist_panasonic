#! /usr/bin/env python

from net.build import TFNet
from tensorflow import flags
import os

flags.DEFINE_string("test", "./test/", "path to testing directory")
flags.DEFINE_string("binary", "./bin/", "path to .weights directory")
flags.DEFINE_string("config", "./cfg/", "path to .cfg directory")
flags.DEFINE_string("dataset", "../../../../../VOCdevkit/VOC2012/JPEGImages", "path to dataset directory")
flags.DEFINE_string("backup", "./ckpt/", "path to backup folder")
flags.DEFINE_string("summary", "./summary/", "path to TensorBoard summaries directory")
flags.DEFINE_string("annotation", "../../../../../VOCdevkit/VOC2012/Annotations/", "path to annotation directory")
flags.DEFINE_float("threshold", 0.1, "detection threshold")
flags.DEFINE_string("model", "./cfg/tiny-yolo-voc.cfg", "configuration of choice")
flags.DEFINE_string("log","","Simple Log file")
flags.DEFINE_string("trainer","adam","training algorithm")
flags.DEFINE_float("momentum", 0.0, "applicable for rmsprop and momentum optimizers")
flags.DEFINE_boolean("verbalise", True, "say out loud while building graph")
flags.DEFINE_boolean("train", False, "train the whole net")
flags.DEFINE_string("load", "/home/tnp/catkin_ws/src/team-naist-panasonic/yolo_light/scripts/bin/tiny-yolo-voc.weights", "how to initialize the net? Either from .weights or a checkpoint, or even from scratch")
flags.DEFINE_boolean("savepb", False, "save net and weight to a .pb file")
flags.DEFINE_float("gpu", 0.8, "how much gpu (from 0.0 to 1.0)")
flags.DEFINE_float("lr", 1e-5, "learning rate")
flags.DEFINE_integer("keep",10,"Number of most recent training results to save")
flags.DEFINE_integer("batch", 20, "batch size")
flags.DEFINE_integer("epoch", 300000, "number of epoch")
flags.DEFINE_integer("save", 15000, "save checkpoint every ? training examples")
flags.DEFINE_string("demo", '', "demo on webcam")
flags.DEFINE_boolean("profile", False, "profile")
flags.DEFINE_boolean("json", False, "Outputs bounding box information in json format.")
flags.DEFINE_boolean("saveVideo", False, "Records video from input video or camera")
FLAGS = flags.FLAGS

# make sure all necessary dirs exist
def get_dir(dirs):
	for d in dirs:
		this = os.path.abspath(os.path.join(os.path.curdir, d))
		if not os.path.exists(this): os.makedirs(this)
get_dir([FLAGS.test, FLAGS.binary, FLAGS.backup, os.path.join(FLAGS.test,'out'), FLAGS.summary])

# fix FLAGS.load to appropriate type
try: FLAGS.load = int(FLAGS.load)
except: pass

tfnet = TFNet(FLAGS)

if FLAGS.profile:
	tfnet.framework.profile(tfnet)
	exit()

if FLAGS.demo:
	tfnet.camera(FLAGS.demo, FLAGS.saveVideo)
	exit()

if FLAGS.train:
	print('Enter training ...'); tfnet.train()
	if not FLAGS.savepb: exit('Training finished')

if FLAGS.savepb:
	print('Rebuild a constant version ...')
	tfnet.savepb(); exit('Done')

tfnet.predict()

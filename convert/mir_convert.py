
'''
extracting function of all features from music data

for extracting feature from mp3 (or other), ffmpeg is required
for extracting chord, sonic-annotator, harmtrace, qm-vampplugins and nnls-chroma are required
for extracting key, sonic-annotator and qm-vampplugins required
for extracting mfcc, librosa is required
for extracting rhythm pattern, rp_extract is required
'''


import os
import librosa
import numpy as np
import subprocess

logdir = "./convert/log/"
vampdir = "./convert/vamp/"
vampkey = "./convert/vamp/keydetector.txt"
vampkeyShort = "./convert/vamp/keydetector_short.txt"
tempdir = "./convert/temp/"
rppath = "./convert/rp_extract/rp_extract_batch.py"

# extract chord progression with harmtrace (with sonic-annotator and vamp plugins)
# output is "<fileName>.chord.csv"
def recognise_chord(filePath,outputDir,outputName,debug):
	print("start recognise chord {0}".format(filePath))
	cmd = ["harmtrace","recognise","-g","pop","-m","mptree"
	,"-i",filePath
	,"-o",outputDir
	,"-v",vampdir
	,"-f",outputDir
	,"-w",logdir
	]
	p = subprocess.Popen(cmd,shell=False, stdout = subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)
	p.wait()
	so = p.stdout.read()
	se = p.stderr.read()
	if(debug):
		print("end recognise")
		print("stdout:"+so)
		print("stderr:"+se)
	baseName = filePath.split("/")[-1].replace(".wav","")
	bothChromaName = "_vamp_nnls-chroma_nnls-chroma_bothchroma.csv"
	chromaName = "_vamp_nnls-chroma_nnls-chroma_chroma.csv"
	beatsName = "_vamp_qm-vamp-plugins_qm-barbeattracker_beats.csv"
	chordName = ".wav.chords.txt"
	chordRename = "_chord.txt"
	os.rename(outputDir+baseName+bothChromaName,outputDir+outputName+"_bothchroma.csv")
	os.rename(outputDir+baseName+chromaName,outputDir+outputName+"_chroma.csv")
	os.rename(outputDir+baseName+beatsName,outputDir+outputName+"_beats.csv")
	os.rename(outputDir+baseName+chordName,outputDir+outputName+"_chord.txt")

# extract key changes with sonic-annotator and vamp skelton
def recognise_key(filePath,outputDir,outputName,debug,short=False):
	print("start recognise key {0}".format(filePath))
	outputPath = outputDir+outputName+"_key.csv"
	if(not short):
		cmd = ["sonic-annotator"
		,"-t",vampkey
		,filePath
		,"-w","csv"
		,"--csv-one-file",outputPath
		,"--csv-force"
		]
	else:
		cmd = ["sonic-annotator"
		,"-t",vampkeyShort
		,filePath
		,"-w","csv"
		,"--csv-one-file",outputPath
		,"--csv-force"
		]
	p = subprocess.Popen(cmd,shell=False, stdout = subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)
	p.wait()
	so = p.stdout.read()
	se = p.stderr.read()
	if(debug):
		print("end recognise")
		print("stdout:"+so)
		print("stderr:"+se)
	if("ERROR" in se):
		if("differ from required 16384" in se):
			if(not short):
				print("keydetection failed, retry with short vamp key")
				recognise_key(filePath,outputDir,outputName,debug,short=True)

# extract mfcc and hpss mfcc with librosa
def recognise_mfcc(filePath,outputDir,outputName,debug):

	print("start decompose harmonic/percussive and extract mfcc {0}".format(filePath))
	y,sr = librosa.load(filePath)
	mfcc = librosa.feature.mfcc(y=y,sr=sr)
	mfcc = np.transpose(mfcc)
	basePath = outputDir+outputName;
	np.savetxt(basePath+"_normal_mfcc.csv",mfcc,delimiter=",")
	harmonic_sep = 3.0
	percussive_sep = 3.0
	h,p = librosa.effects.hpss(y,margin=(harmonic_sep,percussive_sep))
	hmfcc = librosa.feature.mfcc(y=h,sr=sr)
	hmfcc = np.transpose(hmfcc)
	np.savetxt(basePath+"_harmonic_mfcc.csv",hmfcc,delimiter=",")
	pmfcc = librosa.feature.mfcc(y=p,sr=sr)
	pmfcc = np.transpose(pmfcc)
	np.savetxt(basePath+"_percussive_mfcc.csv",pmfcc,delimiter=",")

# extract rhythm patter with rp_extract
def recognise_rp(filePath,outputDir,outputName,debug):
	print("start extract rhythm patters {0}".format(filePath))
	outputPath = outputDir+outputName+"_key.csv"
	cmd = ["python"
	,rppath
	,filePath
	,outputDir+outputName
	]
	p = subprocess.Popen(cmd,shell=False, stdout = subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)
	p.wait()
	so = p.stdout.read()
	se = p.stderr.read()
	if(debug):
		print("end recognise")
		print("stdout:"+so)
		print("stderr:"+se)


# make temporal wav from mp3
def convert(filePath,outputName,debug):
	outputPath = tempdir+outputName+".wav"
	print("convert {0} -> {1}".format(filePath,outputPath))
	cmd = ["ffmpeg","-y","-loglevel","error","-i",filePath,outputPath]
	p = subprocess.Popen(cmd,shell=False, stdout = subprocess.PIPE, stderr=subprocess.PIPE,universal_newlines=True)
	p.wait()
	so = p.stdout.read()
	se = p.stderr.read()
	if(debug):
		print("end convert")
		print("stdout:"+so)
		print("stderr:"+se)
	return outputPath

# clean temporal wav file
def clean(fnc,debug):
	if(debug):
		print("remove {0}".format(fnc))
	os.remove(fnc)

# extract features
# filePath : target file path
# outputName : name of feature output
# outputdir : feature output directory
# chord,key,mfcc,rp : extract feature if True
def process(filePath,outputName,outputdir,chord=True,key=True,mfcc=True,rp=True,debug=False):
	conv = False
	if(not filePath.endswith(".wav")):
		filePath = convert(filePath,outputName,debug)
		conv = True
	else:
		filePath = filePath

	if(chord):
		recognise_chord(filePath,outputdir,outputName,debug)
	if(key):
		recognise_key(filePath,outputdir,outputName,debug)
	if(mfcc):
		recognise_mfcc(filePath,outputdir,outputName,debug)
	if(rp):
		recognise_rp(filePath,outputdir,outputName,debug)

	if(conv):
		clean(filePath,debug)

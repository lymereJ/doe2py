import os
import sys
import subprocess 
import shutil
import pyforms
import json
import re

from pyforms import BaseWidget
from pyforms.Controls import ControlText
from pyforms.Controls import ControlButton
from pyforms.Controls import ControlFile
from pyforms.Controls import ControlCombo
from pyforms.Controls import ControlLabel
from pysettings import conf;
import settings
conf+=settings


def DOE2ENV(act,inpf,wthf,ver,path):
	"""
	Manages the environement to run DOE-2 simulations.
	A few different arguments can be passed to the function in order to perform different tasks:
	- SETUP: create environement variables to run DOE-2
	- RESET: not yet implemented
	- CLEAN: clean the root simulation folder from the binary files creates by DOE-2 during a simulation.
	"""
	if act.upper() == "SETUP":
		os.environ["INPUT2.TMP"]=inpf+".inp"
		os.environ["BDLKEY.BIN"]=path+"\\"+ver+"\\BDLKEY.bin"
		os.environ["BDLLIB.DAT"]=path+"\\"+ver+"\\BDLLIB.dat"
		os.environ["BDLDFT.DAT"]=path+"\\"+ver+"\\BDLDFT.dat"
		os.environ["HDRFIL.BIN"]=path+"\\"+ver+"\\HDRFIL.bin"
		os.environ["TDVCTZ.BIN"]=path+"\\"+ver+"\\TDVCTZ.bin"
		os.environ["WEATHER.BIN"]=wthf
		os.environ["DOEBDL.OUT"]=inpf+".bdl"
		os.environ["DOESIM.OUT"]=inpf+".sim"
		os.environ["DOEBDL.LOG"]=inpf+".bdllog"
		os.environ["DOESIM.LOG"]=inpf+".simlog"
		os.environ["USRLIB.DAT"]=path+"\\"+ver+"\\USRLIB.dat"
		os.environ["for022"]=inpf+".022"
		os.environ["for080"]=inpf+".080"
		os.environ["LDSOUT.TMP"]=inpf+".ldo"
		os.environ["SYSOUT.TMP"]=inpf+".syo"
		os.environ["PLTOUT.TMP"]=inpf+".plo"
		os.environ["DSNFIL.TMP"]=inpf+".dsn"
		os.environ["CTRL.TMP"]=inpf+".ctr"
		os.environ["STDFIL.TMP"]=inpf+".std"
		os.environ["HRREP.TMP"]=inpf+".hrp"
		os.environ["DOEHRREP.BIN"]=inpf+".lin"
		os.environ["DOEHRREP.BIN"]=inpf+".sin"
		os.environ["DOEREP.BIN"]=inpf+".lrp"
		os.environ["DOEREP.BIN"]=inpf+".srp"
		os.environ["DOEREP.BIN"]=inpf+".erp"
	elif act.upper() == "RESET":
		pass
	elif act.upper() == "CLEAN":
		if os.path.exists(path+"\\DOEHRREP.lin"):
			shutil.move(path+"\\DOEHRREP.lin",inpf+".lin")							
			if os.path.exists(path+"\\DOEHRREP.lin"):
				os.remove(path+"\\DOEHRREP.lin")
		if os.path.exists(path+"\\DOEHRREP.sin"):
			shutil.move(path+"\\DOEHRREP.sin",inpf+".sin")			
			if os.path.exists(path+"\\DOEHRREP.sin"):
				os.remove(path+"\\DOEHRREP.sin")			
		if os.path.exists(path+"\\DOEREP.erp"):
			shutil.move(path+"\\DOEREP.erp",inpf+".erp")			
			if os.path.exists(path+"\\DOEHRREP.erp"):
				os.remove(path+"\\DOEHRREP.erp")			
		if os.path.exists(path+"\\DOEREP.lrp"):
			shutil.move(path+"\\DOEREP.lrp",inpf+".lrp")						
			if os.path.exists(path+"\\DOEHRREP.lrp"):
				os.remove(path+"\\DOEHRREP.lrp")			
		if os.path.exists(path+"\\DOEREP.srp"):
			shutil.move(path+"\\DOEREP.srp",inpf+".srp")
			if os.path.exists(path+"\\DOEHRREP.srp"):
				os.remove(path+"\\DOEHRREP.srp")			
			
def DOEBDL(dir):
	"""
	Run BDL.
	"""
	subprocess.call(dir+"DOEBDL.exe")

def DOESIM(dir):
	"""
	Run DOE-2.
	"""
	subprocess.call(dir+"DOESIM.exe")
	
def RunDOE2(inpf, wthf, ver, path):
	"""
	Setup, run and clean-up a DOE-2 simulation for a particular input and weather file for any version of DOE-2 available.
	"""
	try: 
		open(inpf+".inp")
		try: 
			open(wthf)
	
			print "===== DOE-2 Simulation ====="
			print "Input File: "+inpf
			print "Weather File: "+wthf
			print "DOE-2 version:"+ver+"\n"
			
			DOE2ENV("SETUP",inpf,wthf,ver,path)
			DOEBDL(path+"\\"+ver+"\\")
			DOESIM(path+"\\"+ver+"\\")
			DOE2ENV("CLEAN",inpf,wthf,ver,path)
			
			print "\n===== Simulation Completed ====="
			
		except:
			print "Weather file ("+wthf+") does not exist."
	except:
		print "Input file ("+inpf+") does not exist."

def RunBatchDOE2(batch):
	runs = open(batch,'r').read().split('\n')
	for run in runs:
		print run
		run = run.split(',')
		RunDOE2(run[0],run[1],run[2],run[3])
	print "\n===== Batch Simulation Completed ====="

def ImportLib(ver, lib, path):
	"""
	Import a user defined library.
	"""
	shutil.copy(lib, path+"\\"+ver+"\\USRLIB.DAT")
	
def ExtractReports(SIMf,*args):
	"""
	Extract some report out of a SIM file.
	First argument should be the path to the sim file (include the extension).
	Other arguments the names of the reports.
	"""
	SIM = open(SIMf,'r').read().split('\n')
	OUT = open(SIMf[:-4]+"-ext_rpts.SIM",'w+')
	InReport = False
	for j in range(0,len(args[0])):
		Report = args[0][j]
		for i in range(0,len(SIM)):
			if re.search(r'REPORT- '+str(Report)+'.*.',SIM[i]) <> None:
				InReport = True
			if re.search(r'REPORT- .*.',SIM[i]) <> None and re.search(r'REPORT- '+str(Report)+'.*.',SIM[i]) == None and InReport == True:
				InReport = False
			if InReport == True:
				OUT.write(SIM[i]+'\n')	
	
class DOE2py_Utility(BaseWidget):
	
	def __init__(self):
		super(DOE2py_Utility,self).__init__('DOE2py Utility')

		self._Input 	= ControlFile('Input file')
		self._Weather 	= ControlFile('Weather file')
		self._Library 	= ControlFile('User Library')
		self._Version	= ControlCombo('DOE-2 Version')
		#self._Status_1	= ControlLabel('Simulation Status:')
		#self._Status_2	= ControlLabel('-')
		self._Run		= ControlButton('Run Simulation')
		self._Close		= ControlButton('Close')

		self._formset = ['',('  ','_Input','  '),
		                    ('', '_Weather', '' ),
							('', '_Library', '' ),
							('','_Version', '' ),
							('', '_Run', '' ),
							('','_Close',''),''] #('','_Status_1','','_Status_2', '' )
	
		self._Run.value = self.__RunAction
		self._Close.value = self.__CloseAction	
		
		with open('settings-gui.json') as data_file:    
			data = json.load(data_file)
			self._Input.value = data["lastinput"]
			self._Weather.value = data["lastweather"]
			self._Library.value = data["lastlibrary"]
		for i in range(0,len(data["doe2versions"])):
			self._Version.add_item(data["doe2versions"][i])
		
		
	def __RunAction(self):
		path = os.path.dirname(os.path.realpath(__file__))
		if self._Library.value <> "":
			ImportLib(self._Version.value, self._Library.value, path)
		RunDOE2(self._Input.value[:-4], self._Weather.value, self._Version.value, path)
		#self._Status_2.value = "Completed!"
	
	def __CloseAction(self):
		with open('settings-gui.json') as data_file:    
			data = json.load(data_file)
			data["lastinput"] = self._Input.value
			data["lastweather"] = self._Weather.value
			data["lastlibrary"] = self._Library.value
		with open('settings-gui.json','w') as data_file:			
			json.dump(data,data_file)
		sys.exit()	
	
if __name__ == '__main__':
	path = os.path.dirname(os.path.realpath(__file__))
	if sys.argv[1] == "RunDOE2":
		RunDOE2(sys.argv[2], sys.argv[3], sys.argv[4], path)
	elif sys.argv[1] == "RunBatchDOE2":
		RunBatchDOE2(sys.argv[2])
	elif sys.argv[1] == "Extract":
		ExtractReports(sys.argv[2],sys.argv[3:])
	elif sys.argv[1] == "GUI":
		pyforms.start_app( DOE2py_Utility )
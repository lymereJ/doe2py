import os
import sys
import subprocess 
import shutil

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
		if os.path.exists(path+"\\DOEHRREP.sin"):
			shutil.move(path+"\\DOEHRREP.sin",inpf+".sin")			
		if os.path.exists(path+"\\DOEREP.erp"):
			shutil.move(path+"\\DOEREP.erp",inpf+".erp")			
		if os.path.exists(path+"\\DOEREP.lrp"):
			shutil.move(path+"\\DOEREP.lrp",inpf+".lrp")						
		if os.path.exists(path+"\\DOEREP.srp"):
			shutil.move(path+"\\DOEREP.srp",inpf+".srp")
			
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
	
def RunDOE2(inpf, wthf, ver):
	"""
	Setup, run and clean-up a DOE-2 simulation for a particular input and weather file for any version of DOE-2 available.
	"""
	try: 
		open(inpf+".inp")
		try: 
			open(wthf)
			path = os.path.dirname(os.path.realpath(__file__))
	
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

if __name__ == '__main__':
	if sys.argv[1] == "RunDOE2":
		RunDOE2(sys.argv[2], sys.argv[3], sys.argv[4])
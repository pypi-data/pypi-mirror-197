import os

from tkinter import *

from autoappanalysis.model.Vm import Vm
from autoappanalysis.cmd.HostCommand import HostCommand

class Gui():
    def __init__(self, config) -> None:
        self.config = config
        # Tk window
        self.root = Tk()
        self.root.title('AutoAppAnalysis')
        self.root.resizable(False, False)

        # Layouts
        frameLeft = Frame(self.root)
        frameLeft.grid(row=0, column=0, padx=10, pady=10)
        frameLeftBottom = Frame(self.root)
        frameLeftBottom.grid(row=1, column=0, padx=10, pady=5)
        frameRight = Frame(self.root)
        frameRight.grid(row=0, column=1, padx=10, pady=10)
        frameRightBottom = Frame(self.root)
        frameRightBottom.grid(row=1, column=1, padx=10, pady=0)

        # Button
    #    self.rootBtn = Button(frameRight, text="Root", command=self._rootAVD)
    #    self.rootBtn.grid(row=0, column=0, pady=2, sticky="w")
        self.createBtn = Button(frameRight, text="Create Snapshot", command=self._createSnapshot)
        self.createBtn.grid(row=1, column=0, pady=2, sticky="w")
        self.decryptBtn = Button(frameRight, text="Decrypt Snapshots", command=self._decryptSnapshots)
        self.decryptBtn.grid(row=2, column=0, pady=2, sticky="w")
        self.createIdiffBtn = Button(frameRight, text="Create .idiff", command=self._createIdiff)
        self.createIdiffBtn.grid(row=3, column=0, pady=2, sticky="w")
        self.analyseIdiffBtn = Button(frameRight, text="Analyse .idiff", command=self._analyseIdiff)
        self.analyseIdiffBtn.grid(row=4, column=0, pady=2, sticky="w")
        self.analyseDbBtn = Button(frameRight, text="Analyse .db", command=self._analyseDb)
        self.analyseDbBtn.grid(row=5, column=0, pady=2, sticky="w")
        
        self.extractBtn = Button(frameRightBottom, text="Extract Files", command=self.extractFiles)
        self.extractBtn.grid(row=0, column=0, pady=2, sticky="w")

        # Text
        self.labelVm = Label(frameLeft, text='VM Name:')
        self.labelVm.grid(row=0, column=0, sticky="w")
        self.vmTxt = Text(frameLeft, height = 1, width = 20)
        self.vmTxt.insert('1.0', config["vm"])
        self.vmTxt.grid(row=1, column=0)
        
        self.labelUser = Label(frameLeft, text='VM User Name:')
        self.labelUser.grid(row=0, column=1, sticky="w")
        self.userTxt = Text(frameLeft, height = 1, width = 20)
        self.userTxt.insert('1.0', config["user"])
        self.userTxt.grid(row=1, column=1)
        
        self.labelPw = Label(frameLeft, text='VM Password:')
        self.labelPw.grid(row=0, column=2, sticky="w")
        self.pwTxt = Text(frameLeft, height = 1, width = 20)
        self.pwTxt.insert('1.0', config["pw"])
        self.pwTxt.grid(row=1, column=2)

        self.labelInputDir = Label(frameLeft, text='VM Input Directory:')
        self.labelInputDir.grid(row=2, column=0, sticky="w")
        self.inputTxt = Text(frameLeft, height = 1, width = 20)
        self.inputTxt.insert('1.0', config["input"])
        self.inputTxt.grid(row=3, column=0)

        self.labelOutputDir = Label(frameLeft, text='VM Output Directory:')
        self.labelOutputDir.grid(row=2, column=1, sticky="w")
        self.outputTxt = Text(frameLeft, height = 1, width = 20)
        self.outputTxt.insert('1.0', config["output"])
        self.outputTxt.grid(row=3, column=1)

        self.labelhOutputDir = Label(frameLeft, text='Host Output Directory:')
        self.labelhOutputDir.grid(row=2, column=2, sticky="w")
        self.hOutputTxt = Text(frameLeft, height = 1, width = 20)
        self.hOutputTxt.insert('1.0', config["outputHost"])
        self.hOutputTxt.grid(row=3, column=2)

        self.labelAvdPath = Label(frameLeft, text='AVD Path:')
        self.labelAvdPath.grid(row=4, column=0, sticky="w")
        self.avdPathTxt = Text(frameLeft, height = 1, width = 20)
        self.avdPathTxt.insert('1.0', config["snapshot"])
        self.avdPathTxt.grid(row=5, column=0)

        self.labelSName = Label(frameLeft, text='Snapshot Name:')
        self.labelSName.grid(row=4, column=1, sticky="w")
        self.sNameTxt = Text(frameLeft, height = 1, width = 20)
        self.sNameTxt.insert('1.0', "snapshot")
        self.sNameTxt.grid(row=5, column=1)

        self.labelSNumber = Label(frameLeft, text='Snapshot Number:')
        self.labelSNumber.grid(row=4, column=2, sticky="w")
        self.sNumberTxt = Text(frameLeft, height = 1, width = 20)
        self.sNumberTxt.insert('1.0', "1")
        self.sNumberTxt.grid(row=5, column=2)

        self.labelExtractFiles = Label(frameLeftBottom, text='AVD Files to be extracted:')
        self.labelExtractFiles.grid(row=6, column=0, sticky="w")
        self.extFilesTxt = Text(frameLeftBottom, height = 15, width = 60)
        
        for file in config["files"]:
            self.extFilesTxt.insert(END, file + "\n")
        self.extFilesTxt.grid(row=7, column=0)

    def _rootAVD(self):
        cmd = HostCommand.ADB_ROOT
        print(cmd)

    def extractFiles(self):
        outputHost = self.hOutputTxt.get("1.0", "end-1c")
        sName = self.sNameTxt.get("1.0", "end-1c")
        sNumber = self.sNumberTxt.get("1.0", "end-1c")
        paths_ = self.extFilesTxt.get("1.0", "end-1c")
        files = paths_.split("\n")
        hostPath = outputHost + "\\files\\" + sName + "." + sNumber
        for file in files: 
            if(file != ""):
                cmd = HostCommand.ADB_PULL.substitute(androidPath=file, hostPath=hostPath)
                print(cmd)

    def _createSnapshot(self):
        name_ = self.sNameTxt.get("1.0", "end-1c")
        number = self.sNumberTxt.get("1.0", "end-1c")
        cmd = HostCommand.ADB_SNAPSHOT_SAVE.substitute(name=name_ + "." + number)
        print(cmd)
        cmdResult = os.popen(cmd).read()
        print(cmdResult)

    def _getSnapshotList(self):
        snapshots = []
        avdDir = self.avdPathTxt.get("1.0", "end-1c")
        for path, dirs, files in os.walk(os.path.join(avdDir, "snapshots"), topdown=False):
            for name in dirs:
                if("default_boot" not in name):
                    snapshots.append(name)
        return snapshots
    
    def _decryptSnapshots(self):
        vm = self.vmTxt.get("1.0", "end-1c")
        user = self.userTxt.get("1.0", "end-1c")
        pw = self.pwTxt.get("1.0", "end-1c")
        avdPath = self.inputTxt.get("1.0", "end-1c")
        outputDir = self.outputTxt.get("1.0", "end-1c") + "/decrypted"
        snapshots = self._getSnapshotList()

        for snapshot in snapshots:
            py = "/usr/bin/python3"
            avdecrypt = "/home/" + user + "/scripts/avdecrypt/avdecrypt.py"
            params = "-a " + avdPath + " -s " + snapshot + " -o " + outputDir
            cmd = py + " " + avdecrypt + " " + params
            analysisVm = Vm(vm, user, pw)
            analysisVm.executeWithParams(py, cmd)

        print("\n --> Decryption finished \n")
 

    def _createIdiff(self):
        vm = self.vmTxt.get("1.0", "end-1c")
        user = self.userTxt.get("1.0", "end-1c")
        pw = self.pwTxt.get("1.0", "end-1c")
        outputDir = self.outputTxt.get("1.0", "end-1c")
        decryptedDir = outputDir + "/decrypted"
        snapshots = self._getSnapshotList()
        outputHost = self.hOutputTxt.get("1.0", "end-1c")

        print("\n --> Processing with idifference2.py \n")

        py = "/usr/bin/python3"
        dfxml = "/home/" + user + "/scripts/dfxml_python/dfxml/bin/idifference2.py"

        for comparison in self.config["comparison"]:
            resultPath = outputHost + "\\actions\\" + comparison["name"] 
            firstSnapshot = comparison["first"]
            secondSnapshots = comparison["second"]

            if(not os.path.isdir(resultPath)):
                os.mkdir(resultPath)
                os.mkdir(resultPath + "\\ge")

            for snapshotName in secondSnapshots:
                snList = [i for i in snapshots if snapshotName in i]
                for snapshot in snList:
                    before = decryptedDir + "/" + firstSnapshot + ".1.raw"
                    after = decryptedDir + "/" + snapshot + ".raw"
                    target = resultPath + "\\ge\\" + snapshot + ".idiff"
                    cmd = py + " " + dfxml + " " + before + " " + after + " > " + target
                    print(cmd)
                    analysisVm = Vm(vm, user, pw)
                    analysisVm.executeWithParams(py, cmd)

        print("\n --> *.idiff created \n")

    def _analyseIdiff(self):
        vm = self.vmTxt.get("1.0", "end-1c")
        user = self.userTxt.get("1.0", "end-1c")
        pw = self.pwTxt.get("1.0", "end-1c")
        outputDir = self.outputTxt.get("1.0", "end-1c")
        actionsDir = self.hOutputTxt.get("1.0", "end-1c") + "\\" + "actions"
        py = "/usr/bin/python3"
        evidence = "-m evidence"
        
        for dir in os.listdir(actionsDir):
            argsP = "-p " + outputDir + "/actions/" + dir + "/ge" 
            argsO = "-o " + outputDir + "/actions/" + dir
            cmd = py + " " + evidence + argsP + " "
            print(cmd)
            #analysisVm = Vm(vm, user, pw)
            #analysisVm.executeWithParams(py, cmd)

    def _analyseDb(self):
        print("Analyse .db")


    def _processSnapshots(self):
      pass

    def start(self):
        self.root.mainloop()
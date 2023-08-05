import subprocess
import sys
import threading
import tkinter as tk
from tkinter.constants import NW, TOP
import pkg_resources

from ipra.View2.main import Main

class UpdateProcessDialog():

    required = ['selenium', 'beautifulsoup4', 'webdriver_manager',
                'pandas', 'xlsxwriter', 'openpyxl', 'lxml', 'configparser', 'packaging',
                'Pillow','customtkinter',
                'IPRA']

    currentVersion = []

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("IPRA Update Process")

        # sets the geometry of toplevel
        self.root.geometry("400x200")

        mainLabel = tk.Label(self.root, text='Check for update...')
        mainLabel.pack(side=TOP, anchor=NW, padx=10, pady=10)

        # New Line
        emptyLable = tk.Label(self.root, text='')
        emptyLable.pack()

        self.statusText = tk.StringVar()
        self.statusText.set("")

        statusLable = tk.Label(self.root, textvariable=self.statusText)
        statusLable.pack(side=TOP, anchor=NW, padx=10)

        # New Line
        emptyLable = tk.Label(self.root, text='')
        emptyLable.pack()

        self.closeButton = tk.Button(self.root, text="START IPRA",command=self.__closeFrame)
        self.closeButton.pack_forget()


        self.updatePackageThread = threading.Thread(target=self.__updatePackage)
        self.updatePackageThread.start()
        #self.__getCurrentPackageVersion()
        self.root.mainloop()
        
    def __closeFrame(self):
        # Shut down all frame and close all webdriver
        # Important to release all resources
        self.root.destroy()
        Main()

    def __getCurrentPackageVersion(self):
        for packageName in self.required:
            self.currentVersion.append(
                pkg_resources.get_distribution(packageName).version)
        return

    def __updatePackage(self):
        for packageName in self.required:
            self.statusText.set("Checking for Update: {0}".format(packageName))
            python = sys.executable
            subprocess.check_call(
                [python, '-m', 'pip', 'install', packageName, '--user'], stdout=subprocess.DEVNULL)
            python = sys.executable
            subprocess.check_call(
                [python, '-m', 'pip', 'install', packageName, '--user','--upgrade'], stdout=subprocess.DEVNULL)
        else:
            self.statusText.set("Update Completed! Starting IPRA...")
            self.closeButton.pack(side=TOP, anchor=NW, padx=10)
            # time.sleep(3)
            # self.__closeFrame()

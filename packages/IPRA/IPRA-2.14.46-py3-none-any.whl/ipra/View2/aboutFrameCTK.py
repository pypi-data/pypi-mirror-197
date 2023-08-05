import customtkinter
import pkg_resources
from ipra.Utility.StringUtilityCTK import GetStringSingletionCTK
from ipra.Utility.ConfigUtility import GetConfigSingletion
from ipra.Controller.policyCollectionController import PolicyCollectionController


class AboutFrame(customtkinter.CTkFrame):
    __VERSION = pkg_resources.require("ipra")[0].version
    __DATE = "13-Mar-2023"
    __CHECKSUM = "690E9212E0497513"
    
    def __init__(self,app):
        super().__init__(master=app,corner_radius=0,fg_color="transparent")

        self.FONT = customtkinter.CTkFont(size=15,weight='bold')
        self.configParser = GetConfigSingletion()
        self.stringValue = GetStringSingletionCTK()
        self.stringValue.SetString()
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(4, weight=1)

        self.version = customtkinter.CTkLabel(self, text= self.stringValue.versionString.get().format(self.__VERSION), 
                                              font=self.FONT,anchor="w")
        self.version.grid(row=0, column=0, padx=20, pady=10,sticky="ew")

        self.date = customtkinter.CTkLabel(self, text= self.stringValue.releaseDate.get().format(self.__DATE), 
                                              font=self.FONT,anchor="w")
        self.date.grid(row=1, column=0, padx=20, pady=10,sticky="ew")

        self.checksum = customtkinter.CTkLabel(self, text= self.stringValue.releaseDate.get().format(self.__CHECKSUM), 
                                              font=self.FONT,anchor="w")
        self.checksum.grid(row=2, column=0, padx=20, pady=10,sticky="ew")


        self.supportSystem = customtkinter.CTkLabel(self, text= self.stringValue.supportSystem.get(), 
                                              font=self.FONT,anchor="w")
        self.supportSystem.grid(row=3, column=0, padx=20,sticky="ew")

        self.textbox = customtkinter.CTkTextbox(self, width=200,font=self.FONT)
        self.textbox.grid(row=4, column=0, padx=(20, 0),pady=10, sticky="nsew")
        for entry in PolicyCollectionController().getPolicyCollection():
            self.textbox.insert('end', entry[0]+'\n')
        self.textbox.configure(state='disabled')


        pass

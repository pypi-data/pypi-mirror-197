import tkinter.messagebox as mb
import tkinter.ttk as ttk
from abc import abstractmethod

import numpy as np
from numpy import ma
from tksheet import Sheet

from . import moduleFrame
from .style import padding
from .table import ButtonFrame


class KnownSignals(moduleFrame.Strategy):
    requiredAttributes = ()

    @abstractmethod
    def run(self):
        pass


class KnownSpectraPopup(moduleFrame.Popup):
    def __init__(self, titration, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.titration = titration
        self.title("Enter known spectra")

        self.sheet = Sheet(
            self,
            data=self.formatData(titration.knownSpectra),
            headers=list(titration.processedSignalTitlesStrings),
            row_index=list(titration.contributorNames()),
            set_all_heights_and_widths=True,
        )

        self.sheet.pack(side="top", expand=True, fill="both")
        self.sheet.enable_bindings()

        buttonFrame = ButtonFrame(self, self.reset, self.saveData, self.destroy)
        buttonFrame.pack(expand=False, fill="both", side="bottom")

        loadButton = ttk.Button(buttonFrame, text="Load from CSV", command=self.loadCSV)
        loadButton.pack(side="left", padx=padding)

    def formatData(self, data):
        formattedData = data.astype(str)
        formattedData[np.isnan(data)] = ""
        return list(formattedData)

    def reset(self):
        self.sheet.set_sheet_data(self.formatData(self.titration.knownSpectra))

    def saveData(self):
        data = np.array(self.sheet.get_sheet_data(), dtype=object)
        data[np.where(data == "")] = None
        data = data.astype(float)

        if not np.all(np.any(np.isnan(data), 1) == np.all(np.isnan(data), 1)):
            mb.showerror(
                title="Could not save data",
                parent=self,
                message="Please enter full spectra, or leave the entire row blank",
            )
            return

        self.titration.knownSpectra = data
        self.saved = True
        self.destroy()

    def loadCSV(self):
        return


# TODO: make this work with the new format
class GetKnownSpectra(KnownSignals):
    Popup = KnownSpectraPopup
    popupAttributes = ("knownSpectra",)

    def __init__(self, titration):
        self.titration = titration
        if not (
            hasattr(titration, "knownSpectra")
            and titration.knownSpectra.shape
            == (len(titration.contributorNames()), len(titration.processedSignalTitles))
        ):
            titration.knownSpectra = np.full(
                (
                    len(self.titration.contributorNames()),
                    len(self.titration.processedSignalTitles),
                ),
                np.nan,
            )

    def __call__(self):
        return self.titration.knownSpectra


class GetAllSpectra(KnownSignals):
    def run(self):
        return ma.array(
            np.empty(
                (
                    len(self.titration.contributors.contributorNames),
                    len(self.titration.processedSignalTitles),
                )
            ),
            mask=True,
        )


class ModuleFrame(moduleFrame.ModuleFrame):
    group = "Signals"
    dropdownLabelText = "Specify any known spectra?"
    dropdownOptions = {
        "Optimise all spectra": GetAllSpectra,
        # "Specify some known spectra": GetKnownSpectra,
    }
    attributeName = "knownSignals"

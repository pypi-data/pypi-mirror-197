from Orange.data import Table
from Orange.widgets.widget import Output
from Orange.widgets import gui
from ..base_widget import FilterWidget
from ramanchada2.misc.types.peak_candidates import ListPeakCandidateMultiModel
from ramanchada2.spectrum.peaks.fit_peaks import available_models
# from Orange.data.pandas_compat import table_from_frame


class Fit(FilterWidget):
    name = "Fit Peaks"
    description = "Fit Peaks"
    icon = "icons/spectra.svg"

    class Outputs(FilterWidget.Outputs):
        peaks_out = Output("Peaks", Table, default=False)

    def __init__(self):
        super().__init__()
        self.should_auto_proc = False
        box = gui.widgetBox(self.controlArea, self.name)
        self.should_fit = True
        self.vary_baseline = False
        self.peak_profile = available_models[0]

        gui.checkBox(box, self, "should_fit", "Perform fit", callback=self.auto_process)
        gui.checkBox(box, self, "vary_baseline", "Vary baseline", callback=self.auto_process)
        gui.comboBox(box, self, 'peak_profile', sendSelectedValue=True, items=available_models,
                     callback=self.auto_process)

    def process(self):
        self.out_spe = list()
        for spe in self.in_spe:
            cand = ListPeakCandidateMultiModel.validate(spe.result)
            self.out_spe.append(
                spe.fit_peak_multimodel(profile=self.peak_profile, candidates=cand, no_fit=not self.should_fit,
                                        vary_baseline=self.vary_baseline)
            )
        self.send_outputs()
        # TODO: fix the dataframe with peak information
        # self.Outputs.peaks_out.send(table_from_frame(df))

    def custom_plot(self, ax):
        for spe in self.out_spe:
            ListPeakCandidateMultiModel.validate(spe.result).plot(ax)

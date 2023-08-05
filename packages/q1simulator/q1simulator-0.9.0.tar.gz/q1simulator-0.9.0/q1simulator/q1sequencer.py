import logging
from functools import partial
from dataclasses import dataclass
import json
import numpy as np
from typing import Optional, Iterator, Iterable, Tuple

from qcodes.instrument.channel import InstrumentChannel

from .q1core import Q1Core
from .rt_renderer import Renderer, MockDataEntry

from qblox_instruments import SequencerState, SequencerStatus, SequencerStatusFlags

logger = logging.getLogger(__name__)

MockDataType = Iterable[MockDataEntry]


class Q1Sequencer(InstrumentChannel):

    # only logged
    _seq_log_only_parameters = [
        # -- only printed:
        'sync_en',
        'nco_phase_offs',
        'marker_ovr_en',
        'marker_ovr_value',
        'cont_mode_en_awg_path0',
        'cont_mode_en_awg_path1',
        'cont_mode_waveform_idx_awg_path0',
        'cont_mode_waveform_idx_awg_path1',
        'upsample_rate_awg_path0',
        'upsample_rate_awg_path1',
        'gain_awg_path0',
        'gain_awg_path1',
        'offset_awg_path0',
        'offset_awg_path1',
        ]
    _seq_log_only_parameters_qrm = [
        # old v0.8 parameters for backwards compatibility
        # TODO remove in next release.
        'phase_rotation_acq',
        'discretization_threshold_acq',
        ]

    def __init__(self, parent, name, sim_type):
        super().__init__(parent, name)
        self._is_qcm = sim_type in ['QCM', 'QCM-RF', 'Viewer']
        self._is_qrm = sim_type in ['QRM', 'QRM-RF', 'Viewer']
        self._is_rf = sim_type in ['QCM-RF', 'QRM-RF']

        if self._is_qrm:
            log_params = self._seq_log_only_parameters + self._seq_log_only_parameters_qrm
            self._v_max = 0.5
        else:
            log_params = self._seq_log_only_parameters
            self._v_max = 2.5

        if self._is_rf:
            self._v_max = 3.3

        for par_name in log_params:
            self.add_parameter(par_name,
                               set_cmd=partial(self._log_set, par_name))

        self.add_parameter('sequence', set_cmd=self.upload)
        self.add_parameter('mod_en_awg', set_cmd=self._set_mod_en_awg)
        self.add_parameter('nco_freq', set_cmd=self._set_nco_freq)
        self.add_parameter('mixer_corr_gain_ratio', set_cmd=self._set_mixer_gain_ratio)
        self.add_parameter('mixer_corr_phase_offset_degree', set_cmd=self._set_mixer_phase_offset_degree)

        self.add_parameter('channel_map_path0_out0_en',
                           set_cmd=partial(self._set_channel_map_path_en, 0, 0))
        self.add_parameter('channel_map_path1_out1_en',
                           set_cmd=partial(self._set_channel_map_path_en, 1, 1))

        for i in range(1,16):
            self.add_parameter(f'trigger{i}_count_threshold',
                               set_cmd=partial(self._set_trigger_count_threshold, i))
            self.add_parameter(f'trigger{i}_threshold_invert',
                               set_cmd=partial(self._set_trigger_threshold_invert, i))

        if self._is_qcm:
            self.add_parameter('channel_map_path0_out2_en',
                               set_cmd=partial(self._set_channel_map_path_en, 0, 2))
            self.add_parameter('channel_map_path1_out3_en',
                               set_cmd=partial(self._set_channel_map_path_en, 1, 3))
        if self._is_qrm:
            self.add_parameter('demod_en_acq', set_cmd=self._set_demod_en_acq)
            self.add_parameter('integration_length_acq', set_cmd=self._set_integratrion_length_acq)
            self.add_parameter('thresholded_acq_rotation', set_cmd=self._set_thresholded_acq_rotation)
            self.add_parameter('thresholded_acq_threshold', set_cmd=self._set_thresholded_acq_threshold)
            self.add_parameter('thresholded_acq_trigger_en', set_cmd=self._set_thresholded_acq_trigger_en)
            self.add_parameter('thresholded_acq_trigger_address', set_cmd=self._set_thresholded_acq_trigger_address)
            self.add_parameter('thresholded_acq_trigger_invert', set_cmd=self._set_thresholded_acq_trigger_invert)

        self._trace = False
        self.reset()

    def config(self, name, value):
        if name == 'name':
            self.name = value
            self.rt_renderer.name = value
        elif name == 'max_render_time':
            self.rt_renderer.max_render_time = value
        elif name == 'max_core_cycles':
            self.q1core.max_core_cycles = value
        elif name == 'trace':
            self._trace = value
            self.rt_renderer.trace_enabled = value

    def reset(self):
        self.waveforms = {}
        self.weights = {}
        self.acquisition_bins = {}
        self._mock_data = {}
        self._trigger_events = []
        self.run_state = 'IDLE'
        self.rt_renderer = Renderer(self.name)
        self.rt_renderer.trace_enabled = self._trace
        self.q1core = Q1Core(self.name, self.rt_renderer, self._is_qrm)
        self.reset_trigger_thresholding()

    def _log_set(self, name, value):
        logger.info(f'{self.name}: {name}={value}')

    def _set_mod_en_awg(self, value):
        logger.debug(f'{self.name}: mod_en_awg={value}')
        self.rt_renderer.mod_en_awg = value

    def _set_nco_freq(self, value):
        logger.info(f'{self.name}: nco_freq={value}')
        self.rt_renderer.nco_frequency = value

    def _set_demod_en_acq(self, value):
        logger.debug(f'{self.name}: demod_en_acq={value}')
        self.rt_renderer.demod_en_acq = value

    def _set_mixer_gain_ratio(self, value):
        logger.debug(f'{self.name}: mixer_gain_ratio={value}')
        self.rt_renderer.mixer_gain_ratio = value

    def _set_mixer_phase_offset_degree(self, value):
        logger.debug(f'{self.name}: mixer_phase_offset_degree={value}')
        self.rt_renderer.mixer_phase_offset_degree = value

    def _set_channel_map_path_en(self, path, out, value):
        logger.debug(f'{self.name}: channel_map_path{path}_out{out}_en={value}')
        self.rt_renderer.path_enable(path, out, value)

    def _set_trigger_count_threshold(self, address, count):
        self.rt_renderer.set_trigger_count_threshold(address, count)

    def _set_trigger_threshold_invert(self, address, invert: bool):
        self.rt_renderer.set_trigger_threshold_invert(address, invert)

    def _set_integratrion_length_acq(self, value):
        self.rt_renderer.set_integratrion_length_acq(value)

    def _set_thresholded_acq_rotation(self, value):
        self.rt_renderer.set_thresholded_acq_rotation(value)

    def _set_thresholded_acq_threshold(self, value):
        self.rt_renderer.set_thresholded_acq_threshold(value)

    def _set_thresholded_acq_trigger_en(self, value):
        self.rt_renderer.set_thresholded_acq_trigger_en(value)

    def _set_thresholded_acq_trigger_address(self, value):
        self.rt_renderer.set_thresholded_acq_trigger_addr(value)

    def _set_thresholded_acq_trigger_invert(self, value):
        self.rt_renderer.set_thresholded_acq_trigger_invert(value)

    def upload(self, sequence):
        if isinstance(sequence, str):
            filename = sequence
            with open(filename) as fp:
                pdict = json.load(fp)
        else:
            pdict = sequence
        waveforms = pdict['waveforms']
        weights = pdict['weights']
        acquisitions = pdict['acquisitions']
        program = pdict['program']
        self._set_waveforms(waveforms)
        self._set_weights(weights)
        self._set_acquisition_bins(acquisitions)
        self.q1core.load(program)

    def _set_waveforms(self, waveforms):
        self.waveforms = waveforms
        wavedict = {}
        for name, datadict in waveforms.items():
            index = int(datadict['index'])
            data = np.array(datadict['data'])
            wavedict[index] = data
        self.rt_renderer.set_waveforms(wavedict)

    def _set_weights(self, weights):
        self.weights = weights
        weightsdict = {}
        for name, datadict in weights.items():
            index = int(datadict['index'])
            data = np.array(datadict['data'])
            weightsdict[index] = data
        self.rt_renderer.set_weights(weightsdict)

    def _set_acquisition_bins(self, acq_bins):
        self.acquisition_bins = acq_bins
        bins_dict = {}
        for name, datadict in acq_bins.items():
            index = int(datadict['index'])
            num_bins = int(datadict['num_bins'])
            bins_dict[index] = num_bins
        self.rt_renderer.set_acquisition_bins(bins_dict)

    def _set_rt_mock_data(self):
        for name,md in self._mock_data.items():
            if name not in self.acquisition_bins:
                logger.warning(f"no acquisition_bins for mock_data '{name}'")
                continue
            try:
                data = np.asarray(next(md))
            except StopIteration:
                raise Exception(f'No more mock data')
            bin_num = int(self.acquisition_bins[name]['index'])
            self.rt_renderer.set_mock_data(bin_num, data)

    def get_state(self):
        flags = list(self.q1core.errors | self.rt_renderer.errors)
        return SequencerState(
            SequencerStatus[self.run_state],
            [SequencerStatusFlags[flag.replace(' ','_')] for flag in flags],
        )

    def get_acquisition_state(self):
        if not self._is_qrm:
            raise NotImplementedError('Instrument type is not QRM')
        return True

    def set_trigger_thresholding(self, address: int, count: int, invert: bool) -> None:
        self.rt_renderer.set_trigger_count_threshold(address, count)
        self.rt_renderer.set_trigger_threshold_invert(address, invert)

    def get_trigger_thresholding(self, address: int) -> Tuple[int,bool]:
        return (
            self.rt_renderer.get_trigger_count_threshold(address),
            self.rt_renderer.get_trigger_threshold_invert(address)
            )

    def reset_trigger_thresholding(self) -> None:
        for i in range(1, 16):
            self.set_trigger_thresholding(i, 1, False)

    def arm(self):
        self.run_state = 'ARMED'

    def run(self):
        self.run_state = 'RUNNING'
        self.rt_renderer.reset()
        self._set_rt_mock_data()
        self.rt_renderer.trigger_events = self._trigger_events
        self.q1core.run()
        self.run_state = 'STOPPED'

    def get_acquisition_data(self):
        if not self._is_qrm:
            raise NotImplementedError('Instrument type is not QRM')
        cnt,data,thresholded = self.rt_renderer.get_acquisition_data()
        result = {}
        for name, datadict in self.acquisition_bins.items():
            index = int(datadict['index'])
            acq_count = cnt[index]
            path_data = data[index]/acq_count[:,None]
            threshold = thresholded[index]/acq_count

            result[name] = {
                'index':index,
                'acquisition':{
                    'bins':{
                        'integration': {
                            'path0':list(path_data[:,0]),
                            'path1':list(path_data[:,1]),
                            },
                        'threshold':threshold,
                        'avg_cnt':list(acq_count),
                    }
                }}
        return result

    def delete_acquisition_data(self, name='', all=False):
        if all:
            self.rt_renderer.delete_acquisition_data_all()
        else:
            index = self.acquisition_bins[name]['index']
            self.rt_renderer.delete_acquisition_data(index)

    # --- Simulator specific methods ---

    def set_acquisition_mock_data(self,
                                  data: Optional[Iterable[MockDataType]],
                                  name='default',
                                  repeat=False):
        '''
        Sets mock acquisition data for 1 or more runs of the sequence.

        `data` is a list with lists of values to use per run of the sequence.
        The list for a run should have a length equal or bigger than
        the number of acquire calls in the executed sequence.
        The entry for an acquire call is used for both paths.
        If it is a single float value then it is used for both paths.
        If it is a complex value then the real part is used for path 0 and
        the imaginary part for path 1.
        If it is a sequence of two floats then the first is used for path 0
        and the second for path 1.

        Args:
            data:
                if None clears the data and resets default behavior,
                otherwise list of mock data for every run of the sequence.
            name: name of the acquisition
            repeat:
                if True repeatly cycles through the list of mock data,
                otherwise an exception is raised when the list of mock data is exhausted.

        Example:
            # set data for 1 run to return the values 0 till 19 on path 0 and path 1
            data = [np.arange(20)]
            sim.sequencers[0].set_acquisition_mock_data(data)

            # set data for every run to return IQ values with changing phase
            # on path 0 and 1
            data = [np.exp(np.pi*1j*np.arange(20)/10)]
            sim.sequencers[0].set_acquisition_mock_data(data, repeat=True)

            # set data for every run to return the values 0 till 19 on path 0
            # and 100 till 119 on path 1.
            data = [np.arange(20) + 1j*np.arange(100,120)]
            sim.sequencers[0].set_acquisition_mock_data(data, repeat=True)

            # set data for 2 runs to return the values 0 till 19 on the first run
            # and 100 till 119 on the second run.
            data2 = [np.arange(20), np.arange(100, 120)]
            sim.sequencers[0].set_acquisition_mock_data(data2)

            # Return 0...19 and 100...119 alternatingly.
            sim.sequencers[0].set_acquisition_mock_data(data2, repeat=True)

            # reset default behaviour.
            sim.sequencers[0].set_acquisition_mock_data(None)
        '''
        if data is None and name in self._mock_data:
            del self._mock_data[name]
        else:
            self._mock_data[name] = MockData(data, repeat)

    def get_used_triggers(self):
        return self.q1core.get_used_triggers()

    def get_acq_trigger_events(self):
        return self.rt_renderer.acq_trigger_events

    def set_trigger_events(self, events):
        self._trigger_events = events

    def plot(self):
        self.rt_renderer.plot(self._v_max)

    def print_registers(self, reg_nrs=None):
        self.q1core.print_registers(reg_nrs)


@dataclass
class MockData:
    data: Iterable[MockDataType]
    repeat: bool
    data_iter: Iterator[MockDataType] = None

    def __post_init__(self):
        self.data_iter = iter(self.data)

    def __next__(self):
        try:
            return next(self.data_iter)
        except StopIteration:
            if not self.repeat:
                raise
            self.data_iter = iter(self.data)
            return next(self.data_iter)

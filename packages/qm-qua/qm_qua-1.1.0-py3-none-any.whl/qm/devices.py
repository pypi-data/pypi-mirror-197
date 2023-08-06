from octave_sdk import RFInputRFSource, RFOutputMode, IFMode, Octave


RF_OUTPUT_INDEX_TO_INPUT_SOURCE = {
    1: RFInputRFSource.Loopback_RF_out_1,
    2: RFInputRFSource.Loopback_RF_out_2,
    3: RFInputRFSource.Loopback_RF_out_3,
    4: RFInputRFSource.Loopback_RF_out_4,
    5: RFInputRFSource.Loopback_RF_out_5,
}


class OctaveDevice:
    def __init__(self, client: Octave):
        self._client = client

    @property
    def client(self):
        return self._client

    def set_for_calibration(self, calibration_input, output_port):
        state_name_before = "before_cal"
        self._client.snapshot_state(state_name_before)
        # switch to loopback mode to listen in on the RF output
        self._client.rf_inputs[calibration_input].set_rf_source(RF_OUTPUT_INDEX_TO_INPUT_SOURCE[output_port])
        self._client.rf_inputs[calibration_input].set_if_mode_i(IFMode.direct)
        self._client.rf_inputs[calibration_input].set_if_mode_q(IFMode.direct)
        self._client.rf_inputs[1].set_if_mode_i(IFMode.off)
        self._client.rf_inputs[1].set_if_mode_q(IFMode.off)
        self._client.rf_outputs[output_port].set_output(RFOutputMode.on)
        return state_name_before

    def restore_default_state(self):
        self._client.restore_default_state()

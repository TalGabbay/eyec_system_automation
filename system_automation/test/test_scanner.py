import os
import pytest
import logging
from typing import List
from system_automation.infra import file_utils
from system_automation.infra.dfs_enums import ResponseFields, ScannerTestDelta
from system_automation.logic.scanner_utils import get_peak_degree, calculate_differential


@pytest.mark.sanity
def test_start_stop_mirror_scan(tester_lib_instance, initialize_system_for_scanning_test):
    response = tester_lib_instance.scn_start_mirror_scan()
    msg = f"Mirror scan start failed. Return status: {response[ResponseFields.STATUS.value]}"
    assert response[ResponseFields.STATUS.value] == 'Done', msg

    response = tester_lib_instance.scn_get_status()
    msg = f"Mirror scan status check failed. Return status: {response[ResponseFields.OUTPUT.value]}"
    assert response[ResponseFields.OUTPUT.value] == 'SCAN', msg

    response = tester_lib_instance.scn_stop_mirror_scan()
    msg = f"Mirror scan stop failed. Return status: {response[ResponseFields.STATUS.value]}"
    assert response[ResponseFields.STATUS.value] == 'Done', msg

    response = tester_lib_instance.scn_get_status()
    msg = f"Mirror scan status check after stop failed. Return status: {response[ResponseFields.OUTPUT.value]}"
    assert response[ResponseFields.OUTPUT.value] == 'IDLE', msg


@pytest.mark.sanity
@pytest.mark.parametrize("expected_angle", [1.0, 2.5, 0.0])
def test_scn_abs_shift_mirror(tester_lib_instance, initialize_system_for_scanning_test, expected_angle):
    response = tester_lib_instance.scn_abs_shift_mirror(angle=expected_angle)
    msg = f"faild to set absolut mirror shift to angle {expected_angle}"
    assert response[ResponseFields.STATUS.value] == "Done", msg

    response = tester_lib_instance.scn_get_abs_shift_mirror()
    delta = ScannerTestDelta.ABS_MIRROR_SHIFT.value
    actual_angle = response[ResponseFields.OUTPUT.value]
    msg = f"Expected angle: {expected_angle} +- {delta}, Actual angle: {actual_angle}"
    assert abs(expected_angle - actual_angle) <= delta, msg
    logging.info(f"\nTest {test_scn_abs_shift_mirror.__name__} passed:\n"
                 f"expected angle: {expected_angle} actual angle: {actual_angle} delta: {delta}")


@pytest.mark.sanity
@pytest.mark.parametrize(("angle", "scan_time", "pattern"),
                         [
                             ([30], [80], 4),
                             ([35], [80], 5),
                             ([90], [100], 6)
                         ])
def test_set_active_pattern(tester_lib_instance,
                            initialize_system_for_scanning_test,
                            angle, scan_time, pattern):
    response = tester_lib_instance.scn_configure_pattern(angle=angle, scan_time=scan_time, pattern=pattern)
    msg = f"Configure scanning pattern failed. Return status: {response[ResponseFields.OUTPUT.value]}"
    assert response[ResponseFields.STATUS.value] == "Done", msg

    response = tester_lib_instance.scn_start_mirror_scan()
    msg = f"Start mirror scan failed. Return status: {response[ResponseFields.OUTPUT.value]}"
    assert response[ResponseFields.STATUS.value] == "Done", msg

    response = tester_lib_instance.scn_set_active_pattern(pattern)
    msg = f"Set active pattern failed. Return status: {response[ResponseFields.OUTPUT.value]}"
    assert response[ResponseFields.STATUS.value] == "Done", msg

    response = tester_lib_instance.scn_start_mirror_scan()
    msg = f"Start mirror scan failed. Return status: {response[ResponseFields.OUTPUT.value]}"
    assert response[ResponseFields.STATUS.value] == "Done", msg

    response = tester_lib_instance.scn_get_status()
    msg = f"Mirror scan status check failed. Return status: {response[ResponseFields.OUTPUT.value]}"
    assert response[ResponseFields.OUTPUT.value] == 'SCAN', msg

    # TODO Fix scanner sequencer bug to remove code block
    path = os.getcwd() + "/to_delete"
    file_utils.create_directory(path)
    file_utils.create_new_file(path + "/.record_ended")
    file_utils.create_new_file(path + "/.record_started")

    result = tester_lib_instance.scn_record_hpos(1, False, path)
    file_utils.delete_directory(path)

    position_list: List[float] = result[ResponseFields.OUTPUT.value]
    delta = ScannerTestDelta.SET_ACTIVE_PATTERN.value
    actual_angle = get_peak_degree(position_list)
    expected_angle = angle[0]
    calculate_differential(position_list)
    msg = f"Expected angle: {expected_angle} +- {delta}, Actual angle: {actual_angle}"
    assert abs(expected_angle - actual_angle) <= delta, msg
    logging.info(f"\nTest {test_set_active_pattern.__name__} passed:\n"
                 f"expected angle: {expected_angle} actual angle: {actual_angle} delta: {delta}")


@pytest.mark.parametrize("expected_angle", [1.0, 36.0, 0.0])
def test_scn_zenith(tester_lib_instance, initialize_system_for_scanning_test, expected_angle):
    response = tester_lib_instance.scn_set_zenith(angle=expected_angle)
    msg = f"Failed to set zeinith, response: {response[ResponseFields.STATUS.value]}"
    assert response[ResponseFields.STATUS.value] == "Done", msg

    response = tester_lib_instance.scn_get_zenith()
    msg = f"Failed to get zeinith, response: {response[ResponseFields.STATUS.value]}"
    assert response[ResponseFields.STATUS.value] == "Done", msg

    actual_angle = response[ResponseFields.OUTPUT.value]
    delta = ScannerTestDelta.SET_SCANNER_ZEINIT.value
    msg = f"Expected zenith: {expected_angle} +- {delta}, Actual zenith: {actual_angle}"
    assert abs(expected_angle - actual_angle) <= delta, msg
    logging.info(f"\nTest {test_scn_zenith.__name__} passed:\n"
                 f"expected angle: {expected_angle} actual angle: {actual_angle} delta: {delta}")


@pytest.mark.sanity
def test_scn_send_command(tester_lib_instance, initialize_system_for_scanning_test):
    response = tester_lib_instance.scn_send_command(op_code='GET_STATUS', data_in='0')
    msg = f"Send command to scanner filed, response: {response[ResponseFields.STATUS.value]}"
    assert response[ResponseFields.STATUS.value] == "Done", msg


@pytest.mark.sanity
def test_get_temperature(tester_lib_instance, initialize_system_for_scanning_test):
    response = tester_lib_instance.scn_get_temperature()
    assert response[ResponseFields.STATUS.value] == "Error"


@pytest.mark.sanity
def test_scn_deinit_module(tester_lib_instance, initialize_system_for_scanning_test):
    response = tester_lib_instance.scn_deinit_module()
    assert response[ResponseFields.STATUS.value] == "Error"


@pytest.mark.sanity
def test_scn_enable_sync(tester_lib_instance, initialize_system_for_scanning_test):
    response = tester_lib_instance.scn_enable_sync()
    assert response[ResponseFields.STATUS.value] == "Error"


@pytest.mark.sanity
def test_scn_get_error_status(tester_lib_instance, initialize_system_for_scanning_test):
    response = tester_lib_instance.scn_get_error_status()
    assert response[ResponseFields.STATUS.value] == "Error"


@pytest.mark.sanity
def test_scn_get_fw_version(tester_lib_instance, initialize_system_for_scanning_test):
    response = tester_lib_instance.scn_get_fw_version()
    assert response[ResponseFields.STATUS.value] == "Error"


@pytest.mark.sanity
def test_scn_enable_fw_flash(tester_lib_instance, initialize_system_for_scanning_test):
    response = tester_lib_instance.scn_enable_fw_flash()
    assert response[ResponseFields.STATUS.value] == "Error"


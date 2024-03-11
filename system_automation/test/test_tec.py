import pytest


@pytest.mark.sanity
def test_mirror_scan(tester_lib_instance, initialize_system_for_tec_test):
    init_status = tester_lib_instance.tec_init_module()
    assert init_status['Status'] == 'Done', f"Module initialization failed. Return status: {init_status['Status']}"
    response = tester_lib_instance.tec_start_pid()
    print(response)
    pass


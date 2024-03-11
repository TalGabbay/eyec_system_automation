import pytest
from eyec_system_lib.tester_lib import tester_lib
from test_tal_01.infra.dfs_enums import ResponseFields


@pytest.fixture(scope="session")
def tester_lib_instance():
    return tester_lib(bobox_flag=True, power_up=False,  es2_mb=True)


@pytest.fixture(scope="session")
def initialize_system_for_scanning_test(tester_lib_instance):
    response = tester_lib_instance.pmu_power_system_on()
    msg = f"Power system initialization failed. Return status: {response[ResponseFields.STATUS.value]}"
    assert response[ResponseFields.STATUS.value] == 'Done', msg

    response = tester_lib_instance.scn_init_module()
    msg = f"Module initialization failed. Return status: {response[ResponseFields.STATUS.value]}"
    assert response[ResponseFields.STATUS.value] == 'Done', msg


@pytest.fixture(scope="session")
def initialize_system_for_tec_test(tester_lib_instance):
    response = tester_lib_instance.pmu_power_system_on()
    msg = f"Power system initialization failed. Return status: {response[ResponseFields.STATUS.value]}"
    assert response[ResponseFields.STATUS.value] == 'Done', msg

    response = tester_lib_instance.tec_init_module()
    msg = f"Module initialization failed. Return status: {response[ResponseFields.STATUS.value]}"
    assert response[ResponseFields.STATUS.value] == 'Done', msg


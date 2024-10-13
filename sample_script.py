from pyats import aetest
from genie.testbed import load

class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def connect_to_devices(self, testbed):
        """
        Connect to all devices in the testbed
        :param testbed:
        :return:
        """
        self.parent.parameters["testbed"] = testbed
        testbed.connect()

class VerifyDeviceConnectivity(aetest.Testcase):
    @aetest.test
    def show_version(self, testbed):
        """
        Verify device connectivity by parsing 'show version' output
        :param testbed:
        :return:
        """
        for device in testbed.devices.values():
            if device.is_connected():
                output = device.parse('show version')
                print(f"{device.name} show version output: {output}")
            else:
                self.failed(f"{device.name} is not reachable")

class CommonCleanup(aetest.CommonCleanup):
    @aetest.subsection
    def disconnect_from_devices(self, testbed):
        """
        Disconnect from all devices in the testbed
        :param testbed:
        :return:
        """
        testbed.disconnect()


if __name__ == '__main__':
    testbed = load('testbed.yaml')
    aetest.main(testbed=testbed)
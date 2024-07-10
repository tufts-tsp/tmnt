# from .test_examples import TestHotelBookingWebsiteExample, TestInsulinDeliveryDeviceExample
# from .test_oscal_parser import TestOSCALParser
from tests_engines import TestThreatlib
from tests_kb import TestASVS, TestCWES, TestCAPEC
from tests_dsl import (
    TestTM,
    TestElement,
    TestComponent,
    TestAsset,
    TestDataFlow,
    TestWorkFlow,
    TestIssue,
    TestThreat,
    TestWeakness,
    TestVulnerability,
    TestFinding,
    TestControl,
    TestControlCatalog,
    TestActor,
)
from test_tmntparser import TestTMNTParser
import unittest

if __name__ == "__main__":
    unittest.main()

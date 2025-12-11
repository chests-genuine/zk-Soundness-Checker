import unittest
from zk_soundness_checker import verify_zk_contract

class TestZKContractVerification(unittest.TestCase):
    def test_valid_address(self):
        address = "0x5A98FcBEA516Cf06857215779Fd812CA3beF1B32"
        self.assertIsNotNone(verify_zk_contract(address))
    
    def test_invalid_address(self):
        address = "0xInvalidAddress"
        with self.assertRaises(ValueError):
            verify_zk_contract(address)

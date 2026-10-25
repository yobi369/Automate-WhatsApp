import os
import tempfile
import unittest

import database


class DatabaseTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.previous_cwd = os.getcwd()
        os.chdir(self.tempdir.name)
        database.create_table()
        database.create_contact_table()

    def tearDown(self):
        os.chdir(self.previous_cwd)
        self.tempdir.cleanup()

    def test_add_and_get_contact(self):
        database.add_contact("Test User", "+254700000000")
        contacts = database.get_contacts()
        self.assertEqual(len(contacts), 1)
        self.assertEqual(contacts[0][1:], ("Test User", "+254700000000"))

    def test_delete_contact(self):
        database.add_contact("Test User", "+254700000000")
        contact_id = database.get_contacts()[0][0]
        database.delete_contact(contact_id)
        self.assertEqual(database.get_contacts(), [])

    def test_reject_empty_contact(self):
        with self.assertRaises(ValueError):
            database.add_contact("", "+254700000000")

    def test_log_message(self):
        database.log_message("+254700000000", "Test message", "Queued")
        logs = database.get_logs()
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0][1:4], ("+254700000000", "Test message", "Queued"))


if __name__ == "__main__":
    unittest.main()

import unittest
import ranker

class TestRanker(unittest.TestCase):
    def test__get_options_list(self):
        my_ranker = ranker.Ranker()
        sample_dict = {
            "Create new list" : ranker.add_item
        }
        result_list = my_ranker._Ranker__get_options_list(sample_dict)
        actual_list = ["Create new list"]
        self.assertEquals(actual_list, result_list)

if __name__ == "__main__":
    unittest.main()


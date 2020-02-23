from neat_impl.innovation_history import InnovationHistory
import unittest


class InnovationHistoryTest(unittest.TestCase):

    def setUp(self):
        self.inno_history = InnovationHistory()

    def test_initial_call(self):
        expected = 1
        actual = self.inno_history.get_innovation(1, 3)

        self.assertEqual(expected, actual)

    def test_initial_call_adds_gene(self):
        expected = (1, 3)
        actual = self.inno_history.get_innovation(1, 3)

        self.assertEqual(expected[0], self.inno_history.connections[0][0])
        self.assertEqual(expected[1], self.inno_history.connections[0][1])

    def test_existing_gene_behavior(self):
        self.inno_history.get_innovation(1, 3)
        self.inno_history.get_innovation(2, 3)

        expected = 2

        actual = self.inno_history.get_innovation(2, 3)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()

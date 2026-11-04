import unittest

from classify import classify, field, level, place


def raw(title, loc, remote=False, hint=""):
    return dict(title=title, loc=loc, url="https://x/1", remote=remote, level_hint=hint, posted="")


class Place(unittest.TestCase):
    def test_city(self):
        self.assertEqual(place("Cluj-Napoca, CJ, Romania"), (["cluj"], False))
        self.assertEqual(place("Timișoara, TM, Romania")[0], ["timisoara"])
        self.assertEqual(place("Bucharest,Romania / Cluj, Romania")[0], ["cluj", "bucuresti"])

    def test_country_only(self):
        self.assertEqual(place("Employees can work remotely, , Romania"), (["romania"], True))

    def test_remote_europe_kept(self):
        self.assertEqual(place("Remote - Europe"), ([], True))
        self.assertEqual(place("Remote, EMEA"), ([], True))

    def test_remote_us_dropped(self):
        self.assertIsNone(place("Remote"))
        self.assertIsNone(place("Remote - United States"))
        self.assertIsNone(place("New York, NY"))

    def test_iasi_is_a_word(self):
        self.assertIsNone(place("Mexico City, Mexico"))
        self.assertEqual(place("Iași, IS, Romania")[0], ["iasi"])


class Level(unittest.TestCase):
    def test_levels(self):
        self.assertEqual(level("Software Engineer, Intern"), "intern")
        self.assertEqual(level("Working Student in Embedded Software"), "intern")
        self.assertEqual(level("Software Engineer, New Grad"), "junior")
        self.assertEqual(level("Junior Java Developer"), "junior")
        self.assertEqual(level("Senior Data Engineer"), "senior")
        self.assertEqual(level("Staff Software Engineer, Backend (Cluj)"), "senior")
        self.assertEqual(level("Software Engineer II"), "mid")

    def test_hint(self):
        self.assertEqual(level("Software Engineer", "internship"), "intern")
        self.assertEqual(level("Cybersecurity Coordinator", "entry_level"), "mid")


class Field(unittest.TestCase):
    def test_fields(self):
        self.assertEqual(field("Senior Developer (Python)"), "backend")
        self.assertEqual(field("Junior Frontend Developer"), "frontend")
        self.assertEqual(field("Full Stack Engineer"), "fullstack")
        self.assertEqual(field("Machine Learning Intern"), "data")
        self.assertEqual(field("Android Developer"), "mobile")
        self.assertEqual(field("Software Developer in Test II"), "qa")
        self.assertEqual(field("Embedded Software Engineer"), "embedded")
        self.assertEqual(field("Software Engineer II"), "software")

    def test_not_tech(self):
        for t in ("PI Construction Engineer", "Senior Sales Engineer", "Go-to-Market Engineer",
                  "Go beyond for your role!", "Electrician", "Talent Acquisition Partner",
                  "Business Developer", "Data Entry Operator"):
            self.assertIsNone(field(t), t)


class Classify(unittest.TestCase):
    def test_row(self):
        r = classify(raw("Software Engineer, Intern", "Bucharest"))
        self.assertEqual((r["cities"], r["level"], r["field"]), (["bucuresti"], "intern", "software"))

    def test_dropped(self):
        self.assertIsNone(classify(raw("Software Engineer", "Austin, TX")))
        self.assertIsNone(classify(raw("Account Executive", "Cluj-Napoca, Romania")))


if __name__ == "__main__":
    unittest.main()

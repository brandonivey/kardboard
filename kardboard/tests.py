import datetime
import unittest2


class KardboardTestCase(unittest2.TestCase):
    def setUp(self):
        import kardboard
        kardboard.app.config['MONGODB_DB'] = 'kardboard-unittest'
        self.app = kardboard.app.test_client()

    def tearDown(self):
        from mongoengine.connection import _get_db
        db = _get_db()
        #Truncate/wipe the test database
        [db.drop_collection(name) for name in db.collection_names() \
            if 'system.' not in name]

    def _get_target_class(self):
        raise NotImplementedError

    def _make_one(self, *args, **kwargs):
        return self._get_target_class()(*args, **kwargs)


class UtilTests(unittest2.TestCase):
    def test_business_days(self):
        from kardboard.util import business_days_between

        wednesday = datetime.datetime(year=2011, month=6, day=1)
        next_wednesday = datetime.datetime(year=2011, month=6, day=8)
        result = business_days_between(wednesday, next_wednesday)
        self.assertEqual(result, 5)


class KardTests(KardboardTestCase):
    def _get_target_class(self):
        from kardboard.models import Kard
        return Kard

    def test_valid_card(self):
        required_fields = {
            'key': "CMSAD-1",
            'title': "There's always money in the banana stand",
            'backlog_date': datetime.datetime.now()
        }
        k = self._make_one(**required_fields)
        k.save()
        self.assert_(k.id)

    def test_cycle_time(self):
        pass


if __name__ == "__main__":
    unittest2.main()

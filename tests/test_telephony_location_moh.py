"""
Test cases UCM profiles
"""
import random
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager

from wxc_sdk.locations import Location
from wxc_sdk.telephony.location_moh import LocationMoHSetting
from .base import TestWithLocations


class Test(TestWithLocations):

    @contextmanager
    def location_context(self):
        target_location = random.choice(self.locations)
        before = self.api.telephony.location_moh.read(location_id=target_location.location_id)
        try:
            yield target_location
        finally:
            self.api.telephony.location_moh.update(location_id=target_location.location_id,
                                                   settings=before)
            after = self.api.telephony.location_moh.read(location_id=target_location.location_id)
            self.assertEqual(before, after)

    def test_001_read_all(self):
        moh = self.api.telephony.location_moh
        with ThreadPoolExecutor() as pool:
            settings = list(pool.map(lambda location:moh.read(location_id=location.location_id),
                                     self.locations))
        print(f'Got {len(settings)} location MoH settings')

    def test_002_update_call_hold(self):
        """
        try to change call hold moh
        """
        moh = self.api.telephony.location_moh
        with self.location_context() as target_location:
            target_location: Location
            before = moh.read(location_id=target_location.location_id)
            call_hold = not before.call_hold_enabled
            settings = LocationMoHSetting(call_hold_enabled=call_hold,
                                          greeting=before.greeting)
            moh.update(location_id=target_location.location_id,
                       settings=settings)
            after = moh.read(location_id=target_location.location_id)
            self.assertEqual(settings.call_hold_enabled, after.call_hold_enabled)
            after.call_hold_enabled = before.call_hold_enabled
            self.assertEqual(before, after)

    def test_003_update_call_park(self):
        """
        try to change call park moh
        """
        moh = self.api.telephony.location_moh
        with self.location_context() as target_location:
            target_location: Location
            before = moh.read(location_id=target_location.location_id)
            call_park = not before.call_park_enabled
            settings = LocationMoHSetting(call_park_enabled=call_park,
                                          greeting=before.greeting)
            moh.update(location_id=target_location.location_id,
                       settings=settings)
            after = moh.read(location_id=target_location.location_id)
            self.assertEqual(settings.call_park_enabled, after.call_park_enabled)
            after.call_park_enabled = before.call_park_enabled
            self.assertEqual(before, after)


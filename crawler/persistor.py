import logging
from typing import Dict, List

from django.apps import apps
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.forms import model_to_dict

logger = logging.getLogger(__name__)


class Persistor:
    def get(self, model_key: str, **kwargs) -> Dict:
        raise NotImplementedError

    def get_or_create(self, model_key: str, defaults=None, **kwargs):
        raise NotImplementedError

    def update_or_create(self, model_key: str, defaults=None, **kwargs) -> Dict:
        raise NotImplementedError

    def all(self, model_key: str) -> List[Dict]:
        raise NotImplementedError


class DjangoPersistor(Persistor):
    _model_lookup_map = {
        'racetrack': 'Racetrack',
        'course_type': 'CourseType',
        'weather_category': 'WeatherCategory',
        'race': 'Race',
        'horse': 'Horse',
        'horse_sex': 'HorseSex',
        'jockey': 'Jockey',
        'trainer': 'Trainer',
    }

    def get(self, model_key: str, **kwargs) -> Dict:
        model_name = self._model_lookup_map.get(model_key)
        try:
            record = apps.get_model('server', model_name).objects.get(**kwargs)
        except (LookupError, MultipleObjectsReturned, ObjectDoesNotExist) as e:
            logger.error(f'Error occurred during model lookup: {e}')
            raise e
        else:
            return model_to_dict(record)

    def get_or_create(self, model_key: str, defaults=None, **kwargs):
        model_name = self._model_lookup_map.get(model_key)
        record, _ = apps.get_model('server', model_name).objects.get_or_create(defaults=None, **kwargs)
        return record

    def update_or_create(self, model_key: str, defaults=None, **kwargs) -> Dict:
        model_name = self._model_lookup_map.get(model_key)
        record, _ = apps.get_model('server', model_name).objects.update_or_create(defaults=defaults, **kwargs)
        return record

    def all(self, model_key: str) -> List[Dict]:
        model_name = self._model_lookup_map.get(model_key)
        query_set = apps.get_model('server', model_name).objects.all()
        return list(query_set)

import logging

from django.apps import apps
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from django.forms import model_to_dict

logger = logging.getLogger(__name__)


class Persistor:
    def get(self, model_name=None, **kwargs) -> dict:
        try:
            record = apps.get_model('server', model_name).objects.get(kwargs)
        except (LookupError, MultipleObjectsReturned, ObjectDoesNotExist) as e:
            logger.error(f'Error occurred during model lookup: {e}')
        else:
            return model_to_dict(record)

    def get_or_create(self, model_name=None, defaults=None, **kwargs):
        pass

    def update_or_create(self, model_name=None, defaults=None, **kwargs):
        pass

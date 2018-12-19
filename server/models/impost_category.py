from django.db import models

from server.models.base import BaseModel


class ImpostCategory(BaseModel):
    """
    負担重量 (馬齢|定量|別定|ハンデ)
    """
    name = models.CharField(max_length=255)

    class Meta:
        db_table = 'impost_categories'

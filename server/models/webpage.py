from django.db import models

from server.models.base import BaseModel


class WebPage(BaseModel):
    url = models.URLField()
    html = models.TextField()

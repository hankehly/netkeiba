import os
import random

import pandas as pd

from django.conf import settings


class UserAgentMiddleware(object):
    def __init__(self):
        filepath = os.path.join(settings.BASE_DIR, 'netkeiba', 'user_agents.txt')
        self.user_agent_list = pd.read_csv(filepath, header=None, delimiter='\n').values.flatten()

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agent_list)
        if user_agent:
            request.headers['User-Agent'] = user_agent

    def process_exception(self, request, exception, spider):
        user_agent = random.choice(self.user_agent_list)
        request.headers['User-Agent'] = user_agent

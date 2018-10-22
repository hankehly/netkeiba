import json
import os
import random
from itertools import chain


class UserAgentMiddleware(object):
    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        fp = open(f'{dir_path}/../node_modules/crawler-user-agents/crawler-user-agents.json', 'r')
        crawler_user_agents = json.load(fp)
        instances = [item['instances'] for item in crawler_user_agents]
        self.user_agent_list = list(chain.from_iterable(instances))

    def process_request(self, request, spider):
        user_agent = random.choice(self.user_agent_list)
        if user_agent:
            request.headers['User-Agent'] = user_agent

    def process_exception(self, request, exception, spider):
        user_agent = random.choice(self.user_agent_list)
        request.headers['User-Agent'] = user_agent

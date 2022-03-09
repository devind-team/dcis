from time import time
from channels_graphql_ws import GraphqlWsConsumer as GQLWsConsumer
from .schema import schema


class GraphqlWsConsumer(GQLWsConsumer):
    """Graphql consumer, которые обрабатывает все входящие запросы"""
    schema = schema
    group_name_prefix = ''

    async def on_connect(self, payload):
        self.scope['time'] = time()

    async def disconnect(self, code):
        await super().disconnect(code)
        for sid in self._subscriptions:
            sub_inf = self._subscriptions[sid]
            await self._run_in_worker(sub_inf.unsubscribed_callback)

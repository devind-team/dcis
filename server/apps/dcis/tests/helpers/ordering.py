"""Тестирование модуля сортировок."""

import graphene
from devind_helpers.utils import gid2int
from django.test import TestCase

from apps.core.models import User
from apps.core.schema import UserType
from apps.dcis.helpers.ordering import OrderedDjangoFilterConnectionField


class OrderedDjangoFilterConnectionFieldTestCase(TestCase):
    """Тестирование класса `OrderedDjangoFilterConnectionField`."""

    class Query(graphene.ObjectType):
        users = OrderedDjangoFilterConnectionField(UserType)

    schema = graphene.Schema(query=Query)

    def setUp(self) -> None:
        """Создание данных для тестирования."""
        self.users: list[User] = []
        for i in  range(1, 6):
            for j in range(2, 0, -1):
                self.users.append(User.objects.create(
                    username=f'user{i}{j}',
                    email=f'user{i}{j}@gmail.com',
                    first_name=f'user{i}',
                    last_name=f'user{j}',
                ))

    def test_single_forward(self) -> None:
        """Тестирование одиночной сортировки в прямом направлении."""
        result = self.schema.execute(self._get_query('["firstName"]'))
        user_ids = self._get_chunks([gid2int(u['node']['id']) for u in result.data['users']['edges']], 2)
        self.assertEqual(
            self._get_chunks([u.id for u in sorted(self.users, key=lambda u: [u.first_name])], 2),
            user_ids,
        )

    def test_single_reverse(self) -> None:
        """Тестирование одиночной сортировки в обратном направлении."""
        result = self.schema.execute(self._get_query('["-firstName"]'))
        user_ids = self._get_chunks([gid2int(u['node']['id']) for u in result.data['users']['edges']], 2)
        self.assertEqual(
            self._get_chunks([u.id for u in sorted(self.users, key=lambda u: [u.first_name], reverse=True)], 2),
            user_ids,
        )

    def test_multiple(self) -> None:
        """Тестирование множественной сортировки."""
        result = self.schema.execute(self._get_query('["firstName", "lastName"]'))
        user_ids = [gid2int(u['node']['id']) for u in result.data['users']['edges']]
        self.assertEqual(
            [u.id for u in sorted(self.users, key=lambda u: [u.first_name, u.last_name])],
            user_ids,
        )

    @staticmethod
    def _get_query(order_by: str) -> str:
        """Получение строки запроса."""
        return """query {
            users(orderBy: %s) {
                edges {
                    node {
                        id
                    }
                }
            }
        }""" % order_by

    @staticmethod
    def _get_chunks(ids: list[int], size: int) -> list[set[int]]:
        """Разделение списка идентификаторов `ids` на последовательные множества размера `size`."""
        itr = iter(ids)
        result: list[set[int]] = []
        for _ in range(len(ids) // size):
            result.append({next(itr), next(itr)})
        return result

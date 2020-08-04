from rest_framework.pagination import PageNumberPagination, OrderedDict
from rest_framework.response import Response
from utils.response import msg


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response(msg(OrderedDict([
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ])))

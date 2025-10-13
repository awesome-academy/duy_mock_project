from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100
    page_query_param = "page"

    def get_paginated_response(self, data):
        next_page = None
        previous_page = None

        if self.page.has_next():
            next_page = self.page.next_page_number()

        if self.page.has_previous():
            previous_page = self.page.previous_page_number()

        return Response(
            {
                "totalCount": self.page.paginator.count,
                "currentPage": self.page.number,
                "nextPageNumber": next_page,
                "previousPageNumber": previous_page,
                "data": data,
            }
        )

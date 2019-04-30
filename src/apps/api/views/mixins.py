# NOTE: We don't have delete mixin
from rest_framework import status
from rest_framework.response import Response


class BulkViewSetMixin(object):

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['producer'] = self.request.user
        return context

    def get_queryset(self):
        extra_prefetch = self.extra_prefetch if self.extra_prefetch else []
        qs = self.queryset
        qs = qs.prefetch_related('producer', 'user', *extra_prefetch)

        producer = self.request.query_params.get('producer', None)
        creator_id = self.request.query_params.get('creator_id', None)

        if producer:
            qs = qs.filter(producer__id=producer)
        if creator_id:
            qs = qs.filter(creator_id=creator_id)

        return qs

    def create(self, request, *args, **kwargs):
        """Overriding this for the following reasons:

        1. Returning the huge amount of HTML/etc. back by default by DRF was bad
        2. We want to handle creating many competitions this way, and we do that
           custom to make drf-writable-nested able to interpret everything easily"""
        # Make the serializer take many competitions at once
        for object in request.data:
            serializer = self.get_serializer(data=object)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        return Response({}, status=status.HTTP_201_CREATED)

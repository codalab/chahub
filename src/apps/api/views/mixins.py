from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


class ProducerModelViewSet(ModelViewSet):
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['producer'] = self.request.user
        return context

    def get_queryset(self):
        qs = self.queryset
        qs = qs.prefetch_related('producer', 'user')

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
        context = self.get_serializer_context()
        for object_data in request.data:
            if not object_data.get('producer') and context.get('producer'):
                object_data['producer'] = context['producer'].pk
            serializer = self.get_serializer(data=object_data, context=context)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
        return Response({}, status=status.HTTP_201_CREATED)

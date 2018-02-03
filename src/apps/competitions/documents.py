from django_elasticsearch_dsl import DocType, Index, StringField
from .models import Competition

competitions = Index('competitions')
competitions.settings(
    number_of_shards=1,
    number_of_replicas=0
)


# class ModelDocMixin():
#     """
#     This mixin provides some utility function for documents,
#     simplifying access to related model information.
#     """
#     @property
#     def pk(self):
#         return self.meta["id"]
#
#     def get_model_class(self):
#         # return self.get_queryset().model
#         return self._doc_type.model
#
#     def get_model_instance(self):
#         return self.get_queryset().get(pk=self.pk)


@competitions.doc_type
class CompetitionDocument(DocType):
    class Meta:
        model = Competition

        # The fields of the model you want to be indexed in Elasticsearch
        fields = [
            'title',
            'created_when',
        ]

    created_by = StringField()

    def prepare_created_by(self, instance):
        return instance.created_by

        # We are using a regular string for created_by right now, used to be a user instance
        # return instance.created_by.username if instance.created_by else ""

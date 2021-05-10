"""
  Description:    Model Mapper
"""
import logging
from core.general.exceptions import SIDException

class ModelMapper():
    """
        Model Mapper
    """

    def __init__(self, *args, **kwargs):
        self.model_maps = None
        self.source_fields = None
        self.dest_fields = None

        allowed_fields = set(['user_id', 'run_date', 'config'])
        for field in allowed_fields:
            try:
                setattr(self, field, kwargs[field])
            except Exception:
                setattr(self, field, None)

    def map(self):
        """
            find the model_map details
        """
        logging.debug('Execute Map')
        self.get_modelmaps(self.config.job.job_id)

        # self.dest_model = self.get_destmodel()
        self.dest_model = self.config.model

        if not self.dest_model:
            raise SIDException("Mandatory Field Missing", "dest model")

        self.dest_fields = self.get_fields(
            "D", self.dest_model, self.config.conn_object
        )
        if not self.dest_fields:
            raise SIDException("Mandatory Field Missing", "dest fields")

    def get_modelmaps(self, job_id):
        """
            fetch model mapping rules
        """
        from core.models.coreproxy import ModelMapProxy

        model_maps = ModelMapProxy.objects.filter(
            job_id=job_id
        ).values()
        if model_maps:
            self.model_maps = list(model_maps)

        if not self.model_maps:
            raise SIDException("Mandatory Field Missing", "Modelmap")

    def search_mapfield(self, field):
        """
            search field in the model map
        """
        # maps = []
        # if not field:
        #     return maps

        # for map in self.model_maps:
        #     if map['source_field'].lower() == field.lower():
        #         maps.append(map)

        # return maps
        if not field:
            return []

        return [map for map in self.model_maps if map['source_field'].lower() == field.lower()]

    def search_mapconstant(self):
        """
            search field in the model map
        """
        # constant = []
        # for map in self.model_maps:
        #     if map['map_type_id'] == 'constant':
        #         constant.append(map)

        return [map for map in self.model_maps if map['map_type_id'] == 'constant']
        # return constant

    def get_sourcemodel(self):
        """
            fetch source model
        """
        if self.model_maps:
            map = self.model_maps[0]
            return map['source_model']

    def get_destmodel(self):
        """
            fetch source model
        """
        if self.model_maps:
            map = self.model_maps[0]
            return map['dest_model']

    def get_fields(self, type, model_name, conn_object):
        """
            fetch destination fields
        """
        from core.models.coreproxy import FieldsProxy

        fields = FieldsProxy.objects.filter(
            model__conn_object__object_id=conn_object.object_id,
            model__name=model_name
        ).values()
        if len(fields) < 1:
            return None

        if type == 'D':
            self.dest_fields = fields
        else:
            self.source_fields = fields
        return fields

    def search_field(self, type, field_name):
        """
            find field details
        """
        if type == 'D':
            for field in self.dest_fields:
                if field['field_name'].lower() == field_name.lower():
                    return field
        else:
            for field in self.source_fields:
                if field['field_name'].lower() == field_name.lower():
                    return field
        return None

    def get_fieldtype(self, type, field_name):
        """
            find field details
        """
        field = self.search_field(type, field_name)
        if field:
            return field['field_type']
        return None

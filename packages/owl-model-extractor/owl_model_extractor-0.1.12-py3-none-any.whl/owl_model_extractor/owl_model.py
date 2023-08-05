from owlready2 import *
from owl_model_extractor import owl_model_extractor_constants_values as constants


class OwlModel:
    __ontology: Ontology
    is_loaded: bool

    def __init__(self, ontology_url):
        try:
            self.__ontology = get_ontology(ontology_url).load()
            self.is_loaded = True
        except Exception as ex:
            self.is_loaded = False

    def get_base_iri(self):
        if hasattr(self.__ontology, "base_iri"):
            return self.__ontology.base_iri
        else:
            return ""

    def get_license(self):
        for license in constants.LICENSE:
            for metadata in self.__ontology.metadata:
                if isinstance(metadata, str):
                    if license.__eq__(metadata):
                        license_list = list(
                            default_world.sparql(constants.SPARQL_STR.replace("##PH1##", license)))
                        return license_list[0]
                elif isinstance(metadata, AnnotationPropertyClass):
                    if license.__eq__(metadata.namespace.base_iri + metadata.name):
                        return self.__ontology.metadata.license

    def get_preferred_namespace_prefix(self):
        annotation_list = []
        for namespace_prefix in constants.PREFERRED_PREFIX:
            for metadata in self.__ontology.metadata:
                if isinstance(metadata, str):
                    if namespace_prefix.__eq__(metadata):
                        preferredPrefix = list(default_world.sparql(
                            constants.SPARQL_STR.replace("##PH1##", namespace_prefix)))
                        return preferredPrefix[0]
                elif isinstance(metadata, AnnotationPropertyClass):
                    if namespace_prefix.__eq__(metadata.namespace.base_iri + metadata.name):
                        return self.__ontology.metadata.preferredNamespacePrefix

    def get_preferred_namespace_uri(self):
        for namespace_uri in constants.PREFERRED_PREFIX:
            for metadata in self.__ontology.metadata:
                if isinstance(metadata, str):
                    if namespace_uri.__eq__(metadata):
                        namespace_uri_list = list(
                            default_world.sparql(constants.SPARQL_STR.replace("##PH1##", namespace_uri)))
                        return namespace_uri_list[0]
                elif isinstance(metadata, AnnotationPropertyClass):
                    if namespace_uri.__eq__(metadata.namespace.base_iri + metadata.name):
                        return self.__ontology.metadata.preferredNamespaceUri

    def get_version_iri(self):
        for version_iri in constants.VERSION:
            version_iri_list = list(
                default_world.sparql(constants.SPARQL_STR.replace("##PH1##", version_iri),error_on_undefined_entities=False))
            if version_iri_list:
                return version_iri_list[0]
            else:
                return None

    def get_metadata_as_iri_list(self) -> list:
        metadata_list = []
        list_metadata = list(self.__ontology.metadata)
        for metadata in self.__ontology.metadata:
            if isinstance(metadata, AnnotationPropertyClass):
                metadata_list.append(metadata.namespace.base_iri + metadata.name)
            elif isinstance(metadata, str):
                metadata_list.append(metadata)
        return metadata_list

    def get_namespace(self) -> str:
        return self.__ontology.get_namespace(self.__ontology.base_iri)

    def get_classes(self) -> list:
        return list(self.__ontology.classes())

    def get_object_properties(self) -> list:
        return list(self.__ontology.object_properties())

    def get_data_properties(self) -> list:
        return list(self.__ontology.data_properties())

    def get_classes_with_label(self):
        list_classes_with_label = []
        for term in self.__ontology.classes():
            if term.comment is not None and len(term.comment) > 0:
                list_classes_with_label.append(term)
        return len(list_classes_with_label)

    def get_object_properties_with_label(self):
        list_obj_with_label = []
        for term in self.__ontology.object_properties():
            if term.comment is not None and len(term.comment) > 0:
                list_obj_with_label.append(term)
        return len(list_obj_with_label)

    def get_data_properties_with_label(self):
        list_data_with_label = []
        for term in self.__ontology.data_properties():
            if term.comment is not None and len(term.comment) > 0:
                list_data_with_label.append(term)
        return len(list_data_with_label)


    def get_classes_with_description(self):
        list_classes_with_description = []
        for term in self.__ontology.classes():
            if term.comment is not None and len(term.comment) > 0:
                list_classes_with_description.append(term)
        return len(list_classes_with_description)

    def get_object_properties_with_description(self):
        list_obj_with_description = []
        for term in self.__ontology.object_properties():
            if term.comment is not None and len(term.comment) > 0:
                list_obj_with_description.append(term)
        return len(list_obj_with_description)

    def get_data_properties_with_description(self):
        list_data_with_description = []
        for term in self.__ontology.data_properties():
            if term.comment is not None and len(term.comment) > 0:
                list_data_with_description.append(term)
        return len(list_data_with_description)

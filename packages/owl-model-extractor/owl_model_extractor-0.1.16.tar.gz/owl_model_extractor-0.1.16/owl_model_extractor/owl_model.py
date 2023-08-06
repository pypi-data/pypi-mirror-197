from owlready2 import *
from owl_model_extractor import owl_model_extractor_constants_values as constants


class OwlModel:
    __ontology: Ontology
    is_loaded: bool

    def __init__(self, ontology_url):
        try:
            my_world = World()
            self.__ontology = my_world.get_ontology(ontology_url).load()
            self.is_loaded = True
        except Exception as ex:
            # traerme la url con accept rdf+xml, guardar fichero en local y procesar fichero.
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
                            self.__ontology.world.sparql(constants.SPARQL_STR.replace("##PH1##", license)))
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
                        preferredPrefix = list(self.__ontology.world.sparql(
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
                            self.__ontology.world.sparql(constants.SPARQL_STR.replace("##PH1##", namespace_uri)))
                        return namespace_uri_list[0]
                elif isinstance(metadata, AnnotationPropertyClass):
                    if namespace_uri.__eq__(metadata.namespace.base_iri + metadata.name):
                        return self.__ontology.metadata.preferredNamespaceUri

    def get_version_iri(self):
        for version_iri in constants.VERSION:
            version_iri_list = list(
                self.__ontology.world.sparql(constants.SPARQL_STR.replace("##PH1##", version_iri),
                                             error_on_undefined_entities=False))
            if version_iri_list:
                return version_iri_list[0]
            else:
                return None

    def get_metadata_as_iri_list(self) -> list:
        metadata_list = []
        for metadata in self.__ontology.metadata:
            if isinstance(metadata, AnnotationPropertyClass):
                metadata_list.append(metadata.namespace.base_iri + metadata.name)
            elif isinstance(metadata, str):
                metadata_list.append(metadata)

        for annontation_property in self.__ontology.annotation_properties():
            metadata_list.append(annontation_property.namespace.base_iri + annontation_property.name)
        graph = self.__ontology.world.as_rdflib_graph()
        list_metadata = list(
            graph.query(constants.SPARQL_METADATA_EXTRACT.replace("##PH1##", self.__ontology.base_iri)))
        for metadata in list_metadata:
            for m in metadata:
                metadata_list.append(str(m))
        return metadata_list

    def get_namespace(self) -> str:
        return self.__ontology.get_namespace(self.__ontology.base_iri)

    def get_classes(self) -> list:
        classes_list = []
        for classes in self.__ontology.classes():
            if not classes.iri.__str__().startswith(constants.NS_OWL):
                classes_list.append(classes)
        return classes_list

    def get_object_properties(self) -> list:
        obj_property_list = []
        for obj_property in self.__ontology.object_properties():
            if not obj_property.iri.__str__().startswith(constants.NS_OWL):
                obj_property_list.append(obj_property)
        return obj_property_list

    def get_data_properties(self) -> list:
        data_property_list = []
        for data_property in self.__ontology.data_properties():
            if not data_property.iri.__str__().startswith(constants.NS_OWL):
                data_property_list.append(data_property)
        return data_property_list

    def get_classes_with_label(self):
        list_classes_with_label = []
        for term in self.__ontology.classes():
            if term.label is not None and len(term.label) > 0:
                list_classes_with_label.append(term)
        return len(list_classes_with_label)

    def get_object_properties_with_label(self):
        list_obj_with_label = []
        for term in self.__ontology.object_properties():
            if term.label is not None and len(term.label) > 0:
                list_obj_with_label.append(term)
        return len(list_obj_with_label)

    def get_data_properties_with_label(self):
        list_data_with_label = []
        for term in self.__ontology.data_properties():
            if term.label is not None and len(term.label) > 0:
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

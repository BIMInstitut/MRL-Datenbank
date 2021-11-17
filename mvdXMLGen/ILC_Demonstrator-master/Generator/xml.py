# -*- coding: utf-8 -*-

from string import Formatter

#formatter for getting placeholder and set other value
class FormatXML:
    def __init__(self, template_string):
        #self.template = open(template_file).read()
        self.template = template_string
        self.required_keys = [ele[1] for ele in Formatter().parse(self.template) if ele[1]]
        #print(self.required_keys)
        self.parameters = {}

    def set_value(self, key, value):
        self.parameters[key] = value

    def generate(self):
        if not all(k in self.parameters.keys() for k in self.required_keys):
            raise ValueError("Not enough keys.")
        return self.template.format(**self.parameters)

    def __str__(self):
        return str(self.generate())

#placeholderreplacement for different templates and parts of mvdxml
class TempRule:
    @staticmethod
    def get_xml(template_string, template_rule):
        template_rule_format = FormatXML(template_string)
        template_rule_format.set_value("template_rule_parameters", template_rule)
        return template_rule_format.generate()

class Concepts:
    @staticmethod
    def get_xml(concepts_string, concept_uuid, value_name, template_uuid, requirement, er_uuid, operator, template_rules):
        concepts_format = FormatXML(concepts_string)
        concepts_format.set_value("concept_uuid", concept_uuid)
        concepts_format.set_value("value_name", value_name)
        concepts_format.set_value("template_uuid", template_uuid) #ref uuid 
        concepts_format.set_value("require", requirement)
        concepts_format.set_value("er_uuid", er_uuid) #ref uuid
        concepts_format.set_value("operator", operator)
        concepts_format.set_value("template_rules", "\n".join(template_rules))
        return concepts_format.generate()

class Applicability:
    @staticmethod
    def set_aplicaplility_format(applicability_string, template_uuid, vorbedingung):
        applicability_format = FormatXML(applicability_string)
        applicability_format.set_value("template_uuid", template_uuid)
        applicability_format.set_value("vorbedingung", "\n".join(vorbedingung))
        return applicability_format.generate()

class ConceptRoot:
    @staticmethod
    def set_cr_format(conceptroot_string, concept_root_uuid, cr_name, cr_name_ifc, applicability, concepts):
        conceptroot_format = FormatXML(conceptroot_string)
        conceptroot_format.set_value("concept_root_uuid", concept_root_uuid)
        conceptroot_format.set_value("cr_name", cr_name) 
        conceptroot_format.set_value("cr_name_ifc", cr_name_ifc) 
        conceptroot_format.set_value("applicability", "\n".join(applicability))
        conceptroot_format.set_value("concepts", "\n".join(concepts))
        return conceptroot_format.generate()

class ModelView:
    @staticmethod
    def set_view_format(view_string, view_uuid, mv_name, er_uuid, er_name, concept_roots):
        view_format = FormatXML(view_string)
        view_format.set_value("view_uuid", view_uuid)
        view_format.set_value("mv_name", mv_name) 
        view_format.set_value("er_uuid", er_uuid)
        view_format.set_value("er_name", er_name) 
        view_format.set_value("concept_roots", "\n".join(concept_roots))
        return view_format.generate()

class ConceptTemplate:
    @staticmethod
    def set_temp_format(template_string):
        template_format = FormatXML(template_string)
        return template_format.generate()

class create_XML:
    @staticmethod
    def get_xml(template, uuid, templates, views):
        formatter = FormatXML(template)
        formatter.set_value("uuid", uuid)
        formatter.set_value("templates", templates)
        formatter.set_value("views", views)
        return formatter.generate()
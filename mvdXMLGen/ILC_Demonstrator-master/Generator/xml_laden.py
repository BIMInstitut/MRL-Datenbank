#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Generator import xml
from Generator import rules
from Generator import guid
import xml.etree.ElementTree as ET

#open adding template files to written rule classes
class_to_template_file = {
    rules.ConceptTemplate: "02_ConceptTemplate.mvdxml",
    rules.ModelView: "03_View.mvdxml",
    rules.Applicability:"04_Applicability.mvdxml",
    rules.ConceptRoot: "05_ConceptRoot.mvdxml",
    rules.Concept: "06_Concepts.mvdxml",
    rules.TemplateRule: "07_TemplateRule.mvdxml",
    rules.Root: "01_Root.mvdxml"
}

def get_template_file(class_type, template_root):
    return template_root + '/' + class_to_template_file[class_type]

def get_formatted_string(template_root, rule):
    format_string = open(get_template_file(rule.__class__, template_root), 'r').read()

    if (isinstance(rule, rules.TemplateRule)):
        return xml.TempRule.get_xml(format_string, rule.get_rule())

    elif (isinstance(rule, rules.Concept)):
        template_rules = [get_formatted_string(template_root, x) for x in rule.template_rules]
        return xml.Concepts.get_xml(format_string, rule.concept_uuid, rule.value_name, rule.template_uuid, \
                                    rule.requirement, rule.er_uuid, rule.operator, template_rules)

    elif (isinstance(rule, rules.Applicability)):
        vorbedingungen = [get_formatted_string(template_root, x) for x in rule.vorbedingung]
        return xml.Applicability.set_aplicaplility_format(format_string, rule.template_uuid, vorbedingungen)

    elif (isinstance(rule, rules.ConceptRoot)):
        applicabilities = [get_formatted_string(template_root, x) for x in rule.applicability]
        concepts = [get_formatted_string(template_root, x) for x in rule.concepts]
        return xml.ConceptRoot.set_cr_format(format_string, rule.concept_root_uuid, rule.cr_name, rule.cr_name_ifc, applicabilities,
                                             concepts)
                                             
    elif (isinstance(rule, rules.ModelView)):
        concept_roots = [get_formatted_string(template_root, x) for x in rule.concept_roots]
        return xml.ModelView.set_view_format(format_string, rule.view_uuid, rule.mv_name, rule.er_uuid, rule.er_name,
                                             concept_roots)

    elif (isinstance(rule, rules.ConceptTemplate)):
        return xml.ConceptTemplate.set_temp_format(format_string)

    elif (isinstance(rule, rules.Root)):
        concept_template = get_formatted_string(template_root, rule.concept_template)
        view = get_formatted_string(template_root, rule.model_view)
        return xml.create_XML.get_xml(format_string, rule.root_uuid, concept_template, view)

def generate(template_root, rules):
    final_string = xml.create_XML.get_xml(open(get_template_file(Root, template_root), 'r').read(), guid.new_mvd(),
                                          "templates", "views")
    return ET.fromstring(final_string)

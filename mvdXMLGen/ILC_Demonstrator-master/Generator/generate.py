#!/usr/bin/env python
# -*- coding: utf-8 -*-
#https://github.com/IfcOpenShell/IfcOpenShell/blob/master/src/ifcopenshell-python/ifcopenshell/guid.py#L56

from Generator import rules
from xml.sax.saxutils import escape
import numpy as np
import os
import pathlib
from Generator import xml_laden
from Generator import rules
from itertools import groupby
from lxml import etree
 

def xml_parse_uuid(template_root):
    template_file = xml_laden.get_template_file(rules.ConceptTemplate, template_root)
    doc = etree.parse(template_file)
    uuid = doc.getroot().get('uuid')
    return uuid 


def test(concept, template_rule, row):
    template_rule.set_property_set(row[4])
    template_rule.set_property(row[5])
    concept.add_template_rule(template_rule)

def no_comparison(concept, row):
    template_rule = rules.TemplateRule()
    template_rule.set_property_set(row[4])
    if row[5]:
        template_rule.set_property(row[5])
    concept.add_template_rule(template_rule)


def read_temp_con(concept, value_type, row):
    has_comparison = False

    if row[9]: #gleich
        template_rule = rules.TemplateRule()
        template_rule.set_value("Value", value_type, "=", row[9])
        test(concept, template_rule, row)
        has_comparison = True
        return
  

    if row[10]: #ungleich
        template_rule = rules.TemplateRule()
        template_rule.set_value("Value", value_type, "!=", row[10])
        test(concept, template_rule, row)
        has_comparison = True
        return


    if row[11]: #größer
        template_rule = rules.TemplateRule()
        template_rule.set_value("Value", value_type, escape(">"), row[11])
        test(concept, template_rule, row)
        has_comparison = True
        return


    if row[12]: #größergleich
        template_rule = rules.TemplateRule()
        template_rule.set_value("Value", value_type, escape(">="), row[12])
        test(concept, template_rule, row)
        has_comparison = True
        return

    
    if row[13]: #kleiner
        template_rule = rules.TemplateRule()
        template_rule.set_value("Value", value_type, escape(">="), row[13])
        test(concept, template_rule, row)
        has_comparison = True
        return


    if row[14]: #kleinergleich
        template_rule = rules.TemplateRule()
        template_rule.set_value("Value", value_type, escape(">="), row[14])
        test(concept, template_rule, row)
        has_comparison = True
        return


    if not has_comparison:
        no_comparison(concept, row)


def read_enum_con(concept, value_type, row):

    has_comparison = False
    if row[9]:
        zelle_inhalt = row[9]
        elim_space = zelle_inhalt.replace(" ", "")
        liste_zelle = elim_space.split(',')
        for elem in liste_zelle:
            template_rule = rules.TemplateRule()
            template_rule.set_value("Value", value_type, "=", elem)
            test (concept, template_rule, row)
        concept.set_op("or")
        has_comparison = True
    
    if not has_comparison:
        no_comparison(concept, row)


def applic(pset_guid, uuid, concept_root):

    applicability = rules.Applicability(uuid)
    for i in pset_guid: 
        template_rule = rules.TemplateRule()
        template_rule.set_property_set(i)
        applicability.add_vorbedingung(template_rule)
    concept_root.add_applicability(applicability)


def content(unique_elem, person, concept_template, model_view, template_root):
    uuid = xml_parse_uuid(template_root)
    
    for elem in unique_elem:
        objectrelations = person[person[:, 3] == elem]
        pset_guid = np.unique(objectrelations[:,4])
        concept_root = rules.ConceptRoot()
        applic(pset_guid, uuid, concept_root) 
        concept_root.set_ifc_name(objectrelations[0, 3])
    

#just for psets!!!!
        for row in objectrelations:
            concept = rules.Concept(uuid, model_view.er_uuid)
            if row[8] == "No":
                pass
            else:
                if row[7] == "String" or row[7] == "Integer" or row[7] == "Real":
                    print(row[10])
                    read_temp_con(concept, "Value", row)

                elif row[7] == "Logical" or row[7] == "Boolean":
                    read_temp_con(concept, "Value", row)

                elif row[7] == "Enum":
                    read_enum_con(concept, "Value", row)

                elif row[7] == '':
                    read_temp_con(concept, "Value", row)

                elif row[7] == "Entity":
                    pass

                elif row[7] == "Binary":
                    pass
                    
                concept_root.add_concept(concept)
        yield concept_root


#reading and extracting excel colums
def generate_mvd_from_array(csv_data):
    template_root = os.path.abspath(str(pathlib.Path(__file__).parent.absolute()) + "/Templates")

    headers = list(csv_data[0, :])
    
    cols = (headers.index('Prozessbezeichnung E3'),                     #  0
            headers.index('Prozessverantwortlicher (Durchführung)'),    #  1
            headers.index('DIN 276+'),                                  #  2
            headers.index('IFC'),                                       #  3
            headers.index('Property Set'),                              #  4
            headers.index('Merkmal BUW'),                               #  5
            headers.index('Einheit'),                                   #  6
            headers.index('Datentyp'),                                  #  7
            headers.index('Notwendig'),                                 #  8
            headers.index('gleich'),                                    #  9
            headers.index('ungleich'),                                  # 10
            headers.index('größer'),                                    # 11
            headers.index('größergleich'),                              # 12
            headers.index('kleiner'),                                   # 13
            headers.index('kleinergleich'))                             # 14

    bez_und_merkmal = csv_data[1:, cols]

    dateien = []

#dividing mvdxml generation for changing process owner
    number = 0
    for k, g in groupby(bez_und_merkmal, lambda x : x[1]):
        person = np.array(list(g))
        concept_template = rules.ConceptTemplate()
        model_view = rules.ModelView()
        unique_elem = np.unique(person[:, 3])
        for cr in content(unique_elem, person, concept_template, model_view, template_root):
            model_view.add_cr(cr)

        root = rules.Root()
        root.set_ct_mv(concept_template, model_view)

        z = k
        prozessver = z.replace("/", "-")
        dateien.append(["ILC_{}-{}.mvdxml".format(number, prozessver), xml_laden.get_formatted_string(template_root, root)])
        number = number + 1
    return dateien


def csv_laden(file_data):
    csv_data = np.genfromtxt(file_data, dtype=str, delimiter=";")
    return generate_mvd_from_array(csv_data[2:,0:])
   
###################################
#cardinality???
#Unit???
##################################
# -*- coding: utf-8 -*-

from Generator import guid

#rule definition for string, here would be a parse nice
#parser to do
class PropertySetName:
    @staticmethod
    def get(property_set_name):
        return "PropertySetName[Value]='{}'".format(property_set_name)

class PropertyName:
    @staticmethod
    def get(property_name):
        return "PropertyName[Value]='{}'".format(property_name)

class ValueName:
    @staticmethod
    def get(prop_val, metricst, op, val_name):
        return "{}[{}]{}'{}'".format(prop_val, metricst, op, val_name) 

class ValueNum:
    @staticmethod
    def get(prop_val, metricst, op, val_name):
        return "{}[{}]{}{}".format(prop_val, metricst, op, val_name)    


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

#template rule setting rules
class TemplateRule:
    def __init__ (self):
        self.pset_name = "default"
        self.property_name = None
        self.prop_val = None
        self.metricst = None
        self.operator = "="
        self.value_name = None
        
    def set_property_set(self, pset_string):
        self.pset_name = pset_string

    def set_property(self, prop_string):
        self.property_name = prop_string

    def set_value(self, pv_string, me_string, op_string, val_string):
        self.prop_val = pv_string
        self.metricst = me_string
        self.operator = op_string
        self.value_name = val_string

    def get_rule_pset(self):
        result = PropertySetName.get(self.pset_name)
        return result

    def get_rule_pset_prop(self):
        result = PropertyName.get(self.property_name) + " AND " + PropertySetName.get(self.pset_name)
        return result

    def get_rule_complete(self):
        if is_number(self.value_name):  
            result = PropertySetName.get(self.pset_name) + " AND " + PropertyName.get(self.property_name) + " AND " + ValueNum.get(self.prop_val, self.metricst, self.operator, self.value_name)
        else:
            result = PropertySetName.get(self.pset_name) + " AND " + PropertyName.get(self.property_name) + " AND " + ValueName.get(self.prop_val, self.metricst, self.operator, self.value_name)
        return result

    def get_rule(self):
        if(self.pset_name != None and self.property_name != None and self.value_name != None):
            return self.get_rule_complete()
        elif (self.pset_name != None and self.property_name != None):
            return self.get_rule_pset_prop()
        else:
            return self.get_rule_pset()

#conecpt definition rules
class Concept:
    def __init__(self, ref1, ref2):
        self.concept_uuid = guid.new_mvd()
        self.value_name = "default"
        self.template_uuid = ref1
        self.requirement = "mandatory" 
        self.applicability = "both"
        self.er_uuid = ref2
        self.operator = "and"
        self.template_rules = []

    def add_template_rule(self, template_rule):
        self.template_rules.append(template_rule)

    def set_template_uuid(self, t_uuid, e_uuid):
        self.template_uuid = t_uuid
        self.er_uuid = e_uuid

    def set_requirement(self, requirement):
        self.requirement = requirement

    def set_op(self, operator):
        self.operator = operator

#applicability definition rules
class Applicability:
    def __init__(self, ref):
        self.template_uuid = ref
        self.vorbedingung = []

    def add_vorbedingung(self, name):
        self.vorbedingung.append(name)


class ConceptRoot:
    def __init__ (self):
        self.concept_root_uuid = guid.new_mvd()
        self.cr_name = "ILCValueProperty"
        self.cr_name_ifc = "IfcObject" 
        self.applicability = []
        self.concepts = []
        
    def set_uuid(self, temp_uuid):
        self.template_uuid = temp_uuid
        
    def set_name(self, name):
        self.cr_name = name

    def set_ifc_name(self, ifc_name):
        self.cr_name_ifc = ifc_name

    def add_applicability(self, applicability):
        self.applicability.append(applicability)

    def add_concept(self, concept):
        self.concepts.append(concept)


class ConceptTemplate:
    def __init__(self):
        pass



class ModelView:
    def __init__ (self):
        self.view_uuid = guid.new_mvd()
        self.mv_name = "ILCModelView"
        self.er_uuid = guid.new_mvd() # exchange requirement uuid
        self.er_name = "ILCExchangeRequirement" # exchange requirement name
        self.concept_roots = []

    def set_name(self, mv_name, er_name):
        self.mv_name = mv_name
        self.er_name = er_name

    def add_cr(self, concept_root):
        self.concept_roots.append(concept_root)


class Root:
    def __init__(self):
        self.root_uuid = guid.new_mvd()
        self.concept_template = None
        self.model_view = None

    def set_ct_mv(self, concept_template, model_view):
        self.concept_template = concept_template
        self.model_view = model_view

# -*- coding: utf-8 -*-

class specID:
    def __init__ (self):
        self.uuid = uuid
        self.shortTitle = ""
        self.fullTitle = ""
        self.subTitle = ""
        self.idmCode = ""
        self.localCode = ""
        self.bsiStatus = ""
        self.localStatus = ""
        self.version = ""

    def set_required(self, fullTitle, idmCode, bsiStatus):
        self.fullTitle = fullTitle
        self.idmCode = idmCode
        self.bsiStatus = bsiStatus
    
    def set_op_shortTitel(self, shortTitle):
        self.shortTitle = shortTitle

    def set_op_subTitle(self, subTitle):
        self.subTitle = subTitle

    def set_op_localCode(self, localCode):
        self.localCode = localCode

    def set_op_localStatus(self, localStatus):
        self.localStatus = localStatus

    def set_op_version(self, version):
        self.version = version

class er:
    pass
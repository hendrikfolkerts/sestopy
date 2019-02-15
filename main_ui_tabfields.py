# -*- coding: utf-8 -*-

__version__ = '1.0'

class SetTabFields:

    def __init__(self, main):
        self.main = main
        self.ui = main.ui

    """set the fields from the current tab"""
    def setTabFields(self):
        # model 1
        # ui elements middle
        self.main.hierarchymodeltreeviewt1 = self.ui.hierarchymodeltreeviewm1
        self.main.cbnodetypet1 = self.ui.cbnodetypem1
        self.main.buttonst1 = [self.ui.baddsubnodem1, self.ui.baddsiblingnodem1, self.ui.bdeletenodem1,
                        self.ui.bexpandallm1, self.ui.bcollapseallm1]
        self.main.tbpropertiest1 = self.ui.tbpropertiesm1
        self.main.attributefieldst1 = [self.ui.tvattributesviewm1, self.ui.lenameattributesm1, self.ui.levalueattributesm1,
                                self.ui.battributesinsertm1, self.ui.battributesdeletem1, self.ui.battributeshelpm1]
        self.main.aspectrulefieldst1 = [self.ui.tvaspectruleviewm1, self.ui.leprioritym1, self.ui.lepriorityresm1, self.ui.baspectrulehelpm1]
        self.main.numberofreplicationfieldst1 = [self.ui.levaluenumberofreplicationm1, self.ui.levaluenumberofreplicationresm1, self.ui.bnumberofreplicationhelpm1]
        self.main.couplingfieldst1 = [self.ui.tvcouplingviewm1, self.ui.lcouplingssonamem1, self.ui.lcouplingssinamem1, self.ui.cbcouplingssonamem1, self.ui.cbcouplingssinamem1, self.ui.lelistcouplingm1, self.ui.bcouplingsinsertm1,
                               self.ui.bcouplingsdeletem1, self.ui.bcouplingshelpm1, self.ui.lcbcouplingfunselectm1, self.ui.cbcouplingfunselectm1,
                               self.ui.lecouplingfunselectm1, self.ui.lecouplingfunselectresm1]
        self.main.specrulefieldst1 = [self.ui.tvspecruleviewm1, self.ui.bspecrulehelpm1]
        # general ui variables left side
        self.main.tbgeneralsettingst1 = self.ui.tbgeneralsettingsm1
        # ui variables ses pes
        self.main.rbsest1 = self.ui.rbsesm1
        self.main.rbipest1 = self.ui.rbipesm1
        self.main.rbpest1 = self.ui.rbpesm1
        self.main.rbfpest1 = self.ui.rbfpesm1
        self.main.tesescommentt1 = self.ui.tesescommentm1
        self.main.bsespeshelpt1 = self.ui.bsespeshelpm1
        # ui variables ses variables
        self.main.tvsesvariableviewt1 = self.ui.tvsesvariableviewm1
        self.main.lesesvariablenamet1 = self.ui.lesesvariablenamem1
        self.main.lesesvariablevaluet1 = self.ui.lesesvariablevaluem1
        self.main.bsesvariableinsertt1 = self.ui.bsesvariableinsertm1
        self.main.bsesvariabledeletet1 = self.ui.bsesvariabledeletem1
        self.main.bsesvariablehelpt1 = self.ui.bsesvariablehelpm1
        # ui variables ses functions
        self.main.tvsesfunctionsviewt1 = self.ui.tvsesfunctionsviewm1
        self.main.bsesfunctioninsertt1 = self.ui.bsesfunctioninsertm1
        self.main.bsesfunctiondeletet1 = self.ui.bsesfunctiondeletem1
        self.main.bsesfunctionhelpt1 = self.ui.bsesfunctionhelpm1
        # ui variables semantic conditions
        self.main.tvsemanticconditionviewt1 = self.ui.tvsemanticconditionviewm1
        self.main.lesemanticconditiont1 = self.ui.lesemanticconditionm1
        self.main.bsemanticconditioninsertt1 = self.ui.bsemanticconditioninsertm1
        self.main.bsemanticconditiondeletet1 = self.ui.bsemanticconditiondeletem1
        self.main.bsemanticconditionhelpt1 = self.ui.bsemanticconditionhelpm1
        # ui variables selection constraints
        self.main.tvselectionconstraintsviewt1 = self.ui.tvselectionconstraintsviewm1
        self.main.bselectionconstraintsstartt1 = self.ui.bselectionconstraintsstartm1
        self.main.bselectionconstraintsstopt1 = self.ui.bselectionconstraintsstopm1
        self.main.bselectionconstraintscleart1 = self.ui.bselectionconstraintsclearm1
        self.main.lstartnodenamet1 = self.ui.lstartnodenamem1
        self.main.lstopnodenamet1 = self.ui.lstopnodenamem1
        self.main.bselectionconstraintsinsertt1 = self.ui.bselectionconstraintsinsertm1
        self.main.bselectionconstraintsdeletet1 = self.ui.bselectionconstraintsdeletem1
        self.main.bselectionconstraintshelpt1 = self.ui.bselectionconstraintshelpm1

        # model 2
        # ui elements middle
        self.main.hierarchymodeltreeviewt2 = self.ui.hierarchymodeltreeviewm2
        self.main.cbnodetypet2 = self.ui.cbnodetypem2
        self.main.buttonst2 = [self.ui.baddsubnodem2, self.ui.baddsiblingnodem2, self.ui.bdeletenodem2,
                             self.ui.bexpandallm2, self.ui.bcollapseallm2]
        self.main.tbpropertiest2 = self.ui.tbpropertiesm2
        self.main.attributefieldst2 = [self.ui.tvattributesviewm2, self.ui.lenameattributesm2, self.ui.levalueattributesm2,
                                     self.ui.battributesinsertm2, self.ui.battributesdeletem2, self.ui.battributeshelpm2]
        self.main.aspectrulefieldst2 = [self.ui.tvaspectruleviewm2, self.ui.leprioritym2, self.ui.lepriorityresm2, self.ui.baspectrulehelpm2]
        self.main.numberofreplicationfieldst2 = [self.ui.levaluenumberofreplicationm2, self.ui.levaluenumberofreplicationresm2, self.ui.bnumberofreplicationhelpm2]
        self.main.couplingfieldst2 = [self.ui.tvcouplingviewm2, self.ui.lcouplingssonamem2, self.ui.lcouplingssinamem2, self.ui.cbcouplingssonamem2, self.ui.cbcouplingssinamem2, self.ui.lelistcouplingm2, self.ui.bcouplingsinsertm2,
                                    self.ui.bcouplingsdeletem2, self.ui.bcouplingshelpm2, self.ui.lcbcouplingfunselectm2, self.ui.cbcouplingfunselectm2,
                                    self.ui.lecouplingfunselectm2, self.ui.lecouplingfunselectresm2]
        self.main.specrulefieldst2 = [self.ui.tvspecruleviewm2, self.ui.bspecrulehelpm2]
        # general ui variables left side
        self.main.tbgeneralsettingst2 = self.ui.tbgeneralsettingsm2
        # ui variables ses pes
        self.main.rbsest2 = self.ui.rbsesm2
        self.main.rbipest2 = self.ui.rbipesm2
        self.main.rbpest2 = self.ui.rbpesm2
        self.main.rbfpest2 = self.ui.rbfpesm2
        self.main.tesescommentt2 = self.ui.tesescommentm2
        self.main.bsespeshelpt2 = self.ui.bsespeshelpm2
        # ui variables ses variables
        self.main.tvsesvariableviewt2 = self.ui.tvsesvariableviewm2
        self.main.lesesvariablenamet2 = self.ui.lesesvariablenamem2
        self.main.lesesvariablevaluet2 = self.ui.lesesvariablevaluem2
        self.main.bsesvariableinsertt2 = self.ui.bsesvariableinsertm2
        self.main.bsesvariabledeletet2 = self.ui.bsesvariabledeletem2
        self.main.bsesvariablehelpt2 = self.ui.bsesvariablehelpm2
        # ui variables ses functions
        self.main.tvsesfunctionsviewt2 = self.ui.tvsesfunctionsviewm2
        self.main.bsesfunctioninsertt2 = self.ui.bsesfunctioninsertm2
        self.main.bsesfunctiondeletet2 = self.ui.bsesfunctiondeletem2
        self.main.bsesfunctionhelpt2 = self.ui.bsesfunctionhelpm2
        # ui variables semantic conditions
        self.main.tvsemanticconditionviewt2 = self.ui.tvsemanticconditionviewm2
        self.main.lesemanticconditiont2 = self.ui.lesemanticconditionm2
        self.main.bsemanticconditioninsertt2 = self.ui.bsemanticconditioninsertm2
        self.main.bsemanticconditiondeletet2 = self.ui.bsemanticconditiondeletem2
        self.main.bsemanticconditionhelpt2 = self.ui.bsemanticconditionhelpm2
        # ui variables selection constraints
        self.main.tvselectionconstraintsviewt2 = self.ui.tvselectionconstraintsviewm2
        self.main.bselectionconstraintsstartt2 = self.ui.bselectionconstraintsstartm2
        self.main.bselectionconstraintsstopt2 = self.ui.bselectionconstraintsstopm2
        self.main.bselectionconstraintscleart2 = self.ui.bselectionconstraintsclearm2
        self.main.lstartnodenamet2 = self.ui.lstartnodenamem2
        self.main.lstopnodenamet2 = self.ui.lstopnodenamem2
        self.main.bselectionconstraintsinsertt2 = self.ui.bselectionconstraintsinsertm2
        self.main.bselectionconstraintsdeletet2 = self.ui.bselectionconstraintsdeletem2
        self.main.bselectionconstraintshelpt2 = self.ui.bselectionconstraintshelpm2

        # model 3
        # ui elements middle
        self.main.hierarchymodeltreeviewt3 = self.ui.hierarchymodeltreeviewm3
        self.main.cbnodetypet3 = self.ui.cbnodetypem3
        self.main.buttonst3 = [self.ui.baddsubnodem3, self.ui.baddsiblingnodem3, self.ui.bdeletenodem3,
                             self.ui.bexpandallm3, self.ui.bcollapseallm3]
        self.main.tbpropertiest3 = self.ui.tbpropertiesm3
        self.main.attributefieldst3 = [self.ui.tvattributesviewm3, self.ui.lenameattributesm3, self.ui.levalueattributesm3,
                                     self.ui.battributesinsertm3, self.ui.battributesdeletem3, self.ui.battributeshelpm3]
        self.main.aspectrulefieldst3 = [self.ui.tvaspectruleviewm3, self.ui.leprioritym3, self.ui.lepriorityresm3, self.ui.baspectrulehelpm3]
        self.main.numberofreplicationfieldst3 = [self.ui.levaluenumberofreplicationm3, self.ui.levaluenumberofreplicationresm3, self.ui.bnumberofreplicationhelpm3]
        self.main.couplingfieldst3 = [self.ui.tvcouplingviewm3, self.ui.lcouplingssonamem3, self.ui.lcouplingssinamem3, self.ui.cbcouplingssonamem3, self.ui.cbcouplingssinamem3, self.ui.lelistcouplingm3, self.ui.bcouplingsinsertm3,
                                    self.ui.bcouplingsdeletem3, self.ui.bcouplingshelpm3, self.ui.lcbcouplingfunselectm3, self.ui.cbcouplingfunselectm3,
                                    self.ui.lecouplingfunselectm3, self.ui.lecouplingfunselectresm3]
        self.main.specrulefieldst3 = [self.ui.tvspecruleviewm3, self.ui.bspecrulehelpm3]
        # general ui variables left side
        self.main.tbgeneralsettingst3 = self.ui.tbgeneralsettingsm3
        # ui variables ses pes
        self.main.rbsest3 = self.ui.rbsesm3
        self.main.rbipest3 = self.ui.rbipesm3
        self.main.rbpest3 = self.ui.rbpesm3
        self.main.rbfpest3 = self.ui.rbfpesm3
        self.main.tesescommentt3 = self.ui.tesescommentm3
        self.main.bsespeshelpt3 = self.ui.bsespeshelpm3
        # ui variables ses variables
        self.main.tvsesvariableviewt3 = self.ui.tvsesvariableviewm3
        self.main.lesesvariablenamet3 = self.ui.lesesvariablenamem3
        self.main.lesesvariablevaluet3 = self.ui.lesesvariablevaluem3
        self.main.bsesvariableinsertt3 = self.ui.bsesvariableinsertm3
        self.main.bsesvariabledeletet3 = self.ui.bsesvariabledeletem3
        self.main.bsesvariablehelpt3 = self.ui.bsesvariablehelpm3
        # ui variables ses functions
        self.main.tvsesfunctionsviewt3 = self.ui.tvsesfunctionsviewm3
        self.main.bsesfunctioninsertt3 = self.ui.bsesfunctioninsertm3
        self.main.bsesfunctiondeletet3 = self.ui.bsesfunctiondeletem3
        self.main.bsesfunctionhelpt3 = self.ui.bsesfunctionhelpm3
        # ui variables semantic conditions
        self.main.tvsemanticconditionviewt3 = self.ui.tvsemanticconditionviewm3
        self.main.lesemanticconditiont3 = self.ui.lesemanticconditionm3
        self.main.bsemanticconditioninsertt3 = self.ui.bsemanticconditioninsertm3
        self.main.bsemanticconditiondeletet3 = self.ui.bsemanticconditiondeletem3
        self.main.bsemanticconditionhelpt3 = self.ui.bsemanticconditionhelpm3
        # ui variables selection constraints
        self.main.tvselectionconstraintsviewt3 = self.ui.tvselectionconstraintsviewm3
        self.main.bselectionconstraintsstartt3 = self.ui.bselectionconstraintsstartm3
        self.main.bselectionconstraintsstopt3 = self.ui.bselectionconstraintsstopm3
        self.main.bselectionconstraintscleart3 = self.ui.bselectionconstraintsclearm3
        self.main.lstartnodenamet3 = self.ui.lstartnodenamem3
        self.main.lstopnodenamet3 = self.ui.lstopnodenamem3
        self.main.bselectionconstraintsinsertt3 = self.ui.bselectionconstraintsinsertm3
        self.main.bselectionconstraintsdeletet3 = self.ui.bselectionconstraintsdeletem3
        self.main.bselectionconstraintshelpt3 = self.ui.bselectionconstraintshelpm3

        # model 4
        # ui elements middle
        self.main.hierarchymodeltreeviewt4 = self.ui.hierarchymodeltreeviewm4
        self.main.cbnodetypet4 = self.ui.cbnodetypem4
        self.main.buttonst4 = [self.ui.baddsubnodem4, self.ui.baddsiblingnodem4, self.ui.bdeletenodem4,
                             self.ui.bexpandallm4, self.ui.bcollapseallm4]
        self.main.tbpropertiest4 = self.ui.tbpropertiesm4
        self.main.attributefieldst4 = [self.ui.tvattributesviewm4, self.ui.lenameattributesm4, self.ui.levalueattributesm4,
                                     self.ui.battributesinsertm4, self.ui.battributesdeletem4, self.ui.battributeshelpm4]
        self.main.aspectrulefieldst4 = [self.ui.tvaspectruleviewm4, self.ui.leprioritym4, self.ui.lepriorityresm4, self.ui.baspectrulehelpm4]
        self.main.numberofreplicationfieldst4 = [self.ui.levaluenumberofreplicationm4, self.ui.levaluenumberofreplicationresm4, self.ui.bnumberofreplicationhelpm4]
        self.main.couplingfieldst4 = [self.ui.tvcouplingviewm4, self.ui.lcouplingssonamem4, self.ui.lcouplingssinamem4, self.ui.cbcouplingssonamem4, self.ui.cbcouplingssinamem4, self.ui.lelistcouplingm4, self.ui.bcouplingsinsertm4,
                                    self.ui.bcouplingsdeletem4, self.ui.bcouplingshelpm4, self.ui.lcbcouplingfunselectm4, self.ui.cbcouplingfunselectm4,
                                    self.ui.lecouplingfunselectm4, self.ui.lecouplingfunselectresm4]
        self.main.specrulefieldst4 = [self.ui.tvspecruleviewm4, self.ui.bspecrulehelpm4]
        # general ui variables left side
        self.main.tbgeneralsettingst4 = self.ui.tbgeneralsettingsm4
        # ui variables ses pes
        self.main.rbsest4 = self.ui.rbsesm4
        self.main.rbipest4 = self.ui.rbipesm4
        self.main.rbpest4 = self.ui.rbpesm4
        self.main.rbfpest4 = self.ui.rbfpesm4
        self.main.tesescommentt4 = self.ui.tesescommentm4
        self.main.bsespeshelpt4 = self.ui.bsespeshelpm4
        # ui variables ses variables
        self.main.tvsesvariableviewt4 = self.ui.tvsesvariableviewm4
        self.main.lesesvariablenamet4 = self.ui.lesesvariablenamem4
        self.main.lesesvariablevaluet4 = self.ui.lesesvariablevaluem4
        self.main.bsesvariableinsertt4 = self.ui.bsesvariableinsertm4
        self.main.bsesvariabledeletet4 = self.ui.bsesvariabledeletem4
        self.main.bsesvariablehelpt4 = self.ui.bsesvariablehelpm4
        # ui variables ses functions
        self.main.tvsesfunctionsviewt4 = self.ui.tvsesfunctionsviewm4
        self.main.bsesfunctioninsertt4 = self.ui.bsesfunctioninsertm4
        self.main.bsesfunctiondeletet4 = self.ui.bsesfunctiondeletem4
        self.main.bsesfunctionhelpt4 = self.ui.bsesfunctionhelpm4
        # ui variables semantic conditions
        self.main.tvsemanticconditionviewt4 = self.ui.tvsemanticconditionviewm4
        self.main.lesemanticconditiont4 = self.ui.lesemanticconditionm4
        self.main.bsemanticconditioninsertt4 = self.ui.bsemanticconditioninsertm4
        self.main.bsemanticconditiondeletet4 = self.ui.bsemanticconditiondeletem4
        self.main.bsemanticconditionhelpt4 = self.ui.bsemanticconditionhelpm4
        # ui variables selection constraints
        self.main.tvselectionconstraintsviewt4 = self.ui.tvselectionconstraintsviewm4
        self.main.bselectionconstraintsstartt4 = self.ui.bselectionconstraintsstartm4
        self.main.bselectionconstraintsstopt4 = self.ui.bselectionconstraintsstopm4
        self.main.bselectionconstraintscleart4 = self.ui.bselectionconstraintsclearm4
        self.main.lstartnodenamet4 = self.ui.lstartnodenamem4
        self.main.lstopnodenamet4 = self.ui.lstopnodenamem4
        self.main.bselectionconstraintsinsertt4 = self.ui.bselectionconstraintsinsertm4
        self.main.bselectionconstraintsdeletet4 = self.ui.bselectionconstraintsdeletem4
        self.main.bselectionconstraintshelpt4 = self.ui.bselectionconstraintshelpm4

        # model 5
        # ui elements middle
        self.main.hierarchymodeltreeviewt5 = self.ui.hierarchymodeltreeviewm5
        self.main.cbnodetypet5 = self.ui.cbnodetypem5
        self.main.buttonst5 = [self.ui.baddsubnodem5, self.ui.baddsiblingnodem5, self.ui.bdeletenodem5,
                             self.ui.bexpandallm5, self.ui.bcollapseallm5]
        self.main.tbpropertiest5 = self.ui.tbpropertiesm5
        self.main.attributefieldst5 = [self.ui.tvattributesviewm5, self.ui.lenameattributesm5, self.ui.levalueattributesm5,
                                     self.ui.battributesinsertm5, self.ui.battributesdeletem5, self.ui.battributeshelpm5]
        self.main.aspectrulefieldst5 = [self.ui.tvaspectruleviewm5, self.ui.leprioritym5, self.ui.lepriorityresm5, self.ui.baspectrulehelpm5]
        self.main.numberofreplicationfieldst5 = [self.ui.levaluenumberofreplicationm5, self.ui.levaluenumberofreplicationresm5, self.ui.bnumberofreplicationhelpm5]
        self.main.couplingfieldst5 = [self.ui.tvcouplingviewm5, self.ui.lcouplingssonamem5, self.ui.lcouplingssinamem5, self.ui.cbcouplingssonamem5, self.ui.cbcouplingssinamem5, self.ui.lelistcouplingm5, self.ui.bcouplingsinsertm5,
                                    self.ui.bcouplingsdeletem5, self.ui.bcouplingshelpm5, self.ui.lcbcouplingfunselectm5, self.ui.cbcouplingfunselectm5,
                                    self.ui.lecouplingfunselectm5, self.ui.lecouplingfunselectresm5]
        self.main.specrulefieldst5 = [self.ui.tvspecruleviewm5, self.ui.bspecrulehelpm5]
        # general ui variables left side
        self.main.tbgeneralsettingst5 = self.ui.tbgeneralsettingsm5
        # ui variables ses pes
        self.main.rbsest5 = self.ui.rbsesm5
        self.main.rbipest5 = self.ui.rbipesm5
        self.main.rbpest5 = self.ui.rbpesm5
        self.main.rbfpest5 = self.ui.rbfpesm5
        self.main.tesescommentt5 = self.ui.tesescommentm5
        self.main.bsespeshelpt5 = self.ui.bsespeshelpm5
        # ui variables ses variables
        self.main.tvsesvariableviewt5 = self.ui.tvsesvariableviewm5
        self.main.lesesvariablenamet5 = self.ui.lesesvariablenamem5
        self.main.lesesvariablevaluet5 = self.ui.lesesvariablevaluem5
        self.main.bsesvariableinsertt5 = self.ui.bsesvariableinsertm5
        self.main.bsesvariabledeletet5 = self.ui.bsesvariabledeletem5
        self.main.bsesvariablehelpt5 = self.ui.bsesvariablehelpm5
        # ui variables ses functions
        self.main.tvsesfunctionsviewt5 = self.ui.tvsesfunctionsviewm5
        self.main.bsesfunctioninsertt5 = self.ui.bsesfunctioninsertm5
        self.main.bsesfunctiondeletet5 = self.ui.bsesfunctiondeletem5
        self.main.bsesfunctionhelpt5 = self.ui.bsesfunctionhelpm5
        # ui variables semantic conditions
        self.main.tvsemanticconditionviewt5 = self.ui.tvsemanticconditionviewm5
        self.main.lesemanticconditiont5 = self.ui.lesemanticconditionm5
        self.main.bsemanticconditioninsertt5 = self.ui.bsemanticconditioninsertm5
        self.main.bsemanticconditiondeletet5 = self.ui.bsemanticconditiondeletem5
        self.main.bsemanticconditionhelpt5 = self.ui.bsemanticconditionhelpm5
        # ui variables selection constraints
        self.main.tvselectionconstraintsviewt5 = self.ui.tvselectionconstraintsviewm5
        self.main.bselectionconstraintsstartt5 = self.ui.bselectionconstraintsstartm5
        self.main.bselectionconstraintsstopt5 = self.ui.bselectionconstraintsstopm5
        self.main.bselectionconstraintscleart5 = self.ui.bselectionconstraintsclearm5
        self.main.lstartnodenamet5 = self.ui.lstartnodenamem5
        self.main.lstopnodenamet5 = self.ui.lstopnodenamem5
        self.main.bselectionconstraintsinsertt5 = self.ui.bselectionconstraintsinsertm5
        self.main.bselectionconstraintsdeletet5 = self.ui.bselectionconstraintsdeletem5
        self.main.bselectionconstraintshelpt5 = self.ui.bselectionconstraintshelpm5

        # model 6
        # ui elements middle
        self.main.hierarchymodeltreeviewt6 = self.ui.hierarchymodeltreeviewm6
        self.main.cbnodetypet6 = self.ui.cbnodetypem6
        self.main.buttonst6 = [self.ui.baddsubnodem6, self.ui.baddsiblingnodem6, self.ui.bdeletenodem6,
                             self.ui.bexpandallm6, self.ui.bcollapseallm6]
        self.main.tbpropertiest6 = self.ui.tbpropertiesm6
        self.main.attributefieldst6 = [self.ui.tvattributesviewm6, self.ui.lenameattributesm6, self.ui.levalueattributesm6,
                                     self.ui.battributesinsertm6, self.ui.battributesdeletem6, self.ui.battributeshelpm6]
        self.main.aspectrulefieldst6 = [self.ui.tvaspectruleviewm6, self.ui.leprioritym6, self.ui.lepriorityresm6, self.ui.baspectrulehelpm6]
        self.main.numberofreplicationfieldst6 = [self.ui.levaluenumberofreplicationm6, self.ui.levaluenumberofreplicationresm6, self.ui.bnumberofreplicationhelpm6]
        self.main.couplingfieldst6 = [self.ui.tvcouplingviewm6, self.ui.lcouplingssonamem6, self.ui.lcouplingssinamem6, self.ui.cbcouplingssonamem6, self.ui.cbcouplingssinamem6, self.ui.lelistcouplingm6, self.ui.bcouplingsinsertm6,
                                    self.ui.bcouplingsdeletem6, self.ui.bcouplingshelpm6, self.ui.lcbcouplingfunselectm6, self.ui.cbcouplingfunselectm6,
                                    self.ui.lecouplingfunselectm6, self.ui.lecouplingfunselectresm6]
        self.main.specrulefieldst6 = [self.ui.tvspecruleviewm6, self.ui.bspecrulehelpm6]
        # general ui variables left side
        self.main.tbgeneralsettingst6 = self.ui.tbgeneralsettingsm6
        # ui variables ses pes
        self.main.rbsest6 = self.ui.rbsesm6
        self.main.rbipest6 = self.ui.rbipesm6
        self.main.rbpest6 = self.ui.rbpesm6
        self.main.rbfpest6 = self.ui.rbfpesm6
        self.main.tesescommentt6 = self.ui.tesescommentm6
        self.main.bsespeshelpt6 = self.ui.bsespeshelpm6
        # ui variables ses variables
        self.main.tvsesvariableviewt6 = self.ui.tvsesvariableviewm6
        self.main.lesesvariablenamet6 = self.ui.lesesvariablenamem6
        self.main.lesesvariablevaluet6 = self.ui.lesesvariablevaluem6
        self.main.bsesvariableinsertt6 = self.ui.bsesvariableinsertm6
        self.main.bsesvariabledeletet6 = self.ui.bsesvariabledeletem6
        self.main.bsesvariablehelpt6 = self.ui.bsesvariablehelpm6
        # ui variables ses functions
        self.main.tvsesfunctionsviewt6 = self.ui.tvsesfunctionsviewm6
        self.main.bsesfunctioninsertt6 = self.ui.bsesfunctioninsertm6
        self.main.bsesfunctiondeletet6 = self.ui.bsesfunctiondeletem6
        self.main.bsesfunctionhelpt6 = self.ui.bsesfunctionhelpm6
        # ui variables semantic conditions
        self.main.tvsemanticconditionviewt6 = self.ui.tvsemanticconditionviewm6
        self.main.lesemanticconditiont6 = self.ui.lesemanticconditionm6
        self.main.bsemanticconditioninsertt6 = self.ui.bsemanticconditioninsertm6
        self.main.bsemanticconditiondeletet6 = self.ui.bsemanticconditiondeletem6
        self.main.bsemanticconditionhelpt6 = self.ui.bsemanticconditionhelpm6
        # ui variables selection constraints
        self.main.tvselectionconstraintsviewt6 = self.ui.tvselectionconstraintsviewm6
        self.main.bselectionconstraintsstartt6 = self.ui.bselectionconstraintsstartm6
        self.main.bselectionconstraintsstopt6 = self.ui.bselectionconstraintsstopm6
        self.main.bselectionconstraintscleart6 = self.ui.bselectionconstraintsclearm6
        self.main.lstartnodenamet6 = self.ui.lstartnodenamem6
        self.main.lstopnodenamet6 = self.ui.lstopnodenamem6
        self.main.bselectionconstraintsinsertt6 = self.ui.bselectionconstraintsinsertm6
        self.main.bselectionconstraintsdeletet6 = self.ui.bselectionconstraintsdeletem6
        self.main.bselectionconstraintshelpt6 = self.ui.bselectionconstraintshelpm6

        # model 7
        # ui elements middle
        self.main.hierarchymodeltreeviewt7 = self.ui.hierarchymodeltreeviewm7
        self.main.cbnodetypet7 = self.ui.cbnodetypem7
        self.main.buttonst7 = [self.ui.baddsubnodem7, self.ui.baddsiblingnodem7, self.ui.bdeletenodem7,
                             self.ui.bexpandallm7, self.ui.bcollapseallm7]
        self.main.tbpropertiest7 = self.ui.tbpropertiesm7
        self.main.attributefieldst7 = [self.ui.tvattributesviewm7, self.ui.lenameattributesm7, self.ui.levalueattributesm7,
                                     self.ui.battributesinsertm7, self.ui.battributesdeletem7, self.ui.battributeshelpm7]
        self.main.aspectrulefieldst7 = [self.ui.tvaspectruleviewm7, self.ui.leprioritym7, self.ui.lepriorityresm7, self.ui.baspectrulehelpm7]
        self.main.numberofreplicationfieldst7 = [self.ui.levaluenumberofreplicationm7, self.ui.levaluenumberofreplicationresm7, self.ui.bnumberofreplicationhelpm7]
        self.main.couplingfieldst7 = [self.ui.tvcouplingviewm7, self.ui.lcouplingssonamem7, self.ui.lcouplingssinamem7, self.ui.cbcouplingssonamem7, self.ui.cbcouplingssinamem7, self.ui.lelistcouplingm7, self.ui.bcouplingsinsertm7,
                                    self.ui.bcouplingsdeletem7, self.ui.bcouplingshelpm7, self.ui.lcbcouplingfunselectm7, self.ui.cbcouplingfunselectm7,
                                    self.ui.lecouplingfunselectm7, self.ui.lecouplingfunselectresm7]
        self.main.specrulefieldst7 = [self.ui.tvspecruleviewm7, self.ui.bspecrulehelpm7]
        # general ui variables left side
        self.main.tbgeneralsettingst7 = self.ui.tbgeneralsettingsm7
        # ui variables ses pes
        self.main.rbsest7 = self.ui.rbsesm7
        self.main.rbipest7 = self.ui.rbipesm7
        self.main.rbpest7 = self.ui.rbpesm7
        self.main.rbfpest7 = self.ui.rbfpesm7
        self.main.tesescommentt7 = self.ui.tesescommentm7
        self.main.bsespeshelpt7 = self.ui.bsespeshelpm7
        # ui variables ses variables
        self.main.tvsesvariableviewt7 = self.ui.tvsesvariableviewm7
        self.main.lesesvariablenamet7 = self.ui.lesesvariablenamem7
        self.main.lesesvariablevaluet7 = self.ui.lesesvariablevaluem7
        self.main.bsesvariableinsertt7 = self.ui.bsesvariableinsertm7
        self.main.bsesvariabledeletet7 = self.ui.bsesvariabledeletem7
        self.main.bsesvariablehelpt7 = self.ui.bsesvariablehelpm7
        # ui variables ses functions
        self.main.tvsesfunctionsviewt7 = self.ui.tvsesfunctionsviewm7
        self.main.bsesfunctioninsertt7 = self.ui.bsesfunctioninsertm7
        self.main.bsesfunctiondeletet7 = self.ui.bsesfunctiondeletem7
        self.main.bsesfunctionhelpt7 = self.ui.bsesfunctionhelpm7
        # ui variables semantic conditions
        self.main.tvsemanticconditionviewt7 = self.ui.tvsemanticconditionviewm7
        self.main.lesemanticconditiont7 = self.ui.lesemanticconditionm7
        self.main.bsemanticconditioninsertt7 = self.ui.bsemanticconditioninsertm7
        self.main.bsemanticconditiondeletet7 = self.ui.bsemanticconditiondeletem7
        self.main.bsemanticconditionhelpt7 = self.ui.bsemanticconditionhelpm7
        # ui variables selection constraints
        self.main.tvselectionconstraintsviewt7 = self.ui.tvselectionconstraintsviewm7
        self.main.bselectionconstraintsstartt7 = self.ui.bselectionconstraintsstartm7
        self.main.bselectionconstraintsstopt7 = self.ui.bselectionconstraintsstopm7
        self.main.bselectionconstraintscleart7 = self.ui.bselectionconstraintsclearm7
        self.main.lstartnodenamet7 = self.ui.lstartnodenamem7
        self.main.lstopnodenamet7 = self.ui.lstopnodenamem7
        self.main.bselectionconstraintsinsertt7 = self.ui.bselectionconstraintsinsertm7
        self.main.bselectionconstraintsdeletet7 = self.ui.bselectionconstraintsdeletem7
        self.main.bselectionconstraintshelpt7 = self.ui.bselectionconstraintshelpm7

        # model 8
        # ui elements middle
        self.main.hierarchymodeltreeviewt8 = self.ui.hierarchymodeltreeviewm8
        self.main.cbnodetypet8 = self.ui.cbnodetypem8
        self.main.buttonst8 = [self.ui.baddsubnodem8, self.ui.baddsiblingnodem8, self.ui.bdeletenodem8,
                             self.ui.bexpandallm8, self.ui.bcollapseallm8]
        self.main.tbpropertiest8 = self.ui.tbpropertiesm8
        self.main.attributefieldst8 = [self.ui.tvattributesviewm8, self.ui.lenameattributesm8,
                                     self.ui.levalueattributesm8,
                                     self.ui.battributesinsertm8, self.ui.battributesdeletem8,
                                     self.ui.battributeshelpm8]
        self.main.aspectrulefieldst8 = [self.ui.tvaspectruleviewm8, self.ui.leprioritym8, self.ui.lepriorityresm8, self.ui.baspectrulehelpm8]
        self.main.numberofreplicationfieldst8 = [self.ui.levaluenumberofreplicationm8, self.ui.levaluenumberofreplicationresm8,
                                               self.ui.bnumberofreplicationhelpm8]
        self.main.couplingfieldst8 = [self.ui.tvcouplingviewm8, self.ui.lcouplingssonamem8, self.ui.lcouplingssinamem8, self.ui.cbcouplingssonamem8, self.ui.cbcouplingssinamem8, self.ui.lelistcouplingm8,
                                    self.ui.bcouplingsinsertm8,
                                    self.ui.bcouplingsdeletem8, self.ui.bcouplingshelpm8, self.ui.lcbcouplingfunselectm8,
                                    self.ui.cbcouplingfunselectm8,
                                    self.ui.lecouplingfunselectm8, self.ui.lecouplingfunselectresm8]
        self.main.specrulefieldst8 = [self.ui.tvspecruleviewm8, self.ui.bspecrulehelpm8]
        # general ui variables left side
        self.main.tbgeneralsettingst8 = self.ui.tbgeneralsettingsm8
        # ui variables ses pes
        self.main.rbsest8 = self.ui.rbsesm8
        self.main.rbipest8 = self.ui.rbipesm8
        self.main.rbpest8 = self.ui.rbpesm8
        self.main.rbfpest8 = self.ui.rbfpesm8
        self.main.tesescommentt8 = self.ui.tesescommentm8
        self.main.bsespeshelpt8 = self.ui.bsespeshelpm8
        # ui variables ses variables
        self.main.tvsesvariableviewt8 = self.ui.tvsesvariableviewm8
        self.main.lesesvariablenamet8 = self.ui.lesesvariablenamem8
        self.main.lesesvariablevaluet8 = self.ui.lesesvariablevaluem8
        self.main.bsesvariableinsertt8 = self.ui.bsesvariableinsertm8
        self.main.bsesvariabledeletet8 = self.ui.bsesvariabledeletem8
        self.main.bsesvariablehelpt8 = self.ui.bsesvariablehelpm8
        # ui variables ses functions
        self.main.tvsesfunctionsviewt8 = self.ui.tvsesfunctionsviewm8
        self.main.bsesfunctioninsertt8 = self.ui.bsesfunctioninsertm8
        self.main.bsesfunctiondeletet8 = self.ui.bsesfunctiondeletem8
        self.main.bsesfunctionhelpt8 = self.ui.bsesfunctionhelpm8
        # ui variables semantic conditions
        self.main.tvsemanticconditionviewt8 = self.ui.tvsemanticconditionviewm8
        self.main.lesemanticconditiont8 = self.ui.lesemanticconditionm8
        self.main.bsemanticconditioninsertt8 = self.ui.bsemanticconditioninsertm8
        self.main.bsemanticconditiondeletet8 = self.ui.bsemanticconditiondeletem8
        self.main.bsemanticconditionhelpt8 = self.ui.bsemanticconditionhelpm8
        # ui variables selection constraints
        self.main.tvselectionconstraintsviewt8 = self.ui.tvselectionconstraintsviewm8
        self.main.bselectionconstraintsstartt8 = self.ui.bselectionconstraintsstartm8
        self.main.bselectionconstraintsstopt8 = self.ui.bselectionconstraintsstopm8
        self.main.bselectionconstraintscleart8 = self.ui.bselectionconstraintsclearm8
        self.main.lstartnodenamet8 = self.ui.lstartnodenamem8
        self.main.lstopnodenamet8 = self.ui.lstopnodenamem8
        self.main.bselectionconstraintsinsertt8 = self.ui.bselectionconstraintsinsertm8
        self.main.bselectionconstraintsdeletet8 = self.ui.bselectionconstraintsdeletem8
        self.main.bselectionconstraintshelpt8 = self.ui.bselectionconstraintshelpm8

        # model 9
        # ui elements middle
        self.main.hierarchymodeltreeviewt9 = self.ui.hierarchymodeltreeviewm9
        self.main.cbnodetypet9 = self.ui.cbnodetypem9
        self.main.buttonst9 = [self.ui.baddsubnodem9, self.ui.baddsiblingnodem9, self.ui.bdeletenodem9,
                             self.ui.bexpandallm9, self.ui.bcollapseallm9]
        self.main.tbpropertiest9 = self.ui.tbpropertiesm9
        self.main.attributefieldst9 = [self.ui.tvattributesviewm9, self.ui.lenameattributesm9, self.ui.levalueattributesm9,
                                     self.ui.battributesinsertm9, self.ui.battributesdeletem9, self.ui.battributeshelpm9]
        self.main.aspectrulefieldst9 = [self.ui.tvaspectruleviewm9, self.ui.leprioritym9, self.ui.lepriorityresm9, self.ui.baspectrulehelpm9]
        self.main.numberofreplicationfieldst9 = [self.ui.levaluenumberofreplicationm9, self.ui.levaluenumberofreplicationresm9, self.ui.bnumberofreplicationhelpm9]
        self.main.couplingfieldst9 = [self.ui.tvcouplingviewm9, self.ui.lcouplingssonamem9, self.ui.lcouplingssinamem9, self.ui.cbcouplingssonamem9, self.ui.cbcouplingssinamem9, self.ui.lelistcouplingm9, self.ui.bcouplingsinsertm9,
                                    self.ui.bcouplingsdeletem9, self.ui.bcouplingshelpm9, self.ui.lcbcouplingfunselectm9, self.ui.cbcouplingfunselectm9,
                                    self.ui.lecouplingfunselectm9, self.ui.lecouplingfunselectresm9]
        self.main.specrulefieldst9 = [self.ui.tvspecruleviewm9, self.ui.bspecrulehelpm9]
        # general ui variables left side
        self.main.tbgeneralsettingst9 = self.ui.tbgeneralsettingsm9
        # ui variables ses pes
        self.main.rbsest9 = self.ui.rbsesm9
        self.main.rbipest9 = self.ui.rbipesm9
        self.main.rbpest9 = self.ui.rbpesm9
        self.main.rbfpest9 = self.ui.rbfpesm9
        self.main.tesescommentt9 = self.ui.tesescommentm9
        self.main.bsespeshelpt9 = self.ui.bsespeshelpm9
        # ui variables ses variables
        self.main.tvsesvariableviewt9 = self.ui.tvsesvariableviewm9
        self.main.lesesvariablenamet9 = self.ui.lesesvariablenamem9
        self.main.lesesvariablevaluet9 = self.ui.lesesvariablevaluem9
        self.main.bsesvariableinsertt9 = self.ui.bsesvariableinsertm9
        self.main.bsesvariabledeletet9 = self.ui.bsesvariabledeletem9
        self.main.bsesvariablehelpt9 = self.ui.bsesvariablehelpm9
        # ui variables ses functions
        self.main.tvsesfunctionsviewt9 = self.ui.tvsesfunctionsviewm9
        self.main.bsesfunctioninsertt9 = self.ui.bsesfunctioninsertm9
        self.main.bsesfunctiondeletet9 = self.ui.bsesfunctiondeletem9
        self.main.bsesfunctionhelpt9 = self.ui.bsesfunctionhelpm9
        # ui variables semantic conditions
        self.main.tvsemanticconditionviewt9 = self.ui.tvsemanticconditionviewm9
        self.main.lesemanticconditiont9 = self.ui.lesemanticconditionm9
        self.main.bsemanticconditioninsertt9 = self.ui.bsemanticconditioninsertm9
        self.main.bsemanticconditiondeletet9 = self.ui.bsemanticconditiondeletem9
        self.main.bsemanticconditionhelpt9 = self.ui.bsemanticconditionhelpm9
        # ui variables selection constraints
        self.main.tvselectionconstraintsviewt9 = self.ui.tvselectionconstraintsviewm9
        self.main.bselectionconstraintsstartt9 = self.ui.bselectionconstraintsstartm9
        self.main.bselectionconstraintsstopt9 = self.ui.bselectionconstraintsstopm9
        self.main.bselectionconstraintscleart9 = self.ui.bselectionconstraintsclearm9
        self.main.lstartnodenamet9 = self.ui.lstartnodenamem9
        self.main.lstopnodenamet9 = self.ui.lstopnodenamem9
        self.main.bselectionconstraintsinsertt9 = self.ui.bselectionconstraintsinsertm9
        self.main.bselectionconstraintsdeletet9 = self.ui.bselectionconstraintsdeletem9
        self.main.bselectionconstraintshelpt9 = self.ui.bselectionconstraintshelpm9

        # model 10
        # ui elements middle
        self.main.hierarchymodeltreeviewt10 = self.ui.hierarchymodeltreeviewm10
        self.main.cbnodetypet10 = self.ui.cbnodetypem10
        self.main.buttonst10 = [self.ui.baddsubnodem10, self.ui.baddsiblingnodem10, self.ui.bdeletenodem10,
                             self.ui.bexpandallm10, self.ui.bcollapseallm10]
        self.main.tbpropertiest10 = self.ui.tbpropertiesm10
        self.main.attributefieldst10 = [self.ui.tvattributesviewm10, self.ui.lenameattributesm10, self.ui.levalueattributesm10,
                                     self.ui.battributesinsertm10, self.ui.battributesdeletem10, self.ui.battributeshelpm10]
        self.main.aspectrulefieldst10 = [self.ui.tvaspectruleviewm10, self.ui.leprioritym10, self.ui.lepriorityresm10, self.ui.baspectrulehelpm10]
        self.main.numberofreplicationfieldst10 = [self.ui.levaluenumberofreplicationm10, self.ui.levaluenumberofreplicationresm10, self.ui.bnumberofreplicationhelpm10]
        self.main.couplingfieldst10 = [self.ui.tvcouplingviewm10, self.ui.lcouplingssonamem10, self.ui.lcouplingssinamem10, self.ui.cbcouplingssonamem10, self.ui.cbcouplingssinamem10, self.ui.lelistcouplingm10, self.ui.bcouplingsinsertm10,
                                    self.ui.bcouplingsdeletem10, self.ui.bcouplingshelpm10, self.ui.lcbcouplingfunselectm10 ,self.ui.cbcouplingfunselectm10,
                                    self.ui.lecouplingfunselectm10, self.ui.lecouplingfunselectresm10]
        self.main.specrulefieldst10 = [self.ui.tvspecruleviewm10, self.ui.bspecrulehelpm10]
        # general ui variables left side
        self.main.tbgeneralsettingst10 = self.ui.tbgeneralsettingsm10
        # ui variables ses pes
        self.main.rbsest10 = self.ui.rbsesm10
        self.main.rbipest10 = self.ui.rbipesm10
        self.main.rbpest10 = self.ui.rbpesm10
        self.main.rbfpest10 = self.ui.rbfpesm10
        self.main.tesescommentt10 = self.ui.tesescommentm10
        self.main.bsespeshelpt10 = self.ui.bsespeshelpm10
        # ui variables ses variables
        self.main.tvsesvariableviewt10 = self.ui.tvsesvariableviewm10
        self.main.lesesvariablenamet10 = self.ui.lesesvariablenamem10
        self.main.lesesvariablevaluet10 = self.ui.lesesvariablevaluem10
        self.main.bsesvariableinsertt10 = self.ui.bsesvariableinsertm10
        self.main.bsesvariabledeletet10 = self.ui.bsesvariabledeletem10
        self.main.bsesvariablehelpt10 = self.ui.bsesvariablehelpm10
        # ui variables ses functions
        self.main.tvsesfunctionsviewt10 = self.ui.tvsesfunctionsviewm10
        self.main.bsesfunctioninsertt10 = self.ui.bsesfunctioninsertm10
        self.main.bsesfunctiondeletet10 = self.ui.bsesfunctiondeletem10
        self.main.bsesfunctionhelpt10 = self.ui.bsesfunctionhelpm10
        # ui variables semantic conditions
        self.main.tvsemanticconditionviewt10 = self.ui.tvsemanticconditionviewm10
        self.main.lesemanticconditiont10 = self.ui.lesemanticconditionm10
        self.main.bsemanticconditioninsertt10 = self.ui.bsemanticconditioninsertm10
        self.main.bsemanticconditiondeletet10 = self.ui.bsemanticconditiondeletem10
        self.main.bsemanticconditionhelpt10 = self.ui.bsemanticconditionhelpm10
        # ui variables selection constraints
        self.main.tvselectionconstraintsviewt10 = self.ui.tvselectionconstraintsviewm10
        self.main.bselectionconstraintsstartt10 = self.ui.bselectionconstraintsstartm10
        self.main.bselectionconstraintsstopt10 = self.ui.bselectionconstraintsstopm10
        self.main.bselectionconstraintscleart10 = self.ui.bselectionconstraintsclearm10
        self.main.lstartnodenamet10 = self.ui.lstartnodenamem10
        self.main.lstopnodenamet10 = self.ui.lstopnodenamem10
        self.main.bselectionconstraintsinsertt10 = self.ui.bselectionconstraintsinsertm10
        self.main.bselectionconstraintsdeletet10 = self.ui.bselectionconstraintsdeletem10
        self.main.bselectionconstraintshelpt10 = self.ui.bselectionconstraintshelpm10
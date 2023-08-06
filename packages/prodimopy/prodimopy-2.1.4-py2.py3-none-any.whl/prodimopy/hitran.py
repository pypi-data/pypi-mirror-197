"""
.. module:: hitran
   :synopsis: Read routines and data structure for prodimo HITRAN datafiles.

.. moduleauthor:: A. M. Arabhavi


"""

import numpy as np
import pandas as pd
from scipy.constants import h,c,k
from itertools import compress

def _conv_str(a):
    return(str(a))

def _conv_float(a):
    return float(a)

def _conv_int(a):
    return int(_conv_float(a))

_HITRANclassification2004 = {
                        'global':{
                            'diatomic':['CO','HF','HCl','HBr','HI','N2','NO+'],
                            'diatomicDiffElec':['O2'],
                            'diatomicDoubletPIElec':['NO','OH','ClO'],
                            'linearTriatomic':['N2O','OCS','HCN'],
                            'linearTriatomicLargeFermiResonance':['CO2'],
                            'nonlinearTriatomic':['H2O','O3','SO2','NO2','HOCl','H2S','HO2','HOBr'],
                            'linearTetratomic':['C2H2'],
                            'pyramidalTetratomic':['NH3','PH3'],
                            'nonlinearTetratomic':['H2CO','H2O2','COF2'],
                            'polyatomic':['CH4','CH3D','CH3Cl','C2H6','HNO3','SF6','HCOOH','ClONO2','C2H4','CH3OH']
                        },
                        'local':{
                            'asymmetricRotors':['H2O','O3','SO2','NO2','HNO3','H2CO','HOCl','H2O2','COF2','H2S','HO2','HCOOH','ClONO2','HOBr','C2H4'],
                            'diatomicORlinear':['CO2','N2O','CO','HF','HCl','HBr','HI','OCS','N2','HCN','C2H2','NO+'],
                            'sphericalRotors':['SF6','CH4'],
                            'symmetricRotors':['CH3D','CH3Cl','C2H6','NH3','PH3','CH3OH'],
                            'tripletSigmaGroundElec':['O2'],
                            'doubletPiGroundElec':['NO','OH','ClO']
                        }
                        }

_HITRANlevels2004 = {
                        'global':{
                            'diatomic':                          {'upper':[['NULL',13,_conv_str],['v1',2,_conv_int]],                                                                                                                             'lower':[['NULL',13,_conv_str],['v1*',2,_conv_int]]                                                                                                                                 },
                            'diatomicDiffElec':                  {'upper':[['NULL',12,_conv_str],['X',1,_conv_str],['v1',2,_conv_int]],                                                                                                            'lower':[['NULL',12,_conv_str],['X*',1,_conv_str],['v1*',2,_conv_int]]                                                                                                               },
                            'diatomicDoubletPIElec':             {'upper':[['NULL',7,_conv_str],['X',1,_conv_str],['i',3,_conv_str],['NULL',2,_conv_str],['v1',2,_conv_int]],                                                                        'lower':[['NULL',7,_conv_str],['X*',1,_conv_str],['i*',3,_conv_str],['NULL',2,_conv_str],['v1*',2,_conv_int]]                                                                          },
                            'linearTriatomic':                   {'upper':[['NULL',7,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['l2',2,_conv_int],['v3',2,_conv_int]],                                                                        'lower':[['NULL',7,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['l2*',2,_conv_int],['v3*',2,_conv_int]]                                                                         },
                            'linearTriatomicLargeFermiResonance':{'upper':[['NULL',6,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['l2',2,_conv_int],['v3',2,_conv_int],['r',1,_conv_int]],                                                       'lower':[['NULL',6,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['l2*',2,_conv_int],['v3*',2,_conv_int],['r*',1,_conv_int]]                                                       },
                            'nonlinearTriatomic':                {'upper':[['NULL',9,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['v3',2,_conv_int]],                                                                                          'lower':[['NULL',9,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['v3*',2,_conv_int]]                                                                                            },
                            'linearTetratomic':                  {'upper':[['v1',2,_conv_int],['v2',2,_conv_int],['v3',2,_conv_int],['v4',2,_conv_int],['v5',2,_conv_int],['l',2,_conv_int],['pm',2,_conv_str],['r',2,_conv_int],['Sq',1,_conv_str]],     'lower':[['v1*',2,_conv_int],['v2*',2,_conv_int], ['v3*',2,_conv_int],['v4*',2,_conv_int],['v5*',2,_conv_int],['l*',2,_conv_int],['pm*',2,_conv_str],['r*',2,_conv_int],['Sq*',1,_conv_str]]},
                            'pyramidalTetratomic':               {'upper':[['NULL',5,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['v3',2,_conv_int],['v4',2,_conv_int],['Sq',2,_conv_int]],                                                       'lower':[['NULL',5,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['v3*',2,_conv_int],['v4*',2,_conv_int],['Sq*',2,_conv_int]]                                                       },
                            'nonlinearTetratomic':               {'upper':[['NULL',3,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['v3',2,_conv_int],['v4',2,_conv_int],['v5',2,_conv_int],['v6',2,_conv_int]],                                    'lower':[['NULL',3,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['v3*',2,_conv_int],['v4*',2,_conv_int],['v5*',2,_conv_int],['v6*',2,_conv_int]]                                   },
                            'polyatomic':                        {'upper':[['NULL',3,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['v3',2,_conv_int],['v4',2,_conv_int],['n',2,_conv_str],['C',2,_conv_str]],                                      'lower':[['NULL',3,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['v3*',2,_conv_int],['v4*',2,_conv_int],['n*',2,_conv_str],['C*',2,_conv_str]]                                     }
                        },
                        'local':{
                            'asymmetricRotors':      {'upper':[['J',3,_conv_int],['Ka',3,_conv_int],['Kc',3,_conv_int],['F',5,_conv_str],['Sym',1,_conv_str]]                ,  'lower':[['J*',3,_conv_int],['Ka*',3,_conv_int],['Kc*',3,_conv_int],['F*',5,_conv_str],['Sym*',1,_conv_str]]                                      },
                            'diatomicORlinear':      {'upper':[['NULL',10,_conv_str],['F',5,_conv_str]]                                                                   ,  'lower':[['NULL',5,_conv_str],['Br*',1,_conv_str],['J*',3,_conv_int],['Sym*',1,_conv_str],['F*',5,_conv_str]]                                     },
                            'sphericalRotors':       {'upper':[['NULL',2,_conv_str],['J',3,_conv_int],['C',2,_conv_str],['alpha',3,_conv_int],['F',5,_conv_str]]             ,  'lower':[['NULL',2,_conv_str],['J*',3,_conv_int],['C*',2,_conv_str],['alpha*',3,_conv_int],['F*',5,_conv_str]]                                    },
                            'symmetricRotors':       {'upper':[['J',3,_conv_int],['K',3,_conv_int],['l',2,_conv_int],['C',2,_conv_str],['Sym',1,_conv_str],['F',4,_conv_str]] ,  'lower':[['J*',3,_conv_int],['K*',3,_conv_int],['l*',2,_conv_int],['C*',2,_conv_str],['Sym*',1,_conv_str],['F*',4,_conv_str]]                      },
                            'tripletSigmaGroundElec':{'upper':[['NULL',10,_conv_str],['F',5,_conv_str]]                                                                   ,  'lower':[['NULL',1,_conv_str],['Br*',1,_conv_str],['N*',3,_conv_int],['Br*',1,_conv_str],['J*',3,_conv_int],['F*',5,_conv_str],['Sym*',1,_conv_str]]},
                            'doubletPiGroundElec':   {'upper':[['NULL',10,_conv_str],['F',5,_conv_str]]                                                                   ,  'lower':[['NULL',3,_conv_str],['Br*',1,_conv_str],['J*',5,_conv_float],['Sym*',1,_conv_str],['F*',5,_conv_str]]                                   }
                        }
                        }
_HITRANclassification2020 = {
                        'global':{
                            'diatomic_a':           ['CO','HF','HCl','HBr','HI','N2','NO+','H2','CS'],
                            'diatomic_b':           ['O2','NO','OH','ClO','SO'],
                            'linearTriatomic_a':    ['CO2'],
                            'linearTriatomic_b':    ['N2O','OCS','HCN','CS2'],
                            'nonlinearTriatomic':   ['H2O','O3','SO2','NO2','HOCl','H2S','HO2','HOBr'],
                            'pyramidalTetratomic_a':['NH3','PH3'],
                            'pyramidalTetratomic_b':['15NH3'],
                            'linearPolyatomic_a':   ['C2H2'],
                            'linearPolyatomic_b':   ['C4H2'],
                            'linearPolyatomic_c':   ['HC3N'],
                            'linearPolyatomic_d':   ['C2N2'],
                            'asymmetricTop_b':      ['H2O2'],
                            'asymmetricTop_a':      ['H2CO','H2O2','COF2'],
                            'planarSymmetric':      ['SO3'],
                            'sphericalTop':         ['CH4','13CH4','CF4','GeH4'],
                            'explicit':             ['CH3D','13CH3D','HNO3','CH3Cl','C2H6','CH3Br','SF6','HCOOH','ClONO2','C2H4','CH3OH','CH3CN','CH3F','CH3I']
                        },
                        'local':{
                            'asymmetricRotors_a':['H2O'],
                            'asymmetricRotors_b':['O3','SO2','HNO3','H2CO','HOCl','H2O2','COF2','H2S','HCOOH','ClONO2','HOBr','C2H4'],
                            'asymmetricRotors_c':['NO2','HO2'],
                            'closedShellDiatomicORlinear_a':['CO2','N2O','CO','HF','HCl','HBr','HI','OCS','HCN','C2H2','NO+','HC3N','CS','C2N2','CS2'],
                            'closedShellDiatomicORlinear_b':['C4H2'],
                            'closedShellDiatomicORlinear_c':['H2','N2'],
                            'sphericalRotors':['SF6','CH4','13CH4','CF6','GeH4'],
                            'symmetricRotors_a':['CH3D','13CH3D','15NH3','PH3','CH3OH','CH3CN','CH3Br','CH3Cl','CH3F','CH3I','NF3'],
                            'symmetricRotors_b':['NH3'],
                            'symmetricRotors_c':['C2H6'],
                            'planarSymmetric': ['SO3'],
                            'openShellDiatomicTripletSigmaGroundElec':['O2','SO'],
                            'openShellDiatomicDoubletPiGroundElec_a':['NO','ClO'],
                            'openShellDiatomicDoubletPiGroundElec_b':['OH']
                        }
                        }

_HITRANlevels2020 = {
                        'global':{
                            'diatomic_a':           {'upper': [['NULL',13,_conv_str],['v1',2,_conv_int]]                                                                                                                                                                                                                              ,'lower':[['NULL',13,_conv_str],['v1*',2,_conv_int]]                                                                                                                                                                                                                                      },
                            'diatomic_b':           {'upper': [['NULL',6,_conv_str],['X',2,_conv_str],['Omega',3,_conv_str],['NULL',3,_conv_str],['v1',2,_conv_int]]                                                                                                                                                                     ,'lower':[['NULL',6,_conv_str],['X*',2,_conv_str],['Omega*',3,_conv_str],['NULL',3,_conv_str],['v1*',2,_conv_int]]                                                                                                                                                                           },
                            'linearTriatomic_a':    {'upper': [['NULL',6,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['l2',2,_conv_int],['v3',2,_conv_int],['r',1,_conv_int]]                                                                                                                                                        ,'lower':[['NULL',6,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['l2*',2,_conv_int],['v3*',2,_conv_int],['r*',1,_conv_int]]                                                                                                                                                            },
                        'linearTriatomic_b':    {'upper': [['NULL',7,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['l2',2,_conv_int],['v3',2,_conv_int]]                                                                                                                                                                             ,'lower':[['NULL',7,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['l2*',2,_conv_int],['v3*',2,_conv_int]]                                                                                                                                                                              },
                            'nonlinearTriatomic':   {'upper': [['NULL',9,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['v3',2,_conv_int]]                                                                                                                                                                                           ,'lower':[['NULL',9,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['v3*',2,_conv_int]]                                                                                                                                                                                                 },
                            'pyramidalTetratomic_a':{'upper': [['NULL',5,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['v3',2,_conv_int],['v4',2,_conv_int],['Sq',2,_conv_str]]                                                                                                                                                        ,'lower':[['NULL',5,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['v3*',2,_conv_int],['v4*',2,_conv_int],['Sq*',2,_conv_str]]                                                                                                                                                            },
                            'pyramidalTetratomic_b':{'upper': [['NULL',1,_conv_str],['v1',1,_conv_int],['v2',1,_conv_int],['v3',1,_conv_int],['v4',1,_conv_int],['NULL',1,_conv_str],['l3',1],['l4',1],['NULL',1,_conv_str],['l',1],['NULL',1,_conv_str],['gamma_rib',4,_conv_str]]                                                          ,'lower':[['NULL',1,_conv_str],['v1*',1,_conv_int],['v2*',1,_conv_int],['v3*',1,_conv_int],['v4*',1,_conv_int],['NULL',1,_conv_str],['l3*',1,_conv_int],['l4*',1,_conv_int],['NULL',1,_conv_str],['l*',1,_conv_int],['NULL',1,_conv_str],['gamma_rib*',4,_conv_str]]                                },
                            'linearPolyatomic_a':   {'upper': [['NULL',1,_conv_str],['v1',1,_conv_int],['v2',1,_conv_int],['v3',1,_conv_int],['v4',2,_conv_int],['v5',2,_conv_int],['l4',2,_conv_int],['l5',2,_conv_int],['pm',1,_conv_str],['NULL',1,_conv_str],['Sq',1,_conv_str]]                                                            ,'lower':[['NULL',1,_conv_str],['v1*',1,_conv_int],['v2*',1,_conv_int],['v3*',1,_conv_int],['v4*',2,_conv_int],['v5*',2,_conv_int],['l4*',2,_conv_int],['l5*',2,_conv_int],['pm*',1,_conv_str],['NULL',1,_conv_str],['Sq*',1,_conv_str]]                                                            },
                            'linearPolyatomic_b':   {'upper': [['NULL',1,_conv_str],['v1',1,_conv_int],['v2',1,_conv_int],['v3',1,_conv_int],['v4',1,_conv_int],['v5',1,_conv_int],['v6',1,_conv_int],['v7',1,_conv_int],['v8',1,_conv_int],['v9',1,_conv_int],['NULL',1,_conv_str],['Sym',1,_conv_str],['NULL',1,_conv_str],['Sq',2,_conv_str]]   ,'lower':[['NULL',1,_conv_str],['v1*',1,_conv_int],['v2*',1,_conv_int],['v3*',1,_conv_int],['v4*',1,_conv_int],['v5*',1,_conv_int],['v6*',1,_conv_int],['v7*',1,_conv_int],['v8*',1,_conv_int],['v9*',1,_conv_int],['NULL',1,_conv_str],['Sym*',1,_conv_str],['NULL',1,_conv_str],['Sq*',2,_conv_str]] },
                            'linearPolyatomic_c':   {'upper': [['NULL',2,_conv_str],['v1',1,_conv_int],['v2',1,_conv_int],['v3',1,_conv_int],['v4',1,_conv_int],['v5',1,_conv_int],['v6',1,_conv_int],['v7',1,_conv_int],['l5',2,_conv_int],['l6',2,_conv_int],['l7',2,_conv_int]]                                                             ,'lower':[['NULL',2,_conv_str],['v1*',1,_conv_int],['v2*',1,_conv_int],['v3*',1,_conv_int],['v4*',1,_conv_int],['v5*',1,_conv_int],['v6*',1,_conv_int],['v7*',1,_conv_int],['l5*',2,_conv_int],['l6*',2,_conv_int],['l7*',2,_conv_int]]                                                            },
                            'linearPolyatomic_d':   {'upper': [['v1',2,_conv_int],['v2',2,_conv_int],['v3',2,_conv_int],['v4',2,_conv_int],['v5',2,_conv_int],['l',2,_conv_int],['pm',1,_conv_str],['r',1,_conv_int],['Sq',1,_conv_str]]                                                                                                      ,'lower':[['v1*',2,_conv_int],['v2*',2,_conv_int],['v3*',2,_conv_int],['v4*',2,_conv_int],['v5*',2,_conv_int],['l*',2,_conv_int],['pm*',1,_conv_str],['r*',1,_conv_str],['Sq*',1,_conv_str]]                                                                                                      },
                            'asymmetricTop_b':      {'upper': [['NULL',3,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['v3',2,_conv_int],['v4',2,_conv_int],['v5',2,_conv_int],['v6',2,_conv_int]]                                                                                                                                     ,'lower':[['NULL',3,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['v3*',2,_conv_int],['v4*',2,_conv_int],['v5*',2,_conv_int],['v6*',2,_conv_int]]                                                                                                                                        },
                            'asymmetricTop_a':      {'upper': [['NULL',3,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['v3',2,_conv_int],['n',1,_conv_int],['tau',1,_conv_int],['v5',2,_conv_int],['v6',2,_conv_int]]                                                                                                                   ,'lower':[['NULL',3,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['v3*',2,_conv_int],['n*',1,_conv_int],['tau*',1,_conv_int],['v5*',2,_conv_int],['v6*',2,_conv_int]]                                                                                                                     },
                            'planarSymmetric':      {'upper': [['v1',2,_conv_int],['v2',2,_conv_int],['v3',2,_conv_int],['l3',2,_conv_int],['v4',2,_conv_int],['l4',2,_conv_int],['gamma_rib',3,_conv_str]]                                                                                                                                ,'lower':[['v1*',2,_conv_int],['v2*',2,_conv_int],['v3*',2,_conv_int],['l3*',2,_conv_int],['v4*',2,_conv_int],['l4*',2,_conv_int],['gamma_rib*',3,_conv_str]]                                                                                                                                  },
                            'sphericalTop':         {'upper': [['NULL',3,_conv_str],['v1',2,_conv_int],['v2',2,_conv_int],['v3',2,_conv_int],['v4',2,_conv_int],['n',2,_conv_str],['Cg',2,_conv_str]]                                                                                                                                       ,'lower':[['NULL',3,_conv_str],['v1*',2,_conv_int],['v2*',2,_conv_int],['v3*',2,_conv_int],['v4*',2,_conv_int],['n*',2,_conv_str],['Cg*',2,_conv_str]]                                                                                                                                          },
                            'explicit':             {'upper': [['explicit',15,_conv_str]]                                                                                                                                                                                                                                            ,'lower':[['explicit*',15,_conv_str]]                                                                                                                                                                                                                                                    }
                        },
                        'local':{
                            'asymmetricRotors_a':                       {'upper':[['J',3,_conv_int],['Ka',3,_conv_int],['Kc',3,_conv_int],['F',5,_conv_str],['quad',1,_conv_str]]                                                    ,  'lower':[['J*',3,_conv_int],['Ka*',3,_conv_int],['Kc*',3,_conv_int],['F*',5,_conv_str],['quad*',1,_conv_str]]                                                                                 },
                            'asymmetricRotors_b':                       {'upper':[['J',3,_conv_int],['Ka',3,_conv_int],['Kc',3,_conv_int],['F',5,_conv_str],['Sym',1,_conv_str]]                                                     ,  'lower':[['J*',3,_conv_int],['Ka*',3,_conv_int],['Kc*',3,_conv_int],['F*',5,_conv_str],['Sym*',1,_conv_str]]                                                                                  },
                            'asymmetricRotors_c':                       {'upper':[['N',3,_conv_int],['Ka',3,_conv_int],['Kc',3,_conv_int],['F',5,_conv_str],['Sym',1,_conv_str]]                                                     ,  'lower':[['N*',3,_conv_int],['Ka*',3,_conv_int],['Kc*',3,_conv_int],['F*',5,_conv_str],['Sym*',1,_conv_str]]                                                                                  },
                            'closedShellDiatomicORlinear_a':            {'upper':[['m',1,_conv_str],['NULL',9,_conv_str],['F',5,_conv_str]]                                                                                        ,  'lower':[['NULL',5,_conv_str],['Br*',1,_conv_str],['J*',3,_conv_int],['Sym*',1,_conv_str],['F*',5,_conv_str]]                                                                                 },
                            'closedShellDiatomicORlinear_b':            {'upper':[['l6',2,_conv_str],['l7',2,_conv_str],['l8',2,_conv_str],['l9',2,_conv_str],['NULL',7,_conv_str]]                                                  ,  'lower':[['l6*',2,_conv_str],['l7*',2,_conv_str],['l8*',2,_conv_str],['l9*',2,_conv_str],['NULL',1,_conv_str],['Br*',1,_conv_str],['J*',3,_conv_int],['Sym*',1,_conv_str],['NULL',1,_conv_str]]   },
                            'closedShellDiatomicORlinear_c':            {'upper':[['m',1,_conv_str],['NULL',9,_conv_str],['F',5,_conv_str]]                                                                                        ,  'lower':[['NULL',5,_conv_str],['Br*',1,_conv_str],['J*',3,_conv_int],['mag-quad*',1,_conv_str],['F*',5,_conv_str]]                                                                            },
                            'sphericalRotors':                          {'upper':[['NULL',2,_conv_str],['J',3,_conv_int],['C',2,_conv_str],['alpha',3,_conv_int],['F',5,_conv_str]]                                                  ,  'lower':[['NULL',2,_conv_str],['J*',3,_conv_int],['C*',2,_conv_str],['alpha*',3,_conv_int],['F*',5,_conv_str]]                                                                                },
                            'symmetricRotors_a':                        {'upper':[['J',3,_conv_int],['K',3,_conv_int],['l',2,_conv_int],['C',2,_conv_str],['Sym',1,_conv_str],['F',4,_conv_str]]                                      ,  'lower':[['J*',3,_conv_int],['K*',3,_conv_int],['l*',2,_conv_int],['C*',2,_conv_str],['Sym*',1,_conv_str],['F*',4,_conv_str]]                                                                  },
                            'symmetricRotors_b':                        {'upper':[['J',3,_conv_int],['K',3,_conv_int],['l',2,_conv_int],['NULL',1,_conv_str],['gamma_rot',3,_conv_str],['gamma_rot2',3,_conv_str],['NULL',1,_conv_str]],  'lower':[['J*',3,_conv_int],['K*',3,_conv_int],['l*',2,_conv_int],['NULL',1],['gamma_rot*',3],['gamma_rot2*',3,_conv_str],['NULL',1,_conv_str]]                                               },
                            'symmetricRotors_c':                        {'upper':[['J',3,_conv_int],['K',3,_conv_int],['l',2,_conv_int],['Sym',3,_conv_str],['F',4,_conv_str]]                                                       ,  'lower':[['J*',3,_conv_int],['K*',3,_conv_int],['l*',2,_conv_int],['Sym*',3,_conv_str],['F*',4,_conv_str]]                                                                                    },
                            'planarSymmetric':                          {'upper':[['NULL',3,_conv_str],['J',3,_conv_int],['K',3,_conv_int],['NULL',2,_conv_str],['gamma_rot',3,_conv_str],['NULL',1,_conv_str]]                       ,  'lower':[['NULL',3,_conv_str],['J*',3,_conv_int],['K*',3,_conv_int],['NULL',2,_conv_str],['gamma_rot*',3,_conv_str],['NULL',1,_conv_str]]                                                      },
                            'openShellDiatomicTripletSigmaGroundElec':  {'upper':[['NULL',10,_conv_str],['F',5,_conv_str]]                                                                                                        ,  'lower':[['NULL',1,_conv_str],['Br*',1,_conv_str],['N*',3,_conv_int],['Br*',1,_conv_str],['J*',3,_conv_int],['F*',5,_conv_str],['M*',1,_conv_str]]                                              },
                            'openShellDiatomicDoubletPiGroundElec_a':   {'upper':[['m',1,_conv_str],['NULL',9,_conv_str],['F',5,_conv_str]]                                                                                        ,  'lower':[['NULL',2,_conv_str],['Br*',2,_conv_str],['J*',5,_conv_float],['Sym*',1,_conv_str],['F*',5,_conv_str]]                                                                               },
                            'openShellDiatomicDoubletPiGroundElec_b':   {'upper':[['NULL',10,_conv_str],['F',5,_conv_str]]                                                                                                        ,  'lower':[['NULL',1,_conv_str],['Br*',2,_conv_str],['J*',5,_conv_float],['ul-Sym*',2,_conv_str],['F*',5,_conv_str]]                                                                            }
                        }
                        }
_HITRANformat = [2,1,12,10,10,5,5,10,4,8,15,15,15,15,6,12,1,7,7]
_HitranFMT = np.cumsum(_HITRANformat)
_HitranFMT = np.concatenate((np.array([0]),_HitranFMT))
_HITRANcolumns = ['Molecule_ID','Isotopologue_ID','nu','S','A','gamma_air','gamma_self','E_l','n_air','del_air','global_u','global_l','local_u','local_l','err_ind','References','line_mixing','g_u','g_l']


def _fetchLevelFormat(molecule='H2O',format:int=2020,verbose:bool=False):
    if format == 2020:
        HITRANclassification = _HITRANclassification2020
        HITRANlevels = _HITRANlevels2020
    else:
        HITRANclassification = _HITRANclassification2004
        HITRANlevels = _HITRANlevels2004
    A = list(HITRANclassification['global'].values())
    B = list(HITRANclassification['global'].keys())
    molGlobalType = None
    molLocalType = None
    for i in range(len(A)):
        if molecule in A[i]:
            molGlobalType = B[i]
            break
    A = list(HITRANclassification['local'].values())
    B = list(HITRANclassification['local'].keys())
    for i in range(len(A)):
        if molecule in A[i]:
            molLocalType = B[i]
            break
    if (molGlobalType is None) or (molLocalType is None):
        raise ValueError('Requested molecule does not exist in HITRAN classification to fetch quanta level formatting')
    if verbose:
        print('HITRAN classification for ',molecule, ' is: global quanta -',molGlobalType,', local quanta -',molLocalType)
    return HITRANlevels['global'][molGlobalType]['upper'],HITRANlevels['global'][molGlobalType]['lower'],HITRANlevels['local'][molLocalType]['upper'],HITRANlevels['local'][molLocalType]['lower']

def fetchLevelData(filePath,selectedMol='H2O',isotopologue=1,sortLabel=None,lowerLam=1,higherLam=30,format:int=2020,verbose:bool=False):
    globalUpper, globalLower, localUpper, localLower = _fetchLevelFormat(selectedMol,format=format,verbose=verbose)
    gbUfmt = [row[1] for row in globalUpper]
    gbUfmt_cum = np.concatenate((np.array([0]),np.cumsum(gbUfmt)))
    gbLfmt = [row[1] for row in globalLower]
    gbLfmt_cum = np.concatenate((np.array([0]),np.cumsum(gbLfmt)))
    locUfmt = [row[1] for row in localUpper]
    locUfmt_cum = np.concatenate((np.array([0]),np.cumsum(locUfmt)))
    locLfmt = [row[1] for row in localLower]
    locLfmt_cum = np.concatenate((np.array([0]),np.cumsum(locLfmt)))

    print('Molecule: ',selectedMol)
    print('Global upper quanta: ',[row[0] for row in globalUpper if row[0] != 'NULL'])
    print('Global lower quanta: ',[row[0] for row in globalLower if row[0] != 'NULL'])
    print('Local upper quanta: ',[row[0] for row in localUpper if row[0] != 'NULL'])
    print('Local lower quanta: ',[row[0] for row in localLower if row[0] != 'NULL'])

    gu = _HITRANcolumns.index('global_u')
    gl = _HITRANcolumns.index('global_l')
    lu = _HITRANcolumns.index('local_u')
    ll = _HITRANcolumns.index('local_l')

    globalU_d = []
    globalL_d = []
    localU_d = []
    localL_d = []
    lamb = []
    iso = []
    skippedCount = 0
    with open(filePath) as A:
        for i,Firstline in enumerate(A):
            global_u = Firstline[_HitranFMT[gu]:_HitranFMT[gu+1]]
            global_l = Firstline[_HitranFMT[gl]:_HitranFMT[gl+1]]
            local_u = Firstline[_HitranFMT[lu]:_HitranFMT[lu+1]]
            local_l = Firstline[_HitranFMT[ll]:_HitranFMT[ll+1]]
            globalU_d.append(global_u)
            globalL_d.append(global_l)
            localU_d.append(local_u)
            localL_d.append(local_l)
            lamb.append(1e4/_conv_float(Firstline[_HitranFMT[2]:_HitranFMT[3]]))
            iso.append(_conv_int(Firstline[_HitranFMT[1]:_HitranFMT[2]]))
        else:
            print('End of file read')
    
    globalU = pd.DataFrame({'lambda':lamb,'Isotopologue_ID':iso})
    globalL = pd.DataFrame({'lambda':lamb,'Isotopologue_ID':iso})
    localU  = pd.DataFrame({'lambda':lamb,'Isotopologue_ID':iso})
    localL  = pd.DataFrame({'lambda':lamb,'Isotopologue_ID':iso})
    
    for i in isotopologue:
        mask_gU = (globalU['Isotopologue_ID']==i) & (globalU['lambda']>lowerLam) & (globalU['lambda']<higherLam) # | (mask_gU) 
        mask_gL = (globalL['Isotopologue_ID']==i) & (globalL['lambda']>lowerLam) & (globalL['lambda']<higherLam) # | (mask_gL) 
        mask_lU = (localU['Isotopologue_ID']==i)  & (localU['lambda']>lowerLam)  & (localU['lambda']<higherLam)  # | (mask_lU) 
        mask_lL = (localL['Isotopologue_ID']==i)  & (localL['lambda']>lowerLam)  & (localL['lambda']<higherLam)  # | (mask_lL) 
    globalUreq  = globalU[mask_gU]
    globalLreq  = globalL[mask_gL]
    localUreq   = localU[mask_lU]
    localLreq   = localL[mask_lL]
    
    globalUd = list(compress(globalU_d, mask_gU))
    globalLd = list(compress(globalL_d, mask_gL))
    localUd = list(compress(localU_d, mask_lU))
    localLd = list(compress(localL_d, mask_lL))

    globalU_d = []
    globalL_d = []
    localU_d = []
    localL_d = []

    for i,(g_U,g_L,l_U,l_L) in enumerate(zip(globalUd,globalLd,localUd,localLd)):
        try:
            D = [i]+[row[2](g_U[gbUfmt_cum[j]:gbUfmt_cum[j+1]]) for j, row in enumerate(globalUpper)]
            E = [i]+[row[2](g_L[gbLfmt_cum[j]:gbLfmt_cum[j+1]]) for j, row in enumerate(globalLower)]
            F = [i]+[row[2](l_U[locUfmt_cum[j]:locUfmt_cum[j+1]]) for j, row in enumerate(localUpper)]
            G = [i]+[row[2](l_L[locLfmt_cum[j]:locLfmt_cum[j+1]]) for j, row in enumerate(localLower)]
            # print(D)
        except:
            skippedCount += 1
            continue
        try:
            globalU_d.append(D)
            globalL_d.append(E)
            localU_d.append(F)
            localL_d.append(G)
        except:
            warnings.warn('Line: '+str(i)+' Could not append quantum state and/or nu, iso')
    if skippedCount>0:
        warnings.warn(str(skippedCount)+' lines skipped due to mismatch in pharsing format and data')
    
    globalU = pd.DataFrame(globalU_d,columns=['num']+[rows[0] for rows in globalUpper])
    globalL = pd.DataFrame(globalL_d,columns=['num']+[rows[0] for rows in globalLower])
    localU = pd.DataFrame(localU_d,columns=['num']+[rows[0] for rows in localUpper])
    localL = pd.DataFrame(localL_d,columns=['num']+[rows[0] for rows in localLower])
    
    globalU  = globalU.drop(columns='NULL', errors='ignore')
    globalL  = globalL.drop(columns='NULL', errors='ignore')
    localU   =  localU.drop(columns='NULL', errors='ignore')
    localL   =  localL.drop(columns='NULL', errors='ignore')
    globalU.index = globalUreq.index
    globalL.index = globalLreq.index
    localU.index = localUreq.index
    localL.index = localLreq.index
    globalU = pd.concat([globalU,globalUreq],axis=1)
    globalL = pd.concat([globalL,globalLreq],axis=1)
    localU = pd.concat([localU,localUreq],axis=1)
    localL = pd.concat([localL,localLreq],axis=1)
    if sortLabel!=None:
        globalU = globalU.sort_values(sortLabel)
        globalL = globalL.sort_values(sortLabel)
        localU  = localU.sort_values(sortLabel)
        localL  = localL.sort_values(sortLabel)        
    return globalU,globalL,localU,localL

def read_hitran(filePath,moleculeName,isotopologue:list=[1],lowerLam:int=1,higherLam:int=30,sort_label='lambda',quanta=False,format:int=2020,verbose:bool=False):
    '''Returns the pandas dataframe containing HITRAN data of a given molecule'''
    data = pd.read_fwf(filePath,widths=_HITRANformat,header=None, names=_HITRANcolumns)
    data['line_mixing']=data['line_mixing'].fillna(False)
    mask = pd.Series([False]*len(data),dtype=bool)
    for i in isotopologue:
        mask = (mask) | (data['Isotopologue_ID']==i)
    mol = data[mask]
    mol.insert(2,'lambda',1e4/mol['nu'],True) #adding column wavelength in microns from freq in cm-1
    mol.insert(8,'E_u',mol['E_l']+mol['nu'],True)
    mol_MIR = mol[(mol['lambda']>lowerLam) & (mol['lambda']<higherLam)]
    if quanta:
        gu,gl,lu,ll = fetchLevelData(filePath,moleculeName,isotopologue=isotopologue,sortLabel=sort_label,lowerLam=lowerLam,higherLam=higherLam,format=format,verbose=verbose)
        gu = gu.drop(columns='Isotopologue_ID',  errors='ignore')
        gl = gl.drop(columns='Isotopologue_ID',  errors='ignore')
        lu = lu.drop(columns='Isotopologue_ID',  errors='ignore')
        ll = ll.drop(columns='Isotopologue_ID',  errors='ignore')
        
        gu = gu.drop(columns='num',  errors='ignore')
        gl = gl.drop(columns='num',  errors='ignore')
        lu = lu.drop(columns='num',  errors='ignore')
        ll = ll.drop(columns='num',  errors='ignore')
        
        mol_MIR = pd.merge(mol_MIR,gu, on='lambda')
        mol_MIR = pd.merge(mol_MIR,gl, on='lambda')
        mol_MIR = pd.merge(mol_MIR,lu, on='lambda')
        mol_MIR = pd.merge(mol_MIR,ll, on='lambda')
        mol_MIR = mol_MIR.drop(columns='global_u', errors='ignore')
        mol_MIR = mol_MIR.drop(columns='global_l', errors='ignore')
        mol_MIR = mol_MIR.drop(columns='local_u',  errors='ignore')
        mol_MIR = mol_MIR.drop(columns='local_l',  errors='ignore')
        return mol_MIR
    mol_MIR = mol_MIR.sort_values(sort_label)
    return mol_MIR

def getLevelFormat(molecule:str,format:int=2020,level:str='global'):
    fmt = _fetchLevelFormat(molecule,format=format)
    if level=='global':
        j=0
    else:
        j=2
    myList = [i[0] for i in fmt[j]]
    valueToBeRemoved = 'NULL'

    try:
        while True:
            myList.remove(valueToBeRemoved)
    except ValueError:
        pass
    fmt = ''
    for i in myList:
        fmt = fmt+i+' '
    return(fmt)

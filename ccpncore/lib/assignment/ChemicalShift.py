"""Chemical shift-related library functions at API (data storage) level

"""
#=========================================================================================
# Licence, Reference and Credits
#=========================================================================================
__copyright__ = "Copyright (C) CCPN project (http://www.ccpn.ac.uk) 2014 - 2017"
__credits__ = ("Wayne Boucher, Ed Brooksbank, Rasmus H Fogh, Luca Mureddu, Timothy J Ragan & Geerten W Vuister")
__licence__ = ("CCPN licence. See http://www.ccpn.ac.uk/v3-software/downloads/license",
               "or ccpnmodel.ccpncore.memops.Credits.CcpnLicense for licence text")
__reference__ = ("For publications, please use reference from http://www.ccpn.ac.uk/v3-software/downloads/license",
               "or ccpnmodel.ccpncore.memops.Credits.CcpNmrReference")

#=========================================================================================
# Last code modification
#=========================================================================================
__modifiedBy__ = "$modifiedBy: CCPN $"
__dateModified__ = "$dateModified: 2017-07-07 16:33:12 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b5 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================

import os
from math import exp
from collections import OrderedDict

# TBD DNA/RNA residue probs
#
# Sanity checks:
#   Only on amide
#   Gly CA - ignore CB
#

ROOT_TWO_PI = 2.506628274631
PROTEIN_MOLTYPE = 'protein'
REF_STORE_DICT = {}
CHEM_ATOM_REF_DICT = {}

# Moved here from deleted ChemicalShiftRef :

REFDB_SD_MEAN =  {
  ('protein',  'Ala') : {
       "C":(177.828848,2.109680,0.452147,None),
       "CA":(53.352984,1.902676,0.210713,"HA"),
       "CB":(19.222672,1.746981,0.258369,"HB*"),
       "H":(8.198200,0.628909,0.033675,"N"),
       "HA":(4.276693,0.446260,0.146317,"CA"),
       "HB*":(1.364080,0.226681,0.212091,"CB"),
       "N":(122.708700,3.549744,0.159512,"H2"),
   },
   ('protein', 'Arg') : {
       "C":(176.476635,1.985958,0.496077,None),
       "CA":(56.956118,2.286571,0.236270,"HA"),
       "CB":(30.902098,1.776631,0.317743,"HB2"),
       "CD":(43.264272,0.631000,0.568196,"HD2"),
       "CG":(27.332456,1.047844,0.581473,"HG2"),
       "CZ":(160.254836,3.230362,0.982800,None),
       "H":(8.251157,0.626805,0.038322,"N"),
       "HA":(4.312683,0.477117,0.133977,"CA"),
       "HB2":(1.796660,0.261361,0.246530,"CB"),
       "HB3":(1.770165,0.267594,0.301147,"CB"),
       "HD2":(3.124174,0.221769,0.361798,"CD"),
       "HD3":(3.108990,0.237850,0.419433,"CD"),
       "HE":(7.358268,0.581758,0.718769,"NE"),
       "HG2":(1.565723,0.256262,0.342788,"CG"),
       "HG3":(1.543494,0.272259,0.396198,"CG"),
       "HH11":(6.806578,0.394752,0.968618,"NH1"),
       "HH12":(6.804218,0.413009,0.973446,"NH1"),
       "HH21":(6.725168,0.354246,0.971032,"NH2"),
       "HH22":(6.729098,0.436935,0.971636,"NH2"),
       "N":(120.208274,3.814534,0.208509,"H2"),
       "NE":(91.403172,13.311577,0.865419,"HE"),
       "NH1":(76.300233,12.184632,0.993060,"HH12"),
       "NH2":(75.668286,10.259347,0.993060,"HH21"),
   },
   ('protein', 'Asn') : {
       "C":(175.387335,1.722342,0.461435,None),
       "CA":(53.715068,1.780935,0.233736,"HA"),
       "CB":(38.882610,1.637450,0.291751,"HB2"),
       "CG":(176.826660,1.209325,0.911804,None),
       "H":(8.349260,0.632518,0.049966,"N"),
       "HA":(4.681485,0.371691,0.153253,"CA"),
       "HB2":(2.819383,0.300069,0.232059,"CB"),
       "HB3":(2.776859,0.314775,0.260899,"CB"),
       "HD21":(7.356185,0.463488,0.462441,"ND2"),
       "HD22":(7.141474,0.456559,0.466465,"ND2"),
       "N":(118.480741,4.131918,0.192153,"H2"),
       "ND2":(112.784090,2.263417,0.616030,"HD21"),
   },
   ('protein', 'Asp') : {
       "C":(176.552707,1.676911,0.428646,None),
       "CA":(54.879282,1.972805,0.195573,"HA"),
       "CB":(41.088030,1.475807,0.253906,"HB2"),
       "CG":(179.515246,1.549972,0.978906,None),
       "H":(8.315900,0.588151,0.036198,"N"),
       "HA":(4.603843,0.309474,0.133594,"CA"),
       "HB2":(2.726400,0.280057,0.220312,"CB"),
       "HB3":(2.683034,0.255266,0.255729,"CB"),
       "N":(120.230927,3.966225,0.146615,"H"),
   },
   ('protein', 'Cys') : { # CB from CSI, SD guess
       "C":(174.775094,1.963682,0.690521,None),
       "CA":(58.071390,3.292878,0.495920,"HA"),
       "CB":(28.6,1.8,0.549906,"HB2"),
       "H":(8.415828,0.683783,0.061519,"N"),
       "HA":(4.699157,0.549761,0.084118,"CA"),
       "HB2":(2.927206,0.473968,0.123038,"CB"),
       "HB3":(2.884519,0.495915,0.140615,"CB"),
       "HG":(2.539318,2.428652,0.998117,"SG"),
       "N":(119.339964,4.450665,0.438795,"H"),
   },
   ('protein', 'Cyss') : { # CB from CSI, SD guess
       "C":(174.775094,1.963682,0.690521,None),
       "CA":(58.071390,3.292878,0.495920,"HA"),
       "CB":(41.8,1.8,0.549906,"HB2"),
       "H":(8.415828,0.683783,0.061519,"N"),
       "HA":(4.699157,0.549761,0.084118,"CA"),
       "HB2":(2.927206,0.473968,0.123038,"CB"),
       "HB3":(2.884519,0.495915,0.140615,"CB"),
       "N":(119.339964,4.450665,0.438795,"H"),
   },
   ('protein', 'Gln') : {
       "C":(176.404030,1.920946,0.433155,None),
       "CA":(56.761798,2.082327,0.192157,"HA"),
       "CB":(29.358559,1.772749,0.260606,"HB3"),
       "CD":(179.827346,1.026666,0.926916,None),
       "CG":(33.876419,0.890980,0.516221,"HG2"),
       "H":(8.216737,0.612440,0.037790,"N"),
       "HA":(4.281435,0.448260,0.145811,"CA"),
       "HB2":(2.056673,0.235446,0.253476,"CB"),
       "HB3":(2.032193,0.243198,0.301604,"CB"),
       "HE21":(7.243197,0.430273,0.512656,"NE2"),
       "HE22":(7.014516,0.403005,0.512656,"NE2"),
       "HG2":(2.327917,0.242786,0.313369,"CG"),
       "HG3":(2.302919,0.262972,0.378610,"CG"),
       "N":(119.290354,3.686866,0.153298,"H"),
       "NE2":(111.888680,1.758582,0.612478,"HE21"),
   },
   ('protein', 'Glu') : {
       "C":(177.019843,1.918170,0.413230,None),
       "CA":(57.531344,2.064791,0.179611,"HA"),
       "CB":(30.197538,1.660817,0.241365,"HB2"),
       "CD":(182.899624,1.786294,0.982834,None),
       "CG":(36.202941,0.965699,0.497593,"HG3"),
       "H":(8.343540,0.613833,0.030563,"N"),
       "HA":(4.266130,0.434106,0.131673,"CA"),
       "HB2":(2.031746,0.198885,0.230061,"CB"),
       "HB3":(2.009291,0.202896,0.284069,"CB"),
       "HG2":(2.279046,0.202965,0.311911,"CG"),
       "HG3":(2.260935,0.206668,0.364455,"CG"),
       "N":(120.173056,3.592825,0.139837,"H2"),
   },
   ('protein', 'Gly') : {
       "C":(174.017069,1.841177,0.473382,None),
       "CA":(45.562676,1.121685,0.235463,"HA3"),
       "H":(8.330610,0.673335,0.044840,"N"),
       "HA2":(3.988405,0.369611,0.150491,"CA"),
       "HA3":(3.912364,0.373510,0.191237,"CA"),
       "N":(109.068021,3.809180,0.190418,"H"),
   },
   ('protein', 'His') : {
       "C":(175.302898,1.948641,0.514085,None),
       "CA":(56.675864,2.330521,0.279577,"HA"),
       "CB":(30.475373,2.009559,0.331690,"HB2"),
       "CD2":(119.952558,2.769141,0.787324,"HD2"),
       "CE1":(137.238155,2.346656,0.840141,"HE1"),
       "CG":(132.303333,3.787014,0.992253,None),
       "H":(8.262735,0.688922,0.100704,"N"),
       "HA":(4.627289,0.467128,0.186620,"CA"),
       "HB2":(3.110051,0.349972,0.261972,"CB"),
       "HB3":(3.057166,0.355392,0.291549,"CB"),
       "HD1":(8.265318,2.399673,0.943662,"ND1"),
       "HD2":(7.037220,0.429625,0.454930,"CD2"),
       "HE1":(8.013054,0.520085,0.517606,"CE1"),
       "HE2":(9.920824,2.588519,0.981690,"NE2"),
       "N":(119.109795,4.192319,0.235211,"H"),
       "ND1":(195.537424,37.008263,0.947183,"HD1"),
       "NE2":(177.698489,16.243778,0.952817,"HE2"),
   },
   ('protein', 'Ile') : {
       "C":(175.864340,1.828210,0.422507,None),
       "CA":(61.705518,2.600251,0.188136,"HA"),
       "CB":(38.854432,1.944834,0.252690,"HB"),
       "CD1":(13.584336,1.626539,0.482408,"HD1*"),
       "CG1":(27.780248,1.684249,0.515848,"HG13"),
       "CG2":(17.636566,1.237755,0.469613,"HG2*"),
       "H":(8.308229,0.703239,0.032858,"N"),
       "HA":(4.224109,0.580233,0.132306,"CA"),
       "HB":(1.784957,0.304183,0.218377,"CB"),
       "HD1*":(0.685842,0.282454,0.294272,"CD1"),
       "HG12":(1.270219,0.392634,0.329165,"CG1"),
       "HG13":(1.216866,0.399083,0.364059,"CG1"),
       "HG2*":(0.789078,0.258937,0.281477,"CG2"),
       "N":(121.173088,4.413042,0.150044,"H"),
   },
   ('protein', 'Leu') : {
       "C":(177.056361,1.919039,0.431646,None),
       "CA":(55.752106,2.056969,0.191568,"HA"),
       "CB":(42.540153,1.789209,0.255424,"HB2"),
       "CD1":(24.785797,1.489808,0.494267,"HD1*"),
       "CD2":(24.227473,1.601505,0.521609,"HD2*"),
       "CG":(26.875515,0.996005,0.543658,"HG"),
       "H":(8.238177,0.674706,0.033163,"N"),
       "HA":(4.346146,0.491254,0.154877,"CA"),
       "HB2":(1.616793,0.329304,0.261069,"CB"),
       "HB3":(1.534532,0.346944,0.302699,"CB"),
       "HD1*":(0.755018,0.268818,0.295114,"CD1"),
       "HD2*":(0.728231,0.285852,0.323337,"CD2"),
       "HG":(1.509274,0.327438,0.357559,"CG"),
       "N":(121.455301,4.025737,0.146587,"H2"),
   },
   ('protein', 'Lys') : {
       "C":(176.775235,1.906749,0.452691,None),
       "CA":(57.154802,2.135196,0.229246,"HA"),
       "CB":(32.992345,1.700470,0.286857,"HB3"),
       "CD":(29.036786,0.920116,0.588718,"HD2"),
       "CE":(41.966911,0.532535,0.611722,"HE2"),
       "CG":(25.002996,0.954247,0.555511,"HG3"),
       "H":(8.190187,0.626470,0.036807,"N"),
       "HA":(4.283917,0.449233,0.134827,"CA"),
       "HB2":(1.788608,0.231602,0.230646,"CB"),
       "HB3":(1.765164,0.240192,0.286457,"CB"),
       "HD2":(1.606115,0.230201,0.433887,"CD"),
       "HD3":(1.597734,0.235158,0.490898,"CD"),
       "HE2":(2.924529,0.170173,0.447289,"CE"),
       "HE3":(2.919496,0.175103,0.516303,"CE"),
       "HG2":(1.380507,0.240617,0.340068,"CG"),
       "HG3":(1.370381,0.245205,0.400480,"CG"),
       "HZ*":(7.483198,0.367244,0.962393,"NZ"),
       "N":(120.486754,3.843313,0.179236,"H"),
       "NZ":(48.671163,36.303503,0.998200,"HZ*"),
   },
   ('protein', 'Met') : {
       "C":(176.273626,2.049059,0.449133,None),
       "CA":(56.283714,2.173536,0.205727,"HA"),
       "CB":(33.259592,2.202185,0.269028,"HB2"),
       "CE":(17.113516,1.142950,0.691786,"HE*"),
       "CG":(32.098797,1.057559,0.567445,"HG3"),
       "H":(8.266266,0.624249,0.094951,"N"),
       "HA":(4.423979,0.489446,0.147702,"CA"),
       "HB2":(2.033462,0.323993,0.271289,"CB"),
       "HB3":(2.006533,0.336088,0.324039,"CB"),
       "HE*":(1.870402,0.366566,0.595328,"CE"),
       "HG2":(2.416216,0.370668,0.368500,"CG"),
       "HG3":(2.376700,0.421305,0.403919,"CG"),
       "N":(119.593417,3.693716,0.196684,"H2"),
   },
   ('protein', 'Phe') : {
       "C":(175.565521,1.948348,0.445665,None),
       "CA":(58.305101,2.551980,0.217338,"HA"),
       "CB":(40.181708,1.952764,0.279609,"HB2"),
       "CD1":(131.626637,1.261599,0.746439,"HD1"),
       "CD2":(131.620012,1.257999,0.828246,"HD2"),
       "CE1":(130.696973,1.484393,0.782662,"HE1"),
       "CE2":(130.731140,1.294712,0.853480,"HE2"),
       "CD*":(131.620012,1.257999,0.828246,"HD*"),
       "CE*":(130.696973,1.484393,0.782662,"HE*"),
       "CG":(137.410725,3.251523,0.994302,None),
       "CZ":(129.222986,1.622311,0.835165,"HZ"),
       "H":(8.382242,0.749659,0.058201,"N"),
       "HA":(4.648786,0.588854,0.160765,"CA"),
       "HB2":(2.998135,0.362851,0.245828,"CB"),
       "HB3":(2.952455,0.375443,0.268620,"CB"),
       "HD1":(7.058833,0.306262,0.365893,"CD1"),
       "HD2":(7.065550,0.304958,0.494506,"CD2"),
       "HE1":(7.081438,0.306502,0.435083,"CE1"),
       "HE2":(7.084839,0.303505,0.541718,"CE2"),
       "HD*":(7.065550,0.304958,0.494506,"CD*"),
       "HE*":(7.081438,0.306502,0.435083,"CE*"),
       "HZ":(6.996208,0.413472,0.582418,"CZ"),
       "N":(120.085399,4.232138,0.169312,"H3"),
   },
   ('protein', 'Pro') : {
       "C":(176.780325,1.499687,0.483755,None),
       "CA":(63.539193,1.404973,0.228159,"HA"),
       "CB":(31.977618,1.011604,0.292058,"HB2"),
       "CD":(50.448136,0.757834,0.560289,"HD2"),
       "CG":(27.325400,0.926700,0.575090,"HG3"),
       "HA":(4.408505,0.329217,0.180505,"CA"),
       "HB2":(2.077811,0.327969,0.257040,"CB"),
       "HB3":(2.029493,0.322236,0.275812,"CB"),
       "HD2":(3.665299,0.317100,0.331408,"CD"),
       "HD3":(3.643425,0.338100,0.362816,"CD"),
       "HG2":(1.944234,0.266628,0.361372,"CG"),
       "HG3":(1.920546,0.282568,0.404693,"CG"),
       "N":(131.085662,9.209093,0.979783,"H3"),
   },
   ('protein', 'Ser') : {
       "C":(174.683288,1.659248,0.464592,None),
       "CA":(58.850778,2.018005,0.217349,"HA"),
       "CB":(63.993613,1.384288,0.300172,"HB3"),
       "H":(8.290302,0.607958,0.058564,"N"),
       "HA":(4.513436,0.420120,0.147023,"CA"),
       "HB2":(3.884335,0.239598,0.248714,"CB"),
       "HB3":(3.861902,0.250070,0.313159,"CB"),
       "HG":(5.575657,1.195882,0.988238,"OG"),
       "N":(115.813074,3.723294,0.185739,"H3"),
   },
   ('protein', 'Thr') : {
       "C":(174.631688,1.707400,0.462333,None),
       "CA":(62.366001,2.580251,0.224368,"HA"),
       "CB":(69.886568,1.524338,0.292086,"HB"),
       "CG2":(21.649765,0.958760,0.519445,"HG2*"),
       "H":(8.264453,0.646697,0.039162,"N"),
       "HA":(4.487641,0.495678,0.153658,"CA"),
       "HB":(4.167755,0.343464,0.253196,"CB"),
       "HG1":(5.132804,1.738798,0.975524,"OG1"),
       "HG2*":(1.144699,0.201156,0.278216,"CG2"),
       "N":(115.081474,4.991324,0.158009,"H"),
   },
   ('protein', 'Trp') : {
       "C":(176.218157,1.939642,0.518771,None),
       "CA":(57.833198,2.507920,0.324232,"HA"),
       "CB":(30.290294,1.875868,0.369738,"HB2"),
       "CD1":(126.600126,1.837343,0.715586,"HD1"),
       "CD2":(128.065000,2.873504,0.990899,None),
       "CE2":(137.984074,9.322232,0.980660,None),
       "CE3":(120.528840,1.591558,0.786121,"HE3"),
       "CG":(111.433182,0.972309,0.987486,None),
       "CH2":(123.902050,1.477779,0.773606,"HH2"),
       "CZ2":(114.407511,1.382949,0.754266,"HZ2"),
       "CZ3":(121.530652,1.444072,0.781570,"HZ3"),
       "H":(8.287413,0.814690,0.110353,"N"),
       "HA":(4.708245,0.556373,0.196815,"CA"),
       "HB2":(3.173023,0.343723,0.266212,"CB"),
       "HB3":(3.134429,0.352943,0.299204,"CB"),
       "HD1":(7.138713,0.340667,0.357224,"CD1"),
       "HE1":(10.116375,0.537535,0.356086,"NE1"),
       "HE3":(7.305717,0.382677,0.411832,"CE3"),
       "HH2":(6.964333,0.346475,0.420933,"CH2"),
       "HZ2":(7.286362,0.324283,0.379977,"CZ2"),
       "HZ3":(6.871129,0.368175,0.431172,"CZ3"),
       "N":(121.285471,4.389069,0.271900,"H2"),
       "NE1":(129.398739,2.021644,0.547213,"HE1"),
   },
   ('protein', 'Tyr') : {
       "C":(175.491657,1.900925,0.487770,None),
       "CA":(58.281804,2.475766,0.264346,"HA"),
       "CB":(39.616805,2.081812,0.337723,"HB3"),
       "CD1":(132.791984,1.567221,0.745532,"HD1"),
       "CD2":(132.624189,2.080215,0.835842,"HD2"),
       "CE1":(118.057560,1.375306,0.740828,"HE1"),
       "CE2":(118.004726,1.152713,0.833960,"HE2"),
       "CD*":(132.624189,2.080215,0.835842,"HD*"),
       "CE*":(118.057560,1.375306,0.740828,"HE*"),
       "CG":(129.985070,2.882228,0.988241,None),
       "CZ":(157.562708,1.371867,0.992004,None),
       "H":(8.325909,0.750383,0.062088,"N"),
       "HA":(4.645483,0.583003,0.161336,"CA"),
       "HB2":(2.903203,0.371810,0.248824,"CB"),
       "HB3":(2.849544,0.377313,0.265757,"CB"),
       "HD1":(6.937622,0.279576,0.331609,"CD1"),
       "HD2":(6.935375,0.282040,0.447789,"CD2"),
       "HE1":(6.704741,0.220055,0.355597,"CE1"),
       "HE2":(6.705084,0.218493,0.468956,"CE2"),
       "HD*":(6.935375,0.282040,0.447789,"CD*"),
       "HE*":(6.704741,0.220055,0.355597,"CE*"),
       "HH":(9.149362,1.563879,0.984478,"OH"),
       "N":(120.200602,4.345637,0.224365,"H"),
   },
   ('protein', 'Val') : {
       "C":(175.732054,1.819574,0.437803,None),
       "CA":(62.631900,2.794401,0.199169,"HA"),
       "CB":(32.935144,1.675944,0.260559,"HB"),
       "CG1":(21.586062,1.243471,0.477960,"HG1*"),
       "CG2":(21.437030,1.431185,0.509808,"HG2*"),
       "H":(8.307943,0.704303,0.039465,"N"),
       "HA":(4.204042,0.596150,0.143780,"CA"),
       "HB":(1.992687,0.286555,0.228479,"CB"),
       "HG1*":(0.832713,0.242229,0.252943,"CG1"),
       "HG2*":(0.810046,0.266148,0.275790,"CG2"),
       "N":(120.724161,4.673536,0.144242,"H"),
   }}


"""
Below values from ftp://ftp.cbs.cnrs.fr/pub/RESCUE2

For reference see:

J Biomol NMR. 2004 Sep;30(1:47-60
From NMR chemical shifts to amino acid types: investigation of the predictive power
carried by nuclei.
Marin A, Malliavin TE, Nicolas P, Delsuc MA.
"""

RESCUE2_STATS_MISSING = [('Ala','H',0.033675),
                         ('Ala','HA',0.146317),
                         ('Ala','HB',0.212091),
                         ('Ala','C',0.452147),
                         ('Ala','CA',0.210713),
                         ('Ala','CB',0.258369),
                         ('Ala','N',0.159512),
                         ('Arg','H',0.038322),
                         ('Arg','HA',0.133977),
                         ('Arg','HB2',0.246530),
                         ('Arg','HB3',0.301147),
                         ('Arg','HG2',0.342788),
                         ('Arg','HG3',0.396198),
                         ('Arg','HD2',0.361798),
                         ('Arg','HD3',0.419433),
                         ('Arg','HE',0.718769),
                         ('Arg','HH11',0.968618),
                         ('Arg','HH12',0.973446),
                         ('Arg','HH21',0.971032),
                         ('Arg','HH22',0.971636),
                         ('Arg','C',0.496077),
                         ('Arg','CA',0.236270),
                         ('Arg','CB',0.317743),
                         ('Arg','CG',0.581473),
                         ('Arg','CD',0.568196),
                         ('Arg','CZ',0.982800),
                         ('Arg','N',0.208509),
                         ('Arg','NE',0.865419),
                         ('Arg','NH1',0.993060),
                         ('Arg','NH2',0.993060),
                         ('Asp','H',0.036198),
                         ('Asp','HA',0.133594),
                         ('Asp','HB2',0.220312),
                         ('Asp','HB3',0.255729),
                         ('Asp','C',0.428646),
                         ('Asp','CA',0.195573),
                         ('Asp','CB',0.253906),
                         ('Asp','CG',0.978906),
                         ('Asp','N',0.146615),
                         ('Asn','H',0.049966),
                         ('Asn','HA',0.153253),
                         ('Asn','HB2',0.232059),
                         ('Asn','HB3',0.260899),
                         ('Asn','HD21',0.462441),
                         ('Asn','HD22',0.466465),
                         ('Asn','C',0.461435),
                         ('Asn','CA',0.233736),
                         ('Asn','CB',0.291751),
                         ('Asn','CG',0.911804),
                         ('Asn','N',0.192153),
                         ('Asn','ND2',0.616030),
                         ('Cys','H',0.061519),
                         ('Cys','HA',0.084118),
                         ('Cys','HB2',0.123038),
                         ('Cys','HB3',0.140615),
                         ('Cys','HG',0.998117),
                         ('Cys','C',0.690521),
                         ('Cys','CA',0.495920),
                         ('Cys','CB',0.549906),
                         ('Cys','N',0.438795),
                         ('Glu','H',0.030563),
                         ('Glu','HA',0.131673),
                         ('Glu','HB2',0.230061),
                         ('Glu','HB3',0.284069),
                         ('Glu','HG2',0.311911),
                         ('Glu','HG3',0.364455),
                         ('Glu','C',0.413230),
                         ('Glu','CA',0.179611),
                         ('Glu','CB',0.241365),
                         ('Glu','CG',0.497593),
                         ('Glu','CD',0.982834),
                         ('Glu','N',0.139837),
                         ('Gln','H',0.037790),
                         ('Gln','HA',0.145811),
                         ('Gln','HB2',0.253476),
                         ('Gln','HB3',0.301604),
                         ('Gln','HG2',0.313369),
                         ('Gln','HG3',0.378610),
                         ('Gln','HE21',0.512656),
                         ('Gln','HE22',0.512656),
                         ('Gln','C',0.433155),
                         ('Gln','CA',0.192157),
                         ('Gln','CB',0.260606),
                         ('Gln','CG',0.516221),
                         ('Gln','CD',0.926916),
                         ('Gln','N',0.153298),
                         ('Gln','NE2',0.612478),
                         ('Gly','H',0.044840),
                         ('Gly','HA2',0.150491),
                         ('Gly','HA3',0.191237),
                         ('Gly','C',0.473382),
                         ('Gly','CA',0.235463),
                         ('Gly','N',0.190418),
                         ('His','H',0.100704),
                         ('His','HA',0.186620),
                         ('His','HB2',0.261972),
                         ('His','HB3',0.291549),
                         ('His','HD1',0.943662),
                         ('His','HD2',0.454930),
                         ('His','HE1',0.517606),
                         ('His','HE2',0.981690),
                         ('His','C',0.514085),
                         ('His','CA',0.279577),
                         ('His','CB',0.331690),
                         ('His','CG',0.992253),
                         ('His','CD2',0.787324),
                         ('His','CE1',0.840141),
                         ('His','N',0.235211),
                         ('His','ND1',0.947183),
                         ('His','NE2',0.952817),
                         ('Ile','H',0.032858),
                         ('Ile','HA',0.132306),
                         ('Ile','HB',0.218377),
                         ('Ile','HG12',0.329165),
                         ('Ile','HG13',0.364059),
                         ('Ile','HG2',0.281477),
                         ('Ile','HD1',0.294272),
                         ('Ile','C',0.422507),
                         ('Ile','CA',0.188136),
                         ('Ile','CB',0.252690),
                         ('Ile','CG1',0.515848),
                         ('Ile','CG2',0.469613),
                         ('Ile','CD1',0.482408),
                         ('Ile','N',0.150044),
                         ('Leu','H',0.033163),
                         ('Leu','HA',0.154877),
                         ('Leu','HB2',0.261069),
                         ('Leu','HB3',0.302699),
                         ('Leu','HG',0.357559),
                         ('Leu','HD1',0.295114),
                         ('Leu','HD2',0.323337),
                         ('Leu','C',0.431646),
                         ('Leu','CA',0.191568),
                         ('Leu','CB',0.255424),
                         ('Leu','CG',0.543658),
                         ('Leu','CD1',0.494267),
                         ('Leu','CD2',0.521609),
                         ('Leu','N',0.146587),
                         ('Lys','H',0.036807),
                         ('Lys','HA',0.134827),
                         ('Lys','HB2',0.230646),
                         ('Lys','HB3',0.286457),
                         ('Lys','HG2',0.340068),
                         ('Lys','HG3',0.400480),
                         ('Lys','HD2',0.433887),
                         ('Lys','HD3',0.490898),
                         ('Lys','HE2',0.447289),
                         ('Lys','HE3',0.516303),
                         ('Lys','HZ',0.962393),
                         ('Lys','C',0.452691),
                         ('Lys','CA',0.229246),
                         ('Lys','CB',0.286857),
                         ('Lys','CG',0.555511),
                         ('Lys','CD',0.588718),
                         ('Lys','CE',0.611722),
                         ('Lys','N',0.179236),
                         ('Lys','NZ',0.998200),
                         ('Met','H',0.094951),
                         ('Met','HA',0.147702),
                         ('Met','HB2',0.271289),
                         ('Met','HB3',0.324039),
                         ('Met','HG2',0.368500),
                         ('Met','HG3',0.403919),
                         ('Met','HE',0.595328),
                         ('Met','C',0.449133),
                         ('Met','CA',0.205727),
                         ('Met','CB',0.269028),
                         ('Met','CG',0.567445),
                         ('Met','CE',0.691786),
                         ('Met','N',0.196684),
                         ('Phe','H',0.058201),
                         ('Phe','HA',0.160765),
                         ('Phe','HB2',0.245828),
                         ('Phe','HB3',0.268620),
                         ('Phe','HD1',0.365893),
                         ('Phe','HD2',0.494506),
                         ('Phe','HE1',0.435083),
                         ('Phe','HE2',0.541718),
                         ('Phe','HZ',0.582418),
                         ('Phe','C',0.445665),
                         ('Phe','CA',0.217338),
                         ('Phe','CB',0.279609),
                         ('Phe','CG',0.994302),
                         ('Phe','CD1',0.746439),
                         ('Phe','CD2',0.828246),
                         ('Phe','CE1',0.782662),
                         ('Phe','CE2',0.853480),
                         ('Phe','CZ',0.835165),
                         ('Phe','N',0.169312),
                         ('Pro','HA',0.180505),
                         ('Pro','HB2',0.257040),
                         ('Pro','HB3',0.275812),
                         ('Pro','HG2',0.361372),
                         ('Pro','HG3',0.404693),
                         ('Pro','HD2',0.331408),
                         ('Pro','HD3',0.362816),
                         ('Pro','C',0.483755),
                         ('Pro','CA',0.228159),
                         ('Pro','CB',0.292058),
                         ('Pro','CG',0.575090),
                         ('Pro','CD',0.560289),
                         ('Pro','N',0.979783),
                         ('Ser','H',0.058564),
                         ('Ser','HA',0.147023),
                         ('Ser','HB2',0.248714),
                         ('Ser','HB3',0.313159),
                         ('Ser','HG',0.988238),
                         ('Ser','C',0.464592),
                         ('Ser','CA',0.217349),
                         ('Ser','CB',0.300172),
                         ('Ser','N',0.185739),
                         ('Thr','H',0.039162),
                         ('Thr','HA',0.153658),
                         ('Thr','HB',0.253196),
                         ('Thr','HG1',0.975524),
                         ('Thr','HG2',0.278216),
                         ('Thr','C',0.462333),
                         ('Thr','CA',0.224368),
                         ('Thr','CB',0.292086),
                         ('Thr','CG2',0.519445),
                         ('Thr','N',0.158009),
                         ('Trp','H',0.110353),
                         ('Trp','HA',0.196815),
                         ('Trp','HB2',0.266212),
                         ('Trp','HB3',0.299204),
                         ('Trp','HD1',0.357224),
                         ('Trp','HE1',0.356086),
                         ('Trp','HE3',0.411832),
                         ('Trp','HZ2',0.379977),
                         ('Trp','HZ3',0.431172),
                         ('Trp','HH2',0.420933),
                         ('Trp','C',0.518771),
                         ('Trp','CA',0.324232),
                         ('Trp','CB',0.369738),
                         ('Trp','CG',0.987486),
                         ('Trp','CD1',0.715586),
                         ('Trp','CD2',0.990899),
                         ('Trp','CE2',0.980660),
                         ('Trp','CE3',0.786121),
                         ('Trp','CZ2',0.754266),
                         ('Trp','CZ3',0.781570),
                         ('Trp','CH2',0.773606),
                         ('Trp','N',0.271900),
                         ('Trp','NE1',0.547213),
                         ('Tyr','H',0.062088),
                         ('Tyr','HA',0.161336),
                         ('Tyr','HB2',0.248824),
                         ('Tyr','HB3',0.265757),
                         ('Tyr','HD1',0.331609),
                         ('Tyr','HD2',0.447789),
                         ('Tyr','HE1',0.355597),
                         ('Tyr','HE2',0.468956),
                         ('Tyr','HH',0.984478),
                         ('Tyr','C',0.487770),
                         ('Tyr','CA',0.264346),
                         ('Tyr','CB',0.337723),
                         ('Tyr','CG',0.988241),
                         ('Tyr','CD1',0.745532),
                         ('Tyr','CD2',0.835842),
                         ('Tyr','CE1',0.740828),
                         ('Tyr','CE2',0.833960),
                         ('Tyr','CZ',0.992004),
                         ('Tyr','N',0.224365),
                         ('Val','H',0.039465),
                         ('Val','HA',0.143780),
                         ('Val','HB',0.228479),
                         ('Val','HG1',0.252943),
                         ('Val','HG2',0.275790),
                         ('Val','C',0.437803),
                         ('Val','CA',0.199169),
                         ('Val','CB',0.260559),
                         ('Val','CG1',0.477960),
                         ('Val','CG2',0.509808),
                         ('Val','N',0.144242)]


PROTEIN_ATOM_NAMES = {
  'ALA': ['H', 'N', 'C', 'CA', 'HA', 'CB', 'HB%'],
  'ARG': ['H', 'N', 'C', 'CA', 'HA', 'CB', 'HBx', 'HBy', 'HB2', 'HB3', 'CG', 'HGx', 'HGy',
          'HG2', 'HG3', 'CD', 'HDx', 'HDy', 'HD2', 'HD3', 'NE', 'HE', 'CZ', 'NHx', 'NHy',
          'NH1', 'NH2', 'HH1x', 'HH1y', 'HH11', 'HH12', 'HH2x', 'HH2y', 'HH21', 'HH22'],
  'ASN': ['H', 'N', 'C', 'CA', 'HA', 'CB', 'HBx', 'HBy', 'HB2', 'HB3', 'CG', 'ND2',
          'HD2x', 'HD2y', 'HD21', 'HD22'],
  'ASP': ['H', 'N', 'C', 'CA', 'HA', 'CB', 'HBx', 'HBy', 'HB2', 'HB3', 'CG'],
  'CyS': ['H', 'N', 'C', 'CA', 'HA', 'CB', 'HBx', 'HBy', 'HB2', 'HB3', 'HG'],
  'GLN': ['H', 'N', 'C', 'CA', 'HA', 'CB', 'HBx', 'HBy', 'HB2', 'HB3', 'CG', 'HGx', 'HGy',
          'HG2', 'HG3', 'CD', 'NE2', 'HE2x', 'HE2y', 'HE21', 'HE22'],
  'GLU': ['H', 'N', 'C', 'CA', 'HA', 'CB', 'HBx', 'HBy', 'HB2', 'HB3', 'CG', 'HGx', 'HGy',
          'HG2', 'HG3', 'CD'],
  'GLy': ['H', 'N', 'C', 'CA', 'HAx', 'HAy', 'HA2', 'HA3'],
  'HIS': ['H', 'N', 'C', 'CA', 'HA', 'CB', 'HBx', 'HBy', 'HB2', 'HB3', 'CG', 'ND1', 'HD1',
          'CD2', 'HD2', 'CE1', 'HE1', 'NE2', 'HE2'],
  'ILE': ['H', 'N', 'C', 'CA', 'HA', 'CB', 'HB', 'CG1', 'HG1x', 'HG1y',
          'HG12', 'HG13', 'CG2', 'HG2%', 'CD1', 'HD1%'],
  'LEU': ['H', 'N', 'C', 'CA', 'HA', 'CB', 'HBx', 'HBy', 'HB2', 'HB3', 'CG', 'HG', 'CDx',
          'CDy', 'CD1', 'CD2', 'HDx%', 'HDy%', 'HD1%', 'HD2%'],
  'LyS': ['H', 'N', 'C', 'CA', 'HA', 'CB', 'HBx', 'HBy', 'HB2', 'HB3', 'CG', 'HGx', 'HGy',
          'HG2', 'HG3', 'CD', 'HDx', 'HDy', 'HD2', 'HD3', 'CE', 'HEx', 'HEy', 'HE2', 'HE3',
          'NZ', 'HZ%'],
  'MET': ['H', 'N', 'C', 'CA', 'HA', 'CB', 'HBx', 'HBy', 'HB2', 'HB3', 'CG', 'HGx', 'HGy',
          'HG2', 'HG3', 'CE', 'HE%'],
  'PHE': ['H', 'N', 'C', 'CA', 'HA', 'CB', 'HBx', 'HBy', 'HB2', 'HB3', 'CG', 'CDx', 'CDy',
          'CD1', 'CD2', 'HDx', 'HDy', 'HD1', 'HD2', 'CEx', 'CEy', 'CE1', 'CE2', 'HEx', 'HEy',
          'HE1', 'HE2', 'CZ', 'HZ'],
  'PRO': ['H', 'N', 'C', 'CA', 'HA', 'CB', 'HBx', 'HBy', 'HB2', 'HB3', 'CG', 'HGx', 'HGy',
          'HG2', 'HG3', 'CD', 'HDx', 'HDy', 'HD2', 'HD3'],
  'SER': ['H', 'N', 'C', 'CA', 'HA', 'CB', 'HBx', 'HBy', 'HB2', 'HB3', 'HG'],
  'THR': ['H', 'N', 'C', 'CA', 'HA', 'CB', 'HB', 'CG2', 'HG1', 'HG2%'],
  'TRP': ['H', 'N', 'C', 'CA', 'HA', 'CB', 'HBx', 'HBy', 'HB2', 'HB3', 'CG', 'CD1', 'CD2', 'HD1',
          'NE1', 'HE1', 'CE2', 'CE3', 'HE3', 'CZ2', 'CZ3', 'HZ2', 'HZ3', 'CH2', 'HH2'],
  'TyR': ['H', 'N', 'C', 'CA', 'HA', 'CB', 'HBx', 'HBy', 'HB2', 'HB3', 'CG', 'CDx', 'CDy', 'CD1',
          'CD2', 'HDx', 'HDy', 'HD2', 'HD3', 'CEx', 'CEy', 'CE1', 'CE2', 'HEx', 'HEy', 'HE2', 'HE3',
          'CZ', 'HH'],
  'VAL': ['H', 'N', 'C', 'CA', 'HA', 'CB', 'HB', 'CGx', 'CGy', 'CG1', 'CG2',
          'HGx%', 'HGy%', 'HG1%', 'HG2%']
}


ALL_ATOMS_SORTED = {'alphas': ['CA', 'HA', 'HAx', 'HAy', 'HA2', 'HA3'],
                    'betas':  ['CB', 'HB', 'HBx', 'HBy', 'HB%', 'HB2', 'HB3'],
                    'gammas': ['CG', 'CGx', 'CGy', 'CG1', 'CG2', 'HG', 'HGx', 'HGy', 'HG2', 'HG3',
                               'HGx%', 'HGy%'],
                    'moreGammas': ['HG1', 'HG1x', 'HG1y', 'HG12', 'HG13', 'HG1%', 'HG2%'],
                    'deltas': ['CD', 'CDx', 'CDy', 'CD1', 'CD2', 'HDx', 'HDx', 'HD1', 'HD2', 'HD3',
                               'HDx%', 'HDy%'],
                    'moreDeltas': ['ND1', 'ND2', 'HD1%', 'HD2%', 'HD2x', 'HD2y', 'HD21', 'HD22'],
                    'epsilons': ['CE', 'CEx', 'CEy', 'CE1', 'CE2', 'HE', 'HEx', 'HEy', 'HE1', 'HE2',
                                 'HE2x', 'HE2y'],
                    'moreEpsilons': ['CE3', 'NE', 'NE1', 'NE2', 'HE1', 'HE2', 'HE3', 'HE21', 'HE22',
                                     'HE%'],
                    'zetas': ['CZ', 'CZ2', 'CZ3', 'HZ', 'HZ2', 'HZ3', 'HZ%', 'NZ'],
                    'etas': ['CH2', 'HH2', 'HH1x', 'HH1y', 'HH2x', 'HH2y', 'NH1', 'NH2',
                             'NHx', 'NHy', 'HH21', 'HH22'],
                    'moreEtas': ['HH', 'HH11', 'HH12']
                    }


# End moved-in data - functions from original ChemicalShift



def _getResidueProbability(ppms, ccpCode, elements, shiftNames=None, ppmsBound=None,
                          prior=0.05, molType=PROTEIN_MOLTYPE, cutoff=1e-10):
  """Probability that data match a given ccpCode and molType
  NBNB unassigned (unnamed) resonances make no differences, but named resonances
  that do not fit a residue type WILL GIVE PROBABILITY ZERO!"""

  # Use refExperiment info
  # Use bound resonances info

  shiftRefs = REFDB_SD_MEAN.get((molType, ccpCode))
    
  if not shiftRefs:
    return None
  
  if not shiftNames:
    shiftNames = [None] * len(ppms)
  
  if not ppmsBound:
    ppmsBound = [None] * len(ppms)
    
  
  atomData = [(x, shiftRefs[x]) for x in shiftRefs.keys()]

  data = []
  dataAppend = data.append
  for i, ppm in enumerate(ppms):
    element = elements[i]
    shiftName = shiftNames[i]
    ppmB = ppmsBound[i]
    n = 0

    for j, (atomName, stats) in enumerate(atomData):
      if not atomName.startswith(element):
        continue 
      
      if shiftName and not _isAssignmentCompatible(shiftName, atomName):
        continue
      
      mean, sd, pMissing, bound = stats
      d = ppm-mean
      
      if (not shiftName) and (abs(d) > 5*sd):
        continue
      
      e = d/sd   
      p = exp(-0.5*e*e)/(sd*ROOT_TWO_PI)

      if bound and (ppmB is not None):
        boundData = shiftRefs.get(bound)

        if boundData:
          meanB, sdB, pMissingB, boundB = boundData
          dB = ppmB-meanB
          eB = dB/sdB
          pB = exp(-0.5*eB*eB)/(sdB*ROOT_TWO_PI)
      
          p = (p*pB) ** 0.5
      
      if (not shiftName) and (p < cutoff):
        continue
      
      
      dataAppend((i,j,p))
      n += 1

    if n == 0:
      return 0.0
  
  groups = [set([node,]) for node in data if node[0] == 0]
  
  while data:
    node = data.pop()
    i, j, p = node
    
    for group in groups[:]:
      for node2 in group:
        i2, j2, p2 = node2
       
        if (i == i2) or (j == j2):
          break
      
      else:
        newGroup = group.copy()
        newGroup.add(node)
        groups.append(newGroup)
 
  probTot = 0.0
  for group in groups:

    if len(group) != len(ppms):
      continue
    
    found = set([])
    prob = 1.0
    for i,j, p in group:
      found.add(j)  
      prob *= p
    
    #for k, datum in enumerate(atomData:
    #  atomName, stats = datum
    #  pMissing = stats[2]
    #  
    #  if k in found:
    #    prob *= 1-pMissing
    #  else:
    #    prob *= pMissing
    
    if found:
      probTot += prob
      
  return probTot


def getSpinSystemChainProbabilities(spinSystem, chain, shiftList):

  probDict = {}
  getProb = getSpinSystemResidueProbability
  priors = getChainResTypesPriors(chain)

  ccpCodes = set(getChainResidueCodes(chain))

  for ccpCode, molType in ccpCodes:
    probDict[ccpCode] = getProb(spinSystem, shiftList, ccpCode,
                                priors[ccpCode], molType)


  return probDict


def getChainResidueCodes(chain):

  ccpCodes = []
  for residue in chain.residues:
    ccpCode = residue.ccpCode
    if (ccpCode == 'Cys') and (residue.descriptor == 'link:SG'):
      ccpCode = 'Cyss'

    ccpCodes.append((ccpCode, residue.molType))

  return ccpCodes


def getSpinSystemScore(spinSystem, shifts, chain, shiftList):

    scores = getSpinSystemChainProbabilities(spinSystem, chain, shiftList)

    # ejb - error here, this was empty in nef file: 1nk2_docr_extended.ccpn.nef
    if scores:
      total = sum(scores.values())

      if total:
        for ccpCode in scores:
          scores[ccpCode] *= 100.0/total

      else:
        return scores

    return scores


def getChainResTypesPriors(chain):

  priors = {}

  ccpCodes = [x[0] for x in getChainResidueCodes(chain)]
  n = float(len(ccpCodes))

  for ccpCode in set(ccpCodes):
    priors[ccpCode] = ccpCodes.count(ccpCode)/n

  return priors


def getCcpCodes(chain):
  codeDict = {}
  for residue in chain.residues:
    codeDict[residue.ccpCode] = True

  ccpCodes = list(codeDict.keys())
  ccpCodes.sort()

  return ccpCodes


def getSpinSystemResidueProbability(spinSystem, shiftList, ccpCode,
                                    prior=0.05, molType=PROTEIN_MOLTYPE):
  """Get probability that Spin system matches molType and ccpCode
  NB to avoid rejection all atom names must be either unassigned (default) or correct!"""

  ppms = []
  elements = []
  atomNames = []
  ppmsAppend = ppms.append
  elementsAppend = elements.append
  atomNamesAppend = atomNames.append

  for resonance in spinSystem.resonances:

    isotope = resonance.isotope
    if isotope:

      shift = resonance.findFirstShift(parentList=shiftList)
      if shift:
        ppmsAppend(shift.value)
        elementsAppend(isotope.chemElement.symbol)
        # NB, use implName to avoid default (unassigned) names.
        atomNamesAppend(resonance.implName)

  prob = _getResidueProbability(ppms, ccpCode, elements,
                               atomNames, prior=prior, molType=molType)

  return prob

def _isAssignmentCompatible(assignName:str, atomName:str) -> bool:
  """Is assignName compatible with assignment to atomName?
  NB allows for non-standard assignment strings
  NB does NOT do case conversions (nor should it - names are case-sensitive).
  NB does NOT accept 'x' and 'y' as wildcards, only 'x' and 'y'"""

  # convert pseudoAtom names to proton wildcard names
  if assignName[0] in 'QM':
    assignName = 'H' + assignName[1:] + '%'

  if assignName == atomName:
    return True

  lenPrefix = len(os.path.commonprefix((assignName, atomName)))
  lenAtomName = len(atomName)

  if lenAtomName == lenPrefix:
    if assignName[lenPrefix:] in ('*', '%'):
      # E.g. assign HG* v. HG
      return True

  elif lenAtomName - lenPrefix == 1:
    if atomName[-1] in '123%*':
      if assignName[lenPrefix:] in ('', 'x', 'y', '*', '%'):
        # assigned wildcard v. wildcard or single digit, e.g. HGx v. HG* or HG1
        return True

  elif lenAtomName - lenPrefix == 2:
    if atomName[-2] in '123' and atomName[-1] in '123*%':
      if assignName[lenPrefix:] in ('', 'x', 'y', '*', '%', 'x%', 'y%', 'x*', 'y*'):
        # E.g. HG, HG%, or HGy* v. HG21 or HG1*
        return True

  #
  return False


def getAtomProbability(ccpCode, atomName, shiftValue, molType=PROTEIN_MOLTYPE):

  shiftRefs = REFDB_SD_MEAN.get((molType, ccpCode))

  if not shiftRefs:
    return

  stats = shiftRefs.get(atomName)
  if not stats:
    return

  mean, sd, pMissing, bound = stats
  d = shiftValue-mean
  e = d/sd
  p = exp(-0.5*e*e)/(sd*ROOT_TWO_PI)

  return p


def getResidueAtoms(ccpCode, molType=PROTEIN_MOLTYPE):
    return REFDB_SD_MEAN.get((molType, ccpCode)).keys()


def getCcpCodeData(nmrProject, ccpCode, molType=None, atomType=None):

  dataDict = {}
  sourceName = 'RefDB'

  nmrRefStore = nmrProject.root.findFirstNmrReferenceStore(molType=molType, ccpCode=ccpCode)
  chemCompNmrRef = nmrRefStore.findFirstChemCompNmrRef(sourceName=sourceName)
  if chemCompNmrRef:

    chemCompVarNmrRef = chemCompNmrRef.findFirstChemCompVarNmrRef(linking='any', descriptor='any')
    if chemCompVarNmrRef:
      for chemAtomNmrRef in chemCompVarNmrRef.chemAtomNmrRefs:
        atomName = chemAtomNmrRef.name
        element  = chemAtomNmrRef.findFirstChemAtom().elementSymbol

        if not atomType:
          dataDict[atomName] = chemAtomNmrRef

        elif (atomType == 'Hydrogen' and element == 'H') or \
             (atomType == 'Heavy' and element != 'H'):
          dataDict[atomName] = chemAtomNmrRef

  return dataDict



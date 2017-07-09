"""Module Documentation here

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
__dateModified__ = "$dateModified: 2017-07-07 16:33:20 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b2 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================
"""
======================COPYRIGHT/LICENSE START==========================

formats.py: license header generation code for CCPN framework

Copyright (C) 2004  (CCPN Project)

=======================================================================

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public
License as published by the Free Software Foundation; either
version 2 of the License, or (at your option) any later version.
 
A copy of this license can be found in ../../../../license/GPL.license
 
This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.
 
You should have received a copy of the GNU General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

======================COPYRIGHT/LICENSE START==========================

licenses.py: license header generation code for CCPN framework

Copyright (C) 2004  (CCPN Project)

=======================================================================

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public
License as published by the Free Software Foundation; either
version 2 of the License, or (at your option) any later version.
 
A copy of this license can be found in ../../../../license/GPL.license
 
This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.
 
You should have received a copy of the GNU General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

======================COPYRIGHT/LICENSE END============================

for further information, please contact :

- CCPN website (http://www.ccpn.ac.uk/)

- email: ccpn@bioc.cam.ac.uk

=======================================================================

If you are using this software for academic purposes, we suggest
quoting the following references:

===========================REFERENCE START=============================
R. Fogh, J. Ionides, E. Ulrich, W. Boucher, W. Vranken, J.P. Linge, M.
Habeck, W. Rieping, T.N. Bhat, J. Westbrook, K. Henrick, G. Gilliland,
H. Berman, J. Thornton, M. Nilges, J. Markley and E. Laue (2002). The
CCPN project: An interim report on a data model for the NMR community
(Progress report). Nature Struct. Biol. 9, 416-418.

===========================REFERENCE END===============================


======================COPYRIGHT/LICENSE END============================

for further information, please contact :

- CCPN website (http://www.ccpn.ac.uk/)

- email: ccpn@bioc.cam.ac.uk

=======================================================================

If you are using this software for academic purposes, we suggest
quoting the following references:

===========================REFERENCE START=============================
R. Fogh, J. Ionides, E. Ulrich, W. Boucher, W. Vranken, J.P. Linge, M.
Habeck, W. Rieping, T.N. Bhat, J. Westbrook, K. Henrick, G. Gilliland,
H. Berman, J. Thornton, M. Nilges, J. Markley and E. Laue (2002). The
CCPN project: An interim report on a data model for the NMR community
(Progress report). Nature Struct. Biol. 9, 416-418.

===========================REFERENCE END===============================

"""
import re


# Information for generating license headers for autogenerated files.

# The information is used by ccpnmodel.ccpncore.memops.license.headers.py
# It is ordered by packageGroup.
#
# NB 'useLicense', 'stdContact' and 'references' refer to information in
# this file
# Only 'useLicense' is mandatory, the others are optional and may be set to None.
# Neither can be chosebn freely.
# 'extraContact' and 'credits' are strings that are entered 'as is'. They
# are entered in addition to the (optional) 'stdContact' and 'references'.


licenseInfo = {

 'pp' : {
  'author':'Anne Pajon',
  'organization':'MSD group, EBI',
  'useLicense':'LGPL',
  'stdContact':'msd',
  'extraContact': None,
  'references':('MSD2004',),
  'credits':None
 },
 
 'nmr' : {
  'author':'Rasmus Fogh',
  'organization':'CCPN Project',
  'useLicense':'LGPL',
  'stdContact':'ccpn',
  'extraContact':None,
  'references':('CCPNMR2004','MEMOPS2004'),
  'credits':None
 },
 
 'core' : {
  'author':'',
  'organization':'CCPN Project',
  'useLicense':'LGPL',
  'stdContact':'ccpn',
  'extraContact':None,
  'references':('MEMOPS2004',),
  'credits':None
 }


}





# information for different file type formats

formats = {
 'python' : {
  'commentStart': '\"\"\"',
  'commentEnd': '\"\"\"',
  'includeFileMatches': [r'.*\.py$'],
  'ignoreStartLines': ['^#!/']
 },
          
 'xml' : {
  'commentStart': '<!--',
  'commentEnd': '-->',
  'includeFileMatches': [r'.*\.xml$'],
  'ignoreStartLines': ['^\<\?xml']
 },      
 'html' : {
  'commentStart': '<!--',
  'commentEnd': '-->',
  'includeFileMatches': [r'.*\.html$', r'.*\.htm$'],
  'ignoreStartLines': ['^\<\!DOCTYPE', '^\<html']
 },
 
 'css' : {
  'commentStart': '/*',
  'commentEnd': '*/',
  'includeFileMatches': [r'.*\.css'],
  'ignoreStartLines': []
 },

 'c' : {
  'commentStart': '/*',
  'commentEnd': '*/',
  'includeFileMatches': [r'.*\.c$', r'.*\.h$'],
  'ignoreStartLines': []
 },
 
 'java' : {
  'commentStart': '/*',
  'commentEnd': '*/',
  'includeFileMatches': [r'.*\.java$'],
  'ignoreStartLines': []
 },
 
 'text' : {
  'commentStart': '<!--',
  'commentEnd': '-->',
  'includeFileMatches': [],
  'ignoreStartLines': []
 }
}

# preprocess match expressions

emptyLineExpr = re.compile("^\s*$")

for dd in formats.values():

  ll = dd['includeFileMatches']
  for ii in range(len(ll)):
    ll[ii] = re.compile(ll[ii])

  ll = dd['ignoreStartLines']
  for ii in range(len(ll)):
    ll[ii] = re.compile(ll[ii])
    
  dd['ignoreStartLines'].append(emptyLineExpr)



stdContacts = {

'ccpn' : """
for further information, please contact :

- CCPN website (http://www.ccpn.ac.uk/)

- email: ccpn@bioc.cam.ac.uk
""",

'msd' : """
for further information, please contact :

- PIMS website (http://www.pims-lims.org)

- email: Anne Pajon, pajon@ebi.ac.uk
""",

'ccpn-msd' : """
for further information, please contact :

- CCPN website (http://www.ccpn.ac.uk/)
- MSD website (http://www.ebi.ac.uk/msd/)
"""
}

stdContacts['nmr'] = stdContacts['ccpn']


gnuLicense = """
This library is free software; you can redistribute it and/or
modify it under the terms of the GNU %sGeneral Public
License as published by the Free Software Foundation; either
version 2%s of the License, or (at your option) any later version.

A copy of this license can be found in %%(licenseLocation)s/%s.license

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
%sGeneral Public License for more details.

You should have received a copy of the GNU %sGeneral Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

"""


licenses = {

'GPL'  : gnuLicense % ('','','GPL','',''),

'LGPL' : gnuLicense % ('Lesser ','.1','LGPL','Lesser ','Lesser '),

 'restricted' : """
This file contains reserved and/or proprietary information
belonging to the author and/or organisation holding the copyright.
It may not be used, distributed, modified, transmitted, stored,
or in any way accessed, except by members or employees of %(organization)s
and in accordance with the guidelines of %(organization)s.
""",

 'ccpn' :"""
This file contains reserved and/or proprietary information
belonging to the author and/or organisation holding the copyright.
It may not be used, distributed, modified, transmitted, stored,
or in any way accessed, except by members or employees of the CCPN,
and by these people onlyin accordance with the guidelines of the CCPN.
 
A copy of this license can be found in %(licenseLocation)s/CCPN.license.
""",

 'brief' : 
 """The license for this file is in %(licenseLocation)s/%(licenseFileName)s.license"""
}




references = {

'MIDGE1991' :
"""M. Madrid, E. Llinas and M. Llinas (1991).
Model-Independent Refinement of Interproton Distances Generated from
H-1-NMR Overhauser Intensities. 
Journal Of Magnetic Resonance 93: 329-346.""",

'CLOUDS2002' :
"""A. Grishaev and M. Llinas (2002).
CLOUDS, a protocol for deriving a molecular proton density via NMR.
Proc Natl Acad Sci USA. 99, 6707-6712.""",

'CCPN2002' : 
"""R. Fogh, J. Ionides, E. Ulrich, W. Boucher, W. Vranken, J.P. Linge, M.
Habeck, W. Rieping, T.N. Bhat, J. Westbrook, K. Henrick, G. Gilliland,
H. Berman, J. Thornton, M. Nilges, J. Markley and E. Laue (2002). The
CCPN project: An interim report on a data model for the NMR community
(Progress report). Nature Struct. Biol. 9, 416-418.""",

'MSD2004' :
"""A. Pajon, J. Ionides, J. Diprose, J. Fillon, R. Fogh, A.W. Ashton,
H. Berman, W. Boucher, M. Cygler, E. Deleury, R. Esnouf, J. Janin, R. Kim,
I. Krimm, C.L. Lawson, E. Oeuillet, A. Poupon, S. Raymond, T. Stevens,
H. van Tilbeurgh, J. Westbrook, P. Wood, E. Ulrich, W. Vranken, L. Xueli,
E. Laue, D.I. Stuart, and K. Henrick (2005). Design of a Data Model for
Developing Laboratory Information Management and Analysis Systems for
Protein Production. Proteins: Structure, Function and Bioinformatics 58,
278-284.""",

'CCPNMR2004' :  """Wim F. Vranken, Wayne Boucher, Tim J. Stevens, Rasmus
H. Fogh, Anne Pajon, Miguel Llinas, Eldon L. Ulrich, John L. Markley, John
Ionides and Ernest D. Laue (2005). The CCPN Data Model for NMR Spectroscopy:
Development of a Software Pipeline. Proteins 59, 687 - 696.""",

'MEMOPS2004' :  """Rasmus H. Fogh, Wayne Boucher, Wim F. Vranken, Anne
Pajon, Tim J. Stevens, T.N. Bhat, John Westbrook, John M.C. Ionides and
Ernest D. Laue (2005). A framework for scientific data modeling and automated
software development. Bioinformatics 21, 1678-1684."""

}



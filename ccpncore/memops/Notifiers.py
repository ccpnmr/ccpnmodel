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
__dateModified__ = "$dateModified: 2017-07-07 16:33:16 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b5 $"

#=========================================================================================
# Created
#=========================================================================================
__author__ = "$Author: rhf22 $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================
""" Implementation module. Contains Api implementation code.


======================COPYRIGHT/LICENSE START==========================

Implementation.py: Basic implementation class for CCPN Python data model API

Copyright (C) 2005 Rasmus Fogh (CCPN Project)

=======================================================================

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.

A copy of this license can be found in ../../../license/LGPL.license

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
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

Rasmus H. Fogh, Wayne Boucher, Wim F. Vranken, Anne
Pajon, Tim J. Stevens, T.N. Bhat, John Westbrook, John M.C. Ionides and
Ernest D. Laue (2005). A framework for scientific data modeling and automated
software development. Bioinformatics 21, 1678-1684.

===========================REFERENCE END===============================
"""


from ccpnmodel.ccpncore.lib import Util as coreUtil


# Operations that change the data contents will execute registered notifies.
# These operations are delete, __init__, set, remove, and add.
# set, remove, and add functions will also execute notifies registered with
# funcname = ''
# Notifies are disabled during reading.
# set, add, and remove notifies are disabled during delete and __init__

def registerNotify(notify, classname, funcname=''):
  """register notifiers to class clazz (maybe given as API class or as class qualifiedName"""

  metaClasses = coreUtil.getClassFromFullName(classname)._metaclass.getNonAbstractSubtypes()

  for metaClass in metaClasses:
    clazz =  coreUtil.getClassFromFullName(metaClass.qualifiedName())
    notifies = clazz._notifies
    ll = notifies.get(funcname)
    if ll is None:
      notifies[funcname] = [notify]

    elif notify not in ll:
      ll.append(notify)

def unregisterNotify(notify, classname, funcname=''):

  metaClasses = coreUtil.getClassFromFullName(classname)._metaclass.getNonAbstractSubtypes()

  for metaClass in metaClasses:
    clazz =  coreUtil.getClassFromFullName(metaClass.qualifiedName())
    try:
      clazz._notifies[funcname].remove(notify)
    except ValueError:
      pass


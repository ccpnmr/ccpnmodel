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
__dateModified__ = "$dateModified: 2017-07-07 16:33:24 +0100 (Fri, July 07, 2017) $"
__version__ = "$Revision: 3.0.b3 $"
#=========================================================================================
# Created
#=========================================================================================

__author__ = "$Author: CCPN $"
__date__ = "$Date: 2017-04-07 10:28:48 +0000 (Fri, April 07, 2017) $"
#=========================================================================================
# Start of code
#=========================================================================================
""" Language-independent parts for Documentation Generation 
using MOF-style MetaModel.


======================COPYRIGHT/LICENSE START==========================

Documentation.py: Code generation for CCPN framework

Copyright (C) 2007 Rasmus Fogh (CCPN Project)

=======================================================================

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public
License as published by the Free Software Foundation; either
version 2 of the License, or (at your option) any later version.
 
A copy of this license can be found in ../../../license/GPL.license
 
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

Rasmus H. Fogh, Wayne Boucher, Wim F. Vranken, Anne
Pajon, Tim J. Stevens, T.N. Bhat, John Westbrook, John M.C. Ionides and
Ernest D. Laue (2005). A framework for scientific data modeling and automated
software development. Bioinformatics 21, 1678-1684.

===========================REFERENCE END===============================
"""

import time

from ccpn.util import Path
from ccpnmodel.ccpncore.memops import Version
from ccpnmodel.ccpncore.memops.metamodel import MetaModel
from ccpnmodel.ccpncore.memops.metamodel.TextWriter import TextWriter


MemopsError = MetaModel.MemopsError

mandatoryAttributes = ()

class Documentation(TextWriter):

  color1='#F0CC99'
  color2='#794E83'
  styleSheetFile = 'htmldoc.css'

  ###########################################################################

  ###########################################################################

  def __init__(self):

    for tag in mandatoryAttributes:
      if not hasattr(self, tag):
        raise MemopsError("Documentation lacks mandatory %s attribute" % tag)

    super(Documentation, self).__init__()

  ###########################################################################

  ###########################################################################

  # TBD: does this belong in this class?
  def writeHeader(self, scriptName=None, headerComment=None, title=None, styleSheetDir=None):

    styleSheetFile = self.styleSheetFile
    if styleSheetDir:
      styleSheetFile = Path.joinPath(styleSheetDir, styleSheetFile)

    dd = {
      'scriptName'        : scriptName or '?',
      'headerComment'     : headerComment or '?',
      'date'              : time.ctime(),
      'title'             : title or 'CCPN',
      'styleSheetFile'    : styleSheetFile,
    }
  
    headerTemplate = """
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"
"http://www.w3.org/TR/html4/loose.dtd">
<!--Generated by %(scriptName)s on %(date)s-->
<!--%(headerComment)s-->
<HTML>
<head>
  <title>%(title)s</title>
  <link rel=stylesheet type="text/css" href="%(styleSheetFile)s">
  <script language="JavaScript">
    function wopn(href){ window.open(href,'','width=880,height=500,top=300,left=300,resizable=0,toolbar=0,location=0,directories=0,status=0,menubar=0,scrollbars=1')}
  </script>
</head>
<body>
"""

    self.write(headerTemplate % dd)

  ###########################################################################

  ###########################################################################

  # TBD: does this belong in this class?
  def writeFooter(self, dataModelVersion=None, releaseVersion=None, 
        scriptName=None, objName=None):
  
    if releaseVersion:
      releaseName = releaseVersion.name or '?'
      releaseLine = ("""
    &nbsp;%s&nbsp;<em>&nbsp;release,</em>&nbsp;
    <em>version</em>&nbsp;&nbsp;%s""" 
     % (releaseName, releaseVersion)
      )
    else:
      releaseLine = """
      &nbsp;"""
  
    dd = {
      'scriptName'        : scriptName or '?',
      'objName'           : objName or '?',
      'dataModelVersion'  : dataModelVersion or Version.currentModelVersion,
      'releaseLine'       : releaseLine,
      'color'             : self.color2,
      'date'              : time.ctime(),
    }
  
    footerTemplate = """

<table width="100%%" cellpadding=2>
  <tr><td colspan=2 width="100%%" bgcolor=%(color)s></td></tr>
  <tr>
    <td><h5>
    %(releaseLine)s
    <em>Data Model Version</em>&nbsp;%(dataModelVersion)s
    </h5></td>
    <td align=right><a href='#toplink'><span style="font-size:9pt">Go&nbsp;to&nbsp;Top&nbsp;&nbsp;</span></a>
    </td>
  </tr>
</table>

<div class="leftbanner">
<table width=100%% cellspacing=0 cellpadding=2 border=0>
  <tr><td bgcolor=%(color)s style="white-space: nowrap">
    <em>&nbsp;&nbsp;Autogenerated by</em>&nbsp;&nbsp;%(scriptName)s&nbsp;
    <em>on</em>&nbsp;&nbsp;%(date)s&nbsp;
    &nbsp;
    <em>from data model package</em>&nbsp;&nbsp;%(objName)s&nbsp;&nbsp;
  </td></tr>
</table>
</div>
<table width=100%% cellspacing=0 cellpadding=2 border=0>
  <tr valign=top>
    <td><h6>&nbsp;&nbsp;Work done by the <a href="mailto:ccpn-dev@mole.bio.cam.ac.uk">CCPN team</a>.</h6></td>
    <td align=right><h6><a target="blank" href="http://www.ccpn.ac.uk">www.ccpn.ac.uk</a>&nbsp;&nbsp;</h6></td>
  </tr>
</table>
<br>

</body>
</HTML>
"""
  
    self.write(footerTemplate % dd)

  ###########################################################################

  ###########################################################################

  def writeHorizontalLine(self):

    horizontalLine = """
<table borderwidth="1" width="100%%"><tr><td width="100%%" bgcolor=%s></td></tr></table>
""" % self.color2

    self.write(horizontalLine)

  ###########################################################################

  ###########################################################################

  def writeVerticalBar(self):

    self.write('|')

  ###########################################################################

  ###########################################################################

  def writeStartTable(self, **tableAttrs):

    self.write('<table%s>' % self.getAttrString(**tableAttrs))

    self.indent += self.INDENT

  ###########################################################################

  ###########################################################################

  def writeEndTable(self):

    self.indent -= self.INDENT

    self.write('</table>')

  ###########################################################################

  ###########################################################################

  def writeStartRow(self, **rowAttrs):

    self.write('<tr%s>' % self.getAttrString(**rowAttrs))

    self.indent += self.INDENT

  ###########################################################################

  ###########################################################################

  def writeEndRow(self):

    self.indent -= self.INDENT

    self.write('</tr>')

  ###########################################################################

  ###########################################################################

  def writeStartCell(self, **cellAttrs):

    self.write('<td%s>' % self.getAttrString(**cellAttrs))

    self.indent += self.INDENT

  ###########################################################################

  ###########################################################################

  def writeEndCell(self):

    self.indent -= self.INDENT

    self.write('</td>')

  ###########################################################################

  ###########################################################################

  def writeCell(self, cellString='', **cellAttrs):

    self.writeStartCell(**cellAttrs)
    self.write(cellString)
    self.writeEndCell()

  ###########################################################################

  ###########################################################################

  def writeStartStyle(self, **styleAttrs):

    self.write('<span%s>' % self.getAttrString(**styleAttrs))

  ###########################################################################

  ###########################################################################

  def writeEndStyle(self):

    self.write('</span>')

  ###########################################################################

  ###########################################################################

  def writeStyleString(self, styleString='', **styleAttrs):

    self.writeStartStyle(**styleAttrs)
    self.write(styleString)
    self.writeEndStyle()

  ###########################################################################

  ###########################################################################

  def writeEmphasisString(self, emphasisString):

    self.write(self.getEmphasisString(emphasisString))

  ###########################################################################

  ###########################################################################

  def writeStrongString(self, strongString):

    self.write(self.getStrongString(strongString))

  ###########################################################################

  ###########################################################################

  def writeStartSection(self, **sectionAttrs):

    self.writeStartTable(**sectionAttrs)
    self.writeStartRow()
    self.writeStartCell()

  ###########################################################################

  ###########################################################################

  def writeEndSection(self):

    self.writeEndCell()
    self.writeEndRow()
    self.writeEndTable()

  ###########################################################################

  ###########################################################################

  def writeStartDiv(self, **divAttrs):

    self.write('<div%s>' % self.getAttrString(**divAttrs))

    self.indent += self.INDENT

  ###########################################################################

  ###########################################################################

  def writeEndDiv(self):

    self.indent -= self.INDENT

    self.write('</div>')

  ###########################################################################

  ###########################################################################

  def writeStartParagraph(self, **paragraphAttrs):

    self.write('<p%s>' % self.getAttrString(**paragraphAttrs))

    self.indent += self.INDENT

  ###########################################################################

  ###########################################################################

  def writeEndParagraph(self):

    self.indent -= self.INDENT

    self.write('</p>')

  ###########################################################################

  ###########################################################################

  def writeStartCenter(self, **centerAttrs):

    self.write('<center%s>' % self.getAttrString(**centerAttrs))

    self.indent += self.INDENT

  ###########################################################################

  ###########################################################################

  def writeEndCenter(self):

    self.indent -= self.INDENT

    self.write('</center>')

  ###########################################################################

  ###########################################################################

  def writeStartIndent(self):

    self.write('<ul>')

  ###########################################################################

  ###########################################################################

  def writeEndIndent(self):

    self.write('</ul>')

  ###########################################################################

  ###########################################################################

  def writeLink(self, link, message, **attrs):

    self.write(self.getLinkString(link, message, **attrs))

  ###########################################################################

  ###########################################################################

  def writeAnchorLink(self, link, message = '', **attrs):

    self.write(self.getAnchorLinkString(link, message, **attrs))

  ###########################################################################

  ###########################################################################

  def writeHeading(self, heading, level):

    self.write(self.getHeadingString(heading, level))

  ###########################################################################

  ###########################################################################

  def writeBreak(self, n = 1):

    self.write(self.getBreakString(n))

  ###########################################################################

  ###########################################################################

  def writeNonBreakingSpaces(self, n = 1):

    self.write(self.getNonBreakingSpaces(n))

  ###########################################################################

  ###########################################################################

  def getHeadingString(self, heading, level):

    return '<h%s>%s</h%s>' % (level, heading, level)

  ###########################################################################

  ###########################################################################

  def getBreakString(self, n = 1):

    return n * '<br>'

  ###########################################################################

  ###########################################################################

  def getNonBreakingSpaces(self, n = 1):

    return n * '&nbsp;'

  ###########################################################################

  ###########################################################################

  def getAttrString(self, **attrs):

    keys = list(attrs.keys())
    keys.sort()

    substitutionDict = { '_class': 'class' }
    attrString = ' '.join([ '%s="%s"' % (substitutionDict.get(key, key), attrs[key]) for key in keys ])
    if attrString:
      attrString = ' ' + attrString

    return attrString

  ###########################################################################

  ###########################################################################

  def getLinkString(self, link, message, **attrs):

    linkString = '<a href="%s"%s>%s</a>' % (link, self.getAttrString(**attrs), message)

    return linkString

  ###########################################################################

  ###########################################################################

  def getAnchorLinkString(self, link, message = '', **attrs):

    linkString = '<a name="%s"%s>%s</a>' % (link, self.getAttrString(**attrs), message)

    return linkString

  ###########################################################################

  ###########################################################################

  def getStyleString(self, styleString='', **styleAttrs):

    styleString = '<span%s>%s</span>' % (self.getAttrString(**styleAttrs), styleString)

    return styleString

  ###########################################################################

  ###########################################################################

  def getImageString(self, **attrs):

    imageString = '<img %s/>' % self.getAttrString(**attrs)

    return imageString

  ###########################################################################

  ###########################################################################

  def getEmphasisString(self, emphasisString):

    emphasisString = '<em>%s</em>' % emphasisString

    return emphasisString

  ###########################################################################

  ###########################################################################

  def getStrongString(self, strongString):

    strongString = '<strong>%s</strong>' % strongString

    return strongString

  ###########################################################################

  ###########################################################################

  def getSmallString(self, smallString):

    smallString = '<small>%s</small>' % smallString

    return smallString

  ###########################################################################

  ###########################################################################

  def getItalicString(self, italicString):

    italicString = '<i>%s</i>' % italicString

    return italicString

  ###########################################################################

  ###########################################################################

  def normaliseString(self, ss):
    """ convert documentation from string to XML-ready string.
    """

    if ss:
      ss = ss.replace("&", "&amp;")
      ss = ss.replace("<", "&lt;")
      ss = ss.replace("\"", "&quot;")
      ss = ss.replace(">", "&gt;")
      ss = ss.replace("\n", "<br>\n")
      ss = ss.replace("  ", "&nbsp;&nbsp;")
    else:
      ss = '' # in case None passed in

    return ss


  def writeGnuLicense(self):

    self.write("""
<h3>License</h3>
<table>
  <tr>
    <td><img src="http://www.gnu.org/graphics/philosophical-gnu-sm.jpg"/></td>
    <td><p>The GNU <b>L</b>esser <b>G</b>eneral <b>P</b>ublic <b>L</b>icense has been chosen. The <a href="http://www.gnu.org/licenses/lgpl.html" target="blank">LGPL</a> is a derivative of the GPL that was designed for software libraries. Unlike the GPL, a LGPL-ed program can be incorporated into a proprietary program.</p>
        <ul>
          <li>Can be mixed with non-free software. The LGPL, allows someone to merge your program with their own proprietary software, but without allowing people to make modifications to your own code private.<br/><br/></li>
          <li>Modifications cannot be taken private.<br/><br/></li>
          <li>Cannot be re-licensed by anyone.<br/><br/></li>
          <li>Does not contain special privileges for the original copyright holder over your modifications.</li>
        </ul>
    </td>
  </tr>
</table>
""")

  def writeDiagramHelpContent(self):

    self.write("""
<h3>Help</h3>

<p></p><b>How to use this documentation?</b> There is an entry for every package in the left navigation bar. Each package contains overview diagram as well as overview and detailed class diagrams of the individual subpackages.
<ul>
  <li>Colors denote the packages. A package is a collection of classes, data types and possibly other packages. It is used for subdividing the contents of the model.</li>
  <li><b>Boxes</b> show classes with their name (in bold) and attributes.</li>
  <li><b>Black lines</b> represent relationships between two classes that can indicate one or two-way navigation, depending on the presence of an arrow showing the direction of the navigability.</li>
  <li>Multiplicity is specified at the respective end of the association. Examples are '0..1' (zero or one), '2' (exactly 2), '1..*' (1 to infinity) or '*' (0 to infinity). If no multiplicity is given, it defaults to '0..1'.</li>
  <li>The role of the association is represented by a name at either or both ends. If no name is given, it defaults to the name of the class at the other end, starting with lower case, with a final s (for plural) where appropriate. </li>
  <li><b>Diamonds</b> represent a composition association where the containing class is on the diamond side of the line e.g. one instance of ccp.Sample.Sample can contain many ccp.Sample.SampleComponent entities.</li>
  <li><b>Orange lines</b> show inheritance between classes e.g. ccp.SampleComponent.AbstractComponent is the superclass of all subtype components.</li>
</ul>

<p></p><b>What is the 'data model'?</b> The data model itself is an abstract description of all the data commonly used. This abstract description is represented and maintained graphically using the Unified Modelling Language (UML).

<p></p><b>What are 'packages'?</b> The data model is split up in packages. Each of these packages describes a 'unit' of information that can be shared by other packages. For example, the description of a template molecule is done in the 'ccp.Molecule' package, the description of a molecular system with 'real' molecules is done in the 'ccp.MolSystem' package. The 'ccp.Nmr' package uses information from the 'ccp.MolSystem' package, which could be shared by an 'Xray' package if it was available.

<p></p>This documentation may not cover all known model packages. Some diagrams may contain classes from model packages that are not covered in the present documentation. If so, you should assume that these classes are not relevant to your purpose.

""")


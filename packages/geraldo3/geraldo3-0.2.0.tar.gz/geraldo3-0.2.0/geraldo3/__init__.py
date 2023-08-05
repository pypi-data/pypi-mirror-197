"""
Geraldo Reports Engine
======================

Overview
--------

Geraldo is a reports generator created to work like ReportBuilder, QuickReport
or Jasper Reports. It has bands with fixed width and flexible height to show on
top, summary, page header, page footer, in table or each one for an object.

It is under GPL and works only with Django framework and Python language.

It depends on ReportLab library to work.

Packages Structure
------------------

- base.py - contains report base classes and definitions, including report,
  subreport, bands an groupping.

- barcodes.py - contains code related to render barcodes in reports.

- cache.py - contains settings and backend to store reports in cache.

- charts.py - contains code to make charts.

- crossreference.py - contains the crossreference table matrix class.

- exceptions.py - contains Geraldo specific exceptions.

- graphics.py - contains graphic classes and definitions

- models.py - there is nothing. Just to be compatible with Django pluggable
  application structure and make possible run tests suite.

- widgets.py - contains widget classes and definitions.

- utils.py - contains useful functions, decorators and flags.

- generators - a package that contains generator classes.

- tests - a package with automated doc tests.
"""

import importlib.metadata

__version__ = importlib.metadata.version("Geraldo3")
 # todo get info for the other fiels from toml file too
__author__ = 'Marinho Brandao, Nico C. de Groot'
__license__ = 'GNU Lesser General Public License (LGPL)'
__url__ = 'http://geraldo.sourceforge.net/'

from .base import Report, ReportBand, DetailBand, TableBand, ReportGroup,\
        SubReport, landscape, GeraldoObject, ManyElements, CROSS_COLS
from .widgets import Label, ObjectValue, SystemField
from .utils import FIELD_ACTION_VALUE, FIELD_ACTION_COUNT, FIELD_ACTION_AVG,\
        FIELD_ACTION_MIN, FIELD_ACTION_MAX, FIELD_ACTION_SUM,\
        FIELD_ACTION_DISTINCT_COUNT, BAND_WIDTH
from .graphics import RoundRect, Rect, Line, Circle, Arc, Ellipse, Image
from .exceptions import EmptyQueryset, ObjectNotFound, ManyObjectsFound, AbortEvent
from .crossreference import CrossReferenceMatrix


"""Custom typing"""

from enum import Enum


class StudyType(Enum):
	H5_10X=1
	H5AD=2
	MTX_10X=3
	RDS=5
	TSV=6


class Species(Enum):
  HUMAN='human'
  MOUSE='mouse'
  NON_HUMAN_PRIMATE='primate'


class InputMatrixType(Enum):
  RAW='raw'
  NORMALIZED='normalized'


UNIT_RAW = 'raw'
UNIT_LOGNORM = 'lognorm'

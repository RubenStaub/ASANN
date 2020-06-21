#!/usr/bin/env python3

"""Simple reader for chemical structures"""

from six import with_metaclass
from abc import ABCMeta, abstractmethod
import warnings

# Check and try to import libraries for reading various structures
_has_reader = False
# Try to import ASE
try:
    import ase.io
    _has_ase = True
    _has_reader = True
except ImportError:
    _has_ase = False
    warnings.warn('Unable to import ASE for reading file structure, trying other librairies', category=ImportWarning)
# Try to import Pymatgen, if required
if not _has_reader:
    try:
        import pymatgen
        _has_pymatgen = True
        _has_reader = True
    except ImportError:
        _has_pymatgen = False
        warnings.warn('Unable to import Pymatgen for reading file structure, trying other librairies', category=ImportWarning)
# Check that at least one required library is available
if not _has_reader:
    raise(NotImplementedError('Cannot find any suitable library for reading file structures'))



class AbstractStructure(with_metaclass(ABCMeta)):
	"""Basic base class for chemical structures"""
	
	structure = None
	pbc_enabled = False
	
	@abstractmethod
	def __init__(self, filename):
		"""Create chemical structure object"""
		pass
	
	@classmethod
	def from_file(cls, filename):
		return(cls(filename))
	
	@abstractmethod
	def get_cell_matrix(self):
		"""Retrieve cell vectors, if applicable"""
		pass
	
	@abstractmethod
	def get_frac_coords(self):
		"""Retrieve fractional atomic coordinates"""
		pass
	
	@abstractmethod
	def get_cart_coords(self):
		"""Retrieve cartesian atomic coordinates"""
		pass
	
	def get_coords(self):
		"""Retrieve atomic coordinates, fractional if available, cartesian otherwise"""
		if self.pbc_enabled:
			return(self.get_frac_coords())
		else:
			return(self.get_cart_coords())

class AseStructure(AbstractStructure):
	"""Basic ASE atoms wrapper"""
	
	def __init__(self, filename):
		# Import ASE
		import ase.io
		
		# Read structure
		self.structure = ase.io.read(filename)
		
		# Determine if system has unit cell defined
		self.pbc_enabled = all(self.structure.pbc)
	
	def get_cell_matrix(self):
		# Retrieve cell vectors if appplicable
		if self.pbc_enabled:
			return(self.structure.cell)
		else:
			return(None)
	
	def get_frac_coords(self):
		# Check that fractional coordinates are defined
		assert(self.pbc_enabled)
		
		# Retrieve fractional coordinates
		return(self.structure.get_scaled_positions())
	
	def get_cart_coords(self):
		# Retrieve cartesian coordinates
		return(self.structure.get_positions())

class PymatgenStructure(AbstractStructure):
	"""Basic Pymatgen structure wrapper"""
	
	def __init__(self, filename):
		# Import ASE
		import pymatgen as pym
		
		# Read structure and set pbc
		try:
			# Read as periodic structure (pymatgen.Structure)
			self.structure = pym.Structure.from_file(filename)
			self.pbc_enabled = True
		except ValueError: # Pymatgen.Structure raises a ValueError when reading from a file format without unit cell defined
			# Read as non-periodic structure (pymatgen.Molecule)
			self.structure = pym.Molecule.from_file(filename)
			self.pbc_enabled = False
		
		return(self)
	
	def get_cell_matrix(self):
		# Retrieve cell vectors if appplicable
		if self.pbc_enabled:
			return(self.structure.lattice.matrix)
		else:
			return(None)
	
	def get_frac_coords(self):
		# Check that fractional coordinates are defined
		assert(self.pbc_enabled)
		
		# Retrieve fractional coordinates
		return(self.structure.frac_coords)
	
	def get_cart_coords(self):
		# Retrieve cartesian coordinates
		return(self.structure.cart_coords)

def structure_from_file(filename):
	"""Basic chemical structure file reader wrapper"""
	# Choose and fill a structure handler, depending on availability from local librairies
	if _has_ase:
		return(AseStructure.from_file(filename))
	elif _has_pymatgen:
		return(PymatgenStructure.from_file(filename))

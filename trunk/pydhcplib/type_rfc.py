# -*- encoding: utf-8 -*-
"""
pydhcplib module: type_rfc

Purpose
=======
 Defines the pydhcplib-specific RFC types.
 
Legal
=====
 This file is new to pydhcplib, designed as a necessary requirement of
 staticDHCPd.
 pydhcplib is free software; you can redistribute it and/or modify
 it under the terms of the GNU General Public License as published by
 the Free Software Foundation; either version 3 of the License, or
 (at your option) any later version.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 GNU General Public License for more details.

 You should have received a copy of the GNU General Public License
 along with this program. If not, see <http://www.gnu.org/licenses/>.
 
 (C) Neil Tallim, 2010 <flan@uguu.ca>
"""
import type_ipv4

class _rfc(object):
	_value = None
	
	def getValue(self):
		return self._value
		
	def __hash__(self):
		return self._value.__hash__()
		
	def __repr__(self):
		return repr(self._value)
		
	def __nonzero__(self) :
		return 1
		
	def __cmp__(self, other):
		if self._value == other:
			return 0
		return 1
		
		
def _rfc1035Parse(domain_name):
	bytes = []
	for fragment in domain_name.split('.'):
		bytes += [len(fragment)] + [ord(c) for c in fragment]
	return bytes + [0]
	
class rfc3361(_rfc):
	def __init__(self, data):
		ip_4_mode = False
		dns_mode = False
		
		self._value = []
		for token in [token for token in [t.strip() for t in data.split(',')] if token]:
			try:
				ip_4 = type_ipv4.ipv4(token)
				self._value += ip_4.list()
				ip_4_mode = True
			except ValueError:
				self._value += _rfc1035Parse(token)
				dns_mode = True
				
		if not ip_4_mode ^ dns_mode:
			raise ValueError("RFC3361 argument '%(data)s is not valid: contains both IPv4 and DNS-based entries" % {
			 'data': data,
			})
			
		self._value.insert(0, int(ip_4_mode))
		
class rfc3397(_rfc):
	def __init__(self, data):
		self._value = []
		for token in [token for token in [t.strip() for t in data.split(',')] if token]:
			self._value += _rfc1035Parse(token)
			

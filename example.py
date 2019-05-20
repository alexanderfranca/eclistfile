# -*- coding: utf-8 -*-

import pprint

from eclistfile.eclistfile import *

ec = EcListFile('./tests/fixtures/ec.list')

ec.generate_map_data() 
data = ec.maps_data()

pprint.pprint(data)

import sys
import os
import unittest
from eclistfile.eclistfile import *
import re


class TestEcListFile( unittest.TestCase ):

    def setUp( self ):
        self.ec = EcListFile( './tests/fixtures/ec.list' )


    def test_metabolic_map_number( self ):

        result =  self.ec.metabolic_map_number('path:ec00010    ec:2.7.1.199')
        self.assertEqual( result, '00010' )

    def test_metabolic_map_data( self ):

        result =  self.ec.metabolic_map_data('path:ec00010    ec:2.7.1.199')
        self.assertEqual( result, 'ec:2.7.1.199' )

    def test_metabolic_map_ec( self ):

        result =  self.ec.metabolic_map_ec('path:ec00010    ec:2.7.1.199')
        self.assertEqual( result, '2.7.1.199' )

    def test_is_metabolic_map_data_an_ec_number( self ):

        result =  self.ec.is_metabolic_map_data_an_ec_number('path:ec00010    ec:2.7.1.199')
        self.assertTrue( result )

    def test_generate_map_data( self ):

        self.ec.generate_map_data()

        self.assertTrue( type( self.ec.maps_and_ecs) is dict )

    def test_maps_data( self ):

        self.assertTrue( type( self.ec.maps_and_ecs) is dict )

    def test_maps_data_value( self ):

        data = self.ec.maps_and_ecs

        total00010 = len( data['00010'] )
        self.assertEqual( total00010, 98 ) 

    def test_ecs_maps( self ):

        data = self.ec.ecs_maps()

        total00010 = len( data['4.1.1.32'] )
        self.assertEqual( total00010, 7 ) 

    def test_incomplete_ec_numbers( self ):

        data = self.ec.incomplete_ec_numbers()

        self.assertTrue( type( data ) is list ) 
        self.assertTrue( len( data ) > 1 ) 
        self.assertTrue( '1.3.99.-' in data )
        self.assertFalse( '1.1.1.1' in data )

        self.ec.all_ecs_and_maps()

    def test_complete_ec_numbers( self ):

        data = self.ec.complete_ec_numbers()

        self.assertTrue( type( data ) is list ) 
        self.assertTrue( len( data ) > 1 ) 
        self.assertFalse( '1.3.99.-' in data )
        self.assertTrue( '1.1.1.1' in data )

    def test_all_ec_numbers( self ):

        data = self.ec.all_ec_numbers()

        self.assertTrue( type( data ) is list ) 
        self.assertTrue( len( data ) > 1 ) 
        self.assertTrue( '1.3.99.-' in data )
        self.assertTrue( '1.1.1.1' in data )

    def test_all_ecs_and_maps(self):

        data = self.ec.all_ecs_and_maps()
        self.assertTrue( type( data ) is dict ) 
        self.assertTrue( len( data ) > 1 ) 
        self.assertTrue( '00592' in data['1.-.-.-'] )



if __name__ == "__main__":
    unittest.main()

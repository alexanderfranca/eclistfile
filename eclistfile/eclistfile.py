import re
import pprint

class EcListFile:
    """
    KEGG pathway/ec.list file stores the relation between metabolic pathway maps number and EC numbers.

    It's important to emphasize that ec.list file is about the Pathway KEGG database, in other words, metabolic pathways data ONLY.

    Don't rely in this class to relate EC numbers with any other KEGG database (genes, genomes etc).

    Unless, of course, you know what your're doing.

    Attributes:
        ecs_and_maps(dict): EC numbers and its related metabolic map numbers.
        maps_and_ecs(dict): Metabolic map numbers and its related EC numbers.
    """

    ecs_and_maps = {}
    maps_and_ecs = {}

    def __init__(self, ec_file=None):

        self.ec_file = ec_file

    def metabolic_map_number(self, string=None):
        """
        Returns the metabolic map number from a string.

        That kind of string is something like: 'path:ec00010   ec:4.1.1.49'
        """

        re_map = re.compile("^path:ec([0-9]{1,})\s.*$")
        result = re_map.search(string)

        return result.group(1)

    def metabolic_map_data(self, string=None):
        """
        Returns the metabolic map related data from a string.

        That kind of string is something like: 'path:ec00010   ec:4.1.1.49'
        """

        re_map = re.compile("^path:ec[0-9]{1,}\s(.*)$")
        result = re_map.search(string)
        result = result.group(1)
        result = re.sub('^\ {1,}', '', result)

        return result

    def metabolic_map_ec(self, string=None):
        """
        Returns the EC number related to a map (from the ec.list string line).

        That kind of string is something like: 'path:ec00010   ec:4.1.1.49'
        """

        re_map = re.compile("^path:ec[0-9]{1,}\s(.*)$")
        result = re_map.search(string)
        result = result.group(1)
        result = result.replace('ec:', '')
        result = re.sub('^\ {1,}', '', result)
        result = re.sub('\s', '', result)

        return result

    def is_metabolic_map_data_an_ec_number(self, string=None):
        """
        Returns if the map data is an EC number.
        """

        #re_ec_number = re.compile('ec:([0-9]{1,})\.([0-9]{1,})\.([0-9]{1,})\.([0-9]{1,}|n.*)')
        re_ec_number = re.compile(
            'ec:((?:[0-9]{1,}|-)\.(?:[0-9]{1,}|-)\.(?:[0-9]{1,}|-)\.(?:[0-9]{1,}|-)).*$')

        return re_ec_number.search(string)

    def generate_map_data(self):
        """
        Read ec.list and returns full filled dictionary.

        Returns:
            (dict): List of all metabolic maps and related EC numbers.
        """

        with open(self.ec_file) as ec_file:
            for line in ec_file:
                line = line.rstrip('\r\n')

                map_number = self.metabolic_map_number(line)
                map_data = self.metabolic_map_data(line)

                if self.is_metabolic_map_data_an_ec_number(map_data):
                    ec_number = self.metabolic_map_ec(line)

                    if map_number not in self.maps_and_ecs:
                        self.maps_and_ecs[map_number] = []

                    if ec_number not in self.ecs_and_maps:
                        self.ecs_and_maps[ec_number] = []

                    self.maps_and_ecs[map_number].append(ec_number)
                    self.ecs_and_maps[ec_number].append(map_number)

    def maps_data(self):
        """
        Returns a dictionary containing all map numbers and its related EC numbers.

        Returns:
            (dict): Dictionary with all maps data.
        """

        if len(self.maps_and_ecs) == 0:
            self.generate_map_data()

        return self.maps_and_ecs

    def ecs_maps(self):
        """
        Returns a dictionary containing all EC numbers and its map numbers.

        Returns:
            (dict): Dictionary with all maps data.
        """

        if len(self.maps_and_ecs) == 0:
            self.generate_map_data()

        return self.ecs_and_maps

    def incomplete_ec_numbers(self):
        """
        Returns all the incomplete EC numbers.

        Returns:
            (list): EC numbers.
        """

        incomplete_ecs = []

        re_incomplete = re.compile('-')

        if len(self.maps_and_ecs) == 0:
            self.generate_map_data()

        ecs = self.ecs_and_maps.keys()

        for ec in ecs:
            result = re_incomplete.search(ec)

            if result:
                incomplete_ecs.append(ec)

        incomplete_ecs = set(incomplete_ecs)
        incomplete_ecs = list(incomplete_ecs)

        return incomplete_ecs

    def complete_ec_numbers(self):
        """
        Returns all the complete EC numbers.

        Returns:
            (list): EC numbers.
        """

        if len(self.maps_and_ecs) == 0:
            self.generate_map_data()

        complete_ecs = []

        re_incomplete = re.compile('-')

        ecs = self.ecs_and_maps.keys()

        for ec in ecs:
            result = re_incomplete.search(ec)

            if not result:
                complete_ecs.append(ec)

        complete_ecs = set(complete_ecs)
        complete_ecs = list(complete_ecs)

        return complete_ecs

    def all_ec_numbers(self):
        """
        Returns all EC numbers.

        Returns:
            (list): EC numbers.
        """

        if len(self.maps_and_ecs) == 0:
            self.generate_map_data()

        complete = self.complete_ec_numbers()
        incomplete = self.incomplete_ec_numbers()

        all_ecs = complete + incomplete
        all_ecs = set(all_ecs)

        return list(all_ecs) 

    def all_ecs_and_maps(self):
        """
        Returns all EC numbers and its related metabolic map numbers.

        Returns:
            (list): EC numbers and related metabolic map numbers.
        """

        if len(self.maps_and_ecs) == 0:
            self.generate_map_data()

        return self.ecs_and_maps






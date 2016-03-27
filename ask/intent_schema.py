'''
Abstractions around IntentSchema class. 
'''
from __future__ import print_function
import json
from collections import OrderedDict
from argparse import ArgumentParser
import os
from .config.config import read_in

slot_type_mappings = {
    1 : ["AMAZON.LITERAL",
         "Description: " "passes the words for the slot value with no conversion"],
    2 : ["AMAZON.NUMBER",
         "Description: " 'converts numeric words (five) into digits (such as 5)'],
    3 : ["AMAZON.DATE", "Description: "
         'converts words that indicate dates (today, tomorrow, or july) into a date format (such as 2015-07-00T9)'],
    4 : ["AMAZON.TIME",
         "Description: " 'converts words that indicate time (four in the morning, two p m) into a time value (16:00).'],
    5 : ["AMAZON.DURATION",
         "Description: " 'converts words that indicate durations (five minutes) into a numeric duration (5M).'],
    6 : ["AMAZON.US_CITY",
         "Description: Improves slot performance on all major US cities"]
}


class IntentSchema(object):
    '''
    Wrapper class to manipulate Intent Schema
    '''
    def __init__(self, json_obj=None):
        if json_obj:
            self._obj = json_obj
        else:
            self._obj = OrderedDict({ "intents" : [] })

            
    def add_intent(self,intent_name, slots=None):
        if not slots: slots = []
        intent = OrderedDict()
        intent ['intent'], intent['slots'] = intent_name, slots        
        self._obj['intents'].append(intent)
        
        
    def build_slot(self, slot_name, slot_type):
        slot = OrderedDict()
        slot['name'], slot['type'] = slot_name, slot_type
        return slot
    
    def __str__(self):
        return json.dumps(self._obj, indent=2)

    
    def get_intents(self):
        return self._obj['intents']     

    
    @classmethod
    def interactive_build(self, fpath=None):
        intent_schema = IntentSchema.from_filename(fpath)
        print ("How many intents would you like to add")
        num = read_in(int)
        for i in range(num):
            intent_schema._add_intent_interactive(intent_num=i+1)
        return intent_schema

    def save_to_file(self, filename):
        with open(filename, 'w') as fp:
            print(self, file=fp)
            
    def _add_intent_interactive(self, intent_num):
        print ("Name of intent number : ", intent_num)
        intent_name = read_in(str)
        print ("How many slots?")
        num_slots = read_in(int)
        slot_list = []
        for i in range(num_slots):
            print ("Slot name no.", i+1)
            slot_name = read_in(str).strip()
            print ("Slot type? Enter a number for AMAZON supported types below,"
                   "else enter a string for a Custom Slot")
            print (json.dumps(slot_type_mappings, indent=True))
            slot_type_str = read_in(str)
            try: slot_type = slot_type_mappings[int(slot_type_str)][0] 
            except: slot_type = slot_type_str
            slot_list += [self.build_slot(slot_name, slot_type)]                    
        self.add_intent(intent_name, slot_list)                        

    
    @classmethod
    def from_filename(self, filename):
        if os.path.exists(filename):
            with open(filename) as fp:
                return IntentSchema(json.load(fp, object_pairs_hook=OrderedDict))
        else:
            print ('File does not exist')
            return IntentSchema()
        

if __name__ == '__main__':

    parser = ArgumentParser()
    parser.add_argument('--intent_schema', '-i', required=True) 
    parser.add_argument('--overwrite', '-o', action='store_true',
                        default=False)
    args = parser.parse_args()

    if not args.overwrite:
        print ('In "Append", mode')
        intent_schema = IntentSchema.interactive_build(args.intent_schema)
    else:
        print ('In OVERWRITE mode')
        intent_schema = IntentSchema.interactive_build()        

    print ("Write to file:", args.intent_schema,"? (y/n)")
    dec = read_in(str).strip().lower()
    if dec == "y":
        intent_schema.save_to_file(args.intent_schema)
    elif dec == "n":
        pass

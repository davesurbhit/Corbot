# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet, EventType
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Action, Tracker, FormValidationAction
import webbrowser
from rasa_sdk.types import DomainDict
import requests
from rasa_sdk.events import AllSlotsReset, Restarted
from main import Dose_availability_District, Dose_availability_pincode

class ValidateForm(Action):
    def name(self) -> Text:
        return "corona_tracker_form"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        required_slots = ["state"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        # All slots are filled.
        return [SlotSet("requested_slot", None)]

class ActionSubmit(Action):
    def name(self) -> Text:
        return "action_submit"

    def run(
        self,
        dispatcher,
        tracker: Tracker,
        domain: "DomainDict",
    ) -> List[Dict[Text, Any]]:
        State=tracker.get_slot("state")
        response = requests.get("https://api.apify.com/v2/key-value-stores/toDWvRj1JpTXiM8FF/records/LATEST").json()
        message = ("Active Cases: "+str(response["activeCases"])+ "\n" +
                "Newly Infected: "+str(response["activeCasesNew"])+ "\n" +
                "Total Recovered: "+str(response["recovered"])+ "\n" +
                "Total Deceased: "+str(response["deaths"])+ "\n" +
                "Total Infected: "+str(response["totalCases"]))
        dispatcher.utter_message(message)
        return [AllSlotsReset()]

class ValidatepincodeForm(FormValidationAction):
    def name(self) -> Text:
        return "slot_pincode_form"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        required_slots = ["pincode", "date"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

class ValidateDistrictForm(FormValidationAction):
    def name(self) -> Text:
        return "slot_district_form"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        required_slots = ["district_id", "date"]

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                # The slot is not filled yet. Request the user to fill this slot next.
                return [SlotSet("requested_slot", slot_name)]

        return [SlotSet("requested_slot", None)]

class ActionPincodeSubmit(Action):

    def name(self) -> Text:
        return "action_pincode_submit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global message
        message = Dose_availability_pincode(tracker.get_slot('pincode'),tracker.get_slot('date'))
        dispatcher.utter_message(text=message)
        # buttons = [
        #     {'payload': "/affirm", 'title': "Yes"},
        #     {'payload': "/deny", 'title': "No"},
        # ]
        # dispatcher.utter_message(text="Would you like to get the details on your email id?",buttons=buttons)

        return [AllSlotsReset()]

class ActionDistrictSubmit(Action):

    def name(self) -> Text:
        return "action_district_submit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        global message
        message=Dose_availability_District(tracker.get_slot('district_id'),tracker.get_slot('date'))
        dispatcher.utter_message(text=message)
        # buttons = [
        #     {'payload': "/affirm", 'title': "Yes"},
        #     {'payload': "/deny", 'title': "No"},
        # ]
        # dispatcher.utter_message(text="Would you like to get the details on your email id?",buttons=buttons)

        return [AllSlotsReset()]

class ActionRestart(Action):

    def name(self) -> Text:
      return "action_restart"

    async def run(
      self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

      return [Restarted()]
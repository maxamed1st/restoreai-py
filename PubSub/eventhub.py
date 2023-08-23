class EventHub:
    """Observer pattern based hub for event.
     Use subscribe method to be notified when an event occurs 
     Use notify to emit an event to subscribers.
     Optionally attach payload when emitting event"""
    _instance = None
    _subscribers = {}

    def __new__(cls) -> object:
        #create object using the singleton pattern
        if cls._instance is None:
            cls._instance = super(EventHub, cls).__new__(cls)
        return cls._instance

    @classmethod
    def _attach(cls, event: str):
        #add new event
        if event not in cls._subscribers:
            cls._subscribers[event] = []

    @classmethod
    def subscribe(cls, receiver: callable, event: str) -> bool:
        """subscribe to an event
        if the callback function provided is already subscriber to the event,
        then False is returned otherwise True is returned"""
        #create event if necessary
        cls._attach(event)

        #subscribe to the event
        if receiver in cls._subscribers[event]:
            return False
        cls._subscribers[event].append(receiver)
        return True

    @classmethod
    def notify(cls, event: str, payload: dict = None) -> bool:
        """emit event to subscribers.
        if the event is emitted at least to one subscriber 
        then True is returned otherwise False is returned"""
        result: bool = False
        #create event if necessary
        cls._attach(event)

        #notify subscribers about the event
        for callback in cls._subscribers[event]:
            callback(payload)
            if result == False:
              result = True
        return result

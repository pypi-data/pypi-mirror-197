# Copyright 2017 Mycroft AI Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""Event scheduler system for calling skill (and other) methods at a specific
times.
"""
import json
import shutil
import time
from datetime import datetime, timedelta
from threading import Thread, Lock
from os.path import isfile, join, expanduser

from ovos_config.config import Configuration
from ovos_config.locations import get_xdg_data_save_path, get_xdg_config_save_path
from mycroft.messagebus.message import Message
from ovos_utils.log import LOG
from ovos_utils.events import create_basic_wrapper, EventContainer, EventSchedulerInterface


def repeat_time(sched_time, repeat):
    """Next scheduled time for repeating event. Guarantees that the
    time is not in the past (but could skip interim events)

    Args:
        sched_time (float): Scheduled unix time for the event
        repeat (float):     Repeat period in seconds

    Returns: (float) time for next event
    """
    next_time = sched_time + repeat
    while next_time < time.time():
        # Schedule at an offset to assure no doubles
        next_time = time.time() + abs(repeat)
    return next_time


class EventScheduler(Thread):
    """Create an event scheduler thread. Will send messages at a
     predetermined time to the registered targets.

    Args:
        bus:            Mycroft messagebus (mycroft.messagebus)
        schedule_file:  File to store pending events to on shutdown
    """

    def __init__(self, bus, schedule_file='schedule.json', autostart=True):
        super().__init__()

        self.events = {}
        self.event_lock = Lock()

        self.bus = bus
        self.is_running = True

        core_conf = Configuration()
        data_dir = core_conf.get('data_dir') or get_xdg_data_save_path()
        old_schedule_path = join(expanduser(data_dir), schedule_file)

        self.schedule_file = join(get_xdg_config_save_path(), schedule_file)
        if isfile(old_schedule_path):
            shutil.move(old_schedule_path, self.schedule_file)

        if self.schedule_file:
            self.load()

        self.bus.on('mycroft.scheduler.schedule_event',
                    self.schedule_event_handler)
        self.bus.on('mycroft.scheduler.remove_event',
                    self.remove_event_handler)
        self.bus.on('mycroft.scheduler.update_event',
                    self.update_event_handler)
        self.bus.on('mycroft.scheduler.get_event',
                    self.get_event_handler)
        if autostart:
            self.start()

    def load(self):
        """Load json data with active events from json file."""
        if isfile(self.schedule_file):
            json_data = {}
            with open(self.schedule_file) as f:
                try:
                    json_data = json.load(f)
                except Exception as e:
                    LOG.error(e)
            current_time = time.time()
            with self.event_lock:
                for key in json_data:
                    event_list = json_data[key]
                    # discard non repeating events that has already happened
                    self.events[key] = [tuple(e) for e in event_list
                                        if e[0] > current_time or e[1]]

    def run(self):
        while self.is_running:
            self.check_state()
            time.sleep(0.5)

    def check_state(self):
        """Check if an event should be triggered."""
        with self.event_lock:
            # Check all events
            pending_messages = []
            for event in self.events:
                current_time = time.time()
                e = self.events[event]
                # Get scheduled times that has passed
                passed = [(t, r, d, c) for
                          (t, r, d, c) in e if t <= current_time]
                # and remaining times that we're still waiting for
                remaining = [(t, r, d, c) for
                             t, r, d, c in e if t > current_time]
                # Trigger registered methods
                for sched_time, repeat, data, context in passed:
                    pending_messages.append(Message(event, data, context))
                    # if this is a repeated event add a new trigger time
                    if repeat:
                        next_time = repeat_time(sched_time, repeat)
                        remaining.append((next_time, repeat, data, context))
                # update list of events
                self.events[event] = remaining

        # Remove events have are now completed
        self.clear_empty()

        # Finally, emit the queued up events that triggered
        for msg in pending_messages:
            self.bus.emit(msg)

    def schedule_event(self, event, sched_time, repeat=None,
                       data=None, context=None):
        """Add event to pending event schedule.

        Args:
            event (str): Handler for the event
            sched_time ([type]): [description]
            repeat ([type], optional): Defaults to None. [description]
            data ([type], optional): Defaults to None. [description]
            context (dict, optional): context (dict, optional): message
                                      context to send when the
                                      handler is called
        """
        data = data or {}
        with self.event_lock:
            # get current list of scheduled times for event, [] if missing
            event_list = self.events.get(event, [])

            # Don't schedule if the event is repeating and already scheduled
            if repeat and event in self.events:
                LOG.debug(f'Repeating event {event} is already scheduled, discarding')
            else:
                # add received event and time
                event_list.append((sched_time, repeat, data, context))
                self.events[event] = event_list

    def schedule_event_handler(self, message):
        """Messagebus interface to the schedule_event method.
        Required data in the message envelope is
            event: event to emit
            time:  time to emit the event

        Optional data is
            repeat: repeat interval
            data:   data to send along with the event
        """
        event = message.data.get('event')
        sched_time = message.data.get('time')
        repeat = message.data.get('repeat')
        data = message.data.get('data')
        context = message.context
        if event and sched_time:
            self.schedule_event(event, sched_time, repeat, data, context)
        elif not event:
            LOG.error('Scheduled event name not provided')
        else:
            LOG.error('Scheduled event time not provided')

    def remove_event(self, event):
        """Remove an event from the list of scheduled events.

        Args:
            event (str): event identifier
        """
        with self.event_lock:
            if event in self.events:
                self.events.pop(event)

    def remove_event_handler(self, message):
        """Messagebus interface to the remove_event method."""
        event = message.data.get('event')
        self.remove_event(event)

    def update_event(self, event, data):
        """Change an existing events data.

        This will only update the first call if multiple calls are registered
        to the same event identifier.

        Args:
            event (str): event identifier
            data (dict): new data
        """
        with self.event_lock:
            # if there is an active event with this name
            if len(self.events.get(event, [])) > 0:
                time, repeat, _, context = self.events[event][0]
                self.events[event][0] = (time, repeat, data, context)

    def update_event_handler(self, message):
        """Messagebus interface to the update_event method."""
        event = message.data.get('event')
        data = message.data.get('data')
        self.update_event(event, data)

    def get_event_handler(self, message):
        """Messagebus interface to get_event.

        Emits another event sending event status.
        """
        event_name = message.data.get("name")
        event = None
        with self.event_lock:
            if event_name in self.events:
                event = self.events[event_name]
        emitter_name = f'mycroft.event_status.callback.{event_name}'
        self.bus.emit(message.reply(emitter_name, data=event))

    def store(self):
        """Write current schedule to disk."""
        with self.event_lock:
            with open(self.schedule_file, 'w') as f:
                json.dump(self.events, f)

    def clear_repeating(self):
        """Remove repeating events from events dict."""
        with self.event_lock:
            for e in self.events:
                self.events[e] = [i for i in self.events[e] if i[1] is None]

    def clear_empty(self):
        """Remove empty event entries from events dict."""
        with self.event_lock:
            self.events = {k: self.events[k] for k in self.events
                           if self.events[k] != []}

    def shutdown(self):
        """Stop the running thread."""
        self.is_running = False
        # Remove listeners
        self.bus.remove_all_listeners('mycroft.scheduler.schedule_event')
        self.bus.remove_all_listeners('mycroft.scheduler.remove_event')
        self.bus.remove_all_listeners('mycroft.scheduler.update_event')
        # Wait for thread to finish
        self.join()
        # Prune event list in preparation for saving
        self.clear_repeating()
        self.clear_empty()
        # Store all pending scheduled events
        self.store()


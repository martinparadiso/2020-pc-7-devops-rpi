#!/usr/bin/python3

import docker                       # For managing the container
from multiprocessing import Lock    # Lock for accessing the docker daemon
from threading import Thread, Event  # For cancelable sleeps
import time
import signal
from enum import Enum
import os
import json

docker_lock = Lock()
managed_container_name = 'cicd_managed_container'


class ServiceInUse(Exception):
    pass

class States(Enum):
    EXITED = 'exited'
    PULLING = 'pulling'
    STARTING = 'starting'
    RUNNING = 'running'

class Container():
    """Object representing the docker container that is executing (or should be
    executing) in this device
    """

    def __init__(self):
        self.image = os.environ['CONTAINER_IMAGE']
        try:
            self.polling_interval = int(os.environ['POLL_INTERVAL']) * 60
        except:
            self.polling_interval = 30 * 60
        self.state = States.EXITED
        self.clock = Event()
        self.container = None
        self.new_tag = None

        try:
            with open('/app/data/tag') as tag_file:
                self.tag = tag_file.readline().rstrip()
        except:
            self.tag = 'master'

        with open('/app/data/docker_config.json') as config_file:
            self.container_args = json.load(config_file)

        # Configure the SIGTERM callback
        for s in [signal.SIGINT, signal.SIGTERM]:
            signal.signal(s, self.__exit_callback)

        # Connect to the docker client
        self.docker_iface = docker.from_env()

        # Start the control loop
        self.thread = Thread(target=self.__state_loop)
        self.thread.start()

    def __exit_callback(self):
        """Mark the flag of stop, and wake up the state loop
        """
        self.stop = True
        self.clock.set()  # In case the loop is in idle

    def __state_loop(self):
        """Function control the state machine loop
        """
        self.stop = False

        # If the container already exists (from a previous failed attempt)
        try:
            old = self.docker_iface.containers.get(managed_container_name)
            try:
                old_image_id = old.image.id
                old.stop()
                old.remove()
            finally:
                try:
                    # Try-except because the image may be used by other containers
                    self.docker_iface.images.remove(old_image_id)
                except:
                    pass
        except:
            pass

        while not self.stop:

            # Exited state
            if self.state is States.EXITED:
                self.state = States.PULLING

            # Pulling state
            elif self.state is States.PULLING:
                with docker_lock:

                    # The order of images is:
                    # newly assigned -> previous -> 'master'

                    # Try the new tag assigned
                    new_failed = True

                    if self.new_tag:
                        try:
                            new_image = self.docker_iface.images.pull(
                                self.image, tag=self.new_tag)
                            self.tag = self.new_tag
                            new_failed = False
                            # Store the new tag in the tag file
                            with open('/app/data/tag', 'w') as f:
                                f.write(self.tag)
                        except:
                            self.new_tag = None

                    # If there is no new tag, or it failed, download existing
                    if new_failed:
                        try:
                            new_image = self.docker_iface.images.pull(
                                self.image, tag=self.tag)
                        except:
                            # If that fails too, try with master
                            try:
                                new_image = self.docker_iface.images.pull(
                                    self.image, tag='master')
                            
                            except:
                                # If master doesn't work, sleep and try again
                                self.clock.wait(
                                    timeout=self.polling_interval)
                                self.clock.clear()
                                continue

                    # If the container is already running, and the images are
                    # the same, go to running, otherwise, move to start to
                    # recreate the container 
                    if self.__is_running() and new_image.id == self.__get_container().image.id:
                        self.state = States.RUNNING
                    else:
                        self.state = States.STARTING

            # Starting state
            elif self.state is States.STARTING:
                with docker_lock:
                    # If the container is running, get the old image name to
                    # remove, and stop the container
                    if self.__is_running():
                        old_image_id = self.__get_container().image.id
                        self.__get_container().stop()
                        self.__get_container().remove()
                        try:
                            # Try because the image may be used by another container
                            self.docker_iface.images.remove(old_image_id)
                        except:
                            pass

                    # Start the new container
                    self.container = self.docker_iface.containers.run(f"{self.image}:{self.tag}",
                                                                      detach=True,
                                                                      name=managed_container_name,
                                                                      **self.container_args)

                    self.state = States.RUNNING

            # Running state
            elif self.state is States.RUNNING:
                # Sleep for X minutes and then go to PULLING to check for
                # updates
                self.clock.wait(timeout=self.polling_interval)
                self.clock.clear()
                self.state = States.PULLING

        # Stop the container and delete the image
        image_id = self.__get_container().image.id
        try:
            # Try because the image may be used by another container
            self.docker_iface.images.remove(image_id)
        except:
            pass
        self.__get_container().stop()
        self.__get_container().remove()

    def __get_container(self):
        try:
            self.container.reload()
            return self.container
        except:
            return None

    def __is_running(self):
        try:
            # If the container state is not running, is exited
            if self.__get_container().status == 'running':
                return True
            else:
                return False
        # If docker raised an exception, that means the container is not running
        except:
            return False

    def status(self):
        # If the state is running, re-check, in case the container crashed
        return self.state.value

    def force_update(self):
        """Force an update check
        """
        self.clock.set()

    def switch_version(self, new_tag):
        """Change the version (tag) of the container
        """
        self.new_tag = new_tag
        self.clock.set()    # Wake up the state machine, to force the update

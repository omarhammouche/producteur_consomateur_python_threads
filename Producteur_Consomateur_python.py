import random
from threading import Thread,RLock
import threading
import time
import queue

vero = RLock()


class Colors:

    ENDC = '\033[0m'
    Green = "\033[32m"
    Blue = "\033[94m"


def wait(seconds):
    time.sleep(seconds)

# this class used to create the Producer and to add in the list
class Consumer(Thread):
    def __init__(self, products_list):
        Thread.__init__(self)
        self.products_list = products_list

    def delete_from_list(self):
        if not products_list.empty():
            print(f" {Colors.Green}{threading.current_thread().name} "
                  f"DELETED { self.products_list.get() },  "
                  f"{products_list.qsize()} items in queue  {Colors.ENDC}")

    "this function just to execute the deletion function a few times"
    def run(self):
        rand = random.randint(5, 10)
        count = 0

        while count < rand:  # every thread delete some numbers in the list (queue) so the number of deletion is
            # between 5 and 10
            with vero:
                self.delete_from_list()
                wait(1)
                count += 1


# this class call the Consumer class to create consumers threads
class ManageConsumers:
    def __init__(self, number_of_consumer, products_list):
        self.number_of_consumer = number_of_consumer
        self.products_list = products_list

    # list to store the producers Threads
    consumers = []

    def create_consumers(self):
        for i in range(self.number_of_consumer):
            self.consumers.append(Consumer(self.products_list))
        return self.consumers

    def start_consumers(self, consumers):
        for i in range(self.number_of_consumer):
            consumers[i].start()

    def join_consumers(self, consumers):
        for i in range(self.number_of_consumer):
            consumers[i].join()


# this class used to create the Producer and to add in the list
class Producer(Thread):
    def __init__(self, products_list):
        Thread.__init__(self)
        self.products_list = products_list

    def add_to_list(self):
        rand = random.randint(0, 30)
        self.products_list.put(rand)
        print(f" {Colors.Blue}{threading.current_thread().name} "
              f"ADDED {rand},  {products_list.qsize()} "
              f"items in queue  {Colors.ENDC}")

    "this function just to execute the deletion function a few times"
    def run(self):
        rand = random.randint(5, 10)
        count = 0

        while count < rand:  # every thread delete some numbers in the list (queue) so the number of deletion
            # is between 5 and 10
            with vero:
                self.add_to_list()
                wait(1)
                count += 1


# this class call the Consumer class to create consumers threads
class ManageProducers:
    def __init__(self, number_of_producer, products_list):
        self.number_of_producer = number_of_producer
        self.products_list = products_list

    # list to store the producers Threads
    producers = []

    def create_producers(self):
        for i in range(self.number_of_producer):
            self.producers.append(Producer(self.products_list))
        return self.producers

    def start_producers(self, producers):
        for i in range(self.number_of_producer):
            producers[i].start()

    def join_producers(self, producers):
        for i in range(self.number_of_producer):
            producers[i].join()


if __name__ == "__main__":

    products_list = queue.Queue(-1)  # max size is infinite when we put -1

    number_of_producers = 2  # the number of producers is fixed but the number of adding for every thread is random
    number_of_consumers = 2

    producers = []
    consumers = []

    # to create a process for the producer so the mini-processor take care of multiple thread
    producer = ManageProducers(number_of_producers, products_list)
    consumer = ManageConsumers(number_of_consumers, products_list)

    producers = producer.create_producers()
    consumers = consumer.create_consumers()

    producer.start_producers(producers)
    consumer.start_consumers(consumers)

    producer.join_producers(producers)
    consumer.join_consumers(consumers)

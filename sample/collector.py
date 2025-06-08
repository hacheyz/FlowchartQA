from typing import List

from sample.sample import Sample

class SampleCollector:
    def __init__(self, base_id: int=0):
        """
        Initialize the SampleCollector with a list of samples.
        :param base_id: The base ID for the samples, used to calculate the sample IDs.
        """
        self.base_id = base_id
        self._data = []

    def get_id(self) -> int:
        """
        Get the current number (also next sample id) of samples.
        :return: The number of samples in the collector.
        """
        return self.base_id + len(self._data)
    
    def get_samples(self) -> List[Sample]:
        """
        Get the list of samples in the collector.
        :return: List of Sample objects.
        """
        return self._data
    
    def append(self, sample: Sample):
        """
        Append a single sample to the collector.
        :param sample: Sample object to be added.
        """
        self._data.append(sample)

    def extend(self, samples: List[Sample]):
        """
        Extend the collector with a list of samples.
        :param samples: List of Sample objects to be added.
        """
        self._data.extend(samples)

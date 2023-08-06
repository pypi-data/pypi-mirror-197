from __future__ import annotations

from uuid import UUID
from typing import List, Dict, Tuple
from math import fsum, cos, sin, radians

import numpy as np
import cv2

from .bbox import BBox
from .classes_format import ImageDatasetClasses
from ....codable import Codable, KeyDescriptor


SegmentationType = List[float]


class CoretexSegmentationInstance(Codable):

    classId: UUID
    bbox: BBox
    segmentations: List[SegmentationType]

    @classmethod
    def _keyDescriptors(cls) -> Dict[str, KeyDescriptor]:
        descriptors = super()._keyDescriptors()

        descriptors["classId"] = KeyDescriptor("class_id", UUID)
        descriptors["bbox"] = KeyDescriptor("bbox", BBox)
        descriptors["segmentations"] = KeyDescriptor("annotations")

        return descriptors

    @staticmethod
    def create(classId: UUID, bbox: BBox, segmentations: List[SegmentationType]) -> CoretexSegmentationInstance:
        obj = CoretexSegmentationInstance()

        obj.classId = classId
        obj.bbox = bbox
        obj.segmentations = segmentations

        return obj

    def extractSegmentationMask(self, width: int, height: int) -> np.ndarray:
        reconstructed = np.zeros((height, width, 1), dtype="uint8")

        for segmentation in self.segmentations:
            mask = np.array(segmentation, dtype=np.int32).reshape((-1, 2))
            cv2.fillPoly(reconstructed, [mask], 1)

        return reconstructed

    def extractBinaryMask(self, width: int, height: int) -> np.ndarray:
        binaryMask = self.extractSegmentationMask(width, height)
        binaryMask[binaryMask > 0] = 1

        return binaryMask

    def centroid(self) -> Tuple[float, float]:
        flattenedSegmentations = [element for sublist in self.segmentations for element in sublist]

        listCX = [value for index, value in enumerate(flattenedSegmentations) if index % 2 == 0]
        centerX = fsum(listCX) / len(listCX)

        listCY = [value for index, value in enumerate(flattenedSegmentations) if index % 2 != 0]
        centerY = fsum(listCY) / len(listCY)

        return centerX, centerY

    def centerSegmentations(self, newCentroid: Tuple[float, float]) -> None:
        newCenterX, newCenterY = newCentroid
        oldCenterX, oldCenterY = self.centroid()

        modifiedSegmentations: List[List[float]] = []

        for segmentation in self.segmentations:
            modifiedSegmentation: List[float] = []

            for i in range(0, len(segmentation), 2):
                x = segmentation[i] + (newCenterX - oldCenterX)
                y = segmentation[i+1] + (newCenterY - oldCenterY)

                modifiedSegmentation.append(x)
                modifiedSegmentation.append(y)

            modifiedSegmentations.append(modifiedSegmentation)

        self.segmentations = modifiedSegmentations

    def rotateSegmentations(self, degrees: int) -> None:
        rotatedSegmentations: List[List[float]] = []
        centerX, centerY = self.centroid()

        # because rotations with image and segmentations doesn't go in same direction
        # one of the rotations has to be inverted so they go in same direction
        theta = radians(-degrees) 
        cosang, sinang = cos(theta), sin(theta) 

        for segmentation in self.segmentations:
            rotatedSegmentation: List[float] = []

            for i in range(0, len(segmentation), 2):
                x = segmentation[i] - centerX
                y = segmentation[i + 1] - centerY

                newX = (x * cosang - y * sinang) + centerX
                newY = (x * sinang + y * cosang) + centerY

                rotatedSegmentation.append(newX)
                rotatedSegmentation.append(newY)

            rotatedSegmentations.append(rotatedSegmentation)

        self.segmentations = rotatedSegmentations


class CoretexImageAnnotation(Codable):

    name: str
    width: float
    height: float
    instances: List[CoretexSegmentationInstance]

    @classmethod
    def _keyDescriptors(cls) -> Dict[str, KeyDescriptor]:
        descriptors = super()._keyDescriptors()
        descriptors["instances"] = KeyDescriptor("instances", CoretexSegmentationInstance, list)

        return descriptors

    @staticmethod
    def create(
        name: str,
        width: float,
        height: float,
        instances: List[CoretexSegmentationInstance]
    ) -> CoretexImageAnnotation:
        obj = CoretexImageAnnotation()

        obj.name = name
        obj.width = width
        obj.height = height
        obj.instances = instances

        return obj

    def extractSegmentationMask(self, classes: ImageDatasetClasses) -> np.ndarray:
        reconstructed = np.zeros((int(self.height), int(self.width), 1), dtype="uint8")

        for instance in self.instances:
            labelId = classes.labelIdForClassId(instance.classId)
            if labelId is None:
                continue

            for segmentation in instance.segmentations:
                if len(segmentation) == 0:
                    raise ValueError(f">> [Coretex] Empty segmentation")

                mask = np.array(segmentation, dtype=np.int32).reshape((-1, 2))
                cv2.fillPoly(reconstructed, [mask], labelId + 1)

        return reconstructed

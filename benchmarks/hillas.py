import numpy as np
from astropy import units as u
from astropy.coordinates import EarthLocation
from ctapipe.coordinates import CameraFrame, TelescopeFrame
from ctapipe.image import hillas_parameters
from ctapipe.image.cleaning import TailcutsImageCleaner
from ctapipe.visualization import CameraDisplay
from ctapipe.instrument import (
    CameraDescription,
    CameraGeometry,
    OpticsDescription,
    SubarrayDescription,
    TelescopeDescription,
)
from ctapipe.instrument.optics import ReflectorShape, SizeType
from ctapipe.io.toymodel import ToyEventSource


class HillasParameters:
    def setup(self):
        focal_length = 12 * u.m
        geometry = CameraGeometry.make_rectangular(npix_x=40, npix_y=40)
        geometry.frame = CameraFrame(focal_length=focal_length)
        telescope_geometry = geometry.transform_to(TelescopeFrame())

        optics = OpticsDescription(
            name="ToyOptics",
            size_type=SizeType.MST,
            n_mirrors=1,
            equivalent_focal_length=focal_length,
            effective_focal_length=focal_length,
            mirror_area=100 * u.m**2,
            n_mirror_tiles=1,
            reflector_shape=ReflectorShape.PARABOLIC,
        )
        camera = CameraDescription(geometry.name, geometry, readout=None)
        telescope = TelescopeDescription("ToyTelescope", optics, camera)
        subarray = SubarrayDescription(
            "ToySubarray",
            tel_positions={1: [0, 0, 0] * u.m},
            tel_descriptions={1: telescope},
            reference_location=EarthLocation.from_geodetic(0 * u.deg, 0 * u.deg),
        )

        n_images = 500
        source = ToyEventSource(
            subarray=subarray,
            max_events=2 * n_images,
            trigger_probability=1.0,
            rng=np.random.default_rng(0),
        )
        cleaner = TailcutsImageCleaner(subarray=subarray)
        self.cleaned_images = []
        for event in source:
            image = event.tel[1].dl1.image
            mask = cleaner(1, image)
            if mask.any():
                self.cleaned_images.append((telescope_geometry[mask], image[mask]))
            if len(self.cleaned_images) == n_images:
                break

        else:
            raise RuntimeError(f"Could not generate {n_images} usable toy images")

    def time_hillas_parameters(self):
        for geometry, image in self.cleaned_images:
            hillas_parameters(geometry, image)

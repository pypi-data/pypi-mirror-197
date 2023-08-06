import torch
from pyronn.ct_reconstruction.layers.projection_2d import FanProjection2D
from pyronn.ct_reconstruction.geometry.geometry import Geometry
from pyronn.ct_reconstruction.helpers.trajectories.circular_trajectory import circular_trajectory_2d
from pyronn.ct_reconstruction.helpers.filters.filters import ram_lak_2D
from pyronn.ct_reconstruction.helpers.filters.weights import parker_weights_2d
import numpy as np
from pydicom import dcmread
from helper import params_2_proj_matrix
from pathlib import Path
from motion_models_2d import MotionModel2D
from backprojector_fan import DifferentiableFanBeamBackprojector
from geometry import Geometry as Geometry_
from matplotlib import pyplot as plt
from scipy.linalg import null_space
from scipy.ndimage import zoom


device = torch.device('cuda')

### PARAMETERS ###
image_size = 512
image_spacing = 0.4883
image_origin = -0.5 * (image_size - 1.) * image_spacing
detector_size = 1024
detector_spacing = 0.5
detector_origin = -0.5 * (detector_size - 1.) * detector_spacing
num_projections = 360
dsi = 595.
dsd = 1085.6
short_scan = False

# image_size = 256
# image_spacing = 0.5
# image_origin = -0.5 * (image_size - 1.) * image_spacing
# detector_size = 512
# detector_spacing = 1.0
# detector_origin = -0.5 * (detector_size - 1.) * detector_spacing
# num_projections = 300
# dsi = 1000
# dsd = 2000
# short_scan = False


def forward(image, short_scan=False):
    projector = FanProjection2D()
    geometry = Geometry()
    if short_scan:
        angular_range = np.arctan(0.5 * detector_size * detector_spacing / dsd) + np.pi
    else:
        angular_range = 2 * np.pi
    geometry.init_from_parameters(volume_shape=(image_size, image_size), volume_spacing=(image_spacing, image_spacing),
                                  detector_shape=(detector_size,), detector_spacing=(detector_spacing,),
                                  number_of_projections=num_projections, angular_range=angular_range,
                                  trajectory=circular_trajectory_2d, source_isocenter_distance=dsi,
                                  source_detector_distance=dsd)
    filter = ram_lak_2D(detector_shape=(1, detector_size), detector_spacing=(1, detector_spacing),
                        number_of_projections=num_projections)
    filter = torch.unsqueeze(torch.from_numpy(filter), 0).to(device)

    if short_scan:
        geometry.detector_origin = (detector_origin,)
        parker = parker_weights_2d(geometry)
        parker = torch.unsqueeze(torch.from_numpy(parker), 0).to(device)

    with torch.no_grad():
        image = torch.FloatTensor(image).to(device)
        image = torch.unsqueeze(image, 0)
        sinogram = projector.forward(image, **geometry)
        # sinogram = torch.multiply(sinogram, 2)  # because detector spacing missing in pyronn projection multiplier
        filtered_sinogram = torch.fft.fft(sinogram, dim=-1)
        filtered_sinogram = torch.multiply(filtered_sinogram, filter)
        filtered_sinogram = torch.fft.ifft(filtered_sinogram, dim=-1).real
        filtered_sinogram = filtered_sinogram.contiguous()

        if short_scan:
            filtered_sinogram = torch.multiply(filtered_sinogram, parker)

    proj_matrix, _, _ = params_2_proj_matrix(np.linspace(0, angular_range, num_projections, endpoint=False),
                                             dsd * np.ones(num_projections), dsi * np.ones(num_projections),
                                             np.zeros(num_projections), np.zeros(num_projections), detector_spacing,
                                             -detector_origin / detector_spacing)

    return filtered_sinogram.cpu().numpy(), proj_matrix


def backward(filtered_sinogram, proj_matrix):
    projection_multiplier = dsd * 2 * detector_spacing * np.pi / (num_projections * dsi)
    geometry = Geometry_((image_size, image_size), (image_origin, image_origin), (image_spacing, image_spacing),
                         (detector_origin,), (detector_spacing,))

    proj_matrix = torch.from_numpy(proj_matrix)

    filtered_sinogram = torch.from_numpy(filtered_sinogram.copy())
    filtered_sinogram = filtered_sinogram.to(device)
    proj_matrix = proj_matrix.to(device)

    backprojector = DifferentiableFanBeamBackprojector.apply

    reco = backprojector(filtered_sinogram, proj_matrix, geometry)

    return reco.cpu().numpy()


def main():
    # folder = Path('/media/mareike/Elements/Data/LDCT-and-Projection-data/N024/12-23-2021-NA-NA-13377/1.000000-Full Dose Images-01203')
    # image = dcmread(folder / '1-10.dcm').pixel_array
    # image = image.astype(np.float64)

    image = np.load('/home/mareike/Code/moco/geometry_gradients/analytical_gradients_fan/data/image.npy').astype(np.float64)
    image = zoom(image, 4)

    sino, proj_matrix = forward(image, short_scan=short_scan)
    sino = np.squeeze(sino.astype(np.float64))

    plt.figure()
    plt.imshow(sino, cmap='gray')
    plt.axis('off')

    proj_matrix = np.moveaxis(proj_matrix, 0, 2)
    m = MotionModel2D('stepwise_rigid', num_projections=360, start_projection=0, step_length=150)
    proj_matrix_updated, motion_curves = m.eval(np.array([0.08, -3, 5]), proj_matrix, return_motion_curves=True)
    # m = MotionModel2D('spline_akima', num_projections=360, num_nodes=10)
    # node_values = np.zeros(30)
    # node_values[0::3] = 0.08 * (np.random.rand(10) - 0.5)
    # node_values[1::3] = 3 * (np.random.rand(10) - 0.5)
    # node_values[2::3] = 5 * (np.random.rand(10) - 0.5)
    # proj_matrix_updated, motion_curves = m.eval(node_values, proj_matrix, return_motion_curves=True)
    proj_matrix = np.moveaxis(proj_matrix_updated, 2, 0)

    reco = backward(sino, proj_matrix)

    out_x = np.zeros(num_projections)
    out_y = np.zeros(num_projections)
    for i in range(num_projections):
        mat = proj_matrix[i, :, :]
        test_h = null_space(mat)
        test = test_h[:2] / test_h[2]
        test2 = - 1. / (mat[0, 0] * mat[1, 1] - mat[0, 1] * mat[1, 0]) * np.array([mat[1, 1] * mat[0, 2] - mat[0, 1] * mat[1, 2], -mat[1, 0] * mat[0, 2] + mat[0, 0] * mat[1, 2]])
        out_x[i] = test[0]
        out_y[i] = test[1]

    plt.figure()
    plt.scatter(out_x, out_y, marker='.')
    plt.show()

    plt.figure()
    plt.subplot(131)
    plt.imshow(image, cmap='gray')
    plt.axis('off')
    plt.colorbar()

    plt.subplot(132)
    plt.imshow(reco, cmap='gray')
    plt.axis('off')
    plt.colorbar()

    plt.subplot(133)
    plt.imshow(image - reco, cmap='gray')
    plt.axis('off')
    plt.colorbar()

    plt.figure()
    plt.plot(motion_curves[0] * 180 / np.pi, label='r [deg]')
    plt.plot(motion_curves[1], label='tx [mm]')
    plt.plot(motion_curves[2], label='ty [mm]')
    plt.legend()

    plt.show()


if __name__ == '__main__':
    main()
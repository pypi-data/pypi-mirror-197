import torch
from pytorch3d.transforms import euler_angles_to_matrix
from torchcubicspline import natural_cubic_spline_coeffs, NaturalCubicSpline


class MotionModel3DTorch:
    def __init__(self, selection, **kwargs):
        ''' Creates a 3D cone-beam motion model.

        :param selection: string selecting one of the types below
        :param kwargs: selection specific additional arguments like number of projections/ number of spline nodes
        '''
        if selection == 'rigid_3d':
            assert 'num_projections' in kwargs.keys(), 'Please provide the num_projections argument for the motion model.'
            self.free_parameters_per_node = 6
            self.free_parameters = self.free_parameters_per_node * kwargs['num_projections']
            self.eval = self.rigid_3d
        elif selection == 'spline_cubic':
            assert 'num_nodes' in kwargs.keys(), 'Please provide the num_nodes argument for the motion model.'
            assert 'num_projections' in kwargs.keys(), 'Please provide the num_projections argument for the motion model.'
            self.free_parameters_per_node = 6
            self.free_parameters = self.free_parameters_per_node * kwargs['num_nodes']
            self.num_nodes = kwargs['num_nodes']
            self.eval = self.spline_cubic
            # nodes: a 1D numpy array of increasing values indicating at which projection indices the spline nodes are,
            # if None, then evenly spaced along the projections with both endpoints included
            if 'nodes' in kwargs.keys() and (kwargs['nodes'] is not None):
                self.nodes = torch.FloatTensor(kwargs['nodes'])
            else:
                self.nodes = torch.linspace(0, kwargs['num_projections'] - 1, steps=self.num_nodes)
            print(f'Cubic spline nodes: {self.nodes}')

    def rigid_3d(self, free_params, projection_matrices_input, do_zero_center=False):
        '''Computes out = P @ M for M being a 3d rigid transformation matrix

        :param free_params: params for M; (rx, ry, rz, tx, ty, tz) for each projection as 1D torch tensor of size
        6*num_projections
        :param projection_matrices_input: the best guess for good projection matrices as 3D torch tensor of size
        3x4xnum_projections
        :param do_zero_center: whether the values for each motion parameter are zero centered over the scan range
        :return: the motion adjusted projection matrices as 3D torch tensor of size 3x4xnum_projections
        '''
        num_projections = projection_matrices_input.shape[2]
        assert (free_params.shape[0] == self.free_parameters), 'Wrong input to motion model rigid_3d.'

        if do_zero_center:
            for i in range(6):
                free_params[i::6] = free_params[i::6] - torch.mean(free_params[i::6])

        euler_angles = torch.zeros((num_projections, 3), device=free_params.get_device())
        euler_angles[:, 0] = free_params[0::6]
        euler_angles[:, 1] = free_params[1::6]
        euler_angles[:, 2] = free_params[2::6]

        rotations = euler_angles_to_matrix(euler_angles, 'XYZ')
        rotations = torch.moveaxis(rotations, 0, 2)

        translations = torch.zeros((3, 1, num_projections), device=free_params.get_device())
        translations[0, 0, :] = free_params[3::6]
        translations[1, 0, :] = free_params[4::6]
        translations[2, 0, :] = free_params[5::6]

        lower_row = torch.zeros((1, 4, num_projections), device=free_params.get_device())
        lower_row[:, 3, :] = 1

        rigid_transform = torch.cat((torch.cat((rotations, translations), 1), lower_row), 0)
        # apply matrix multiplication along third dimension
        out = torch.einsum('ijn,jkn->ikn', projection_matrices_input, rigid_transform)

        return out

    def spline_cubic(self, free_params, projection_matrices_input, return_motion_curves=False, do_zero_center=False):
        ''' Models a 3d rigid motion trajectory as 6 individual akima splines for rx, ry, rz, tx, ty, tz

        :param free_params: params for spline nodes; (rx, ry, rz, tx, ty, tz) for each node as 1D torch tensor of size
        6*num_nodes
        :param projection_matrices_input: the best guess for good projection matrices as 3D torch tensor of size
        3x4xnum_projections
        :return: the motion adjusted projection matrices as 3D torch tensor of size 3x4xnum_projections
        '''
        num_projections = projection_matrices_input.shape[2]
        assert (free_params.shape[0] == self.free_parameters), 'Wrong input to motion model spline_akima.'
        self.nodes = self.nodes.to(free_params.get_device())

        rx = torch.unsqueeze(free_params[0::6], 1)
        ry = torch.unsqueeze(free_params[1::6], 1)
        rz = torch.unsqueeze(free_params[2::6], 1)
        tx = torch.unsqueeze(free_params[3::6], 1)
        ty = torch.unsqueeze(free_params[4::6], 1)
        tz = torch.unsqueeze(free_params[5::6], 1)
        motion_types = [rx, ry, rz, tx, ty, tz]
        # do the interpolation, one spline per parameter
        interpolated_values = torch.zeros((num_projections, 6), device=free_params.get_device())

        for i in range(6):
            coeffs = natural_cubic_spline_coeffs(self.nodes, motion_types[i])
            spline = NaturalCubicSpline(coeffs)
            evaluation_points = torch.arange(num_projections, device=free_params.get_device())
            interpolated_values[:, i] = torch.squeeze(spline.evaluate(evaluation_points))

        out = torch.zeros(num_projections * 6, device=free_params.get_device())
        out[0::6] = interpolated_values[:, 0]
        out[1::6] = interpolated_values[:, 1]
        out[2::6] = interpolated_values[:, 2]
        out[3::6] = interpolated_values[:, 3]
        out[4::6] = interpolated_values[:, 4]
        out[5::6] = interpolated_values[:, 5]

        motion_model_rigid = MotionModel3DTorch('rigid_3d', num_projections=num_projections)
        if return_motion_curves:
            return motion_model_rigid.eval(out, projection_matrices_input, do_zero_center=do_zero_center), \
                   (out[0::6], out[1::6], out[2::6], out[3::6], out[4::6], out[5::6])
        else:
            return motion_model_rigid.eval(out, projection_matrices_input, do_zero_center=do_zero_center)


if __name__ == '__main__':
    m = MotionModel3DTorch('spline_cubic', num_projections=360, num_nodes=5)
    proj_mats_updated, motion_curves = m.eval(torch.rand(5 * 6).to('cuda'), torch.rand(3, 4, 360).to('cuda'), True, True)

    import matplotlib.pyplot as plt
    plt.figure()
    for i in range(6):
        plt.plot(motion_curves[i].cpu().numpy())
    plt.show()
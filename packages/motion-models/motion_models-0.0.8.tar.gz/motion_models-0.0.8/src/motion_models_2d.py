import numpy as np
from scipy.interpolate import Akima1DInterpolator


class MotionModel2D:
    def __init__(self, selection, **kwargs):
        ''' Creates a 2D fan-beam motion model.

        :param selection: string selecting one of the types below
        :param kwargs: selection specific additional arguments like number of projections/ number of spline nodes
        '''
        if selection == 'rigid_2d':
            assert 'num_projections' in kwargs.keys(), 'Please provide the num_projections argument for the motion model.'
            self.free_parameters_per_node = 3
            self.free_parameters = self.free_parameters_per_node * kwargs['num_projections']
            self.eval = self.rigid_2d
        elif selection == 'spline_akima':
            assert 'num_nodes' in kwargs.keys(), 'Please provide the num_nodes argument for the motion model.'
            assert 'num_projections' in kwargs.keys(), 'Please provide the num_projections argument for the motion model.'
            self.free_parameters_per_node = 3
            self.free_parameters = self.free_parameters_per_node * kwargs['num_nodes']
            self.num_nodes = kwargs['num_nodes']
            self.eval = self.spline_akima
            # nodes: a 1D numpy array of increasing values indicating at which projection indices the spline nodes are,
            # if None, then evenly spaced along the projections with both endpoints included
            if 'nodes' in kwargs.keys() and (kwargs['nodes'] is not None):
                self.nodes = kwargs['nodes']
            else:
                self.nodes = np.linspace(0, kwargs['num_projections'] - 1, num=self.num_nodes, endpoint=True)
            print(f'Akima spline nodes: {self.nodes}')
        elif selection == 'stepwise_rigid':
            assert 'num_projections' in kwargs.keys(), 'Please provide the num_projections argument for the motion model.'
            assert 'start_projection' in kwargs.keys(), 'Please provide the projection index where the step starts.'
            assert 'step_length' in kwargs.keys(), 'Please provide the number of projection which the step lasts.'
            assert kwargs['start_projection'] + kwargs['step_length'] < kwargs['num_projections']
            self.free_parameters = 3
            self.start_projection = kwargs['start_projection']
            self.step_length = kwargs['step_length']
            self.eval = self.stepwise_rigid
        else:
            print('This model is not implemented.')

    def rigid_2d(self, free_params, projection_matrices_input, return_motion_curves=False):
        '''Computes out = P @ M for M being a 2d rigid transformation matrix

        :param free_params: params for M; (r, tx, ty) for each projection as 1D numpy array of size 3*num_projections
        :param projection_matrices_input: the best guess for good projection matrices as 3D numpy array of size
        2x3xnum_projections
        :return: the motion adjusted projection matrices as 3D numpy array of size 2x3xnum_projections
        '''
        num_projections = projection_matrices_input.shape[2]
        assert (free_params.shape[0] == self.free_parameters), 'Wrong input to motion model rigid_2d.'

        free_params = np.asarray(np.split(free_params, num_projections))
        rotations = np.zeros((2, 2, num_projections))
        rotations[0, 0, :] = np.cos(free_params[:, 0])
        rotations[0, 1, :] = -np.sin(free_params[:, 0])
        rotations[1, 0, :] = np.sin(free_params[:, 0])
        rotations[1, 1, :] = np.cos(free_params[:, 0])

        translations = np.zeros((2, 1, num_projections))
        translations[0, :, :] = free_params[:, 1]
        translations[1, :, :] = free_params[:, 2]

        # lower row of 0s and 1s to make a 4x4 transformation matrix
        lower_row = np.zeros((1, 3, num_projections))
        lower_row[:, 2, :] = 1

        rigid_transform = np.concatenate((np.concatenate((rotations, translations), 1), lower_row), 0)
        # apply matrix multiplication along third dimension
        out = np.einsum('ijn,jkn->ikn', projection_matrices_input, rigid_transform)

        if return_motion_curves:
            return out, (free_params[:, 0], free_params[:, 1], free_params[:, 2])
        else:
            return out

    def spline_akima(self, free_params, projection_matrices_input, return_motion_curves=False):
        ''' Models a 3d rigid motion trajectory as 3 individual akima splines for r, tx, ty

        :param free_params: params for the spline nodes; (r, tx, ty) for each node as 1D numpy array of size 3*num_nodes
        :param projection_matrices_input: the best guess for good projection matrices as 3D numpy array of size
        2x3xnum_projections
        :return: the motion adjusted projection matrices as 3D numpy array of size 2x3xnum_projections
        '''
        num_projections = projection_matrices_input.shape[2]
        assert (free_params.shape[0] == self.free_parameters), 'Wrong input to motion model spline_akima.'

        free_params = np.asarray(np.split(free_params, self.num_nodes))
        r = free_params[:, 0]
        tx = free_params[:, 1]
        ty = free_params[:, 2]
        motion_types = [r, tx, ty]
        # do the interpolation, one spline per parameter
        interpolated_values = np.zeros((num_projections, 3))
        for i in range(3):
            interpolator = Akima1DInterpolator(self.nodes, motion_types[i])
            evaluation_points = np.arange(num_projections)
            interpolated_values[:, i] = interpolator(evaluation_points, extrapolate=True)

        out = np.zeros(num_projections * 3)
        out[0::3] = interpolated_values[:, 0]
        out[1::3] = interpolated_values[:, 1]
        out[2::3] = interpolated_values[:, 2]

        motion_model_rigid = MotionModel2D('rigid_2d', num_projections=num_projections)
        if return_motion_curves:
            return motion_model_rigid.eval(out, projection_matrices_input), (out[0::3], out[1::3], out[2::3])
        else:
            return motion_model_rigid.eval(out, projection_matrices_input)

    def stepwise_rigid(self, free_params, projection_matrices_input, return_motion_curves=False):
        num_projections = projection_matrices_input.shape[2]
        assert (free_params.shape[0] == self.free_parameters), 'Wrong input to motion model stepwise_rigid.'
        interpolated_values = np.zeros((num_projections, 3))
        interpolated_values[:self.start_projection, :] = 0
        interpolated_values[self.start_projection + self.step_length:, :] = free_params
        if (self.start_projection + self.step_length) < num_projections:
            interpolated_values[self.start_projection:self.start_projection + self.step_length, 0] = np.linspace(0, free_params[0], num=self.step_length, endpoint=False)
            interpolated_values[self.start_projection:self.start_projection + self.step_length, 1] = np.linspace(0, free_params[1], num=self.step_length, endpoint=False)
            interpolated_values[self.start_projection:self.start_projection + self.step_length, 2] = np.linspace(0, free_params[2], num=self.step_length, endpoint=False)

        out = np.zeros(num_projections * 3)
        out[0::3] = interpolated_values[:, 0]
        out[1::3] = interpolated_values[:, 1]
        out[2::3] = interpolated_values[:, 2]

        motion_model_rigid = MotionModel2D('rigid_2d', num_projections=num_projections)
        if return_motion_curves:
            return motion_model_rigid.eval(out, projection_matrices_input), (out[0::3], out[1::3], out[2::3])
        else:
            return motion_model_rigid.eval(out, projection_matrices_input)

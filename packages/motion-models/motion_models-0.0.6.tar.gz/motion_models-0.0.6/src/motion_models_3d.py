import numpy as np
from scipy.spatial.transform import Rotation as R
from scipy.interpolate import Akima1DInterpolator
import matplotlib.pyplot as plt
from pathlib import Path


iteration = 0


class MotionModel3D:
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

        elif selection == 'translation_3d':
            assert 'num_projections' in kwargs.keys(), 'Please provide the num_projections argument for the motion model.'
            self.free_parameters_per_node = 3
            self.free_parameters = self.free_parameters_per_node * kwargs['num_projections']
            self.eval = self.translation_3d

        elif selection == 'translation_z':
            assert 'num_projections' in kwargs.keys(), 'Please provide the num_projections argument for the motion model.'
            self.free_parameters_per_node = 1
            self.free_parameters = self.free_parameters_per_node * kwargs['num_projections']
            self.eval = self.translation_z

        elif selection == 'spline_akima':
            assert 'num_nodes' in kwargs.keys(), 'Please provide the num_nodes argument for the motion model.'
            assert 'num_projections' in kwargs.keys(), 'Please provide the num_projections argument for the motion model.'
            self.free_parameters_per_node = 6
            self.free_parameters = self.free_parameters_per_node * kwargs['num_nodes']
            self.num_nodes = kwargs['num_nodes']
            self.eval = self.spline_akima
            self.eval_spline = self.eval_spline_akima
            # nodes: a 1D numpy array of increasing values indicating at which projection indices the spline nodes are,
            # if None, then evenly spaced along the projections with both endpoints included
            if 'nodes' in kwargs.keys() and (kwargs['nodes'] is not None):
                self.nodes = kwargs['nodes']
            else:
                self.nodes = np.linspace(0, kwargs['num_projections'] - 1, num=self.num_nodes, endpoint=True)
            print(f'Akima spline nodes: {self.nodes}')

        elif selection == 'spline_akima_adjustable_nodes':
            assert 'num_nodes' in kwargs.keys(), 'Please provide the num_nodes argument for the motion model.'
            assert 'num_projections' in kwargs.keys(), 'Please provide the num_projections argument for the motion model.'
            self.free_parameters_per_node = 7
            self.free_parameters = self.free_parameters_per_node * kwargs['num_nodes']  # for each node find the rigid transform and node position
            self.num_nodes = kwargs['num_nodes']
            self.eval = self.spline_akima_adjustable_nodes
            self.eval_spline = self.eval_spline_akima_adjustable_nodes

        elif selection == 'spline_akima_fixed_first_node':
            assert 'num_nodes' in kwargs.keys(), 'Please provide the num_nodes argument for the motion model.'
            assert 'num_projections' in kwargs.keys(), 'Please provide the num_projections argument for the motion model.'
            self.free_parameters_per_node = 6
            self.free_parameters = self.free_parameters_per_node * (kwargs['num_nodes'] - 1)
            self.num_nodes = kwargs['num_nodes']
            self.eval = self.spline_akima_fixed_first_node
            self.eval_spline = self.eval_spline_akima_fixed_first_node
            # nodes: a 1D numpy array of increasing values indicating at which projection indices the spline nodes are,
            # if None, then evenly spaced along the projections with both endpoints included
            if 'nodes' in kwargs.keys() and (kwargs['nodes'] is not None):
                assert 0 in list(kwargs['nodes']), 'If nodes are provided, they must include position 0 which is fixed.'
                self.nodes = kwargs['nodes']
            else:
                self.nodes = np.linspace(0, kwargs['num_projections'] - 1, num=self.num_nodes, endpoint=True)
            print(f'Akima spline nodes: {self.nodes}. Motion of node 0 is fixed.')

        elif selection == 'spline_akima_fixed_first_node_out_of_plane_only':
            assert 'num_nodes' in kwargs.keys(), 'Please provide the num_nodes argument for the motion model.'
            assert 'num_projections' in kwargs.keys(), 'Please provide the num_projections argument for the motion model.'
            self.free_parameters_per_node = 3
            self.free_parameters = self.free_parameters_per_node * (kwargs['num_nodes'] - 1)
            self.num_nodes = kwargs['num_nodes']
            self.eval = self.spline_akima_fixed_first_node_out_of_plane_only
            self.eval_spline = self.eval_spline_akima_fixed_first_node_out_of_plane_only
            # nodes: a 1D numpy array of increasing values indicating at which projection indices the spline nodes are,
            # if None, then evenly spaced along the projections with both endpoints included
            if 'nodes' in kwargs.keys() and (kwargs['nodes'] is not None):
                assert 0 in list(kwargs['nodes']), 'If nodes are provided, they must include position 0 which is fixed.'
                self.nodes = kwargs['nodes']
            else:
                self.nodes = np.linspace(0, kwargs['num_projections'] - 1, num=self.num_nodes, endpoint=True)
            print(f'Akima spline nodes: {self.nodes}. Motion of node 0 is fixed.')
            print('Optimizing only out-of-plane parameters.')

        elif selection == 'spline_akima_fixed_first_node_in_plane_only':
            assert 'num_nodes' in kwargs.keys(), 'Please provide the num_nodes argument for the motion model.'
            assert 'num_projections' in kwargs.keys(), 'Please provide the num_projections argument for the motion model.'
            self.free_parameters_per_node = 3
            self.free_parameters = self.free_parameters_per_node * (kwargs['num_nodes'] - 1)
            self.num_nodes = kwargs['num_nodes']
            self.eval = self.spline_akima_fixed_first_node_in_plane_only
            self.eval_spline = self.eval_spline_akima_fixed_first_node_in_plane_only
            # nodes: a 1D numpy array of increasing values indicating at which projection indices the spline nodes are,
            # if None, then evenly spaced along the projections with both endpoints included
            if 'nodes' in kwargs.keys() and (kwargs['nodes'] is not None):
                assert 0 in list(kwargs['nodes']), 'If nodes are provided, they must include position 0 which is fixed.'
                self.nodes = kwargs['nodes']
            else:
                self.nodes = np.linspace(0, kwargs['num_projections'] - 1, num=self.num_nodes, endpoint=True)
            print(f'Akima spline nodes: {self.nodes}. Motion of node 0 is fixed.')
            print('Optimizing only in-plane parameters.')
        else:
            print('This model is not implemented.')

    def rigid_3d(self, free_params, projection_matrices_input):
        '''Computes out = P @ M for M being a 3d rigid transformation matrix

        :param free_params: params for M; (rx, ry, rz, tx, ty, tz) for each projection as 1D numpy array of size 6*num_projections
        :param projection_matrices_input: the best guess for good projection matrices as 3D numpy array of size
        3x4xnum_projections
        :return: the motion adjusted projection matrices as 3D numpy array of size 3x4xnum_projections
        '''
        num_projections = projection_matrices_input.shape[2]
        assert (free_params.shape[0] == self.free_parameters), 'Wrong input to motion model rigid_3d.'

        free_params = np.asarray(np.split(free_params, num_projections))
        # compute rotation matrices from rx, ry, rz
        rotations = R.from_euler('xyz', free_params[:, :3].tolist(), degrees=True)
        rotations = np.moveaxis(rotations.as_matrix(), 0, 2)
        # reshape the translation vectors
        translations = np.expand_dims(np.swapaxes(free_params[:, 3:], 0, 1), 1)
        # lower row of 0s and 1s to make a 4x4 transformation matrix
        lower_row = np.zeros((1, 4, num_projections))
        lower_row[:, 3, :] = 1

        rigid_transform = np.concatenate((np.concatenate((rotations, translations), 1), lower_row), 0)
        # apply matrix multiplication along third dimension
        out = np.einsum('ijn,jkn->ikn', projection_matrices_input, rigid_transform)

        return out

    def translation_3d(self, free_params, projection_matrices_input):
        ''' Computes out = P @ M for M being a 3d translation matrix

        :param free_params: params for M; (tx, ty, tz) for each projection as 1D numpy array of size 3*num_projections
        :param projection_matrices_input: the best guess for good projection matrices as 3D numpy array of size
        3x4xnum_projections
        :return: the motion adjusted projection matrices as 3D numpy array of size 3x4xnum_projections
        '''
        num_projections = projection_matrices_input.shape[2]
        assert (free_params.shape[0] == self.free_parameters), 'Wrong input to motion model translation_3d.'

        rotation = np.eye(3)
        rotations = np.repeat(rotation[:, :, np.newaxis], num_projections, axis=2)
        free_params = np.asarray(np.split(free_params, num_projections))
        # reshape the translation vectors
        translations = np.expand_dims(np.swapaxes(free_params, 0, 1), 1)
        # lower row of 0s and 1s to make a 4x4 transformation matrix
        lower_row = np.zeros((1, 4, num_projections))
        lower_row[:, 3, :] = 1

        rigid_transform = np.concatenate((np.concatenate((rotations, translations), 1), lower_row), 0)
        # apply matrix multiplication along third dimension
        out = np.einsum('ijn,jkn->ikn', projection_matrices_input, rigid_transform)

        return out

    def translation_z(self, free_params, projection_matrices_input):
        ''' Computes out = P @ M for M modeling a translation in z direction

        :param free_params: params for M; tz for each projection as 1D numpy array of size num_projections
        :param projection_matrices_input: the best guess for good projection matrices as 3D numpy array of size
        3x4xnum_projections
        :return: the motion adjusted projection matrices as 3D numpy array of size 3x4xnum_projections
        '''
        num_projections = projection_matrices_input.shape[2]
        assert (free_params.shape[0] == self.free_parameters), 'Wrong input to motion model translation_z.'

        rotation = np.eye(3)
        rotations = np.repeat(rotation[:, :, np.newaxis], num_projections, axis=2)
        # reshape the translation vectors
        translations = np.zeros((3, 1, num_projections))
        translations[2, :, :] = free_params
        # lower row of 0s and 1s to make a 4x4 transformation matrix
        lower_row = np.zeros((1, 4, num_projections))
        lower_row[:, 3, :] = 1

        rigid_transform = np.concatenate((np.concatenate((rotations, translations), 1), lower_row), 0)
        # apply matrix multiplication along third dimension
        out = np.einsum('ijn,jkn->ikn', projection_matrices_input, rigid_transform)

        return out

    def spline_akima(self, free_params, projection_matrices_input, save_figs=False, save_dir=None):
        ''' Models a 3d rigid motion trajectory as 6 individual akima splines for rx, ry, rz, tx, ty, tz

        :param free_params: params for the spline nodes; (rx, ry, rz, tx, ty, tz) for each node as 1D numpy array of
        size 6*num_nodes
        :param projection_matrices_input: the best guess for good projection matrices as 3D numpy array of size
        3x4xnum_projections
        :param save_figs: whether or not a figure with the current splines should be saved
        :return: the motion adjusted projection matrices as 3D numpy array of size 3x4xnum_projections
        '''
        global iteration
        num_projections = projection_matrices_input.shape[2]
        assert (free_params.shape[0] == self.free_parameters), 'Wrong input to motion model spline_akima.'

        if save_dir is None:
            save_dir = Path.cwd() / 'spline_figures'
        else:
            save_dir = Path(save_dir) / 'spline_figures'
        save_dir.mkdir(parents=False, exist_ok=True)

        interpolated_values = self.eval_spline_akima(free_params, num_projections, save_dir, save_figs, iteration)

        iteration += 1

        out = np.zeros(num_projections * 6)
        out[0::6] = interpolated_values[:, 0]
        out[1::6] = interpolated_values[:, 1]
        out[2::6] = interpolated_values[:, 2]
        out[3::6] = interpolated_values[:, 3]
        out[4::6] = interpolated_values[:, 4]
        out[5::6] = interpolated_values[:, 5]

        motion_model_rigid = MotionModel3D('rigid_3d', num_projections=num_projections)
        return motion_model_rigid.eval(out, projection_matrices_input)

    def eval_spline_akima(self, free_params, num_projections, save_dir=None, save_figs=False, iteration=0):
        free_params = np.asarray(np.split(free_params, self.num_nodes))
        # compute rotation matrices from rx, ry, rz
        rx = free_params[:, 0]
        ry = free_params[:, 1]
        rz = free_params[:, 2]
        tx = free_params[:, 3]
        ty = free_params[:, 4]
        tz = free_params[:, 5]
        motion_types = [rx, ry, rz, tx, ty, tz]
        names = ['rx', 'ry', 'rz', 'tx', 'ty', 'tz']
        # do the interpolation, one spline per parameter rx, ry, rz, tx, ty, tz
        interpolated_values = np.zeros((num_projections, 6))
        if save_figs:
            plt.figure()
        for i in range(6):
            interpolator = Akima1DInterpolator(self.nodes, motion_types[i])
            evaluation_points = np.arange(num_projections)
            interpolated_values[:, i] = interpolator(evaluation_points, extrapolate=True)

            if save_figs:
                plt.plot(self.nodes, motion_types[i], 'x')
                plt.plot(evaluation_points, interpolated_values[:, i], label=names[i])
                plt.xlabel('Projection number')
                plt.ylabel('Interpolated spline value')
        if save_figs:
            plt.legend(loc='upper right')
            plt.savefig(save_dir / f'spline_iteration{iteration}')
            plt.close()
        return interpolated_values

    def spline_akima_adjustable_nodes(self, free_params, projection_matrices_input, save_figs=False, save_dir=None):
        global iteration
        num_projections = projection_matrices_input.shape[2]
        assert (free_params.shape[0] == self.free_parameters), 'Wrong input to motion model spline_akima.'

        if save_dir is None:
            save_dir = Path.cwd() / 'spline_figures'
        else:
            save_dir = Path(save_dir) / 'spline_figures'
        save_dir.mkdir(parents=False, exist_ok=True)

        interpolated_values = self.eval_spline_akima_adjustable_nodes(free_params, num_projections, save_dir,
                                                                      save_figs, iteration)

        iteration += 1

        out = np.zeros(num_projections * 6)
        out[0::6] = interpolated_values[:, 0]
        out[1::6] = interpolated_values[:, 1]
        out[2::6] = interpolated_values[:, 2]
        out[3::6] = interpolated_values[:, 3]
        out[4::6] = interpolated_values[:, 4]
        out[5::6] = interpolated_values[:, 5]

        motion_model_rigid = MotionModel3D('rigid_3d', num_projections=num_projections)
        return motion_model_rigid.eval(out, projection_matrices_input)

    def eval_spline_akima_adjustable_nodes(self, free_params, num_projections, save_dir=None, save_figs=False, iteration=0):
        free_params = np.asarray(np.split(free_params, self.num_nodes))
        # compute rotation matrices from rx, ry, rz
        rx = free_params[:, 0]
        ry = free_params[:, 1]
        rz = free_params[:, 2]
        tx = free_params[:, 3]
        ty = free_params[:, 4]
        tz = free_params[:, 5]
        pos = free_params[:, 6]
        pos = np.sort(pos)
        motion_types = [rx, ry, rz, tx, ty, tz]
        names = ['rx', 'ry', 'rz', 'tx', 'ty', 'tz']
        # do the interpolation, one spline per parameter rx, ry, rz, tx, ty, tz
        interpolated_values = np.zeros((num_projections, 6))
        if save_figs:
            plt.figure()
        for i in range(6):
            interpolator = Akima1DInterpolator(pos, motion_types[i])
            evaluation_points = np.arange(num_projections)
            interpolated_values[:, i] = interpolator(evaluation_points, extrapolate=True)

            if save_figs:
                plt.plot(pos, motion_types[i], 'x')
                plt.plot(evaluation_points, interpolated_values[:, i], label=names[i])
                plt.xlabel('Projection number')
                plt.ylabel('Interpolated spline value')
        if save_figs:
            plt.legend(loc='upper right')
            plt.savefig(save_dir / f'spline_iteration{iteration}')
            plt.close()
        return interpolated_values

    def spline_akima_fixed_first_node(self, free_params, projection_matrices_input, save_figs=False, save_dir=None):
        global iteration
        num_projections = projection_matrices_input.shape[2]
        assert (free_params.shape[0] == self.free_parameters), 'Wrong input to motion model spline_akima_fixed_first_node.'

        if save_dir is None:
            save_dir = Path.cwd() / 'spline_figures'
        else:
            save_dir = Path(save_dir) / 'spline_figures'
        save_dir.mkdir(parents=False, exist_ok=True)

        interpolated_values = self.eval_spline_akima_fixed_first_node(free_params, num_projections, save_dir, save_figs,
                                                                      iteration)

        iteration += 1

        out = np.zeros(num_projections * 6)
        out[0::6] = interpolated_values[:, 0]
        out[1::6] = interpolated_values[:, 1]
        out[2::6] = interpolated_values[:, 2]
        out[3::6] = interpolated_values[:, 3]
        out[4::6] = interpolated_values[:, 4]
        out[5::6] = interpolated_values[:, 5]

        motion_model_rigid = MotionModel3D('rigid_3d', num_projections=num_projections)
        return motion_model_rigid.eval(out, projection_matrices_input)

    def eval_spline_akima_fixed_first_node(self, free_params, num_projections, save_dir=None, save_figs=False, iteration=0):
        free_params = np.asarray(np.split(free_params, self.num_nodes - 1))
        # compute rotation matrices from rx, ry, rz
        # add a 0 for the first node in each parameter group
        rx = np.concatenate(([0.], free_params[:, 0]))
        ry = np.concatenate(([0.], free_params[:, 1]))
        rz = np.concatenate(([0.], free_params[:, 2]))
        tx = np.concatenate(([0.], free_params[:, 3]))
        ty = np.concatenate(([0.], free_params[:, 4]))
        tz = np.concatenate(([0.], free_params[:, 5]))
        motion_types = [rx, ry, rz, tx, ty, tz]
        names = ['rx', 'ry', 'rz', 'tx', 'ty', 'tz']
        # do the interpolation, one spline per parameter rx, ry, rz, tx, ty, tz
        interpolated_values = np.zeros((num_projections, 6))
        if save_figs:
            plt.figure(1)
            plt.figure(2)
        for i in range(6):
            interpolator = Akima1DInterpolator(self.nodes, motion_types[i])
            evaluation_points = np.arange(num_projections)
            interpolated_values[:, i] = interpolator(evaluation_points, extrapolate=True)

            if save_figs:
                if i < 3:
                    plt.figure(1)
                    plt.plot(self.nodes, motion_types[i], 'x', color='black')
                    plt.plot(evaluation_points, interpolated_values[:, i], label=names[i])
                    plt.xlabel('Projection number')
                    plt.ylabel('Rotation [deg]')
                elif i >= 3:
                    plt.figure(2)
                    plt.plot(self.nodes, motion_types[i], 'x', color='black')
                    plt.plot(evaluation_points, interpolated_values[:, i], label=names[i])
                    plt.xlabel('Projection number')
                    plt.ylabel('Translation [mm]')
        if save_figs:
            plt.figure(1)
            plt.legend(loc='upper right')
            plt.savefig(save_dir / f'spline_rotation_iteration{iteration}')
            plt.close()
            plt.figure(2)
            plt.legend(loc='upper right')
            plt.savefig(save_dir / f'spline_translation_iteration{iteration}')
            plt.close()
        return interpolated_values

    def spline_akima_fixed_first_node_out_of_plane_only(self, free_params, projection_matrices_input, save_figs=False, save_dir=None):
        global iteration
        num_projections = projection_matrices_input.shape[2]
        assert (free_params.shape[0] == self.free_parameters), 'Wrong input to motion model spline_akima_fixed_first_node.'

        if save_dir is None:
            save_dir = Path.cwd() / 'spline_figures'
        else:
            save_dir = Path(save_dir) / 'spline_figures'
        save_dir.mkdir(parents=False, exist_ok=True)

        interpolated_values = self.eval_spline_akima_fixed_first_node_out_of_plane_only(free_params, num_projections,
                                                                                        save_dir, save_figs, iteration)

        iteration += 1

        out = np.zeros(num_projections * 6)
        out[0::6] = interpolated_values[:, 0]
        out[1::6] = interpolated_values[:, 1]
        out[2::6] = interpolated_values[:, 2]
        out[3::6] = interpolated_values[:, 3]
        out[4::6] = interpolated_values[:, 4]
        out[5::6] = interpolated_values[:, 5]

        motion_model_rigid = MotionModel3D('rigid_3d', num_projections=num_projections)
        return motion_model_rigid.eval(out, projection_matrices_input)

    def eval_spline_akima_fixed_first_node_out_of_plane_only(self, free_params, num_projections, save_dir=None, save_figs=False, iteration=0):
        free_params = np.asarray(np.split(free_params, self.num_nodes - 1))
        # compute rotation matrices from rx, ry, rz
        # add a 0 for the first node in each parameter group
        # add zeros for all in plane parameters which are not optimized in this motion model
        rx = np.concatenate(([0.], free_params[:, 0]))
        ry = np.concatenate(([0.], free_params[:, 1]))
        rz = np.zeros(self.num_nodes)
        tx = np.zeros(self.num_nodes)
        ty = np.zeros(self.num_nodes)
        tz = np.concatenate(([0.], free_params[:, 2]))
        motion_types = [rx, ry, rz, tx, ty, tz]
        names = ['rx', 'ry', 'rz', 'tx', 'ty', 'tz']
        # do the interpolation, one spline per parameter rx, ry, rz, tx, ty, tz
        interpolated_values = np.zeros((num_projections, 6))
        if save_figs:
            plt.figure(1)
            plt.figure(2)
        for i in range(6):
            interpolator = Akima1DInterpolator(self.nodes, motion_types[i])
            evaluation_points = np.arange(num_projections)
            interpolated_values[:, i] = interpolator(evaluation_points, extrapolate=True)

            if save_figs:
                if i < 3:
                    plt.figure(1)
                    plt.plot(self.nodes, motion_types[i], 'x', color='black')
                    plt.plot(evaluation_points, interpolated_values[:, i], label=names[i])
                    plt.xlabel('Projection number')
                    plt.ylabel('Rotation [deg]')
                elif i >= 3:
                    plt.figure(2)
                    plt.plot(self.nodes, motion_types[i], 'x', color='black')
                    plt.plot(evaluation_points, interpolated_values[:, i], label=names[i])
                    plt.xlabel('Projection number')
                    plt.ylabel('Translation [mm]')
        if save_figs:
            plt.figure(1)
            plt.legend(loc='upper right')
            plt.savefig(save_dir / f'spline_rotation_iteration{iteration}')
            plt.close()
            plt.figure(2)
            plt.legend(loc='upper right')
            plt.savefig(save_dir / f'spline_translation_iteration{iteration}')
            plt.close()
        return interpolated_values

    def spline_akima_fixed_first_node_in_plane_only(self, free_params, projection_matrices_input, save_figs=False, save_dir=None):
        global iteration
        num_projections = projection_matrices_input.shape[2]
        assert (free_params.shape[0] == self.free_parameters), 'Wrong input to motion model spline_akima_fixed_first_node.'

        if save_dir is None:
            save_dir = Path.cwd() / 'spline_figures'
        else:
            save_dir = Path(save_dir) / 'spline_figures'
        save_dir.mkdir(parents=False, exist_ok=True)

        interpolated_values = self.eval_spline_akima_fixed_first_node_in_plane_only(free_params, num_projections,
                                                                                    save_dir, save_figs, iteration)

        iteration += 1

        out = np.zeros(num_projections * 6)
        out[0::6] = interpolated_values[:, 0]
        out[1::6] = interpolated_values[:, 1]
        out[2::6] = interpolated_values[:, 2]
        out[3::6] = interpolated_values[:, 3]
        out[4::6] = interpolated_values[:, 4]
        out[5::6] = interpolated_values[:, 5]

        motion_model_rigid = MotionModel3D('rigid_3d', num_projections=num_projections)
        return motion_model_rigid.eval(out, projection_matrices_input)

    def eval_spline_akima_fixed_first_node_in_plane_only(self, free_params, num_projections, save_dir=None, save_figs=False, iteration=0):
        free_params = np.asarray(np.split(free_params, self.num_nodes - 1))
        # compute rotation matrices from rx, ry, rz
        # add a 0 for the first node in each parameter group
        # add zeros for all out of plane parameters which are not optimized in this motion model
        rx = np.zeros(self.num_nodes)
        ry = np.zeros(self.num_nodes)
        rz = np.concatenate(([0.], free_params[:, 0]))
        tx = np.concatenate(([0.], free_params[:, 1]))
        ty = np.concatenate(([0.], free_params[:, 2]))
        tz = np.zeros(self.num_nodes)
        motion_types = [rx, ry, rz, tx, ty, tz]
        names = ['rx', 'ry', 'rz', 'tx', 'ty', 'tz']
        # do the interpolation, one spline per parameter rx, ry, rz, tx, ty, tz
        interpolated_values = np.zeros((num_projections, 6))
        if save_figs:
            plt.figure(1)
            plt.figure(2)
        for i in range(6):
            interpolator = Akima1DInterpolator(self.nodes, motion_types[i])
            evaluation_points = np.arange(num_projections)
            interpolated_values[:, i] = interpolator(evaluation_points, extrapolate=True)

            if save_figs:
                if i < 3:
                    plt.figure(1)
                    plt.plot(self.nodes, motion_types[i], 'x', color='black')
                    plt.plot(evaluation_points, interpolated_values[:, i], label=names[i])
                    plt.xlabel('Projection number')
                    plt.ylabel('Rotation [deg]')
                elif i >= 3:
                    plt.figure(2)
                    plt.plot(self.nodes, motion_types[i], 'x', color='black')
                    plt.plot(evaluation_points, interpolated_values[:, i], label=names[i])
                    plt.xlabel('Projection number')
                    plt.ylabel('Translation [mm]')
        if save_figs:
            plt.figure(1)
            plt.legend(loc='upper right')
            plt.savefig(save_dir / f'spline_rotation_iteration{iteration}')
            plt.close()
            plt.figure(2)
            plt.legend(loc='upper right')
            plt.savefig(save_dir / f'spline_translation_iteration{iteration}')
            plt.close()
        return interpolated_values


if __name__ == '__main__':
    m = MotionModel3D('rigid_3d', num_projections=360)
    proj_mats_updated = m.eval(np.random.rand(360 * 6), np.random.rand(3, 4, 360))
    print('bla')
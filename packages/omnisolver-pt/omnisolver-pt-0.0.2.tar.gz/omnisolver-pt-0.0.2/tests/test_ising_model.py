import itertools

import numpy as np
import pytest

from omnisolver.pt.model import ising_model


class TestIsingModel:
    @pytest.mark.parametrize(
        "h_vec, j_mat",
        [
            (
                # Correct shapes individually, but biases don't maatch couplers
                np.array([0.2, 0.3, 0.4]),
                np.array([[-0.5, 1.2], [-2.3, 4.5]]),
            ),
            (
                # Biases have incorrect shape
                np.array([[1.0, 2.0], [3.0, 4.5]]),
                np.array([[-0.5, 1.2], [-2.3, 4.5]]),
            ),
            (
                # Couplings have incorrect shape
                np.array([0.2, 0.3, 0.4]),
                np.array([0.2, 0.3, 0.4]),
            ),
        ],
    )
    def test_cannot_be_initialized_with_arrays_of_incorrect_shape(self, h_vec, j_mat):
        with pytest.raises(ValueError):
            ising_model(h_vec, j_mat)

    @pytest.mark.parametrize(
        "h_vec, j_mat",
        [
            (
                np.array([0.5, -1.3], dtype=np.float32),
                np.array([[0.0, -2.3], [-2.3, 0.0]], dtype=np.float64),
            )
        ],
    )
    def test_cannot_be_initialized_with_arrays_of_different_dtypes(self, h_vec, j_mat):
        with pytest.raises(ValueError):
            ising_model(h_vec, j_mat)

    @pytest.mark.parametrize(
        "h_vec, j_mat",
        [
            (
                np.array([0.5, 0.25, -1.0]),
                np.array([[0.0, 0.3, 0.2], [0.3, 0.0, -2.5], [0.2, -2.5, 0.0]]),
            ),
            (
                np.array([0.5, 0.25, -1.0], dtype=np.float32),
                np.array([[0.0, 0.3, 0.2], [0.3, 0.0, -2.5], [0.2, -2.5, 0.0]], np.float32),
            ),
        ],
    )
    def test_retains_components_it_was_initialized_with(self, h_vec, j_mat):
        model = ising_model(h_vec, j_mat)

        np.testing.assert_array_equal(model.h_vec, h_vec)
        np.testing.assert_array_equal(model.j_mat, j_mat)

    @pytest.mark.parametrize(
        "h_vec, j_mat, expected_adjacency_list, expected_neighbours_count",
        [
            (
                np.array([0.5, 1.2, 0.3, -1.2, 3.0]),
                np.array(
                    [
                        [0.0, 0.0, 1.0, 0.0, 0.0],
                        [0.0, 0.0, -2.0, 0.0, 0.0],
                        [1.0, -2.0, 0.0, 0.0, 0.0],
                        [0.0, 0.0, 0.0, 0.0, 0.5],
                        [0.0, 0.0, 0.0, 0.5, 0.0],
                    ]
                ),
                np.array([[2, 0], [2, 0], [0, 1], [4, 0], [3, 0]]),
                np.array([1, 1, 2, 1, 1]),
            )
        ],
    )
    def test_stores_correct_adjacency_list_and_neighbours_count_for_each_spin(
        self, h_vec, j_mat, expected_adjacency_list, expected_neighbours_count
    ):
        model = ising_model(h_vec, j_mat)

        np.testing.assert_array_equal(model.adjacency_list, expected_adjacency_list)
        np.testing.assert_array_equal(model.neighbours_count, expected_neighbours_count)

    @pytest.mark.parametrize(
        "state, expected_energy",
        [
            (
                np.array([s0, s1, s2]),
                (s0 * 0.2 + s1 * 1.3 - s2 * 1.5 + s0 * s1 * 2.0 - s0 * s2 * 0.7 + s1 * s2 * 0.3),
            )
            for s0, s1, s2 in itertools.product([-1, 1], repeat=3)
        ],
    )
    def test_correctly_computes_energy_given_a_state(self, state, expected_energy):
        h_vec = np.array([0.2, 1.3, -1.5])
        j_mat = np.array([[0.0, 2.0, -0.7], [2.0, 0.0, 0.3], [-0.7, 0.3, 0.0]])

        model = ising_model(h_vec, j_mat)

        np.testing.assert_almost_equal(model.energy(state), expected_energy)

    @pytest.mark.parametrize(
        "state, position",
        [
            (np.array([s0, s1, s2]), position)
            for s0, s1, s2 in itertools.product([-1, 1], repeat=3)
            for position in (0, 1, 2)
        ],
    )
    def test_correctly_computes_energy_difference_obtained_by_flipping_one_spin(
        self, state, position
    ):
        h_vec = np.array([0.2, 1.3, -1.5])
        j_mat = np.array([[0.0, 2.0, -0.7], [2.0, 0.0, 0.3], [-0.7, 0.3, 0.0]])

        model = ising_model(h_vec, j_mat)
        flipped_state = state.copy()
        flipped_state[position] = -flipped_state[position]

        np.testing.assert_almost_equal(
            model.energy_diff(state, position),
            model.energy(state) - model.energy(flipped_state),
        )

    @pytest.mark.parametrize("dtype", [np.float32, np.float64])
    def test_models_with_equal_couplings_biases_and_dtypes_are_considered_equal(self, dtype):
        h_vec = np.array([-0.25, 1.2], dtype=dtype)
        j_mat = np.array([[0.0, -0.5], [-0.5, 0.0]], dtype=dtype)

        model_1 = ising_model(h_vec, j_mat)
        model_2 = ising_model(h_vec, j_mat)

        assert model_1.is_equal(model_2)
        assert model_2.is_equal(model_1)

    @pytest.mark.parametrize(
        "model_1, model_2",
        [
            # Mismatched biases
            (
                ising_model(np.array([-0.25, 1.2]), np.array([[0.0, -0.5], [-0.5, 0.0]])),
                ising_model(np.array([-0.25, 1.0]), np.array([[0.0, -0.5], [-0.5, 0.0]])),
            ),
            # Mismatched couplings
            (
                ising_model(np.array([-0.25, 1.2]), np.array([[0.0, -0.5], [-0.5, 0.0]])),
                ising_model(np.array([-0.25, 1.2]), np.array([[0.0, -0.3], [-0.3, 0.0]])),
            ),
            # Matching values, different dtypes
            (
                ising_model(np.array([-0.25, 1.2]), np.array([[0.0, -0.5], [-0.5, 0.0]])),
                ising_model(
                    np.array([-0.25, 1.2], dtype=np.float32),
                    np.array([[0.0, -0.5], [-0.5, 0.0]], dtype=np.float32),
                ),
            ),
        ],
    )
    def test_models_are_unequal_if_values_of_coefficients_or_dtypes_differs(self, model_1, model_2):
        assert not model_1.is_equal(model_2)
        assert not model_2.is_equal(model_1)

    def test_creating_multiple_models_with_same_dtypes_reuses_existing_class(self):
        h_vec = np.array([0.2, 1.3, -1.5])
        j_mat = np.array([[0.0, 2.0, -0.7], [2.0, 0.0, 0.3], [-0.7, 0.3, 0.0]])

        model_1 = ising_model(h_vec, j_mat)
        model_2 = ising_model(h_vec, j_mat)

        assert type(model_1) == type(model_2)

    def test_number_of_spins_in_model_is_correctly_inferred_based_on_its_coefficients_shape(
        self,
    ):
        h_vec = np.array([0.2, 1.3, -1.5])
        j_mat = np.array([[0.0, -2.0, -0.7], [-2.0, 0.0, 0.3], [-0.7, 0.3, 0.0]])

        model = ising_model(h_vec, j_mat)

        assert model.num_spins == 3

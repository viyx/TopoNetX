"""Test cell complex class."""

import unittest

import networkx as nx
import numpy as np

from toponetx.classes.cell import Cell
from toponetx.classes.cell_complex import CellComplex


class TestCellComplex(unittest.TestCase):
    def test_init_empty_cell_complex(self):
        """Test empty cell complex."""
        CX = CellComplex()
        assert len(CX.cells) == 0
        assert len(CX.nodes) == 0
        assert len(CX.edges) == 0
        self.assertEqual(CX.dim, 0)
        assert CX.is_regular

    def test_init_cell_complex_with_list_of_cells(self):
        """Test cell complex with cells."""
        c1 = Cell([1, 2, 3])
        c2 = Cell([1, 2, 3, 4])
        CX = CellComplex([c1, c2])
        assert c1 in CX.cells
        assert c2 in CX.cells
        self.assertEqual(CX.dim, 2)

        c1 = Cell((1, 2, 3))
        c2 = Cell((1, 2, 3, 4))
        CX = CellComplex([c1, c2])
        assert len(CX.cells) == 2
        assert len(CX.nodes) == 4
        assert len(CX.edges) == 5

    def test_nodes_and_edges(self):
        """Test cell complex with cells."""
        c1 = Cell([1, 3, 4])
        c2 = Cell([2, 3, 4])
        CX = CellComplex([c1, c2])
        assert set(CX.nodes) == {1, 2, 3, 4}
        assert set(CX.edges) == {(1, 3), (1, 4), (3, 2), (3, 4), (4, 2)}

    def test_init_networkx_graph(self):
        """Test cell complex with networkx graph as input."""
        gr = nx.Graph()
        gr.add_edge(1, 0)
        gr.add_edge(2, 0)
        gr.add_edge(1, 2)
        CX = CellComplex(gr)
        self.assertEqual(CX.dim, 1)
        assert len(CX.cells) == 0
        assert len(CX.nodes) == 3
        assert len(CX.edges) == 3

    def test_is_regular(self):
        """Test is_regular property."""
        # Test non-regular cell complex
        # allows for constructions of non-regular cells
        CX = CellComplex(regular=False)
        # the "is_regular" method checks if any non-regular cells are added
        self.assertEqual(CX.is_regular, True)
        self.assertEqual(CX.dim, 0)

        # test non-regular cell complex
        CX = CellComplex(regular=False)
        CX.add_cell([1, 2, 3, 4], rank=2)
        CX.add_cell([2, 3, 4, 5, 2, 3, 4, 5], rank=2)  # non-regular 2-cell
        c1 = Cell((1, 2, 3, 4, 5, 1, 2, 3, 4, 5), regular=False)
        CX.add_cell(c1)
        CX.add_cell([5, 6, 7, 8], rank=2)

        assert CX.is_regular is False

    def test_add_cell(self):
        """Test adding cells to a cell complex."""
        # Test adding a single cell
        CX = CellComplex()
        CX.add_cell([1, 2, 3, 4], rank=2)
        assert len(CX.cells) == 1

        # Test adding multiple cells
        CX = CellComplex()
        CX.add_cell([1, 2, 3, 4], rank=2)
        CX.add_cell([2, 3, 4, 5], rank=2)
        CX.add_cell([5, 6, 7, 8], rank=2)
        assert len(CX.cells) == 3

        # Test adding cells to CellComplex
        CX = CellComplex()
        CX.add_cell([1, 2, 3], rank=2)
        CX.add_cell([2, 3, 4, 5], rank=2)
        CX.add_cell([5, 6, 7, 8], rank=2)
        assert len(CX.cells) == 3
        assert len(CX.nodes) == 8
        assert len(CX.edges) == 10

    def test_add_cells_from(self):
        """Test adding cells from a list of cells or cell lists."""
        # Test adding cells from a list of cells
        CX = CellComplex()
        cells = [Cell((1, 2, 3, 4)), Cell((2, 3, 4, 5))]
        CX.add_cells_from(cells)
        assert len(CX.cells) == 2

        # Test adding cells from a list of cell lists
        CX = CellComplex()
        cell_lists = [[1, 2, 3, 4], [2, 3, 4, 5]]
        CX.add_cells_from(cell_lists, rank=2)
        assert len(CX.cells) == 2

        # Test adding cells from a list of lists
        CX = CellComplex()
        CX.add_cells_from([[1, 2, 4], [1, 2, 7]], rank=2)
        assert len(CX.cells) == 2
        assert len(CX.nodes) == 4
        assert len(CX.edges) == 5

        # Test adding multiple cells to an empty cell complex
        CX = CellComplex()
        CX.add_cells_from([[1, 2, 3], [2, 3, 4]], rank=2)

        # Test adding multiple cells with duplicate vertices to a cell complex
        CX.add_cells_from([[1, 2, 3, 4], [2, 3, 4, 5]], rank=2)
        assert len(CX.cells) == 4

        # Test adding multiple cells with vertices that do not exist in the cell complex
        CX.add_cells_from([[4, 5, 6], [7, 8, 9]], rank=2)

        assert 6 in CX.nodes
        assert 9 in CX.nodes
        assert 8 in CX.nodes

    def test_add_cell_and_remove_cell(self):
        """Test removing one cell and several cells from a cell complex."""
        CX = CellComplex()
        CX.add_cell([1, 2, 3, 4], rank=2)
        CX.remove_cell([1, 2, 3, 4])
        assert len(CX.cells) == 0

        CX = CellComplex()
        CX.add_cell([1, 2, 3, 4], rank=2)
        CX.add_cell([2, 3, 4, 5], rank=2)
        CX.add_cell([5, 6, 7, 8], rank=2)
        CX.remove_cell([1, 2, 3, 4])
        CX.remove_cell([2, 3, 4, 5])
        assert len(CX.cells) == 1

        CX = CellComplex()
        CX.add_cell([1, 2, 3], rank=2)
        CX.add_cell([2, 3, 4, 5], rank=2)
        CX.add_cell([5, 6, 7, 8], rank=2)
        CX.remove_cell([2, 3, 4, 5])
        assert len(CX.cells) == 2
        assert len(CX.nodes) == 8
        assert len(CX.edges) == 10

    def test_incidence_matrix_shape(self):
        """Test the shape of the incidence matrix for the cell complex."""
        CX = CellComplex()
        CX.add_cells_from([[1, 2, 3, 4], [2, 3, 4, 5], [5, 6, 7, 8]], rank=2)
        B = CX.incidence_matrix(2)
        assert B.shape == (10, 3)
        B = CX.incidence_matrix(1)
        assert B.shape == (8, 10)

    def test_incidence_matrix_empty_cell_complex(self):
        """Test the incidence matrix for an empty cell complex."""
        CX = CellComplex()
        np.testing.assert_array_equal(
            CX.incidence_matrix(2).toarray(), np.zeros((0, 0))
        )

    def test_incidence_matrix_cell_complex_with_one_cell(self):
        """Test the incidence matrix for a cell complex with only one cell."""
        CX = CellComplex()
        CX.add_cell([1, 2, 3], rank=2)
        np.testing.assert_array_equal(
            CX.incidence_matrix(2).toarray(), np.array([[1, -1, 1]]).T
        )

    def test_incidence_matrix_cell_complex_with_multiple_cells(self):
        """Test the incidence matrix for a cell complex with multiple cells."""
        # Test cell complex with multiple cells
        CX = CellComplex()
        CX.add_cell([2, 3, 4], rank=2)
        CX.add_cell([1, 3, 4], rank=2)
        np.testing.assert_array_equal(
            CX.incidence_matrix(rank=2).toarray(),
            np.array([[0, 0, 1, -1, 1], [1, -1, 0, 0, 1]]).T,
        )

        # Test non-regular cell complex
        CX = CellComplex(regular=False)
        CX.add_cell([1, 2, 3], rank=2)
        CX.add_cell([2, 3, 4], rank=2)
        np.testing.assert_array_equal(
            CX.incidence_matrix(rank=2).toarray(),
            np.array([[1, -1, 1, 0, 0], [0, 0, 1, -1, 1]]).T,
        )

    def test_incidence_matrix_unsigned_and_signed(self):
        """Test incidence matrix for the cell complex."""
        CX = CellComplex()
        CX.add_cell([1, 2, 3], rank=2)
        CX.add_cell([2, 3, 4], rank=2)
        CX.add_cell([3, 4, 5], rank=2)

        # Test the incidence matrix for the full cell complex
        inc_2 = CX.incidence_matrix(rank=2, signed=False)
        assert inc_2.shape == (7, 3)
        assert (inc_2[:, 0].T.toarray()[0] == np.array([1, 1, 1, 0, 0, 0, 0])).all()
        assert (inc_2[:, 1].T.toarray()[0] == np.array([0, 0, 1, 1, 1, 0, 0])).all()
        assert (inc_2[:, 2].T.toarray()[0] == np.array([0, 0, 0, 0, 1, 1, 1])).all()

        # Test the incidence matrix for the full cell complex
        inc_1 = CX.incidence_matrix(rank=1, signed=False)
        assert inc_1.shape == (5, 7)
        assert (inc_1[:, 0].T.toarray()[0] == np.array([1, 1, 0, 0, 0])).all()
        assert (inc_1[:, 1].T.toarray()[0] == np.array([1, 0, 1, 0, 0])).all()
        assert (inc_1[:, 2].T.toarray()[0] == np.array([0, 1, 1, 0, 0])).all()

        inc_2_signed = CX.incidence_matrix(rank=2, signed=True)
        inc_1_signed = CX.incidence_matrix(rank=1, signed=True)

        # B1 * B2 == 0
        assert np.sum(inc_1_signed.dot(inc_2_signed).toarray()) == 0.0

        CX = CellComplex()
        inc_1 = CX.incidence_matrix(rank=1)
        assert inc_1.shape == (0, 0)

        CX = CellComplex()
        inc_2 = CX.incidence_matrix(rank=2)
        assert inc_2.shape == (0, 0)

    def test_clear(self):
        """Test the clear method of the cell complex."""
        CX = CellComplex()
        CX.add_cells_from([[1, 2, 3, 4], [5, 6, 7, 8]], rank=2)
        CX.clear()
        assert len(CX.cells) == 0

    def test_add_cell_with_color_feature(self):
        """Test adding a cell with a color feature."""
        CX = CellComplex()
        c1 = Cell((2, 3, 4), color="black")
        CX.add_cell(c1, weight=3)
        CX.add_cell([1, 2, 3, 4], rank=2, color="red")
        CX.add_cell([2, 3, 4, 5], rank=2, color="blue")
        CX.add_cell([5, 6, 7, 8], rank=2, color="green")

        assert CX.cells[(1, 2, 3, 4)]["color"] == "red"
        assert CX.cells[(2, 3, 4, 5)]["color"] == "blue"
        assert CX.cells[(5, 6, 7, 8)]["color"] == "green"

    def test_adjacency_matrix_empty_cell_complex(self):
        """Test adjacency matrix for an empty cell complex."""
        CX = CellComplex()
        np.testing.assert_array_equal(CX.adjacency_matrix(0), np.zeros((0, 0)))

    def test_adjacency_matrix_cell_complex_with_one_cell(self):
        """Test adjacency matrix for a cell complex with one cell."""
        CX = CellComplex()
        CX.add_cell([1, 2, 3], rank=2)
        A = np.array([[0.0, 1.0, 1.0], [1.0, 0.0, 1.0], [1.0, 1.0, 0.0]])
        np.testing.assert_array_equal(CX.adjacency_matrix(0).todense(), A)

    def test_adjacency_matrix_cell_complex_with_multiple_cell(self):
        """Test adjacency matrix for a cell complex with multiple cells."""
        CX = CellComplex()
        CX.add_cell([1, 2, 3], rank=2)
        CX.add_cell([2, 3, 4], rank=2)
        CX.add_cell([4, 5, 6], rank=2)
        A = np.array(
            [
                [0.0, 1.0, 1.0, 0.0, 0.0, 0.0],
                [1.0, 0.0, 1.0, 1.0, 0.0, 0.0],
                [1.0, 1.0, 0.0, 1.0, 0.0, 0.0],
                [0.0, 1.0, 1.0, 0.0, 1.0, 1.0],
                [0.0, 0.0, 0.0, 1.0, 0.0, 1.0],
                [0.0, 0.0, 0.0, 1.0, 1.0, 0.0],
            ]
        )
        np.testing.assert_array_equal(CX.adjacency_matrix(rank=0).toarray(), A)

    def test_up_laplacian_matrix_empty_cell_complex(self):
        """Test up laplacian matrix for an empty cell complex."""
        CX = CellComplex()
        np.testing.assert_array_equal(CX.up_laplacian_matrix(rank=0), np.zeros((0, 0)))

    def test_up_laplacian_matrix_and_incidence_matrix(self):
        CX = CellComplex()
        CX.add_cell([2, 3, 4], rank=2)
        CX.add_cell([1, 3, 4], rank=2)

        inc_1 = CX.incidence_matrix(rank=1)
        up_lap_0 = CX.up_laplacian_matrix(rank=0)
        expected = inc_1.dot(inc_1.T)
        np.testing.assert_array_equal(up_lap_0.toarray(), expected.toarray())

        inc_2 = CX.incidence_matrix(rank=2)
        up_lap_1 = CX.up_laplacian_matrix(rank=1)
        expected = inc_2.dot(inc_2.T)
        np.testing.assert_array_equal(up_lap_1.toarray(), expected.toarray())

    def test_down_laplacian_matrix_and_incidence_matrix(self):
        CX = CellComplex()
        CX.add_cell([2, 3, 4], rank=2)
        CX.add_cell([1, 3, 4], rank=2)

        inc_1 = CX.incidence_matrix(rank=1)
        down_lap_1 = CX.down_laplacian_matrix(rank=1)
        expected = (inc_1.T).dot(inc_1)
        np.testing.assert_array_equal(down_lap_1.toarray(), expected.toarray())

        inc_2 = CX.incidence_matrix(rank=2)
        down_lap_2 = CX.down_laplacian_matrix(rank=2)
        expected = (inc_2.T).dot(inc_2)
        np.testing.assert_array_equal(down_lap_2.toarray(), expected.toarray())

    def test_hodge_laplacian_and_up_down_laplacians(self):
        CX = CellComplex()
        CX.add_cell([2, 3, 4], rank=2)
        CX.add_cell([1, 3, 4], rank=2)

        up_lap_1 = CX.up_laplacian_matrix(rank=1)
        down_lap_1 = CX.down_laplacian_matrix(rank=1)
        hodge_lap_1 = CX.hodge_laplacian_matrix(rank=1)
        expected = up_lap_1 + down_lap_1
        np.testing.assert_array_equal(hodge_lap_1.toarray(), expected.toarray())


if __name__ == "__main__":
    unittest.main()

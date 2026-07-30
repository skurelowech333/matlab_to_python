# -*- coding: utf-8 -*-
"""
Created on Mon Jul 27 14:31:09 2026

@author: N05690
"""

import unittest
import numpy as np

from matlab_tests import (
    test_arithmetic,
    simple_test,
    test_for_loop,
    test_multiple_returns,
    test_strings,
    test_try_catch,
    test_while_loop,
    test_concatenation,
    test_conditional,
    test_break_continue,
    test_function_composition,
    test_expr_assign,
    test_counter_class,
    test_point_class,
    test_cell_arrays,
    test_nested_loops,
    test_switch,
    test_multiple_calls,
    test_lambda,
    test_logical_not,
    test_for_array,
    test_for_step,
)


class TestGeneratedPythonFromMatlab(unittest.TestCase):
    """Verify generated Python functions match known MATLAB outputs."""

    # --- Helper for floating-point comparisons -----------------------------

    def assertAlmostEqualWithTol(self, actual, expected,
                                 atol=1e-12, rtol=1e-9, msg=None):
        """Absolute + relative tolerance comparison."""
        delta = atol + abs(expected) * rtol
        self.assertAlmostEqual(actual, expected, delta=delta, msg=msg)

    # --- Tests derived from the Known Outputs table ------------------------

    def test_test_arithmetic(self):
        """
        MATLAB:
            test_arithmetic(1, 2) -> 2
        """
        result = test_arithmetic.test_arithmetic(1, 2)
        self.assertAlmostEqualWithTol(
            result, 2.0,
            msg=f"test_arithmetic(1, 2) returned {result}, expected 2.0",
        )

    def test_simple_test(self):
        """
        MATLAB:
            simple_test(3) -> 18.411
        """
        result = simple_test.simple_test(3)
        self.assertAlmostEqualWithTol(
            result, 18.141120008059868,
            msg=f"simple_test(3) returned {result}, expected 18.1411",
        )

    def test_test_for_loop(self):
        """
        MATLAB:
            test_for_loop(5) -> 15
        """
        result = test_for_loop.test_for_loop(5)
        self.assertAlmostEqualWithTol(
            result, 15.0,
            msg=f"test_for_loop(5) returned {result}, expected 15.0",
        )

    def test_test_multiple_returns(self):
        """
        MATLAB:
            [max_value, min_value, mean_value] = test_multiple_returns([0 1 2])
            max_value = 2
            min_value = 0
            mean_value = 1
        """
        result = test_multiple_returns.test_multiple_returns([0, 1, 2])

        # Allow tuple or list return
        self.assertIsInstance(
            result, (tuple, list),
            msg=f"Expected sequence from test_multiple_returns, got {type(result)}",
        )

        expected = (2.0, 0.0, 1.0)
        self.assertEqual(
            len(result), len(expected),
            msg=f"Expected {len(expected)} outputs, got {len(result)}",
        )

        for i, (actual, exp) in enumerate(zip(result, expected)):
            self.assertAlmostEqualWithTol(
                actual, exp,
                msg=f"Output index {i} was {actual}, expected {exp}",
            )
            
    def test_test_while_loop_zero_to_hundred(self):
        """
        MATLAB:
            test_while_loop(0, 100) -> 100
        """
        result = test_while_loop.test_while_loop(0, 100)
        self.assertAlmostEqual(
            result, 100.0, places=8,
            msg=f"test_while_loop(0, 100) returned {result}, expected 100.0",
        )
        
    def test_test_concatenation(self):
        """
        MATLAB:
            [C, D] = test_concatenation()

            C =
                 1     2     3     4     5     6

            D =
                 1     2     3
                 4     5     6
        """
        C, D = test_concatenation.test_concatenation()

        # Check types
        self.assertIsInstance(C, np.ndarray, msg="C is not a NumPy array")
        self.assertIsInstance(D, np.ndarray, msg="D is not a NumPy array")

        # Expected values
        expected_C = np.array([1, 2, 3, 4, 5, 6])
        expected_D = np.array([[1, 2, 3],
                               [4, 5, 6]])

        # Check shapes
        self.assertEqual(
            C.shape, expected_C.shape,
            msg=f"C shape {C.shape} != expected {expected_C.shape}",
        )
        self.assertEqual(
            D.shape, expected_D.shape,
            msg=f"D shape {D.shape} != expected {expected_D.shape}",
        )

        # Check values (exact integers, but allclose is fine)
        np.testing.assert_array_equal(
            C, expected_C,
            err_msg=f"C values {C} != expected {expected_C}",
        )
        np.testing.assert_array_equal(
            D, expected_D,
            err_msg=f"D values\n{D}\n!= expected\n{expected_D}",
        )
        

    def test_negative(self):
        category = test_conditional.test_conditional(-1)
        self.assertEqual(category, 'negative')

    def test_zero(self):
        category = test_conditional.test_conditional(0)
        self.assertEqual(category, 'zero')

    def test_small(self):
        category = test_conditional.test_conditional(5)
        self.assertEqual(category, 'small')

    def test_large(self):
        category = test_conditional.test_conditional(10)
        self.assertEqual(category, 'large')
        
    def test_all_branches(self):
        # 1) limit < 5: no continue, no break
        # i = 1,2,3,4 -> result = 1+2+3+4 = 10
        self.assertEqual(
            test_break_continue.test_break_continue(4),
            10,
            msg="limit=4 should sum 1..4 with no breaks/continues",
        )

        # 2) 5 <= limit < 10: continue at i==5, never break
        # i = 1,2,3,4,5,6,7 -> skip 5 -> 1+2+3+4+6+7 = 23
        self.assertEqual(
            test_break_continue.test_break_continue(7),
            23,
            msg="limit=7 should skip i=5 but not break",
        )

        # 3) limit >= 10: continue at i==5, break at i==10
        # i = 1..10, skip 5, break at 10 (10 not added):
        # 1+2+3+4+6+7+8+9 = 40
        self.assertEqual(
            test_break_continue.test_break_continue(10),
            40,
            msg="limit=10 should skip 5 and break before adding 10",
        )
        
    def test_test_function_composition(self):
        """
        MATLAB:
            test_for_loop(5) -> 15
        """
        result = test_function_composition.test_function_composition(2)
        self.assertAlmostEqualWithTol(
            result, 0.155312411720123,
            msg=f"test_function_composition(5) returned {result}, expected 0.155312411720123",
        )
        
    def test_test_expr_assign(self):
        """
        MATLAB:
            test_expr_assign() -> -1.5
        """
        result = test_expr_assign.test_expr_assign()
        self.assertAlmostEqualWithTol(
            result, -1.50,
            msg=f"test_expr_assign returned {result}, expected -1.5",
        )
        
    def test_initial_value(self):
        c = test_counter_class.Counter(5)
        self.assertEqual(c.Value, 5)

    def test_increment_default(self):
        # If you implement a default amount (like MATLAB), test it
        c = test_counter_class.Counter(0)
        c.increment(1)  # or c.increment() if you add default logic
        self.assertEqual(c.Value, 1)

    def test_increment_multiple_times(self):
        c = test_counter_class.Counter(10)
        c.increment(2)
        c.increment(3)
        self.assertEqual(c.Value, 15)

    def test_get_value_method(self):
        c = test_counter_class.Counter(7)
        v = c.getValue()
        self.assertEqual(v, 7)

    def test_increment_once(self):
        c = test_counter_class.Counter(10)
        c.increment(3)
        self.assertEqual(c.Value, 13)

    def test_increment_multiple_times(self):
        c = test_counter_class.Counter(0)
        c.increment(1)
        c.increment(2)
        c.increment(3)
        self.assertEqual(c.Value, 6)  # 1 + 2 + 3

    def test_get_value_after_operations(self):
        c = test_counter_class.Counter(2)
        c.increment(4)
        c.increment(1)
        v = c.getValue()
        self.assertEqual(v, 7)

    def test_multiple_instances_independent(self):
        c1 = test_counter_class.Counter(1)
        c2 = test_counter_class.Counter(100)

        c1.increment(4)   # 1 + 4 = 5
        c2.increment(10)  # 100 + 10 = 110

        self.assertEqual(c1.Value, 5)
        self.assertEqual(c2.Value, 110)

    def test_increment_negative_and_zero(self):
        c = test_counter_class.Counter(10)
        c.increment(0)     # no change
        c.increment(-3)    # 10 - 3 = 7
        self.assertEqual(c.Value, 7)

    def test_get_value_direct_property_match(self):
        c = test_counter_class.Counter(42)
        self.assertEqual(c.getValue(), c.Value)
        
    def test_constructor_and_properties(self):
        p = test_point_class.Point(3, 4)
        self.assertEqual(p.X, 3)
        self.assertEqual(p.Y, 4)

    def test_move(self):
        p = test_point_class.Point(0, 0)
        p.move(2, -1)
        self.assertEqual((p.X, p.Y), (2, -1))

    def test_distance(self):
        p = test_point_class.Point(3, 4)
        self.assertAlmostEqual(p.distanceToOrigin(), 5.0, places=12)

    def test_above_and_right(self):
        p = test_point_class.Point(1, 2)
        self.assertTrue(p.isAboveXAxis())
        self.assertTrue(p.isRightOfYAxis())
        
    def test_test_cell_arrays(self):
        """
        MATLAB:
            test_cell_arrays() -> 14
        """
        result = test_cell_arrays.test_cell_arrays()
        self.assertEqual(
            result, 14,
            msg=f"test_cell_arrays() returned {result}, expected 14",
        )

    # -----------------------------------------------------------------------
    # test_nested_loops
    # -----------------------------------------------------------------------

    def test_nested_loops(self):
        """
        MATLAB:
            test_nested_loops(3, 4) -> 60
            sum of i*j for i=1..3, j=1..4
        """
        result = test_nested_loops.test_nested_loops(3, 4)
        self.assertAlmostEqualWithTol(
            result, 60.0,
            msg=f"test_nested_loops(3, 4) returned {result}, expected 60",
        )

    # -----------------------------------------------------------------------
    # test_switch
    # -----------------------------------------------------------------------

    def test_switch_case1(self):
        result = test_switch.test_switch(1)
        self.assertEqual(result, 'addition')

    def test_switch_case3(self):
        result = test_switch.test_switch(3)
        self.assertEqual(result, 'multiplication')

    def test_switch_otherwise(self):
        result = test_switch.test_switch(99)
        self.assertEqual(result, 'unknown')

    # -----------------------------------------------------------------------
    # test_try_catch
    # -----------------------------------------------------------------------

    def test_try_catch_normal(self):
        """Division by non-zero returns the quotient."""
        result = test_try_catch.test_try_catch(10, 2)
        self.assertAlmostEqualWithTol(
            result, 5.0,
            msg=f"test_try_catch(10, 2) returned {result}, expected 5.0",
        )

    def test_try_catch_division_by_zero(self):
        """Division by zero triggers catch block and returns 0."""
        result = test_try_catch.test_try_catch(10, 0)
        self.assertEqual(
            result, 0,
            msg=f"test_try_catch(10, 0) returned {result}, expected 0",
        )

    # -----------------------------------------------------------------------
    # test_multiple_calls  (uses np.maximum / np.minimum)
    # -----------------------------------------------------------------------

    def test_multiple_calls(self):
        """
        MATLAB:
            test_multiple_calls(3, 1, 2)
            = max(3, max(1,2)) + min(3, min(1,2))
            = max(3,2) + min(3,1) = 3 + 1 = 4
        """
        result = test_multiple_calls.test_multiple_calls(3, 1, 2)
        self.assertAlmostEqualWithTol(
            result, 4.0,
            msg=f"test_multiple_calls(3, 1, 2) returned {result}, expected 4",
        )

    # -----------------------------------------------------------------------
    # test_lambda  (anonymous function / closure)
    # -----------------------------------------------------------------------

    def test_lambda_basic(self):
        """
        MATLAB:
            f = @(t) t * t + 1;
            test_lambda(3) -> 10
        """
        result = test_lambda.test_lambda(3)
        self.assertAlmostEqualWithTol(
            result, 10.0,
            msg=f"test_lambda(3) returned {result}, expected 10",
        )

    def test_lambda_zero(self):
        result = test_lambda.test_lambda(0)
        self.assertAlmostEqualWithTol(
            result, 1.0,
            msg=f"test_lambda(0) returned {result}, expected 1",
        )

    # -----------------------------------------------------------------------
    # test_logical_not  (unary ~ operator)
    # -----------------------------------------------------------------------

    def test_logical_not_below_threshold(self):
        """~(3 > 5) -> True -> 1"""
        result = test_logical_not.test_logical_not(3)
        self.assertEqual(
            result, 1,
            msg=f"test_logical_not(3) returned {result}, expected 1",
        )

    def test_logical_not_above_threshold(self):
        """~(10 > 5) -> False -> 0"""
        result = test_logical_not.test_logical_not(10)
        self.assertEqual(
            result, 0,
            msg=f"test_logical_not(10) returned {result}, expected 0",
        )

    # -----------------------------------------------------------------------
    # test_for_array  (for loop over a vector)
    # -----------------------------------------------------------------------

    def test_for_array_partial(self):
        """Sum elements of [1,3,5,7,9] that are <= 5 -> 1+3+5 = 9"""
        result = test_for_array.test_for_array(5)
        self.assertAlmostEqualWithTol(
            result, 9.0,
            msg=f"test_for_array(5) returned {result}, expected 9",
        )

    def test_for_array_all(self):
        """Sum all elements of [1,3,5,7,9] -> 25"""
        result = test_for_array.test_for_array(9)
        self.assertAlmostEqualWithTol(
            result, 25.0,
            msg=f"test_for_array(9) returned {result}, expected 25",
        )

    # -----------------------------------------------------------------------
    # test_for_step  (for loop with step value)
    # -----------------------------------------------------------------------

    def test_for_step_ten(self):
        """for i = 1:2:10 -> 1+3+5+7+9 = 25"""
        result = test_for_step.test_for_step(10)
        self.assertAlmostEqualWithTol(
            result, 25.0,
            msg=f"test_for_step(10) returned {result}, expected 25",
        )

    def test_for_step_five(self):
        """for i = 1:2:5 -> 1+3+5 = 9"""
        result = test_for_step.test_for_step(5)
        self.assertAlmostEqualWithTol(
            result, 9.0,
            msg=f"test_for_step(5) returned {result}, expected 9",
        )

if __name__ == "__main__":
    unittest.main()
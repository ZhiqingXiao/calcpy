import numpy as np
import pandas as pd

from calcpy import unique, concat, union, intersect, exclude, xor, eq, ne
from calcpy.matcher import PandasFrameMatcher


def test_all():
    in0_list = [8, 6, 4, 2, 0, 1, 3, 5, 6, 7]
    in1_list = [1, 3, 5, 7, 9, 8, 6, 4, 2]
    in2_list = [2, 6, 6, 3, 5, 5, 6, 7]
    lists = [in0_list, in1_list, in2_list]
    uni_list = [8, 6, 4, 2, 0, 1, 3, 5, 7]
    assert eq(unique(in0_list), uni_list)
    con_list = in0_list + in1_list + in2_list
    assert eq(concat(*lists), con_list)
    unn_list = [8, 6, 4, 2, 0, 1, 3, 5, 7, 9]
    assert eq(union(*lists), unn_list)
    int_list = [6, 2, 3, 5, 6, 7]
    assert eq(intersect(*lists), int_list)
    exc_list = [0]
    assert eq(exclude(*lists), exc_list)
    xor_list = [0, 9, 2, 6, 6, 3, 5, 5, 6, 7]
    assert eq(xor(*lists), xor_list)

    in0_tuple = tuple(in0_list)
    in1_tuple = tuple(in1_list)
    in2_tuple = tuple(in2_list)
    tuples = [in0_tuple, in1_tuple, in2_tuple]
    uni_tuple = tuple(uni_list)
    assert eq(unique(in0_tuple), uni_tuple)
    con_tuple = tuple(con_list)
    assert eq(concat(*tuples), con_tuple)
    unn_tuple = tuple(unn_list)
    assert eq(union(*tuples), unn_tuple)
    int_tuple = tuple(int_list)
    assert eq(intersect(*tuples), int_tuple)
    exc_tuple = tuple(exc_list)
    assert eq(exclude(*tuples), exc_tuple)
    xor_tuple = tuple(xor_list)
    assert eq(xor(*tuples), xor_tuple)

    in0_set = set(in0_list)
    in1_set = set(in1_list)
    in2_set = set(in2_list)
    sets = [in0_set, in1_set, in2_set]
    uni_set = set(uni_list)
    assert eq(unique(in0_set), uni_set)
    con_set = set(con_list)
    assert eq(concat(*sets), con_set)
    unn_set = set(unn_list)
    assert eq(union(*sets), unn_set)
    int_set = set(int_list)
    assert eq(intersect(*sets), int_set)
    exc_set = set(exc_list)
    assert eq(exclude(*sets), exc_set)
    xor_set = set(xor_list)
    assert eq(xor(*sets), xor_set)

    in0_arr = np.array(in0_list)
    in1_arr = np.array(in1_list)
    in2_arr = np.array(in2_list)
    arrs = [in0_arr, in1_arr, in2_arr]
    uni_arr = np.array(uni_list)
    assert eq(unique(in0_arr), uni_arr, matcher=np.array_equal)
    con_arr = np.array(con_list)
    assert eq(concat(*arrs), con_arr, matcher=np.array_equal)
    unn_arr = np.array(unn_list)
    assert eq(union(*arrs), unn_arr, matcher=np.array_equal)
    int_arr = np.array(int_list)
    assert eq(intersect(*arrs), int_arr, matcher=np.array_equal)
    exc_arr = np.array(exc_list)
    assert eq(exclude(*arrs), exc_arr, matcher=np.array_equal)
    xor_arr = np.array(xor_list)
    assert eq(xor(*arrs), xor_arr, matcher=np.array_equal)

    in0_s = pd.Series(in0_list, index=in0_list)
    in1_s = pd.Series(in1_list, index=in1_list)
    in2_s = pd.Series(in2_list, index=in2_list)
    ss = [in0_s, in1_s, in2_s]
    uni_s = pd.Series(uni_list, index=uni_list)
    assert eq(unique(in0_s), uni_s, matcher=PandasFrameMatcher())
    con_s = pd.Series(con_list, index=con_list)
    assert eq(concat(*ss), con_s, matcher=PandasFrameMatcher())
    unn_s = pd.Series(unn_list, index=unn_list)
    assert eq(union(*ss), unn_s, matcher=PandasFrameMatcher())
    int_s = pd.Series(int_list, index=int_list)
    assert eq(intersect(*ss), int_s, matcher=PandasFrameMatcher())
    exc_s = pd.Series(exc_list, index=exc_list)
    assert eq(exclude(*ss), exc_s, matcher=PandasFrameMatcher())
    xor_s = pd.Series(xor_list, index=xor_list)
    assert eq(xor(*ss), xor_s, matcher=PandasFrameMatcher())

    in0_df = in0_s.to_frame("V")
    in1_df = in1_s.to_frame("V")
    in2_df = in2_s.to_frame("V")
    dfs = [in0_df, in1_df, in2_df]
    uni_df = uni_s.to_frame("V")
    assert eq(unique(in0_df), uni_df, matcher=PandasFrameMatcher())
    con_df = con_s.to_frame("V")
    assert eq(concat(*dfs), con_df, matcher=PandasFrameMatcher())
    unn_df = unn_s.to_frame("V")
    assert eq(union(*dfs), unn_df, matcher=PandasFrameMatcher())
    int_df = int_s.to_frame("V")
    assert eq(intersect(*dfs), int_df, matcher=PandasFrameMatcher())
    exc_df = exc_s.to_frame("V")
    assert eq(exclude(*dfs), exc_df, matcher=PandasFrameMatcher())
    xor_df = xor_s.to_frame("V")
    assert eq(xor(*dfs), xor_df, matcher=PandasFrameMatcher())

    df1 = pd.DataFrame({"A": 1, "B": 2, "C": 3}, index=[0])
    df2 = pd.DataFrame({"A": 1, "B": 2, "C": 3}, index=[0])
    df3 = pd.DataFrame({"A": 1, "B": 2, "C": 3}, index=[0])
    assert len(unique([df1, df2, df3], matcher=PandasFrameMatcher())) == 1

    df1 = pd.DataFrame({"A": [1, 2, 3], "B": [3, 2, 3]}, index=["X", "Y", "Z"])
    df2 = pd.DataFrame({"C": [4, 5, 6], "D": [8, 5, 2]}, index=["U", "V", "X"])
    intersect(df1, df2, matcher=PandasFrameMatcher(method="index"))

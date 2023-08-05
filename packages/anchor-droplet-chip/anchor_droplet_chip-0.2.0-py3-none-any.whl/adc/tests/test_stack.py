import os
import shutil
import time
from glob import glob

import dask.array as da
import napari
import numpy as np
from pytest import fixture
from tifffile import imread

from adc._projection_stack import ProjectAlong
from adc._split_stack import SplitAlong
from adc._sub_stack import SubStack


@fixture
def test_stack():
    sizes = {"T": 30, "P": 10, "C": 3, "Z": 15, "Y": 256, "X": 256}
    tpcz_stack = np.zeros(tuple(sizes.values()), dtype="uint16")
    return {
        "data": tpcz_stack,
        "metadata": {
            "dask_data": da.from_array(tpcz_stack),
            "sizes": sizes,
            "pixel_size_um": 0.3,
        },
        "channel_axis": 2,
    }


def test_substack(test_stack):
    v = napari.Viewer()
    v.add_image(**test_stack)
    # v.add_image(
    #     tpcz_stack,
    #     channel_axis=2,
    #     metadata={
    #         "dask_data": da.from_array(tpcz_stack),
    #         "sizes":sizes,
    #         "pixel_size_um":.3
    #     }
    # )
    assert len(v.layers) == 3

    ss = SubStack(v)
    # v.window.add_dock_widget(ss)
    assert v.dims.axis_labels == tuple("TPZYX")  # C used for as channel axis

    ss.slice_container[3].start.value = 5
    ss.slice_container[3].stop.value = 10
    ss.make_new_layer()
    assert len(v.layers) == 6
    assert v.layers[3].data.shape == (30, 10, 5, 256, 256)
    assert v.layers[3].metadata["dask_data"].shape == (30, 10, 3, 5, 256, 256)

    ps = ProjectAlong(v)
    # v.window.add_dock_widget(ps)
    ps.axis_selector.value = "Z:15"
    ps.make_projection()
    assert len(v.layers) == 9
    assert v.layers[6].data.shape == (30, 10, 256, 256)
    assert v.layers[6].metadata["dask_data"].shape == (30, 10, 3, 256, 256)

    for i in v.layers[:6]:
        v.layers.remove(i)
    assert len(v.layers) == 3

    st = SplitAlong(v)
    # v.window.add_dock_widget(st)

    st.axis_selector.value = "P:10"
    st.split_data()
    assert len(st.data_list) == 10
    assert st.data_list[0].shape == (30, 3, 256, 256)
    try:
        os.mkdir(testdir_name := "test_split")
    except FileExistsError:
        shutil.rmtree(testdir_name)
        os.mkdir(testdir_name := "test_split")

    st.path_widget.value = (
        testdir := os.path.join(os.path.curdir, testdir_name)
    )
    try:
        st.start_export()
        time.sleep(12)
        st.worker.await_workers(msecs=5000)
        assert len(flist := glob(os.path.join(testdir, "*.tif"))) == 10
        assert imread(flist[0]).shape == (30, 3, 256, 256)
    except Exception as e:
        raise e
    finally:
        shutil.rmtree(testdir)

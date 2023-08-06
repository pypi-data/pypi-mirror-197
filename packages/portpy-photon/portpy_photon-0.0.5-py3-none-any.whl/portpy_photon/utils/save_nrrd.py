from __future__ import annotations
import SimpleITK as sitk
from pathlib import Path
import numpy as np
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from portpy_photon.plan import Plan


def save_nrrd(my_plan: Plan, sol: dict, data_dir: str = None) -> None:
    """
    save nrrd in the path directory else save in patient data directory

    :param my_plan: object of class Plan
    :param sol: optimal solution dict
    :param data_dir: save nrrd images of ct, dose_1d and structure set in path directory
    :return: save nrrd images in path
    """
    import os
    if data_dir is None:
        data_dir = os.path.join(Path(__file__).parents[2], 'data', my_plan.patient_id)
    ct_arr = my_plan.ct['ct_hu_3d'][0]
    ct = sitk.GetImageFromArray(ct_arr)
    ct.SetOrigin(my_plan.ct['origin_xyz_mm'])
    ct.SetSpacing(my_plan.ct['resolution_xyz_mm'])
    ct.SetDirection(my_plan.ct['direction'])
    sitk.WriteImage(ct, os.path.join(data_dir, 'ct.nrrd'))

    if sol['inf_matrix'].dose_3d is None:
        dose_1d = sol['inf_matrix'].A * sol['optimal_intensity']*my_plan.get_num_of_fractions()
        dose_arr = sol['inf_matrix'].dose_1d_to_3d(dose_1d=dose_1d)
    else:
        dose_arr = sol['inf_matrix'].dose_3d
    dose = sitk.GetImageFromArray(dose_arr)
    dose.SetOrigin(my_plan.ct['origin_xyz_mm'])
    dose.SetSpacing(my_plan.ct['resolution_xyz_mm'])
    dose.SetDirection(my_plan.ct['direction'])
    sitk.WriteImage(dose, os.path.join(data_dir, 'dose.nrrd'))

    labels = my_plan.structures.structures_dict['structure_mask_3d']
    mask_arr = np.array(labels).transpose((1, 2, 3, 0))
    mask = sitk.GetImageFromArray(mask_arr.astype('uint8'))
    # for i, struct_name in enumerate(my_plan.structures.structures_dict['name']):
    #     segment_name = "Segment{0}_Name".format(i)
    #     mask.SetMetaData(segment_name, struct_name)
    mask.SetOrigin(my_plan.ct['origin_xyz_mm'])
    mask.SetSpacing(my_plan.ct['resolution_xyz_mm'])
    mask.SetDirection(my_plan.ct['direction'])
    sitk.WriteImage(mask, os.path.join(data_dir, 'rtss.seg.nrrd'), True)
    # my_plan.visualize.patient_name = my_plan.patient_name

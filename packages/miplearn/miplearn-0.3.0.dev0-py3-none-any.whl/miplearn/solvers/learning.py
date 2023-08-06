#  MIPLearn: Extensible Framework for Learning-Enhanced Mixed-Integer Optimization
#  Copyright (C) 2020-2022, UChicago Argonne, LLC. All rights reserved.
#  Released under the modified BSD license. See COPYING.md for more details.
from os.path import exists
from typing import List, Any

from miplearn.h5 import H5File
from miplearn.io import load


class LearningSolver:
    def __init__(self, components: List[Any], skip_lp=False):
        self.components = components
        self.skip_lp = skip_lp

    def fit(self, train_filenames):
        train_h5 = [f.replace(".pkl.gz", ".h5") for f in train_filenames]
        for comp in self.components:
            comp.fit(train_h5)

    def optimize(self, data_filename, build_model):
        stats = {}
        h5_filename = data_filename.replace(".pkl.gz", ".h5")
        mode = "r+" if exists(h5_filename) else "w"
        with H5File(h5_filename, mode) as h5:
            model = load(data_filename, build_model)
            model.extract_after_load(h5)
            if not self.skip_lp:
                relaxed = model.relax()
                relaxed.optimize()
                relaxed.extract_after_lp(h5)
            for comp in self.components:
                comp.before_mip(h5_filename, model, stats)
            model.optimize()
            model.extract_after_mip(h5)

        model.optimize()
        return stats

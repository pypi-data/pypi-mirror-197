import os
import numpy as np
import IQM_Vis


def run():
    file_path = os.path.dirname(os.path.abspath(__file__))

    # metrics functions must return a single value
    metric = {'MAE': IQM_Vis.metrics.MAE,
              'MSE': IQM_Vis.metrics.MSE,
              '1-SSIM': IQM_Vis.metrics.ssim()}

    # metrics images return a numpy image
    metric_images = {'MSE': IQM_Vis.metrics.MSE_image,
                     'SSIM': IQM_Vis.metrics.SSIM_image()}

    # first row of images
    row_1 = IQM_Vis.data_holder(('X1', IQM_Vis.utils.load_image(os.path.join(file_path, 'images', 'wave3.jpeg'))),
                             ('X1', IQM_Vis.utils.load_image(os.path.join(file_path, 'images', 'wave3.jpeg'))),
                             metric,
                             metric_images)
    # second row of images
    row_2 = IQM_Vis.data_holder(('X1', IQM_Vis.utils.load_image(os.path.join(file_path, 'images', 'wave3.jpeg'))),
                            ('X2', IQM_Vis.utils.load_image(os.path.join(file_path, 'images', 'waves1.jpeg'))),
                             metric,
                             metric_images)
    # define the transformations
    transformations = {
               'rotation':{'min':-180, 'max':180, 'function':IQM_Vis.transforms.rotation},    # normal input
               'blur':{'min':1, 'max':41, 'normalise':'odd', 'function':IQM_Vis.transforms.blur},  # only odd ints
               'brightness':{'min':-1.0, 'max':1.0, 'function':IQM_Vis.transforms.brightness},   # normal but with float
               }

    # use the API to create the UI
    IQM_Vis.make_UI([row_1, row_2],
                transformations,
                metrics_avg_graph=True)


if __name__ == '__main__':
    run()

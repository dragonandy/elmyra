import bpy

from glob import glob
from natsort import natsorted
from os import makedirs, path
from subprocess import call
from time import strftime

from common import get_view3d_context


VISUALIZATIONS_PATH = path.join(path.dirname(__file__), "visualizations")


def all_versions(visualization):
    visualizations_directory = path.join(VISUALIZATIONS_PATH, visualization)
    versions = glob(path.join(visualizations_directory, "*"))

    return natsorted(versions)


def latest_version(visualization):
    return all_versions(visualization)[-1]


def open_latest(visualization):
    filepath = path.join(VISUALIZATIONS_PATH,
                            visualization,
                            latest_version(visualization),
                            "scene.blend")

    bpy.ops.wm.open_mainfile(filepath=filepath)


def save_new(visualization):
    new_version = strftime("%Y%m%dT%H%M")
    directory = path.join(VISUALIZATIONS_PATH, visualization, new_version)

    makedirs(directory)

    filepath = path.join(directory, "scene.blend")

    bpy.ops.file.pack_all()
    bpy.ops.wm.save_as_mainfile(filepath=filepath)

    thumbnail_filepath = path.join(directory, "thumbnail.png")

    view3d_context = get_view3d_context()

    for region in view3d_context['area'].regions:
        if region.type == 'WINDOW':
            view3d_context['region'] = region

    forged_context = {
        'area': view3d_context['area'],
        'region': view3d_context['region'],
        'window': view3d_context['window']
    }

    from pprint import pprint

    pprint(forged_context)

    bpy.ops.view3d.viewnumpad(forged_context, type='CAMERA')
    bpy.ops.screen.screenshot(forged_context,
                              check_existing=False,
                              filepath=thumbnail_filepath,
                              full=False)

    # Rescale thumbnail with ffmpeg
    call([
        "ffmpeg",
        "-y",
        "-f", "image2",
        "-i", thumbnail_filepath,
        "-vf", "scale=480:270:force_original_aspect_ratio=decrease",
        thumbnail_filepath
    ])

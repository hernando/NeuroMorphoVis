####################################################################################################
# Copyright (c) 2016 - 2018, EPFL / Blue Brain Project
#               Marwan Abdellah <marwan.abdellah@epfl.ch>
#
# This file is part of NeuroMorphoVis <https://github.com/BlueBrain/NeuroMorphoVis>
#
# This library is free software; you can redistribute it and/or modify it under the terms of the
# GNU Lesser General Public License version 3.0 as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License along with this library;
# if not, write to the Free Software Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
# MA 02110-1301 USA.
####################################################################################################

__author__      = "Marwan Abdellah"
__copyright__   = "Copyright (c) 2016 - 2018, Blue Brain Project / EPFL"
__credits__     = ["Ahmet Bilgili", "Juan Hernando", "Stefan Eilemann"]
__version__     = "1.0.0"
__maintainer__  = "Marwan Abdellah"
__email__       = "marwan.abdellah@epfl.ch"
__status__      = "Production"


# System imports
import sys, os
import_paths = ['core']
for import_path in import_paths:
    sys.path.append(('%s/%s' %(os.path.dirname(os.path.realpath(__file__)), import_path)))

# NeuroMorphoVis imports
import neuromorphovis as nmv
import neuromorphovis.shading
import neuromorphovis.rendering
import neuromorphovis.enums
import neuromorphovis.geometry

####################################################################################################
# @get_tag_rgb_color
####################################################################################################
def get_tag_rgb_color(tag,
                      styles):
    """Returns the RGB color of a given tag from the style list.

    :param tag:
        A given tag.
    :param styles:
        A list of styles
    :return:
        RGB color.
    """

    for style in styles:
        if style[0] == tag:
            return style[1]


####################################################################################################
# @get_tag_alpha
####################################################################################################
def get_tag_alpha(tag,
                  styles):
    """Returns the alpha value of a given tag from the style list.

    :param tag:
        A given tag.
    :param styles:
        A list of styles
    :return:
        Alpha value.
    """

    for style in styles:
        if style[0] == tag:
            return style[2]


####################################################################################################
# @get_tag_shader
####################################################################################################
def get_tag_shader(tag,
                   styles):
    """Returns the shader of a given tag from the style list.

    :param tag:
        A given tag.
    :param styles:
        A list of styles
    :return:
        Alpha value.
    """

    for style in styles:
        if style[0] == tag:
            return style[3]


####################################################################################################
# @apply_style
####################################################################################################
def apply_style(neurons,
                styles):
    """Apply a style given from the configuration to the loaded neurons.

    :param neurons:
        A list of neurons loaded to the scene.
    :param styles:
        A style configuration.
    """

    print('* Applying style')
    for i, neuron in enumerate(neurons):

        if neuron.membrane_meshes is None:
            continue

        # Get the tag
        tag = neuron.tag

        # Color
        color = get_tag_rgb_color(tag, styles)

        # Shader
        shader = nmv.enums.Shading.get_enum(get_tag_shader(tag, styles))

        # Alpha
        alpha = get_tag_alpha(tag, styles)

        style_name = 'style_%s_%s' % (str(tag),  str(neuron.gid))

        # Create the shader from the shader library
        material = nmv.shading.create_material(style_name, color, shader)

        # Apply the shader to the membrane object
        for membrane_mesh in neuron.membrane_meshes:
            nmv.shading.set_material_to_object(membrane_mesh, material)


####################################################################################################
# @apply_style
####################################################################################################
def draw_spheres(neurons,
                 styles):
    """Draw the neurons as spheres.

    :param neurons:
        A list of neurons.
    :param styles:
        A style configuration.
    :return:
        Draw spheres list.
    """

    spheres = list()

    for i, neuron in enumerate(neurons):

        # Get the tag
        tag = neuron.tag

        # Color
        color = get_tag_rgb_color(tag, styles)

        # Shader
        shader = nmv.enums.Shading.get_enum(get_tag_shader(tag, styles))

        # Alpha
        alpha = get_tag_alpha(tag, styles)

        style_name = 'style_%s_%s' % (str(tag), str(neuron.gid))

        # Create the shader from the shader library
        material = nmv.shading.create_material(style_name, color, shader)

        # Draw the sphere
        neuron_sphere = nmv.geometry.create_uv_sphere(location=neuron.position,
            radius=neuron.soma_mean_radius, name='neuron_%s' % str(neuron.gid))
        spheres.append(neuron_sphere)

        nmv.shading.set_material_to_object(neuron_sphere, material)

    # Return a list of spheres of the neurons
    return spheres

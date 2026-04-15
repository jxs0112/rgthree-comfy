import nodes

from comfy_api.latest import IO

from .constants import get_category, get_name


class RgthreeImageComparer(IO.ComfyNode):
  """A node that compares two images in the UI."""

  NAME = get_name('Image Comparer')
  CATEGORY = get_category()
  DESCRIPTION = "Compares two images with a slider interface."

  @classmethod
  def define_schema(cls):
    return IO.Schema(
      node_id=cls.NAME,
      display_name=cls.NAME,
      description=cls.DESCRIPTION,
      category=cls.CATEGORY,
      is_output_node=True,
      inputs=[
        IO.Image.Input("image_a", optional=True),
        IO.Image.Input("image_b", optional=True),
        # Let the frontend render the native compare control in Node 2.0.
        IO.ImageCompare.Input("compare_view"),
      ],
      hidden=[IO.Hidden.prompt, IO.Hidden.extra_pnginfo],
      outputs=[],
    )

  @classmethod
  def compare_images(cls,
                     image_a=None,
                     image_b=None,
                     compare_view=None,
                     prompt=None,
                     extra_pnginfo=None):
    return cls.execute(
      image_a=image_a,
      image_b=image_b,
      compare_view=compare_view,
      prompt=prompt,
      extra_pnginfo=extra_pnginfo,
    )

  @classmethod
  def execute(cls,
              image_a=None,
              image_b=None,
              compare_view=None,
              prompt=None,
              extra_pnginfo=None) -> IO.NodeOutput:
    del compare_view

    result = {"a_images": [], "b_images": []}
    preview_node = nodes.PreviewImage()

    if image_a is not None and len(image_a) > 0:
      saved = preview_node.save_images(
        image_a, "rgthree.compare.a", prompt, extra_pnginfo
      )
      result["a_images"] = saved["ui"]["images"]

    if image_b is not None and len(image_b) > 0:
      saved = preview_node.save_images(
        image_b, "rgthree.compare.b", prompt, extra_pnginfo
      )
      result["b_images"] = saved["ui"]["images"]

    return IO.NodeOutput(ui=result)

from nefertem_inference.plugins._dummy.plugin import InferencePluginDummy
from nefertem_inference.plugins.builder import InferencePluginBuilder


class InferenceBuilderDummy(InferencePluginBuilder):
    """
    Inference plugin builder.
    """

    def build(self, *args) -> list[InferencePluginDummy]:
        """
        Build a plugin.
        """
        return [InferencePluginDummy()]

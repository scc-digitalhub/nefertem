from nefertem.utils.commons import RUN_OBJECT, RUN_HANDLER_OBJECT

MAPPER = {
    RUN_OBJECT: ["nefertem_inference.run.run", "RunInference"],
    RUN_HANDLER_OBJECT: ["nefertem_inference.run.handler", "RunHandlerInference"],
}

PLUGINS = {
    "frictionless": ["nefertem_inference.plugins.frictionless.builder", "InferenceBuilderFrictionless"],
    "_dummy": ["nefertem_inference.plugins._dummy.dummy", "InferenceBuilderDummy"],
}

# Disable caching; caching is useful for inference but not for training
base_model.config.use_cache = False
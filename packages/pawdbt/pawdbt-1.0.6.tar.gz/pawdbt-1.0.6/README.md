# pawdbt

A bespoke implementation of automated dbt model configuration and documentation. 

### Features

- Supports standard dbt `--select` parameters.
- Optionally build your pipeline before running documentation to avoid table not-exist errors.
- Realtime feedback on state of execution.
- Store all your `docs` in a single relations markdown file for ease of location.
- Choose how to materialise your configuration and documentation.

### Requirements
- dbt version `>=1.3.0`
- Shared docs file located in `models/_docs/dry.md`
	- doc blocks prefixed with `dry_`
- Pipeline first, transformation layer second directory structure within `models/`. E.g.
	- my_pipeline
		 - transformation_layer_1
		 - transformation_layer_2

### Usability

```shell
pip install pawdbt 
```
```shell
pawdbt -s my_model -d my_model
```

| Argument                | Required? | Description                                                                                       | Example          |
|-------------------------|-----------|---------------------------------------------------------------------------------------------------|------------------|
| -s /  --select             | Yes       | Standard dbt selector. Does not support selectors with spaces (my_model my_model2)                | -s +my_model+    |
| -d / --save-doc-blocks-in | Yes       | Relation name to house shared column docs                                                         | -d my_model      |
| -o / --always-overwrite   | No        | Boolean value to tell package to overwrite existing files rather than prompt user during runtime. | -o true / _null_ |
| -r / --run-models         | No        | Boolean value to tell package whether to run your selector before attempting to build docs.       | -r true / _null_ |


### Screenshot
![Thumb01](thumbnail.png) 
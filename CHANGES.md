# Changelog

# 0.3.2

- Added new actions `puppet.lookup`, `puppet.lookup_remote`, `puppet.epp_render` and `puppet.epp_render_remote`.

  Contributed by Nick Maludy (Encore Technologies)

# 0.3.0

- Updated action `runner_type` from `run-python` to `python-script`

## v0.2.0

**BREAKING CHANGE**

The configuration in `config.yaml` has been flattened, and moved
to `config.schema.yaml`. 

Any older configuration will need to be updated. `hostname` and `port`
are no longer subsections under `master` - they are now top-level
configuration items. Similarly, `client_cert_path`, `client_cert_key_path`,
`ca_cert_path` are now top-level items, not under `auth`.

## v0.1.0

* Initial release

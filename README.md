# ctapipe ASV benchmarks


Note: this is about benchmarking the computing performance of ctapipe (CPU / memory),
_not_ scientific performance benchmarks such as angular resolution or other 
reconstruction quality metrics.

ASV fetches [ctapipe](https://github.com/cta-observatory/ctapipe) from GitHub.
The suite runs on Python 3.12, 3.13, and 3.14. From this repository, use uv to
install those interpreters and run ASV.

```sh
uv python install 3.12 3.13 3.14
export PATH="$(uv python dir --bin):$PATH"
uv sync --locked --python 3.12
uv run --no-sync asv machine --yes
uv run --no-sync asv run
```

To measure two upstream ctapipe commits in one run, use
`uv run --no-sync asv continuous --interleave-rounds BASE_SHA HEAD_SHA`.

To benchmark commits from a local checkout, copy `asv.conf.json` to
`asv.conf.local.json` and set its `repo` field to the checkout path relative
to the config file, for example `../ctapipe`. Pass
`--config asv.conf.local.json` to ASV.

The Hillas benchmark reports the time to process a batch of 500 images from
`ToyEventSource`. It uses a fixed seed and a synthetic 40 × 40 pixel camera.
Image generation, cleaning with the default `TailcutsImageCleaner`, and
preparing the matching telescope-frame geometry all run during setup, outside
the timed method. Images with no surviving pixels are replaced during setup.

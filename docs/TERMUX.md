# Termux Setup

```bash
pkg update
pkg install python ffmpeg git
cd ~/AFRITOON
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -q
python render.py scenes/tunde_test.yaml
```

Expected render path: `output/tunde_test.mp4`.

For the first smoke test, inspect the MP4 on the phone before adding features. The production loop is render → watch → improve.

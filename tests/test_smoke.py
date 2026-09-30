from pathlib import Path

def test_src_directory_exists():
    assert Path("src").is_dir()
import base64
import pytest
from mailing.html_utils import render_body_with_inline_images


def test_replaces_known_cid_with_data_uri(tmp_path):
    img = tmp_path / "logo.png"
    img.write_bytes(b"\x89PNG\r\n")
    body = '<img src="cid:logo">'
    result = render_body_with_inline_images(body, {"logo": "logo.png"}, str(tmp_path))
    expected_b64 = base64.b64encode(b"\x89PNG\r\n").decode()
    assert f"data:image/png;base64,{expected_b64}" in result
    assert "cid:logo" not in result


def test_unknown_cid_left_unchanged(tmp_path):
    body = '<img src="cid:unknown">'
    result = render_body_with_inline_images(body, {}, str(tmp_path))
    assert "cid:unknown" in result


def test_multiple_cids_all_replaced(tmp_path):
    (tmp_path / "a.png").write_bytes(b"PNG_A")
    (tmp_path / "b.jpg").write_bytes(b"JPG_B")
    body = '<img src="cid:a"><img src="cid:b">'
    result = render_body_with_inline_images(body, {"a": "a.png", "b": "b.jpg"}, str(tmp_path))
    assert "cid:a" not in result
    assert "cid:b" not in result
    assert "data:image/png;base64," in result
    assert "data:image/jpeg;base64," in result


def test_missing_file_leaves_cid_unchanged(tmp_path):
    body = '<img src="cid:ghost">'
    result = render_body_with_inline_images(body, {"ghost": "ghost.png"}, str(tmp_path))
    assert "cid:ghost" in result

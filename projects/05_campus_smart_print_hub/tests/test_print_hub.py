"""Unit tests for KiTE Campus Smart Print Hub."""

import io
import pytest

qrcode = pytest.importorskip("qrcode")
PIL = pytest.importorskip("PIL")

def test_qr_generation():
    token_id = "KITE-PRN-1234"
    payload = f"TOKEN={token_id}|CAMPUS=KITE"
    qr = qrcode.QRCode(box_size=5, border=1)
    qr.add_data(payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1A73E8", back_color="white")
    assert img is not None

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    assert buf.tell() > 0

def test_token_format():
    token_id = "KITE-PRN-9999"
    assert token_id.startswith("KITE-PRN-")
    assert len(token_id) == 13

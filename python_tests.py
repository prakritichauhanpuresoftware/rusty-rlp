import pytest
from rlp import decode
from rlp.codec import encode_raw
import rusty_rlp

from eth_utils import decode_hex


@pytest.mark.parametrize(
    'input',
    (
        b'',
        b'asdf',
        b'fds89032#$@%',
        b'dfsa',
        [b'dfsa', b''],
        [],
        [b'fdsa', [b'dfs', [b'jfdkl']]],
        # https://etherscan.io/block/400000
        [b'\x1ew\xd8\xf1&sH\xb5\x16\xeb\xc4\xf4\xda\x1e*\xa5\x9f\x85\xf0\xcb\xd8S\x94\x95\x00\xff\xac\x8b\xfc8\xba\x14', b'\x1d\xccM\xe8\xde\xc7]z\xab\x85\xb5g\xb6\xcc\xd4\x1a\xd3\x12E\x1b\x94\x8at\x13\xf0\xa1B\xfd@\xd4\x93G', b'*e\xac\xa4\xd5\xfc[\\\x85\x90\x90\xa6\xc3M\x16A59\x82&', b'\x0b^C\x86h\x0fC\xc2$\xc5\xc07\xef\xc0\xb6E\xc8\xe1\xc3\xf6\xb3\r\xa0\xee\xc0rr\xb4\xe6\xf8\xcd\x89', b'V\xe8\x1f\x17\x1b\xccU\xa6\xff\x83E\xe6\x92\xc0\xf8n[H\xe0\x1b\x99l\xad\xc0\x01b/\xb5\xe3c\xb4!', b'V\xe8\x1f\x17\x1b\xccU\xa6\xff\x83E\xe6\x92\xc0\xf8n[H\xe0\x1b\x99l\xad\xc0\x01b/\xb5\xe3c\xb4!', b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00', b'\x05zA\x8a|>', b'\x06\x1a\x80', b'/\xef\xd8', b'', b'V"\xef\xdc', b'\xd5\x83\x01\x02\x02\x84Geth\x85go1.5\x85linux', b'?\xbe\xa7\xafd*N \xcd\x93\xa9E\xa1\xf5\xe2;\xd7/\xc5&\x11S\xe0\x91\x02\xcfq\x89\x80\xae\xff8', b'j\xf2<\xaa\xe9V\x92\xef'],
    )
)
def test_decode_raw(input):
    pyrlp_encoded = encode_raw(input)
    rustyrlp_encoded = rusty_rlp.encode_raw(input)

    assert pyrlp_encoded == rustyrlp_encoded

    pyrlp_decoded = decode(pyrlp_encoded)
    rustyrlp_decoded = rusty_rlp.decode_raw(rustyrlp_encoded, True)

    assert pyrlp_decoded == rustyrlp_decoded == input


@pytest.mark.parametrize(
    'rlp_data',
    (
        0,
        32,
        ['asdf', ['fdsa', [5]]],
        str
    ),
)
def test_invalid_serializations(rlp_data):
    with pytest.raises(rusty_rlp.EncodingError, match='Can not encode value'):
        rusty_rlp.encode_raw(rlp_data)


@pytest.mark.parametrize(
    'rlp_data, expected_error',
    (
        (None, TypeError),
        ('asdf', TypeError),
        # Empty list with trailing bytes
        (decode_hex('0xc000'), rusty_rlp.DecodingError),
        # https://github.com/ethereum/pyrlp/blob/37396698aeb949932e70a53fa10f3046b7915bf3/tests/test_codec.py#L47-L50
        (decode_hex('b8056d6f6f7365'), rusty_rlp.DecodingError),
        # trailing bytes to https://github.com/ethereum/pyrlp/blob/37396698aeb949932e70a53fa10f3046b7915bf3/tests/rlptest.json#L68
        (decode_hex('0xcc83646f6783676f648363617400'), rusty_rlp.DecodingError),
        # trailing bytes to short string
        (decode_hex('0x83646f6700'), rusty_rlp.DecodingError),
        (b'', rusty_rlp.DecodingError),
        (b'\x83do', rusty_rlp.DecodingError),
        (b'\xb8\x00', rusty_rlp.DecodingError),
        (b'\xb9\x00\x00', rusty_rlp.DecodingError),
        (b'\xba\x00\x02\xff\xff', rusty_rlp.DecodingError),
    ),
)
def test_invalid_deserializations(rlp_data, expected_error):
    with pytest.raises(expected_error):
        rusty_rlp.decode_raw(rlp_data, True)


@pytest.mark.parametrize(
    'rlp_data, expected',
    (
        (decode_hex('0xc0'), []),
        (decode_hex('0xcc83646f6783676f6483636174'), [ b"dog", b"god", b"cat" ]),
        (decode_hex('0xc6827a77c10401'), [b'zw', [b'\x04'], b'\x01']),
    ),
)
def test_decode_special_cases(rlp_data, expected):
    assert rusty_rlp.decode_raw(rlp_data, True) == expected


@pytest.mark.parametrize(
    'rlp_data, expected',
    (
        # Trailing bytes to empty list
        (decode_hex('0xc000'), []),
        #trailing bytes to https://github.com/ethereum/pyrlp/blob/37396698aeb949932e70a53fa10f3046b7915bf3/tests/rlptest.json#L68
        (decode_hex('0xcc83646f6783676f648363617400'), [b'dog', b'god', b'cat']),
        # trailing bytes to short string
        (decode_hex('0x83646f6700'), b'dog'),
    ),
)
def test_nonstrict_deserializations(rlp_data, expected):
    assert rusty_rlp.decode_raw(rlp_data, False) == expected
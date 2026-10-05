from unittest.mock import patch

import cli


@patch("cli.requests.get")
def test_show_inventory(mock_get, capsys):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {
            "id": 1,
            "name": "Nutella",
            "brand": "Ferrero",
            "price": 650,
            "stock": 10
        }
    ]

    cli.show_inventory()

    output = capsys.readouterr().out

    assert "Nutella" in output
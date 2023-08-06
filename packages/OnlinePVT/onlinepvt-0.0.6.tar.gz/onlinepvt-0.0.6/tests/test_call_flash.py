import pytest
from onlinepvt.models import CalculationComposition, FlashCalculationType, ProblemDetails
from onlinepvt.online_pvt_client import OnlinePvtClient


@pytest.mark.asyncio
async def test_call_flash():
    client = OnlinePvtClient(
        "https://api.onlinepvt.com", "52E6292C-BC9B-402F-83D8-D59D08223BC1", "##glD47#al!=(d+53ES3?qW")

    input = client.get_flash_input()
    input.temperature = 445
    input.pressure = 20
    input.components = [
        CalculationComposition(mass=0.78),
        CalculationComposition(mass=0.02),
        CalculationComposition(mass=0.20)
    ]
    input.flash_type = FlashCalculationType.PT
    input.fluid_id = "9E9ABAD5-C6CA-427F-B5E7-15AB3F7CF076"

    result: ProblemDetails = await client.call_flash_async(input)

    await client.cleanup()

    assert result.status == 400

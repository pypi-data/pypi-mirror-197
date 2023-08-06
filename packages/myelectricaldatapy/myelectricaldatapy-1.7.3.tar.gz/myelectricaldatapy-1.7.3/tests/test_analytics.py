from __future__ import annotations

import pytest

from myelectricaldatapy import EnedisAnalytics

from .consts import DATASET_30 as DS_30
from .consts import DATASET_DAILY as DS_DAILY
from .consts import DATASET_DAILY_COMPARE as DS_COMPARE
from .consts import TEMPO

PDL = "012345"
TOKEN = "xxxxxxxxxxxxx"


@pytest.mark.asyncio
async def test_hours_analytics() -> None:
    """Test analytics compute."""
    dataset = DS_30["meter_reading"]["interval_reading"]
    cumsums = {
        "standard": {"sum_value": 1000, "sum_price": 0},
        "offpeak": {"sum_value": 1000, "sum_price": 0},
    }
    prices = {"standard": {"price": 0.17}, "offpeak": {"price": 0.18}}
    intervals = [("01:30:00", "08:00:00"), ("12:30:00", "14:00:00")]
    analytics = EnedisAnalytics(dataset)
    resultat = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=False,
        intervals=intervals,
        groupby=True,
        summary=True,
        cumsums=cumsums,
        prices=prices,
    )
    assert resultat[0]["notes"] == "offpeak"
    assert resultat[0]["value"] == 1.079
    assert resultat[0].get("sum_value") is not None
    assert resultat[0].get("sum_price") is not None
    print(resultat)

    analytics = EnedisAnalytics(dataset)
    resultat = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=False,
        intervals=intervals,
        groupby=True,
        prices=prices,
    )
    assert resultat[0]["notes"] == "offpeak"
    assert resultat[0]["value"] == 1.079
    assert round(resultat[2]["price"], 3) == 0.833
    assert resultat[0].get("sum_value") is None
    print(resultat)

    analytics = EnedisAnalytics(dataset)
    resultat = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=True,
        intervals=intervals,
        groupby=True,
        prices=prices,
    )
    print(resultat)

    analytics = EnedisAnalytics(dataset)
    resultat = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=False,
        intervals=intervals,
        groupby=True,
    )
    assert resultat[27]["value"] == 1.296
    assert resultat[28]["value"] == 0.618
    print(resultat)

    dataset = DS_DAILY["meter_reading"]["interval_reading"]
    analytics = EnedisAnalytics(dataset)
    resultat = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=False,
        intervals=intervals,
        groupby=True,
        summary=True,
        cumsums=cumsums,
        prices=prices,
    )
    assert resultat[0]["value"] == 42.045
    print(resultat)


@pytest.mark.asyncio
async def test_daily_analytics() -> None:
    prices = {"standard": {"price": 0.17}, "offpeak": {"price": 0.18}}
    dataset = DS_30["meter_reading"]["interval_reading"]
    intervals = [("01:30:00", "08:00:00"), ("12:30:00", "14:00:00")]
    dataset = DS_DAILY["meter_reading"]["interval_reading"]
    analytics = EnedisAnalytics(dataset)
    resultat = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=False,
        intervals=intervals,
        groupby=True,
        summary=True,
        prices=prices,
    )
    assert resultat[359]["value"] == 68.68
    print(resultat)


@pytest.mark.asyncio
async def test_compare_analytics() -> None:
    prices = {"standard": {"price": 0.17}, "offpeak": {"price": 0.18}}
    cumsums = {
        "standard": {"sum_value": 0, "sum_price": 0},
        "offpeak": {"sum_value": 0, "sum_price": 0},
    }
    intervals = [("01:30:00", "08:00:00"), ("12:30:00", "14:00:00")]
    dataset = DS_30["meter_reading"]["interval_reading"]
    analytics = EnedisAnalytics(dataset)
    resultat1 = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=False,
        intervals=intervals,
        groupby=True,
        summary=True,
        cumsums=cumsums,
        prices=prices,
    )
    print(resultat1)
    sum_value = 0
    for rslt in resultat1:
        sum_value = sum_value + rslt["value"]

    sum_value_1 = resultat1[26]["sum_value"] + resultat1[77]["sum_value"]
    assert round(sum_value, 3) == round(sum_value_1, 3)
    dataset = DS_COMPARE["meter_reading"]["interval_reading"]
    analytics = EnedisAnalytics(dataset)
    resultat2 = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=False,
        intervals=intervals,
        groupby=True,
        summary=True,
        cumsums=cumsums,
        prices=prices,
        start_date="2023-02-28",
    )
    assert round(sum_value, 3) == resultat2[2]["sum_value"]
    print(resultat2)


@pytest.mark.asyncio
async def test_cumsums_analytics() -> None:
    prices = {"standard": {"price": 0.17}, "offpeak": {"price": 0.18}}
    cumsums = {
        "standard": {"sum_value": 100, "sum_price": 50},
        "offpeak": {"sum_value": 1000, "sum_price": 75},
    }
    intervals = [("01:30:00", "08:00:00"), ("12:30:00", "14:00:00")]
    dataset = DS_30["meter_reading"]["interval_reading"]
    analytics = EnedisAnalytics(dataset)
    resultat = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=False,
        intervals=intervals,
        groupby=True,
        summary=True,
        cumsums=cumsums,
        prices=prices,
        start_date="2023-02-28",
    )
    # offpeak
    assert resultat[0]["sum_value"] == resultat[0]["value"] + 1000
    assert resultat[0]["sum_price"] == resultat[0]["price"] + 75
    # standard
    assert resultat[27]["sum_value"] == resultat[27]["value"] + 100
    assert resultat[27]["sum_price"] == resultat[27]["price"] + 50


@pytest.mark.asyncio
async def test_tempo_analytics() -> None:
    """Test tempo pricings."""
    prices = {
        "standard": {"blue": 0.2, "white": 0.3, "red": 3},
        "offpeak": {"blue": 0.1, "white": 0.2, "red": 1.5},
    }
    cumsums = {
        "standard": {"sum_value": 100, "sum_price": 50},
        "offpeak": {"sum_value": 1000, "sum_price": 75},
    }
    intervals = [("01:30:00", "08:00:00"), ("12:30:00", "14:00:00")]
    dataset = DS_30["meter_reading"]["interval_reading"]
    analytics = EnedisAnalytics(dataset)
    resultat = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=False,
        intervals=intervals,
        groupby=True,
        summary=True,
        cumsums=cumsums,
        prices=prices,
        start_date="2023-02-28",
        tempo=TEMPO,
    )
    assert resultat[0]["tempo"] == "blue"
    analytics = EnedisAnalytics(dataset)
    resultat = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=False,
        intervals=intervals,
        groupby=True,
        summary=True,
        cumsums=cumsums,
        prices=prices,
        start_date="2023-02-28",
        tempo=TEMPO,
    )
    assert resultat[0]["tempo"] == "blue"
    assert resultat[0]["value"] == 1.079
    assert resultat[0]["sum_price"] == resultat[0]["price"] + 75
    assert resultat[0]["sum_value"] == resultat[0]["value"] + 1000


@pytest.mark.asyncio
async def test_standard_analytics() -> None:
    cumsums = {
        "standard": {"sum_value": 100, "sum_price": 50},
        "offpeak": {"sum_value": 1000, "sum_price": 75},
    }
    intervals = [("01:30:00", "08:00:00"), ("12:30:00", "14:00:00")]
    dataset = DS_30["meter_reading"]["interval_reading"]
    prices = {"standard": {"price": 0.5}, "offpeak": {"price": 1}}
    analytics = EnedisAnalytics(dataset)
    resultat = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=False,
        intervals=intervals,
        groupby=True,
        summary=True,
        cumsums=cumsums,
        prices=prices,
    )
    assert resultat[0]["value"] == 1.079
    prices = {"standard": {"price": 0.5}, "offpeak": {"price": 1}}
    dataset = DS_DAILY["meter_reading"]["interval_reading"]
    analytics = EnedisAnalytics(dataset)
    resultat = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=False,
        intervals=intervals,
        groupby=True,
        summary=True,
        cumsums=cumsums,
        prices=prices,
        start_date="2023-02-28",
    )
    assert resultat[0]["price"] == resultat[0]["value"] * 0.5


@pytest.mark.asyncio
async def test_start_date_analytics() -> None:
    dataset = DS_DAILY["meter_reading"]["interval_reading"]
    analytics = EnedisAnalytics(dataset)
    resultat = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=False,
        groupby=True,
        start_date="2023-3-7",
    )
    print(resultat)
    assert len(resultat) == 0
    dataset = DS_30["meter_reading"]["interval_reading"]
    analytics = EnedisAnalytics(dataset)
    resultat = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=False,
        groupby=True,
        start_date="2023-3-4",
    )
    print(resultat)
    assert len(resultat) == 0


@pytest.mark.asyncio
async def test_price_analytics() -> None:
    dataset = DS_30["meter_reading"]["interval_reading"]
    prices = {
        "standard": {"blue": 0.2, "white": 0.3, "red": 3},
        "offpeak": {"blue": 0.1, "white": 0.2, "red": 1.5},
    }
    analytics = EnedisAnalytics(dataset)
    resultat = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=False,
        groupby=True,
        prices=prices,
        tempo=None,
    )
    assert resultat[0].get("price") is None

    dataset = DS_30["meter_reading"]["interval_reading"]
    prices = {"standard": {"price": 0.5}, "offpeak": {"price": 1}}
    analytics = EnedisAnalytics(dataset)
    resultat = analytics.get_data_analytics(
        convertKwh=True,
        convertUTC=False,
        groupby=True,
        prices=prices,
        tempo=TEMPO,
    )
    assert resultat[0].get("price") is not None

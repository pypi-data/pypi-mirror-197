from __future__ import annotations

from typing import Optional, Tuple

import numpy as np
import pandas as pd
from pandas import DataFrame

from retentioneering.constants import DATETIME_UNITS
from retentioneering.data_processor import DataProcessor
from retentioneering.eventstream.types import EventstreamType
from retentioneering.params_model import ParamsModel
from retentioneering.widget.widgets import ReteTimeWidget


class TruncatedEventsParams(ParamsModel):
    """
    Class with parameters for class :py:class:`.TruncatedEvents`
    """

    left_truncated_cutoff: Optional[Tuple[float, DATETIME_UNITS]]
    right_truncated_cutoff: Optional[Tuple[float, DATETIME_UNITS]]

    _widgets = {
        "left_truncated_cutoff": ReteTimeWidget(),
        "right_truncated_cutoff": ReteTimeWidget(),
    }


class TruncatedEvents(DataProcessor):
    """
    Creates new synthetic event(s) for each user on the base of timeout threshold:
    ``truncated_left`` and ``truncated_right``

    Parameters
    ----------
    left_truncated_cutoff : Tuple(float, :numpy_link:`DATETIME_UNITS<>`), optional
        Threshold value, and it's unit of measure.
        Timedelta between last event in each user's path and first event in whole Eventstream is calculating.
        For users with timedelta less than selected ``left_truncated_cutoff``, new synthetic event - ``truncated_left``
        will be added.

    right_truncated_cutoff : Tuple(float, :numpy_link:`DATETIME_UNITS<>`), optional
        Threshold value and its unit of measure.
        Timedelta between first event in each user's path and last event in whole Eventstream is calculating.
        For users with timedelta less than selected ``right_truncated_cutoff``,
        new synthetic event - ``truncated_right`` will be added.

    Returns
    -------
    Eventstream
        ``Eventstream`` with new synthetic events only, for users whose paths satisfy the specified cut-offs.

        +-------------------+-------------------+------------------+
        | **event_name**    | **event_type**    |  **timestamp**   |
        +-------------------+-------------------+------------------+
        | truncated_left    | truncated_left    |  first_event     |
        +-------------------+-------------------+------------------+
        | truncated_right   | truncated_right   |  last_event      |
        +-------------------+-------------------+------------------+

    See Also
    --------
    Hists

    Raises
    ------
    ValueError
        If both of ``left_truncated_cutoff`` and ``right_truncated_cutoff`` are empty.
    """

    params: TruncatedEventsParams

    def __init__(self, params: TruncatedEventsParams):
        super().__init__(params=params)

    def apply(self, eventstream: EventstreamType) -> EventstreamType:
        from retentioneering.eventstream.eventstream import Eventstream

        events: DataFrame = eventstream.to_dataframe(copy=True)
        user_col = eventstream.schema.user_id
        time_col = eventstream.schema.event_timestamp
        type_col = eventstream.schema.event_type
        event_col = eventstream.schema.event_name

        left_truncated_cutoff, left_truncated_unit = None, None
        right_truncated_cutoff, right_truncated_unit = None, None

        if self.params.left_truncated_cutoff:
            left_truncated_cutoff, left_truncated_unit = self.params.left_truncated_cutoff

        if self.params.right_truncated_cutoff:
            right_truncated_cutoff, right_truncated_unit = self.params.right_truncated_cutoff
        truncated_events = pd.DataFrame()

        if not left_truncated_cutoff and not right_truncated_cutoff:
            raise ValueError("Either left_truncated_cutoff or right_truncated_cutoff must be specified!")

        userpath = (
            events.groupby(user_col)[time_col].agg([np.min, np.max]).rename(columns={"amin": "start", "amax": "end"})
        )

        if left_truncated_cutoff:
            timedelta = (userpath["end"] - events[time_col].min()) / np.timedelta64(
                1, left_truncated_unit  # type: ignore
            )
            truncated_users_index = userpath[timedelta < left_truncated_cutoff].index
            left_truncated_events = events.groupby(user_col).first().reindex(truncated_users_index).reset_index()

            left_truncated_events[event_col] = "truncated_left"
            left_truncated_events[type_col] = "truncated_left"
            left_truncated_events["ref"] = None
            truncated_events = pd.concat([truncated_events, left_truncated_events])

        if right_truncated_cutoff:
            timedelta = (events[time_col].max() - userpath["start"]) / np.timedelta64(
                1, right_truncated_unit  # type: ignore
            )
            truncated_users_index = userpath[timedelta < right_truncated_cutoff].index
            right_truncated_events = events.groupby(user_col).last().reindex(truncated_users_index).reset_index()

            right_truncated_events[event_col] = "truncated_right"
            right_truncated_events[type_col] = "truncated_right"
            right_truncated_events["ref"] = None
            truncated_events = pd.concat([truncated_events, right_truncated_events])

        eventstream = Eventstream(
            raw_data_schema=eventstream.schema.to_raw_data_schema(),
            raw_data=truncated_events,
            relations=[{"raw_col": "ref", "eventstream": eventstream}],
        )
        return eventstream

import { Card, CardContent, CardHeader, Grid, Typography } from "@mui/material";
import {
  Timeline,
  TimelineItem,
  TimelineSeparator,
  TimelineConnector,
  TimelineContent,
  TimelineDot,
  TimelineOppositeContent,
  timelineOppositeContentClasses,
} from "@mui/lab";
import React from "react";


function ModelTrain({ epochs }) {
  return (
    <Timeline
      sx={{
        [`& .${timelineOppositeContentClasses.root}`]: {
          flex: 0.3,
        },
        marginRight: 2,
      }}
    >
      <>
        {epochs.map((timeline, index) => (
          <TimelineItem key={index}>
            <TimelineOppositeContent color="textSecondary">
              {timeline.created_at}
            </TimelineOppositeContent>
            <TimelineSeparator>
              <TimelineDot />
              <TimelineConnector />
            </TimelineSeparator>
            <TimelineContent>
              Epoch: {timeline.epoch}, Train: {timeline.train_loss}, Validate:{" "}
              {timeline.val_loss}{" "}
            </TimelineContent>
          </TimelineItem>
        ))}
      </>
    </Timeline>
  );
}

export default ModelTrain;

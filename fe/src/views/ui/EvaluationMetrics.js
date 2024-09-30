import { Grid, Typography } from '@mui/material'
import React from 'react'

const styletitle = {
    fontWeight: 'bold'
}

function EvaluationMetrics({ metrics }) {
    return (
        <Grid container spacing={1}>
            <Grid item xs={6}>
                <Typography sx={styletitle} color={'black'}>
                    Precision
                </Typography>
            </Grid>
            <Grid item xs={6}>
                {Object.keys(metrics).length > 0 ? metrics.precision : ''}
            </Grid>
            <Grid item xs={6}>
                <Typography sx={styletitle} color={'black'}>
                    Recall
                </Typography>
            </Grid>
            <Grid item xs={6}>
                {Object.keys(metrics).length > 0 ? metrics.recall : ''}
            </Grid>
            <Grid item xs={6}>
                <Typography sx={styletitle} color={'black'}>
                    F1-score
                </Typography>
            </Grid>
            <Grid item xs={6}>
                {Object.keys(metrics).length > 0 ? metrics.f1_score : ''}
            </Grid>
            <Grid item xs={6}>
                <Typography sx={styletitle} color={'black'}>
                    Accuracy
                </Typography>
            </Grid>
            <Grid item xs={6}>
                {Object.keys(metrics).length > 0 ? metrics.accuracy : ''}
            </Grid>
        </Grid>
    )
}

export default EvaluationMetrics
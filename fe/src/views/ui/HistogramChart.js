import PropTypes from 'prop-types';
import ReactApexChart from 'react-apexcharts';
// @mui
import { Card, CardHeader, Box } from '@mui/material';
// components
import useChart from '../../components/chart/useChart';
import { useEffect } from 'react';

// ----------------------------------------------------------------------

HistogramChart.propTypes = {
    title: PropTypes.string,
    subheader: PropTypes.string,
    chartData: PropTypes.array.isRequired,
    chartLabels: PropTypes.arrayOf(PropTypes.string).isRequired,
};

export default function HistogramChart({ title, subheader, chartLabels, chartData, type, ...other }) {
    const chartOptions = useChart({
        plotOptions: { bar: { columnWidth: '16%' } },
        fill: { type: chartData.map((i) => i.fill) },
        labels: ['1', '2', '3', '4'],
        // xaxis: { type: 'datetime' },
        xaxis: { categories: chartLabels },
        tooltip: {
            shared: true,
            intersect: false,
            y: {
                formatter: (y) => {
                    if (typeof y !== 'undefined') {
                        return `${y.toFixed(0)} customers`;
                    }
                    return y;
                },
            },
        },
    });
    

    return (
        <Card {...other} sx = {{width: type=== 'new' ?  '70%' : '100%', height: type === 'chosen' && '90%' || type === 'new' && '100%'}}>
            <CardHeader title={title} subheader={subheader} />

            <Box sx={{ p: 3, pb: 1 }} dir="ltr">
                <ReactApexChart type="line" series={chartData} options={chartOptions} height={364} />
            </Box>
        </Card>
    );
}

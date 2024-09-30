import { Box, Card, CardHeader } from '@mui/material';
import React, { useState } from 'react'
import ReactApexChart from 'react-apexcharts';


function HeatMapChart({ confusionMatrix }) {
    const generateData = (model) => {
        const series = [];
        for (let i = 0; i < model.length; i++) {
            let x = `${i + 1}`

            let y = model[i]
            series.push({ x, y })

        }
        return series;
    };

    let test = confusionMatrix.map((model, index) => model = {
        name: `${index + 1}`,
        data: generateData(model)
    })


    const [options] = useState({
        chart: {
            height: 350,
            type: 'heatmap',
            width: 200
        },
        plotOptions: {
            heatmap: {
                colorScale: {
                    ranges: [{
                        from: 0,
                        to: 5,
                        color: '#e3f2fd'
                    }, {
                        from: 5,
                        to: 10,
                        color: '#bbdefb'
                    }, {
                        from: 10,
                        to: 15,
                        color: '#90caf9'    
                    },{
                        from: 15,
                        to: 20,
                        color: '#64b5f6'
                    }, {
                        from: 20,
                        to: 25,
                        color: '#42a5f5'
                    }, {
                        from: 25,
                        to: 50,
                        color: '#1976d2'
                    }]
                }
            }
        },
        dataLabels: {
            enabled: true,
            style: {
                colors: ['#000000']
            }
        },
        colors: ["#008FFB"],
    });
    return (
        <Card sx={{ width: '100%' }}>
            <Box sx={{ p: 3, pb: 1 }} dir="ltr">
                <ReactApexChart options={options} series={test} type="heatmap" height={350} />
            </Box>
        </Card>
    )
}

export default HeatMapChart
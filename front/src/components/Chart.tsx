import React, { useState } from "react";
import { AgCharts } from "ag-charts-react";
import {
  AgBarSeriesOptions,
  AgCategoryAxisOptions,
  AgChartCaptionOptions,
  AgChartLegendOptions,
  AgChartOptions,
  AgNumberAxisOptions,
} from "ag-charts-community";
import Bridge from "../models/bridge";

interface BridgeListProps {
  bridges: Bridge[];
}

function countStatuses(bridges: Bridge[]): { status: string; number: number }[] {
  const statusCount: Record<string, number> = {};

  for (const bridge of bridges) {
      if (statusCount[bridge.status]) {
          statusCount[bridge.status] += 1;
      } else {
          statusCount[bridge.status] = 1;
      }
  }
  return Object.entries(statusCount).map(([status, number]) => ({
      status,
      number,
  }));
}

const Chart: React.FC<BridgeListProps> = ({ bridges }) => {
  const data = countStatuses(bridges);

  const [options, setOptions] = useState<AgChartOptions>({
    title: { text: "X" } as AgChartCaptionOptions,
    data: data,
    series: [
      {
        type: "bar",
        xKey: "status",
        yKey: "number",
        yName: "Y",
      } as AgBarSeriesOptions,
    ],
    axes: [
      {
        type: "category",
        position: "bottom",
      } as AgCategoryAxisOptions,
      {
        type: "number",
        position: "left",
        keys: ["number"],
        label: {
          formatter: (params) => {
            return parseFloat(params.value).toLocaleString();
          },
        },
      } as AgNumberAxisOptions,
      {
        type: "number",
        position: "right",
        keys: ["avgTemp"],
        label: {
          formatter: (params) => {
            return params.value + " °C";
          },
        },
      } as AgNumberAxisOptions,
    ],
    legend: {
      position: "right",
    } as AgChartLegendOptions,
  });

  return <AgCharts options={options} />;
};

export default Chart;
import {
  CartesianGrid,
  Line,
  LineChart,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

export default function ChartBMI({ data }) {
  return (
    <LineChart width={500} height={300} data={data}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="patient_id" />
      <YAxis />
      <Tooltip />
      <Line type="monotone" dataKey="bmi" stroke="#8884d8" />
    </LineChart>
  );
}

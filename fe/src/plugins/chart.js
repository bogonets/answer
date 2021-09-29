import {Chart, registerables} from 'chart.js';
import 'chartjs-adapter-moment';
import ChartStreaming from 'chartjs-plugin-streaming';
Chart.register(ChartStreaming, ...registerables);

import Vue from 'vue';

import VueCompositionAPI from '@vue/composition-api';
Vue.use(VueCompositionAPI);

import {Chart, registerables} from 'chart.js';
import 'chartjs-adapter-moment';
import ChartStreaming from 'chartjs-plugin-streaming';
Chart.register(ChartStreaming, ...registerables);

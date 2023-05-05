import http from 'k6/http';

import { sleep } from 'k6';

// export const options = {
//   vus: 10,
//   duration: '2s',
// };


var vus = 10;
var iterations = 100;
var max_duration = '60s';
var executor = 'shared-iterations';

export const options = {
  scenarios: {
    pytheus_singleprocess: {
      executor: executor,
      exec: 'pytheus_singleprocess',
      vus: vus,
      iterations: iterations,
      maxDuration: max_duration,
    },
    pytheus_multiprocess: {
      executor: executor,
      exec: 'pytheus_multiprocess',
      vus: vus,
      iterations: iterations,
      maxDuration: max_duration,
    },
    old_singleprocess: {
      executor: executor,
      exec: 'old_singleprocess',
      vus: vus,
      iterations: iterations,
      maxDuration: max_duration,
    },
    old_multiprocess: {
      executor: executor,
      exec: 'old_multiprocess',
      vus: vus,
      iterations: iterations,
      maxDuration: max_duration,
    },

  },

};

// export default function () {
//   http.get('http://localhost:5000');
//   http.get('http://localhost:5001');
//   http.get('http://localhost:5002');
//   // http.get('http://localhost:5003');
//   // http.get('http://localhost:5004');
//   sleep(1);
// }

export function pytheus_singleprocess() {
  http.get('http://localhost:5000');
  sleep(1);
}

export function pytheus_multiprocess() {
  http.get('http://localhost:5001');
  sleep(1);
}

export function old_singleprocess() {
  http.get('http://localhost:5002');
  sleep(1);
}

export function old_multiprocess() {
  http.get('http://localhost:5003');
  sleep(1);
}

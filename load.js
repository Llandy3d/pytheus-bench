import http from 'k6/http';

import { sleep } from 'k6';

// export const options = {
//   vus: 10,
//   duration: '2s',
// };

export const options = {
  scenarios: {
    pytheus_singleprocess: {
      executor: 'shared-iterations',
      exec: 'pytheus_singleprocess',
      vus: 10,
      iterations: 100,
      maxDuration: '60s',
    },
    pytheus_multiprocess: {
      executor: 'shared-iterations',
      exec: 'pytheus_multiprocess',
      vus: 10,
      iterations: 100,
      maxDuration: '60s',
    },
    old_singleprocess: {
      executor: 'shared-iterations',
      exec: 'old_singleprocess',
      vus: 10,
      iterations: 100,
      maxDuration: '60s',
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

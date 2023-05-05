import http from 'k6/http';

import { sleep } from 'k6';


var vus = 20;
var iterations = 100;
var max_duration = '60s';
var executor = 'shared-iterations';

export const options = {
  scenarios: {
    pytheus_singleprocess: {
      executor: executor,
      // exec: 'pytheus_singleprocess',
      vus: vus,
      iterations: iterations,
      maxDuration: max_duration,
      env: {PORT: '5000'},
    },
    pytheus_multiprocess: {
      executor: executor,
      // exec: 'pytheus_multiprocess',
      vus: vus,
      iterations: iterations,
      maxDuration: max_duration,
      env: {PORT: '5001'},
    },
    old_singleprocess: {
      executor: executor,
      // exec: 'old_singleprocess',
      vus: vus,
      iterations: iterations,
      maxDuration: max_duration,
      env: {PORT: '5002'},
    },
    old_multiprocess: {
      executor: executor,
      // exec: 'old_multiprocess',
      vus: vus,
      iterations: iterations,
      maxDuration: max_duration,
      env: {PORT: '5003'},
    },

  },

};

export default function () {
  http.get(`http://localhost:${__ENV.PORT}`);
  sleep(1);
}

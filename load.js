import http from 'k6/http';

import { sleep } from 'k6';


var vus = 20;
var duration = '1m';
var executor = 'constant-vus';

export const options = {
  scenarios: {
    pytheus_singleprocess: {
      executor: executor,
      vus: vus,
      duration: duration,
      env: {PORT: '5000'},
    },
    pytheus_multiprocess: {
      executor: executor,
      vus: vus,
      duration: duration,
      env: {PORT: '5001'},
    },
    old_singleprocess: {
      executor: executor,
      vus: vus,
      duration: duration,
      env: {PORT: '5002'},
    },
    old_multiprocess: {
      executor: executor,
      vus: vus,
      duration: duration,
      env: {PORT: '5003'},
    },

  },

};

export default function () {
  http.get(`http://localhost:${__ENV.PORT}`);

  const url_base = `http://localhost:${__ENV.PORT}`;

  const payload = JSON.stringify({
    username: 'aaa',
    email: 'bbb',
  });

  const params = {
    headers: {
      'Content-Type': 'application/json',
    },
  };

  http.post(url_base + '/users/create', payload, params);

  sleep(1);
}

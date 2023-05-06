import http from 'k6/http';

import { sleep } from 'k6';


var vus = 20;
// var iterations = 100;
var iterations = 100;
var max_duration = '60s';
// var executor = 'shared-iterations';
var executor = 'constant-vus';
// var duration = '10m';
var duration = '1m';

export const options = {
  scenarios: {
    pytheus_singleprocess: {
      executor: executor,
      // exec: 'pytheus_singleprocess',
      vus: vus,
      duration: duration,
      // iterations: iterations,
      // maxDuration: max_duration,
      env: {PORT: '5000'},
    },
    pytheus_multiprocess: {
      executor: executor,
      // exec: 'pytheus_multiprocess',
      vus: vus,
      duration: duration,
      // iterations: iterations,
      // maxDuration: max_duration,
      env: {PORT: '5001'},
    },
    old_singleprocess: {
      executor: executor,
      // exec: 'old_singleprocess',
      vus: vus,
      duration: duration,
      // iterations: iterations,
      // maxDuration: max_duration,
      env: {PORT: '5002'},
    },
    old_multiprocess: {
      executor: executor,
      // exec: 'old_multiprocess',
      vus: vus,
      duration: duration,
      // iterations: iterations,
      // maxDuration: max_duration,
      env: {PORT: '5003'},
    },

  },

};

export default function () {
  http.get(`http://localhost:${__ENV.PORT}`);

  const url_base = `http://localhost:${__ENV.PORT}`;

  // for (let id = 1; id <= 100; id++) {
  //   http.get(`http://example.com/posts/${id}`, {
  //     tags: { name: 'PostsItemURL' },
  //   });
  // }
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

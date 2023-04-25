import http from 'k6/http';

import { sleep } from 'k6';

export const options = {
  vus: 10,
  duration: '30s',
};

export default function () {
  http.get('http://localhost:5000');
  http.get('http://localhost:5001');
  http.get('http://localhost:5002');
  http.get('http://localhost:5003');
  sleep(1);
}

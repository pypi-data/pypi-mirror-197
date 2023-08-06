A simple user agent random. 

### Usage

``` python
import usr_agent_rnd_rs import useragent


s = requests.Session()
print(s.headers['User-Agent'])

# Without a session
resp = requests.get('https://httpbin.org/user-agent')
print(resp.json()['user-agent'])
```


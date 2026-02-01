# API Rate Limiter

Python + MySQL API rate limiter with fixed time window logic.

## Approach
- Limit requests per user, per API
- Fixed window ensures request count per user, per API resets every hour according to clock

## API
REST API created using Flask
- Curl requests need a user ID
- api_name declared within code
- JSON responses on missing user id, limit exceeded and successful requests
  
## Database/Table Structure
MySQL Table contains 
- id(int)
- user_id (varchar)
- api_name(varchar)
- window_start(datetime)
- request_count(int)

## Testing

### Manual Testing
curl.exe -i -H "X-User-ID: user1" http://localhost:5000/api/data

### Rate Limit Test
for ($i=1; $i -le 10; $i++) {
  curl.exe http://127.0.0.1:5000/api/data -i -H "X-User-ID: user1"
}


### Expected Result
- First 5 requests → 200 OK
- Subsequent requests → 429 Too Many Requests

## Depenedencies
- flask
- mysql-connector-python

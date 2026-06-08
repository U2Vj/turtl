# Authentication backend
TURTL uses [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/) for authentication.
## Introduction
When authenticating with an API via a JSON Web Token ([RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519)), there are typically two kinds of tokens being generated:
1. ...an **access token**, which is what is used to actually authenticate with the API. Access tokens usually have a short lifespan, typically between thirty seconds and one hour.
2. ...a **refresh token**, which can be used to obtain a new access token. These have a much longer lifespan, ranging from a few hours to a few weeks.

The access tokens issued by the TURTL API are valid for one hour and refresh tokens expire after one day.

## Login process
The API provides a login endpoint located at `/users/login`. This POST endpoint needs to receive a request similar to this:
```json
{
  "email": "admin@localhost",
  "password": "admin"
}
```
When the credentials are valid, the server responds with a status code of `200 OK` and a JSON object containing an access and a refresh token is returned:
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMzA4NjcyMywiaWF0IjoxNzAzMDAwMzIzLCJqdGkiOiJmYzM0ODY5ODZhNjM0ZGMwOTU4ZTljN2Q5MDdmY2ZlNiIsInVzZXJfaWQiOjksInVzZXJuYW1lIjpudWxsLCJyb2xlIjoiQURNSU5JU1RSQVRPUiIsInJvbGVfZGlzcGxheSI6IkFkbWluaXN0cmF0b3IiLCJlbWFpbCI6ImFkbWluQGxvY2FsaG9zdCJ9.x2CjJgPyKzJtF1ck6AGN1mPaLs6yzDC1mbtDcarqKY0",
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAzMDAwNjIzLCJpYXQiOjE3MDI5OTAwMjMsImp0aSI6ImQ4ZDIwMTQ2NmM1NzQ3M2ZhODM4ZDMxMDQ1MjY5YWEwIiwidXNlcl9pZCI6OSwidXNlcm5hbWUiOm51bGwsInJvbGUiOiJBRE1JTklTVFJBVE9SIiwicm9sZV9kaXNwbGF5IjoiQWRtaW5pc3RyYXRvciIsImVtYWlsIjoiYWRtaW5AbG9jYWxob3N0In0.7iLHlpS0IpnQPiG25pcQb2X39TM_CuoxvGeI18YVn5o"
}
```
In case the credentials are invalid, the server returns a status code of `401 Unauthorized` and the following response body:
```json
{
  "detail": "No active account found with the given credentials"
}
```
When the request is malformed (e.g. the property `"email"` is missing), the server responds with a status of `400 Bad Request`.

## Rate limiting
To prevent bad actors from brute forcing the application login rate limiting has been implemented for its endpoints.
Login attempts can be rate limited by IP address and username. The respective environment variables can be set in the .env File: `LOGIN_USER_THROTTLE_RATE` and `LOGIN_IP_THROTTLE_RATE`.

## Authenticating with the API
Access to a protected API endpoint requires authentication using a previously obtained access token. This requires adding an `Authorization` HTTP header to the request. This header contains the word `Bearer` followed by a space and the access token, like this: 
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAzMDAwNjIzLCJpYXQiOjE3MDI5OTAwMjMsImp0aSI6ImQ4ZDIwMTQ2NmM1NzQ3M2ZhODM4ZDMxMDQ1MjY5YWEwIiwidXNlcl9pZCI6OSwidXNlcm5hbWUiOm51bGwsInJvbGUiOiJBRE1JTklTVFJBVE9SIiwicm9sZV9kaXNwbGF5IjoiQWRtaW5pc3RyYXRvciIsImVtYWlsIjoiYWRtaW5AbG9jYWxob3N0In0.7iLHlpS0IpnQPiG25pcQb2X39TM_CuoxvGeI18YVn5o
```
If the authorization header is missing or not set correctly on a protected API endpoint, the server will return a status code of `401 Unauthorized`:
```json
{
  "detail": "Authentication credentials were not provided."
}
```
If the token is invalid or expired, the server will return a status code of `401 Unauthorized` with the following response:
```json
{
  "detail": "Given token not valid for any token type",
  "code": "token_not_valid",
  "messages": [
    {
      "token_class": "AccessToken",
      "token_type": "access",
      "message": "Token is invalid or expired"
    }
  ]
}
```
## Refreshing tokens
Access tokens have a lifespan of 60 minutes, which is why they need to be refreshed once they are expired. For this, the API provides a POST endpoint located at `/users/login/refresh`. Sending a request containing a valid refresh token...
```json
{
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMzA3NjQyMywiaWF0IjoxNzAyOTkwMDIzLCJqdGkiOiI4ZTRlMjA2MWIyM2Y0OGQ0YmViZTY0MTVhODc5MmIwMSIsInVzZXJfaWQiOjksInVzZXJuYW1lIjpudWxsLCJyb2xlIjoiQURNSU5JU1RSQVRPUiIsInJvbGVfZGlzcGxheSI6IkFkbWluaXN0cmF0b3IiLCJlbWFpbCI6ImFkbWluQGxvY2FsaG9zdCJ9.oKaRcyVVoN7dJzEMJ4mKBSsqJKLQe7DpDP1DXhqOqYc"
}
```
... returns a new access token along with a new refresh token from the API:
```json
{
  "access": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzAzMDAwNjIzLCJpYXQiOjE3MDI5OTAwMjMsImp0aSI6ImQ4ZDIwMTQ2NmM1NzQ3M2ZhODM4ZDMxMDQ1MjY5YWEwIiwidXNlcl9pZCI6OSwidXNlcm5hbWUiOm51bGwsInJvbGUiOiJBRE1JTklTVFJBVE9SIiwicm9sZV9kaXNwbGF5IjoiQWRtaW5pc3RyYXRvciIsImVtYWlsIjoiYWRtaW5AbG9jYWxob3N0In0.7iLHlpS0IpnQPiG25pcQb2X39TM_CuoxvGeI18YVn5o",
  "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcwMzA4NjcyMywiaWF0IjoxNzAzMDAwMzIzLCJqdGkiOiJmYzM0ODY5ODZhNjM0ZGMwOTU4ZTljN2Q5MDdmY2ZlNiIsInVzZXJfaWQiOjksInVzZXJuYW1lIjpudWxsLCJyb2xlIjoiQURNSU5JU1RSQVRPUiIsInJvbGVfZGlzcGxheSI6IkFkbWluaXN0cmF0b3IiLCJlbWFpbCI6ImFkbWluQGxvY2FsaG9zdCJ9.x2CjJgPyKzJtF1ck6AGN1mPaLs6yzDC1mbtDcarqKY0"
}
```
Since the access token might be invalid, the refresh request does not need to contain an Authorization header.

Be aware that once a refresh token has been used, the old refresh token is being blacklisted and cannot be used to obtain a new access token again.

## Logging out
To log out, there is a POST endpoint located at `/users/logout` which expects a refresh token. This endpoint blacklists the refresh token and thus prevents it from being used to obtain a new access token. Sending a POST request containing a valid and not already blacklisted refresh token...
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4OTA4OTMyMywiaWF0IjoxNjg5MDAyOTIzLCJqdGkiOiI5NjExZTUzYjZjYmQ0ODY5YTdjMmMwYjVkODc0YjhjOCIsInVzZXJfaWQiOjEsInVzZXJuYW1lIjoic2ltb24iLCJyb2xlIjoiQURNSU5JU1RSQVRPUiIsImVtYWlsIjoic2ltb24ubHVkd2lnQGhzLWR1ZXNzZWxkb3JmLmRlIn0.ENEJ4m_RQNusdFPxlGYyAVPwTgRxNHxAam5dfjL0rME"
}
```
... results in a status code of `200 OK` and an empty response body.

This endpoint does not expect an Authorization header.

## Token structure and claims
JWTs have three distinct parts separated by a dot (**.**): a **header** which contains information about the token type (for TURTL, this value should always be JWT) and the signature algorithm being used, a **payload** containing the token claims (for more information, see below) and a **signature** used to verify the token. The header and payload are Base64Url encoded. 

An example would be this token: 
```
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4OTA4OTMyMywiaWF0IjoxNjg5MDAyOTIzLCJqdGkiOiI5NjExZTUzYjZjYmQ0ODY5YTdjMmMwYjVkODc0YjhjOCIsInVzZXJfaWQiOjEsInVzZXJuYW1lIjoic2ltb24iLCJyb2xlIjoiQURNSU5JU1RSQVRPUiIsImVtYWlsIjoic2ltb24ubHVkd2lnQGhzLWR1ZXNzZWxkb3JmLmRlIn0.ENEJ4m_RQNusdFPxlGYyAVPwTgRxNHxAam5dfjL0rME
```
### Token claims
Claims are information about an entity (like a user) and additional data. The claims are contained in the payload section of a token. If you use a Base64 decoder to decode the payload (the middle part) of the example token above, you get the following:
```json
{
  "token_type":"access",
  "exp":1703000623,
  "iat":1702990023,
  "jti":"d8d201466c57473fa838d31045269aa0",
  "user_id":9,
  "username":null,
  "role":"ADMINISTRATOR",
  "role_display":"Administrator",
  "email":"admin@localhost"
}
```
#### Description of the token claims
Below is a description of every claim that is contained in the tokens the TURTL API issues.

| Property name | Data type | Description | See |
| ------ | ------ | ------ | ------ |
| `token_type` | String | Either `"access"` or `"refresh"` |  |
| `exp` | Number | A timestamp when the token will expire. | [RFC 7519, Section 4.1.4](https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.4) |
| `iat` | Number | A timestamp when the token was issued. | [RFC 7519, Section 4.1.6](https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.6) |
| `jti` | Number | A unique identifier for the JWT. | [RFC 7519, Section 4.1.7](https://datatracker.ietf.org/doc/html/rfc7519#section-4.1.7) |
| `user_id` | Number | The ID of the user this token belongs to | |
| `username` | String or null | The username of the user this token belongs to | |
| `role` | String | The role of the user this token belongs to. Can be either `"ADMINISTRATOR"`, `"INSTRUCTOR"` or `"STUDENT"`. | |
| `role_display` | String | A display-friendly representation of the role of the user this token belongs to. | |
| `email` | String | The email address of the user this token belongs to | |

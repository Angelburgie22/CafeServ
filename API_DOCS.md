# CafeServ API Documentation

## Standard request protocol

1. Send the request to the HTTP server. If the method is `POST`, the parameters
   must be sent as a JSON object. If it is `GET`, parameters are sent as indicated.
   Routes are usually under `/api/`.

2. The server validates the request, processes it, and returns a response.

3. The client processes the response:

    - Check the HTTP status code. If the code is an error (400-599), the
      operation is considered invalid/failed.

    - If the code is OK (2xx), inspect the JSON object: if the `success` field is
      not true, the operation is considered failed.

4. The client acts on the response.

Every server response includes the `success` field, and when it is false, the
failure reason is provided in the `reason` field.

## API

### auth
User login endpoints.

Location:
`/api/auth/`

#### `/create`
Create a user session. Returns a login identifier.

Method:
`POST`

Arguments:
- `user`: Email or username.
- `passwd`: User password.
- `token`: CSRF token. Obtained from `/api/auth/get_login_token` (temporary and
    may change in the future).

Response:
- `identifier`: The type of identifier returned to confirm login. Currently the
    only valid value is `cookies`.

#### `/close`
Close an existing session.

Method:
`DELETE`

Arguments:
None

Response:
None

### menu
API for listing and searching dishes.

Location:
`/api/menu`

#### `/dish_info`
Returns information for the specified dish.

Method:
`GET`

Arguments:
The dish is specified through a subroute.
Example: `/api/menu/dish_info/72` (SUBJECT TO CHANGE; later the API may be
normalized to use JSON or HTTP query parameters).

Response:
- `id`: The dish id.
- `name`: The display name of the dish.
- `ingredients`: List of available ingredients/sides you can add to the order:
    - `id`: ingredient id.
    - `name`: ingredient name.

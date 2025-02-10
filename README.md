## Technology Stack

- ⚡ [**FastAPI**](https://fastapi.tiangolo.com) for the API.
    - 🧰 [SQLModel](https://sqlmodel.tiangolo.com) for the SQL database interactions (ORM).
    - 🔍 [Pydantic](https://docs.pydantic.dev), used by FastAPI, for the data validation and settings management.
    - 💾 [PostgreSQL](https://www.postgresql.org) as the SQL database.
- 🚀 [Flutterwave](https://flutterwave.com) for the payment API.

## Installation and Usage

You can just clone this repository.

### Create a Virtual Environment

Create a virtual environment inside the project.

```bash
python -m venv .venv
```

Activate the new virtual environment.

```bash
source .venv/bin/activate
```

### Install Packages

Install the project packages from `requirements.txt`.

```bash
pip install -r requirements.txt
```

### Create Database

Create the PostgreSQL database that the project will use.

### Configuration

Create a `.env` file inside the project and fill it with the Flutterwave API token and your database params.
Here's an example of the `.env` file content:

API_TOKEN=FLWSECK_TEST-SANDBOXDEMOKEY-X
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=root
DB_NAME=abjfintech

You can this token `FLWSECK_TEST-SANDBOXDEMOKEY-X` for the Flutterwave API sandbox.

### Run program

```bash
fastapi dev main.py
```

Now go to `http://127.0.0.1:8000/docs`.

You will see the automatic interactive API documentation (provided by Swagger UI).

### Endpoints

#### Initiate Payment

`POST` `{base_url}`/payments/initiate

**Request body**

```json
{
  "tx_ref": "string",
  "phone": "string",
  "amount": 0,
  "currency": "string",
  "email": "string",
  "country": "string"
}
```

- `tx_ref`: Unique reference to identify the payment.
- `phone`: Phone number linked to the customer's mobile money account. Starts with the country prefix e.g. 2250101020304.
- `amount`: Amount to be charged. N.B. Amount should not be less than 100.
- `currency`: The specified currency to charge in. (expected value: XAF or XOF).
- `email`: The email address of the customer.
- `country`: The country code of the francophone country making the mobile money payment. Possible values are CM (Cameroon), SN (Senegal), BF (Burkina Faso) and so on.

#### Verify Payment

`GET` `{base_url}`/payments/verify?transaction_id=`{transaction_id}`
# Python and React: Insurance Sample Application

### Github repo: sample-app-insurance-python

## Introduction
The Docusign Insurance Sample App written in Python 3.7 (server) and React (client). You can find a live instance running at [https://insurance.sampleapps.docusign.com/](https://insurance.sampleapps.docusign.com/).

The Insurance Sample App demonstrates the following:

1. Authentication with Docusign via [JSON Web Token (JWT) Grant](https://developers.docusign.com/platform/auth/jwt/)
2. **Submit a claim:** [Source](./app/api/requests.py)
   This example demonstrates an integration for submitting a claim. It allows you to pass data received from the user to fill in a document. It also adds the ability to attach additional information to the document.
   * The document, based on an HTML template, is combined with Docusign AutoPlace and attachment features.
   * The signing ceremony is implemented with embedded signing for a single signer.
   * The Docusign signing ceremony is initiated from your website.
   * Anchor text ([AutoPlace](https://developers.docusign.com/docs/esign-rest-api/esign101/concepts/tabs/auto-place/)) is used to position the signing fields in the document.
   * [Adding attachments](https://developers.docusign.com/docs/esign-rest-api/esign101/concepts/documents/attachments/) enables users to add additional information to the document.
3. **Renew an insurance policy.** [Source](./app/api/clickwrap.py)
   This example shows how to use the Click API to create a clickwrap programmatically, render it in your UI, and and then submit it. It also tracks the submission event and, just after submission, redirects the user to the final page.
   * [More information about Click API](https://developers.docusign.com/docs/click-api)
4. **Purchase a new insurance policy.** [Source](./app/api/requests.py)
   The example shows how to [request payment using Docusign](https://developers.docusign.com/docs/esign-rest-api/how-to/request-a-payment/). It's implemented using an HTML-based template with [payment tabs](https://developers.docusign.com/docs/esign-rest-api/esign101/concepts/tabs/payment/). The document also includes different tab types, such as [Formula](https://developers.docusign.com/docs/esign-rest-api/esign101/concepts/tabs/calculated-fields/) and
   [Checkbox](https://developers.docusign.com/docs/esign-rest-api/reference/envelopes/enveloperecipienttabs/).

   The document contains additional logic to calculate the total amount. At completion, the user is able to pay the calculated amount and get back to the original website.

   To use this example, [create a test payments gateway](#user-content-configuring-a-docusign-payments-gateway) for your developer account.

## Installation

### Prerequisites
* A Docusign Developer account (email and password) on [demo.docusign.net](https://demo.docusign.net). If you don't already have a developer account, create a [free account](https://go.docusign.com/sandbox/productshot/?elqCampaignId=16535).
* A Docusign integration key (a client ID) that is configured to use **JSON Web Token (JWT) Grant**.
   You will need the **integration key** itself and its **RSA key pair**. To use this application, you must add your application's **Redirect URI** to your integration key. This [**video**](https://www.youtube.com/watch?v=GgDqa7-L0yo) demonstrates how to create an integration key (client ID) for a user application like this example.
* [Python 3.7+](https://www.python.org/downloads/)
* The Python [venv](https://docs.python.org/3/library/venv.html#module-venv) module
* [Node.js](https://nodejs.org/) v10+

### Required environment variables

* **DS_CLIENT_ID** - The integration key is the same as the client ID
* **DS_CLIENT_SECRET** - Integration Secret Key
* **DS_IMPERSONATED_USER_GUID** - API account ID
* **DS_TARGET_ACCOUNT_ID** - Target account ID. Use FALSE to indicate the user's default
* **DS_PAYMENT_GATEWAY_ID** - Payment gateway ID (Only Stripe method supported)
* **DS_PAYMENT_GATEWAY_NAME** - Payment gateway name
* **DS_PAYMENT_GATEWAY_DISPLAY_NAME** - Payment gateway display name
* **CLICKWRAP_ID** - The ID of clickwrap with dynamic content properties
* **DS_PRIVATE_KEY** - Private key string, source or path; for instance: /app/id_rsa
* **REACT_APP_DS_RETURN_URL** - URL where the back end of the application is located (If you run it locally, use `http://localhost:3000`)
* **REACT_APP_API_BASE_URL** - URL where the front end of the application is located; will be used by Docusign to redirect back after signing ceremony (If you run it locally, use `http://localhost:5001/api`)
* **DS_AUTH_SERVER** - The Docusign authentication server (for testing purposes, use `https://account-d.docusign.com`)
* **REACT_APP_DS_DEMO_SERVER** - Link to the Docusign demo server (for testing purposes, use `https://demo.docusign.net`)
* **REACT_APP_DS_CLICKWRAP_URL** - Link to the hosted clickwrap client (for testing purposes, use `//demo.docusign.net/clickapi/sdk/latest/docusign-click.js`)

### Installation steps

**Manual**

1. Download or clone this repository to your workstation in a new folder named **sample-app-insurance-python**.
2. Navigate to that folder: **`cd sample-app-insurance-python`**
3. Install python packages: **`pip install -r requirements.txt`**
4. Install React dependencies using the [npm](https://www.npmjs.com/) package manager:  **npm install**
5. Update the **.env** file with the integration key and other settings.
    > **Note:** Protect your integration key and client secret. You should make sure that the **.env** file will not be stored in your source code repository.
6. Navigate to [the admin demo Apps and Keys page](https://admindemo.docusign.com/authenticate?goTo=appsAndKeys), add the Redirect URI http://localhost:3000/callback and then hit save

    > **Note:** You should add a dynamic content properties to your clickwrap by following this [instruction](https://developers.docusign.com/docs/click-api/click101/customize-elastic-template-fields/) before using it in the sample app.

**Using installation scripts**

1. Download or clone this repository to your workstation in a new folder named **sample-app-insurance-python**.
2. Navigate to the scripts subfolder:**`cd sample-app-insurance-python/scripts`**
3. Run the installation script: **`./install.sh`** (`./install.bat` for Windows)
4. Update the **.env** file with the integration key and other settings.
    > **Note:** Protect your integration key and client secret. You should make sure that the **.env** file will not be stored in your source code repository.
5. Navigate to [the admin demo Apps and Keys page](https://admindemo.docusign.com/authenticate?goTo=appsAndKeys), add the Redirect URI http://localhost:3000/callback and then hit save

### Additional installation scripts
All installation scripts are located in the **scripts** folder.
1. To stop the application, run **`./stop.sh`**
1. To remove the virtual environment and modules, run **`./clean.sh`**

## Running the Insurance Sample App

### Manual

1. Navigate to the application folder: **`cd sample-app-insurance-python`**
2. Run the application: **`flask run --port 5001`**
3. Run npm: **`npm start`**
4. Open a browser to **http://localhost:3000**

### Using installation scripts

All installation scripts are located in the **scripts** folder.
1. Navigate to the scripts subfolder: **`cd scripts`**
2. Run the application script: **`./run.sh`**
3. Open a browser to **http://localhost:3000**

### Configuring a Docusign payments gateway
Docusign offers built-in connections to multiple payment gateways. The payments example in this sample app uses a demo account for the Stripe gateway service.

To create the payments gateway account:

1. Log in to your [developer account](https://appdemo.docusign.com/) and select Admin.
2. On the Integrations/Payments screen, click Stripe.
3. For development, you can skip the Stripe account application by using the `Skip this account form` on the top of the page.
  The Admin Panel will show that an enabled Stripe payment gateway account has been associated with your Docusign developer account.
5. Configure the example launcher with the gateway account ID shown in the Admin panel.
6. Add the payment gateway account ID to the **.env** file.

## Additional documentation
* [Managing Payment Gateways](https://support.docusign.com/en/guides/managing-payment-gateways)
* [Credit card numbers for testing](https://stripe.com/docs/testing)

## License information
This repository uses the MIT License. See the [LICENSE](./LICENSE) file for more information.

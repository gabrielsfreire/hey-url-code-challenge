# HeyURL! Code Challenge (Django)

This repository has been created as a code challenge for candidates with
FullStack Labs. The candidate will clone and setup an existing Django
application. The application will contain routes, migrations, models, and
minimal views but with no actual functionality created. The candidate will show
all her/his expertise building apps with the Django framework and problem
solving skills.

## Overview

HeyURL! is a service to create awesome friendly URLs to make it easier for
people to remember. Our team developed some mockup views but don't have our
awesome functionality in place yet.

## Requirements

- Implement actions to create shorter URLs based on a given full URL
- If URL is not valid, the application returns an error message to the user
- We want to be able to provide click metrics to our users for each URL in the
system. Every time that someone clicks a short URL, it should record that click
and also user platform and browser using the user agent request header
- We want to create a metrics panel for the user to view the stats for every
short URL. The user should be able to see total clicks per day on the current
month along with a breakdown of browsers and platforms
- If someone tries to visit a invalid short URL then it should return a custom
404 page
- Unit Tests should be created which cover the code that is added as applicable

### Short URL Format

- Max length 5 character e.g. `NELNT`
- Allows upper and lower case characters
- Allows numbers
- Any non letter or number characters are not allowed, including whitespace
- `original_url` and `short_url` must be unique
- Original URL format should be validated

## Getting Started

1. Ensure your environment is setup to run Python3 and you have Django installed
2. Clone this repository
3. Install dependencies listed in `requirements.txt`
4. Run database migrations
5. Load default data
6. Run development server

## Notes

### Pages

The following pages have already been created with general boiler-plate to get
you started:

- `GET /` This page lists the current URLs in the system along with a form to
create a new URL
- `POST /store` Skeleton in place to accept the posting of the create URL form
- `GET /u/<short_url>` Skeleton in place to track a click event of a short URL

### User Agent Package

Use the `django-user-agents` (https://github.com/selwin/django-user_agents)
package, which has been pulled in for you, to pull in the visiting user's
browser and user agent for saving when invoking the click method of a shortened
URL.

## Bonus

As an additional requirement if you run through all of the above, the HeyURL!
app requires an API endpoint to retrieve the ten (10) latest URLs submitted. It
should be a JSON API compliant endpoint. Here is an example of what the response
should look like:

```json
{
  "data": [
    {
      "type": "urls",
      "id": "1",
      "attributes": {
        "created-at": "2018-08-15T02:48:08.642Z",
        "original-url": "http://www.fullstacklabs.com",
        "url": "https://app-domain/a",
        "clicks": 1000000
      },
      "relationships": {
        "metrics": {
          "data": [
            {
              "id": 1,
              "type": "metrics"
            }
          ]
        }
      }
    }
  ],
  "included": []
}
```
